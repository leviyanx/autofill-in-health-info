import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from EmailUtil import notify_manager
from util import load_json_data
import logging

# set log (output INFO level)
logging.basicConfig(filename="execution.log", encoding="utf-8",
                    level=logging.INFO, format='%(asctime)s %(message)s')


def verify_identity(driver, username, password):
    """Login in.

    :param driver: web driver
    :param username:
    :param password:
    :return: none
    """
    try:
        # fill in username and password
        # wait page to load (report failure if waiting time exceeded)
        username_box = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        password_box = driver.find_element(
            By.XPATH, "//input[@type='password']")
        username_box.send_keys(username)
        password_box.send_keys(password)

        # click 'submit' button
        submit_button = driver.find_element(
            By.CLASS_NAME, 'login-button.ant-btn')
        submit_button.click()

        logging.info("Login in")
    except Exception:
        logging.error(username + " cannot login in.")
        notify_manager(username + " cannot login in")


def fill_health_info(driver, in_campus_status=True, location="jingjiang", name=""):
    """ Fill the health info form, and submit. If the user has submitted health info, skip the process, else continue.

    :param driver: web driver
    :param in_campus_status: 'True' represent inside school, 'False' represent outside school
    :param location: location outside school
    :param name: name of user
    :return: none
    """

    try:
        # click the 'start process' button
        start_process = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, "preview_start_button"))
        )
        start_process.click()

        # wait to new page (new url) load or pop up the message that the user has submitted health info
        time.sleep(3)

        # recognize if the user has submitted the info
        # If the user has submitted, skip the user, else continue
        if has_submitted(driver):
            # the user has submitted info, skip
            logging.info(name + " has submitted the info")
        else:
            # the user need fill the form
            logging.info("Enter the health info page.")

            # find the text boxes
            student_class = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located(
                    (By.NAME, "fieldJBXXnj"))  # wait the page to load
            )
            travel_record = driver.find_element(By.NAME, "fieldCXJL")
            # fill in text box
            student_class.send_keys("22电子信息")
            travel_record.send_keys("无")

            logging.info("text boxed filled")

            # find checkbox
            promise_1 = driver.find_element(By.NAME, "fieldCN1")
            promise_2 = driver.find_element(By.NAME, "fieldCN2")
            promise_3 = driver.find_element(By.NAME, "fieldCN3")
            promise_4 = driver.find_element(By.NAME, "fieldCN4")
            promise_understand = driver.find_element(By.NAME, "fieldTBTX")
            promise = driver.find_element(By.NAME, "fieldCNS")
            # click checkbox
            promise_1.click()
            promise_2.click()
            promise_3.click()
            promise_4.click()
            promise_understand.click()
            promise.click()

            logging.info("checkboxes filled")

            # find the radios and select (not use 'click' because clicking radio is not stable)
            driver.execute_script(
                "document.getElementById('V1_CTRL109').checked = true;")  # health_condition_1
            driver.execute_script(
                "document.getElementById('V1_CTRL111').checked = true;")  # health_condition_2
            driver.execute_script(
                "document.getElementById('V1_CTRL114').checked = true;")  # health_condition_3
            driver.execute_script(
                "document.getElementById('V1_CTRL133').checked = true;")  # health_condition_4
            driver.execute_script(
                "document.getElementById('V1_CTRL135').checked = true;")  # health_condition_5
            driver.execute_script(
                "document.getElementById('V1_CTRL137').checked = true;")  # health_condition_6
            # default: inside school
            # check this radio instead of click it, because 'this radio is not clickable at represented point
            driver.execute_script(
                "document.getElementById('fieldSFZX-0').checked = true;")
            # TODO: separate data
            # TODO: outside school, parse location string, choose region

            logging.info("radio filled")

            # click 'submit' button
            submit_button = driver.find_element(
                By.CLASS_NAME, 'command_button')
            submit_button.click()

            # wait the form to be submitted
            time.sleep(10)

            logging.info("submit all information")
    except Exception:
        logging.error(name + " fill health info over time")
        notify_manager(name + " fill health info over time")


def has_submitted(driver):
    """ Check if the user has submitted health info.

    :param driver: web driver
    :return: If the user has submitted, return true, else return false
    """

    # If still stay the 'start process' page, means that the user has submitted
    if driver.title == "学生健康状况申报":
        return True
    else:
        return False


def fill_for_multiply_user(users):
    """Automatic fill health information for given users.

    :param users: user information, include username, password, in_campus_status, location
    :return: none
    """

    for user in users:
        # set single user info
        name = user['name']
        username = user['username']
        password = user['password']
        in_campus_status = user['in_campus_status']
        location = user['location']

        # config chrome driver to enable script to be performed in server
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=ChromeService(
            executable_path=ChromeDriverManager().install()), options=options)

        driver.get("https://ehall.yzu.edu.cn/infoplus/form/XNYQSB/start")

        # login in
        title = driver.title
        if title == "统一身份认证平台":
            # need verify identity (every day need verify)
            verify_identity(driver, username, password)

        # wait page to load
        time.sleep(5)

        # fill the info
        fill_health_info(driver, in_campus_status, location, name)

        # end the session
        driver.quit()


def main():
    data = load_json_data("users-info.json")  # load users' info
    fill_for_multiply_user(data['users_info'])


if __name__ == "__main__":
    main()
