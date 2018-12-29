import logging

class fcCon:

  def __init__(self):
    logging.debug("fcCon: initializing fcCon object.")

    self.SOURCE_ANY = 0xffffff00	#A special input source constant that is used when filtering input devices to match devices that provide any type of input source.
    self.KEYCODE_MEDIA_PLAY = 126
    self.KEYCODE_MEDIA_PAUSE = 127
    self.VERSION_CODE = 146
    self.REQUEST_CONTROL_AVOID = 177
    self.SET_WEATHER_REQUEST_CODE = 105
    self.SET_WEATHER_RESULT_CODE = 106
    self.BAR_HEIGHT = 136
    self.f2050b = 160
    self.DEHUMI = -95
    self.DEHUMI_STR = "0xA1"	#Dehumidificator device
    self.HUMI = -3
    self.crc8_854_table = [0, 94, 188, 226, 97, 63, 221, 131, 194, 156, self.KEYCODE_MEDIA_PLAY, 32, 163, 253, 31, 65, 157, 195, 33, self.KEYCODE_MEDIA_PAUSE, 252, 162, 64, 30, 95, 1, 227, 189, 62, 96, 130, 220, 35, 125, 159, 193, 66, 28, 254, self.f2050b, 225, 191, 93, 3, 128, 222, 60, 98, 190, 224, 2, 92, 223, 129, 99, 61, 124, 34, 192, 158, 29, 67, 161, 255, 70, 24, 250, 164, 39, 121, 155, 197, 132, 218, 56, 102, 229, 187, 89, 7, 219, 133, 103, 57, 186, 228, 6, 88, 25, 71, 165, 251, 120, 38, 196, 154, 101, 59, 217, 135, 4, 90, 184, 230, 167, 249, 27, 69, 198, 152, 122, 36, 248, 166, 68, 26, 153, 199, 37, 123, 58, 100, 134, 216, 91, 5, 231, 185, 140, 210, 48, 110, 237, 179, 81, 15, 78, 16, 242, 172, 47, 113, 147, 205, 17, 79, 173, 243, 112, 46, 204, self.VERSION_CODE, 211, 141, 111, 49, 178, 236, 14, 80, 175, 241, 19, 77, 206, 144, 114, 44, 109, 51, 209, 143, 12, 82, 176, 238, 50, 108, 142, 208, 83, 13, 239, self.REQUEST_CONTROL_AVOID, 240, 174, 76, 18, 145, 207, 45, 115, 202, 148, 118, 40, 171, 245, 23, 73, 8, 86, 180, 234, self.SET_WEATHER_REQUEST_CODE, 55, 213, 139, 87, 9, 235, 181, 54, 104, 138, 212, 149, 203, 41, 119, 244, 170, 72, 22, 233, 183, 85, 11, self.BAR_HEIGHT, 214, 52, self.SET_WEATHER_RESULT_CODE, 43, 117, 151, 201, 74, 20, 246, 168, 116, 42, 200, 150, 21, 75, 169, 247, 182, 232, 10, 84, 215, 137, 107, 53]

    self.order = 0
    self.windSpeed = 0
    self.ionSetSwitch = 0
    self.btnSound = 0
    self.humidity = 0
    self.humidity_cur = 0
    self.humidity_cur_dot = 0
    self.humidity_set_dot = 0
    self.filterShow = 0
    self.tankShow = 0

    #Not used by Dehumidificator device
    self.childSleepMode = 0
    self.clearTime = 0
    self.controlSource = 0
    self.defrostingShow = 0
    self.displayClass = 0
    self.dustShow = 0
    self.dustTimeSet = 0
    self.dustTimeShow = 0
    self.errCode = 0
    self.faultFlag = 0
    self.iMode = 0
    self.indoorTmp = 0
    self.indoorTmpT1_dot = 0
    self.leftandrightSwing = 0
    self.lightClass = 0
    self.lightValue = 0
    self.mode_F1_return = 0
    self.mode_FC_return = 0
    self.mode_FD_return = 0
    self.optCommand = 0
    self.pmHighValue = 0
    self.pmLowValue = 0
    self.pumpSwitch = 0
    self.pumpSwitch_flag = 0
    self.quickChkSts = 0
    self.rareShow = 0
    self.rareValue = 0
    self.runStatus = 0
    self.sleepSwitch = 0
    self.sound = 0
    self.timingIsValid = 0
    self.timingOffHour = 0
    self.timingOffMinute = 0
    self.timingOffSwitch = 0
    self.timingOnHour = 0
    self.timingOnMinute = 0
    self.timingOnSwitch = 0
    self.timingType = 0
    self.upanddownSwing = 0


  # Used by stdAirConEx_pro2byte
  def crc8_854(self, dataBuf, dataLen):
    #logging.debug("fcCon: crc8_854_dataLen=%s crc8_854_dataBuf=%s", str(dataLen), str(dataBuf))
    #logging.debug("fcCon: crc8_854 table length=%s", str(len(self.crc8_854_table)))

    if (dataBuf is None or dataLen is None):
      return 0

    crc = 0
    tmp = dataBuf
    for si in range(dataLen):
      try:
        index = crc ^ tmp[si]
        if index > 256:
          index += self.SOURCE_ANY
        if index < 0:
          index += 256

        crc = self.crc8_854_table[index]
      except:
        logging.error("fcCon: ERROR: exception occured when canculating CRC.")

    logging.debug("fcCon: crc8-854 result=%s", str(crc))
    return crc


  # Used by DataBodyDeHumiResponse.toObject() in order to decode reply token received via API
  def stdAirConEx_byte2pro(self, srcBuf, srcLen):
    logging.debug("fcCon: executing stdAirConEx_byte2pro method")

    datLen = srcLen
    msgcmd = srcBuf[10]
    logging.debug("fcCon: msgcmd=%s", str(msgcmd))

    info = [None] * 64
    info = srcBuf[10:]

    self.faultFlag = (info[1] & 128) >> 7
    self.runStatus = info[1] & 1
    self.timingType = (info[1] & 16) >> 4
    self.iMode = (info[1] & 4) >> 2
    self.quickChkSts = (info[1] & 32) >> 5
    self.mode_FC_return = (info[2] & 240) >> 4
    self.mode_F1_return = info[2] & 15
    self.windSpeed = info[3] & self.KEYCODE_MEDIA_PAUSE
    self.timingOnSwitch = (info[4] & 128) >> 7
    self.timingOffSwitch = (info[5] & 128) >> 7
    if 1 == self.timingType:
      if 1 == self.timingOnSwitch:
        self.timingOnHour = ((info[4] & self.KEYCODE_MEDIA_PAUSE) >> 2) & 31
        self.timingOnMinute = (((info[4] & self.KEYCODE_MEDIA_PAUSE) & 3) * 15) + (info[6] & 240)
      if 1 == self.timingOffSwitch:
        self.timingOffHour = ((info[5] & self.KEYCODE_MEDIA_PAUSE) >> 2) & 31
        self.timingOffMinute = (((info[5] & self.KEYCODE_MEDIA_PAUSE) & 3) * 15) + (info[6] & 15)
    else:
      if 1 == self.timingOnSwitch and self.KEYCODE_MEDIA_PAUSE != (info[4] & self.KEYCODE_MEDIA_PAUSE):
        self.timingOnHour = ((((info[4] & self.KEYCODE_MEDIA_PAUSE) + 1) * 15) - ((info[6] >> 4) & 15)) // 60
        self.timingOnMinute = ((((info[4] & self.KEYCODE_MEDIA_PAUSE) + 1) * 15) - ((info[6] >> 4) & 15)) % 60
      if 1 == self.timingOffSwitch and self.KEYCODE_MEDIA_PAUSE != (info[5] & self.KEYCODE_MEDIA_PAUSE):
        self.timingOffHour = ((((info[5] & self.KEYCODE_MEDIA_PAUSE) + 1) * 15) - (info[6] & 15)) // 60
        self.timingOffMinute = ((((info[5] & self.KEYCODE_MEDIA_PAUSE) + 1) * 15) - (info[6] & 15)) % 60

    self.humidity = info[7]
    if info[7] > 100:
      info[7] = 99

    self.humidity_set_dot = info[8] & 15
    self.mode_FD_return = info[10] & 7
    self.filterShow = (info[9] & 128) >> 7
    self.ionSetSwitch = (info[9] & 64) >> 6
    self.sleepSwitch = (info[9] & 32) >> 5
    self.pumpSwitch_flag = (info[9] & 16) >> 4
    self.pumpSwitch = (info[9] & 8) >> 3
    self.displayClass = info[9] & 7
    self.defrostingShow = (info[10] & 128) >> 7
    self.tankShow = info[10] & self.KEYCODE_MEDIA_PAUSE
    self.dustTimeShow = info[11] * 2
    self.rareShow = (info[12] & 56) >> 3
    self.dustShow = info[12] & 7
    self.pmLowValue = info[13]
    self.pmHighValue = info[14]
    self.rareValue = info[15]
    self.humidity_cur = info[16]

    logging.info("fcCon: Current humidity reported by device = %s", str(self.humidity_cur))

    self.indoorTmp = info[17]
    self.humidity_cur_dot = info[18] & 240
    self.indoorTmpT1_dot = (info[18] & 15) >> 4
    self.lightClass = info[19] & 240
    self.upanddownSwing = (info[19] & 32) >> 5
    self.leftandrightSwing = (info[19] & 32) >> 4
    self.lightValue = info[20]
    self.errCode = info[21]
    return 0


  # Used by DataBodyDeHumiQuery.tobytes() and DataBodyDeHumiRequest.tobytes() to set token order 
  def stdAirConEx_pro2byte(self, devType, msgType, tmpBuf, dstLen):

    #devType=253 (DataBodyDehumiRequest)
    #devType=161 (DataBodyDehumiQuery)
    if (devType != 253 and devType != 161):
      return -1

    #DataBodyDeHumiQuery
    if msgType == 1:
      logging.debug("fcCon: msgType: DataBodyDeHumiQuery")

      tmpBuf[0] = 65
      tmpBuf[1] = (self.sound << 6) | 33
      tmpBuf[2] = 0
      tmpBuf[3] = 255
      tmpBuf[4] = self.optCommand
      tmpBuf[5] = 0
      tmpBuf[6] = 0
      tmpBuf[7] = 2
      tmpBuf[8] = 0
      tmpBuf[9] = 0
      tmpBuf[10] = 0
      tmpBuf[11] = 0
      tmpBuf[12] = 0
      tmpBuf[13] = 0
      tmpBuf[14] = 0
      tmpBuf[15] = 0
      tmpBuf[16] = 0
      tmpBuf[17] = 0
      tmpBuf[18] = 0
      tmpBuf[19] = 0
      tmpBuf[20] = self.order
      tmpBuf[21] = self.crc8_854(tmpBuf, 21)

      return 22

    #DataBodyDeHumiRequest
    elif msgType == 4:
      logging.debug("fcCon: msgType: DataBodyDeHumiRequest")

      tmpBuf[0] = 72
      tmpBuf[1] = (((((((self.btnSound & 1) << 6) | ((self.quickChkSts & 1) << 5)) | ((self.timingType & 1) << 4)) | ((self.childSleepMode & 1) << 3)) | ((self.iMode & 1) << 2)) | ((self.controlSource & 1) << 1)) | ((self.runStatus & 1) << 0)
      tmpBuf[2] = ((self.mode_FC_return & 15) << 4) | (self.mode_F1_return & 15)
      tmpBuf[3] = ((self.timingIsValid & 1) << 7) | (self.windSpeed & self.KEYCODE_MEDIA_PAUSE)
      if 1 == self.timingType:
        tmpBuf[4] = ((self.timingOnSwitch << 7) | (self.timingOnHour << 2)) | (self.timingOnMinute // 15)
        tmpBuf[5] = ((self.timingOffSwitch << 7) | (self.timingOffHour << 2)) | (self.timingOffMinute & 3)
        tmpBuf[6] = ((self.timingOnMinute % 15) << 4) | (self.timingOffMinute % 15)
      else:
        tmpMinute = (self.timingOnHour * 60) + self.timingOnMinute
        if (1 != self.timingOnSwitch or tmpMinute == 0):
          tmpBuf[4] = self.KEYCODE_MEDIA_PAUSE
          tmpBuf[6] = tmpBuf[6] & 15
        else:
          tmpBuf[4] = 128
        if (tmpMinute % 15 != 0):
          tmpBuf[4] = tmpBuf[4] | ((tmpMinute // 15) & self.KEYCODE_MEDIA_PAUSE)
          tmpBuf[6] = tmpBuf[6] | (((15 - (tmpMinute % 15)) & 15) << 4)
        else:
          tmpBuf[4] = tmpBuf[4] | (((tmpMinute // 15) - 1) & self.KEYCODE_MEDIA_PAUSE)
          tmpBuf[6] = tmpBuf[6] & 15
          tmpMinute = (self.timingOffHour * 60) + self.timingOffMinute
        if (1 != self.timingOffSwitch or tmpMinute == 0):
          tmpBuf[5] = self.KEYCODE_MEDIA_PAUSE
          tmpBuf[6] = tmpBuf[6] & 240
        else:
          tmpBuf[5] = 128
          if (tmpMinute % 15 != 0):
            tmpBuf[5] = tmpBuf[5] | ((tmpMinute // 15) & self.KEYCODE_MEDIA_PAUSE)
            tmpBuf[6] = tmpBuf[6] | ((15 - (tmpMinute % 15)) & 15)
          else:
            tmpBuf[5] = tmpBuf[5] | (((tmpMinute // 15) - 1) & self.KEYCODE_MEDIA_PAUSE)
            tmpBuf[6] = tmpBuf[6] & 240

      tmpBuf[7] = self.humidity & self.KEYCODE_MEDIA_PAUSE
      tmpBuf[8] = self.humidity_set_dot & 15
      tmpBuf[9] = (((((self.displayClass & 7) | (self.pumpSwitch << 3)) | (self.pumpSwitch_flag << 4)) | (self.sleepSwitch << 5)) | (self.ionSetSwitch << 6)) | (self.filterShow << 7)
      tmpBuf[10] = (self.mode_FD_return & 7) | (self.clearTime << 7)
      tmpBuf[10] = (tmpBuf[10] | (self.upanddownSwing << 3)) | (self.leftandrightSwing << 4)
      tmpBuf[11] = self.dustTimeSet
      tmpBuf[12] = 0
      tmpBuf[13] = 0
      tmpBuf[14] = 0
      tmpBuf[15] = 0
      tmpBuf[16] = 0
      tmpBuf[17] = 0
      tmpBuf[18] = 0
      tmpBuf[19] = 0
      tmpBuf[20] = 0
      tmpBuf[21] = 0
      tmpBuf[22] = self.order
      tmpBuf[23] = self.crc8_854(tmpBuf, 23)

      return 24

    else:
      return -2


  def toString(self):
    return "Dehumidifier Model Water tank = " + str(self.tankShow) + "  swing = " + str(self.upanddownSwing) + "  Negative ion = " + str(self.ionSetSwitch) + "  Power on state = " + str(self.runStatus) + "  Set humidity = " + str(self.humidity) + "  Set humidity fraction = " + str(self.humidity_set_dot) + "  Humidity received = " + str(self.humidity_cur) + "  Humidity fraction received = " + str(self.humidity_cur_dot) + "  Wind speed = " + str(self.windSpeed) + "  mode = " + str(self.mode_F1_return) + "  timing = " + str(self.timingIsValid) + "  Timed on = " + str(self.timingOnSwitch) + "  Timed H = " + str(self.timingOnHour) + "  Timed M = " + str(self.timingOnMinute) + "  Timing off = " + str(self.timingOffSwitch) + "  Timing off H = " + str(self.timingOffHour) + "  Timig off M = " + str(self.timingOffMinute)


