#! python3
# Usage: python uploader.py username password slackname folder
# E.g. python uploader.py Kevin haha123 example "C:\Users\Kevin\Example"

from selenium import webdriver
import time
import sys
import pathlib

# Get the needed input from user
driver = webdriver.Firefox()
username = sys.argv[1]
password = sys.argv[2]
slack = sys.argv[3]
upload = sys.argv[4]

# Set some variables and grab the paths to the files
slack_url = "https://" + slack + ".slack.com/"
customize_url = "customize/emoji"
files = [p for p in pathlib.Path(upload).iterdir() if p.is_file()]

# Navigate to the slack page and log in
driver.get(slack_url)
email_input = driver.find_element_by_id("email")
password_input = driver.find_element_by_id("password")
login_button = driver.find_element_by_id("signin_btn")

email_input.send_keys(username)
password_input.send_keys(password)
time.sleep(1)
login_button.click()

# Go to the  customize page
driver.get("https://slack.com/" + customize_url)

# Wait till the page is properly loaded
while 1:
    try:
        emoji_button = driver.find_element_by_class_name("c-button--primary")
        break
    except:
        pass

# Wait for the emoji's to load in
while 1:
    try:
        driver.find_elements_by_class_name("p-customize_emoji_list__row_icons")
        time.sleep(2)
        break
    except:
        pass

# Upload all the emoji's that are not uploaded yet
for file in files:
    name = pathlib.PurePath(file.name).stem

    # See if this icon has already been uploaded
    try:
        uploaded = driver.find_element_by_xpath("//*[text()[contains(.,'" + name + "')]]")
    except:
        emoji_button.click()
        input_file = driver.find_element_by_id("emojiimg")
        input_file.send_keys(str(file))
        input_name = driver.find_element_by_id("emojiname")
        input_name.send_keys(name)
        save_button = driver.find_element_by_xpath("//*[text()[contains(.,'Save')]]")
        save_button.click()
        time.sleep(3)
        pass
