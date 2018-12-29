import binascii
import logging
from .midea_fcCon import fcCon


class DataBodyDeHumiQuery:

  def __init__(self):
    logging.debug("DataBodyDeHumiQuery: initializing DataBodyDeHumiQuery object")
    self.mOrder = 10
    self.AChead = [-86, 0, -84, 0, 0, 0, 0, 0, 3, 2]


  def __addHead(self, bytes, deivceType, isQuery):
    self.AChead[1] = len(bytes) + len(self.AChead)
    self.AChead[2] = deivceType;
    if isQuery:
      self.AChead[len(self.AChead) - 1] = 3
    else:
      self.AChead[len(self.AChead) - 1] = 2

    result = self.AChead + bytes

    crcsum = self.__makeSum(result, len(result))
    if crcsum > 128:
      crcsum -= 256

    result.append(crcsum)
    logging.debug("DataBodyDeHumiQuery: result=%s", str(result))

    return result


  def __makeSum(self, bytes, tmpLen):
    resVal = 0
    for si in range(1, tmpLen):
      resVal = bytes[si] + resVal

    resVal = (255 - (resVal % 256)) + 1
    logging.debug("DataBodyDeHumiQuery: generated checksum length=%s : %s", str(tmpLen), str(resVal))
    return resVal


  def toBytes(self):
    con = fcCon()
    con.sound = 0;
    con.optCommand = 3;
    self.mOrder += 1
    con.order = self.mOrder

    buff = [0] * 128

    #devType=161
    #msgType=1
    length = con.stdAirConEx_pro2byte(161, 1, buff, len(buff))
    if length < 0:
      logging.error("DataBodyDeHumiQuery: ERROR: con.stdAirConEx_pro2byte()")

    logging.debug("DataBodyDeHumiQuery: pro2byte result=%s", str(buff))

    #unsigned int[] to signed byte[] conversion
    newBuf = []
    for i in range(length):
      if buff[i]>= 128:
        newBuf.append(buff[i] - 256)
      else:
        newBuf.append(buff[i])

    logging.debug("DataBodyDeHumiQuery: pro2byte result to signed bytes=%s", str(newBuf))

    result = self.__addHead(newBuf, con.DEHUMI, True)
    logging.debug("DataBodyDeHumiQuery: result=%s", str(result))

    return result

