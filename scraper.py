import csv
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import pyperclip

print('- Finish importing packages')

driver = webdriver.Chrome()
sleep(1)
url = 'https://www.linkedin.com/login'
driver.get(url)
print('- Finish initializing a driver')
sleep(1)

# Task 1.2: Import username and password
importMember = open('thien.txt')
line = importMember.readlines()
# username = line[0]
# password = line[1]
# Strip removes leading/trailing spaces and newline characters
username = line[0].strip()
password = line[1].strip()
group_url = line[2].strip()  # New entry for group_url
your_name = line[3].strip()  # New entry for your_name
print('- Finish importing the login')
sleep(2)

# Task 1.2: Key in login
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
sleep(5)

# Đường dẫn đến trang group của bạn
# group_url = "https://www.linkedin.com/groups/14285566/manage/membership/members/"
# Truy cập vào trang group của bạn
driver.get(group_url)
sleep(5)
print('Truy cập vào trang group của bạn')

# Hàm để kiểm tra xem còn nút "Next" hay không


def has_next_page():
    try:
        driver.find_element(
            By.XPATH, '//button[@class="artdeco-pagination__button artdeco-pagination__button--next artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view"]')
        return True
    except:
        return False

# Hàm để chuyển sang trang kế tiếp


def go_to_next_page():
    try:
        next_button = driver.find_element(
            By.XPATH, '//button[@class="artdeco-pagination__button artdeco-pagination__button--next artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view"]')
        next_button.click()
        sleep(5)
    except:
        print('No next page')
# Định vị phần tử chứa danh sách các thành viên trong nhóm


# Get your LinkedIn account's name
didntsent = ["Gokula Kandaswamy",
             "JONATHAN ARNOLD~ACA 🇱🇰, FCCA 🇬🇧, CPA 🇦🇺🇨🇦, (Triple Chartered Accountant and KPMG SoQM Manager) BSc. (Hons)🎓l Award-winning Auditor🏆l Musician🎸",
             "Tal Cohen",
             your_name
             ]
cannotsends = []
# Gửi tin nhắn cho từng thành viên trên tất cả các trang
while True:
    member_names = []
    for abcsd in driver.find_elements(By.CSS_SELECTOR, ".artdeco-entity-lockup__title.ember-view"):
        print(abcsd.text)
        member_names.append(abcsd.text)
    print("Định vị phần tử chứa danh sách các thành viên trong nhóm")
    for member in member_names:
        buttons = driver.find_elements(
            By.XPATH, '//button[@class="msg-overlay-bubble-header__control artdeco-button artdeco-button--circle artdeco-button--1 artdeco-button--primary ember-view"]')
        # Duyệt qua từng phần tử và thực hiện click
        for button in buttons:
            button.click()
        # Skip sending a message to your own account
        if member in didntsent:
            continue
        try:
            # Tìm ô tin nhắn trên trang group
            message_box_click = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, f'//*[@aria-label="Message {member}"]'))
            )

            # Move the mouse cursor to the element and then click
            action = ActionChains(driver)
            action.move_to_element(message_box_click).click().perform()
            print("Click chat cho ", member)
            # Wait for a short duration (adjust this sleep time if needed)
            sleep(1)

            # Find the input field for composing the message
            message_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '.msg-form__contenteditable'))
            )

            # Compose your customized message for the specific member
            message = open('content.txt')
            # Remove specified prefixes from the member name
            prefixes = ["CPE", "Eng.", "Md.", "CMA",
                        
                        "MSC CPA", "CPA", "FCCA", "CA", "CPA, FMVA"]
            for prefix in prefixes:
                if member.startswith(prefix):
                    full_name = member[len(prefix):].strip()
                    break
                else:
                    full_name = member
            with open('content.txt', encoding='utf-8') as message_file:
                customized_message = message_file.read()
                firstname = full_name.split()[0]
            send_message = str("Hi " +
                               firstname.capitalize() + ",\n" + customized_message)
            # Paste the customized message into the input field
            pyperclip.copy(send_message)

            # Click on the message_input field
            message_input.click()

            # Simulate paste action (Ctrl + V) to paste content from clipboard
            action = ActionChains(driver)
            action.key_down(Keys.CONTROL).send_keys(
                'v').key_up(Keys.CONTROL).perform()
            # Wait for a short duration (adjust this sleep time if needed)
            sleep(1)

            # Find the "Send" button and click it
            send_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, ".msg-form__send-button.artdeco-button.artdeco-button--1"))
            )
            send_button.click()

            # Wait for a short duration (adjust this sleep time if needed)
            sleep(2)
            exception_occurred = True
        except Exception as e:
            print(f"Error sending message to {member}: {e}")
            cannotsends.append(member)
            exception_occurred = False
            continue
        finally:
            if exception_occurred:
                close_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, '//button[@class="msg-overlay-bubble-header__control artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--1 artdeco-button--tertiary ember-view"]'))
                )
                close_button.click()
                print("Sent to", member)
                sleep(2)
            else:
                print("Error")

    if not has_next_page():
        break
    go_to_next_page()

# Kết thúc khi đã gửi tin nhắn cho toàn bộ thành viên trong nhóm
print("Sent to all")


# when running this bot please change zoom in your settings = 80%
