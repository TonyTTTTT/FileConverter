import unittest
from appium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import os.path
from pathlib import Path
import PyInstaller.__main__
import time


class UsecasesTests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        PyInstaller.__main__.run([
            '../gui.py',
            '-y',
            '--distpath=executable',
            '--workpath=executable/build'
            '--clean'
        ])
        # set up appium
        desired_caps = {"app": os.path.join(os.getcwd(), "executable/gui/gui.exe"),
                        "platformName": "Windows",
                        "deviceName": "WindowsPC",
                        "newCommandTimeout": 10000}
        self.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4723/wd/hub',
            desired_capabilities=desired_caps)

    @classmethod
    def tearDownClass(self):
        self.driver.quit()

    def test_img2pdf(self):
        actions = ActionChains(self.driver)

        self.select_usecase(actions, 40)

        self.select_file(actions, '"img1.jpg""img2.jpg""img3.jpg"')

        actions.reset_actions()
        WebDriverWait(self.driver, 100).until(EC.element_to_be_clickable((By.XPATH, "/Window/Pane/Pane[2]/Pane")))
        actions.drag_and_drop_by_offset(self.driver.find_element_by_xpath("/Window/Pane/Pane[2]/Pane"), 0, -100).perform()

        self.save_file(actions)

        time.sleep(2)

    def test_pdf2img(self):
        actions = ActionChains(self.driver)

        self.select_usecase(actions, 30)

        self.select_file(actions, "PDF1.pdf")

        actions.reset_actions()
        WebDriverWait(self.driver, 100).until(EC.element_to_be_clickable((By.XPATH, "/Window/Pane/Pane[2]/Pane[2]")))
        actions.move_to_element(self.driver.find_element_by_xpath("/Window/Pane/Pane[2]/Pane[2]")).click().\
            move_by_offset(0,-50).click().perform()

        self.save_file(actions)

        time.sleep(2)

    def test_combinePDF(self):
        actions = ActionChains(self.driver)

        self.select_usecase(actions, 60)

        self.select_file(actions, '"PDF1.pdf""PDF2.pdf"')

        actions.reset_actions()
        WebDriverWait(self.driver, 100).until(EC.element_to_be_clickable((By.XPATH, "/Window/Pane/Pane[2]/Pane")))
        actions.drag_and_drop_by_offset(self.driver.find_element_by_xpath("/Window/Pane/Pane[2]/Pane"), 0, -100).perform()

        actions.reset_actions()
        actions.click(self.driver.find_element_by_xpath(("/Window/Pane/Pane[2]/Button"))).perform()

        actions.reset_actions()
        WebDriverWait(self.driver, 100).until(EC.element_to_be_clickable((By.XPATH, "/Window/Pane/Pane[2]/Pane[1]")))
        actions.click(self.driver.find_element_by_xpath("/Window/Pane/Pane[2]/Pane[1]")).perform()

        actions.reset_actions()
        actions.move_by_offset(0, -20).click().perform()

        self.save_file(actions)

        time.sleep(2)

    def test_extractPDF(self):
        actions = ActionChains(self.driver)

        self.select_usecase(actions, 80)

        self.select_file(actions, '"PDF2.pdf"')

        actions.reset_actions()
        WebDriverWait(self.driver, 100).until(EC.element_to_be_clickable((By.XPATH, "/Window/Pane/Pane[2]/Pane[2]")))
        actions.click(self.driver.find_element_by_xpath("/Window/Pane/Pane[2]/Pane[2]")).move_by_offset(0, 50).\
            click().perform()

        actions.reset_actions()
        actions.click(self.driver.find_element_by_xpath("/Window/Pane/Pane[2]/Pane[1]")).move_by_offset(0, 150).\
            click().perform()

        self.save_file(actions)

        time.sleep(2)

    def select_file(self, actions, file_name):
        actions.reset_actions()
        actions.click(self.driver.find_element_by_xpath("//ProgressBar/Pane/ToolBar")) \
            .send_keys(Path.cwd().absolute().__str__() + Keys.ENTER).perform()

        actions.reset_actions()
        actions.click(self.driver.find_element_by_xpath("/Window/Window/ComboBox[1]/Edit")).\
            send_keys(file_name).perform()

        actions.reset_actions()
        actions.click(self.driver.find_element_by_xpath("/Window/Window/Button[1]")).perform()

    def select_usecase(self, actions, usecase_offset):
        actions.reset_actions()
        actions.click(self.driver.find_element_by_xpath("/Window/Pane/Pane[3]/Pane")).perform()

        actions.reset_actions()
        actions.move_by_offset(0, usecase_offset).click().perform()

        actions.reset_actions()
        actions.click(self.driver.find_element_by_xpath("/Window/Pane/Pane[3]/Button")).perform()

    def save_file(self, actions):
        actions.reset_actions()
        actions.click(self.driver.find_element_by_xpath("/Window/Pane/Pane[1]/Button")).perform()

        actions.reset_actions()
        actions.click(self.driver.find_element_by_xpath("//ProgressBar/Pane/ToolBar")). \
            send_keys(Path.joinpath(Path.cwd().parent.absolute(), 'result').__str__() + Keys.ENTER).perform()

        actions.reset_actions()
        actions.click(self.driver.find_element_by_xpath("/Window/Window/Button[1]")).perform()

        actions.reset_actions()
        WebDriverWait(self.driver, 100).until(EC.element_to_be_clickable((By.XPATH, "/Window/Pane/Pane[1]/Button[1]")))
        actions.click(self.driver.find_element_by_xpath("/Window/Pane/Pane[1]/Button[1]")).perform()

        actions.reset_actions()
        actions.click(self.driver.find_element_by_xpath("/Window/Window/Button")).perform()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(UsecasesTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
