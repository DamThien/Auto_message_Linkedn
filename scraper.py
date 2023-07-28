import csv
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
# Hiện tại có thể nhắn tin cho nhiều người nhưng đang gặp một vấn đề đó là vẫn không thể ấn nút x để tắt thành viên đã nhắn tin.
# Import libraries and packages for the project

print('- Finish importing packages')

driver = webdriver.Chrome()
sleep(1)
url = 'https://www.linkedin.com/login'
driver.get(url)
print('- Finish initializing a driver')
sleep(1)

# Task 1.2: Import username and password
credential = open('credentials.txt')
line = credential.readlines()
username = line[0]
password = line[1]
print('- Finish importing the login credentials')
sleep(2)

# Task 1.2: Key in login credentials
email_field = driver.find_element(By.ID, 'username').send_keys(username)
print('- Finish keying in email')
sleep(1)

password_field = driver.find_element(
    By.NAME, 'session_password').send_keys(password)
print('- Finish keying in password')
sleep(1)

# Task 1.2: Click the Login button
signin_field = driver.find_element(
    By.XPATH, '//*[@id="organic-div"]/form/div[3]/button')
signin_field.click()
print('- Finish Task 1: Login to Linkedin')
sleep(15)

# Đường dẫn đến trang group của bạn
group_url = "https://www.linkedin.com/groups/14285566/manage/membership/members/"
# Truy cập vào trang group của bạn
driver.get(group_url)
sleep(5)
print('Truy cập vào trang group của bạn')
# Định vị phần tử chứa danh sách các thành viên trong nhóm

member_names = []
for abcsd in driver.find_elements(By.CSS_SELECTOR, ".artdeco-entity-lockup__title.ember-view"):
    print(abcsd.text)
    member_names.append(abcsd.text)
print("Định vị phần tử chứa danh sách các thành viên trong nhóm")

# Get your LinkedIn account's name
your_name = "Dam Long Thien"

# Gửi tin nhắn cho từng thành viên
for member in member_names:
    # Skip sending a message to your own account
    if member == your_name:
            continue
    try:
        # Tìm ô tin nhắn trên trang group
        message_box_click = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, f"//*[@aria-label='Message {member}']"))
        )
        # Scroll to the message button to bring it into view
        driver.execute_script(
            "arguments[0].scrollIntoView();", message_box_click)

        # Move the mouse cursor to the element and then click
        action = ActionChains(driver)
        action.move_to_element(message_box_click).click().perform()

        # Wait for a short duration (adjust this sleep time if needed)
        sleep(1)

        # Find the input field for composing the message
        message_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '.msg-form__contenteditable'))
        )
        
        # Compose your customized message for the specific member
        message = open('message.txt')
        with open('message.txt', encoding='utf-8') as message_file:
            customized_message = message_file.read()
        send_message = "Hi " + member.split()[0] + ",\n" + customized_message

        # Paste the customized message into the input field
        action = ActionChains(driver)
        action.click(message_input).send_keys(send_message).perform()

        # Wait for a short duration (adjust this sleep time if needed)
        sleep(1)

        # Find the "Send" button and click it
        send_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".msg-form__send-button.artdeco-button.artdeco-button--1"))
        )
        send_button.click()

        # Wait for a short duration (adjust this sleep time if needed)
        sleep(3)

    except Exception as e:
        print(f"Error sending message to {member}: {e}")

    finally:
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[@class="msg-overlay-bubble-header__control artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--1 artdeco-button--tertiary ember-view"]'))
        )
        close_button.click()
        print("Đã gửi tin nhắn cho",member)
        sleep(2)

# Kết thúc khi đã gửi tin nhắn cho toàn bộ thành viên
print("Đã gửi tin nhắn cho toàn bộ thành viên trong nhóm")
