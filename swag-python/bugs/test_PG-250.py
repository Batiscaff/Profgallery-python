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

        def test_00_register_recruter(self):
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
            checkStatus = rest["status"]
            self.assertEqual(checkStatus, "success")
            global accessTokenRecruter
            accessTokenRecruter = str(rest["items"]["accessToken"])

        def test_00_register_user(self):
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

            url = self.base_url + "applicant/" + uid + "/update/?token=" + accessToken
            userInfo = {
                "fieldName": "availabilityOfProfile",
                "fieldValue": 1}
            r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
            rest = json.loads(r.text)
            checkStatus = rest["status"]
            self.assertEqual(checkStatus, "success")

        def test_02_applicant_edu(self):
            for i in xrange(randint(1, 3)):
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
                    "beginYear": randint(1999,2005),
                    "endYear": randint(2007,2012),
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

                global eduID
                eduID = []
                eduID.append(str(rest["items"]["id"]))


        def test_03_applicant_characteristic(self):
            url = self.base_url + "applicant/" + uid + "/characteristics/update/?token=" + accessToken
            project = randint(5, 10)
            managment = randint(5, 10)
            totalExp = project + managment
            userInfo = {
                "project": project,
                "totalExperience": totalExp,
                "management": managment,
                "budget": randint(1000000, 99999999)
            }
            r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
            rest = json.loads(r.text)
            checkStatus = rest["status"]
            self.assertEqual(checkStatus, "success")

        def test_04_applicant_exp(self):
            global expListId
            expListId = []
            for i in xrange(randint(1,5)):
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
                global indistryID
                indistryID = len(rest["items"]) - 1
                indistryID = randint(0, indistryID)
                indistryID = rest["items"][indistryID]["element"]["id"]

                # Берем gejob_position
                url = self.base_url + "vocabulary/gejob_position/tree/?token=" + accessToken
                r = requests.get(url, self.head)
                rest = json.loads(r.text)
                positionId = len(rest["items"]) - 1
                positionId = randint(0, positionId)
                global positionIdText
                positionIdText = rest["items"][positionId]["element"]["title"]

                url = self.base_url + "applicant/" + uid + "/experience/new/?token=" + accessToken
                userInfo = {
                    "type": 1,
                    "companyId": companyID,
                    "companyNote": "string",
                    "started": "10.02.2005",
                    "position": positionIdText,
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

                # добавляяем Property
                url = self.base_url + "vocabulary/grading/tree/?token=" + accessToken
                r = requests.get(url, self.head)
                rest = json.loads(r.text)
                functionID = rest["items"][randint(0, len(rest["items"]) - 1)]["element"]["id"]
                url = self.base_url + "applicant/" + uid + "/experience/" + expId + "/property/add/?token=" + accessToken
                userInfo = {
                    "propertyId": [functionID],
                    "isMain": 1
                }
                r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
                rest = json.loads(r.text)
                checkStatus = rest["status"]
                self.assertEqual(checkStatus, "success")

        def test_05_search_build(self):
            url = self.base_url + "applicant/" + uid + "/percent/?token=" + accessToken
            r = requests.get(url, self.head)
            rest = json.loads(r.text)
            checkStatus = rest["status"]
            self.assertEqual(checkStatus, "success")

            url = self.base_url + "search/build/?token=profTest"
            r = requests.get(url, self.head)
            rest = json.loads(r.text)
            checkStatus = rest["status"]
            self.assertEqual(checkStatus, "success")

            url = self.base_url + "search/reindex/?token=profTest"
            r = requests.get(url, self.head)
            rest = json.loads(r.text)
            checkStatus = rest["status"]
            self.assertEqual(checkStatus, "success")
            url = self.base_url + "search/applicant/?token=" + accessTokenRecruter
            userInfo = {
                    "text" : positionIdText
            }
            r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
            rest = json.loads(r.text)
            checkStatus = rest["status"]
            self.assertEqual(checkStatus,"success")
            userList = []
            j = 0
            for i in xrange(len(rest["items"])):
                userList.append(rest["items"][j]["user"]["id"])
                j += 1
            self.assertIn(uid,userList,"Созданный пользователь не в индексе!")

        def test_06_search_remove(self):
            dice =  randint(1,len(requiredFields))
            for i in xrange(dice):
                    dice = requiredFields[randint(0, len(requiredFields) - 1)]
                    if dice == "user":
                        userAppends = {}
                        fuckIt = []
                        checkList = []
                        for j in xrange(len(userFileds)):
                            dice1 = userFileds[randint(0,len(userFileds)-1)]
                            if dice1 not in checkList:
                                if dice1 == "phone":
                                    userAppends.update({"fieldName": "phone",  "fieldValue": None})
                                    fuckIt.append(userAppends)
                                    checkList.append("phone")
                                elif dice1 == "name":
                                    userAppends.update({"fieldName": "name",  "fieldValue": None})
                                    fuckIt.append(userAppends)
                                    checkList.append("name")
                                elif dice1 == "surname":
                                    userAppends.update({"fieldName": "surname",  "fieldValue": None})
                                    fuckIt.append(userAppends)
                                    checkList.append("surname")
                                elif dice1 == "middle_name":
                                    userAppends.update({"fieldName": "middle_name",  "fieldValue": None})
                                    fuckIt.append(userAppends)
                                    checkList.append("middle_name")
                            url = self.base_url + "user/" + uid + "/update/multiple/?token=" + accessToken
                            userInfo = {
                                "multiple": fuckIt
                            }
                            r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
                            rest = json.loads(r.text)
                            checkStatus = rest["status"]
                            self.assertEqual(checkStatus, "success")

                    elif dice == "education":
                        for x in eduID:
                            print x
                            url = self.base_url + "applicant/" + uid + "/education/" + x + "/delete/?token=" + accessToken
                            r = requests.get(url, self.head)
                            rest = json.loads(r.text)
                            checkStatus = rest["status"]
                            self.assertEqual(checkStatus, "success")

                    elif dice == "experience":
                        count = 0
                        for i in xrange(len(expListId)):
                            url = self.base_url + "applicant/" + uid + "/experience/" + expListId[count] + "/delete/?token=" + accessToken
                            r = requests.get(url, self.head)
                            rest = json.loads(r.text)
                            checkStatus = rest["status"]
                            self.assertEqual(checkStatus, "success")
                            count += 1

                    elif dice == "character":
                        url = self.base_url + "applicant/" + uid + "/characteristics/update/?token=" + accessToken
                        userInfo = {
                            "project": None,
                            "totalExperience": None,
                            "management": None,
                            "budget": None
                        }

                    requiredFields.remove(dice)

            url = self.base_url + "search/build/?token=profTest"
            r = requests.get(url, self.head)
            rest = json.loads(r.text)
            checkStatus = rest["status"]
            self.assertEqual(checkStatus, "success")

            url = self.base_url + "search/reindex/?token=profTest"
            r = requests.get(url, self.head)
            rest = json.loads(r.text)
            checkStatus = rest["status"]
            self.assertEqual(checkStatus, "success")


            url = self.base_url + "search/applicant/?token=" + accessTokenRecruter
            userInfo = {
                    "text" : positionIdText,
                    "limit": 100
            }
            r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
            rest = json.loads(r.text)
            checkStatus = rest["status"]
            self.assertEqual(checkStatus,"success")
            userList = []
            j = 0
            for i in xrange(0,len(rest["items"])):
                userList.append(rest["items"][j]["user"]["id"])
                j =+ 1
            self.assertNotIn(uid,userList,"Пользователь с незаполненным полем в индексе!")