# -*- coding: utf-8 -*-
from selenium import webdriver
from random import randint
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import os,json,requests

class Application(object):
    def __init__(self, driver, base_url):
        self.driver = driver
        self.wait = WebDriverWait(driver,10)
        self.base_url = base_url

    def homepage(self):
        driver = self.driver
        driver.get(self.base_url)
        driver.maximize_window()

    def regPage(self):
        driver = self.driver
        driver.get(self.base_url)
        driver.maximize_window()
        driver.get(self.base_url + "register/")

    def regApplicant(self):
        driver = self.driver
        driver.maximize_window()
        driver.find_element_by_xpath("//label").click()
        driver.find_element_by_xpath("//input[@type='email']").send_keys('test' + str(randint(1000, 9999)) + '@test.ru')
        driver.find_element_by_xpath("//input[@type='password']").send_keys('123456789')
        driver.find_element_by_xpath('//div[4]/input').send_keys('123456789')
        driver.find_element_by_xpath("//div[5]/div/input").send_keys('123456789')
        driver.find_element_by_xpath("//form/button").click()

    def regEmployer(self):
        driver = self.driver
        driver.maximize_window()
        driver.find_element_by_xpath("//label[2]").click()
        # Запоминаем почту для верификации компании
        global useremail
        useremail = 'test' + str(randint(1000, 9999)) + '@test.ru'
        print useremail
        WebDriverWait(driver, 10).until(lambda x: x.find_element(By.XPATH, "//input[@type='email']"))
        driver.find_element_by_xpath("//input[@type='email']").send_keys(useremail)

        WebDriverWait(driver, 10).until(lambda x: x.find_element(By.XPATH, "//input[@type='password']"))
        driver.find_element_by_xpath("//input[@type='password']").send_keys('123456789')

        WebDriverWait(driver, 10).until(lambda x: x.find_element(By.XPATH, "//div[4]/input"))
        driver.find_element_by_xpath('//div[4]/input').send_keys('123456789')
        driver.find_element_by_xpath("//div[5]/div/input").send_keys('Captcha')
        driver.find_element_by_xpath("//form/button").click()

    def regCompanyAdmin(self):
        driver = self.driver
        WebDriverWait(driver,10).until(lambda x: x.find_element(By.XPATH,"//div[6]/label"))
        driver.find_element(By.XPATH,"//input").send_keys(u"Фамилия")

        WebDriverWait(driver, 10).until(lambda x: x.find_element(By.XPATH, "//div[2]/input"))
        driver.find_element(By.XPATH, "//div[2]/input").send_keys(u"Имя")

        WebDriverWait(driver, 10).until(lambda x: x.find_element(By.XPATH, "//div[3]/input"))
        driver.find_element(By.XPATH, "//div[3]/input").send_keys(u"Отчество")

        WebDriverWait(driver, 10).until(lambda x: x.find_element(By.XPATH, "//div[4]/input"))
        driver.find_element(By.XPATH, "//div[4]/input").send_keys(u"Дожность")

        WebDriverWait(driver, 10).until(lambda x: x.find_element(By.XPATH, "//div[5]/input"))
        driver.find_element(By.XPATH, "//div[5]/input").send_keys(str(randint(89000000000,89999999999)))

        WebDriverWait(driver, 10).until(lambda x: x.find_element(By.XPATH, "//form/button"))
        driver.find_element(By.XPATH, "//form/button").click()

    def regCompany(self):
        driver = self.driver
        WebDriverWait(driver, 10).until(lambda x: x.find_element(By.XPATH, "//company-address/div/input"))

        WebDriverWait(driver, 10).until(lambda x: x.find_element(By.XPATH, "//input"))
        driver.find_element(By.XPATH, "//input").send_keys(u"Фирменное имя " + str(randint(1000,9999)))

        WebDriverWait(driver, 10).until(lambda x: x.find_element(By.XPATH, "//div[2]/input"))
        driver.find_element(By.XPATH, "//div[2]/input").send_keys(u"Коммерческое имя " + str(randint(1000,9999)))

        WebDriverWait(driver, 10).until(lambda x: x.find_element(By.XPATH, "//div[4]/input"))
        driver.find_element(By.XPATH, "//div[4]/input").send_keys(str(randint(100000000000,999999999999)))

        WebDriverWait(driver, 10).until(lambda x: x.find_element(By.XPATH, "//geochooser/div/div/div/button"))
        driver.find_element(By.XPATH, "//geochooser/div/div/div/button").click()

        WebDriverWait(driver,10).until(lambda x: x.find_element(By.XPATH,"//li/span"))
        driver.find_element(By.XPATH, "//li/span").click()

        driver.find_element(By.XPATH, "//div[2]/div/button").click()
        WebDriverWait(driver, 10).until(lambda x: x.find_element(By.XPATH, "//li[2]/span"))
        driver.find_element(By.XPATH, "//li[2]/span").click()

        driver.find_element(By.XPATH, "//company-address/div/input").send_keys(u"Адрес компании "+ str(randint(1000,9999)))
        driver.find_element(By.XPATH,"//div[6]/button").click()
        WebDriverWait(driver,10).until(lambda x: x.find_element(By.XPATH,"//h1"))

    def veryfiCompany(self):
        # Модерируем компанию
        url = "http://api.corp.profgallery.ru/api/recruiter/?limit=10000&token=profTest"
        head = {"Content-Type": "application/json", "Accept": "application/json"}
        r = requests.get(url, head)
        rest = json.loads(r.text)
        for i in xrange(len(rest["items"])):
            if rest["items"][i]["email"] == useremail:
                print "Нашел!"
                global userid
                userid = rest["items"][i]["id"]
                print userid
        url = "http://api.corp.profgallery.ru/api/recruiter/" + userid + "/?token=profTest"
        r = requests.get(url, head)
        r = json.loads(r.text)
        partnerid = r["items"]["partnerId"]
        url = "http://api.corp.profgallery.ru/api/company/" + partnerid + "/update/?token=profTest"
        userInfo = {
            "fieldName": "isVerified",
            "fieldValue": 1
        }
        requests.post(url=url, data=json.dumps(userInfo), headers=head)


    def login(self,user):
        driver = self.driver
        driver.find_element_by_xpath("//li[5]/div/button").click()
        driver.find_element_by_xpath("//ul/li[2]/a").click()
        wait = WebDriverWait(driver, 10)
        wait.until(lambda s: s.find_element(By.CSS_SELECTOR, "h3").text == u"Вход в личный кабинет")
        driver.find_element_by_xpath("//input[@type='email']").clear()
        driver.find_element_by_xpath("//input[@type='email']").send_keys(user.username)
        driver.find_element_by_xpath("//input[@type='password']").clear()
        driver.find_element_by_xpath("//input[@type='password']").send_keys(user.password)
        driver.find_element_by_css_selector("button.form-submit.apply").click()

    def is_login(self):
        driver  = self.driver
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH,"//li[5]/a")))
            return True
        except EC:
            return False

    def is_on_reg_emplo(self):
            driver = self.driver
            url = driver.current_url
            assert (url,self.base_url + "recruiter/contacts")

    def in_on_reg_company(self):
        driver = self.driver
        url = driver.current_url
        assert (url, self.base_url + "recruiter/contacts")

    def login_incorrect(self):
        driver = self.driver
        driver.find_element_by_xpath("//li[5]/div/button").click()
        driver.find_element_by_xpath("//ul/li[2]/a").click()
        wait = WebDriverWait(driver, 10)
        wait.until(lambda s: s.find_element(By.CSS_SELECTOR, "h3").text == u"Вход в личный кабинет")
        driver.find_element_by_xpath("//input[@type='email']").clear()
        driver.find_element_by_xpath("//input[@type='email']").send_keys("test_incorrect@" \
                                                                         + str(randint(1,99999)) + ".ru")
        driver.find_element_by_xpath("//input[@type='password']").clear()
        driver.find_element_by_xpath("//input[@type='password']").send_keys("12345678")
        driver.find_element_by_css_selector("button.form-submit.apply").click()
        wait.until(lambda x: x.find_element(By.XPATH,"//form/div").text == u"Логин или пароль неверны.")

