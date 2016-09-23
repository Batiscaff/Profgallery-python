# -*- coding: utf-8 -*-
from selenium import webdriver
from random import randint
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import os

class Vacancy(object):
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver,10)
        self.base_url = "http://da.corp.profgallery.ru/app/"

    def open_vacancy(self):
        driver = self.driver
        driver.get(self.base_url + "")