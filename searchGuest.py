#!/usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
import unittest,time

class guestSerch(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://admin:hlj1ErT@Pg.fvds.ru"

    def test_guestApplicantSearch(self):
        driver = self.driver
        driver.get(self.base_url + "/applicant/search/")

        #Находим элемент с ID = search-submit-btn (кнопка "Найти") и нажимаем
        driver.find_element_by_id("search-submit-btn").click()

        #driver