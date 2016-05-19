#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint
import unittest,json, requests


class test_regUser(unittest.TestCase):

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
        global uid
        uid = rest["items"]["id"]
        global accessToken
        accessToken =  rest["items"]["accessToken"]


    def test_recruter(self):
        url = self.base_url + "user/recruiter/" + str(uid) + "/?token=" + accessToken



if __name__ == "__main__":
    unittest.main()

