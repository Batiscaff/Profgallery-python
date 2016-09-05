#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint
import unittest, json, requests, random


class findGeneral(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://api-test.corp.profgallery.ru/api/"
        self.head = {"Content-Type": "application/json", "Accept": "application/json"}

    def test_00_register_user_recruter(self):
        url = self.base_url + "tests-init/"
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

        url = self.base_url + "user/register/"
        userInfo = {
            "login": "test_" + str(randint(10000, 99999)) + "@blalba.ru",
            "password": "string",
            "type": "8"}
        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        # Проверка на success
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")

        global accessToken
        accessToken = str(rest["items"]["accessToken"])

        global uid
        uid = str(rest["items"]["id"])

    def test_01_search_function(self):
        global status
        status = "false"
        global status2
        status2 = False
        # Выбираем функция
        requestError = 0

        funtionList = []
        while status != "find":
            # Выбираем функцию из словаря, которую будем искать
            url = self.base_url + "vocabulary/gejob_function/tree/?token=profTest"
            r = requests.get(url, self.head)
            rest = json.loads(r.text)
            checkStatus = rest["status"]
            self.assertEqual(checkStatus, "success")

            # Выбираем отрасль
            func = randint(0, random.randint(0, len(rest["items"]) - 1))
            global userFunction
            userFunction = rest["items"][func]["child"][randint(0, len(rest["items"][func]["child"]) - 1)]["element"][
                "id"]
            print "Найденная функция пользователя: " + str(userFunction)
            # userFunction = 11604

            # Проверяем ну дубли
            if userFunction in funtionList:
                continue

            funtionList.append(userFunction)
            # Производим поиск по соискателям и добавляем их в массив
            global userList
            userList = []
            # Поиск осуществляем от рекрутера
            url = self.base_url + "search/applicant/?token=" + accessToken
            userInfo = {
                "properties": {
                    "gejob_function": [userFunction]
                }
            }
            r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
            rest = json.loads(r.text)
            checkStatus = rest["status"]
            self.assertEqual(checkStatus, "success")

            global varA
            varA = 0
            # Проверяем, найдены ли пользователи по нашему запросу
            if len(rest["items"]) > 0:
                status = "find"
                for i in xrange(len(rest["items"])):
                    userList.append(rest["items"][varA]["user"]["id"])
                    varA = + 1
            requestError = requestError + 1
            self.assertIsNot(15, requestError, "Более 15 неудачных поисковых запросов")
            print userList

        # Для каждого пользователя из списка userList
        varUser = 0
        for i in xrange(len(userList)):
            status2 = False
            while status2 == False:
                # Получаем список работы
                url = self.base_url + "applicant/" + userList[varUser] + "/experience/?token=profTest"
                r = requests.get(url, self.head)
                rest = json.loads(r.text)
                checkStatus = rest["status"]
                self.assertEqual(checkStatus, "success")

                # Cобираем ID работ пользователя
                varA = 0
                userExpList = []
                for j in xrange(len(rest["items"])):
                    userExpList.append(rest["items"][varA]["id"])
                    varA = varA + 1

                varExp = 0
                userProperties = []
                # Собираем Properties в массив
                for x in range(0, len(userExpList)):
                    url = self.base_url + "applicant/" + userList[varUser] + "/experience/" + userExpList[
                        varExp] + "/property/?token=profTest"
                    varExp = varExp + 1
                    r = requests.get(url, self.head)
                    rest = json.loads(r.text)
                    checkStatus = rest["status"]
                    self.assertEqual(checkStatus, "success")
                    varC = 0
                    for key in range(0, len(rest["items"]["isMain"])):
                        userProperties.append(int(rest["items"]["isMain"][varC]))
                        varC = varC + 1

                print userProperties
                self.assertIn(userFunction, userProperties)
                # Проверяем массив на наличие
                varUser = varUser + 1
                status2 = True

    def test_02_search_branch(self):
        global status
        status = False
        global status2
        status2 = False
        requestError = 0
        branchList = []

        while status != "find":
            # Выбираем отрасль из словаря, которую будем искать
            url = self.base_url + "vocabulary/gejob_branch/tree/?token=profTest"
            r = requests.get(url, self.head)
            rest = json.loads(r.text)
            checkStatus = rest["status"]
            self.assertEqual(checkStatus, "success")

            # Выбираем отрасль
            func = randint(0, random.randint(0, len(rest["items"]) - 1))
            global userBranch

            i = randint(0, 1)
            if i == 0:
                print "Ищем по основной отрасли"
                userBranch = rest["items"][func]["element"]["id"]
                print "Найденная отрасль " + str(userBranch)

            else:
                print "ищем по подотрасли "
                userBranch = rest["items"][func]["child"][randint(0, len(rest["items"][func]["child"]) - 1)]["element"][
                    "id"]
                print "Найденная отрасль " + str(userBranch)
            # userBranch = 11604

            # Проверяем ну дубли
            if userBranch in branchList:
                continue

            branchList.append(userBranch)
            # Производим поиск по соискателям и добавляем их в массив
            global userList
            userList = []
            # Поиск осуществляем от рекрутера
            url = self.base_url + "search/applicant/?token=" + accessToken
            userInfo = {
                "properties": {
                    "gejob_branch": [userBranch]
                }
            }
            r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
            rest = json.loads(r.text)
            checkStatus = rest["status"]
            self.assertEqual(checkStatus, "success")

            global varA
            varA = 0
            # Проверяем, найдены ли пользователи по нашему запросу
            if len(rest["items"]) > 0:
                status = "find"
                for i in range(0, len(rest["items"])):
                    userList.append(rest["items"][varA]["user"]["id"])
                    varA = + 1
            requestError = requestError + 1
            self.assertIsNot(15, requestError, "Более 15 неудачных поисковых запросов")
            print userList

        # Для каждого пользователя из списка userList
        varUser = 0
        for i in range(0, len(userList)):
            status2 = False
            while status2 == False:
                # Получаем список работы
                url = self.base_url + "applicant/" + userList[varUser] + "/experience/?token=" + accessToken
                r = requests.get(url, self.head)
                rest = json.loads(r.text)
                checkStatus = rest["status"]
                self.assertEqual(checkStatus, "success")

                # Cобираем id опыта работы пользователя
                varA = 0
                userExpList = []
                for j in xrange(len(rest["items"])):
                    userExpList.append(rest["items"][varA]["id"])
                    varA = varA + 1

                varExp = 0
                userProperites = []
                # Собираем branch в массив
                for x in xrange(len(userExpList)):
                    # Собираем отрасли
                    url = self.base_url + "applicant/" + userList[varUser] + "/experience/?token=profTest"
                    r = requests.get(url, self.head)
                    rest = json.loads(r.text)
                    checkStatus = rest["status"]
                    self.assertEqual(checkStatus, "success")
                    userProperites.append(rest["items"][varExp]["industryId"])

                    # Собираем подотрасли
                    url = self.base_url + "applicant/" + userList[varUser] + "/experience/" + userExpList[
                        varExp] + "/property/?token=profTest"
                    varExp = varExp + 1
                    r = requests.get(url, self.head)
                    rest = json.loads(r.text)
                    checkStatus = rest["status"]
                    self.assertEqual(checkStatus, "success")
                    varC = 0
                    for key in xrange(len(rest["items"]["company"])):
                        userProperites.append(int(rest["items"]["company"][varC]))
                        varC += 1

                print userProperites
                self.assertIn(userBranch, userProperites)
                # Проверяем массив на наличие
                varUser = varUser + 1
                status2 = True

    def test_03_final(self):
        url = self.base_url + "applicant/" + uid + "/percent/?token=" + accessToken
        print url
