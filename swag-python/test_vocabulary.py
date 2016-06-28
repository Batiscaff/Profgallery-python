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


    def  test_vocabularies(self):
         url = self.base_url + "vocabularies/?token=" + accessToken
         r = requests.get(url, self.head)
         rest = json.loads(r.text)
         checkStatus = rest["status"]
         self.assertEqual(checkStatus, "success")
         global vocId
         vocId = len(rest["items"]) - 1
         vocId = randint(0, vocId)
         vocId = str(rest["items"][vocId]["id"])

    def test_vocabularies_id(self):
        url = self.base_url + "vocabulary/" + vocId +  "/items/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus,"success")

    def test_vocabularies_id_tree(self):
        url = self.base_url + "vocabulary/" + vocId +  "/tree/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus,"success")

    def test_vocabularies_id_search(self):
        url = self.base_url + "vocabulary/17/search/?search=%D0%B0%D0%B2%D1%82%D0%BE&token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus,"success")

    def test_vocabularies_item_itemid_leveled(self):
        url = self.base_url + "vocabulary/" + vocId + "/leveled/?level=" + str(randint(0,3)) +"&token=" + accessToken
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

    def test_vocabularies_item_itemid_compatible(self):
        url = self.base_url + "vocabulary/item/13604/compatible/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus,"success")

    def test_id_language(self):
        url = self.base_url + "applicant/" + uid +  "/language/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus,"success")

    def test_id_language_add(self):
        url = self.base_url + "vocabulary/71/items/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)

        global langId
        langId = len(rest["items"]) - 1
        langId = randint(0, langId)
        langId = str(rest["items"][langId]["id"])

        url = self.base_url + "applicant/" + uid + "/language/new/?token=" + accessToken
        userInfo = {
            "languageId": langId,
            "languageDegreeId": random.randrange(10,40,10)
        }
        r = requests.post(url=url,data=json.dumps(userInfo),headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus,"success")

    def test_id_language_update(self):
        url = self.base_url + "applicant/" + uid + "/language/update/?token=" + accessToken
        userInfo = {
            "languageId": langId,
            "languageDegreeId": random.randrange(10,40,10)
        }
        r = requests.post(url=url,data=json.dumps(userInfo),headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus,"success")

    def test_id_language_w_delete(self):
        url = self.base_url + "applicant/" + uid +"/language/" + langId +"/delete/?token=" + accessToken
        r = requests.get(url,self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus,"success")


if __name__ == "__main__":
    unittest.main()