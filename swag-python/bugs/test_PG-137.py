# -*- coding: utf-8 -*-

from random import randint
import unittest, json, requests, time

companyFileds = ["title", "addrMain", "addr", "inn", "geoId"]
requiredFields = ["structureType", "url"]


class userComplitedPositive(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://api-test.corp.profgallery.ru/api/"
        self.head = {"Content-Type": "application/json", "Accept": "application/json"}

    def test_00_register_user(self):
        # Инициализация тестов
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
        # global uid
        # uid = str(rest["items"]["id"])
        global accessToken
        accessToken = str(rest["items"]["accessToken"])

    # def test_01_user_update(self):
    #     url = self.base_url + "user/" + uid + "/update/multiple/?token=" + accessToken
    #     userInfo = {
    #         "multiple": [
    #             {
    #                 "fieldName": "name",
    #                 "fieldValue": str(username[randint(0, len(username) - 1)])
    #             },
    #             {
    #                 "fieldName": "surname",
    #                 "fieldValue": str(usersurname[randint(0, len(usersurname) - 1)])
    #             },
    #             {
    #                 "fieldName": "middle_name",
    #                 "fieldValue": str(usermiddlename[randint(0, len(usermiddlename) - 1)])
    #             },
    #             {
    #                 "fieldName": "phone",
    #                 "fieldValue": str(randint(89000000001, 89999999999))
    #             }
    #         ]
    #     }
    #     r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
    #     rest = json.loads(r.text)
    #     checkStatus = rest["status"]
    #     self.assertEqual(checkStatus, "success")
    #
    #     url = self.base_url + "user/" + uid + "/update/?token=profTest"
    #     userInfo = {
    #         "fieldName": "isValidated",
    #         "fieldValue": 1
    #     }
    #     r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
    #     rest = json.loads(r.text)
    #     checkStatus = rest["status"]
    #     self.assertEqual(checkStatus, "success")

    def test_02_company_create(self):
        company = {}
        for i in xrange(len(companyFileds)):
            dice = companyFileds[randint(0, len(companyFileds) - 1)]
            if dice == "title":
                company.update({"title": "title" + str(randint(1000, 9999))})
                companyFileds.remove("title")
            elif dice == "addrMain":
                company.update({"addrMain": "string"})
                companyFileds.remove("addrMain")
            elif dice == "addr":
                company.update({"addr": "string"})
                companyFileds.remove("addr")
            elif dice == "inn":
                companyFileds.remove("inn")
                company.update({"inn": randint(10000000, 99999999)})
            elif dice == "geoId":
                companyFileds.remove("geoId")
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
                company.update({"geoId": rest["items"][countryId]["child"][cityId]["element"]["id"]})
            # Проверяем, сможем ли мы создать компанию
            if len(companyFileds) == 0:
                pass
            else:
                url = self.base_url + "company/create/?token=" + accessToken
                r = requests.post(url=url, data=json.dumps(company), headers=self.head)
                rest = json.loads(r.text)
                # Проверка на success
                checkStatus = rest["status"]
                self.assertEqual(checkStatus, "error")

        url = self.base_url + "company/create/?token=" + accessToken
        r = requests.post(url=url, data=json.dumps(company), headers=self.head)
        rest = json.loads(r.text)
        # Проверка на success
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")
        global compId
        compId = str(rest["items"]["id"])

        url = self.base_url + "company/" + compId + "/percent/?token=" + accessToken
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")
        checkStatus = rest["items"]["required"]["is_completed"]["status"]
        self.assertEqual(checkStatus, False)

    def test_03_company_update_postitve(self):
        # модерируем компанию, что бы мы могли творить всякие непотребства
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
        company = {}
        for i in xrange(len(requiredFields)):
            dice = requiredFields[randint(0, len(requiredFields) - 1)]
            print requiredFields
            print dice
            if dice == "structureType":
                requiredFields.remove("structureType")
                url = self.base_url + "vocabulary/gejob_business_type/tree/?token=" + accessToken
                r = requests.get(url, self.head)
                rest = json.loads(r.text)
                obj = randint(0, len(rest["items"]) - 1)
                # obj =  3
                if len(rest["items"][obj]["child"]) > 0 and randint(1, 1) == 1:

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
                print rest
                # Проверка на success
                checkStatus = rest["status"]
                self.assertEqual(checkStatus, "success")
            elif dice == "url":
                requiredFields.remove("url")
                if randint(0, 0) == 1:
                    url = self.base_url + "company/" + compId + "/update/?token=" + accessToken
                    userInfo = {
                        "fieldName": "url",
                        "fieldValue": "string"
                    }
                    r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
                    rest = json.loads(r.text)
                    # Проверка на success
                    checkStatus = rest["status"]
                    self.assertEqual(checkStatus, "success")
                else:
                    url = self.base_url + "company/" + compId + "/update/?token=" + accessToken
                    userInfo = {
                        "fieldName": "url",
                        "fieldValue": "string"
                    }
                    r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
                    userInfo = {
                        "fieldName": "description",
                        "fieldValue": "string"
                    }
                    r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
                    rest = json.loads(r.text)
                    print rest
                    # Проверка на success
                    checkStatus = rest["status"]
                    self.assertEqual(checkStatus, "success")
            if len(requiredFields) == 0:
                pass
            else:
                url = self.base_url + "company/" + compId + "/percent/?token=" + accessToken
                r = requests.get(url, self.head)
                rest = json.loads(r.text)
                checkStatus = rest["status"]
                self.assertEqual(checkStatus, "success")
                checkStatus = rest["items"]["required"]["is_completed"]["status"]
                self.assertEqual(checkStatus, False)

        url = self.base_url + "company/" + compId + "/percent/?token=" + accessToken
        print url
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")
        checkStatus = rest["items"]["required"]["is_completed"]["status"]
        self.assertEqual(checkStatus, True)

    # def test_04_negative(self):
    #     url = self.base_url + "company/" + compId + "/update/?token=" + accessToken
    #     userInfo = {
    #         "fieldName": "url",
    #         "fieldValue": ""
    #     }
    #     r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
    #     rest = json.loads(r.text)
    #     userInfo = {
    #         "fieldName": "description",
    #         "fieldValue": ""
    #     }
    #     r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
    #     rest = json.loads(r.text)
    #     # Проверка на success
    #     checkStatus = rest["status"]
    #     self.assertEqual(checkStatus, "success")
    #
    #     url = self.base_url + "company/" + compId + "/percent/?token=" + accessToken
    #     r = requests.get(url, self.head)
    #     rest = json.loads(r.text)
    #     checkStatus = rest["status"]
    #     self.assertEqual(checkStatus, "success")
    #     checkStatus = rest["items"]["required"]["is_completed"]["status"]
    #     self.assertEqual(checkStatus, False)

