#!/usr/bin/python
# -*- coding: utf-8 -*-

class Student:
    def __init__(self, login):
        self.login = login
        self.userId = None
        self.campus = None
        self.url = None
        self.image_url = None
        self.displayname = None

        self.first_name = None
        self.last_name = None
        self.phone = None
        self.email = None

        self.level = None
        self.wallet = None
        self.achievements = None
        self.campus_users = None
        self.correction_point = None
        self.cursus_users = None
        self.expertises_users = None
        self.groups = None
        self.languages_users = None
        self.location = None
        self.partnerships = None
        self.patroned = None
        self.patroning = None
        self.pool_month = None
        self.pool_year = None
        self.projects_users = None
        self.staff = None
        self.titles = None
        self.userData = None

    def printInfo(self):
        print self.userId
        print self.login
        print self.displayname
        print self.level
