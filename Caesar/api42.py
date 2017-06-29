#!/usr/bin/python
# -*- coding: utf-8 -*-

DEBUG = True
GET_NEW_DATA = False
PRINT_LOG = False

def get_info(API42, URL, token):
    # if DEBUG: print (API42.strip() + URL.strip() +'?%s' % "&".join(token))
    page = 0
    ret = '['
    while True:
        # if DEBUG: print "page: " + str(page)
        try:
            timestart = time.time()
            res = requests.get(API42.strip() + URL.strip() + '?%s' % "&".join(token) + "&page[number]=" + str(page) + "&page[size]=100")
            timeend = time.time()
            # if DEBUG: print('response' + '%6.2f' % ((timeend - timestart)) + ' seconds')
        except:
            # if DEBUG: print "bad request"
            pass
        res.encoding = 'UTF-8'
        if res.text == '[]':
            break
        ret = ret + res.text[1:-1] + ','
        page = page + 1
    return ret[:-1] + ']'

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

def write_to_file(name, data):
    file = open(name, 'w')
    file.write(data)
    file.close

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

def campus_users():
    API42 = 'https://api.intra.42.fr'
    URL = '/v2/campus_users'

    pass

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
    def __init__(self, id42, secret42, api42='https://api.intra.42.fr', debug=False, logs=True):
        self.id = str(id42).strip()
        self.secret = str(secret42).strip()
        self.debug = debug
        self.api42 = str(api42).strip()
        self.__debugCounter = 1
        self.__getToken()
        self.__lastStatusCode = -1
        self.__logs = logs

    def __debug(self, text):
        if self.debug:
            print str('api [{}] >> ' +  text).format(self.__debugCounter)
        self.__debugCounter += 1

    def __connected(self, statusCode):
        self.__lastStatusCode = statusCode
        if int(statusCode) == 200:
            self.__debug('connected: ' + str(statusCode))
            return True
        else:
            self.__debug('not connected: ' + str(statusCode))
            return False

    def __getToken(self):
        url = '/oauth/token'
        args = {'grant_type=client_credentials', 'client_id=' + self.id, 'client_secret=' + self.secret}
        self.__debug('request to ' + self.api42 + url)
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

    def __makeRequest(self, url):
        try:
            timestart = time.time()
            self.__debug('request to ' + self.api42 + url + '?%s' % "&".join(self.token))
            res = requests.get(self.api42 + url + '?%s' % "&".join(self.token))
            timeend = time.time()
            self.__debug('response' + '%6.2f' % ((timeend - timestart)) + ' seconds')
        except:
            self.__debug('bad request')
            return None
        res.encoding = 'UTF-8'
        return res.text.encode('utf8')

    def getUser(self, login='akalmyko'):
        user = Student(str(login).strip())
        url = '/v2/users/' + str(login).strip()
        user.userData = json.loads(self.__makeRequest(url))
        write_to_file(login + '_data', json.dumps(user.userData, indent=4, sort_keys=True))
        if len(user.userData) == 0:
            return None
        user.userId = user.userData['id']
        user.campus = user.userData['campus']
        user.url = user.userData['url']
        user.image_url = user.userData['image_url']
        user.displayname = user.userData['displayname']
        user.first_name = user.userData['first_name']
        user.last_name = user.userData['last_name']
        user.phone = user.userData['phone']
        user.email = user.userData['email']
        user.level = user.userData['cursus_users'][0]['level']
        # user.achievements = user.userData['achievements']
        # user.campus = user.userData['campus']
        return user

    def getUsers(self):
        pass