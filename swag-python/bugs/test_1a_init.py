# -*- coding: utf-8 -*-
import requests, json, unittest,allure

@allure.MASTER_HELPER.story("Инициализация тестов")
class setup(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://api-test.corp.profgallery.ru/api/"
        self.head = {"Content-Type": "application/json", "Accept": "application/json"}

    def test_01(self):
        allure.MASTER_HELPER.label("Test-init")
        url = self.base_url + "tests-init/"
        r = requests.get(url, self.head)
        print r
        rest = json.loads(r.text)
        print rest
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")
        my_file = open("setup.txt", "w")
        my_file.write(rest["message"])
        my_file.close()