import logging

class MideaDehumidificationDevice:

  def __init__(self):
    logging.debug("Initializing MideaDehumidificationDevice object")

    self.powerMode = 0		#off
    self.setMode = 0
    self.humidity_set = 45
    self.humidity_dot_set = 0
    self.windSpeed = 40
    self.ionSetSwitch = 0	#off

    self.isDisplay = True
    self.filterShow = False
    self.tankShow = False

    self.humidity = 50
    self.humidity_dot = 0
    self.dryClothesSetSwitch = 0
    self.timingCloseHour = 0
    self.timingCloseMark = 0
    self.timingCloseMinute = 0
    self.timingOpenHour = 0
    self.timingOpenMark = 0
    self.timingOpenMinute = 0
    self.upanddownSwing = 0
    #self._faultMark = 0
    #self.mobileTiming = 0
    #self.modeRecovery = 0
    #self.quackCheckStatus = 0
    #self.sharpTurning = 0
    #self.timingMode = 0


  def setStatus(self, status):
    self.powerMode = status.powerMode
    self.setMode = status.setMode
    self.filterShow = status.filterShow
    self.tankShow = status.tankShow
    self.ionSetSwitch = status.ionSetSwitch
    self.humidity = status.humidity
    self.humidity_dot = status.humidity_dot
    self.humidity_dot_set = status.humidity_dot_set
    self.humidity_set = status.humidity_set
    self.isDisplay = status.isDisplay
    self.windSpeed = status.windSpeed
    self.dryClothesSetSwitch = status.dryClothesSetSwitch


  def toString(self):
    return "DeHumidification [switch=" + str(self.powerMode) + ", mode=" + str(self.setMode) + ", Filter=" + str(self.filterShow) + ", Water tank=" + str(self.tankShow) + ", Current humidity=" + str(self.humidity) + ", Current humidity (decimal)=" + str(self.humidity_dot) + ", Wind speed=" + str(self.windSpeed) + ", Set humidity=" + str(self.humidity_set) + ", Set humidity (decimal)" + str(self.humidity_dot_set) +", ionSetSwitch=" +str(self.ionSetSwitch) + ", isDisplay=" +str(self.isDisplay) + ", dryClothesSetSwitch=" +str(self.dryClothesSetSwitch) +"]"
