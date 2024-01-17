from selenium.webdriver.common.by import By
from pylib.web_driver import WebDriver


class ChatroomPageLocator:
    chatroom_pic = (By.XPATH, "//div[@class='chat-empty -start']/img[@class='chat-empty__img']")
    fake_chatroom_pic = (By.XPATH, "//div[@class='fake']")


class ChatroomPage(WebDriver):
    def __init__(self, driver):
        super().__init__(driver)
