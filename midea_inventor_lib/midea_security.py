import hashlib
import binascii
import logging
from Crypto.Cipher import AES


class MideaSecurity:

  def __init__(self, app_key=None, access_token=None):
    logging.debug("MideaSecurity: initializing MideaSecurity object.")
    self.app_key = app_key
    self.access_token = access_token


  @property
  def data_key(self):
    if self.app_key is None:
      logging.error("MideaSecurity: ERROR: app_key is not initialized.")
      return ""

    if self.access_token is None:
      logging.error("MideaSecurity: ERROR: access_token is not initialized")
      return ""

    m = hashlib.md5()
    m.update(self.app_key.encode('utf-8'))
    md5appkey = m.hexdigest()

    logging.debug("MideaSecurity: md5(app_key)=%s", md5appkey[:16])

    msg = self.aes_decrypt(self.access_token, md5appkey[:16])
    return msg


  def aes_decrypt(self, data, key):
    logging.debug("MideaSecurity: executing aes_decrypt()")
    enc_data = binascii.unhexlify(data)
    #logging.debug("MideaSecurity: enc_data=%s", enc_data)
    blocks = [enc_data[i:i+16] for i in range(0, len(enc_data), 16)]

    final = ""
    for b in blocks:
      #Python3 support
      #cipher = AES.new(key, AES.MODE_ECB)
      #final += cipher.decrypt(b)
      cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
      final += cipher.decrypt(b).decode('utf-8')
      #logging.debug("MideaSecurity: block=%s", final)

    pad = ord(final[-1])
    return final[0:len(final)-pad]



  def loginEncrypt(self, password, login_id):
    """Encrypt login information"""

    if self.app_key is None:
      logging.error("MideaSecurity: ERROR: app_key is not initialized.")
      return ""

    #Python3 support
    #hash_obj1 = hashlib.sha256(password)
    hash_obj1 = hashlib.sha256(password.encode('utf-8'))

    #logging.debug("---------------------------------")
    #logging.debug(hash_obj1.hexdigest())
    #logging.debug("---------------------------------")

    strToHash = login_id+hash_obj1.hexdigest()+self.app_key
    #Python3 support
    #hash_obj2 = hashlib.sha256(strToHash)
    hash_obj2 = hashlib.sha256(strToHash.encode('utf-8'))
    return hash_obj2.hexdigest()


  def loginEncryptWithSHA256password(self, sha256password, login_id):
    """Encrypt login information"""

    if self.app_key is None:
      logging.error("MideaSecurity: ERROR: app_key is not initialized.")
      return ""

    strToHash = login_id+sha256password+self.app_key

    logging.debug("MideaSecurity: strToHash=%s", strToHash)

    #Python3 support
    #hash_obj2 = hashlib.sha256(strToHash)
    hash_obj2 = hashlib.sha256(strToHash.encode('utf-8'))
    return hash_obj2.hexdigest()



  def sign(self, path, args):
    """Sign API message (args is a string key1=token1&key2=token2..."""

    logging.debug("MideaSecurity: executing sign() method.")
    if self.app_key is None:
      logging.error("MideaSecurity: ERROR: app_key is not initialized.")
      return ""

    #Re-ordering keys values
    args_array = args.split('&')
    args_array.sort()
    logging.debug("MideaSecurity: args_array=%s", args_array)

    query = ""
    for token in args_array:
      query += token + "&"

    query = query[:-1]
    #logging.debug(query)

    content = path+query+self.app_key
    #logging.debug(content)

    #Python3 support
    #hash_obj = hashlib.sha256(content)
    hash_obj = hashlib.sha256(content.encode('utf-8'))
    return hash_obj.hexdigest()


  def signDict(self, path, args):
    """Sign API message (args is a dictionary)"""

    argsStr = "&".join("=".join((str(k),str(v))) for k,v in args.items())
    #logging.debug(argsStr)

    return self.sign(path, argsStr)


  def aes_encryptArray(self, data, key):
    """Encrypt data using key (data is an Array of int)"""

    #Convert array of int into a string (remove beginning and ending brackets)
    dataStr = ",".join(str(k) for k in data)
    #logging.debug(dataStr)

    return self.aes_encrypt(dataStr, key)


  def aes_encrypt(self, dataStr, key):
    """Encrypt dataStr using key (dataStr is a string of comma-separated integers)"""

    logging.debug("MideaSecurity: executing aes_encrypt()")
    cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)

    blocks = [dataStr[i:i+16] for i in range(0, len(dataStr), 16)]
    if len(blocks[-1]) < 16:
      pad = 16 - len(blocks[-1])
      padStr = chr(pad)*pad
      #Pad last block to 16 chars length
      blocks[-1] += padStr
    else:
      #Add another 16 bytes long block
      blocks.append(chr(16)*16)

    #logging.debug(blocks)

    #Python3 support
    #final = ""
    final = b""
    for b in blocks:
      #Python3 support
      #cipher = AES.new(key, AES.MODE_ECB)
      cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
      final += cipher.encrypt(b.encode('utf-8'))

    #logging.debug(final)

    enc_data = binascii.hexlify(final)
    logging.debug("MideaSecurity: enc_data=%s", enc_data)

    #Python3 support
    #return enc_data
    return enc_data.decode('utf-8')



  def transcode(self, dataStr):
    newdata = []
    for d in dataStr.split(","):
      n = int(d)
      if n >= 128:
        newdata.append(n - 256)
      else:
        newdata.append(n)
    return newdata


  def transcodeArray(self, data):
    newdata = []
    for d in data:
      if d >= 128:
        newdata.append(d - 256)
      else:
        newdata.append(d)
    return newdata


  def transencode(self, dataStr):
    newdata = []
    for d in dataStr.split(","):
      n = int(d)
      if n < 0:
        newdata.append(n + 256)
      else:
        newdata.append(n)
    return newdata


  def transencodeArray(self, data):
    newdata = []
    for d in data:
      if n < 0:
        newdata.append(n + 256)
      else:
        newdata.append(n)
    return newdata

