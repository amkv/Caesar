#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import os
from Caesar import *

def main():
    id42 = 'your_id'
    secret42 = 'your_secret'
    api = Api42(id42, secret42, debug=True)
    # user = api.getUser('akalmyko')
    # user.printUserInfo()
    users = api.getUsers()
    for each in users:
        api.getUser(each)

    # token = getToken(API42)
    # result = as_corrector(API42, USER, token)
    # print_log(USER, result)


if __name__ == '__main__':
    os.system('clear')
    main()
