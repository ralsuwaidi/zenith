import logging
import time
from os import environ as env

import openai
import telebot
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import markdownify



options = Options()
options.headless = True


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

bot = telebot.TeleBot(env["TELEGRAM_BOT_KEY"])
openai.api_key = env["OPENAI_API_KEY"]


@bot.message_handler(func=lambda message: True)
def get_chatgpt(message):
    driver = webdriver.Firefox(options=options)
    driver.get("https://chat.openai.com")
    driver.find_element(By.XPATH, '//button[text()="Log in"]').click()
    elem = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.ID, "username")) 
    )

    driver.get(driver.current_url)
    username = driver.find_element(By.ID, "username")
    username.send_keys(env["OPENAI_USERNAME"])
    driver.find_element(By.XPATH, '//button[text()="Continue"]').click()
    password = driver.find_element(By.ID, "password")
    password.send_keys(env["OPENAI_PASSWORD"])
    driver.find_element(By.XPATH, '//button[text()="Continue"]').click()

    WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]')) 
    )

    driver.find_element(By.XPATH, '//button[text()="Next"]').click()
    driver.find_element(By.XPATH, '//button[text()="Next"]').click()
    driver.find_element(By.XPATH, '//button[text()="Done"]').click()
    input_prompt = driver.find_element(By.CSS_SELECTOR, "textarea.w-full")
    input_prompt.send_keys(message.text)
    input_prompt.send_keys(Keys.ENTER)

    WebDriverWait(driver, 90).until(
    EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Try again')]")) 
    )
    response=driver.find_element(By.XPATH, "//div[contains(@class, 'markdown prose')]").get_attribute('innerHTML')
    response = markdownify.markdownify(response, heading_style="ATX")
    print(response)

    bot.send_message(message.chat.id,
                     f'{response}',
                     parse_mode="markdown")
    driver.close()

bot.infinity_polling(timeout=120, long_polling_timeout=240)
