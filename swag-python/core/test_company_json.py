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
        global accessToken
        accessToken =  rest["items"]["accessToken"]

    def test_01_company(self):
        url = self.base_url + "company/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus,"success")

        #Запоминаем ID компании
        global uId
        uId = rest["items"][0]["id"]

    def test_02_company_create(self):
        # Берем ID гео
        url = self.base_url + "vocabulary/geo/tree/?token=" + accessToken
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
        rest = json.loads(r.text)
        # Проверка на success
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")


    def test_03_company_id(self):
        url = self.base_url + "company/" + compId + "/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus,"success")

    def test_04_company_id_update(self):
        url = self.base_url + "company/" + compId + "/update/?token=" + accessToken
        userInfo = {
            "fieldName": "description",
            "fieldValue": "description :" + str(randint(1000,9999))
        }
        r = requests.post(url=url,data=json.dumps(userInfo),headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus,"success")

        url = self.base_url + "company/" + compId + "/update/?token=" + accessToken
        userInfo = {
                "fieldName": "url",
                "fieldValue": "http://" + str(randint(1000,9999)) + ".ru"
            }
        r = requests.post(url=url,data=json.dumps(userInfo),headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus,"success")

        # Берем ID гео
        url = self.base_url + "vocabulary/geo/tree/?token=" + accessToken
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

        url = self.base_url + "company/" + compId + "/update/?token=" + accessToken
        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

    def test_05_company_id_percent(self):
        url = self.base_url + "company/" + compId + "/percent/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus,"success")

    def test_06_company_id_stat(self):
        url = self.base_url + "company/" + compId + "/stats/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus,"success")

    def test_07_company_search(self):
        url = self.base_url + "company/search/?search=string&token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus,"success")

    def test_08_company_property_add(self):
        url = self.base_url + "company/" + compId + "/property/add/?token=" + accessToken
        userInfo = {
            "properties": [
                11135,
                8772
            ]
        }
        r = requests.post(url=url,data=json.dumps(userInfo),headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus,"success")

    def test_10_company_property_delete(self):
        url = self.base_url + "company/" + compId + "/property/delete/?token=" + accessToken
        userInfo = {
            "properties": [
                11135,
                8772
            ]
        }
        r = requests.post(url=url,data=json.dumps(userInfo),headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus,"success")

    def test_09_company_property(self):
        url = self.base_url + "company/" + compId + "/property/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus,"success")

    def test_11_company_logo(self):
        url = self.base_url + "company/" + compId + "/logo/?token=" + accessToken
        userInfo = {
                    "body": "iVBORw0KGgoAAAANSUhEUgAAAEUAAABZCAIAAADn+36eAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyFpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuNS1jMDE0IDc5LjE1MTQ4MSwgMjAxMy8wMy8xMy0xMjowOToxNSAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENDIChXaW5kb3dzKSIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDo4OUMxMEVFREE0QjExMUU1OTE4QkY0RjE4NzFBMTBEQiIgeG1wTU06RG9jdW1lbnRJRD0ieG1wLmRpZDo4OUMxMEVFRUE0QjExMUU1OTE4QkY0RjE4NzFBMTBEQiI+IDx4bXBNTTpEZXJpdmVkRnJvbSBzdFJlZjppbnN0YW5jZUlEPSJ4bXAuaWlkOjg5QzEwRUVCQTRCMTExRTU5MThCRjRGMTg3MUExMERCIiBzdFJlZjpkb2N1bWVudElEPSJ4bXAuZGlkOjg5QzEwRUVDQTRCMTExRTU5MThCRjRGMTg3MUExMERCIi8+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+htdJvwAABgBJREFUeNrsm1dT4zwU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"
        }
        r = requests.post(url=url,data=json.dumps(userInfo),headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus,"success")

    def test_11_company_logo_del(self):
        url = self.base_url + "company/" + compId + "/logo/delete/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus,"success")

    def test_12_company_partner_update(self):
        url = self.base_url + "company/" + compId + "/partner/update/?token=" + accessToken
        userInfo = {
            "isDirect": 0,
            "hasContract": 0,
            "isStealth": 0
        }
        r = requests.post(url=url,data=json.dumps(userInfo),headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus,"success")



