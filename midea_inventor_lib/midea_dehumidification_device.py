import logging

class MideaDehumidificationDevice:

  def __init__(self):
    logging.debug("Initializing MideaDehumidificationDevice object")

    self._powerMode = 0		#off
    self._setMode = 0
    self._humidity = 50
    self._humidity_set = 45
    self._humidity_dot = 0
    self._humidity_dot_set = 0
    self._windSpeed = 40
    self._ionSetSwitch = 0	#off

    self._isDisplay = True
    self._filterShow = False
    self._tankShow = False
    self._dryClothesSetSwitch = 0
    self._upAndDownSwing = 0

    self.timingCloseHour = 0
    self.timingCloseMark = 0
    self.timingCloseMinute = 0
    self.timingOpenHour = 0
    self.timingOpenMark = 0
    self.timingOpenMinute = 0

    ##Not used in dehumi device
    #self._faultMark = 0
    #self.mobileTiming = 0
    #self.modeRecovery = 0
    #self.quackCheckStatus = 0
    #self.sharpTurning = 0
    #self.timingMode = 0


  def setStatus(self, status):
    self._powerMode = status.powerMode
    self._setMode = status.setMode
    self._humidity = status.humidity
    self._humidity_set = status.humidity_set
    self._humidity_dot = status.humidity_dot
    self._humidity_dot_set = status.humidity_dot_set
    self._windSpeed = status.windSpeed
    self._ionSetSwitch = status.ionSetSwitch

    self._isDisplay = status.isDisplay
    self._filterShow = status.filterShow
    self._tankShow = status.tankShow
    self._dryClothesSetSwitch = status.dryClothesSetSwitch
    self._upAndDownSwing = status.upAndDownSwing

    self._timingCloseHour = status._timingCloseHour
    self._timingCloseMark = status._timingCloseMark
    self._timingCloseMinute = status._timingCloseMinute
    self._timingOpenHour = status._timingOpenHour
    self._timingOpenMark = status._timingOpenMark
    self._timingOpenMinute = status._timingOpenMinute


  def toString(self):
    #TODO: add timingXX attributes
    return "DeHumidification [powerMode=" + str(self._powerMode) + ", mode=" + str(self._setMode) + ", Filter=" + str(self._filterShow) + ", Water tank=" + str(self._tankShow) + ", Current humidity=" + str(self._humidity) + ", Current humidity (decimal)=" + str(self._humidity_dot) + ", Wind speed=" + str(self._windSpeed) + ", Set humidity=" + str(self._humidity_set) + ", Set humidity (decimal)=" + str(self._humidity_dot_set) +", ionSetSwitch=" +str(self._ionSetSwitch) + ", isDisplay=" +str(self._isDisplay) + ", dryClothesSetSwitch=" + str(self._dryClothesSetSwitch) + ", Up&Down Swing=" +str(self._upAndDownSwing) +"]"


  @property
  def powerMode(self):
    return self._powerMode

  @property
  def setMode(self):
    return self._setMode

  @property
  def humidity(self):
    """Return the current humidity"""
    return self._humidity

  @property
  def humidity_set(self):
    """Return the target humidity"""
    return self._humidity_set

  @property
  def humidity_dot(self):
    """Return the current humidity (decimal)"""
    return self._humidity_dot

  @property
  def humidity_dot_set(self):
    """Return the target humidity (decimal)"""
    return self._humidity_dot_set

  @property
  def windSpeed(self):
    return self._windSpeed

  @property
  def ionSetSwitch(self):
    return self._ionSetSwitch

  @property
  def isDisplay(self):
    return self._isDisplay

  @property
  def filterShow(self):
    return self._filterShow

  @property
  def tankShow(self):
    return self._tankShow

  @property
  def dryClothesSetSwitch(self):
    return self._dryClothesSetSwitch

  @property
  def upAndDownSwing(self):
    return self._upAndDownSwing

  #TODO: add timingXX attributes

