# Library for EVA II PRO WiFi Smart Dehumidifier appliance
[![PyPI](https://img.shields.io/pypi/v/midea-inventor-lib.svg)](https://pypi.org/project/midea-inventor-lib/)
[![](https://img.shields.io/pypi/pyversions/midea-inventor-lib.svg)](https://pypi.org/project/midea-inventor-lib/)
[![](https://img.shields.io/pypi/l/midea-inventor-lib.svg)](https://pypi.org/project/midea-inventor-lib/)
[![](https://img.shields.io/pypi/wheel/midea-inventor-lib.svg)](https://pypi.org/pypi/midea-inventor-lib/)
[![](https://img.shields.io/pypi/status/midea-inventor-lib.svg)](https://pypi.org/pypi/midea-inventor-lib/)
[![](https://img.shields.io/pypi/implementation/midea-inventor-lib.svg)](https://pypi.org/pypi/midea-inventor-lib/)
[![<100kB](https://img.shields.io/github/languages/code-size/barban-dev/midea_inventor_dehumidifier.svg)](https://github.com/barban-dev/midea_inventor_dehumidifier)
[![<100kB](https://img.shields.io/github/repo-size/barban-dev/midea_inventor_dehumidifier.svg)](https://github.com/barban-dev/midea_inventor_dehumidifier)
[![Build status](https://travis-ci.com/barban-dev/midea_inventor_dehumidifier.svg?branch=master)](https://travis-ci.com/barban-dev/midea_inventor_dehumidifier)
[![Known Vulnerabilities](https://snyk.io/test/github/barban-dev/midea_inventor_dehumidifier/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/barban-dev/midea_inventor_dehumidifier?targetFile=requirements.txt)
[![HitCount](http://hits.dwyl.io/barban-dev/midea_inventor_dehumidifier.svg)](http://hits.dwyl.io/barban-dev/midea_inventor_dehumidifier)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=5E7ULVFGCGKU2&source=url)


Author: Andrea Barbaresi =2018, 2019=

Licence: GPLv3

This repo contains the python package ***midea_inventor_lib*** that implements a client-side library to connect to the Web API provided by Midea/Inventor, in order to remotely control an **EVA II PRO WiFi Smart Dehumidifier device**.

Info about the dehumidifier appliance can be found [here.](https://www.inventorappliances.com/dehumidifiers/eva-ii-pro-wi-fi-20l)

You can buy the smart dehumidifier appliance (WiFi version) on Amazon (the two links below contain my referral code):
* [Amazon.co.uk](https://www.amazon.co.uk/gp/product/B07665CCSM/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=barban0d-21&creative=6738&linkCode=as2&creativeASIN=B07665CCSM&linkId=a7408b12a09679586e1816acc3c9d74b)
* [Amazon.it](https://www.amazon.it/gp/product/B075486X31/ref=as_li_tl?ie=UTF8&camp=3414&creative=21718&creativeASIN=B075486X31&linkCode=as2&tag=barban03-21&linkId=33e8ff818aaa4b45f0c320e6661773b2)


Target devices
--------------
Even though the library has been designed to generically address any kind of existing MIDEA devices, ***please note that at the moment the implemented functionalities work on the dehumidifier appliance only (0xA1 type devices).***

If you are interested in developing code that is able to control Midea/Inventor Air Condition systems (0xAC type devices), you can have a look at ***midea-air-condition*** Ruby&Rails library by **Balazs Nadasdi** available [here.](https://github.com/yitsushi/midea-air-condition)


Prerequisites
-------------
In order to control the EVA II PRO WiFi Smart Dehumidifier appliance using the provided Python library, first of all it is necessary to download and install the official App, in order to register a valid user to the cloud platform (a valid email address is required). 
The official companion Apps are available on Google's and Apple's App Stores:
* [Google Play](https://play.google.com/store/apps/details?id=com.inventor)
* [Apple Store](https://itunes.apple.com/gr/app/invmate-ii/id1109243423)

Once connected with valid credentials (i.e. email address and password), your home device has to be added to the list of configured devices using the App (please refer to the manual of the official App to accomplish this task).

Once having a valid registered user and the home device configured, you can start to use the python library instead of the offical App to control the device via Internet (both the client when the library is installed and the home device should be connected to the Internet).


Installation
------------
Install from PyPi using [pip](http://www.pip-installer.org/en/latest), a package manager for
Python.
```
pip install midea-inventor-lib
```
Don't have pip installed? Try installing it, by running this from the
command line:
```
$ curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python
```
Or, you can [download the source code (ZIP)](https://github.com/barban-dev/midea_inventor_dehumidifier/zipball/master) and then run:
```
python setup.py install
```
You may need to run the above commands with ``sudo``.


Getting started
---------------
Minimal steps to use the library in your python code are reported below:

**Step 1: Include the python package**
```python
from midea_inventor_lib import MideaClient
```
**Step 2: Instantiate the MideaClient object**

Using clear-text password:
```python
client = MideaClient("user.example@gmail.com", "myPassword", "")
```
Using password's sha-256 hash:
```python
client = MideaClient("user.example@gmail.com", "", "76549b827ec46e705fd03831813fa52172338f0dfcbd711ed44b81a96dac51c6")
```
**Enable logging (optional):**

You can enable logging by setting the 'verbose' parameter to True (default is False) in the MideaClient constructor. 
Set 'debug' parameter to True in order to log debugging messages too (default is False).
Set 'logfile' string parameter to a full-path filename in order to make the library log messages into a file instead of using the console (default).
E.g.:
```python
_email = "user@example.com"
_password = "passwordExample"
_sha256password = ""
_verbose = True		#Enable logging
_debug = False		#Disable debug messages
_logfile = ""		#Log to console (default)
client = MideaClient(_email, _password, _sha256password, _debug, _verbose, _logfile)
```
**Step 3: Activate a new session by logging in**
```python
res = client.login()
if res == -1:
  print "Login error: please check log messages."
else:
  sessionId = client.current["sessionId"]
```
**Step 4: Get the target deviceId by retrieving the list of configured appliances**
```python
appliances = {}
appliances = client.listAppliances()
for a in appliances:
  print "[id="+a["id"]+" type="+a["type"]+" name="+a["name"]+"]"
```
**Step 5: Send commands to control the target device**
Get the device state:
```python
res = client.get_device_status(deviceId)
if res == 1:
  print client.deviceStatus.toString()
```
Power-on:
```python
res = client.send_poweron_command(deviceId)
if res:
  print client.deviceStatus.toString();
```
Power-off:
```python
res = client.send_poweroff_command(deviceId)
if res:
  print client.deviceStatus.toString();
```
Set Ion on:
```python
res = client.send_ion_on_command(deviceId)
if res:
  print client.deviceStatus.toString();
```
Set Ion off:
```python
res = client.send_ion_off_command(deviceId)
if res:
  print client.deviceStatus.toString();
```
Set fan speed:
```python
if speed > 0 and speed < 100:
  res = client.send_fan_speed_command(deviceId, speed)
  if res:
    print client.deviceStatus.toString();
```
Set target humidity:
```python
if hum >= 30 and hum <= 70:
  res = client.send_target_humidity_command(deviceId, hum)
  if res:
    print client.deviceStatus.toString();
```
Set operation mode:
```python
if mode > 0 and mode < 5:
  res = client.send_mode_command(deviceId, mode)  #set Mode (1:TARGET_MODE, 2:CONTINOUS_MODE, 3:SMART_MODE, 4:DRYER_MODE)
  if res:
    print client.deviceStatus.toString();
```
Set updated status (usefull to update multiple attributes at one):
```python
status =client.get_device_status(deviceId)  #get current status
#Update status
status.ionSetSwitch = 1   #Ion on
status.setMode = 1        #target-mode
res = self._client.send_update_status_command(self._device["id"], status)
if res:
  print client.deviceStatus.toString();
```

Client example
--------------
This repo also contains a fully working client (***dehumi_control.py***) that demonstrates how to use the ***midea_inventor_lib*** library in order to control the EVA II PRO WiFi Smart Dehumidifier appliance via a Command Line Interface.

To use the client, the email address of a registered user and the associated password have to be provided via command line parameters (either clear-text password or password's sha-256 hash has to be provided using the '-p' or '-s' options):
```
# python dehumi_control.py  -h
Usage:dehumi_control.py -e <email_address> -p <cleartext password> -s <sha256_password> -l <logfile> [-h] [-v] [-d]
```

Home Assistant custom-component
-------------------------------
***[NEW]*** Custom-component for the Home Assistant platform can be found on ``/homeassistant`` folder.
In order to activate the component, follow these steps:

**Step 1: Copy necessary files to your HA's configuration shared folder** 

Copy ***the content of*** ``/homeassistant`` folder (***not the folder itself***), ***including subfolders***, on your HA's configuration shared folder.

Copy ``/midea_inventor_lib`` folder on ``\deps\lib\python3.6\site-packages\`` of your HA's configuration shared folder.

Final result should look similar to this:
```
\\<ha_ip_address>
    └── config
        ├── custom_components
        │   ├── climate
        │   │   └── midea_dehumi.py
        │   ├── midea_dehumi.py
        │   └── sensor
        │       └── midea_dehumi.py
        └── deps
            └── lib
                └── python3.6
                    └── site-packages
                        └── midea_inventor_lib
                            └── libfiles...
```

**Step 2: Activate midea_dehumi platform on your HA's configuration file**

Add the following section in your ``configuration.yaml``
```
midea_dehumi:
  username: user@example.com
  password: passwordExample
```
As usual, you can hide your secret password by means of ``!secret`` notation by specifing it in ``secrets.yaml``

Alternatively, if you prefer, ``sha256password`` parameter can be used instead of the ``password`` one to specify password's sha-256 hash
```
midea_dehumi:
  username: user@example.com
  sha256password: cf76d55503cdee3....
```
**Step 3: Activate DEBUG-level logging (optional)**

It is highly suggested to activate DEBUG-level logging for the three components the midea_dehumi platform consists of. This let you perform troubleshooting analysis if the component doesn't work as expected.
```
logger:
  default: info
  logs:
    custom_components.midea_dehumi: debug
    custom_components.climate.midea_dehumi: debug
    custom_components.sensor.midea_dehumi: debug
```
** Step 4: Restart HA**

You can restart HA by using one of your preferred method (e.g. using reboot button on Settings>General>Server Management og HA's Web dashboard).

If everything is ok, you will find the following two new entities in your HA dashboard:

* **climate.midea_dehumi_*[Device_ID]***
* **sensor.midea_dehumi_*[Device_ID]*_humidity**

By means of the climate entity, you can control your appliance whereas the sensor reports the detected current humidity of your environment.

If you cannot find the entities reported above, check the logs generated by HA to track the issue.

Internals 
---------
***You can skip this part if you are not interested in technical details concerning the format of the API messages used by the library.***

Official companion Apps for Android and IOS platforms are based on the midea-SDKs made available by Midea Smart Technology Co., Ltd.:
* [ios-sdk](https://github.com/midea-sdk-org/ios-sdk)
* [android-sdk](https://github.com/midea-sdk-org/android-sdk)

According to the SDK's documentation, "MideaSDK is a software develop kit maintained by MSmart. You can develop your own APP, Smart Hardware or Smart TV based on this SDK to control the smart appliances produced by Midea."

Official documentation for the open API can be found here (chinese language only):
https://github.com/midea-sdk/midea-sdk.github.io/tree/master/api

Apart Androd and IOS platforms, no other environment is currently officially supported. In order to develop the client-side library for all the platform supporting Python, I used a Man-In-The-Middle Web Proxy as a packet sniffer to understand the basics on the API messages exchanged between the offical Android client and the Midea cloud Server.

Web API server can be reached via ```https://mapp-appsmb.com/<endpoint>``` (POST web requests shoud be used).

A brief description of the most relevant endpoints follows:

```/v1/user/login/id/get``` endpoint with 'loginAccount' parameter is used to get 'loginId' parameter (different for each session).

```/v1/user/login``` endpoint with 'password' parameter is used to perform the login ('accessToken' and 'sessionId' parameters are returned). The password parameter sent by the client is SHA-256 hash of a string derived from 'loginId', 'password' and 'appKey' parameters.

```/v1/appliance/user/list/get``` endpoint is used to retrieve the list of configured devices together withh all the associated parameters ('name', 'modelNumber', 'activeStaus', 'onlineStatus', etc.)

```/v1/appliance/transparent/send``` endpoint with the 'order' parameter is used to control the home device (the 'reply' parameter is returned). Both the 'order' and 'reply' parameters are AES encryted; the encryption/decryption key used by AES is derived from the 'APP_key' parameter (constant string) and the 'accessToken' parameter returned when logging in. The revelant part of code used for the encription and decryption tasks can be found in the **MideaSecurity** class in **midea_security.py** file.

For Further Studies (FFS)
-------------------------
At the moment, the client-side Python library can control a dehumidifier appliance by sending API messages to the cloud Server that talks to the home device. Both the client and the home device need Internet access in this cloud-to-cloud scenario. 
The possibility to control the home device locally (i.e. the possibility to let the client to send API messagges directly to the home device) when both the client and the home device are associated to the same WiFi network is FFS.

How to contribute
-----------------
If you can code in Python and you are interested in improving and expanding this work, feel free to clone this repo. Drop me a line if you wish to merge your modifications in my repo too.

Disclaimer
----------
Besides owning an EVA II PRO WiFi device, I have no connection with Midea/Inventor company. This library was developed for my own personal use and shared to other people interested on Internet of Things systems and domotic platforms. This software is provided as is, without any warranty, according to the GNU Public Licence version 3.

Donations
---------
If this project helps you to reduce time to develop your code, you can make me a donation.

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=5E7ULVFGCGKU2&source=url)

