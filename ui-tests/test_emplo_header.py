# -*- coding: utf-8 -*-

import unittest,sys
reload(sys)

from selenium import webdriver

class findEmploHeader(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://profgallery.com"
        self.webdriver = webdriver.Firefox()

    def tearDown(self):
        self.webdriver.quit()

    def test_01_emplohead(self):
        driver = self.webdriver
        url = self.base_url
        driver.get(url + '/login')
        driver.find_element_by_id('uName').send_keys("sm@profgallery.com")
        driver.find_element_by_id('uPassword').send_keys("12378999")
        driver.find_element_by_xpath("//div[5]/div/input").click()
        self.webdriver.find_element_by_xpath("//a[contains(text(),'Поиск сотрудников')]")
        driver.get(url + '/employee/cabinet/profile/')
        self.webdriver.find_element_by_xpath("//a[contains(text(),'Поиск сотрудников')]")
        driver.get(url + '/employee/cabinet/vakansii/')
        self.webdriver.find_element_by_xpath("//a[contains(text(),'Поиск сотрудников')]")
        driver.get(url + '/employee/cabinet/messages/')
        self.webdriver.find_element_by_xpath("//a[contains(text(),'Поиск сотрудников')]")



