#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint
import unittest,json, requests


class test_Statistic(unittest.TestCase):

    def setUp(self):
        self.base_url ="http://api.corp.profgallery.ru/api/"
        self.head = {"Content-Type": "application/json", "Accept": "application/json"}

    def test_a_register_user_recruter(self):
        url = self.base_url + "user/register/"
        userInfo = {
            "login": "test_" + str(randint(10000,99999)) + "@blalba.ru",
            "password": "string",
            "type": "8"}
        r = requests.post(url=url,data=json.dumps(userInfo),headers=self.head)
        rest = json.loads(r.text)
        #Проверка на success
        checkStatus = rest["status"]
        self.assertEqual(checkStatus,"success")

        #Запоминаем для дальнейшей работы
        global accessToken
        accessToken =  rest["items"]["accessToken"]

    """def test_statistic(self):
        url = self.base_url +"statistic/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus,"success")"""

    def test_vocabulary(self):
        url = self.base_url + "vocabulary/options/"
        userInfo = {
            "optionNames": "string"
        }

        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        print rest
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

if __name__ == "__main__":
    unittest.main()