# -*- coding: utf-8 -*-

import unittest,os

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
        driver.find_element_by_id('uName').send_keys(os.environ['applicant'])
        driver.find_element_by_id('uPassword').send_keys(os.environ['applicantPassword'])
        driver.find_element_by_xpath("//div[5]/div/input").click()
        self.webdriver.find_element_by_xpath("//a[contains(text(),'Поиск сотрудников')]")
        driver.get(url + '/employee/cabinet/profile/')
        self.webdriver.find_element_by_xpath("//a[contains(text(),'Поиск сотрудников')]")
        driver.get(url + '/employee/cabinet/vakansii/')
        self.webdriver.find_element_by_xpath("//a[contains(text(),'Поиск сотрудников')]")
        driver.get(url + '/employee/cabinet/messages/')
        self.webdriver.find_element_by_xpath("//a[contains(text(),'Поиск сотрудников')]")

    def test_02_applicant(self):
        driver = self.webdriver
        url = self.base_url
        driver.get(url + '/login')
        driver.find_element_by_id('uName').send_keys(os.environ['employer'])
        driver.find_element_by_id('uPassword').send_keys(os.environ['employerPassword'])
        driver.find_element_by_xpath("//div[5]/div/input").click()
        self.webdriver.find_element_by_xpath("//a[contains(text(),'Эффективность профиля')]")
        driver.get(url + '/applicant/cabinet/poisk-vakansij/')
        self.webdriver.find_element_by_xpath("//a[contains(text(),'Эффективность профиля')]")
        driver.get(url + '/applicant/cabinet/profile/')
        self.webdriver.find_element_by_xpath("//a[contains(text(),'Эффективность профиля')]")
        driver.get(url + '/applicant/cabinet/messages/')
        self.webdriver.find_element_by_xpath("//a[contains(text(),'Эффективность профиля')]")



