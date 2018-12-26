import time
import datetime
import requests
import json
import logging
from midea_security import MideaSecurity
from midea_databody_dehumi_query import DataBodyDeHumiQuery
from midea_databody_dehumi_response import DataBodyDeHumiResponse
from midea_dehumidification_device import MideaDehumidificationDevice
from midea_databody_dehumi_request import DataBodyDeHumiRequest


#Main class
class MideaClient:

  APP_KEY = "3742e9e5842d4ad59c2db887e12449f9"
  APP_ID = 1017
  SRC = 17
  SERVER_URL  = "https://mapp.appsmb.com"
  CLIENT_TYPE = 1                 # Android
  FORMAT      = 2                 # JSON
  LANGUAGE    = "en_US"


  def __init__(self, email, password, sha256password, debug=False, verbose=False, logFile=""):

    #Set logging
    if debug:
      loglevel=logging.DEBUG
      loglevelStr = "DEBUG"
    elif verbose:
      loglevel=logging.INFO
      loglevelStr = "INFO"
    else:
      loglevel=logging.WARNING
      loglevelStr = "WARNING"

    if not logFile:
      logging.basicConfig(level=loglevel)
      logging.info("MideaClient: logging to console.")
    else:
      logging.basicConfig(filename=logFile, level=loglevel)
      logging.info("MideaClient: logging to file: %s", logFile)

    logging.info("MideaClient: logging level set to: %s", loglevelStr)


    logging.debug("MideaClient: initializing MideaClient object")
    self.email    = email
    self.password = password
    self.sha256password = sha256password
    self.app_key  = self.APP_KEY
    self.app_id   = self.APP_ID
    self.src      = self.SRC

    logging.debug("MideaClient: creating MideaSecurity object using APPKEY=%s", self.app_key)
    self.security = MideaSecurity(self.app_key)

    self.current = None
    self.deviceStatus = None
    self.default_home = None


  def login(self):
    logging.debug("MideaClient: executing login()")

    #Receive loginId by calling '/v1/user/login/id/get' API endpoint
    result = self.__api_request("/v1/user/login/id/get", {"loginAccount": self.email})
    if not "loginId" in result:
      logging.error("MideaClient: ERROR trying to get login ID.")
      return -1

    login_id = result["loginId"]
    logging.info("MideaClient: login ID successfully retrived: %s", login_id)

    if self.password:
      encrypted_password = self.security.loginEncrypt(self.password, login_id)
    elif self.sha256password:
      encrypted_password = self.security.loginEncryptWithSHA256password(self.sha256password, login_id)
    else:
      logging.error("MideaClient: ERROR: a plaintext password or sha256 hash must be provided to log in.")
      return -1

    #Log-in
    #Receive accessToken and sessionId by calling '/v1/user/login' endpoint
    self.current = self.__api_request("/v1/user/login",
      {"loginAccount": self.email,
      "password": encrypted_password}
    )
    if not "accessToken" in self.current:
      logging.error("MideaClient: ERROR trying to log in.")
      return -1

    self.security.access_token = self.current["accessToken"]
    logging.info("MideaClient: successfully logged in.")
    logging.info("MideaClient: accessToken=%s", self.security.access_token)
    logging.info("MideaClient: sessionId=%s", self.current["sessionId"])
    return 1


  def listAppliances(self):
    if self.current is None:
      logging.warning("MideaClient::listAppliances: API session is not initialized: login first.")
      return None

    #Receive homegroupID by calling '/v1/homegroup/list/get' API endpoint
    result = self.__api_request("/v1/homegroup/list/get")

    if not "list" in result:
      logging.error("MideaClient::listAppliances: ERROR getting devices list.")
      return None

    #result["list"] is an array of dictionaries
    self.default_home = None
    for dict in result["list"]:
      if dict["isDefault"] == "1":
        self.default_home = dict
        logging.info("MideaClient::listAppliances: ID of default device: %s", dict["id"])

    if self.default_home is None:
      logging.error("MideaClient::listAppliances: ERROR: default device not found.")
      return None

    #Receive appliance info by calling '/v1/appliance/list/get' API endpoint
    result = self.__api_request("/v1/appliance/list/get",
        {"homegroupId": self.default_home["id"]}
      )

    return result["list"]


  def get_device_status(self, deviceId):
    if self.current is None:
      logging.warning("MideaClient::get_device_status: API session is not initialized: please login first.")
      return -1

    query = DataBodyDeHumiQuery()
    decoded_order = query.toBytes()

    #signed to unsigned bytes conversion
    decoded_order2 = []
    for i in decoded_order:
      if i < 0:
        decoded_order2.append(i+256)
      else:
        decoded_order2.append(i)

    #Header for switch-on/off & query-status command
    data = [90,90,1,0,89,0,32,0,1,0,0,0,39,36,17,9,13,10,18,20,218,73,0,0,0,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    data += decoded_order2
    data += [0]*16
    data[4] = len(data)

    #Convert array of int into a string (remove beginning and ending brackets)
    dataStr = ",".join(str(k) for k in data)
    decodedReplyStr = self.appliance_transparent_send(deviceId, dataStr)

    #Convert from comma-separated int string to int array
    decoded_reply = []
    for d in decodedReplyStr.split(","):
      n = int(d)
      decoded_reply.append(n)

    status = decoded_reply[40:]
    #Process response (get device status)
    response = DataBodyDeHumiResponse()
    self.deviceStatus = response.toMideaDehumidificationDeviceObject(status)
    logging.info("MideaClient::get_device_status: %s", self.deviceStatus.toString())

    return 1


  def send_poweron_command(self, deviceId):
    if self.current is None:
      logging.info("MideaClient::send_poweron_command: API session is not initialized: please login first.")
      return -1

    if self.deviceStatus is None:
      logging.info("MideaClient::send_poweron_command: device's status unknown: please call get_device_status() first.")
      return -1

    if self.deviceStatus.powerMode == 1:
      logging.info("MideaClient::send_poweron_command: device is already on.")
      return 1

    #Create new command request
    request = DataBodyDeHumiRequest()
    request.setDataBodyStatus(self.deviceStatus)
    request.powerMode = 1  #power-on command

    #Header for switch-on/off & query-status command
    header = [90,90,1,0,89,0,32,0,1,0,0,0,39,36,17,9,13,10,18,20,218,73,0,0,0,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    return self.__send_command(request, header, deviceId)


  def send_poweroff_command(self, deviceId):
    if self.current is None:
      logging.info("MideaClient::send_poweroff_command: API session is not initialized: please login first.")
      return 0

    if self.deviceStatus is None:
      logging.info("MideaClient::send_poweroff_command: device's status unknown: please call get_device_status() first.")
      return 0

    if self.deviceStatus.powerMode == 0:
      logging.info("MideaClient::send_poweroff_command: device is already off.")
      return 0

    #Create new command request
    request = DataBodyDeHumiRequest()
    request.setDataBodyStatus(self.deviceStatus)
    request.powerMode = 0  #power-off command

    #Header for switch-on/off & query-status command
    header = [90,90,1,0,89,0,32,0,1,0,0,0,39,36,17,9,13,10,18,20,218,73,0,0,0,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    return self.__send_command(request, header, deviceId)


  def send_fan_speed_silent_command(self, deviceId):
    self.send_fan_speed_command(deviceId, 20)

  def send_fan_speed_medium_command(self, deviceId):
    self.send_fan_speed_command(deviceId, 60)

  def send_fan_speed_high_command(self, deviceId):
    self.send_fan_speed_command(deviceId, 80)


  def send_fan_speed_command(self, deviceId, speed):
    if self.current is None:
      loggin.info("MideaClient::send_fan_speed_command: API session is not initialized: please login first.")
      return 0

    if self.deviceStatus is None:
      logging.info("MideaClient::send_fan_speed_command: device's status unknown: please call get_device_status() first.")
      return 0

    if self.deviceStatus.powerMode == 0:
      logging.info("MideaClient::send_fan_speed_command: device is off.")
      return 0

    if not (speed > 0 and speed < 100):
      logging.info("MideaClient::send_fan_speed_command: speed value is not valid.")
      return 0

    #Create new command request
    request = DataBodyDeHumiRequest()
    request.setDataBodyStatus(self.deviceStatus)
    request.windSpeed = speed  #set speed

    #Header for non-power-related command
    header = [90,90,1,0,91,0,32,0,10,0,0,0,10,10,10,3,2,11,18,20,218,73,0,0,0,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    return self.__send_command(request, header, deviceId)


  def send_target_humidity_command(self, deviceId, humidity):
    if self.current is None:
      logging.info("MideaClient::send_target_humidity_command: API session is not initialized: please login first.")
      return 0

    if self.deviceStatus is None:
      logging.info("MideaClient::send_target_humidity_command: device's status unknown: please call get_device_status() first.")
      return 0

    if self.deviceStatus.powerMode == 0:
      logging.info("MideaClient::send_target_humidity_command: device is off.")
      return 0

    if not (humidity >= 30 and humidity <= 70):
      logging.info("MideaClient::send_target_humidity_command: range for target humidity is not valid.")
      return 0

    #Create new command request
    request = DataBodyDeHumiRequest()
    request.setDataBodyStatus(self.deviceStatus)
    request.humidity_set = humidity  #set target humidity

    #Header for non-power-related command
    header = [90,90,1,0,91,0,32,0,10,0,0,0,10,10,10,3,2,11,18,20,218,73,0,0,0,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    return self.__send_command(request, header, deviceId)


  def send_target_mode_command(self, deviceId):
    self.send_mode_command(deviceId, 1)

  def send_continous_mode_command(self, deviceId):
    self.send_mode_command(deviceId, 2)

  def send_smart_mode_command(self, deviceId):
    self.send_mode_command(deviceId, 3)

  def send_dryer_mode_command(self, deviceId):
    self.send_mode_command(deviceId, 4)


  def send_mode_command(self, deviceId, mode):
    if self.current is None:
      logging.info("MideaClient::send_mode_command: API session is not initialized: please login first.")
      return 0

    if self.deviceStatus is None:
      logging.info("MideaClient::send_mode_command: device's status unknown: please call get_device_status() first.")
      return 0

    if self.deviceStatus.powerMode == 0:
      logging.info("MideaClient::send_mode_command: device is off.")
      return 0

    if not (mode > 0 and mode < 5):
      logging.info("MideaClient::send_mode_command: mode is not valid.")
      return 0

    #Create new command request
    request = DataBodyDeHumiRequest()
    request.setDataBodyStatus(self.deviceStatus)
    request.setMode = mode  #set Mode (1:TARGET_MODE, 2:CONTINOUS_MODE, 3:SMART_MODE, 4:DRYER_MODE)

    #Header for non-power-related command
    header = [90,90,1,0,91,0,32,0,10,0,0,0,10,10,10,3,2,11,18,20,218,73,0,0,0,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    return self.__send_command(request, header, deviceId)


  def send_ion_on_command(self, deviceId):
    if self.current is None:
      logging.info("MideaClient::send_ion_on_command: API session is not initialized: please login first.")
      return 0

    if self.deviceStatus is None:
      logging.info("MideaClient::send_ion_on_command: device's status unknown: please call get_device_status() first.")
      return 0

    if self.deviceStatus.powerMode == 0:
      logging.info("MideaClient::send_ion_on_command: device is off.")
      return 0

    if self.deviceStatus.ionSetSwitch == 1:
      logging.info("MideaClient::send_ion_on_command: Ion mode is alreay on.")
      return 0

    #Create new command request
    request = DataBodyDeHumiRequest()
    request.setDataBodyStatus(self.deviceStatus)
    request.ionSetSwitch = 1  #on

    #Header for non-power-related command
    header = [90,90,1,0,91,0,32,0,10,0,0,0,10,10,10,3,2,11,18,20,218,73,0,0,0,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    return self.__send_command(request, header, deviceId)


  def send_ion_off_command(self, deviceId):
    if self.current is None:
      logging.info("MideaClient::send_ion_off_command: API session is not initialized: please login first.")
      return 0

    if self.deviceStatus is None:
      logging.info("MideaClient::send_ion_off_command: device's status unknown: please call get_device_status() first.")
      return 0

    if self.deviceStatus.powerMode == 0:
      logging.info("MideaClient::send_ion_off_command: device is off.")
      return 0

    if self.deviceStatus.ionSetSwitch == 0:
      logging.info("MideaClient::send_ion_off_command: Ion mode is alreay off.")
      return 0

    #Create new command request
    request = DataBodyDeHumiRequest()
    request.setDataBodyStatus(self.deviceStatus)
    request.ionSetSwitch = 0  #off

    #Header for non-power-related command
    header = [90,90,1,0,91,0,32,0,10,0,0,0,10,10,10,3,2,11,18,20,218,73,0,0,0,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    return self.__send_command(request, header, deviceId)


  def __send_command(self, request, header, deviceId):
    decoded_order = request.toBytes()

    #signed to unsigned bytes conversion
    decoded_order2 = []
    for i in decoded_order:
      if i < 0:
        decoded_order2.append(i+256)
      else:
        decoded_order2.append(i)

    data = header
    data += decoded_order2
    data += [0]*16
    data[4] = len(data)

    #Convert array of int into a string (remove beginning and ending brackets)
    dataStr = ",".join(str(k) for k in data)
    decodedReplyStr = self.appliance_transparent_send(deviceId, dataStr)

    #Convert from comma-separated int string to int array
    decoded_reply = []
    for d in decodedReplyStr.split(","):
      n = int(d)
      decoded_reply.append(n)

    status = decoded_reply[40:]
    #Process response (get device status)
    response = DataBodyDeHumiResponse()
    self.deviceStatus = response.toMideaDehumidificationDeviceObject(status)
    logging.info("MideaClient::__send_command: %s", self.deviceStatus.toString())
    return 1



  def appliance_transparent_send(self, appliance_id, dataStr):
    """dataStr is a string of comma-separated integer"""
    dataArr = self.security.transcode(dataStr)
    dataStr2 = ",".join(str(k) for k in dataArr)

    encoded_command = self.__encode(dataStr2)
    logging.debug("MideaClient::appliance_transparent_send: encoded_command=%s", encoded_command)

    #Send command to applicance via API /v1/appliance/transparent/send endpoint
    result = self.__api_request("/v1/appliance/transparent/send",
        { "order": encoded_command,
          "funId": "0000",
          "applianceId": appliance_id })

    #print "result="+json.dumps(result)
    logging.debug("MideaClient::appliance_transparent_send: result=%s", json.dumps(result))

    #response = decode(response['reply']).split(',').map { |p| p.to_i & 0xff }
    return self.__decode(result["reply"])


  def __api_request(self, endpoint, _args={}):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')

    args = {}
    args["appId"] = self.app_id
    args["format"] = self.FORMAT
    args["clientType"] = self.CLIENT_TYPE
    args["language"] = self.LANGUAGE
    args["src"] = self.src
    args["stamp"] = int(st)
    args.update(_args)

    if self.current is not None:
      args["sessionId"] = str(self.current["sessionId"])

    #print endpoint
    argsStr = "&".join("=".join((str(k),str(v))) for k,v in args.items())
    #print argsStr
    sign = self.security.sign(endpoint, argsStr)
    args["sign"] = sign

    path = self.SERVER_URL+endpoint
    result = self.__send_api_request(path, args)
    return result


  def __send_api_request(self, uri, args):
    #Https POST request
    response = requests.post(uri, data=args)
    logging.debug("MideaClient::send_api_request: response=%s", response.text) #TEXT/HTML
    logging.info("MideaClient::send_api_request: response_status=%s, response_reason=%s", response.status_code, response.reason) #HTTP

    data = response.json()
    errorCodeStr = data["errorCode"]
    if errorCodeStr != "0":
      logging.error("MideaClient::send_api_request: errorCode=%s, errorMessage=\"%s\"", data["errorCode"], data["msg"])
      return "ERROR"
    else:
      if "result" in data:
        return data["result"]
      else:
        return "ERROR"


  def __encode(self, data):
    return self.security.aes_encrypt(data, self.security.data_key)


  def __decode(self, data):
    return self.security.aes_decrypt(data, self.security.data_key)
