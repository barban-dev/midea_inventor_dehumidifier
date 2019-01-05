import sys
import getopt
import time
import datetime
import requests
import json
import logging
from midea_inventor_lib import MideaClient
#from midea_inventor_lib import MideaSecurity
#from midea_inventor_lib import DataBodyDeHumiQuery
#from midea_inventor_lib import DataBodyDeHumiResponse
#from midea_inventor_lib import MideaDehumidificationDevice
#from midea_inventor_lib import DataBodyDeHumiRequest


client = None
sessionId = ""
deviceId = ""


def do_login():
  global client
  global sessionId

  res = client.login()
  if res == -1:
    print("Login error: please check log messages.")
  else:
    sessionId = client.current["sessionId"]


def list_appliances():
  global client

  if client.security.access_token is None:
    print("Please login first!\n")
    return None

  appliances = {}
  appliances = client.listAppliances()

  for a in appliances:
    print("[id="+a["id"]+" type="+a["type"]+" name="+a["name"]+"]")
    if a["onlineStatus"] == "1":
      print("is online")
    else:
      print("is offline")
    if a["activeStatus"] == "1":
      print("is active")
    else:
      print("is not active")

  #The first appliance having type="0xA1" is returned for default (otherwise, 'Set deviceId' option can be used)
  return appliances


def setDeviceId():
  global client
  global deviceId

  id = str(input("deviceId ["+deviceId+"]: "))
  if id:
    deviceId = id


def getDeviceStatus():
  global client
  global deviceId

  if client.security.access_token is None:
    print("Please login first!\n")
  elif not deviceId:
    print("Please set deviceId first!\n")
  else:
    res = client.get_device_status(deviceId)
    if res == 1:
      print(client.deviceStatus.toString())

def power_on():
  global client
  global deviceId

  if client.security.access_token is None:
    print("Please login first!\n")
  elif not deviceId:
    print("Please set deviceId first!\n")
  elif client.deviceStatus is None:
    print("Please get device status first!\n")
  elif client.deviceStatus.powerMode == 1:
      print("Device is already on.\n")
  else:
    res = client.send_poweron_command(deviceId)
    if res is not None:
      print(client.deviceStatus.toString())


def power_off():
  global client
  global deviceId

  if client.security.access_token is None:
    print("Please login first!\n")
  elif not deviceId:
    print("Please set deviceId first!\n")
  elif client.deviceStatus is None:
    print("Please get device status first!\n")
  elif client.deviceStatus.powerMode == 0:
      print("Device is already off.\n")
  else:
    res = client.send_poweroff_command(deviceId)
    if res:
      print(client.deviceStatus.toString())


def ion_on():
  global client
  global deviceId

  if client.security.access_token is None:
    print("Please login first!\n")
  elif not deviceId:
    print("Please set deviceId first!\n")
  elif client.deviceStatus is None:
    print("Please get device status first!\n")
  elif client.deviceStatus.powerMode == 0:
    print("Device is off.\n")
  elif client.deviceStatus.ionSetSwitch == 1:
      print("Ion is already on.\n")
  else:
    res = client.send_ion_on_command(deviceId)
    if res:
      print(client.deviceStatus.toString())


def ion_off():
  global client
  global deviceId

  if client.security.access_token is None:
    print("Please login first!\n")
  elif not deviceId:
    print("Please set deviceId first!\n")
  elif client.deviceStatus is None:
    print("Please get device status first!\n")
  elif client.deviceStatus.powerMode == 0:
      print("Device is off.\n")
  elif client.deviceStatus.ionSetSwitch == 0:
      print("Ion is already off.\n")
  else:
    res = client.send_ion_off_command(deviceId)
    if res:
      print(client.deviceStatus.toString())



def set_speed():
  global client
  global deviceId

  if client.security.access_token is None:
    print("Please login first!\n")
  elif not deviceId:
    print("Please set deviceId first!\n")
  elif client.deviceStatus is None:
    print("Please get device status first!\n")
  elif client.deviceStatus.powerMode == 0:
    print("Device is off.\n")
  else:
    loop = True
    while loop:
      print("Please remember that speed value cannot be changed in DRY MODE");
      speedStr = str(input("Speed [0..100] (silent:40, medium:60, high:80):"))
      try:
        speed = int(speedStr)
      except ValueError:
        print("input value is not a valid integer, please retry.")
      else:
        if speed > 0 and speed < 100:
          loop = False
        else:
          print("input value is not in the valid range, please retry.")


    if speed > 0 and speed < 100:
      res = client.send_fan_speed_command(deviceId, speed)
      if res:
        print(client.deviceStatus.toString())



