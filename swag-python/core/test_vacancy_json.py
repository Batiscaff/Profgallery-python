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
        print rest
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

        url = self.base_url + "company/create/?token=" + accessToken
        userInfo = {
            "title": "title" + str(randint(1000, 9999)),
            "inn": randint(10000000, 99999999),
            "addr": "string",
            "geoId": geoId
        }
        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        # Проверка на success
        checkStatus = rest["status"]
        print rest
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

    def test_02_vacancy_id(self):
        url = self.base_url + "vacancy/" + vacId +"/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus,"success")

    def test_03_vacancy_find(self):
        #Берем случайный ID отрасли
        url = self.base_url + "vocabulary/17/tree/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        indId =  rest["items"][randint(0,len(rest))]["element"]["id"]

        url = self.base_url + "vacancy/find/?token=" + accessToken
        userInfo = {
          "industryId": indId,
          "isDirect": "false"
        }
        r = requests.post(url=url,data=json.dumps(userInfo),headers=self.head)
        rest = json.loads(r.text)
        #Проверка на success
        checkStatus = rest["status"]
        print rest
        self.assertEqual(checkStatus,"success")

        #Проверка на пустой массив.
        if len(rest["items"]) == 0:
            pass
        #Если не пустой - сравниваем ID отрасли любой вакансии и той отрасли, что мы забивал
        else:
            self.assertEqual(indId,rest["items"][randint(0,len(rest))]["industry"]["id"])

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

        for i in range(1, randint(1, 9)):
            vacPropety = len(rest["items"]) - 1
            vacPropety = randint(0,vacPropety)
            vacPropety = rest["items"][vacPropety]["element"]["id"]
            vacPropetyList.append(vacPropety)
            print vacPropetyList
            for i in range(len(vacPropetyList) - 1):
                c = vacPropetyList[i]
                for j in range(len(vacPropetyList)):
                    if vacPropetyList[j] == c and i < j:
                        del vacPropetyList[-1]
                    else:
                        pass

        userInfo = {
            "properties": vacPropetyList
        }
        url = self.base_url +"vacancy/" + vacId + "/property/add/?token=" + accessToken
        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        print rest
        self.assertEqual(checkStatus, "success")

    def test_07_poperties(self):
        url = self.base_url +"vacancy/" + vacId + "/property/?token=" + accessToken
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        print rest
        self.assertEqual(checkStatus, "success")

    def test_08_properties_del(self):
        url = self.base_url + "vacancy/" + vacId + "/property/delete/?token=" + accessToken
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

        url = self.base_url + "vacancy/" + vacId + "/language/add/?token=" + accessToken
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
        url = self.base_url +"vacancy/" + vacId + "/language/?token=" + accessToken
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

    def test_11_vacancy_lang_del(self):
        url = self.base_url + "vacancy/" + vacId + "/language/delete/?token=" + accessToken
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