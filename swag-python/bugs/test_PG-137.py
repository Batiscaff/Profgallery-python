# -*- coding: utf-8 -*-

from random import randint
import unittest, json, requests

class requiredFileds(unittest.TestCase):
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
            "type": "8"
        }
        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")
        global accessToken
        accessToken = str(rest["items"]["accessToken"])

    def test_02_company_create(self):
        company = {}
        requiredFields= ["addrMain","title","addr","inn","geoId"]
        for i in xrange(len(requiredFields)):
            x = requiredFields.pop(randint(0,len(requiredFields)-1))
            # Пробуем создать компанию
            url = self.base_url + "company/create/?token=" + accessToken
            r = requests.post(url=url, data=json.dumps(company), headers=self.head)
            rest = json.loads(r.text)
            checkStatus = rest["status"]
            self.assertEqual(checkStatus, "error")

            if x == 'addrMain':
                company.update({"addrMain": "string"})
            elif x == "title":
                company.update({"title": "title" + str(randint(1000, 9999))})
            elif x == "addr":
                company.update({"addr": "string"})
            elif x == "inn":
                company.update({"inn": randint(10000000, 99999999)})
            elif x == "geoId":
                # Берем ID гео
                url = self.base_url + "vocabulary/geo/tree/?token=" + accessToken
                r = requests.get(url, self.head)
                rest = json.loads(r.text)
                checkStatus = rest["status"]
                self.assertEqual(checkStatus, "success")

                countryId = randint(0, len(rest["items"]) - 1)
                cityId = randint(0, len(rest["items"][countryId]["child"]) - 1)
                company.update({"geoId": rest["items"][countryId]["child"][cityId]["element"]["id"]})

        # После заполнения всех полей - успешное создание компании
        url = self.base_url + "company/create/?token=" + accessToken
        r = requests.post(url=url, data=json.dumps(company), headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")
        global compId
        compId = str(rest["items"]["id"])

        # Проверяем, что is_completed == False
        url = self.base_url + "company/" + compId + "/percent/?token=" + accessToken
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")
        checkStatus = rest["items"]["required"]["is_completed"]["status"]
        self.assertEqual(checkStatus, False)

    def test_03_company_update_postitve(self):
        url = self.base_url + "company/" + compId + "/update/?token=profTest"
        userInfo = {
            "fieldName": "isVerified",
            "fieldValue": 1
        }
        requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        # Обязательные поля
        requiredFields = ["structureType", "url"]
        for i in xrange(len(requiredFields)):
            x = requiredFields.pop(randint(0,len(requiredFields))-1)
            if x == "url":
                url = self.base_url + "company/" + compId + "/percent/?token=" + accessToken
                r = requests.get(url, self.head)
                rest = json.loads(r.text)
                checkStatus = rest["status"]
                self.assertEqual(checkStatus, "success")
                checkStatus = rest["items"]["required"]["is_completed"]["status"]
                self.assertEqual(checkStatus, False)

                url = self.base_url + "company/" + compId + "/update/?token=" + accessToken
                if randint(0,1) == 1:
                    userInfo = {
                        "fieldName": "url",
                        "fieldValue": "http://" + str(randint(1000,9999)) + ".ru"
                    }
                    r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
                    rest = json.loads(r.text)
                    checkStatus = rest["status"]
                    self.assertEqual(checkStatus, "success")
                else:
                    userInfo = {
                        "fieldName": "description",
                        "fieldValue": "string"
                    }
                    r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
                    rest = json.loads(r.text)
                    checkStatus = rest["status"]
                    self.assertEqual(checkStatus, "success")

            elif x == "structureType":
                url = self.base_url + "vocabulary/gejob_business_type/tree/?token=" + accessToken
                r = requests.get(url, self.head)
                rest = json.loads(r.text)
                obj = randint(0, len(rest["items"]) - 1)
                if len(rest["items"][obj]["child"]) > 0 and randint(0, 1) == 1:

                    structureType = \
                        rest["items"][obj]["child"][randint(0, len(rest["items"][obj]["child"])-1)]["element"][
                            "id"]

                else:
                    structureType = rest["items"][obj]["element"]["id"]

                url = self.base_url + "company/" + compId + "/update/?token=" + accessToken
                userInfo = {
                    "fieldName": "structureType",
                    "fieldValue": structureType
                }
                r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
                rest = json.loads(r.text)
                checkStatus = rest["status"]
                self.assertEqual(checkStatus, "success")

        url = self.base_url + "company/" + compId + "/percent/?token=" + accessToken
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        print rest
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")
        checkStatus = rest["items"]["required"]["is_completed"]["status"]
        self.assertEqual(checkStatus, True)

    # def test_04_negative(self):
    #     url = self.base_url + "company/" + compId + "/update/?token=" + accessToken
    #     requiredFields = ["structureType", "url"]
    #
    #     x = requiredFields.pop(randint(0,len(requiredFields)-1))
    #     if x == "url":
    #         url = self.base_url + "company/" + compId + "/update/?token=" + accessToken
    #         userInfo = {
    #             "fieldName": "url",
    #             "fieldValue": ""
    #         }
    #         requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
    #         userInfo = {
    #             "fieldName": "description",
    #             "fieldValue": ""
    #         }
    #         requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
    #
    #     elif x == 'structureType':
    #         url = self.base_url + "company/" + compId + "/update/?token=" + accessToken
    #         userInfo = {
    #             "fieldName": "structureType",
    #             "fieldValue": ""
    #         }
    #         requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
    #
    #     url = self.base_url + "company/" + compId + "/percent/?token=" + accessToken
    #     print url
    #     r = requests.get(url, self.head)
    #     rest = json.loads(r.text)
    #     checkStatus = rest["status"]
    #     self.assertEqual(checkStatus, "success")
    #     checkStatus = rest["items"]["required"]["is_completed"]["status"]
    #     self.assertEqual(checkStatus, False)
