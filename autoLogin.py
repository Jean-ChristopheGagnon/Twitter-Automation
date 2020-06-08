from selenium import webdriver
import time

def autoLogin(email, password):
    driver = webdriver.Firefox()

    while True:
        try:
            driver.get('https://twitter.com/login')

            usernameField = driver.find_element_by_name("session[username_or_email]")
            passwordField = driver.find_element_by_name("session[password]")

            usernameField.send_keys(email)
            passwordField.send_keys(password)

            driver.find_element_by_class_name("css-18t94o4").click()

            return driver
            break
        except Exception as e:
            print(e)

if __name__ == '__main__':
    autoLogin()
