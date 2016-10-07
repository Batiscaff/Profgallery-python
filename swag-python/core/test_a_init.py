# -*- coding: utf-8 -*-
import requests, json, unittest,allure

@allure.MASTER_HELPER.feature("Иницализация тестов")
@allure.MASTER_HELPER.testcase("Базовая инициализация тестов")
@allure.MASTER_HELPER.severity(allure.MASTER_HELPER.severity_level.CRITICAL)
class setup(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://api-test.corp.profgallery.ru/api/"
        self.head = {"Content-Type": "application/json", "Accept": "application/json"}

    @allure.MASTER_HELPER.step("Инициализируем тестовую базу")
    @allure.MASTER_HELPER.severity(allure.MASTER_HELPER.severity_level.CRITICAL)
    def test_01(self):
        url = self.base_url + "tests-init/"
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        print rest
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")
        my_file = open("setup.txt", "w")
        my_file.write(rest["message"])
        my_file.close()

