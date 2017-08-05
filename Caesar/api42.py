#!/usr/bin/python
# -*- coding: utf-8 -*-

DEBUG = True
GET_NEW_DATA = False
PRINT_LOG = False

import requests
import json
import time
import os
from student import *


def open_file(name):
    try:
        file = open(name, 'r')
    except:
        print 'bad file: ' + str(name)
        sys.exit(0)
    text = file.read()
    file.close()
    return text


def check(text):
    if text is not None:
        return text.encode('utf-8').strip()
    else:
        return "BAD TEXT"


def as_corrector(API42, USER, token):
    URL = "/v2/users/" + USER + "/scale_teams/as_corrector"
    if GET_NEW_DATA:
        result = get_info(API42, URL, token)
        result = result.encode('utf-8')
        write_to_file('data_' + USER, result)
        result = json.loads(result)
    else:
        result = open_file('data_' + USER)
        result = json.loads(str(result))
        write_to_file('json_data_' + USER, json.dumps(result, indent=4))
    return result


def print_log(USER, result):
    if PRINT_LOG:
        zero = 0
        corrections = 0
        for each in result:
            print "student(s): ",
            for person in each['correcteds']:
                print check(person['login']),
            print "\nproject: " + check(each['scale']['name'])
            print "corrector: " + check(each['comment'])
            print "feedback: " + check(each['feedback'])
            if each['final_mark'] <= 50:
                zero = zero + 1
            else:
                corrections = corrections + 1
            print "final_mark: " + str(each['final_mark'])
            print "--------------------"
        print 'negative: ' + str(zero)
        print 'positive: ' + str(corrections)
        print 'all: ' + str(zero + corrections)

class Api42:
    """Class providing wrapper for api calls to the 42 school API"""
    def __init__(self, id42, secret42, api42='https://api.intra.42.fr', debug=False, logs=True, dataFolder='data'):
        self.id = str(id42).strip()
        self.secret = str(secret42).strip()
        self.debug = debug
        self.api42 = str(api42).strip()
        self.dataFolder = dataFolder.strip()
        self.__debugCounter = 1
        self.__lastStatusCode = -1
        self.__logs = logs
        self.__logsFile = 'logs'
        self.__folderExist(self.dataFolder)
        if self.__logs:
            self.__writeToFile(self.__logsFile, '---------------------\n', typeOfRecord='a')
        self.__getToken()

    def __debug(self, text):
        """Print debug info, if gebug is enabled"""
        if self.__logs:
            self.__writeToFile(self.__logsFile, ('api [{}] >> ' +  text + '\n').format(self.__debugCounter), typeOfRecord='a')
        if self.debug:
            print str('api [{}] >> ' +  text).format(self.__debugCounter)
        self.__debugCounter += 1

    def __folderExist(self, folderName):
        """Check folder exist or not"""
        if os.path.exists(folderName):
            return
        self.__debug('creating folder: ' + folderName)
        os.mkdir(folderName)

    def __writeToFile(self, fileName, data, typeOfRecord='w'):
        """Write the raw user data to the specific folder"""
        if typeOfRecord == 'w':
            self.__debug('writing to file: ' + fileName)
        file = open(fileName, typeOfRecord)
        file.write(data)
        file.close

    def __connected(self, statusCode):
        """Check status of connection"""
        self.__lastStatusCode = statusCode
        if int(statusCode) == 200:
            self.__debug('connected: ' + str(statusCode))
            return True
        else:
            self.__debug('not connected: ' + str(statusCode))
            return False

    def __getToken(self):
        """Private function, get token from the server"""
        url = '/oauth/token'
        args = {'grant_type=client_credentials', 'client_id=' + self.id, 'client_secret=' + self.secret}
        self.__debug('get token request to ' + self.api42 + url)
        timestart = time.time()
        try:
            ret = requests.post(self.api42 + url + "?%s" % "&".join(args))
            timeend = time.time()
            self.__connected(ret.status_code)
        except:
            self.__debug('bad token')
            return None
        self.__debug('response' + '%6.2f' % ((timeend - timestart)) + ' seconds')
        self.__debug('token received')
        text = json.loads(ret.text)
        token = ['access_token=' + text['access_token'].encode("ascii"), 'token_type=' + text['token_type'].encode("ascii")]
        self.token = token
        return self.token

    def __makeRequest(self, url, pageRequest=None):
        """Make one request to the server"""
        try:
            if pageRequest is not None:
                self.__debug(self.api42 + url + '?%s' % "&".join(self.token) + "&page[size]=100" + "&page[number]=" + str(pageRequest))
                timestart = time.time()
                res = requests.get(self.api42 + url + '?%s' % "&".join(self.token) + "&page[size]=100" + "&page[number]=" + str(pageRequest))
            else:
                self.__debug('request to ' + self.api42 + url + '?%s' % "&".join(self.token))
                timestart = time.time()
                res = requests.get(self.api42 + url + '?%s' % "&".join(self.token))
            timeend = time.time()
            self.__debug('response' + '%6.2f' % ((timeend - timestart)) + ' seconds')
        except:
            self.__debug('bad request')
            return None
        res.encoding = 'UTF-8'
        return res.text.encode('utf8')

    def __makeRequests(self, url):
        """Make multiple requests to the server"""
        pageNumber = 0
        result = '['
        text = '[]'
        timestart = time.time()
        while True:
            self.__debug('page number (multi request): ' + str(pageNumber))
            try:
                text = self.__makeRequest(url, pageNumber)
            except:
                self.__debug('something wrong')
                return None
            if text == '[]':
                break
            result = result + text[1:-1] + ','
            pageNumber = pageNumber + 1
        timeend = time.time()
        self.__debug('total time: ' + str(timeend - timestart))
        result = result[:-1] + ']'
        return result

    def getUser(self, login='akalmyko'):
        """Get info about specific user"""
        self.__debug('creating user: ' + login)
        url = '/v2/users/' + login
        login = str(login).strip()
        user = Student(login)
        user.userData = json.loads(self.__makeRequest(url))
        if len(user.userData) == 0:
            self.__debug('bad login: ' + login)
            return None
        self.__writeToFile(self.dataFolder + '/' + login + '_data', json.dumps(user.userData, indent=4, sort_keys=True))
        user.userId = user.userData['id']
        user.campus = user.userData['campus']
        user.url = user.userData['url']
        user.image_url = user.userData['image_url']
        user.displayname = user.userData['displayname']
        user.first_name = user.userData['first_name']
        user.last_name = user.userData['last_name']
        user.phone = user.userData['phone']
        user.email = user.userData['email']
        try:
            user.level = user.userData['cursus_users'][0]['level']
        except:
            pass
        # user.achievements = user.userData['achievements']
        # user.campus = user.userData['campus']
        return user

    def getUsers(self, campus=7):
        """Get the list of the users in campus"""
        self.__debug('getUsers')
        url = '/v2/campus/' + str(campus).strip() + '/users'
        text = self.__makeRequests(url)
        result = json.loads(text)
        listOfUsers = []
        for each in result:
            listOfUsers.append(each['login'])
        # self.__writeToFile('users_list', json.dumps(result, indent=4, sort_keys=True))
        return listOfUsers
