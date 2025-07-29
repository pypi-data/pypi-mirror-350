#
# Copyright 2018 Joachim Lusiardi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import json
from json.decoder import JSONDecodeError
import logging
import random
import uuid
import re
import tlv8

from homekit.exceptions import AccessoryNotFoundError, ConfigLoadingError, UnknownError, \
    AuthenticationError, ConfigSavingError, AlreadyPairedError, TransportNotSupportedError, MalformedPinError
from homekit.protocol import States, Methods, Errors, TlvTypes
from homekit.http_impl import HomeKitHTTPConnection
from homekit.protocol.statuscodes import HapStatusCodes
from homekit.protocol import perform_pair_setup_part1, perform_pair_setup_part2, create_ip_pair_setup_write
from homekit.model.services.service_types import ServicesTypes
from homekit.model.characteristics.characteristic_types import CharacteristicsTypes
from homekit.protocol.opcodes import HapBleOpCodes
from homekit.controller.tools import NotSupportedPairing
from homekit.controller.additional_pairing import AdditionalPairing

from homekit.zeroconf_impl import discover_homekit_devices, find_device_ip_and_port
from homekit.controller.ip_implementation import IpPairing, IpSession


class Controller(object):
    """
    This class represents a HomeKit controller (normally your iPhone or iPad).
    """

    def __init__(self):
        """
        Initialize an empty controller. Use 'load_data()' to load the pairing data.

        """
        self.pairings = {}
        self.logger = logging.getLogger('homekit.controller.Controller')

    @staticmethod
    def discover(max_seconds=10):
        """
        Perform a Bonjour discovery for HomeKit accessory. The discovery will last for the given amount of seconds. The
        result will be a list of dicts. The keys of the dicts are:
         * name: the Bonjour name of the HomeKit accessory (i.e. Testsensor1._hap._tcp.local.)
         * address: the IP address of the accessory
         * port: the used port
         * c#: the configuration number (required)
         * ff / flags: the numerical and human readable version of the feature flags (supports pairing or not, see table
                       5-8 page 69)
         * id: the accessory's pairing id (required)
         * md: the model name of the accessory (required)
         * pv: the protocol version
         * s#: the current state number (required)
         * sf / statusflags: the status flag (see table 5-9 page 70)
         * ci / category: the category identifier in numerical and human readable form. For more information see table
                        12-3 page 254 or homekit.Categories (required)

        IMPORTANT:
        This method will ignore all HomeKit accessories that exist in _hap._tcp domain but fail to have all required
        TXT record keys set.

        :param max_seconds: how long should the Bonjour service browser do the discovery (default 10s). See sleep for
                            more details
        :return: a list of dicts as described above
        """
        return discover_homekit_devices(max_seconds)

    @staticmethod
    def identify(accessory_id):
        """
        This call can be used to trigger the identification of an accessory, that was not yet paired. A successful call
        should cause the accessory to perform some specific action by which it can be distinguished from others (blink a
        LED for example).

        It uses the /identify url as described on page 88 of the spec.

        :param accessory_id: the accessory's pairing id (e.g. retrieved via discover)
        :raises AccessoryNotFoundError: if the accessory could not be looked up via Bonjour
        :raises AlreadyPairedError: if the accessory is already paired
        """
        connection_data = find_device_ip_and_port(accessory_id)
        if connection_data is None:
            raise AccessoryNotFoundError('Cannot find accessory with id "{i}".'.format(i=accessory_id))

        conn = HomeKitHTTPConnection(connection_data['ip'], port=connection_data['port'])
        conn.request('POST', '/identify')
        resp = conn.getresponse()

        # spec says status code 400 on any error (page 88). It also says status should be -70401 (which is "Request
        # denied due to insufficient privileges." table 5-12 page 80) but this sounds odd.
        if resp.code == 400:
            data = json.loads(resp.read().decode())
            code = data['status']
            conn.close()
            raise AlreadyPairedError(
                'identify failed because: {reason} ({code}).'.format(reason=HapStatusCodes[code],
                                                                     code=code))
        conn.close()

    def shutdown(self):
        """
        Shuts down the controller by closing all connections that might be held open by the pairings of the controller.
        """
        for p in self.pairings:
            self.pairings[p].close()

    def get_pairings(self):
        """
        Returns a dict containing all pairings known to the controller.

        :return: the dict maps the aliases to Pairing objects
        """
        return self.pairings

    def load_data(self, filename):
        """
        Loads the pairing data of the controller from a file. If the connection type of a pairing is currently not
        supported by the python environment (e.g. because of missing modules for BLE), an instance of
        `NotSupportedPairing` is used. By this no pairings are lost during a `load_data`/`save_data` cycle.

        :param filename: the file name of the pairing data
        :raises ConfigLoadingError: if the config could not be loaded. The reason is given in the message.
        :raises TransportNotSupportedError: if the dependencies for the selected transport are not installed
        """
        try:
            with open(filename, 'r') as input_fp:
                data = json.load(input_fp)
                for pairing_id in data:
                    if 'Connection' not in data[pairing_id]:
                        # This is a pre BLE entry in the file with the pairing data, hence it is for an IP based
                        # accessory. So we set the connection type (in case save data is used everything will be fine)
                        # and also issue a warning
                        data[pairing_id]['Connection'] = 'IP'
                        self.logger.warning(
                            'Loaded pairing for %s with missing connection type. Assume this is IP based.', pairing_id)

                    if data[pairing_id]['Connection'] == 'IP':
                        self.pairings[pairing_id] = IpPairing(data[pairing_id])
                    elif data[pairing_id]['Connection'] == 'ADDITIONAL_PAIRING':
                        self.pairings[pairing_id] = AdditionalPairing(data[pairing_id])
                    else:
                        # ignore anything else, issue warning
                        self.logger.warning('could not load pairing %s of type "%s"', pairing_id,
                                            data[pairing_id]['Connection'])
        except PermissionError:
            raise ConfigLoadingError('Could not open "{f}" due to missing permissions'.format(f=filename))
        except JSONDecodeError:
            raise ConfigLoadingError('Cannot parse "{f}" as JSON file'.format(f=filename))
        except FileNotFoundError:
            raise ConfigLoadingError('Could not open "{f}" because it does not exist'.format(f=filename))

    def save_data(self, filename):
        """
        Saves the pairing data of the controller to a file.

        :param filename: the file name of the pairing data
        :raises ConfigSavingError: if the config could not be saved. The reason is given in the message.
        """
        data = {}
        for pairing_id in self.pairings:
            # package visibility like in java would be nice here
            data[pairing_id] = self.pairings[pairing_id]._get_pairing_data()
        try:
            with open(filename, 'w') as output_fp:
                json.dump(data, output_fp, indent='  ')
        except PermissionError:
            raise ConfigSavingError('Could not write "{f}" due to missing permissions'.format(f=filename))
        except FileNotFoundError:
            raise ConfigSavingError(
                'Could not write "{f}" because it (or the folder) does not exist'.format(f=filename))

    @staticmethod
    def check_pin_format(pin):
        """
        Checks the format of the given pin: XXX-XX-XXX with X being a digit from 0 to 9

        :raises MalformedPinError: if the validation fails
        """
        if not re.match(r'^\d\d\d-\d\d-\d\d\d$', pin):
            raise MalformedPinError('The pin must be of the following XXX-XX-XXX where X is a digit between 0 and 9.')

    def perform_pairing(self, alias, accessory_id, pin):
        """
        This performs a pairing attempt with the IP accessory identified by its id.

        Accessories can be found via the discover method. The id field is the accessory's id for the second parameter.

        The required pin is either printed on the accessory or displayed. Must be a string of the form 'XXX-YY-ZZZ'.

        Important: no automatic saving of the pairing data is performed. If you don't do this, the information is lost
            and you have to reset the accessory!

        :param alias: the alias for the accessory in the controllers data
        :param accessory_id: the accessory's id
        :param pin: function to return the accessory's pin
        :raises AccessoryNotFoundError: if no accessory with the given id can be found
        :raises AlreadyPairedError: if the alias was already used
        :raises UnavailableError: if the device is already paired
        :raises MaxTriesError: if the device received more than 100 unsuccessful attempts
        :raises BusyError: if a parallel pairing is ongoing
        :raises AuthenticationError: if the verification of the device's SRP proof fails
        :raises MaxPeersError: if the device cannot accept an additional pairing
        :raises UnavailableError: on wrong pin
        :raises MalformedPinError: if the pin is malformed
        """
        Controller.check_pin_format(pin)
        finish_pairing = self.start_pairing(alias, accessory_id)
        return finish_pairing(pin)

    def start_pairing(self, alias, accessory_id):
        """
        This starts a pairing attempt with the IP accessory identified by its id.
        It returns a callable (finish_pairing) which you must call with the pairing pin.

        Accessories can be found via the discover method. The id field is the accessory's id for the second parameter.

        The required pin is either printed on the accessory or displayed. Must be a string of the form 'XXX-YY-ZZZ'. If
        this format is not used, a MalformedPinError is raised.

        Important: no automatic saving of the pairing data is performed. If you don't do this, the information is lost
            and you have to reset the accessory!

        :param alias: the alias for the accessory in the controllers data
        :param accessory_id: the accessory's id
        :param pin: function to return the accessory's pin
        :raises AccessoryNotFoundError: if no accessory with the given id can be found
        :raises AlreadyPairedError: if the alias was already used
        :raises UnavailableError: if the device is already paired
        :raises MaxTriesError: if the device received more than 100 unsuccessful attempts
        :raises BusyError: if a parallel pairing is ongoing
        :raises AuthenticationError: if the verification of the device's SRP proof fails
        :raises MaxPeersError: if the device cannot accept an additional pairing
        :raises UnavailableError: on wrong pin
        """
        if alias in self.pairings:
            raise AlreadyPairedError('Alias "{a}" is already paired.'.format(a=alias))

        connection_data = find_device_ip_and_port(accessory_id)
        if connection_data is None:
            raise AccessoryNotFoundError('Cannot find accessory with id "{i}".'.format(i=accessory_id))
        conn = HomeKitHTTPConnection(connection_data['ip'], port=connection_data['port'])

        try:
            write_fun = create_ip_pair_setup_write(conn)

            state_machine = perform_pair_setup_part1()
            request, expected = state_machine.send(None)
            while True:
                try:
                    response = write_fun(request, expected)
                    request, expected = state_machine.send(response)
                except StopIteration as result:
                    salt, pub_key = result.value
                    break

        except Exception:
            conn.close()
            raise

        def finish_pairing(pin):
            Controller.check_pin_format(pin)
            try:
                state_machine = perform_pair_setup_part2(pin, str(uuid.uuid4()), salt, pub_key)
                request, expected = state_machine.send(None)
                while True:
                    try:
                        response = write_fun(request, expected)
                        request, expected = state_machine.send(response)
                    except StopIteration as result:
                        pairing = result.value
                        break
            finally:
                conn.close()

            pairing['AccessoryIP'] = connection_data['ip']
            pairing['AccessoryPort'] = connection_data['port']
            pairing['Connection'] = 'IP'
            self.pairings[alias] = IpPairing(pairing)

        return finish_pairing

    def perform_pairing_ble(self, alias, accessory_mac, pin, adapter='hci0'):
        """
        This performs a pairing attempt with the Bluetooth LE accessory identified by its mac address.

        Accessories can be found via the discover method. The mac field is the accessory's mac for the second parameter.

        The required pin is either printed on the accessory or displayed. Must be a string of the form 'XXX-YY-ZZZ'. If
        this format is not used, a MalformedPinError is raised.

        Important: no automatic saving of the pairing data is performed. If you don't do this, the information is lost
            and you have to reset the accessory!

        :param alias: the alias for the accessory in the controllers data
        :param accessory_mac: the accessory's mac address
        :param pin: function to return the accessory's pin
        :param adapter: the bluetooth adapter to be used (defaults to hci0)
        :raises MalformedPinError: if the pin is malformed
        # TODO add raised exceptions
        """
        Controller.check_pin_format(pin)
        finish_pairing = self.start_pairing_ble(alias, accessory_mac, adapter)
        return finish_pairing(pin)

    def remove_pairing(self, alias, pairingId=None):
        """
        Remove a pairing between the controller and the accessory. The pairing data is delete on both ends, on the
        accessory and the controller.

        Important: no automatic saving of the pairing data is performed. If you don't do this, the accessory seems still
            to be paired on the next start of the application.

        :param alias: the controller's alias for the accessory
        :param pairingId: the pairing id to be removed
        :raises AuthenticationError: if the controller isn't authenticated to the accessory.
        :raises AccessoryNotFoundError: if the device can not be found via zeroconf
        :raises UnknownError: on unknown errors
        """
        # package visibility like in java would be nice here
        pairing_data = self.pairings[alias]._get_pairing_data()
        connection_type = pairing_data['Connection']
        if not pairingId:
            pairingIdToDelete = pairing_data['iOSPairingId']
        else:
            pairingIdToDelete = pairingId

        # Prepare the common (for IP and BLE) request data
        request_tlv = tlv8.encode([
            tlv8.Entry(TlvTypes.State, States.M1),
            tlv8.Entry(TlvTypes.Method, Methods.RemovePairing),
            tlv8.Entry(TlvTypes.Identifier, pairingIdToDelete.encode())
        ])

        if connection_type == 'IP':
            session = IpSession(pairing_data)
            response = session.post('/pairings', request_tlv, content_type='application/pairing+tlv8')
            session.close()
            data = response.read()
            data = tlv8.decode(data, {
                TlvTypes.State: tlv8.DataType.INTEGER,
                TlvTypes.Error: tlv8.DataType.INTEGER

            })
        elif connection_type == 'BLE':
            raise Exception('not implemented (not IP)')

        # act upon the response
        # handle the result, spec says, if it has only one entry with state == M2 we unpaired, else its an error.
        logging.debug('response data: %s', tlv8.format_string(data))
        state = data.first_by_id(TlvTypes.State).data
        if len(data) == 1 and state == States.M2:
            if not pairingId:
                del self.pairings[alias]
        else:
            error = data.first_by_id(TlvTypes.Error)
            if error and error.data == Errors.Authentication:
                raise AuthenticationError('Remove pairing failed: missing authentication')
            else:
                raise UnknownError('Remove pairing failed: unknown error')
