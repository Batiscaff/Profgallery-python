#!/usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
import unittest,time

class guestSerch(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)

    def tearDown(self):
        self.driver.quit()

    def test_guestResumeSearch_and_open(self):
        driver = self.driver
        driver.get(self.base_url + "/employee/search/")
        driver.maximize_window()
        #driver.save_screenshot("screen.png")
        #Находим элемент с ID = search-submit-btn (кнопка "Найти") и
        driver.find_element_by_id("search-submit-btn").click()
        driver.find_element_by_xpath(".//*[@id='result-list']/li[1]/div[2]/div[1]/div").click()
        #Перевлючаемся на активное
        main_window = driver.current_window_handle
        other_windows = [win for win in driver.window_handles if win != main_window]
        driver.switch_to_window(other_windows[0])

        #Убеждаемся, что мы зашли на страницу, нажав на кнопку "редактировать"
        time.sleep(10)
        #driver.find_element_by_xpath("//div[@id='company-info']/div/div[2]/div[4]/a").click()
