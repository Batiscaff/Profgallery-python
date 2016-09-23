#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint
import unittest,json, requests,random

class hideOptions(unittest.TestCase):
    def setUp(self):
        my_file = open("setup.txt", "r")
        self.base_url ="http://api-test.corp.profgallery.ru/api/"
        self.head = {"Content-Type": "application/json", "Accept": "application/json","testing-db": my_file.read()}

    def test_00_register_user(self):
        url = self.base_url + "user/register/"
        userInfo = {
            "login": "test_" + str(randint(10000,99999)) + "@blalba.ru",
            "password": "string",
            "type": "4"}
        r = requests.post(url=url,data=json.dumps(userInfo),headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus,"success")
        global uid
        uid = str(rest["items"]["id"])
        global accessToken
        accessToken = str(rest["items"]["accessToken"])
        global email
        email = rest["items"]["email"]

    def test_01_user_update_multi(self):
        url = self.base_url +"user/" + uid + "/update/multiple/?token=" + accessToken
        userInfo = {
            "multiple": [
                {
                    "fieldName": "surname",
                    "fieldValue": "HideForAgency"
                },
                {
                "fieldName": "middle_name",
                "fieldValue": "HideForEmplo"
                }
            ]
        }
        r = requests.post(url=url,data=json.dumps(userInfo),headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

        url = self.base_url +"applicant/" + uid + "/update/multiple/?token=" + accessToken
        userInfo = {
            "multiple": [
                {
                    "fieldName": "availabilityOfSurname ",
                    "fieldValue": "3"
                },
                {
                    "fieldName": "availabilityOfMiddleName ",
                    "fieldValue": "4"
                },
                {
                    "fieldName": "availabilityOfProfile  ",
                    "fieldValue": "1"
                }
            ]
        }
        r = requests.post(url=url,data=json.dumps(userInfo),headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

    def test_02_view_as_agency(self):
        url = self.base_url +"user/" + uid + "/?token=" + accessToken + "&userRole=agency"
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

        checkStatus = rest["items"]["surname"]
        self.assertEqual(checkStatus, "HideForAgency")

        checkStatus = rest["items"]["middle_name"]
        self.assertEqual(checkStatus, False)

    def test_03_view_as_emplo(self):
        url = self.base_url +"user/" + uid + "/?token=" + accessToken + "&userRole=direct"
        print url
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

        checkStatus = rest["items"]["middle_name"]
        self.assertEqual(checkStatus, "HideForEmplo")

        checkStatus = rest["items"]["surname"]
        self.assertEqual(checkStatus, False)


