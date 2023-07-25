# Import libraries and packages for the project
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.service import Service
from time import sleep
import csv
print('- Finish importing packages')

# Task 1: Login to Linkedin

# Task 1.1: Open Chrome and Access Linkedin login site
driver = webdriver.Chrome()
sleep(2)
url = 'https://www.linkedin.com/login'
driver.get(url)
print('- Finish initializing a driver')
sleep(2)

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
sleep(10)


# Đường dẫn đến trang group của bạn
group_url = "https://www.linkedin.com/groups/14285566/manage/membership/members/"
# Truy cập vào trang group của bạn
driver.get(group_url)
sleep(5)
print('Truy cập vào trang group của bạn')
# Định vị phần tử chứa danh sách các thành viên trong nhóm

member_names = []
for abcsd in driver.find_elements(By.CSS_SELECTOR,".artdeco-entity-lockup__title.ember-view"):
    print(abcsd.text)
    member_names.append(abcsd.text)
print("Định vị phần tử chứa danh sách các thành viên trong nhóm")

# Gửi tin nhắn cho từng thành viên
for member in member_names:
    # Định vị phần tử chứa tên của thành viên.
    member_container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.artdeco-entity-lockup__title.ember-view'))
    )
    print(member_container)

    # Lấy tên của thành viên từ phần tử đã định vị.
    member_name = member
    print(member)
    message = open('message.txt')
    # Tạo nội dung tin nhắn với tên thành viên
    customized_message = message.read()
    send_message = "Hi " + member.split()[0] + ",\n" + customized_message
    print(customized_message)
    print(send_message)
    
    # Tìm ô tin nhắn và gửi nội dung tin nhắn
    message_box_click = driver.find_element(
        (By.XPATH, "//*[@aria-label='Message {member}']"))
    message_box_click.click()
    
    # message_box = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located(
    #         (By.CSS_SELECTOR, 'artdeco-button__text'))
    # )
    # message_box.send_keys(customized_message)
    # message_box.send_keys(Keys.RETURN)
    # sleep(2)

# # Đóng trình duyệt
# driver.quit()
# print('Mission Completed!')