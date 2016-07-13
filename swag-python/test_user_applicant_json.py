#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint
import unittest,json, requests


class test_regUser(unittest.TestCase):
    def setUp(self):
        self.base_url ="http://api.corp.profgallery.ru"
        self.head = {"Content-Type": "application/json", "Accept": "application/json"}

    def test_register_user(self):
        url = self.base_url + "/api/user/register/"
        userInfo = {
            "login": "test_" + str(randint(10000,99999)) + "@blalba.ru",
            "password": "string",
            "type": "4"}
        r = requests.post(url=url,data=json.dumps(userInfo),headers=self.head)
        rest = json.loads(r.text)
        #Проверка на success
        checkStatus = rest["status"]
        self.assertEqual(checkStatus,"success")

        #Запоминаем для дальнейшей работы
        global  uid
        uid = rest["items"]["id"]
        global accessToken
        accessToken =  rest["items"]["accessToken"]
        global email
        email = rest["items"]["email"]

    def test_user_login(self):
        url = self.base_url + "/api/user/login/"
        userInfo = {
            "login": email,
            "password": "string"
        }
        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus,"success")
        global accessToken
        accessToken = rest["items"]["accessToken"]

    def test_user_login_by_token(self):
        url = self.base_url +"/api/user/login/token/"
        userInfo = {
            "token": accessToken,
        }
        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

    def test_user_id(self):
        url = self.base_url +"/api/user/" + str(uid) + "/?token=" + str(accessToken)
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

    def test_user_id_update(self):
        url = self.base_url + "/api/user/" + str(uid) + "/update/?token=" + str(accessToken)
        userInfo = {
                "fieldName": "surname",
                "fieldValue": "string"
            }
        r = requests.post(url,userInfo,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

if __name__ == "__main__":
    unittest.main()

