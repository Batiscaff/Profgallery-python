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
        uid = str(rest["items"]["id"])
        global accessToken
        accessToken =  str(rest["items"]["accessToken"])

    def test_vacancy_id(self):
        url = self.base_url + "vacancy/" + vacId +"/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus,"success") 

    def test_vacancy(self):
        url = self.base_url + "vacancy/?token=" + accessToken
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")
        global vacId
        vacId = len(rest["items"]) - 1
        vacId = randint(0,vacId)
        vacId = str(rest["items"][vacId]["id"])



if __name__ == "__main__":
    unittest.main()