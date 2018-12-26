import logging
from midea_fcCon import fcCon
from midea_dehumidification_device import MideaDehumidificationDevice


class DataBodyDeHumiResponse:

  def __init__(self):
    logging.debug("DataBodyDeHumiResponse: initializing DataBodyDeHumiResponse object.")


  def toMideaDehumidificationDeviceObject(self, bytes):
    dehumi = MideaDehumidificationDevice()
    con = fcCon()

    length = len(bytes)
    int_data = [None] * length

    for i in range(length):
      int_data[i] = bytes[i]
      if int_data[i] < 0:
        int_data[i] = int_data[i] + 256

    #msgType = 1
    #Set fcCon attributes according to int_data
    log = con.stdAirConEx_byte2pro(int_data, len(int_data))
    if (log != 0):
      logging.error("DataBodyDeHumiResponse: ERROR calling con.stdAirConEx_byte2pro()")

    if con.ionSetSwitch == 1:
      dehumi.ionSetSwitch = 1
    else:
      dehumi.ionSetSwitch = 0

    dehumi.powerMode = con.runStatus
    dehumi.setMode = con.mode_F1_return
    dehumi.humidity = con.humidity_cur
    dehumi.humidity_dot = con.humidity_cur_dot

    if con.filterShow == 0:
      dehumi.filterShow = False
    else:
      dehumi.filterShow = True

    if dehumi.setMode == 1:
      dehumi.humidity_set = con.humidity
      dehumi.humidity_dot_set = con.humidity_set_dot
    else:
      dehumi.humidity_set = con.humidity

    dehumi.windSpeed = con.windSpeed
    dehumi.upanddownSwing = con.upanddownSwing
    dehumi.timingCloseHour = con.timingOffHour
    dehumi.timingCloseMinute = con.timingOffMinute
    dehumi.timingCloseMark = con.timingOffSwitch
    dehumi.timingOpenHour = con.timingOnHour
    dehumi.timingOpenMinute = con.timingOnMinute
    dehumi.timingOpenMark = con.timingOnSwitch

    if con.tankShow == 100:
      dehumi.tankShow = True
    else:
      dehumi.tankShow = False

    if con.displayClass != 7:
      dehumi.isDisplay = True
    else:
      dehumi.isDisplay = False

    return dehumi
