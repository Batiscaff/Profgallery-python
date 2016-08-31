#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint
import unittest,json, requests

class availabilityOf(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://api-test.corp.profgallery.ru/api/"
        self.head = {"Content-Type": "application/json", "Accept": "application/json"}

    def test_00_register_user_applicant(self):
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
            "type": "4"}
        r = requests.post(url=url,data=json.dumps(userInfo),headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        print rest
        self.assertEqual(checkStatus,"success")
        global uid
        uid = str(rest["items"]["id"])
        global accessToken
        accessToken = str(rest["items"]["accessToken"])

    def test_01_applicant_id_experience_new(self):
        for i in range(1,5,1):
            print "Создаем вакансию: " + str(i)
            # Берем ID компании
            url = self.base_url + "company/?token=" + accessToken
            r = requests.get(url, self.head)
            rest = json.loads(r.text)
            global companyID
            companyID = len(rest["items"]) - 1
            companyID = randint(0, companyID)
            companyID = rest["items"][companyID]["id"]

            # Берем ID индустрии
            url = self.base_url + "vocabulary/17/tree/?token=" + accessToken
            r = requests.get(url, self.head)
            rest = json.loads(r.text)
            global indistryID
            indistryID = len(rest["items"]) - 1
            indistryID = randint(0, indistryID)
            indistryID = rest["items"][indistryID]["element"]["id"]

            url = self.base_url + "applicant/" + uid + "/experience/new/?token=" + accessToken
            userInfo = {
                "id": 0,
                "type": 1,
                "companyId": companyID,
                "companyNote": "string",
                "started": "10.02.2010",
                "position": "string",
                "responsibilities": "string",
                "achievements": "string",
                "subordinate": "string",
                "completed": 0,
                "directScount": 0,
                "funcScount": 0,
                "projectScount": 0,
                "industryId": indistryID,
                "availabilityOfCompany": i
            }
            r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
            rest = json.loads(r.text)
            checkStatus = rest["status"]
            print rest
            self.assertEqual(checkStatus, "success")
            # Запоминаем созданный ID опыта работы
            expId = str(rest["items"]["id"])

        # Проверяем видимость как прямой работодатель
        url = self.base_url + "applicant/" + uid + "/experience/?token=" + accessToken + "&userRole=direct"
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        print rest
        self.assertEqual(checkStatus, "success")

        i = 1
        y = 0
        while i < 4:
            i += 1
            y += 1
            checkStatus = rest["items"][y]["companyId"]
            print checkStatus
            if (i == 2) or (i == 3):
                self.assertEqual(checkStatus,False)
            else:
                self.assertNotEquals(checkStatus,False)


        # Проверяем видимость как прямой работодатель
        url = self.base_url + "applicant/" + uid + "/experience/?token=" + accessToken + "&userRole=agency"
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        print rest
        self.assertEqual(checkStatus, "success")

        i = 1
        y = 0
        while i < 4:
            i += 1
            y += 1
            checkStatus = rest["items"][y]["companyId"]
            print checkStatus
            if (i == 2) or (i == 4):
                self.assertEqual(checkStatus,False)
            else:
                self.assertNotEquals(checkStatus,False)



