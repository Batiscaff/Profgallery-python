#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint
import unittest,json, requests,random


class test_regUser(unittest.TestCase):
    def setUp(self):
        self.base_url ="http://api.corp.profgallery.ru/api/"
        self.head = {"Content-Type": "application/json", "Accept": "application/json"}


    def test_a_register_user(self):
        url = self.base_url + "user/register/"
        userInfo = {
            "login": "test_" + str(randint(10000,99999)) + "@blalba.ru",
            "password": "string",
            "type": "4"}
        r = requests.post(url=url,data=json.dumps(userInfo),headers=self.head)
        rest = json.loads(r.text)
        #Проверка на success
        checkStatus = rest["status"]
        self.assertEqual(checkStatus,"success")

        # Запоминаем для дальнейшей работы
        global uid
        uid = str(rest["items"]["id"])
        global accessToken
        accessToken = str(rest["items"]["accessToken"])
        global email
        email = rest["items"]["email"]

    def test_w_applicant_id_percent(self):
        url = self.base_url +"applicant/" + uid + "/percent/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

    def test_w_applicant_id(self):
        url = self.base_url +"applicant/" + uid + "/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

    def test_w_applicant_id_character(self):
        url = self.base_url +"applicant/" + uid + "/characteristics/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

    def test_w_applicant_id_experience(self):
        url = self.base_url +"applicant/" + uid + "/experience/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

    def test_w_applicant_id_experience_new(self):
        #Берем ID компании
        url = self.base_url + "company/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        global companyID
        companyID = len(rest["items"]) - 1
        companyID = randint(0,companyID)
        companyID = rest["items"][companyID]["id"]

        #Берем ID индустрии
        url = self.base_url + "vocabulary/17/tree/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        global indistryID
        indistryID = len(rest["items"]) - 1
        indistryID = randint(0,indistryID)
        indistryID = rest["items"][indistryID]["element"]["id"]

        url = self.base_url +"applicant/" + uid + "/experience/new/?token=" + accessToken
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
          "industryId": indistryID
        }
        r = requests.post(url=url,data=json.dumps(userInfo),headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")
        #Запоминаем созданный ID опыта работы
        global expId
        expId = str(rest["items"]["id"])



    def test_w_applicant_id_experience_w_delete(self):
        url = self.base_url +"applicant/" + uid + "/experience/" + expId + "/delete/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")


    def test_w_applicant_id_experience_z_expID_propery_add(self):
        url = self.base_url + "applicant/" + uid + "/experience/" + expId + "/property/add/?token=" + accessToken

        #Берем список функций
        url = self.base_url + "vocabulary/25/tree/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)

        #Берем ID фукции
        functionID = len(rest["items"]) - 1

        functionList = []
        if (len(rest["items"][functionID]["child"]) == 0 ):
            functionList = [3800]

        else:
            for i in range(0,randint(1,5)):
                functionID = len(rest["items"][1]["element"])
                functionID = randint(0,functionID) - 1
                #Из Items мы берем второй элемент (Функции), от неё берет Child, в нем ищем по FunctID, element, id
                functionID = rest["items"][1]["child"][functionID]["element"]["id"]
                functionList.append(functionID)

        #лист для удаления
        global  functionListRemove
        functionListRemove = functionList
        userInfo = {
          "propertyId": functionList
        }

        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")


        """
        ######################################
        Добавление происходит массивом, удаление же происходит по 1 функции.
        Леонов Василий: Пока на данный тест кладем. Ждем пока реализуют данный метод "в железо", что бы сделать максимально похожим


    def test_w_applicant_id_experience_z_expID_property_remove(self):
        url = self.base_url + "applicant/" + uid + "/experience/" + expId + "/property/remove/?token=" + accessToken

        print functionListRemove
        userInfo = {
            "propertyId": functionListRemove
        }

        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        print rest
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")"""


    def test_w_applicant_id_education(self):
        url = self.base_url +"applicant/" + uid + "/education/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

    def test_w_aapplicant_id_education_new(self):
        url = self.base_url +"applicant/" + uid + "/education/new/?token=" + accessToken
        userInfo = {
          "id": 0,
          "institution": "string",
          "speciality": "string",
          "endYear": 2012,
          "faculty": "string",
          "eduLevel": 0,
          "eduType": 0,
          "isAdditional": 0,
          "degree": 0,
          "beginYear": 2007,
          "cdate": "string",
          "mdate": "string",
          "completed": 0,
          "course": "string",
          "certificate": "string"
        }

        r = requests.post(url=url,data=json.dumps(userInfo),headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

        global eduID
        eduID = str(rest["items"]["id"])

    def test_w_applicant_id_education_update(self):
        url = self.base_url + "applicant/" + uid + "/education/" + eduID + "/update/?token=" + accessToken
        userInfo = {
            "fieldName": "faculty",
            "fieldValue": "string"
        }

        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

    def test_w_applicant_id_education_z_eduId_delete(self):
        url = self.base_url +"applicant/" + uid + "/education/" + eduID +"/delete/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")


    def test_w_applicant_update(self):
        url = self.base_url +"applicant/" + uid + "/update/?token=" + accessToken
        userInfo = {
            "fieldName": "skills",
            "fieldValue": "string"
        }
        r = requests.post(url=url,data=json.dumps(userInfo),headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

    def test_w_applicant_id_stats(self):
        url = self.base_url +"applicant/" + uid + "/stats/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

    def test_w_applicant_goals(self):
        url = self.base_url +"applicant/" + uid + "/goals/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

    def test_w_applicant_goal_add(self):
        url = self.base_url +"applicant/" + uid + "/goal/add/?token=" + accessToken
        userInfo = {
          "title": "string",
          "description": "string",
          "salaryMonthMin": 0,
          "salaryYearMin": 0,
          "cdate": "string",
          "mdate": "string",
          "geoId": 0,
          "availabilityOfGoal": 0
        }
        r = requests.post(url=url,data=json.dumps(userInfo),headers=self.head)

        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

        global goalID
        goalID = str(rest['items']["id"])

    def test_w_applicant_id_goal_goalID(self):
        url = self.base_url +"applicant/" + uid + "/goals/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

    def test_w_applicant_id_goal_update(self):
        url = self.base_url +"applicant/" + uid + "/goal/" + goalID +"/update/?token=" + accessToken

        userInfo = {
          "fieldName": "title",
          "fieldValue": "string"
        }
        r = requests.post(url=url,data=json.dumps(userInfo),headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

    def test_w_applicant_id_goal_z_delete(self):
        url = self.base_url +"applicant/" + uid + "/goal/" + goalID +"/delete/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

    def test_w_applicant_id_referer(self):
        url = self.base_url +"applicant/" + uid + "/referrer/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

    def test_w_applicant_id_referer_new(self):
        url = self.base_url +"applicant/" + uid + "/referrer/new/?token=" + accessToken
        userInfo = {
            "companyId": companyID,
            "position": "string",
            "referrerType": randint(1,3),
            "availabilityOfName": randint(1,4),
            "availabilityOfCompany": randint(1,4)
        }
        r = requests.post(url=url,data=json.dumps(userInfo),headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")
        global refId
        refId = str(rest["items"]["id"])

    def test_w_applicant_id_referer_w_delete(self):
        url = self.base_url +"applicant/" + uid + "/referrer/" + refId + "/delete/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

    def test_w_applicant_language(self):
        url = self.base_url +"applicant/" + uid + "/language/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")


    def test_w_applicant_language_new(self):
        # Берем ID языка
        url = self.base_url + "vocabulary/71/tree/?token=" + accessToken
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

        global langId
        langId = len(rest["items"]) - 1
        langId = randint(0, langId)
        langId = rest["items"][langId]["element"]["id"]

        url = self.base_url + "applicant/" + uid + "/language/new/?token=" + accessToken

        userInfo = {
            "languageId": langId,
            "title": "string" + str(randint(0, 100)),
            "languageDegreeId": random.randrange(10, 40, 10)
        }
        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

    def test_w_applicant_language_update(self):
        url = self.base_url + "applicant/" + uid + "/language/update/?token=" + accessToken
        userInfo = {
            "languageId": langId,
            "title": "string" + str(randint(0, 100)),
            "languageDegreeId": random.randrange(10, 40, 10)
        }
        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

    def test_wz_applicant_language_del(self):
        url = self.base_url +"applicant/" + uid + "/language/" + str(langId) + "/delete/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")



if __name__ == "__main__":
    unittest.main()
