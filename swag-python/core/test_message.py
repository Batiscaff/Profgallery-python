#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint
import unittest,json, requests

class test_regUser(unittest.TestCase):
    def setUp(self):
        my_file = open("setup.txt", "r")
        self.base_url = "http://api-test.corp.profgallery.ru/api/"
        self.head = {"Content-Type": "application/json", "Accept": "application/json", "testing-db": my_file.read()}

    def test_00_register_user_applicant(self):
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
        global accessToken
        accessToken =  rest["items"]["accessToken"]
        print accessToken
        global applicantId
        applicantId = str(rest["items"]["id"])
        uId = rest["items"]["id"]


        url = self.base_url + "applicant/"+ uId +"/update/?token=" + accessToken
        userInfo = {
            "fieldName": "availabilityOfProfile",
            "fieldValue": 1}
        r = requests.post(url=url,data=json.dumps(userInfo),headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        print rest
        self.assertEqual(checkStatus,"success")

    def test_00_register_user_emplo(self):
        url = self.base_url + "user/register/"
        userInfo = {
            "login": "test_" + str(randint(10000, 99999)) + "@blalba.ru",
            "password": "string",
            "type": "8"}
        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")
        global accessTokenEmplo
        accessTokenEmplo = rest["items"]["accessToken"]
        global emploId
        emploId = str(rest["items"]["id"])



    def test_01_company_create(self):
            # Берем ID гео
            url = self.base_url + "vocabulary/geo/tree/?token=" + accessTokenEmplo
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
            url = self.base_url + "vocabulary/gejob_business_type/tree/?token=" + accessTokenEmplo
            r = requests.get(url, self.head)
            rest = json.loads(r.text)
            obj = randint(0, len(rest["items"]) - 1)
            # obj =  3


            if len(rest["items"][obj]["child"]) > 0 and randint(1, 1) == 1:

                structureType = rest["items"][obj]["child"][randint(0, len(rest["items"][obj]["child"])-1)]["element"][
                    "id"]

            else:
                structureType = rest["items"][obj]["element"]["id"]

            url = self.base_url + "company/create/?token=" + accessTokenEmplo
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

    def test_02_vacancy_create(self):
        url = self.base_url + "vocabulary/17/tree/?token=" + accessTokenEmplo
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        global indistryID
        indistryID = len(rest["items"]) - 1
        indistryID = randint(0, indistryID)
        indistryID = rest["items"][indistryID]["element"]["id"]

        url = self.base_url + "vacancy/create/?token=" + accessTokenEmplo
        userInfo = {
            "companyId": compId,
            "geoId": geoId,
            "industryId": indistryID,
            "title": "string",
            "description": "string" + str(randint(1000, 9999)),
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



    def test_03_message_recruter_new(self):
        url = self.base_url + "message/recruiter/new/?token=" + accessTokenEmplo
        userInfo = {
            "itemId": applicantId,
            "itemType": 4,
            "body": "string"
        }
        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        print rest
        checkStatus = rest["status"]
        print rest
        self.assertEqual(checkStatus, "success")
        global threadIdEmplo
        threadIdEmplo = rest["items"]["threadId"]
        global messageIdFromEmplo
        messageIdFromEmplo = rest["items"]["id"]

    def test_04_message_recruter_invite(self):
        url = self.base_url + "message/recruiter/new/invite/?token=" + accessTokenEmplo
        userInfo = {
            "applicantId": applicantId,
            "body": "Hello",
            "vacancyId": vacIdCreate
        }
        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        print rest
        self.assertEqual(checkStatus, "success")

    def test_05_message_applicant(self):
        url = self.base_url + "message/applicant/new/?token=" + accessToken
        userInfo = {
            "itemId": vacIdCreate,
            "itemType": 2,
            "body": "string"
        }
        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        print rest
        self.assertEqual(checkStatus, "success")
        global threadIdApplicant
        threadIdApplicant = rest["items"]["threadId"]

        global messageIdFromApplicant
        messageIdFromApplicant = rest["items"]["id"]


    def test_06_message_thread(self):
        url = self.base_url + "message/thread/?token=" + accessTokenEmplo
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        print rest
        self.assertEqual(checkStatus, "success")

    def test_07_message_thread_threadId_by_emplo(self):
      url = self.base_url + "message/thread/" + threadIdEmplo + "/?token=" + accessTokenEmplo
      r = requests.get(url, self.head)
      rest = json.loads(r.text)
      checkStatus = rest["status"]
      print rest
      self.assertEqual(checkStatus, "success")

    def test_07_message_thread_threadId_by_applicant(self):
      url = self.base_url + "message/thread/" + threadIdApplicant + "/?token=" + accessToken
      r = requests.get(url, self.head)
      rest = json.loads(r.text)
      checkStatus = rest["status"]
      print rest
      self.assertEqual(checkStatus, "success")

    def test_08_message_read_applicant(self):
        url = self.base_url + "message/read/?token=" + accessToken
        userInfo = {
            "messageId": messageIdFromEmplo,
        }
        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        print rest
        self.assertEqual(checkStatus, "success")

    def test_08_message_read_emplo(self):
        url = self.base_url + "message/read/?token=" + accessTokenEmplo
        userInfo = {
            "messageId": messageIdFromApplicant,
        }
        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        print rest
        self.assertEqual(checkStatus, "success")


    def test_09_message_check_applicant(self):
        url = self.base_url + "message/check/?token=" + accessToken
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        print rest
        self.assertEqual(checkStatus, "success")

    def test_09_message_check_emplo(self):
        url = self.base_url + "message/check/?token=" + accessTokenEmplo
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        print rest
        checkStatus = rest["status"]
        print rest
        self.assertEqual(checkStatus, "success")

    def test_10_threadId_info_applicant(self):
      url = self.base_url + "message/thread/" + threadIdApplicant + "/info/?token=" + accessToken
      r = requests.get(url, self.head)
      rest = json.loads(r.text)
      checkStatus = rest["status"]
      print rest
      self.assertEqual(checkStatus, "success")


    def test_11_threadId_info_emplo(self):
      url = self.base_url + "message/thread/" + threadIdEmplo + "/info/?token=" + accessToken
      print url
      r = requests.get(url, self.head)
      rest = json.loads(r.text)
      checkStatus = rest["status"]
      print rest
      self.assertEqual(checkStatus, "success")

