import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from HTML.pageHtml import Getpage
import os
import time


class Parser:
    url = "https://www.pencarrie.com/"

    def __init__(self):
        self.l = input("Введите Логин: ")
        self.p = input("Введите Пароль: ")
        self.page = input("Введите страницы через запятую: ")
        self.num = int(input("Введите число ссылок: "))
        self.auth()


    def auth(self, *args):
        # driver = webdriver.Firefox(executable_path='./geckodriver')
        driver = webdriver.Chrome(executable_path='C:\chromedriver.exe')
        driver.set_window_size(900, 900)
        driver.set_window_position(0, 0)
        driver.get(self.url)
        time.sleep(1)
        driver.wait = WebDriverWait(driver, 8)

        login = driver.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "login-btn")))
        login.click()

        time.sleep(3)

        email = driver.wait.until(EC.presence_of_element_located((By.NAME, "email")))
        password = driver.wait.until(EC.presence_of_element_located((By.NAME, "password")))
        email.send_keys(self.l)
        password.send_keys(self.p)

        button = driver.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "login-btn")))
        driver.wait = WebDriverWait(driver, 5)
        button.click()
        time.sleep(5)
        # link = "https://www.pencarrie.com/catalogue?p=11775", "https://www.pencarrie.com/catalogue?p=599m", "https://www.pencarrie.com/catalogue?p=h400"
        listMassiv = []
        listStr = self.page.split(",")
        
        for x in range(0, self.num):
            listMassiv.append(listStr[x])

        for page in listMassiv:
            driver.get(page)
            time.sleep(2)
            requiredHtml = driver.page_source
            requests = Getpage()
            requests.get_data(requiredHtml)
        driver.close


if __name__ == '__main__':
    parser = Parser()
