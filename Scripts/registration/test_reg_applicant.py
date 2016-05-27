#!/usr/bin/python
# -*- coding: cp1251 -*-

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from random import randint
import unittest,time, sys



class mainPage(unittest.TestCase):
    #Настрйоки опций
    def setUp(self):
        #Урл
        self.base_url = sys.argv[0]
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
        #driver.find_element_by_id("select2-countryID-container").click()

        country_block = driver.find_element_by_id('countryID').find_element_by_xpath('..')
        country_block.find_element_by_css_selector('span.select2-selection__arrow').click()

        country_list = driver.find_elements_by_css_selector('ul#select2-countryID-results li')
        country_list[1].click()
        time.sleep(1)

        driver.find_element_by_xpath("//*[@id='select2-cityID-container']").click()
        driver.find_element_by_xpath("//*[@id='index-page']/body/span/span/span[1]/input").send_keys(u"Москва")
        driver.find_element_by_xpath("//*[@id='index-page']/body/span/span/span[1]/input").send_keys(Keys.ENTER)

        #driver.find_element_by_xpath("//input[@id='uPhone']").send_keys(randint(89000000000,89999999999))
        driver.find_element_by_xpath("//input[@id='uPhone2']").send_keys(str(randint(89000000000,89999999999)))
        driver.find_element_by_xpath("//*[@id='formUser']/div[11]/input").click()


        #Заполняем карьерную цель
        driver.find_element_by_xpath("//div[3]/div/a").click()
        driver.find_element_by_xpath("//*[@id='careerGoals']").send_keys(u"Карьерная цель")
        driver.find_element_by_xpath("//*[@id='block']/form/div/input").click()

        #Заполняем "текущий уровень дохода"
        driver.find_element_by_xpath("//div[3]/div[2]/a").click()
        driver.find_element_by_xpath("//*[@id='currentSalary']").send_keys(randint(50000,60000))
        driver.find_element_by_xpath("//*[@id='csAnnual']").send_keys(randint(500000, 600000))
        driver.find_element_by_xpath("//*[@id='block']/form/div[4]/input").click()

        #Заполняем "желаемый уровень дохода"
        driver.find_element_by_xpath("//div[3]/div[3]/a").click()
        driver.find_element_by_xpath("//*[@id='expectedSalary']").send_keys(randint(50000,60000))
        driver.find_element_by_xpath("//*[@id='esAnnual']").send_keys(randint(500000, 600000))
        driver.find_element_by_xpath("//*[@id='block']/form/div[3]/input").click()

        #Заполняем опыт работы
        driver.find_element_by_xpath("//div[3]/div[4]/a").click()
        driver.find_element_by_xpath("//*[@id='experience-ctName']").send_keys(u"Тестовое название компании")
        driver.find_element_by_xpath("//*[@id='beginYear']").send_keys(randint(1999,2005))
        driver.find_element_by_xpath("//*[@id='endYear']").send_keys(randint(2006,2010))
        driver.find_element_by_xpath("//*[@id='new-company']/a").click()
        driver.find_element_by_xpath("//*[@id='experience-edit-form']/div[2]/div[5]/div[1]/label[2]").click()
        driver.find_element_by_xpath("//input[@id='nn3']").click()
        driver.find_element_by_xpath("//*[@id='industryInput']").send_keys(u"Автомобильный бизнес")
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id='13503']").click()
        driver.find_element_by_xpath("//*[@id='experience-position']").send_keys(u"Тестовая Занимаемая Должность")
        driver.find_element_by_xpath("//*[@id='13307']").click()
        driver.find_element_by_xpath("//*[@id='experience-edit-form']/div[2]/div[9]/div[1]/div/div").click()
        driver.find_element_by_xpath("//*[@id='11551']").click()
        driver.find_element_by_xpath("//*[@id='modalMy']/div[3]/input").click()
        driver.find_element_by_xpath("//*[@id='experience-edit-form']/div[2]/div[9]/div[2]/ul/li/span/input").click()
        driver.find_element_by_xpath("//*[@id='subordinate']").send_keys(u"Уровень Подчинения")
        driver.find_element_by_xpath("//*[@id='directSubCount']").send_keys(randint(10,50))
        driver.find_element_by_xpath("//*[@id='experience-edit-form']/div[2]/div[10]/div[2]/div[2]/div").send_keys(u" Функциональные обязанности! Функциональные обязанности! Функциональные обязанности! Функциональные обязанности! Функциональные обязанности! Функциональные обязанности! Функциональные обязанности!")
        driver.find_element_by_xpath("//*[@id='experience-edit-form']/div[2]/div[11]/input").click()

        #Профессиональные и управленческие характеристики
        driver.find_element_by_xpath("//div[3]/div[5]/a").click()
        driver.find_element_by_xpath("//*[@id='commonExperience']").send_keys(randint(1,50))
        driver.find_element_by_xpath("//*[@id='leadingExperience']").send_keys(randint(1,50))
        driver.find_element_by_xpath("//*[@id='projectExperience']").send_keys(randint(1,50))
        driver.find_element_by_xpath("//*[@id='budgetControlSum']").send_keys(randint(1000000,5000000))
        driver.find_element_by_xpath("//div[5]/form/div[3]/input").click()

        #Ключевые навыки
        driver.find_element_by_xpath("//div[3]/div[6]/a").click()
        driver.find_element_by_xpath("//div[6]/form/div[2]/div[2]/div").send_keys(u"Ключевые навыки! Ключевые навыки! Ключевые навыки! Ключевые навыки! Ключевые навыки!")
        driver.find_element_by_xpath("//div[6]/form/div[3]/input").click()

        #Образование
        driver.find_element_by_xpath("//div[3]/div[7]/a").click()
        driver.find_element_by_xpath("//*[@id='institution']").send_keys(u"Образовательное учереждение")
        driver.find_element_by_xpath("//*[@id='faculty']").send_keys(u"Факультет")
        driver.find_element_by_xpath("//*[@id='specialty']").send_keys(u"Специальность")
        driver.find_element_by_xpath("//div[3]/div[2]/div/div/input").send_keys(randint(2000,2005))
        driver.find_element_by_xpath("//div[3]/div[2]/div/div[2]/input").send_keys(randint(2006,2010))
        ActionChains(driver).move_to_element(driver.find_element_by_xpath("//input[@name='education_save']")).click()




if __name__ == "__main__":
    unittest.main()
#Собираем наши  тесты в один общий тест
