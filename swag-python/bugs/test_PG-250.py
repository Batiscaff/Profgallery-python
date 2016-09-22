# -*- coding: utf-8 -*-

from random import randint
import unittest, json, requests, time

username = ["Адам", "Вадим", "Евгений", "Никита",
            "Дмитрий",    "Михаил"]
usersurname = ["ФамилияОдин", "ФамилияДва", "Фамилия3"]
usermiddlename = ["ОтчествоОдин", "ОтчествоДва", "Отчетство3"]
requiredFields = ["user", "education", "experience", "character"]
userFileds = ["name", "surname", "phone", "middle_name"]


class userComplitedPositive(unittest.TestCase):
    def setUp(self):
        my_file = open("../core/setup.txt", "r")
        self.base_url ="http://api-test.corp.profgallery.ru/api/"
        self.head = {"Content-Type": "application/json", "Accept": "application/json","testing-db": my_file.read()}

    def test_00_testini(self):
        # Регим соискателя
        url = self.base_url + "user/register/"
        userInfo = {
            "login": "test_" + str(randint(10000, 99999)) + "@blalba.ru",
            "password": "string",
            "type": "4"}
        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")
        global accessToken
        accessToken = str(rest["items"]["accessToken"])
        global uid
        uid = str(rest["items"]["id"])
        print uid

        # Регим работодателя
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
        print accessTokenRecruter


        # Находим список компаний
        url = self.base_url + "company/?token=" + accessToken
        r = requests.get(url, self.head)
        global companyIDList
        companyIDList = json.loads(r.text)
        checkStatus = companyIDList["status"]
        self.assertEqual(checkStatus, "success")

        # Берем ID индустрии
        url = self.base_url + "vocabulary/gejob_branch/tree/?token=" + accessToken
        r = requests.get(url, self.head)
        global indistryList
        indistryList = json.loads(r.text)
        checkStatus = indistryList["status"]
        self.assertEqual(checkStatus, "success")

        # Берем gejob_position
        url = self.base_url + "vocabulary/gejob_position/tree/?token=" + accessToken
        r = requests.get(url, self.head)
        global positionIdList
        positionIdList = json.loads(r.text)
        checkStatus = positionIdList["status"]
        self.assertEqual(checkStatus, "success")

        # Кэшируем Properties
        url = self.base_url + "vocabulary/grading/tree/?token=" + accessToken
        r = requests.get(url, self.head)
        global functionID
        functionID = json.loads(r.text)
        checkStatus = functionID["status"]
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
        global eduID
        eduID = []
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
                "beginYear": randint(1999, 2005),
                "endYear": randint(2007, 2012),
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

            eduID.append(rest["items"]["id"])

    def test_03_applicant_characteristic(self):
        url = self.base_url + "applicant/" + uid + "/characteristics/update/?token=" + accessToken
        project = randint(5, 10)
        managment = randint(5, 10)
        totalExp = project + managment + 2
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
        for i in xrange(randint(1, 3)):
            url = self.base_url + "applicant/" + uid + "/experience/new/?token=" + accessToken
            global positionIdTitle
            positionIdTitle = positionIdList["items"][randint(0, len(positionIdList["items"]) - 1)]["element"]["title"]
            print positionIdTitle
            userInfo = {
                "type": 1,
                "companyId": companyIDList["items"][randint(0, len(companyIDList["items"]) - 1)]["id"],
                "companyNote": "string",
                "started": "10.02.2005",
                "position": positionIdTitle,
                "responsibilities": "string",
                "achievements": "string",
                "subordinate": "string",
                "completed": 1,
                "directScount": 40,
                "funcScount": 10,
                "projectScount": 30,
                "industryId": indistryList["items"][randint(0, len(indistryList["items"]) - 1)]["element"]["id"]
            }
            r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
            rest = json.loads(r.text)
            checkStatus = rest["status"]
            self.assertEqual(checkStatus, "success")
            expListId.append(rest["items"]["id"])

            # добавляяем Property
            url = self.base_url + "applicant/" + uid + "/experience/" + rest["items"][
                "id"] + "/property/add/?token=" + accessToken
            userInfo = {
                "propertyId": [functionID["items"][randint(0, len(functionID["items"]) - 1)]["element"]["id"]],
                "isMain": 1
            }
            r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
            rest = json.loads(r.text)
            checkStatus = rest["status"]
            self.assertEqual(checkStatus, "success")

        time.sleep(1)

    def test_05_search_build(self):
        url = self.base_url + "search/applicant/?token=" + accessTokenRecruter
        userInfo = {
            "text": positionIdTitle,
            "limit": 100
        }
        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")
        userList = []
        for i in xrange(len(rest["items"]['list'])):
            userList.append(rest["items"]['list'][i]["user"]["id"])

        self.assertIn(uid, userList, "Созданный пользователь не в индексе!")

    def test_06_search_remove(self):
        dice = requiredFields[randint(0, len(requiredFields) - 1)]
        if dice == "user":
            print "user!"
            url = self.base_url + "user/" + uid + "/update/multiple/?token=" + accessToken
            userInfo = {
                "multiple": [
                    {
                        "fieldName": "middle_name",
                        "fieldValue": None
                    },
                    {
                        "fieldName": "surname",
                        "fieldValue": None
                    },
                    {
                        "fieldName": "name",
                        "fieldValue": None
                    },
                    {
                        "fieldName": "phone",
                        "fieldValue": None
                    }
                ]
            }
            r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
            rest = json.loads(r.text)
            checkStatus = rest["status"]
            self.assertEqual(checkStatus, "success")

        elif dice == "education":
            print "edu!"
            for x in eduID:
                url = self.base_url + "applicant/" + uid + "/education/" + x + "/delete/?token=" + accessToken
                print url
                r = requests.get(url, self.head)
                rest = json.loads(r.text)
                checkStatus = rest["status"]
                self.assertEqual(checkStatus, "success")

        elif dice == "experience":
            print "exp!"
            for i in xrange(len(expListId)):
                url = self.base_url + "applicant/" + uid + "/experience/" + expListId[i] + "/delete/?token=" + accessToken
                print url
                r = requests.get(url, self.head)
                rest = json.loads(r.text)
                checkStatus = rest["status"]
                self.assertEqual(checkStatus, "success")
                i += 1

        elif dice == "character":
            print "char!"
            url = self.base_url + "applicant/" + uid + "/characteristics/update/?token=" + accessToken
            userInfo = {
                "project": None,
                "totalExperience": None,
                "management": None,
                "budget": None
            }
            r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
            rest = json.loads(r.text)
            checkStatus = rest["status"]
            self.assertEqual(checkStatus, "success")

        time.sleep(1)

        url = self.base_url + "search/applicant/?token=" + accessTokenRecruter
        userInfo = {
            "text": positionIdTitle,
            "limit": 100
        }
        r = requests.post(url=url, data=json.dumps(userInfo), headers=self.head)
        rest = json.loads(r.text)
        print rest
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")
        userList = []
        for i in xrange(0, len(rest["items"]["list"])):
            userList.append(rest["items"]["list"][i]["user"]["id"])
            i += 1
        print userList
        self.assertNotIn(uid, userList, "Пользователь с незаполненным полем в индексе!")
