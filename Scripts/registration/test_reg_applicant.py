#!/usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from random import randint
import unittest,time, sys


class mainPage(unittest.TestCase):
    #Настрйоки опций
    def setUp(self):
        #Урл
        self.base_url = sys.argv[1]
        #Выбор браузера
        self.driver = webdriver.Firefox()
        #Настрйоки ожидания (Сколько ждать перед тем, как прервать тест)
        self.driver.implicitly_wait(30)
    # Функция завершения работы браузера.
    def tearDown(self):
        self.driver.quit()

    def test_applicantReg(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.maximize_window()
        #Выбираем меню, которое будем автоматизировать
        menu_elements = driver.find_elements_by_css_selector('div.menu > ul > li')
        #Наводим на него мышку, иначе работать не будет
        ActionChains(driver).move_to_element(menu_elements[2]).perform()
        #Ищем по css кнопку, с именем li.registration-btn и нажимаем на неё click()
        driver.find_element_by_css_selector('li.registration-btn').click()
        driver.find_element_by_css_selector('a[data-reg=applicant]').click()
        #Вбираем поле, с именем uEmailи вводим (send_keys) значения
        driver.find_element_by_css_selector('input[name="uEmail"]').send_keys("applicant" + str(randint(1000,9999)) + "@test.test")
        driver.find_element_by_css_selector('input[name="uPassword"]').send_keys("12345678")
        driver.find_element_by_css_selector('input[name="uPasswordConfirm"]').send_keys("12345678")
        driver.find_element_by_css_selector('input[name="regCaptchaCode"]').send_keys("12345678")
        driver.find_element_by_css_selector('input.custom-btn.green').click()
        #Проверяем, что мы зарегистрированы и есть блок "Опыт работы"
        for i in range(10):
            try:
                if u"Опыт работы" == driver.find_element_by_xpath("(//div[@id='block']/div)[10]").text: break
            except: pass
            time.sleep(1)
        else: self.fail("time out")

        #Заполняем профиль
        driver.find_element_by_xpath("//*[@id='personal-block']/a").click()
        driver.find_element_by_id("uLastName").send_keys(u"ФамилияТестовая")
        driver.find_element_by_id("uFirstName").send_keys(u"ИмяТестовое")
        driver.find_element_by_id("uPatronymic").send_keys(u"ОтчествоТестовое")
        driver.find_element_by_id("select2-countryID-container").click()
        select = driver.find_element_by_id("select2-countryID-container")
        select.send_keys(Keys.ARROW_DOWN)
        time.sleep(10)


        driver.find_element_by_xpath("//div[@id='block']/a").click()

if __name__ == "__main__":
    unittest.main()
#Собираем наши  тесты в один общий тест