def set_humidity():
  global client
  global deviceId

  if client.security.access_token is None:
    print("Please login first!\n")
  elif not deviceId:
    print("Please set deviceId first!\n")
  elif client.deviceStatus is None:
    print("Please get device status first!\n")
  elif client.deviceStatus.powerMode == 0:
    print("Device is off.\n")
  else:
    loop = True
    while loop:
      humStr = str(input("Target Humidity [30..70]:"))
      try:
        hum = int(humStr)
      except ValueError:
        print("input value is not a valid integer, retry.")
      else:
        if hum >= 30 and hum <= 70:
          loop = False
        else:
          print("input value is not in the valid range, please retry.")


    if hum >= 30 and hum <= 70:
      res = client.send_target_humidity_command(deviceId, hum)
      if res is not None:
        print(client.deviceStatus.toString())



def set_mode():
  global client
  global deviceId

  if client.security.access_token is None:
    print("Please login first!\n")
  elif not deviceId:
    print("Please set deviceId first!\n")
  elif client.deviceStatus is None:
    print("Please get device status first!\n")
  elif client.deviceStatus.powerMode == 0:
    print("Device is off.\n")
  else:
    loop = True
    while loop:
      modeStr = str(input("Mode [1..4] (1: TARGET_MODE, 2: CONTINUOUS_MODE, 3: SMART_MODE, 4: DRYER_MODE): "))
      try:
        mode= int(modeStr)
      except ValueError:
        print("input value is not a valid integer, retry.")
      else:
        loop = False

    if mode > 0 and mode < 5:
      res = client.send_mode_command(deviceId, mode)
      if res:
        print(client.deviceStatus.toString())




def menu():
  global sessionId
  global deviceId
  global deviceStatus

  print("=============================")
  if not sessionId:
    print("0: Login")
  else:
    print("0: Login [Logged in: sessionId="+sessionId+"]")
  print("1: List configured appliances")
  if not deviceId:
    print("2: Set deviceID")
  else:
    print("2: Set deviceID [deviceId="+deviceId+"]")

  if client.deviceStatus is None:
    print("3: Get device status")
  else:
    print("3: Get device status ["+client.deviceStatus.toString()+"]")

  print("4: Send power on command")
  print("5: Send power off command")
  print("6: Send fan speed command")
  print("7: Send Mode command")
  print("8: Send Ion switch on command")
  print("9: Send Ion switch off command")
  print("10: Set humidity point")
  print("11: Set on-off timer")
  print("99: Exit")


def main(argv):
  global client
  global deviceId

  _email = ""
  _password = ""
  _sha256password = ""
  _log = False
  _logfile = ""
  _verbose = False
  _debug = False

  try:
    opts, args = getopt.getopt(sys.argv[1:], "e:p:s:l:hvd", ["email=", "password=", "md5_password="])
  except getopt.GetoptError:
    print("Usage:"+sys.argv[0]+" -e <email_address> -p <cleartext password> -s <sha256_password> -l <logfile> [-h] [-v] [-d]")
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print("Usage:"+sys.argv[0]+" -e <email_address> -p <cleartext password> -s <sha256_password> -l <logfile> [-h] [-v] [-d]")
      sys.exit()
    elif opt == '-d':
      _debug = True
    elif opt == '-v':
      _verbose = True
    elif opt in ("-e", "--email"):
      _email = arg
    elif opt in ("-p", "--password"):
      _password = arg
    elif opt in ("-s", "--sha256_password"):
      _sha256password = arg
    elif opt in ("-l", "--logfile"):
      _logfile = arg
      _log = True

  if _debug:
    print("---ARGS---")
    print("- email: "+_email)
    print("- password: "+_password)
    print("- sha256password: "+_sha256password)
    print("- log: "+str(_log))
    print("- logfile: "+_logfile)
    print("- debug: "+str(_debug))
    print("- verbose: "+str(_verbose))
    print("----------")

  if not _email:
    print("Error: you must specify -e input parameter")
    sys.exit(2)

  if not _password and not _sha256password:
    print("Error: you must specify -p or -s input parameter")
    sys.exit(2)
  else:
    #client = MideaClient(_email, _password, _sha256password)
    client = MideaClient(_email, _password, _sha256password, _debug, _verbose, _logfile)


  while True:
    menu()
    cmd = str(input("Choose a command: "))
    if cmd == "0":
      #Perform login
      do_login()
    elif cmd == "1":
      appliances = list_appliances()
      if appliances is not None:
        for a in appliances:
          if a["type"] == "0xA1":
            deviceId = str(a["id"])
            print("deviceID="+deviceId)
    elif cmd == "2":
      setDeviceId()
    elif cmd == "3":
      getDeviceStatus()
    elif cmd == "4":
      power_on()
    elif cmd == "5":
      power_off()
    elif cmd == "6":
      set_speed()
    elif cmd == "7":
      set_mode()
    elif cmd == "8":
      ion_on()
    elif cmd == "9":
      ion_off()
    elif cmd == "10":
      set_humidity()
    elif cmd == "11":
      print("TODO\n")
    elif cmd == "99":
      sys.exit(0)
    else:
      print("Unrecognized command!\n")


#Call main() function
if __name__ == "__main__":
    main(sys.argv)


