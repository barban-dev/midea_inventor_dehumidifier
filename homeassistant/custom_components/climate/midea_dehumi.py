"""
Support for EVA II PRO WiFi Smart Dehumidifier appliance by Midea/Inventor.

This sub-component creates a climate device for EVA II PRO WiFi Smart Dehumidifier

For more details please refer to the documentation at 
https://home-assistant.io/components/climate.midea-dehumi/

The third-party Python3 library able to interface with the dehumidificator appliance is:
https://github.com/barban-dev/midea_inventor_dehumidifier
"""
VERSION = '0.9.9'

import logging
from custom_components.midea_dehumi import DOMAIN, MIDEA_API_CLIENT, MIDEA_TARGET_DEVICE
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD, DEVICE_CLASS_HUMIDITY, TEMP_CELSIUS

from homeassistant.components.climate import (
    ClimateDevice, ATTR_CURRENT_HUMIDITY, ATTR_HUMIDITY, ATTR_MIN_HUMIDITY, ATTR_MAX_HUMIDITY,
	SUPPORT_TARGET_HUMIDITY, SUPPORT_TARGET_HUMIDITY_LOW, SUPPORT_TARGET_HUMIDITY_HIGH,
    SUPPORT_FAN_MODE, SUPPORT_OPERATION_MODE, SUPPORT_ON_OFF,
    ATTR_FAN_MODE, ATTR_FAN_LIST, ATTR_OPERATION_MODE, ATTR_OPERATION_LIST,
    PLATFORM_SCHEMA)


_LOGGER = logging.getLogger(__name__)

SUPPORT_FLAGS =  SUPPORT_TARGET_HUMIDITY | SUPPORT_TARGET_HUMIDITY_LOW | SUPPORT_TARGET_HUMIDITY_HIGH | SUPPORT_FAN_MODE | SUPPORT_OPERATION_MODE | SUPPORT_ON_OFF

ATTR_DEHUMI_ION = "dehumi_ion"
ATTR_DEHUMI_MODE = "dehumi_mode"
ATTR_DEHUMI_FAN_SPEED = "dehumi_fan_speed"

#TODO: gestire questo range da midea client (ora c'è il range 30-70 hard-coded!!!!!)
#MIN_HUMITIDY = 30	#da qualche parte (forse nella libreria) è deciso che il valore minimo non può essere < 35
MIN_HUMITIDY = 35
MAX_HUMITIDY = 70

DEHUMI_OPERATION_DICT = { 'target_mode-ion_on' : 1, 'continuos_mode-ion_on' : 2, 'smart_mode-ion_on' : 3, 'dryer_mode-ion_on' : 4, 'target_mode-ion_off' : 5, 'continuos_mode-ion_off' : 6, 'smart_mode-ion_off' : 7, 'dryer_mode-ion_off' : 8 }
DEHUMI_OPERATION_LIST = [ 'target_mode-ion_on', 'continuos_mode-ion_on', 'smart_mode-ion_on', 'dryer_mode-ion_on', 'target_mode-ion_off', 'continuos_mode-ion_off', 'smart_mode-ion_off', 'dryer_mode-ion_off' ]

