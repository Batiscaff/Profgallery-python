# -*- coding: utf-8 -*-

from random import randint
import unittest, json, requests

class viewAs(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://api-test.corp.profgallery.ru/api/"
        self.head = {"Content-Type": "application/json", "Accept": "application/json"}

    def test_01_reguser(self):
        # Инициализация тестов
        url = self.base_url + "tests-init/"
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

        #регистрируем работодателя
        url = self.base_url + "user/register/"
        userInfo = {
            "login": "test_" + str(randint(10000, 99999)) + "@blalba.ru",
            "password": "string",
            "type": "4"
        }
        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")
        global accessToken
        accessToken = str(rest["items"]["accessToken"])
        global uid
        uid = str(rest["items"]["id"])


    def test_02_applicant_id_experience_new(self):
        # Берем ID компании
        url = self.base_url + "company/?token=" + accessToken
        r = requests.get(url, self.head)
        companyList = json.loads(r.text)

        # Берем ID индустрии
        url = self.base_url + "vocabulary/gejob_branch/tree/?token=" + accessToken
        r = requests.get(url, self.head)
        indistrylist = json.loads(r.text)

        for x in xrange(1,5):
            print x
            url = self.base_url + "applicant/" + uid + "/experience/new/?token=" + accessToken
            userInfo = {
                "id": 0,
                "type": 1,
                "companyId": companyList["items"][randint(0,len(companyList["items"]) - 1)]["id"],
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
                "industryId": indistrylist["items"][randint(0,len(indistrylist)-1)]["element"]["id"],
                "availabilityOfCompany": x
            }
            r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
            rest = json.loads(r.text)
            checkStatus = rest["status"]
            self.assertEqual(checkStatus, "success")


            # Проверяем видимость как прямой работодатель
            url = self.base_url + "applicant/" + uid + "/experience/?token=" + accessToken + "&userRole=direct"
            r = requests.get(url, self.head)
            rest = json.loads(r.text)
            checkStatus = rest["status"]
            self.assertEqual(checkStatus, "success")

            checkStatus = rest["items"][x-1]["companyId"]
            if (x == 2) or (x == 3):
                self.assertEqual(checkStatus, False)
            else:
                self.assertNotEquals(checkStatus, False)


            # Проверяем видимость как агентство
            url = self.base_url + "applicant/" + uid + "/experience/?token=" + accessToken + "&userRole=agency"
            r = requests.get(url, self.head)
            rest = json.loads(r.text)
            checkStatus = rest["status"]
            self.assertEqual(checkStatus, "success")

            checkStatus = rest["items"][x-1]["companyId"]
            if (x == 2) or (x == 4):
                self.assertEqual(checkStatus,False)
            else:
                self.assertNotEquals(checkStatus,False)
