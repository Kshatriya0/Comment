from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pyperclip
import pyautogui
import time

def clickComment(): 
    F = driver.find_element(By.NAME, 'mainFrame')
    F.send_keys(Keys.SPACE)
    time.sleep(2)
    driver.switch_to.frame("mainFrame")

    try:
        driver.find_element(By.XPATH, '//*[@id="btn_comment_2"]').click()
    
    except:
        print("Ex")
        driver.switch_to.default_content()
        F.send_keys(Keys.SPACE)
        driver.switch_to.frame("mainFrame")
        driver.find_element(By.XPATH, '//*[@id="btn_comment_2"]').click()
    
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
    pyautogui.hotkey("ctrl")
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)  
    
    pwBox = driver.find_element(By.ID, "pw")
    pwBox.click()
    pyperclip.copy(myPw)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)

    loginBtn = driver.find_element(By.ID, "log.login")
    loginBtn.click()

    driver.switch_to.window(main_window)
    time.sleep(1)


def makeComment(comment):
    driver.find_element(By.CLASS_NAME, 'u_cbox_inbox').click()
    pyperclip.copy(comment)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, '.u_cbox .u_cbox_btn_upload').click()
    time.sleep(1)
    


def findFirstPost():
    driver.switch_to.frame("mainFrame")
    mainPage = driver.find_element(By.XPATH, '//*[@id="blog-menu"]/div/table/tbody/tr/td[1]/ul/li[2]/a')
    driver.execute_script("arguments[0].click();", mainPage)
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="categoryTitle"]').click()
    time.sleep(2)
    firstPost = driver.find_element(By.XPATH, '//*[@id="listTopForm"]/table/tbody/tr[1]/td[1]/div')
    firstPost.click()
    time.sleep(3)
    driver.switch_to.default_content()


myId = input("Id를 입력하세요")
myPw = input("Pw를 입력하세요")
comment = "잘 보고 갑니다~"


url = input("블로그 링크를 입력해주세요")
driver = webdriver.Chrome() 
driver.get(url)
time.sleep(2)

clickComment()
Login(myId, myPw)
F = driver.find_element(By.NAME, 'mainFrame')
F.send_keys(Keys.SPACE)
time.sleep(2)
driver.switch_to.frame("mainFrame")
profile = driver.find_elements(By.CLASS_NAME, "u_cbox_nick")
main_tab = driver.window_handles[0]
time.sleep(1)
for i in range(len(profile)):
    profile[i].click()
    time.sleep(2)
    new_tab = driver.window_handles[1]
    driver.switch_to.window(new_tab)
    findFirstPost()
    if True:
        clickComment()
        makeComment(comment)
    time.sleep(1)
    pyautogui.hotkey("ctrl", "w") #Close tab
    time.sleep(1)
    driver.switch_to.window(main_tab)
    driver.switch_to.frame("mainFrame")

print("Success")