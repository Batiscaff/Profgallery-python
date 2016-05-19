#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint
import unittest,json, requests


class test_regUser(unittest.TestCase):
    def setUp(self):
        self.base_url ="http://api.corp.profgallery.ru/api/"
        self.head = {"Content-Type": "application/json", "Accept": "application/json"}


    def test_a_register_user(self):
        url = self.base_url + "user/register/"
        userInfo = {
            "login": "test_" + str(randint(1000, 9999)) + "@blalba.ru",
            "password": "string",
            "type": "4"}
        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        # Проверка на success
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

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

    def test_w_applicant_id_education(self):
        url = self.base_url +"applicant/" + uid + "/education/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

    def test_w_aapplicant_id_education_new(self):
        url = self.base_url +"applicant/" + uid + "/education/?token=" + accessToken
        userInfo = {
          "institution": "string",
          "speciality": "string",
          "endYear": "string",
          "faculty": "string",
          "eduLevel": "string",
          "eduType": "string",
          "isAdditional": 0,
          "degree": "string",
          "beginYear": "string",
          "cdate": "string",
          "mdate": "string",
          "completed": 0,
          "course": "string",
          "certificate": "string"
        }

        r = requests.post(url,json.dumps(userInfo),self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

        global eduID
        eduID = rest["id"]

    def test_w_applicant_id_education_update(self):
        url = self.base_url +"applicant/" + uid + "/education/" + eduID +"/update/?token=" + accessToken

        userInfo = {
          "institution": "string",
        }

        r = requests.post(url,json.dumps(userInfo),self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

    def test_w_applicant_id_education_eduId_delete(self):
        url = self.base_url +"applicant/" + uid + "/education/" + eduID +"/delete/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")
    """
    def test_w_applicant_update(self):
        url = self.base_url +"applicant/" + uid + "/update/?token=" + accessToken
        print url
        userInfo = {
            "fieldName": "skills",
            "fieldValue": "string"
        }
        r = requests.post(url,json.dumps(userInfo),self.head)
        rest = json.loads(r.text)
        print rest
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")"""

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
          "userId": 0,
          "title": "string",
          "description": "string",
          "salaryMonthMin": 0,
          "salaryYearMin": 0,
          "cdate": "string",
          "mdate": "string",
          "geoId": 0,
          "availabilityOfGoal": 0
        }
        r = requests.post(url,json.dumps(userInfo),self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

        global goalID
        goalID = rest['item']["id"]

    def test_w_applicant_id_goal_goalID(self):
        url = self.base_url +"applicant/" + uid + "/goals/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

    def test_w_applicant_id_goal_update(self):
        url = self.base_url +"applicant/" + uid + "/goal/" + eduID +"/update/?token=" + accessToken

        userInfo = {
          "description": "string-1",
        }

        r = requests.post(url,json.dumps(userInfo),self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

    def test_w_applicant_id_goal_delete(self):
        url = self.base_url +"applicant/" + uid + "/goal/" + eduID +"/delete/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")


if __name__ == "__main__":
    unittest.main()