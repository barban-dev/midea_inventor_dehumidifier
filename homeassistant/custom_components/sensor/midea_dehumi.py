"""
Support for EVA II PRO WiFi Smart Dehumidifier appliance by Midea/Inventor.

Midea-dehumi component to create current & target humidity sensors binded with the EVA II PRO WiFi Smart Dehumidifier climate device.
For more details please refer to the documentation at 
https://home-assistant.io/components/sensor.midea-dehumi/

The third-party Python3 library able to interface with the dehumidificator appliance is:
https://github.com/barban-dev/midea_inventor_dehumidifier
"""
VERSION = '0.9.9'

import logging
from custom_components.midea_dehumi import DOMAIN, MIDEA_TARGET_DEVICE
from homeassistant.helpers.entity import Entity
from homeassistant.const import (DEVICE_CLASS_HUMIDITY)

_LOGGER = logging.getLogger(__name__)

#TODO: check if it is usefull
#DEPENDENCIES = ['midea_dehumi']


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up available sensors for MideaDehumi Climate Entity."""
    _LOGGER.info("sensor.midea_dehumi: initializing sensor entity sub-component")
    _LOGGER.debug("sensor.midea_dehumi: starting async_setup_platform")

    #ref: https://developers.home-assistant.io/docs/en/creating_component_generic_discovery.html
    targetDevice = discovery_info[MIDEA_TARGET_DEVICE]
    _LOGGER.debug("sensor.midea_dehumi: targetDevice = %s", targetDevice)
    
    if targetDevice:
        #Create sensor entity
        sensor = MideaDehumiSensor(targetDevice, hass)

        #Add sensor entity
        async_add_entities([sensor])
        _LOGGER.info("sensor.midea_dehumi: sensor entity initialized.")
    else:
        _LOGGER.error("sensor.midea_dehumi: error initializing sensor entity.")

    
    
	
class MideaDehumiSensor(Entity):
    """Representation of a MideaDehumiDevice sensor."""

    def __init__(self, targetDevice, hass):
        """Initialize the sensor."""

        self._device = targetDevice
        self._hass = hass
        self._name = 'midea_dehumi_' + targetDevice['id'] + '_humidity'
        self._unique_id = 'midea_dehumi_' + targetDevice['id'] + '_humidity'
        #self._type = type
        self._device_class = DEVICE_CLASS_HUMIDITY
        self._unit_of_measurement = '%'
        self._icon = 'mdi:water-percent'
        #self._battery = battery

        self._state = None
        self._climate_entity_state = None

        #Retrieve the state of the climate midea_dehumi entity
        climate_entity_id = 'climate.midea_dehumi_' + targetDevice['id']
        #hass.sates.get is async friendly (ref. https://dev-docs.home-assistant.io/en/master/api/core.html#homeassistant.core.StateMachine)
        state = self._hass.states.get(climate_entity_id)
        if state:
            self._climate_entity_state = state

            self._state = state.attributes["current_humidity"]
            _LOGGER.debug("sensor.midea_dehumi: current humidity = %s", self._state)
        else:
            _LOGGER.debug("sensor.midea_dehumi: cannot retrieve the state of midea_humi climate entity")


    @property
    def unique_id(self):
        """Return the unique id."""
        return self._unique_id

    @property
    def name(self):
        """Return the name of the sensor device. The Name is derived from the device id"""
        return self._name

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return self._icon

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return self._device_class

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return self._unit_of_measurement

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    async def async_update(self):
        #Get the latest data from state's attributes of midea_dehumi climate entity
        _LOGGER.debug("sensor.midea_dehumi: ASYC UPDATE called")
        if self._climate_entity_state:
            self._state = self._climate_entity_state.attributes["current_humidity"]
            _LOGGER.debug("sensot.midea_dehumi: current humidity = %s", self._state)
        else:
            _LOGGER.debug("sensor.midea_dehumi: cannot retrieve the state of midea_humi climate entity")

    @property
    def should_poll(self):
        return True

#    def update(self):
#        """Update method called when should_poll is true."""
#        #Get the latest data from state's attributes of midea_dehumi climate entity
#        _LOGGER.debug("sensor.midea_dehumi: UDPATE called")
#        if self._climate_entity_state:
#            self._state = self._climate_entity_state.attributes["current_humidity"]
#            _LOGGER.debug("sensot.midea_dehumi: current humidity = %s", self._state)
#        else:
#            _LOGGER.debug("sensor.midea_dehumi: cannot retrieve the state of midea_humi climate entity")

