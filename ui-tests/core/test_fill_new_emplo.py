# -*- coding: utf-8 -*-

from selenium_fixtures import app
from model.loginuser import *

def test_new_emplo(app):
   app[0].regPage()
   app[0].regEmployer()
   app[0].regCompanyAdmin()
   app[0].regCompany()
   app[0].veryfiCompany()

def test_fill_companyinfo(app):
   app[2].open_companyedit()
   app[2].edit_companyinfo()
   app[2].fill_commerciename()
   app[2].fill_companycountry()
   app[2].fill_companycity()
   app[2].fill_companyadress()
   app[2].edit_companysave()

def test_fill_company_structuretype(app):
   app[2].open_companyedit()
   app[2].open_structedit()
   app[2].edit_companyindustry()
   app[2].fill_companyindustry()
   app[2].fill_companystructuretype()
   app[2].fill_companysecondind()
   app[2].edit_structuresave()

def test_fill_about_company(app):
   app[2].open_companyedit()
   app[2].edit_about()
   app[2].fill_aboutabout()
   app[2].fill_abouturl()
   app[2].edit_aboutsave()
















