# -*- coding: utf-8 -*-

from random import randint
import unittest, json, requests

global rest


class userComplitedPositive(unittest.TestCase):
    def setUp(self):
        my_file = open("../core/setup.txt", "r")
        self.base_url ="http://api-test.corp.profgallery.ru/api/"
        self.head = {"Content-Type": "application/json", "Accept": "application/json","testing-db": my_file.read()}

    def user_update(self, userFileds):
        url = self.base_url + "user/" + uid + "/update/multiple/?token=" + accessToken
        userInfo = {
            "multiple": [
                {
                    "fieldName": "name",
                    "fieldValue": "Name"
                },
                {
                    "fieldName": "surname",
                    "fieldValue": "Surname"
                },
                {
                    "fieldName": "middle_name",
                    "fieldValue": "middleName"
                },
                {
                    "fieldName": "phone",
                    "fieldValue": "89039999999"
                }
            ]
        }
        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")
        userFileds.remove("user")

    def applicant_exp(self, userFileds):
        # Берем ID компании
        url = self.base_url + "company/?token=" + accessToken
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        companyID = len(rest["items"]) - 1
        companyID = randint(0, companyID)
        companyID = rest["items"][companyID]["id"]

        # Берем ID индустрии
        url = self.base_url + "vocabulary/17/tree/?token=" + accessToken
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        indistryID = len(rest["items"]) - 1
        indistryID = randint(0, indistryID)
        indistryID = rest["items"][indistryID]["element"]["id"]

        url = self.base_url + "applicant/" + uid + "/experience/new/?token=" + accessToken
        userInfo = {
            "type": 1,
            "companyId": companyID,
            "companyNote": "string",
            "started": "10.02.2005",
            "position": "3068",
            "responsibilities": "string",
            "achievements": "string",
            "subordinate": "string",
            "completed": 1,
            "directScount": 40,
            "funcScount": 10,
            "projectScount": 30,
            "industryId": indistryID
        }
        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")
        expId = str(rest["items"]["id"])

        url = self.base_url + "applicant/" + uid + "/percent/?token=" + accessToken
        print url
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

        # Прверяем что  опыт работы не заполнен
        checkStatus = rest["items"]["required"]["experience"]["status"]
        self.assertEqual(checkStatus, False)

        # добавляяем Property
        url = self.base_url + "vocabulary/grading/tree/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        functionID = rest["items"][randint(0,len(rest["items"]) - 1)]["element"]["id"]
        url = self.base_url + "applicant/" + uid + "/experience/" + expId + "/property/add/?token=" + accessToken
        userInfo = {
            "propertyId": [functionID],
            "isMain": 1
        }
        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

        url = self.base_url + "applicant/" + uid + "/percent/?token=" + accessToken
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")
        checkStatus = rest["items"]["required"]["experience"]["status"]
        self.assertEqual(checkStatus, 1)
        userFileds.remove("exp")

    def applicant_characteristic(self, userFileds):
        url = self.base_url + "applicant/" + uid + "/percent/?token=" + accessToken
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

        # Прверяем character не заполнен
        checkStatus = rest["items"]["required"]["characteristics"]["status"]
        self.assertEqual(checkStatus, False)
        print "Character не заполнен. Ок!"

        url = self.base_url + "applicant/" + uid + "/characteristics/update/?token=" + accessToken
        userInfo = {
            "project": 5,
            "totalExperience": 10,
            "management": 10,
            "budget": 100000000
        }
        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")
        # checkStatus = rest["items"]["completed"]
        # self.assertEqual(checkStatus, 1)
        userFileds.remove("character")

    def user_validate(self, userFileds):
        url = self.base_url + "applicant/" + uid + "/percent/?token=" + accessToken
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

        # Прверяем is_validated False
        checkStatus = rest["items"]["required"]["is_validated"]["status"]
        self.assertEqual(checkStatus, False)
        print "is_validated False. Ок!"

        url = self.base_url + "user/" + uid + "/update/?token=profTest"
        userInfo = {
            "fieldName": "isValidated",
            "fieldValue": 1
        }
        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)

        # Проверка на success
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")
        userFileds.remove("email")

    def applicant_edu(self, userFileds):
        url = self.base_url + "applicant/" + uid + "/percent/?token=" + accessToken
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

        # Прверяем edu не заполнен
        checkStatus = rest["items"]["required"]["education"]["status"]
        self.assertEqual(checkStatus, False)
        print "Edu не заполнен. Ок!"

        url = self.base_url + "applicant/" + uid + "/education/new/?token=" + accessToken
        userInfo = {
            "id": 0,
            "institution": "string",
            "specialty": "string",
            "faculty": "string",
            "eduLevelId": 1,
            "eduTypeId": 1,
            "isAdditional": 0,
            "degree": 1,
            "beginYear": 2007,
            "endYear": 2012,
            "cdate": "string",
            "mdate": "string",
            "completed": 1,
            "course": "string",
            "certificate": "string"
        }
        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

        checkStatus = rest["items"]["completed"]
        self.assertEqual(checkStatus, 1)
        userFileds.remove("edu")

    def test_00_register_user(self):
        url = self.base_url + "tests-init/"
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

        url = self.base_url + "user/register/"
        userInfo = {
            "login": "test_" + str(randint(10000, 99999)) + "@blalba.ru",
            "password": "string",
            "type": "4"}
        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")
        global uid
        uid = str(rest["items"]["id"])
        global accessToken
        accessToken = str(rest["items"]["accessToken"])

    def test_01_user_complited(self):
        status = False
        userFileds = ["edu", "exp", "character", "email","user"]
        while (status == False):
            dice = userFileds[randint(0, len(userFileds) - 1)]
            # dice = "exp"
            if dice == "user":
                print "user fill"
                self.user_update(userFileds)

            elif dice == "edu":
                print "edu"
                self.applicant_edu(userFileds)

            elif dice == "exp":
                print "exp"
                self.applicant_exp(userFileds)

            elif dice == "character":
                print "char"
                self.applicant_characteristic(userFileds)

            elif dice == "email":
                print "email"
                self.user_validate(userFileds)


            if len(userFileds) == 0:
                status = True
                continue

            url = self.base_url + "applicant/" + uid + "/percent/?token=" + accessToken
            r = requests.get(url, self.head)
            rest = json.loads(r.text)
            self.assertEqual(rest["items"]["required"]["is_completed"]["status"], False,
                             msg="Не заполнены обязательные поля " + str(userFileds))

        url = self.base_url + "applicant/" + uid + "/percent/?token=" + accessToken
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

        # Прверяем что профиль полностью заполнен
        checkStatus = rest["items"]["required"]["is_completed"]["status"]
        self.assertEqual(checkStatus, 1)
