# -*- coding: utf-8 -*-
import requests, json, unittest,allure

@allure.MASTER_HELPER.story("Инициализация тестов")
@allure.MASTER_HELPER.severity(allure.MASTER_HELPER.severity_level.CRITICAL)
class setup(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://api-test.corp.profgallery.ru/api/"
        self.head = {"Content-Type": "application/json", "Accept": "application/json"}

    @allure.MASTER_HELPER.severity(allure.MASTER_HELPER.severity_level.CRITICAL)
    @allure.MASTER_HELPER.label("Запуск скрипта tests-init")
    def test_01(self):
        url = self.base_url + "tests-init/"
        r = requests.get(url, self.head)
        rest = json.loads(r.text)
        allure.MASTER_HELPER.attach("api response",rest)
        checkStatus = rest["status"]
        self.assertEqual(checkStatus, "success")
        my_file = open("setup.txt", "w")
        my_file.write(rest["message"])
        my_file.close()

