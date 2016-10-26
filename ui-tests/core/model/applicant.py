# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains as AC
import os,random,time

class Applicant(object):
    def __init__(self, driver,base_url):
        self.driver = driver
        self.wait = WebDriverWait(driver,10)
        self.base_url = base_url

    def open_applicantprofile(self):
        driver = self.driver
        base_url = self.base_url
        driver.get(base_url + "applicant/profile/")
        WebDriverWait(driver,10).until(lambda s:s.find_element(By.XPATH,"//li[4]/h3"))

    def open_personal(self):
        driver = self.driver
        driver.find_element(By.XPATH,"//div[@id='person']/ul/i").click()

    def fill_personal_surname(self):
        driver = self.driver
        WebDriverWait(driver, 10).until(lambda s: s.find_element(By.XPATH, "//ul[@id='personEdit']/form/div/div/div/input"))
        driver.find_element(By.XPATH,"//ul[@id='personEdit']/form/div/div/div/input").send_keys("surname")

    def fill_personal_username(self):
        driver = self.driver
        WebDriverWait(driver, 10).until(lambda s: s.find_element(By.XPATH, "//div[@id='username']/div/input"))
        driver.find_element(By.XPATH,"//div[@id='username']/div/input").send_keys("surname")

    def fill_personal_middlename(self):
        driver = self.driver
        WebDriverWait(driver, 10).until(lambda s: s.find_element(By.XPATH, "//div[@id='username']/div[2]/input"))
        driver.find_element(By.XPATH,"//div[@id='username']/div[2]/input").send_keys("surname")

    def fill_sex(self):
        driver = self.driver
        WebDriverWait(driver, 10).until(lambda s: s.find_element(By.XPATH, "//div[3]/div/div/button"))
        driver.find_element(By.XPATH,"//div[3]/div/div/button").click()
        WebDriverWait(driver, 10).until(lambda s: s.find_element(By.XPATH, "//a[contains(text(),'Женский')]"))
        # driver.find_element(By.XPATH,"//a[contains(text(),'Женский')]").click()
        AC(driver).move_to_element(driver.find_element(By.XPATH,"//a[contains(text(),'Женский')]")).perform()
        driver.find_element_by_link_text(u"Женский").click()
        time.sleep(900000)

    def fill_phone(self):
        driver = self.driver
        WebDriverWait(driver,10).until(lambda x: x.find_element(By.CSS_SELECTOR,"label.communicate"))
        driver.find_element(By.XPATH,"//div[@id='phone']/div/input").send_keys(str(random.randint(89000000000,89999999999)))

    def fill_additionalphone(self):
        driver = self.driver
        WebDriverWait(driver,10).until(lambda x: x.find_element(By.CSS_SELECTOR,"label.communicate"))
        driver.find_element(By.XPATH,"//div[@id='additional_phone']/div/input").send_keys(str(random.randint(89000000000,89999999999)))

    def fill_commentphone(self):
        driver = self.driver
        WebDriverWait(driver, 10).until(lambda x: x.find_element(By.CSS_SELECTOR, "label.communicate"))
        driver.find_element(By.XPATH, "//div[@id='phone']/div[2]/input").send_keys("Comment phone")

    def fill_commentadditionphone(self):
        driver = self.driver
        WebDriverWait(driver, 10).until(lambda x: x.find_element(By.CSS_SELECTOR, "label.communicate"))
        driver.find_element(By.XPATH, "//div[@id='additional_phone']/div[2]/input").send_keys("Comment additional phone")

    def save_pesonal(self):
        driver = self.driver
        driver.find_element(By.XPATH,"//div[@id='contacts']/button").click()

    def break_personal(self):
        driver = self.driver
        driver.find_element(By.XPATH,"//div[@id='contacts']/button[2]").click()

    def open_current(self):
        driver = self.driver
        base_url = self.base_url
        driver.get(base_url + "applicant/profile/#current")
        driver.find_element(By.XPATH, "//li[@id='current']/div/i").click()

    def fill_currentmonth(self):
        driver = self.driver
        WebDriverWait(driver,10).until(lambda x: x.find_element(By.XPATH,"//li[@id='current']/div[2]/form/div/div/input"))
        driver.find_element(By.XPATH, "//li[@id='current']/div[2]/form/div/div/input").send_keys(str(random.randrange(50000,150000,10000)))

    def fill_currentyear(self):
        driver = self.driver
        WebDriverWait(driver,10).until(lambda x: x.find_element(By.XPATH,"//li[@id='current']/div[2]/form/div/div[2]/input"))
        driver.find_element(By.XPATH, "//li[@id='current']/div[2]/form/div/div[2]/input").send_keys(str(random.randrange(250000,500000,50000)))

    def save_current(self):
        driver = self.driver
        driver.find_element(By.XPATH, "//li[@id='current']/div[2]/form/button").click()

    def break_current(self):
        driver = self.driver
        driver.find_element(By.XPATH, "xpath=(//button[@type='button'])[22]s").click()

    def fill_dms(self):
        driver = self.driver
        WebDriverWait(driver, 10).until(
            lambda x: x.find_element(By.XPATH, "//li[@id='current']/div[2]/form/div/div[2]/input"))
        driver.find_element(By.XPATH, "//li[@id='current']/div[2]/form/div/div[2]/input").send_keys(
            str(random.randrange(250000, 500000, 50000)))





