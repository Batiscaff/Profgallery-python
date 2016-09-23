# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains as AC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import random,time

class Employer(object):
    def __init__(self, driver,base_url):
        self.driver = driver
        self.wait = WebDriverWait(driver,10)
        self.base_url = base_url

    def open_employerprofile(self):
        base_url = self.base_url
        driver = self.driver
        driver.get(base_url + "recruiter/profile")

    def open_employerstatic(self):
        base_url = self.base_url
        driver = self.driver
        driver.get(base_url + "recruiter/statistics")

    def open_companyedit(self):
        base_url = self.base_url
        driver = self.driver
        driver.get(base_url + "recruiter/edit")
        WebDriverWait(driver,10).until(lambda x:x.find_element(By.XPATH,"//div[@id='main-content']/div/div/div/div[2]/div/div/button"))

    def edit_companyinfo(self):
        driver = self.driver
        driver.find_element(By.XPATH,"//div[@id='main-content']/div/div/div/div[2]/div/div/button").click()
        WebDriverWait(driver,10).until(lambda x: x.find_element(By.XPATH,"//label"))

    def fill_commerciename(self):
        driver = self.driver
        driver.find_element(By.XPATH, "//div[2]/div/input").clear()
        driver.find_element(By.XPATH,"//div[2]/div/input").send_keys("Company " + str(random.randint(1000,9999)))

    def fill_companycountry(self):
        driver = self.driver
        WebDriverWait(driver,10).until(lambda x: x.find_element(By.CSS_SELECTOR,"button.select.dropdown-toggle"))
        driver.find_element(By.CSS_SELECTOR,"button.select.dropdown-toggle").click()
        time.sleep(1)
        WebDriverWait(driver,10).until(lambda x: x.find_element(By.XPATH,"//li/span"))
        driver.find_element(By.XPATH,"//li/span").click()

    def fill_companycity(self):
        driver = self.driver
        WebDriverWait(driver,10).until(lambda x:x.find_element(By.XPATH,"//div[2]/div/button"))
        driver.find_element(By.XPATH,"//div[2]/div/button").click()
        WebDriverWait(driver,10).until(lambda x: x.find_element(By.XPATH,"//li[2]/span"))
        driver.find_element(By.XPATH,"//li[2]/span").click()

    def fill_companyadress(self):
        driver = self.driver
        driver.find_element(By.XPATH, "//company-address/div/input").clear()
        driver.find_element(By.XPATH,"//company-address/div/input").send_keys("Company adress " + str(random.randint(1000,9999)))

    def edit_companysave(self):
        driver = self.driver
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

    def edit_companybreak(self):
        driver = self.driver
        driver.find_element(By.XPATH, "//button[2]").click()

    # Structure Type
    def open_structedit(self):
        driver = self.driver
        driver.execute_script("window.scrollTo(0,150);")
        WebDriverWait(driver,10).until(lambda x: x.find_element(By.XPATH,'//editable-block[2]/div/div/div/button'))
        driver.find_element(By.XPATH,"//editable-block[2]/div/div/div/button").click()

    def edit_companyindustry(self):
        driver = self.driver
        # driver.execute_script("window.scrollTo(0,150);")
        WebDriverWait(driver,10).until(lambda x: x.find_element(By.XPATH,'//span/button'))
        driver.find_element(By.XPATH,"//span/button").click()

    def fill_companyindustry(self):
        driver = self.driver
        WebDriverWait(driver,10).until(lambda x: x.find_element(By.XPATH,'//li[1]/span[2]'))
        driver.find_element(By.XPATH,"//li[" + str(random.randint(1,37)) + "]/span[2]").click()
        driver.find_element(By.XPATH,"//search-with-popup/div/div/div/button").click()

    def fill_companystructuretype(self):
        driver = self.driver
        WebDriverWait(driver,10).until(lambda x: x.find_element(By.XPATH,'//li[3]/label/span'))
        driver.find_element(By.XPATH,"//li[3]/label/span").click()

    def fill_companysecondind(self):
        driver = self.driver
        WebDriverWait(driver,10).until(lambda x: x.find_element(By.XPATH,'//checkbox-tree/ul/li[1]/label/span'))
        driver.find_element(By.XPATH,"//checkbox-tree/ul/li[1]/label/span").click()

    def edit_structuresave(self):
        driver = self.driver
        WebDriverWait(driver,10).until(lambda x: x.find_element(By.XPATH,'//editable-block[2]/div/div/div[2]/button'))
        driver.find_element(By.XPATH,"//editable-block[2]/div/div/div[2]/button").click()

    def edit_structurebreak(self):
        driver = self.driver
        WebDriverWait(driver,10).until(lambda x: x.find_element(By.XPATH,'//div[2]/button[2]'))
        driver.find_element(By.XPATH,"//div[2]/button[2]n").click()

    def edit_character(self):
        driver = self.driver
        WebDriverWait(driver,10).until(lambda x: x.find_element(By.XPATH,'//editable-block[3]/div/div/div/button'))
        driver.find_element(By.XPATH,"//editable-block[3]/div/div/div/button").click()

    def fill_money(self):
        driver = self.driver
        WebDriverWait(driver,10).until(lambda x: x.find_element(By.XPATH,'//property-edit/ul/li[4]/label/span'))
        driver.find_element(By.XPATH,"//property-edit/ul/li[" + random.randint(1,4) + "]/label/span").click()

    def edit_about(self):
        driver = self.driver
        WebDriverWait(driver,10).until(lambda x: x.find_element(By.XPATH,'//editable-block/div/div/div/button'))
        driver.find_element(By.XPATH,"//editable-block/div/div/div/button").click()

    def fill_abouturl(self):
        driver = self.driver
        WebDriverWait(driver,10).until(lambda x: x.find_element(By.XPATH,'//edit-mode/div[2]/div/input'))
        driver.find_element(By.XPATH,"//edit-mode/div[2]/div/input").send_keys("http://" + str(random.randint(1000,8888)) + ".ru")

    def fill_aboutabout(self):
        a = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed quis justo sollicitudin, elementum dui ac,
        nascetur ridiculus mus. In sit amet rutrum neque. Praesent condimentum leo sapien, sed elementum ex imperdiet ut. Aenean et ante augue. Suspendisse. """

        driver = self.driver
        WebDriverWait(driver, 10).until(lambda x: x.find_element(By.XPATH, '//textarea'))
        driver.find_element(By.XPATH, "//textarea").send_keys(a)

    def edit_aboutsave(self):
        driver = self.driver
        WebDriverWait(driver, 10).until(lambda x: x.find_element(By.XPATH, '//editable-block/div/div/div[2]/button'))
        driver.find_element(By.XPATH, "//editable-block/div/div/div[2]/button").click()

    def edit_aboutbreak(self):
        driver = self.driver
        WebDriverWait(driver, 10).until(lambda x: x.find_element(By.XPATH, '//div[2]/button[2]'))
        driver.find_element(By.XPATH, "//div[2]/button[2]").click()



