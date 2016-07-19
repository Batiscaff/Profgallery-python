#!/usr/bin/env python
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
        self.assertEqual(checkStatus,"success")

        #Запоминаем для дальнейшей работы
        global uId
        uId = rest["items"]["id"]
        global accessTokenRecrut
        accessTokenRecrut =  rest["items"]["accessToken"]

    def test_01_company_create(self):
        url = self.base_url + "vocabulary/geo/tree/?token=" + accessTokenRecrut
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")
        countryId = len(rest["items"]) - 1
        countryId = randint(0, countryId)
        cityId = len(rest["items"][countryId]["child"]) - 1
        cityId = randint(0, cityId)
        global geoId
        geoId = rest["items"][countryId]["child"][cityId]["element"]["id"]
        url = self.base_url + "company/create/?token=" + accessTokenRecrut
        userInfo = {
            "title": "title" + str(randint(1000, 9999)),
            "inn": randint(10000000, 99999999),
            "addr": "string",
            "geoId": geoId
        }
        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")


    def test_01_recruter(self):
        url = self.base_url + "recruiter/?token=profTest"
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

    def test_02_recruter_id(self):
        url = self.base_url + "recruiter/" + uId + "/?token=" + accessTokenRecrut
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

    def test_03_recruter_id_update(self):
        url = self.base_url + "recruiter/" + uId + "/update/?token=" + accessTokenRecrut
        userInfo = {"position": "CEO"
        }
        r = requests.post(url=url,data=json.dumps(userInfo),headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus,"success")

    def test_04_recruter_role_add(self):
        url = self.base_url + "recruiter/roles/add/?token=" + accessTokenRecrut
        userInfo = {
            "recruiterId": str(uId),
            "roles": [
                1,
                3,
                5
            ]
        }
        r = requests.post(url=url,data=json.dumps(userInfo),headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus,"success")

    def test_05_recruter_role_del(self):
        url = self.base_url + "recruiter/roles/delete/?token=" + accessTokenRecrut
        userInfo = {
            "recruiterId": str(uId),
            "roles": [
                1,
                3,
                5
            ]
        }
        r = requests.post(url=url,data=json.dumps(userInfo),headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus,"success")


