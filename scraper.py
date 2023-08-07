from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from urllib.parse import urljoin
import pyperclip
import openpyxl

print('- Finish importing packages')

driver = webdriver.Chrome()
sleep(1)
url = 'https://www.linkedin.com/login'
driver.get(url)
print('- Finish initializing a driver')
sleep(1)

# Task 1.2: Import username and password
importMember = open('importMember.txt')
line = importMember.readlines()
# Strip removes leading/trailing spaces and newline characters
username = line[0].strip()
password = line[1].strip()
group_url = line[2].strip()  # New entry for group_url
your_name = line[3].strip()  # New entry for your_name
page = int(line[4].strip())   # Start page
end_page = int(line[5].strip())  # End page
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

#  Create page url
page_url = urljoin(group_url, f"?page={page}")

# Visit your group page
driver.get(page_url)
sleep(5)
print('Go to your group page')


# Function to check if "Next" button is still available
def has_next_page():
    try:
        driver.find_element(
            By.XPATH, '//button[@class="artdeco-pagination__button artdeco-pagination__button--next artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view"]')
        return True
    except:
        return False

# Function to go to next page
def go_to_next_page():
    try:
        next_button = driver.find_element(
            By.XPATH, '//button[@class="artdeco-pagination__button artdeco-pagination__button--next artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view"]')
        next_button.click()
        sleep(5)
    except:
        print('No next page')

# List LinkedIn account who didn't want message
didntsent = ["Gokula Kandaswamy",
             "JONATHAN ARNOLD~ACA 🇱🇰, FCCA 🇬🇧, CPA 🇦🇺🇨🇦, (Triple Chartered Accountant and KPMG SoQM Manager) BSc. (Hons)🎓l Award-winning Auditor🏆l Musician🎸",
             "Tal Cohen",
             your_name,
             "emmanuel mawejje",
             "Manisha Dayma"
             ]
# Create array who can not send
cannotsends = []

# The loop to message
while page <= end_page:
    member_names = []
    for abcsd in driver.find_elements(By.CSS_SELECTOR, ".artdeco-entity-lockup__title.ember-view"):
        print(abcsd.text)
        member_names.append(abcsd.text)
    print("Locate the list of group members")
    for member in member_names:
        # Find the button to turn off the message who is replying
        buttons = driver.find_elements(
             By.XPATH, '//button[@class="msg-overlay-bubble-header__control artdeco-button artdeco-button--circle artdeco-button--1 artdeco-button--primary ember-view"]')
        # Iterate over each element and do a click
        for button in buttons:
            button.click()
        # Skip sending a message to your own account
        if member in didntsent:
            continue
        try:
            # Find the message button on the group page
            message_box_click = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, f'//*[@aria-label="Message {member}"]'))
            )

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
            message = open('content.txt')
            # Remove specified prefixes from the member name
            prefixes = ["CPE", "Eng.", "Md.", "Md", "CMA",
                        "MSC CPA", "CPA", "FCCA", "CA", "CPA, FMVA", "CS", "Dr."]
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
            sleep(1)

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
                sleep(1)
            else:
                print("Error")

    if not has_next_page():
        break
    go_to_next_page()
    page += 1
# Ends when the message has been sent to all members of the group
print("Sent to all")

# Print a list of people who can't message them yet
print("List of who cannot send\n")
for cantsend in cannotsends:
    print(cantsend, "\n")
    file_path = "cannotsend.txt"

# Ghi danh sách vào tệp
with open(file_path, "w", encoding='utf-8') as file:
    file.write("List of who cannot send:\n")
    for cantsend in cannotsends:
        file.write(cantsend + "\n")
print("List of who cannot send has been saved to", file_path)
