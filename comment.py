from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pyperclip
import pyautogui
import time

def clickComment(): 
    driver.find_element(By.NAME, 'mainFrame').send_keys(Keys.SPACE)
    time.sleep(2)
    driver.switch_to.frame("mainFrame")
    try:
        driver.find_element(By.XPATH, '//*[@id="btn_comment_2"]').click()
    except:
        driver.find_element(By.CLASS_NAME, 'u_cbox_inbox').click()
    time.sleep(2)

def Login(myId, myPw):
    driver.find_element(By.CLASS_NAME, 'u_cbox_inbox').click()
    main_window = driver.current_window_handle
    for handle in driver.window_handles:
        if handle != main_window:
            driver.switch_to.window(handle)
            break

    idBox = driver.find_element(By.ID, "id")
    idBox.click()
    pyperclip.copy(myId)
    pyautogui.hotkey("command")
    pyautogui.hotkey("command", "v")
    time.sleep(1)  
    
    pwBox = driver.find_element(By.ID, "pw")
    pwBox.click()
    pyperclip.copy(myPw)
    pyautogui.hotkey("command", "v")
    time.sleep(1)

    loginBtn = driver.find_element(By.ID, "log.login")
    loginBtn.click()

    driver.switch_to.window(main_window)
    time.sleep(1)


def makeComment(comment):
    pyperclip.copy(comment)
    pyautogui.hotkey("command", "v")
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, '.u_cbox .u_cbox_btn_upload').click()
    time.sleep(2)

myId = input("Id를 입력하세요")
myPw = input("Pw를 입력하세요")

url = input("블로그 링크를 입력해주세요")
driver = webdriver.Chrome() 
driver.get(url)
time.sleep(3)

comment = "안녕하세요 이웃님, 좋은 게시글 잘 읽고 갑니다! \n 연말 즐겁게 보내시고 새해 복 많이 받으세요~"

clickComment()
Login(myId, myPw)
clickComment()
makeComment(comment)