DEHUMI_FAN_SPEED_DICT = { 'SILENT' : 40, 'MEDIUM' : 60, 'HIGH' : 80 }
DEHUMI_FAN_SPEED_LIST = [ 'SILENT', 'MEDIUM', 'HIGH' ]


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up Midea/Inventor dehumidificator climate platform based on config_entry."""
    _LOGGER.info("climate.midea_dehumi: initializing climate entity sub-component")
    _LOGGER.debug("climate.midea_dehumi: starting async_setup_platform")

    #ref: https://developers.home-assistant.io/docs/en/creating_component_generic_discovery.html
    client = hass.data[MIDEA_API_CLIENT]
    targetDevice = discovery_info[MIDEA_TARGET_DEVICE]
    _LOGGER.debug("climate.midea_dehumi: targetDevice = %s", targetDevice)

    if targetDevice is not None:
        #Create climate entity
        climate_entity = MideaDehumiDevice(hass, client, targetDevice)

		#Add climate entity
        async_add_entities([climate_entity])
        _LOGGER.info("climate.midea_dehumi: climate entity initialized.")
    else:
        _LOGGER.error("climate.midea_dehumi: error initializing climate entity.")



class MideaDehumiDevice(ClimateDevice):
    """Representation of a Midea/Inventor dehumidificator device."""

    def __init__(self, hass, client, targetDevice):
        _LOGGER.debug("midea-dehumi: initializing MideaDehumiDevice...")

        self._hass = hass
        self._supported_features = SUPPORT_FLAGS

        self._fan_dict = DEHUMI_FAN_SPEED_DICT
        self._operation_dict = DEHUMI_OPERATION_DICT

        self._fan_list = DEHUMI_FAN_SPEED_LIST
        self._operation_list = DEHUMI_OPERATION_LIST

        self._client = client
        self._device = targetDevice
        self._name = "midea_dehumi_"+targetDevice['id']
        self._unique_id = 'midea_dehumi_' + targetDevice['id']

        #Default values for device state
        self._powerMode = None			# 0:off, 1:on
        self._setMode = None			# (1:TARGET_MODE, 2:CONTINOUS_MODE, 3:SMART_MODE, 4:DRYER_MODE)
        self._ionSetSwitch = None      # 0:off, 1:on
        self._setOperationMode = None
        self._humidity = None			# current humidity
        self._humidity_set = None		# target hunidity
        self._humidity_dot = None		# current humidity (decimal)
        self._humidity_dot_set = None	# target humidity (decimal)
        self._windSpeed = None			# fan speed [0:100] (SILENT:40, MEDIUM:60, HIGH:80)
        self._windSpeedMode = None		# fan speed [0:100] (SILENT:40, MEDIUM:60, HIGH:80)
        self._isDisplay = None
        self._filterShow = False
        self._tankShow = False
        self._dryClothesSetSwitch = None
        self._upanddownSwing = None

        #Get appliance's status to set initial values for the device
        _LOGGER.debug("midea-client: querying appliance status via Web API...")
        res = self._client.get_device_status(self._device['id'])
        #res = await self._hass.async_add_executor_job(self._client.get_device_status(self._device['id']))
        if res == 1:
            _LOGGER.debug("climate.midea_dehumi: get_device_status suceeded: "+self._client.deviceStatus.toString())
            #Set initial values for device's status
            self.__refresh_device_status()
        else:
            _LOGGER.error("climate.midea_dehumi: get_device_status error")


    def __refresh_device_status(self):
        if self._client.deviceStatus is not None:
            self._powerMode = self._client.deviceStatus.powerMode
            
            self._ionSetSwitch = self._client.deviceStatus.ionSetSwitch
            self._setMode = self._client.deviceStatus.setMode
			
            #In the Midea dehumi appliance setMode (4-states) and ionSetSwitch (2-states) are independent: in MideaDehumiDevice these two modes are combined (8-states) to be managed together using ATTR_OPERATION_MODE
            if self._ionSetSwitch == 1:
                self._setOperationMode = self._setMode
            else:
                self._setOperationMode = self._setMode + 4

            self._windSpeed = self._client.deviceStatus.windSpeed
            if self._windSpeed == 40:
                self._windSpeedMode = self._fan_list[0]
            elif self._windSpeed == 60:
                self._windSpeedMode = self._fan_list[1]
            elif self._windSpeed == 80:
                self._windSpeedMode = self._fan_list[2]
            else:
                self._windSpeedMode = "unknown"

            self._humidity = self._client.deviceStatus.humidity
            self._humidity_set = self._client.deviceStatus.humidity_set
            self._humidity_dot = self._client.deviceStatus.humidity_dot
            self._humidity_dot_set = self._client.deviceStatus.humidity_dot_set
            self._isDisplay = self._client.deviceStatus.isDisplay
            self._filterShow = self._client.deviceStatus.filterShow
            self._tankShow = self._client.deviceStatus.tankShow
            self._dryClothesSetSwitch = self._client.deviceStatus.dryClothesSetSwitch
            self._upAndDownSwing = self._client.deviceStatus.upAndDownSwing


    # Climate entity assumes that ATTR_CURRENT_TEMPERATUR and ATTR_TEMPERATURE are always present: this method has to be reimplemented to avoid to have these attributes on the state of the cliamte entity
    # Unfortunately, it seems also that homeassistant's front-end assumes that these attributes are always present and try to graph it when the entity card is open (an invalid graph is shown in this case)
	# Ref. https://github.com/home-assistant/home-assistant-polymer/blob/dev/src/components/ha-climate-state.js
    """@property
    def state_attributes(self):
        #Return the optional device state attributes.
        data = {}

        #code from /climate/__init.py__
        if self.supported_features & SUPPORT_TARGET_HUMIDITY:
            data[ATTR_HUMIDITY] = self.target_humidity
            data[ATTR_CURRENT_HUMIDITY] = self.current_humidity

            if self.supported_features & SUPPORT_TARGET_HUMIDITY_LOW:
                data[ATTR_MIN_HUMIDITY] = self.min_humidity

            if self.supported_features & SUPPORT_TARGET_HUMIDITY_HIGH:
                data[ATTR_MAX_HUMIDITY] = self.max_humidity

        if self.supported_features & SUPPORT_FAN_MODE:
            data[ATTR_FAN_MODE] = self.current_fan_mode
            if self.fan_list:
                data[ATTR_FAN_LIST] = self.fan_list

        if self.supported_features & SUPPORT_OPERATION_MODE:
            data[ATTR_OPERATION_MODE] = self.current_operation
            if self.operation_list:
                data[ATTR_OPERATION_LIST] = self.operation_list


        if self._ionSetSwitch is not None:
            data[ATTR_DEHUMI_ION] = self._ionSetSwitch

        if self._setMode is not None:
            data[ATTR_DEHUMI_MODE] = self._setMode

        if self._windSpeed is not None:
            data[ATTR_DEHUMI_FAN_SPEED] = self._windSpeed

        _LOGGER.debug("state_attributes = %s", data)
        return data"""

    @property
    def unique_id(self):
        """Return the unique id."""
        return self._unique_id

    @property
    def name(self):
        """Return the name of the climate device. The Name is derived from the device id"""
        return self._name

    @property
    def device_class(self):
        """Return the class of this device, from component DEVICE_CLASSES."""
        return DEVICE_CLASS_HUMIDITY

    @property
    def should_poll(self):
        """Get appliance's status by polling it: Midea Web API lacks of notification capability"""
        return True

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return self._supported_features		

    @property
    def operation_list(self):
        """Return the list of available operation modes."""
        if not self.is_on:
            return None			#it is not possible to change operation mode when device is off
        return self._operation_list

    @property
    def fan_list(self):
        """Return the list of available fan modes."""
        if not self.is_on:
            return None							#it is not possible to change fan speed when device is off
        if self._setMode == 4:
            return [self._fan_list[2]]			# When in dryer mode, fan is fixed to 'HIGH'
  
        return self._fan_list

    @property
    def min_humidity(self):
        """Return the minimum target humidity."""
        return MIN_HUMITIDY

    @property
    def max_humidity(self):
        """Return the maximum target humidity."""
        return MAX_HUMITIDY
	
    """@property
    def ionSetSwitch(self):
        #Return the status (on/off) of ion.
        return self._ionSetSwitch"""
		
    @property
    def available(self):
        """Checks if the appliance is available for commands."""
        #_LOGGER.debug("midea-dehumi: available method called: onlineStatus=%s", self._device["onlineStatus"])
        if self._device["onlineStatus"] == "1":
            return True
        else:
            return False

    @property
    def is_on(self):
        """Return true if the device is on."""
        if self._powerMode == 1:
            return True

        return False

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return "%"

    @property
    def current_humidity(self):
        """Return the current humidity."""
        _LOGGER.debug("midea-dehumi: current_humidity called, humidity=%s", self._humidity)
        return self._humidity
        

    @property
    def target_humidity(self):
        """Return the target humidity."""
        #_LOGGER.debug("midea-dehumi: target_humidity called, humidity=%s", self._humidity_set)
        return self._humidity_set

    @property
    def current_operation(self):
        """Return current operation"""
        _LOGGER.debug("climate.midea_dehumi: current_operation called, mode_operation=%s, mode_operationStr=%s", self._setOperationMode, self._operation_list[self._setOperationMode - 1])
        return self._operation_list[self._setOperationMode - 1]

    @property
    def current_fan_mode(self):
        """Return the fan setting."""
        _LOGGER.debug("climate.midea_dehumi: current_fan_mode called, windSpeedMode=%s", self._windSpeedMode)
        return self._windSpeedMode


    async def async_update(self):
        """Retrieve latest state from the appliance"""
        _LOGGER.debug("async_update called.")
        _LOGGER.debug("access_token=%s", self._client.security.access_token)
        _LOGGER.debug("data_key=%s", self._client.security.data_key)

        if self._client.security.access_token:
            #Get apppliance's status using Web API
            res = self._client.get_device_status(self._device['id'])
            if res == 1:
                _LOGGER.info(self._client.deviceStatus.toString())
                #Update MideaDehumiDevice's status
                self.__refresh_device_status()
            else:
                _LOGGER.error("climate.midea_dehui: errog getting appliance's status via Web API.")


    async def async_set_humidity(self, **kwargs):
        """Set new value for target humidity."""
        _LOGGER.debug("async_set_humidity called.")
        humidity = int(kwargs.get(ATTR_HUMIDITY))
        _LOGGER.debug("humidity value to set = "+str(humidity))
        if self._humidity_set != humidity:
            _LOGGER.debug("midea-dehumi: setting new target hunidity value via Web API...")
            res = self._client.send_target_humidity_command(self._device["id"], humidity)
            if res is not None:
                _LOGGER.info("midea-dehumi: send_target_humidity_command succeeded: "+self._client.deviceStatus.toString())
                #Refresh device status
                self.__refresh_device_status()
            else:
                _LOGGER.error("climate.midea-dehumi: send_target_humidity_command ERROR")


    async def async_turn_on(self):
        """Turn on."""
        _LOGGER.debug("async_turn_on called.")
        if not self.is_on:
            _LOGGER.debug("midea-dehumi: sending power-on command via Web API...")
            res = self._client.send_poweron_command(self._device["id"])
            if res is not None:
                _LOGGER.debug("midea-dehumi: send_poweron_command suceeded: "+self._client.deviceStatus.toString())
                #Refresh device status
                self.__refresh_device_status()
            else:
                _LOGGER.error("climate.midea-dehumi: send_poweron_command ERROR.")


    async def async_turn_off(self):
        """Turn off."""
        _LOGGER.debug("async_turn_off called.")
        if self.is_on:
            _LOGGER.debug("midea-dehumi: sending power-off command via Web API...")
            res = self._client.send_poweroff_command(self._device["id"])
            if res is not None:
                _LOGGER.debug("midea-dehumi: send_poweroff_command suceeded: "+self._client.deviceStatus.toString())
                #Refresh device status
                self.__refresh_device_status()
            else:
                _LOGGER.error("climate.midea-dehumi: send_poweroff_command ERROR.")


    async def async_set_operation_mode(self, operation_mode):
        """Set new value for operation mode."""
        _LOGGER.debug("async_set_operation_mode called; current_mode=%s, new mode=%s", self._setOperationMode, operation_mode)
        
        if self.is_on:
            mode = self._operation_dict.get(operation_mode, 0)
            if mode and mode != self._setOperationMode:
                if mode > 4:
                    mode -= 4
                    ionSetSwitch = 0
                else:
                    ionSetSwitch = 1

                self._client.deviceStatus._setMode = mode
                self._client.deviceStatus._ionSetSwitch = ionSetSwitch

                _LOGGER.debug("midea-dehumi: sending update status command via Web API...")
                #TODO: usare wait async....
                res = self._client.send_update_status_command(self._device["id"], self._client.deviceStatus)
                if res is not None:
                    _LOGGER.debug("midea-dehumi: send_update_status_command suceeded: "+self._client.deviceStatus.toString())
                    #Refresh device status
                    self.__refresh_device_status()
                else:
                    _LOGGER.error("climate.midea-dehumi: send_update_status_command ERROR.")


    async def async_set_fan_mode(self, fan_mode):
        """Set new fan speed mode"""
        _LOGGER.debug("async_set_fan_mode called; mode=%s", fan_mode)

        if not self.is_on:
            _LOGGER.warning("midea-dehumi: cannot set fan mode when device is off.")
            return
        if self._setMode == 4:
            _LOGGER.warning("climate.midea-dehumi: cannot set fan mode when device is in dryer mode (fan is fixed to HIGH).")
            return

        speed = self._fan_dict.get(fan_mode, 0)
        if speed and speed != self._windSpeed:
            self._windSpeedMode = fan_mode

            _LOGGER.debug("midea-dehumi: sending speed mode command via Web API...")
            res = self._client.send_fan_speed_command(self._device["id"], speed)
            if res is not None:
                _LOGGER.debug("midea-dehumi: send_fan_speed_command suceeded: "+self._client.deviceStatus.toString())
                #Refresh device status
                self.__refresh_device_status()
            else:
                _LOGGER.error("climate.midea-dehumi: send_fan_speed_command ERROR.")


#
# Temperature-related methods. 
# At the moment, temperature related attributes are kept in the state of device and set equal to the huidity ones in order to display a correct graph in the entity card.
# I know, this is a ugly work-around....
#
    @property
    def current_temperature(self):
        """Return the current temperature."""
        #return None
        return self._humidity

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        #return None
        return self._humidity_set

    @property
    def temperature_unit(self):
        #Return the unit of measurement.
        return TEMP_CELSIUS #Avoid NotImplementedError raised by climate/__init__.py", line 293

    @property
    def min_temp(self):
        """Return the minimum temperature."""
        return MIN_HUMITIDY

    @property
    def max_temp(self):
        """Return the minimum temperature."""
        return MAX_HUMITIDY
