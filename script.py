#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json
import sys
import os
import time
from Caesar import *

def main():
    id42 = 'c4b496ced4be232b6ec55a1738cb188ca8ec754251c142919e16abfaed18ff94'
    secret42 = '31a701451b2cbc9c1c896bf5cb3d954e7c679cef1d66e79283771d64bd2754fe'
    api = Api42(id42, secret42, debug=True)
    user = api.getUser('akalmyko')
    user.printInfo()

    # token = getToken(API42)
    # result = as_corrector(API42, USER, token)
    # print_log(USER, result)

if __name__ == '__main__':
    os.system('clear')
    main()

# def connected(status):
#     if int(status) == 200:
#         if DEBUG: print 'connected: ' + str(status)
#         return True
#     else:
#         if DEBUG: print 'not connected: ' + str(status)
#         return False

# def getToken(API42):
#     ID = "c4b496ced4be232b6ec55a1738cb188ca8ec754251c142919e16abfaed18ff94"
#     SECRET = "31a701451b2cbc9c1c896bf5cb3d954e7c679cef1d66e79283771d64bd2754fe"
#     URL = '/oauth/token'
#     args = {
#                 'grant_type=client_credentials',
#                 'client_id=' + ID,
#                 'client_secret=' + SECRET
#             }
#     try:
#         timestart = time.time()
#         ret = requests.post(API42.strip() + URL.strip() + "?%s" % "&".join(args))
#         timeend = time.time()
#         if DEBUG: print('response' + '%6.2f' % ((timeend - timestart)) + ' seconds')
#         if not connected(ret.status_code):
#             sys.exit(0)
#     except:
#         if DEBUG: print 'bad token'
#         sys.exit(0)
#     text = json.loads(ret.text)
#     token = [
#                 'access_token=' + text['access_token'].encode("ascii"),
#                 'token_type=' + text['token_type'].encode("ascii"),
#             ]
#     return token

# def get_info(API42, URL, token):
#     if DEBUG: print (API42.strip() + URL.strip() +'?%s' % "&".join(token))
#     ret = requests.get(API42.strip() + URL.strip() +'?%s' % "&".join(token))
#     return ret
#
# def main():
#     API42 = 'https://api.intra.42.fr'
#     # URL = "/v2/users/akalmyko"
#     URL = "/v2/users/akalmyko/scale_teams/as_corrector"
#     token = getToken(API42)
#     result = get_info(API42, URL, token)
#     result = json.loads(result.text)
#     for each in result:
#         print each["correcteds"][0]['login']
