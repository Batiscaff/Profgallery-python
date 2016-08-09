# -*- coding: utf-8 -*-

from random import randint
import unittest,json, requests


class test_regUser(unittest.TestCase):
    def setUp(self):
        self.base_url ="http://api-test.corp.profgallery.ru/api/"
        self.head = {"Content-Type": "application/json", "Accept": "application/json"}

    def test_00_register_user_recruter(self):
        url = self.base_url + "tests-init/"
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus,"success")

        url = self.base_url + "user/register/"
        userInfo = {
            "login": "test_" + str(randint(10000,99999)) + "@blalba.ru",
            "password": "string",
            "type": "8"}
        r = requests.post(url=url,data=json.dumps(userInfo),headers=self.head)
        rest = json.loads(r.text)

        #Проверка на success
        checkStatus = rest["status"]
        print rest
        self.assertEqual(checkStatus,"success")

        #Запоминаем для дальнейшей работы
        global accessToken
        accessToken =  rest["items"]["accessToken"]
        print accessToken

    def test_01_search_applicant(self):
        url = self.base_url + "search/applicant/?token=" + accessToken
        userInfo = {
            "text": "string"
        }
        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        print rest
        self.assertEqual(checkStatus,"success")

    def test_02_search_filter_save(self):
        url = self.base_url + "search/filter/save/?token=" + accessToken
        userInfo = {
          "title": "string" + str(randint(1999,2999)),
          "parameters": [
              {}
          ]
        }
        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        print rest
        self.assertEqual(checkStatus, "success")
        global filterId
        filterId = str(rest["items"]["id"])

    def test_03_search_filter_update(self):
        url = self.base_url + "search/filter/" + filterId + "/update/?token=" + accessToken
        userInfo = {
            "fields": {
                "parameters": {
                    "new_one": ["1", 2, 5, randint(10,50)]
                }
            }
        }
        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        print rest
        self.assertEqual(checkStatus, "success")

    def test_04_search_filter_list(self):
        url = self.base_url + "search/filter/list/?token=" + accessToken
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        print rest
        self.assertEqual(checkStatus, "success")

    def test_05_search_filter_del(self):
        url = self.base_url + "search/filter/" + filterId + "/delete/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        print rest
        self.assertEqual(checkStatus, "success")

