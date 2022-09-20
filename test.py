import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def verify_identity(driver):
    try:
        # wait page to load (report failure if waiting time exceeded)
        username_box = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        password_box = driver.find_element(By.XPATH, "//input[@type='password']")

        # TODO: separate data
        # fill in username and password
        username_box.send_keys("MZ120220574")
        password_box.send_keys("Yl15252627912_yz")

        # submit
        submit_button = driver.find_element(By.CLASS_NAME, 'login-button.ant-btn')
        submit_button.click()
    except Exception:
        # TODO: notify user
        print("Cannot load the SSO page.")

def start_process(driver):
    try:
        start_process = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, "preview_start_button"))
        )
        start_process.click()
        print("Enter the health info page.")
    except Exception:
        # TODO: notify user
        print("Cannot enter the start process page.")


def fill_health_info(driver, in_campous_status=True):
    """
    driver: web driver
    in_campous_status: True -> inside school, False -> outside school
    """

    try:
        # text box
        student_class = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.NAME, "fieldJBXXnj"))
        )
        travel_record = driver.find_element(By.NAME, "fieldCXJL")

        student_class.send_keys("22电子信息")
        travel_record.send_keys("无")

        print("text boxed filled")

        # checkbox
        promise_1 = driver.find_element(By.NAME, "fieldCN1")
        promise_2 = driver.find_element(By.NAME, "fieldCN2")
        promise_3 = driver.find_element(By.NAME, "fieldCN3")
        promise_4 = driver.find_element(By.NAME, "fieldCN4")
        promise_understand = driver.find_element(By.NAME, "fieldTBTX")
        promise = driver.find_element(By.NAME, "fieldCNS")

        promise_1.click()
        promise_2.click()
        promise_3.click()
        promise_4.click()
        promise_understand.click()
        promise.click()

        # random check
        print(promise.is_selected())
        print("checkboxes filled")

        # radio
        health_condition_1 = driver.find_element(By.ID, "V1_CTRL109")
        health_condition_2 = driver.find_element(By.ID, "V1_CTRL111")
        health_condition_3 = driver.find_element(By.ID, "V1_CTRL114")
        health_condition_4 = driver.find_element(By.ID, "V1_CTRL133")
        health_condition_5 = driver.find_element(By.ID, "V1_CTRL135")
        health_condition_6 = driver.find_element(By.ID, "V1_CTRL137")
        # TODO: separate data
        # TODO: outside school, choose region
        # default: inside school
        in_campous = driver.find_element(By.ID, "fieldSFZX-0")
        # if not in_campous_status:
        #     in_campous = driver.find_element(By.ID, "fieldSFZX-1")  # outside school

        health_condition_1.click()
        health_condition_2.click()
        health_condition_3.click()
        health_condition_4.click()
        health_condition_5.click()
        health_condition_6.click()
        in_campous.click()

        print("radio filled")

        # submit
        submit_button = driver.find_element(By.CLASS_NAME, "command_button")
        submit_button.click()

        print("submit all information")

        time.sleep(10)
    except Exception:
        print("over time")
    finally:
        driver.quit()

def main():
    driver = webdriver.Chrome(service=ChromeService(executable_path=ChromeDriverManager().install()))

    # TODO: separate data
    driver.get("https://ehall.yzu.edu.cn/infoplus/form/8670489/render")
    # driver.get("https://ehall.yzu.edu.cn/infoplus/form/XNYQSB/start")

    # request brower information
    title = driver.title

    if title == "统一身份认证平台":
        # need verify identity
        verify_identity(driver)
        print("Verify identity.")
    elif title == "":
        # have verified identity
        # start_process(driver)
        # print("Fill in the health infomation.")
        # fill_health_info(driver)
        # driver.quit()
        return

    # wait page to load
    time.sleep(5)

    # start process
    if driver.title != "填报健康信息 Fill in health information - 学生健康状况申报":
        start_process(driver)

    # start fill information
    fill_health_info(driver, True)

    # end the session
    driver.quit()

if __name__ == "__main__":
    main()