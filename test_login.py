import logging
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as WDW
from webdriver_manager.chrome import ChromeDriverManager as CDM
import time

logging.basicConfig(
    level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',
    handlers =[
        logging.FileHandler("test_log.log", mode='w', encoding = 'utf-8-sig'),
        logging.StreamHandler()
    ],
    force=True
)
logging.getLogger('selenium').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('asyncio').setLevel(logging.WARNING)

@pytest.fixture
def driver():
    driver = webdriver.Chrome(service=Service(CDM().install()))
    driver.get("https://www.saucedemo.com/")
    yield driver
    driver.quit()

class TestLoginFlow:
    def test_login_flow(self, driver):
        try:
            WDW(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "user-name"))
            )
            self.login_info_input(driver)
            time.sleep(2)
            self.login_button_click(driver)
            time.sleep(5)
            logging.debug("ここまで来た")
            self.login_judge(driver)
        except Exception as e:
            logging.debug("error: %s", e)

    def login_info_input(self, driver):
        namearea = driver.find_element(By.ID, "user-name").send_keys("standard_user")
        passarea = driver.find_element(By.ID, "password").send_keys("secret_sauce")

    def login_button_click(self, driver):
        loginbutton = driver.find_element(By.ID, "login-button").click()

    def login_judge(self, driver):
        try:
            WDW(driver, 20).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "inventory_list"))
            )
            logging.info("ログイン成功")
            driver.save_screenshot("login_successed.png")
            print("成功")
        except Exception as e:
            logging.error("ログイン失敗: %s", e)
            driver.save_screenshot("login_failed.png")

    def test_login_invalid_name(self, driver):
        driver.find_element(By.ID, "user-name").send_keys("wrong_name")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        self.login_button_click(driver)
        self.login_error_judge(driver)


    def login_error_judge(self, driver):
        try:
            WDW(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "error-message-container"))
            )
            logging.info("ログイン失敗挙動")
            driver.save_screenshot("wrongInfo_login.png")
        except:
            logging.warning("危険！誤った情報でログインできる可能性があります")
            driver.save_screenshot("wrong_login.png")
            assert False

    def test_login_invalid_pass(self, driver):
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("wrong_pass")
        self.login_button_click(driver)
        self.login_error_judge(driver)

    def test_login_empty_fields(self, driver):
        self.login_button_click(driver)
        self.login_error_judge(driver)