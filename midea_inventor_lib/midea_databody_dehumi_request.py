import binascii
import logging
from .midea_fcCon import fcCon


class DataBodyDeHumiRequest:

  def __init__(self):
    logging.debug("DataBodyDeHumiRequest: initializing DataBodyDeHumiReqyest object.")

    self.mOrder = 10
    self.AChead = [-86, 0, -84, 0, 0, 0, 0, 0, 3, 2]

    self.powerMode = 0
    self.setMode = 0
    self.ionSetSwitch = 0
    self.humidity_dot_set = 0
    self.humidity_set = 45
    self.windSpeed = 40
    self.isDisplay = True

    self.humidity = 50
    self.humidity_dot = 0

    self.timingMode = 0
    self.timingCloseHour = 0
    self.timingCloseMark = 0
    self.timingCloseMinute = 0
    self.timingOpenHour = 0
    self.timingOpenMark = 0
    self.timingOpenMinute = 0
    self.upanddownSwing = 0


  def __addHead(self, bytes, deivceType, isQuery):
    self.AChead[1] = len(bytes) + len(self.AChead)
    self.AChead[2] = deivceType;
    if isQuery:
      self.AChead[len(self.AChead) - 1] = 3
    else:
      self.AChead[len(self.AChead) - 1] = 2

    result = self.AChead + bytes
    #logging.debug("result=%s", str(result))

    crcsum  = self.__makeSum(result, len(result))
    if crcsum > 128:
      crcsum -= 256

    result.append(crcsum)
    #logging.debug("result=%s", str(result))

    return result


  def __makeSum(self, bytes, tmpLen):
    resVal = 0
    for si in range(1, tmpLen):
      resVal = bytes[si] + resVal

    resVal = (255 - (resVal % 256)) + 1
    logging.debug("DataBodyDeHumiRequest: generated checksum length=%s : %s", str(tmpLen), str(resVal))

    return resVal


  def toBytes(self):
    """Returns [signed bytes]"""

    con = fcCon()
    con.btnSound = 1
    con.controlSource = 1
    con.optCommand = 3
    con.runStatus = self.powerMode
    con.windSpeed = self.windSpeed
    con.humidity = self.humidity_set
    con.humidity_set_dot = self.humidity_dot
    con.mode_F1_return = self.setMode
    con.ionSetSwitch = self.ionSetSwitch
    con.timingOffHour = self.timingCloseHour
    con.timingOffMinute = self.timingCloseMinute
    con.timingOffSwitch = self.timingCloseMark
    con.timingOnHour = self.timingOpenHour
    con.timingOnMinute = self.timingOpenMinute
    con.timingOnSwitch = self.timingOpenMark
    con.timingIsValid = 1
    con.timingType = self.timingMode
    con.controlSource = 1
    con.upanddownSwing = self.upanddownSwing
    con.mode_FD_return = self.setMode

    if self.isDisplay:
      con.displayClass = 0
    else:
      con.displayClass = 7

    self.mOrder += 1
    con.order = self.mOrder

    buff = [0] * 128
    #devType=253
    #msgType=4
    length = con.stdAirConEx_pro2byte(253, 4, buff, len(buff))
    if length < 0:
      logging.error("DataBodyDeHumiRequest: ERROR: con.stdAirConEx_pro2byte()")

    #print buff
    logging.debug("DataBodyDeHumiRequest::toBytes: buff=%s", buff)

    #unsigned int[] to signed byte[] conversion
    newBuf = []
    for i in range(length):
      if buff[i] >= 128:
        newBuf.append(buff[i] - 256)
      else:
        newBuf.append(buff[i])

    #print newBuf
    logging.debug("DataBodyDeHumiRequest::toBytes: newBuff=%s", newBuf)

    result = self.__addHead(newBuf, con.DEHUMI, False)
    #print str(result)
    logging.debug("DataBodyDeHumiRequest: tobytes()=%s", result)

    return result


  def setDataBodyStatus(self, status):
    """status is derived from MideaDehumidificationDevice"""

    self.powerMode = status.powerMode
    self.setMode = status.setMode
    self.windSpeed = status.windSpeed
    self.humidity_dot_set = status.humidity_dot_set
    self.humidity_set = status.humidity_set
    self.isDisplay = status.isDisplay
    self.ionSetSwitch = status.ionSetSwitch

