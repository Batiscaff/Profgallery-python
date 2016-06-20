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
        global accessToken
        accessToken =  rest["items"]["accessToken"]

    def test_company(self):
        url = self.base_url + "company/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus,"success")

        #Запоминаем ID компании
        global uId
        uId = rest["items"][0]["id"]

    def test_b_company_create(self):
        # Берем ID гео
        url = self.base_url + "vocabulary/74/tree/?token=" + accessToken
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

        countryId = len(rest["items"]) - 1
        countryId = randint(0, countryId)

        cityId = len(rest["items"][countryId]["child"]) - 1
        cityId = randint(0, cityId)
        geoId = rest["items"][countryId]["child"][cityId]["element"]["id"]

        url = self.base_url + "company/create/?token=" + accessToken
        userInfo = {
           "title": "title" + str(randint(1000,9999)),
           "inn": randint(10000000,99999999),
           "addr": "string",
           "geoId": geoId
        }
        r = requests.post(url=url,data=json.dumps(userInfo),headers=self.head)
        rest = json.loads(r.text)
        #Проверка на success
        checkStatus = rest["status"]
        self.assertEqual(checkStatus,"success")
        global compId
        compId = str(rest["items"]["id"])

        url = self.base_url + "company/" + compId + "/update/?token=profTest"
        userInfo = {
            "fieldName": "isVerified",
            "fieldValue": 1
        }
        r = requests.post(url=url,data=json.dumps(userInfo),headers=self.head)


    def test_company_id(self):
        url = self.base_url + "company/" + compId + "/?token=" + str(accessToken)
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus,"success")

    def test_company_id_update(self):
        url = self.base_url + "company/" + compId + "/update/?token=" + str(accessToken)
        userInfo = {
            "fieldName": "description",
            "fieldValue": "description :" + str(randint(1000,9999))
        }
        r = requests.post(url=url,data=json.dumps(userInfo),headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus,"success")

        url = self.base_url + "company/" + compId + "/update/?token=" + str(accessToken)
        userInfo = {
                "fieldName": "url",
                "fieldValue": "http://" + str(randint(1000,9999)) + ".ru"
            }
        r = requests.post(url=url,data=json.dumps(userInfo),headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus,"success")

        # Берем ID гео
        url = self.base_url + "vocabulary/74/tree/?token=" + accessToken
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

        countryId = len(rest["items"]) - 1
        countryId = randint(0, countryId)

        cityId = len(rest["items"][countryId]["child"]) - 1
        cityId = randint(0, cityId)
        geoId = rest["items"][countryId]["child"][cityId]["element"]["id"]
        userInfo = {
            "fieldName": "geoId",
            "fieldValue": geoId
        }

        url = self.base_url + "company/" + compId + "/update/?token=" + str(accessToken)
        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")