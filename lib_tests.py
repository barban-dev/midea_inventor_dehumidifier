import sys
from midea_inventor_lib import MideaSecurity

TOTAL_TESTS_NUM = 7
APP_KEY = "3742e9e5842d4ad59c2db887e12449f9"


def test_result(numtest, targetClassName, success=True):
  if success:
    print("Test num. "+str(numtest)+" ("+targetClassName+"): [OK]")
  else:
    print("Test num. "+str(numtest)+" ("+targetClassName+"): [FAILED]")
    sys.exit(1)


def do_test(numtest):
  if numtest == 1:
    # Test num. 1
    access_token = "f4fe051b7611d07d54a7f0a5e07ca2beb920ebb829d567559397ded751813801"
    security = MideaSecurity(APP_KEY, access_token)
    if security.data_key == "23f4b15525824bc3":
      test_result(numtest, "MideaSecurity")
    else:
      test_result(numtest, "MideaSecurity", False)
  elif numtest == 2:
    # Test num. 2
    access_token = "f4fe051b7611d07d54a7f0a5e07ca2beb920ebb829d567559397ded751813801"
    security = MideaSecurity(APP_KEY, access_token)
    reply = "02940d3220c4a1a1fcfb4e8593a93c0facebf2d3d170c089f8c9d7274f8048462f8d8ac5ab6b8073382dbc9b9dcc63c293b3dffc38a7bb66832fb4ae3514a40873768e0b3c6cc653c5802496e2b271cba2bfc89ca102623370e8901845328834c53227ac9ea088605ee64825413692b1df952de8baf0dd76ecd34202f91dcc4908baeaf21a29ca4c11203f2c984fd282ec23185ce83c99215494482d87bebdcb3b31f06f44f810c15404be14b1ed8bf090f1e835d796869adf20bf35ff5b7ebc73768e0b3c6cc653c5802496e2b271cb6eb166994a36e79b29551a0dc87fed53"
    decoded_reply = "90,90,1,0,91,0,32,-128,1,0,0,0,0,0,0,0,0,0,0,0,-38,73,0,0,0,16,0,0,0,0,0,0,0,0,0,0,1,0,0,0,-86,34,-95,0,0,0,0,0,3,3,-56,1,4,80,127,127,0,35,0,64,0,0,0,0,0,0,61,86,0,0,0,0,-92,-85,-41,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
    decoded_reply2 = security.aes_decrypt(reply, security.data_key)
    if decoded_reply == decoded_reply2:
      test_result(numtest, "MideaSecurity")
    else:
      test_result(numtest, "MideaSecurity", False)
  elif numtest == 3:
    # Test num. 3
    access_token = "87836529d24810fb715db61f2d3eba2ab920ebb829d567559397ded751813801"
    security = MideaSecurity(APP_KEY, access_token)
    query = [90,90,1,0,89,0,32,0,1,0,0,0,39,36,17,9,13,10,18,20,-38,73,0,0,0,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-86,32,-95,0,0,0,0,0,3,3,65,33,0,-1,3,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,11,36,-92,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    encStr = "7c8911b6de8e29fa9a1538def06c9018a9995980893554fb80fd87c5478ac78b360f7b35433b8d451464bdcd3746c4f5c05a8099eceb79aeb9cc2cc712f90f1c9b3bb091bcf0e90bddf62d36f29550796c55acf8e637f7d3d68d11be993df933d94b2b43763219c85eb21b4d9bb9891f1ab4ccf24185ccbcc78c393a9212c24bef3466f9b3f18a6aabcd58e80ce9df61ccf13885ebd714595df69709f09722ff41eb37ea5b06f727b7fab01c94588459ccf13885ebd714595df69709f09722ff32b544a259d2fa6e7ddaac1fdff91bb0"
    encStr2 = security.aes_encryptArray(query, security.data_key)
    if encStr == encStr:
      test_result(numtest, "MideaSecurity")
    else:
      test_result(numtest, "MideaSecurity", False)
  elif numtest == 4:
    # Test num. 4
    access_token = "87836529d24810fb715db61f2d3eba2ab920ebb829d567559397ded751813801"
    security = MideaSecurity(APP_KEY, access_token)
    query = "90,90,1,0,89,0,32,0,1,0,0,0,39,36,17,9,13,10,18,20,-38,73,0,0,0,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-86,32,-95,0,0,0,0,0,3,3,65,33,0,-1,3,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,11,36,-92,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
    encStr = "7c8911b6de8e29fa9a1538def06c9018a9995980893554fb80fd87c5478ac78b360f7b35433b8d451464bdcd3746c4f5c05a8099eceb79aeb9cc2cc712f90f1c9b3bb091bcf0e90bddf62d36f29550796c55acf8e637f7d3d68d11be993df933d94b2b43763219c85eb21b4d9bb9891f1ab4ccf24185ccbcc78c393a9212c24bef3466f9b3f18a6aabcd58e80ce9df61ccf13885ebd714595df69709f09722ff41eb37ea5b06f727b7fab01c94588459ccf13885ebd714595df69709f09722ff32b544a259d2fa6e7ddaac1fdff91bb0"
    encStr2 = security.aes_encrypt(query, security.data_key)
    if encStr == encStr:
      test_result(numtest, "MideaSecurity")
    else:
      test_result(numtest, "MideaSecurity", False)
  elif numtest == 5:
    # Test num. 5
    security = MideaSecurity(APP_KEY, "")
    enc_password = "f6a8f970344eb9b84f770d8eb9e8b511f4799bbce29bdef6990277783c243b5f"
    enc_password2 = security.loginEncrypt("passwordExample", "592758da-e522-4263-9cea-3bac916a0416")
    if enc_password == enc_password2:
      test_result(numtest, "MideaSecurity")
    else:
      test_result(numtest, "MideaSecurity", False)
  elif numtest == 6:
    # Test num. 6
    security = MideaSecurity(APP_KEY, "")
    sign = "f6755b1e3d231b3c96943f89b85c244fdcd7080eb4414b119fb15cb2a5d50082"
    sign2 = security.sign("/v1/user/login/id/get", "loginAccount=example-user@gmail.com&clientType=1&src=17&appId=1017&format=2&stamp=20181113211528&language=en_US")
    if sign == sign2:
      test_result(numtest, "MideaSecurity")
    else:
      test_result(numtest, "MideaSecurity", False)
  elif numtest == 7:
    # Test num. 7
    security = MideaSecurity(APP_KEY, "")
    sign = "f6755b1e3d231b3c96943f89b85c244fdcd7080eb4414b119fb15cb2a5d50082"
    args = {"loginAccount":"example-user@gmail.com", "appId":1017, "clientType":1, "format":2, "language":"en_US", "src":17, "stamp":20181113211528}
    sign2 = security.signDict("/v1/user/login/id/get", args)
    if sign == sign2:
      test_result(numtest, "MideaSecurity")
    else:
      test_result(numtest, "MideaSecurity", False)



def main():
  print("**********************************************************************")
  print("lib_test.py: Performing low-lovel tests on midea_inventor_lib classes.")
  print("**********************************************************************")
  numtest = 1
  while (numtest <= TOTAL_TESTS_NUM):
    do_test(numtest)
    numtest +=1

  print("All tests passed.")
  sys.exit(0)


#Call main() function
if __name__ == "__main__":
    main()




