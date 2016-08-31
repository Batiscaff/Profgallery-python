# -*- coding: utf-8 -*-

from random import randint
import unittest, json, requests, time

username = ["Адам", "Вадим", "Евгений", "Никита",
            "Дмитрий"    "Михаил"]
usersurname = ["ФамилияОдин","ФамилияДва","Фамилия3"]
usermiddlename = ["ОтчествоОдин","ОтчествоДва","Отчетство3"]
requiredFields = ["user","education","experience","character"]
userFileds = ["name","surname","phone","middle_name"]


class userComplitedPositive(unittest.TestCase):
        def setUp(self):
            self.base_url = "http://api-test.corp.profgallery.ru/api/"
            self.head = {"Content-Type": "application/json", "Accept": "application/json"}

        def test_00_register_user(self):
            #Инициализация тестов
            url = self.base_url + "tests-init/"
            r = requests.get(url, self.head)
            rest = json.loads(r.text)
            checkStatus = rest["status"]
            self.assertEqual(checkStatus, "success")


            url = self.base_url + "user/register/"
            userInfo = {
                "login": "test_" + str(randint(10000, 99999)) + "@blalba.ru",
                "password": "string",
                "type": "8"
            }
            r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
            rest = json.loads(r.text)
            checkStatus = rest["status"]
            self.assertEqual(checkStatus, "success")
            global uid
            uid = str(rest["items"]["id"])
            global accessToken
            accessToken = str(rest["items"]["accessToken"])
            print accessToken

        def test_01_user_update(self):
            url = self.base_url + "user/" + uid + "/update/multiple/?token=" + accessToken
            userInfo = {
                "multiple": [
                    {
                        "fieldName": "name",
                        "fieldValue": str(username[randint(0, len(username) - 1)])
                    },
                    {
                        "fieldName": "surname",
                        "fieldValue": str(usersurname[randint(0, len(usersurname) - 1)])
                    },
                    {
                        "fieldName": "middle_name",
                        "fieldValue": str(usermiddlename[randint(0, len(usermiddlename) - 1)])
                    },
                    {
                        "fieldName": "phone",
                        "fieldValue": str(randint(89000000001, 89999999999))
                    }
                ]
            }
            r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
            rest = json.loads(r.text)
            checkStatus = rest["status"]
            self.assertEqual(checkStatus, "success")

            url = self.base_url + "user/" + uid + "/update/?token=profTest"
            userInfo = {
                "fieldName": "isValidated",
                "fieldValue": 1
            }
            r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
            rest = json.loads(r.text)
            checkStatus = rest["status"]
            self.assertEqual(checkStatus, "success")

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

            url = self.base_url + "vocabulary/gejob_business_type/tree/?token=" + accessToken
            r = requests.get(url, self.head)
            rest = json.loads(r.text)
            obj = randint(0, len(rest["items"]) - 1)
            # obj =  3


            if len(rest["items"][obj]["child"]) > 0 and randint(1, 1) == 1:

                structureType = rest["items"][obj]["child"][randint(0, len(rest["items"][obj]["child"]))]["element"][
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
            self.assertEqual(checkStatus, "success")

        def test_03_company_id(self):
            url = self.base_url + "company/" + compId + "/?token=" + accessToken
            print url
            r = requests.get(url, self.head)
            rest = json.loads(r.text)
            checkStatus = rest["status"]
            self.assertEqual(checkStatus, "success")

        def test_03_company_id_percent(self):
            url = self.base_url + "company/" + compId + "/percent/?token=" + accessToken
            print url
            r = requests.get(url, self.head)
            rest = json.loads(r.text)
            checkStatus = rest["status"]
            self.assertEqual(checkStatus, "success")