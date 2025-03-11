from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoSuchElementException
import pyperclip
import pyautogui
import time

def isExistElement(element):
    try:
        driver.find_element(By.XPATH, element)
        return True
    except Exception:
        return False

def isLiked():
    try:
        time.sleep(1)
        likeBtn = driver.find_element(By.XPATH, '//*[@id="floating_bottom"]/div/div/div[1]/div/div/a')
        is_like = likeBtn.get_attribute('aria-pressed')   #좋아요 버튼 상태 확인
        if is_like == 'false':
            likeBtn.click()
            try:
                time.sleep(1)
                alert = Alert(driver)   #팝업창으로 메시지 뜰 경우를 대비
                alert.accept()
                return "alert"
            except Exception:
                pass
            time.sleep(1)
            return False
        elif is_like == 'true':
            return True
    except Exception:   #간혹 공감 버튼 자체가 없는 게시글이 존재함
        return None

def findFloater():
    F = driver.find_element(By.NAME, 'mainFrame')
    F.send_keys(Keys.SPACE)
    F.send_keys(Keys.SPACE)
    time.sleep(1)
    driver.switch_to.frame("mainFrame")   

def clickComment(): #댓글창 클릭 
    try:
        toComment = driver.find_element(By.XPATH, '//*[@id="btn_comment_2"]')
        toComment.send_keys(Keys.ENTER)
        time.sleep(1)
    except Exception:
        try:
            findFloater()
            toComment = driver.find_element(By.XPATH, '//*[@id="btn_comment_2"]') 
            toComment.send_keys(Keys.ENTER)
            time.sleep(1)
        except Exception:
            print("댓글창 클릭 실패")
            pass

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
    time.sleep(5)



    driver.switch_to.window(main_window)
    time.sleep(5)

def makeComment(comment):
    driver.find_element(By.CLASS_NAME, 'u_cbox_inbox').click()
    pyperclip.copy(comment)
    pyautogui.hotkey("command", "v")
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, '.u_cbox .u_cbox_btn_upload').click()
    time.sleep(1)

def findFirstPost():
    try:
        driver.switch_to.frame("mainFrame")
    except Exception:
        print("이미 프레임에 있습니다.")
        pass
    try:
        x = driver.find_element(By.XPATH, '//*[@id="categoryTitle"]')
        x.click()
        time.sleep(1)
    except NoSuchElementException:
        try:
            mainPage = driver.find_element(By.XPATH, '//*[@id="blog-menu"]/div/table/tbody/tr/td[1]/ul/li[2]/a')
            driver.execute_script("arguments[0].click();", mainPage)
            time.sleep(2)
            postList = driver.find_element(By.XPATH, '//*[@id="categoryTitle"]')
            postList.click()
            time.sleep(2)
        except NoSuchElementException:
            pass
    
    firstPost = driver.find_element(By.XPATH, '//*[@id="listTopForm"]/table/tbody/tr[1]/td[1]/div')
    try:
        firstPost.click()
    except Exception:
        try:
            driver.execute_script("arguments[0].click();", firstPost)
        except Exception:  
            print("첫번째 게시글 클릭 실패")
            return
    time.sleep(2)
    driver.switch_to.default_content()

myId = input("Id를 입력하세요")
myPw = input("Pw를 입력하세요")
comment = "주말이 가고 벌써 월요일이네요!ㅠ \n 이번 한주도 화이팅합시다~. 😊"

url = input("블로그 링크를 입력해주세요")
driver = webdriver.Chrome() 
driver.get(url)
driver.maximize_window()

time.sleep(2)

findFloater()
try:
    commentCount = driver.find_element(By.ID, "floating_bottom_commentCount")
    commentCount = int(commentCount.text)
    print("총 댓글 수: ", commentCount)
except Exception:
    print("댓글 수를 찾지 못했습니다.")
    pass
clickComment()
Login(myId, myPw)

time.sleep(15)

driver.switch_to.frame("mainFrame")
main_tab = driver.window_handles[0]
pageList = driver.find_elements(By.CLASS_NAME, "u_cbox_page")
page = 0
time.sleep(1)

Count = 0
madeComment = 0
nameList = []
failList = []
profile = driver.find_elements(By.CLASS_NAME, "u_cbox_nick")

for i in range(commentCount):
    if commentCount > 50:
        if (Count%50 == 0) or (Count == 0):
            try:
                driver.switch_to.frame("mainFrame")
            except Exception:
                pass
            pageList[page].send_keys(Keys.ENTER)
            page += 1
            time.sleep(2)
            profile = driver.find_elements(By.CLASS_NAME, "u_cbox_nick")
            print(profile)
            print(len(profile))
            time.sleep(1)
    Count += 1
    crrPro = profile[i]
    try:
        crrPro.click()
    except Exception:
        print("프로필 클릭 실패")
        continue
    proName = crrPro.text
    nameList.append(proName)
    
    time.sleep(2)
    
    new_tab = driver.window_handles[1]
    driver.switch_to.window(new_tab)
    try:
        findFirstPost()
    except Exception:
        print(nameList[i] + "님의 첫번째 게시글 클릭 실패")
        failList.append(proName)
        pyautogui.hotkey("command", "w") #Close tab
        time.sleep(1)
        driver.switch_to.window(main_tab)
        driver.switch_to.frame("mainFrame")
        continue
    findFloater()
    time.sleep(1)
    if isLiked() == False:
        clickComment()
        time.sleep(1)
        try:
            makeComment(comment)
            madeComment += 1
            print(nameList[i] + "님의 게시글에 성공적으로 댓글을 작성했습니다.")
        except Exception:
            failList.append(proName)
            print(nameList[i] + "님의 게시글에 댓글을 작성하지 못했습니다.")
    elif isLiked() == True:
        print(nameList[i] + "님의 게시글은 이미 좋아요를 눌렀습니다.")
    elif isLiked() == "alert":
        print(nameList[i] + "님의 게시글에는 자동으로 댓글을 달 수 없습니다.")
    else: 
        print(nameList[i] + "님의 게시글에는 공감 버튼이 없습니다.")
    time.sleep(1)
    pyautogui.hotkey("command", "w") #Close tab
    time.sleep(1)
    driver.switch_to.window(main_tab)
    driver.switch_to.frame("mainFrame")

print(madeComment, "개의 댓글을 작성했습니다.")
print("댓글 작성 실패한 사람들: ", failList)
driver.quit()