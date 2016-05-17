#!/usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver import ActionChains
import unittest,time, pytest

class guestSerch(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://admin:hlj1ErT@Pg.fvds.ru"

    def tearDown(self):
        self.driver.quit()

    def test_guestApplicantSearch(self):
        driver = self.driver
        driver.get(self.base_url + "/applicant/search/")
        driver.maximize_window()
        #driver.save_screenshot("screen.png")
        #Находим элемент с ID = search-submit-btn (кнопка "Найти") и
        driver.find_element_by_id("search-submit-btn").click()
        driver.find_element_by_xpath("//ul[@id='result-list']/li[2]").click()
        #Перевлючаемся на активное
        main_window = driver.current_window_handle
        other_windows = [win for win in driver.window_handles if win != main_window]
        driver.switch_to_window(other_windows[0])

        driver.find_element_by_xpath("//div[@id='company-info']/div/div[2]/div[4]/a").click()


