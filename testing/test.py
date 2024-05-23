#******************************************************************************
#
# Copyright (c) 2016 Microsoft Corporation. All rights reserved.
#
# This code is licensed under the MIT License (MIT).
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# // LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#******************************************************************************


import unittest
from appium import webdriver
# from appium.options.windows import WindowsOptions
# from appium.options.common import AppiumOptions
# from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.action_chains import ActionBuilder
import time
from selenium.webdriver.common.actions.pointer_input import PointerInput
import PyInstaller.__main__
from pathlib import Path
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class SimpleCalculatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # set up appium
        desired_caps = {"app": "C:\\Users\\TonyTTTTT\\Desktop\\side-project\\FileConverter\\testing\\dist\\gui\\gui.exe",
                        "platformName": "Windows",
                        "deviceName": "WindowsPC",
                        "newCommandTimeout": 10000}
        self.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4723/wd/hub',
            desired_capabilities=desired_caps)

    @classmethod
    def tearDownClass(self):
        self.driver.quit()

    def test_pdf2img(self):

        # actions.click(self.driver.find_element_by_xpath("/Window/Pane/Pane[3]/Button"))
        self.driver.find_element_by_xpath("/Window/Pane/Pane[3]/Button").click()
        # time.sleep(2)
        # self.driver.find_element_by_xpath("//ProgressBar/Pane").click()
        # self.driver.find_element_by_xpath("//ProgressBar/Pane/ToolBar").click()
        # WebDriverWait(self.driver, 10000).until(EC.element_to_be_clickable(By.XPATH, "//ProgressBar/Pane/ToolBar"))
        actions = ActionChains(self.driver)
        actions.click(self.driver.find_element_by_xpath("//ProgressBar/Pane/ToolBar"))\
            .send_keys("C:/Users/TonyTTTTT/Desktop/side-project/FileConverter"+Keys.ENTER).perform()

        actions.reset_actions()
        actions.click(self.driver.find_element_by_xpath("/Window/Window/ComboBox[1]/Edit")).send_keys("TAB.pdf").perform()

        actions.reset_actions()
        actions.click(self.driver.find_element_by_xpath("/Window/Window/Button[1]")).perform()

        WebDriverWait(self.driver, 1000).until(EC.element_to_be_clickable((By.XPATH, "/Window/Pane/Pane[1]/Pane[2]")))

        actions.reset_actions()
        actions.move_to_element(self.driver.find_element_by_xpath("/Window/Pane/Pane[1]/Pane[2]")).click().\
            move_by_offset(0,-50).click()

        actions.perform()

        # self.driver.find_element_by_xpath("/Window/Window/button[0]").click()


        time.sleep(2)


if __name__ == '__main__':
    # PyInstaller.__main__.run([
    #     '../gui.py',
    #     '-y',
    #     '--clean'
    # ])

    suite = unittest.TestLoader().loadTestsFromTestCase(SimpleCalculatorTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
