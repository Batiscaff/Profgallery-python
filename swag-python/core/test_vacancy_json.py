#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint
import unittest,json, requests,pytest


class test_regUser(unittest.TestCase):
    def setUp(self):
        my_file = open("setup.txt", "r")
        self.base_url ="http://api-test.corp.profgallery.ru/api/"
        self.head = {"Content-Type": "application/json", "Accept": "application/json","testing-db": my_file.read()}

    def test_00_register_user_recruter(self):
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
        global uid
        uid = str(rest["items"]["id"])

        global accessToken
        accessToken =  str(rest["items"]["accessToken"])

    def test_01_company_create(self):
        # Берем ID гео
        url = self.base_url + "vocabulary/geo/tree/?token=" + accessToken
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        print rest
        self.assertEqual(checkStatus, "success")

        countryId = len(rest["items"]) - 1
        countryId = randint(0, countryId)

        cityId = len(rest["items"][countryId]["child"]) - 1
        cityId = randint(0, cityId)
        global geoId
        geoId = rest["items"][countryId]["child"][cityId]["element"]["id"]

        url = self.base_url + "vocabulary/gejob_business_type/tree/?token=" + accessToken
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        obj = randint(0, len(rest["items"]) - 1)
        # obj =  3


        if len(rest["items"][obj]["child"]) > 0 and randint(1, 1) == 1:

            structureType = rest["items"][obj]["child"][randint(0, len(rest["items"][obj]["child"])-1)]["element"][
                "id"]

        else:
            structureType = rest["items"][obj]["element"]["id"]

        url = self.base_url + "company/create/?token=" + accessToken
        userInfo = {
            "title": "title" + str(randint(1000, 9999)),
            "addr": "string",
            "addrMain": "string main",
            "url": "string",
            "structureType": structureType,
            "description": "string",
            "brand": "string",
            "inn": randint(10000000, 99999999),
            "geoId": geoId
        }
        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        # Проверка на success
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")
        global compId
        compId = str(rest["items"]["id"])


        url = self.base_url + "company/" + compId + "/update/?token=profTest"
        userInfo = {
            "fieldName": "isVerified",
            "fieldValue": 1
        }
        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        # Проверка на success
        checkStatus = rest["status"]
        print rest
        self.assertEqual(checkStatus, "success")

    def test_01_vacancy(self):
        pytest.skip(msg="Метод доступен только для админа")
        url = self.base_url + "vacancy/?token=" + accessToken
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        print rest
        self.assertEqual(checkStatus, "success")
        global vacId
        vacId = len(rest["items"]) - 1
        vacId = randint(0,vacId)
        vacId = str(rest["items"][vacId]["id"])

    def test_05_vacancy_id(self):
        url = self.base_url + "vacancy/" + vacIdCreate +"/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus,"success")

    def test_04_vacancy_create(self):
        url = self.base_url + "vocabulary/17/tree/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        global indistryID
        indistryID = len(rest["items"]) - 1
        indistryID = randint(0,indistryID)
        indistryID = rest["items"][indistryID]["element"]["id"]

        url = self.base_url + "vacancy/create/?token=" + accessToken
        userInfo = {
            "companyId": compId,
            "geoId": geoId,
            "industryId": indistryID,
            "title": "string",
            "description": "string" + str(randint(1000,9999)),
            "salaryMonthMin": 0,
            "salaryMonthMax": 0,
            "salaryYearMin": 0,
            "salaryYearMax": 0,
            "publishStart": "2016-06-21T12:51:18+0000",
            "publishFinish": "2016-06-21T12:51:18+0000",
            "vacancyType": 0,
            "address": "string",
            "packageMobile": 0,
            "packageMedicine": 0,
            "packageCar": 0,
            "packageFeeding": 0,
            "packageOther": "string",
            "degreeId": 0,
            "eduLevelId": 0,
            "eduTypeId": 0,
            "education": "string",
            "weTotal": 0,
            "weManagement": 0,
            "weProject": 0,
            "weMaxbudget": 0,
            "totalScount": 0,
            "suspended": 0,
            "requirements": "string"
        }
        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        print rest
        self.assertEqual(checkStatus, "success")

        global vacIdCreate
        vacIdCreate = str(rest["items"]["id"])


    def test_05_vacancy_id_update(self):
        url = self.base_url + "vacancy/" + vacIdCreate + "/update/?token=" + accessToken
        userInfo = {
            "companyId": compId,
            "geoId": geoId,
            "industryId": indistryID,
            "title": "string",
            "description": "string" + str(randint(1000,9999)),
            "salaryMonthMin": 0,
            "salaryMonthMax": 0,
            "salaryYearMin": 0,
            "salaryYearMax": 0,
            "publishStart": "2016-06-21T12:51:18+0000",
            "publishFinish": "2016-06-21T12:51:18+0000",
            "vacancyType": 0,
            "address": "string",
            "packageMobile": 0,
            "packageMedicine": 0,
            "packageCar": 0,
            "packageFeeding": 0,
            "packageOther": "string",
            "degreeId": 0,
            "eduLevelId": 0,
            "eduTypeId": 0,
            "education": "string",
            "weTotal": 0,
            "weManagement": 0,
            "weProject": 0,
            "weMaxbudget": 0,
            "totalScount": 0,
            "suspended": 0,
            "requirements": "string"
        }
        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        print rest
        self.assertEqual(checkStatus, "success")

    def test_06_vacancy_property_add(self):
        url = self.base_url + "vocabulary/gejob_activity_area/tree/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)

        global vacPropetyList
        vacPropetyList = []

        for i in xrange(1, randint(2, 9)):
            vacPropety = len(rest["items"]) - 1
            vacPropety = randint(0,vacPropety)
            vacPropety = rest["items"][vacPropety]["element"]["id"]
            print vacPropetyList
            if vacPropety not in vacPropetyList:
                vacPropetyList.append(vacPropety)
                print vacPropetyList

        userInfo = {
            "properties": vacPropetyList
        }
        print userInfo
        url = self.base_url +"vacancy/" + vacIdCreate + "/property/add/?token=" + accessToken
        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        print rest
        self.assertEqual(checkStatus, "success")

    def test_07_poperties(self):
        url = self.base_url +"vacancy/" + vacIdCreate + "/property/?token=" + accessToken
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        print rest
        self.assertEqual(checkStatus, "success")

    def test_08_properties_del(self):
        url = self.base_url + "vacancy/" + vacIdCreate + "/property/delete/?token=" + accessToken
        userInfo = {
            "properties": vacPropetyList
        }
        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        print rest
        self.assertEqual(checkStatus, "success")

    def test_09_vacancy_lang_add(self):
        url = self.base_url + "vocabulary/languages/tree/?token=" + accessToken
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        print rest
        self.assertEqual(checkStatus, "success")

        global langId
        langId = len(rest["items"]) - 1
        langId = randint(0,langId)
        langId = rest["items"][langId]["element"]["id"]

        url = self.base_url + "vacancy/" + vacIdCreate + "/language/add/?token=" + accessToken
        userInfo = {
            "languageId": langId,
            "degreeId": 10
        }
        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        print rest
        self.assertEqual(checkStatus, "success")

    def test_10_vacancy_lang(self):
        url = self.base_url +"vacancy/" + vacIdCreate + "/language/?token=" + accessToken
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

    def test_11_vacancy_lang_del(self):
        url = self.base_url + "vacancy/" + vacIdCreate + "/language/delete/?token=" + accessToken
        userInfo = {
            "languageId": langId,
            "degreeId": 0
        }
        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        print rest
        self.assertEqual(checkStatus, "success")

    def test_12_vacancy_by_partner(self):
        url = self.base_url +"vacancy/by-partner/?token=" + accessToken
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        print rest
        self.assertEqual(checkStatus, "success")

    def test_13_vacancy_by_my(self):
        url = self.base_url +"vacancy/by-me/?token=" + accessToken
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        print rest
        self.assertEqual(checkStatus, "success")

if __name__ == "__main__":
    unittest.main()