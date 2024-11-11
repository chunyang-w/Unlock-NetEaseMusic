# coding: utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time,os,logging
from retrying import retry

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    target = browser.find_element_by_xpath("//*[starts-with(@id,'x-URS-iframe')]")
    # browser.execute_script('arguments[0].scrollIntoView(true);', target)
    browser.switch_to.frame(target)

    return browser

# 失败后随机 1-3s 后重试，最多 3 次
@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=1)
def extension_login(email,password):
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_argument('--headless')
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Load Chrome driver")
    # browser = webdriver.Chrome(executable_path="chromedriver.exe", options=chrome_options)
    # browser = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)
    browser = webdriver.Chrome(options=chrome_options)
    # 设置全局的隐式等待(直到找到元素),20秒后找不到抛出找不到元素
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # 查找登录按钮
    target = browser.find_element_by_xpath("//a[text()='登录']")
    browser.execute_script('arguments[0].scrollIntoView(true);', target)

    time.sleep(10)
    # 点击"登录"按钮
    logging.info("Click login button")
    browser.find_element_by_xpath("//a[text()='登录']").click()
    # browser.find_element_by_css_selector('a.link.s-fc3').click()

    logging.info("Select login method")
    # browser.find_element_by_css_selector('.u-btn2.other').click()
    browser.find_element_by_xpath("//a[text()='选择其他登录模式']").click()

    # 勾选同意协议
    logging.info("Click agreements")
    browser.find_element_by_id('j-official-terms').click()

    browser.find_element_by_xpath("//a[text()='网易邮箱帐号登录']").click()

    # 进入iframe
    time.sleep(10)
    browser = enter_iframe(browser)

    # 输入账号密码
    logging.info("Enter email and password")
    browser.find_element_by_css_selector("input.j-inputtext[name='email']").send_keys(email)
    browser.find_element_by_name('password').send_keys(password)

    time.sleep(2)

    # 点击登录按钮
    logging.info("Click login button")
    browser.find_element_by_id('dologin').click()

    time.sleep(2)

    browser.refresh() # 刷新页面
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,format='[%(levelname)s] %(asctime)s %(message)s')
    
    try:
        email = os.environ['EMAIL']
        password = os.environ['PASSWORD']
    except:
        logging.error('Fail to read email and password.')
    else:
        extension_login(email,password)