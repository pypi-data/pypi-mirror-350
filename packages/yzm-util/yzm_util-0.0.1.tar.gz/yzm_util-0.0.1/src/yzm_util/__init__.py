#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import random
import re
import time
import uuid

from yzm_log import Logger

from selenium.webdriver import Firefox
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
# noinspection PyPep8Naming
from selenium.webdriver.support import expected_conditions as EC

from yzm_util.snowflake import IdWorker

'''
 * @Author       : Zheng-Min Yu
 * @Description  : Util class
'''

SPECIAL_SYMBOLS: str = "[ |)>=,%;&#:'<(/\\\\+-]+"


class Util:
    """
    初始化文件
    """

    def __init__(self, log_file: str = "util", is_verbose: bool = False, is_form_log_file: bool = False):
        """
        Initialization creation information, public information
        :param log_file: Path to form a log file
        :param is_verbose: Is log information displayed
        :param is_form_log_file: Is a log file formed
        """
        self.log = Logger(name="util", log_path=log_file, is_form_file=is_form_log_file)
        self.is_verbose = is_verbose

    @staticmethod
    def generate_unique_id() -> str:
        """
        Generate unique ID
        """
        uuid_: str = str(uuid.uuid1())
        uuid__: str = re.sub("-", "", uuid_)
        id_: int = round(random.Random().random() * 100 % 31)
        unique: str = uuid__ + IdWorker().generator(str(id_))
        # The normal length should not exceed 62 to prevent accidents. The database storage length is pow(2, 6)
        return unique[1:62]

    def circle_run(self, title_, callback, refresh, i=0):
        """
        The callback function is mainly accessed by the user selenium to retrieve relevant information and retrieve it again
        :param title_: It is the parameter information of the callback function
        :param callback: The first function of the callback, the main execution function
        :param refresh: The second callback function performs a certain refresh loop when the first callback function encounters an error
        :param i: The number of loops, which is the number of times the callback function executes errors
        :return: Related Information
        """
        try:
            return callback(title_)
        except Exception as e:
            i += 1
            self.log.warn(f"Failed to retrieve element, retrieve again: {e}")
            print(i)
            if i % 5 == 0:
                refresh()
            elif i % 10 == 0:
                refresh(True)
            return self.circle_run(title_, callback, refresh, i)

    def exec_command(self, command: str) -> list:
        """
        Execute command
        :param command: command code
        :return: Result array
        """
        if self.is_verbose:
            self.log.info(f">>>>>>>>> Start executing {command} command >>>>>>>>>")

        info: str = os.popen(command).read()
        info_split: list = info.split("\n")
        info_list: list = []
        i: int = 0
        while True:
            if info_split[i] is None or info_split[i] == "":
                break
            info_list.append(info_split[i])
            i += 1

        if self.is_verbose:
            self.log.info(f">>>>>>>>> End executing {command} command >>>>>>>>>")

        return info_list

    @staticmethod
    def format_str_abbr(str_name: str):
        str_split = re.split(SPECIAL_SYMBOLS, str_name)
        str_sample = ""
        if len(str_split) > 1:
            for t_s in str_split:
                if t_s is not None and t_s != "":
                    str_sample += t_s[0].capitalize()
        else:
            str_sample = str_name
        return str_sample

    @staticmethod
    def get_number(str_: str) -> int:
        """
        Retrieve quantity from the flushing string
        :param str_:
        :return:
        """
        re_compile = re.compile("[0-9]+")
        page_number = re.findall(re_compile, str_)[0]
        return int(page_number)

    @staticmethod
    def remove_r_n(str_: str, repl: str = " | ") -> str:
        """
        remove \r \n
        :param str_:
        :param repl:
        :return:
        """
        return re.sub("[\r\n]+", repl, str_)

    @staticmethod
    def single_line(info_list: list):
        """
        Generate information for adding rows
        :param info_list:
        :return:
        """
        line_one: str = ''
        for col in info_list:
            line_one += f"{str(col)}\t"
        return f"{line_one.strip()}\n"


class FirefoxSelenium:

    def __init__(
        self,
        driver=None,
        wait=None,
        timeout=10,
        is_show: bool = False,
        is_refresh: bool = False,
        log_file: str = "util",
        is_form_log_file: bool = False
    ):
        """
        Selenium Util
        :param driver: driver
        :param wait: selenium wait
        :param timeout: Waiting seconds
        :param is_show: Is headless mode activated
        :param is_refresh: Whether to refresh the page
        """
        self.log = Logger(name="util", log_path=log_file, is_form_file=is_form_log_file)
        self.is_show = is_show
        self.is_refresh = is_refresh
        self.driver = driver if driver else self.init_driver()
        self.wait = wait if wait else WebDriverWait(self.driver, timeout)

    def init_driver(self):
        """
        Browser engine initialization
        :return: Browser driver
        """
        options = FirefoxOptions()
        # Set not to load
        options.page_load_strategy = 'normal'
        # Is it set to headless mode
        if self.is_show:
            # Set Firefox to headless interface free mode
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
        # Instantiating browser objects
        return Firefox(options=options)

    def refresh_handle(self):
        """
        Window processing, handling of selenium redirect URLs
        :return: None
        """
        time.sleep(1)
        # Get the page before jumping
        original_window = self.driver.current_window_handle
        # Get all windows
        handles = self.driver.window_handles
        # switch windows
        for handle in handles:
            if handle != original_window:
                # Close the previous window
                self.driver.close()
                self.driver.switch_to.window(handle)
        # Refreshing and sleeping are to prevent incomplete page code obtained
        time.sleep(1)
        if self.is_refresh:
            self.driver.refresh()

    def is_element_exist(self, xpath):
        """
        Determine whether a certain label exists
        :param xpath: Parsed path
        :return: Is there true: Yes
        """
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            return True
        except Exception as e:
            self.log.debug(f"Label does not exist: {e.args}")
            return False
