import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from EmailUtil import notify_manager
from util import load_json_data


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
        password_box = driver.find_element(By.XPATH, "//input[@type='password']")
        username_box.send_keys(username)
        password_box.send_keys(password)

        # click 'submit' button
        submit_button = driver.find_element(By.CLASS_NAME, 'login-button.ant-btn')
        submit_button.click()
    except Exception:
        # TODO: log error
        print("Cannot login in.")


def fill_health_info(driver, in_campus_status=True, location="jingjiang"):
    """ Fill the health info form, and submit. If have 'start process' page, click the 'start process' button, and then
    start to fill the form.

    :param driver: web driver
    :param in_campus_status: 'True' represent inside school, 'False' represent outside school
    :return: none
    """

    try:
        # click 'start process' button if needed
        if driver.title != "填报健康信息 Fill in health information - 学生健康状况申报":
            start_process(driver)

        # find the text boxes
        student_class = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.NAME, "fieldJBXXnj")) # wait the page to load
        )
        travel_record = driver.find_element(By.NAME, "fieldCXJL")
        # fill in text box
        student_class.send_keys("22电子信息")
        travel_record.send_keys("无")

        print("text boxed filled")

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

        print("checkboxes filled")

        # find the radios
        health_condition_1 = driver.find_element(By.ID, "V1_CTRL109")
        health_condition_2 = driver.find_element(By.ID, "V1_CTRL111")
        health_condition_3 = driver.find_element(By.ID, "V1_CTRL114")
        health_condition_4 = driver.find_element(By.ID, "V1_CTRL133")
        health_condition_5 = driver.find_element(By.ID, "V1_CTRL135")
        health_condition_6 = driver.find_element(By.ID, "V1_CTRL137")
        # click radio
        health_condition_1.click()
        health_condition_2.click()
        health_condition_3.click()
        health_condition_4.click()
        health_condition_5.click()
        health_condition_6.click()
        # default: inside school
        # check this radio instead of click it, because 'this radio is not clickable at represented point
        driver.execute_script("document.getElementById('fieldSFZX-0').checked = true;")
        # TODO: separate data
        # TODO: outside school, parse location string, choose region

        print("radio filled")

        # click 'submit' button
        submit_button = driver.find_element(By.CLASS_NAME, "command_button")
        submit_button.click()

        print("submit all information")
    except Exception:
        # TODO: log error
        print("over time")
    finally:
        driver.quit()


def start_process(driver):
    """ Click 'start process' button and then fill the health info.

    :param driver: web driver
    :param in_campus_status: 'True' represent inside school, 'False' represent outside school
    :return: none
    """
    try:
        # click the 'start process' button
        start_process = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, "preview_start_button"))
        )
        start_process.click()
        print("Enter the health info page.")

        # wait to new page (new url) load
        time.sleep(3)
    except Exception:
        # TODO: log error
        print("Cannot enter the start process page.")


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

        driver = webdriver.Chrome(service=ChromeService(executable_path=ChromeDriverManager().install()))
        driver.get("https://ehall.yzu.edu.cn/infoplus/form/XNYQSB/start")

        # login in
        title = driver.title
        if title == "统一身份认证平台":
            # need verify identity (every day need verify)
            try:
                verify_identity(driver, username, password)
                # TODO log
                print("Login in.")
            except Exception:
                notify_manager(name + " not login in")

        # wait page to load
        time.sleep(5)

        # fill the info
        try:
            fill_health_info(driver, in_campus_status, location)
        except Exception:
            notify_manager(name + " not fill the health the info")

        # end the session
        driver.quit()

def main():
    data = load_json_data("users-info.json")  # load users' info
    fill_for_multiply_user(data['users_info'])

if __name__ == "__main__":
    main()