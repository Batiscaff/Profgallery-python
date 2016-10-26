import pytest
from model.applicationmanager import *
from model.applicant import *
from model.employer import *
import os

@pytest.fixture(scope="session")
def app(request):
    # driver =  os.environ("browser")
    driver =  webdriver.Chrome()
    base_url = os.environ["url"]
    return Application(driver,base_url),Applicant(driver,base_url),Employer(driver,base_url)
