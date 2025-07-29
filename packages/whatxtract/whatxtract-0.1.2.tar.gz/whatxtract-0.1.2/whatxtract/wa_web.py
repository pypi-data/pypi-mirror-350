#!/usr/bin/env python3
"""WhatsAppWeb module for WhatsAppWeb."""

import os
import sys
import copy
import json
import time
import random
import shutil
import logging
import argparse
import subprocess
from typing import Any
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

try:
    import undetected_chromedriver as uc
    from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
except ImportError:
    DEPS_IMPORT_FAILED = True
    uc = By = EC = WebDriverWait = TimeoutException = WebDriverException = NoSuchElementException = None
else:
    DEPS_IMPORT_FAILED = False

from whatxtract import utils, constants
from whatxtract.utils import (
    DotDict,
    DummyError,
    timed,
    chunk_list,
    get_digits,
    append_to_file,
    load_config_file,
    ensure_output_dir,
    write_dicts_to_csv,
    generate_vcf_batches,
    read_numbers_from_txt,
    timestamped_output_path,
    extract_contacts_from_json_db,
    extract_chat_list_from_json_db,
)
from whatxtract.constants import (
    APP__DIV,
    OUTPUT_DIR,
    PROFILE_DIR,
    DEFAULT_WAIT,
    WAMS_DB_PATH,
    CHAT_LIST__DIV,
    LOADING__TEXTS,
    BUTTON_ROLE__DIV,
    CHAT_LIST_PARENT,
    NEW_CHAT__BUTTON,
    CONTACT_ITEM__DIV,
    MAIN_NAV_BAR__DIV,
    CONTACT_INFO__SPAN,
    CONTACT_AVATAR__IMG,
    INVALID_NUMBER__DIV,
    INITIAL_STARTUP__DIV,
    CONTACT_AVATAR__DEFAULT,
    CONTACTS_CONTAINER__DIV,
    INDEXEDDB_EXPORT_SCRIPT,
    MAIN_SEARCH_BAR__SEARCH_BOX,
    MAIN_SEARCH_BAR__SEARCH_ICON,
    CONTACTS_CONTAINER_PARENT__DIV,
)
from whatxtract.logging_setup import logger


class WhatsAppBot:
    """
    A wrapper class to configure and initialize an undetected Chrome WebDriver
    for WhatsApp automation. Supports user profile, proxy, headless mode, and
    additional runtime arguments.
    """

    # 1. Dunder methods (constructor and context managers)
    def __init__(self, args, headless: bool = False, _id: int | str = 1):
        """
        Initializes the WhatsAppBot with specified options.

        Args:
            args (Namespace | None): Parsed argparse arguments.
                proxy (str | None): Proxy server address (e.g., 'http://proxy:port').
            headless (bool): Whether to run the browser in headless mode.
            _id (int): Optional identifier (e.g., thread number).
        """
        if isinstance(args, dict):
            args = DotDict(args)

        self.args = args
        self.proxy = args.proxy
        self.headless = headless
        self.profile_dir = args.profile_dir
        self.driver: uc.Chrome | None = None
        self.base_url = 'https://web.whatsapp.com'
        self.class_name = self.__class__.__name__
        self.id = self.identifier = f'[W~{_id}]'
        self.id_full = self.full_id = f'<{self.class_name} {self.id}>'
        logger.debug(f'{self.id} Instance initialized.')

    def __enter__(self):
        logger.debug(f'{self} Entering context manager')
        if not self.driver:
            self.init_driver()
        return self  # This allows `as bot` to work in `with WhatsAppBot(...) as bot:`

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.debug(f'{self} Exiting context manager')
        try:
            self.quit()
        except (Exception, WebDriverException) as e:
            logger.error(f'{self} [x] Exception occurred while quitting the driver: {e}')

        if exc_type:
            logger.error(f'{self} [x] Exception: {exc_val}')

        return False  # Return False to propagate exceptions, True to suppress

    def __repr__(self) -> str:
        return self.full_id

    def __str__(self) -> str:
        return self.id

    # 2. Static and class methods (optional)
    @classmethod
    @timed
    def add_account(cls, args, _id: int | str = 1):
        """Add a new WhatsApp account via QR."""
        logger.info('[+] Add new WhatsApp account via QR')
        with cls(args, headless=False, _id=_id) as bot:
            bot.login()

    @classmethod
    @timed
    def run(cls, args, thread_id: int | str = 1):
        """Run the bot."""
        logger.info(f'[W~{thread_id}] Running {cls.__name__}')
        with cls(args, headless=args.headless, _id=thread_id) as bot:
            if bot.login():
                if args.extract:
                    if args.mode in ['web-db', 'all']:
                        size_kb = bot.export_wa_db(db_name=args.db_name, timeout=10, min_size_kb=10, max_attempts=3)
                        if not size_kb:
                            logger.error(f'{bot} [x] Failed to export WhatsApp IndexedDB.')
                    if args.contact_list or args.mode in ['web-db', 'all']:
                        bot.extract_contacts_from_wams_db()
                    if args.chat_list or args.mode in ['web-db', 'all']:
                        bot.extract_chat_list_from_wams_db()
                    if args.contact_list or args.mode in ['web-scrape', 'all']:
                        bot.scrape_contact_list()
                    if args.chat_list or args.mode in ['web-scrape', 'all']:
                        bot.scrape_chat_list_contacts()
                if args.check:
                    bot.check_numbers(args.numbers, base_delay=args.delay)
            else:
                logger.error(f'{bot} Failed to login.')

    # 3. Initialization helpers
    @timed
    def init_driver(self):
        """
        Sets up and launches the Chrome WebDriver instance with the specified options.

        Returns:
            WebDriver: The configured undetected_chromedriver instance.
        """
        options = uc.ChromeOptions()
        options.add_argument(f'--user-data-dir={self.profile_dir}')
        options.add_argument('--no-sandbox')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--disable-site-isolation-trials')
        options.add_argument('--disable-features=IntentHandling')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option(
            'prefs',
            {
                'profile.default_content_setting_values.automatic_downloads': 1,
                'profile.default_content_setting_values.popups': 0,
            },
        )

        if self.proxy:
            options.add_argument(f'--proxy-server={self.proxy}')
        if self.headless:
            options.add_argument('--headless=new')
            options.add_argument('--window-size=1200,700')

        Path(self.profile_dir).mkdir(parents=True, exist_ok=True)
        self.driver = uc.Chrome(options=options, headless=self.headless)

        if self.headless:
            self.driver.set_window_size(1200, 800)
            self.driver.maximize_window()

        logger.info(f'{self.id} Driver initialized')
        return self.driver

    @timed
    def login(self, timeout: int = 180) -> bool:
        """Login to WhatsApp Web."""
        logger.info(f'{self} Waiting for WhatsApp Web Login...')
        self.driver.get(self.base_url)
        self.driver.implicitly_wait(30)

        logger.debug(f'{self} Checking if QR Login is presented')
        if self._is_login_page(timeout=20):
            logger.debug(f'{self} QR Login detected. Waiting {timeout} seconds for login...')

            if self._wait_for_presence_of_any_element(
                [MAIN_NAV_BAR__DIV, MAIN_SEARCH_BAR__SEARCH_BOX, MAIN_SEARCH_BAR__SEARCH_ICON], timeout=timeout
            ):
                logger.info(f'{self} Successfully logged into WhatsApp Web using QR code.')
                return True
            logger.error(f'{self} Failed to login into WhatsApp.')
            return False
        else:
            if self._wait_for_presence_of_any_element(
                [MAIN_NAV_BAR__DIV, MAIN_SEARCH_BAR__SEARCH_BOX, MAIN_SEARCH_BAR__SEARCH_ICON], timeout=timeout
            ):
                logger.info(f'{self} Successfully logged into WhatsApp Web using QR code.')
                return True
            logger.error(f'{self} Failed to login into WhatsApp.')
            return False

    @timed
    def quit(self):
        """Quits the WebDriver if it has been initialized."""
        logger.info(f'{self} Quitting')

        if self.driver:
            _is_logged_in = self.is_logged_in
            self.driver.quit()
            logger.info(f'{self} Driver closed')
            if _is_logged_in:
                logger.info(f'{self} [✓] Saved profile: {self.profile_dir}')
            if not _is_logged_in:
                logger.info(f'{self} [-] Removing Account Profile from {self.profile_dir}')
                shutil.rmtree(self.profile_dir)

    # 4. Properties
    @timed
    @property
    def is_logged_in(self) -> bool:
        """Check if WhatsApp Web is logged in by looking for the main UI elements."""
        return bool(
            self._wait_for_presence_of_any_element(
                [MAIN_NAV_BAR__DIV, MAIN_SEARCH_BAR__SEARCH_BOX, MAIN_SEARCH_BAR__SEARCH_ICON], timeout=5
            )
        )

    @property
    def session_info(self) -> dict:
        """Return current session metadata."""
        return {
            'id': self.id,
            'logged_in': self.is_logged_in,
            'driver_status': self.driver.service.process.pid if self.driver else None,
        }

    # 5. Public API methods (core functionalities)
    @timed
    def check_number(self, number: str, save_result: bool = True) -> bool | None:
        """Check if a WhatsApp number is active by opening its URL and checking for errors."""
        number = utils.get_digits(number)

        if len(number) == 10:
            number = f'1{number}'

        # url = f'https://wa.me/{number}'
        url = f'https://web.whatsapp.com/send/?phone={number}&text&type=phone_number'
        self.driver.get(url)
        self._wait_for_whatsapp_loading(timeout=20)
        try:
            time.sleep(1)
            self.driver.find_element(*INVALID_NUMBER__DIV)
            logger.info(f'{self} [-] INACTIVE: {number}')
            if save_result:
                filename = 'checked_invalid_numbers'
                filename = timestamped_output_path(str(OUTPUT_DIR), filename, ext='txt', fmt='%Y_%m_%d')
                append_to_file(str(filename), number)
            return False
        except NoSuchElementException:
            logger.info(f'{self} [✓] ACTIVE: {number}')
            if save_result:
                filename = 'checked_valid_numbers'
                filename = timestamped_output_path(str(OUTPUT_DIR), filename, ext='txt', fmt='%Y_%m_%d')
                append_to_file(str(filename), number)
            return True
        except (Exception, DummyError) as e:
            logger.info(f'{self} [!] SKIPPED: {number}')
            if save_result:
                filename = 'check_skipped_numbers'
                filename = timestamped_output_path(str(OUTPUT_DIR), filename, ext='txt', fmt='%Y_%m_%d')
                append_to_file(str(filename), number)
            logger.exception(f'{self} Unexpected error checking {number}: {e}')
            return None

    @timed
    def check_numbers(self, numbers: list, base_delay=5, save_result: bool = True) -> dict:
        """Check a list of WhatsApp numbers for active status."""
        logger.info(f'{self} Starting checking: {len(numbers)} numbers')
        results = {}
        for i, number in enumerate(numbers, 1):
            logger.info(f'{self} [{i}/{len(numbers)}] Checking: {number}')
            _r = self.check_number(number, save_result=save_result)
            results[number] = 'valid' if _r else 'invalid' if _r is False else 'skipped' if _r is None else 'unknown'
            delay = base_delay + random.randint(0, 10)
            logger.info(f'{self} Waiting for {delay} seconds')
            time.sleep(delay)

        logger.info(f'{self} Done checking: {len(numbers)}.')
        return results

    @timed
    def export_wa_db(
        self, db_name: str = 'model-storage', timeout: int = 20, min_size_kb: int = 10, max_attempts: int = 3
    ) -> float:
        """Export WhatsApp IndexedDB to a JSON file."""
        export_size_kb = 0.0
        logger.info(f'{self} Exporting WhatsApp IndexedDB to {WAMS_DB_PATH}')
        for i in range(1, max_attempts + 1):
            logger.info(f'{self} [attempt-{i}] Waiting {timeout} sec to ensure whatsapp db loads properly')
            time.sleep(timeout)

            try:
                self.driver.set_script_timeout(120)
                db_data = self.driver.execute_async_script(INDEXEDDB_EXPORT_SCRIPT, db_name)
            except (Exception, WebDriverException) as e:
                logger.error(f'{self} [attempt-{i}] ERROR in execute_async_script: {e}')
                input(f'{self} [>] Press [ENTER] to continue')
            else:
                WAMS_DB_PATH.write_text(json.dumps(db_data, indent=2), encoding='utf-8', newline='')
                export_size_kb = os.path.getsize(WAMS_DB_PATH) / 1024
                logger.debug(f'{self} [attempt-{i}] [+] Exported: {db_name} [{export_size_kb:.2f}KB] to:{WAMS_DB_PATH}')
                if export_size_kb >= min_size_kb:
                    break

        return export_size_kb

    @timed
    def extract_contacts_from_wams_db(self):
        """Extract contacts from WhatsAppWeb IndexedDB."""
        logger.info(f'{self} Starting contacts extraction from wams db')
        filename = timestamped_output_path(str(OUTPUT_DIR), 'extracted_contacts', '.csv')
        extract_contacts_from_json_db(WAMS_DB_PATH, filename)

    @timed
    def extract_chat_list_from_wams_db(self):
        """Extract Chat list contacts from WhatsAppWeb IndexedDB."""
        logger.info(f'{self} Starting Chat list extraction from wams db')
        filename = timestamped_output_path(str(OUTPUT_DIR), 'extracted_chat_list_contacts', '.csv')
        extract_chat_list_from_json_db(WAMS_DB_PATH, filename)

    @timed
    def scrape_contact_list(self):
        """Extract WhatsApp contacts from the contact list sidebar by screen-scraping the UI."""
        logger.info(f'{self} Starting contact list scraping')
        wait = WebDriverWait(self.driver, DEFAULT_WAIT)

        new_chat_btn = wait.until(EC.element_to_be_clickable(NEW_CHAT__BUTTON))
        new_chat_btn.click()
        logger.debug(f'{self} Opened the contact list sidebar.')

        # contact list
        copyable_area = wait.until(EC.presence_of_element_located(CONTACTS_CONTAINER_PARENT__DIV))
        contacts_container = copyable_area.find_element(*CONTACTS_CONTAINER__DIV)

        seen_items = set()
        contacts_data = []

        prev_item_count = 0
        same_count_retries = 0

        logger.info(f'{self} Scrolling and collecting contacts...')
        while True:
            list_items = contacts_container.find_elements(*CONTACT_ITEM__DIV)
            for item in list_items:
                random_wait = random.randint(2, 9) / 100
                logger.debug(f'{self} randomly waiting: {random_wait:.2f}s')
                time.sleep(random_wait)

                if item.text in seen_items:
                    continue
                seen_items.add(item.text)

                try:
                    contact_div = item.find_element(*BUTTON_ROLE__DIV)
                except (Exception, NoSuchElementException) as e:
                    logger.debug(f'{self} [x] scraping contact finding contact_div {e}')
                    logger.debug(f'{self} {item.text.replace("\n", " || ")}')
                    continue
                else:
                    contact_text = contact_div.text.replace('\n', ' || ')
                    logger.debug(f'{self} [>] {contact_text}')
                    if 'Message yourself' in contact_text:
                        continue

                    data = {}
                    try:
                        contact_div.find_element(*CONTACT_AVATAR__DEFAULT)
                        data['user_avatar'] = ''
                    except (Exception, NoSuchElementException):
                        try:
                            avatar_img = contact_div.find_element(*CONTACT_AVATAR__IMG)
                            data['user_avatar'] = avatar_img.get_attribute('src')
                        except (Exception, NoSuchElementException) as e:
                            logger.debug(f'{self} [x] scraping contact avatar: {e}')
                            data['user_avatar'] = 'unknown'

                    # Name and About
                    try:
                        spans = contact_div.find_elements(*CONTACT_INFO__SPAN)
                        if len(spans) >= 1:
                            data['name'] = spans[0].get_attribute('title')
                        if len(spans) >= 2:
                            data['about'] = spans[1].get_attribute('title')
                    except (Exception, NoSuchElementException) as e:
                        logger.debug(f'{self} [x] scraping contact info {e}')
                        data['name'] = data.get('name', '')
                        data['about'] = data.get('about', '')

                    if data.get('name'):
                        contacts_data.append(data)
                        logger.info(f'{self} [{len(contacts_data):^3}] extracted: {data["name"]}')
                        append_to_file('extracted_valid_contacts.txt', f'{data}')

            current_count = len(seen_items)
            if current_count == prev_item_count:
                same_count_retries += 1
            else:
                same_count_retries = 0

            if same_count_retries >= 3:
                break

            prev_item_count = current_count
            self.driver.execute_script('arguments[0].scrollIntoView();', list_items[-1])
            time.sleep(random.randint(90, 200) / 100)

        filepath = timestamped_output_path(str(OUTPUT_DIR), 'scraped_valid_whatsapp_contacts', '.csv')
        write_dicts_to_csv(contacts_data, ['name', 'about', 'user_avatar'], filepath)

        logger.info(f'{self} Done scraping contact list.')

    @timed
    def scrape_chat_list_contacts(self):
        """Extract WhatsApp chatlist contacts from the chats sidebar by screen-scraping the UI."""
        logger.info(f'{self} Starting Chat list scraping')

        # chat list
        pane_side_div = self.driver.find_element(*CHAT_LIST_PARENT)
        chat_list_div = pane_side_div.find_element(*CHAT_LIST__DIV)

        seen_items = set()
        contacts_data = []

        prev_item_count = 0
        same_count_retries = 0

        logger.info(f'{self} Scrolling and collecting Chat list contacts...')
        while True:
            list_items = chat_list_div.find_elements(*CONTACT_ITEM__DIV)
            for item in list_items:
                contact_text = item.text.replace('\n', ' || ')
                logger.debug(f'{self} [>] {contact_text}')

                if contact_text in seen_items:
                    continue

                seen_items.add(contact_text)

                data = {}
                # Avatar logic
                try:
                    item.find_element(*CONTACT_AVATAR__DEFAULT)
                    data['user_avatar'] = ''
                except (Exception, NoSuchElementException):
                    try:
                        avatar_img = item.find_element(*CONTACT_AVATAR__IMG)
                        data['user_avatar'] = avatar_img.get_attribute('src')
                    except (Exception, NoSuchElementException) as e:
                        logger.debug(f'{self} [x] scraping chat list contact avatar: {e}')
                        data['user_avatar'] = 'unknown'

                # Name and About
                try:
                    spans = item.find_elements(*CONTACT_INFO__SPAN)
                    if len(spans) >= 1:
                        data['name'] = spans[0].get_attribute('title')
                    if len(spans) >= 2:
                        data['about'] = spans[1].get_attribute('title')
                except (Exception, NoSuchElementException) as e:
                    logger.debug(f'{self} [x] scraping chat list contact info {e}')
                    data['name'] = data.get('name', '')
                    data['about'] = data.get('about', '')

                if data.get('name'):
                    contacts_data.append(data)
                    logger.info(f'{self} [{len(contacts_data):^3}] extracted: {data["name"]}')
                    append_to_file('extracted_chat_list_contacts.txt', f'{data}')

            current_count = len(seen_items)
            if current_count == prev_item_count:
                same_count_retries += 1
            else:
                same_count_retries = 0

            if same_count_retries >= 3:
                break  # We scrolled 3 times and saw no new content

            prev_item_count = current_count
            self.driver.execute_script('arguments[0].scrollIntoView();', list_items[-1])
            time.sleep(random.randint(150, 250) / 100)

        filepath = timestamped_output_path(str(OUTPUT_DIR), 'scraped_chat_list_contacts', '.csv')
        write_dicts_to_csv(contacts_data, ['name', 'about', 'user_avatar'], filepath)

        logger.info(f'{self} Done scraping Chat list contacts.')

    # 6. Private/helper methods
    @timed
    def _wait_for_presence_of_any_element(self, selectors: list[tuple[str, str]], timeout: int = DEFAULT_WAIT) -> Any:
        """
        Waits for the presence of any web element matching the given selector(s) within the specified timeout.
        Supports multiple (By, value) tuples. Returns the first found element or None if nothing matches.
        """
        # Defensive check: ensure all selectors are valid (By, value) tuples
        if not selectors or not all(isinstance(s, tuple) and len(s) == 2 for s in selectors):
            logger.warning(f'Invalid or empty selectors passed: {selectors}')
            return None

        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.any_of(*[EC.presence_of_element_located(selector) for selector in selectors])
            )
        except (TimeoutException, NoSuchElementException, WebDriverException):
            return None
        except (Exception, DummyError) as e:
            logger.debug(f'Unexpected exception occurred while waiting for element: {e}')
            return None
        else:
            return element

    @timed
    def _wait_for_visibility_of_any_element(self, selectors: list[tuple[str, str]], timeout: int = DEFAULT_WAIT) -> Any:
        """
        Waits for the visibility of any web element matching the given selector(s) within the specified timeout.
        Supports multiple (By, value) tuples. Returns the first found element or None if nothing matches.
        """
        # Defensive check: ensure all selectors are valid (By, value) tuples
        if not selectors or not all(isinstance(s, tuple) and len(s) == 2 for s in selectors):
            logger.warning(f'Invalid or empty selectors passed: {selectors}')
            return None

        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.any_of(*[EC.visibility_of_element_located(selector) for selector in selectors])
            )
        except (TimeoutException, NoSuchElementException):
            return None
        except (Exception, WebDriverException) as e:
            logger.debug(f'Unexpected exception while waiting for element visibility: {e}')
            return None
        else:
            return element

    @timed
    def _wait_for_startup_div_to_disappear(self, timeout=60, poll_frequency: float = 0.5) -> bool:
        """
        Waits for the <div id="wa_web_initial_startup"> to disappear from the DOM.
        If it is already not present, returns immediately.

        :param timeout: Maximum number of seconds to wait
        :param poll_frequency: Frequency of polling, in seconds. Defaults to 0.5 seconds.
        :return: True if the div is absent or disappears in time, False otherwise
        """
        try:
            try:
                self.driver.find_element(*APP__DIV)
            except (Exception, NoSuchElementException):
                # Assume loading if #app not found
                time.sleep(5)
            try:
                self.driver.find_element(*INITIAL_STARTUP__DIV)
            except NoSuchElementException:
                logger.debug(f'{self} Startup div not present. Proceeding immediately.')
                return True
            else:
                logger.debug(f'{self} Startup div is present. Waiting for it to disappear...')

                wait = WebDriverWait(self.driver, timeout, poll_frequency=poll_frequency)
                wait.until_not(EC.presence_of_element_located(INITIAL_STARTUP__DIV))
                logger.debug(f'{self} Startup div disappeared.')
                return True
        except TimeoutException:
            logger.debug(f'{self} Timeout waiting for startup div to disappear.')
            return False

    @timed
    def _wait_for_whatsapp_loading(self, timeout=60, poll_frequency: float = 0.5) -> str:
        """Waits for WhatsApp Web's post-login loading process to complete."""
        logger.info(f'{self} Waiting for WhatsApp Loading to finish...')
        wait = WebDriverWait(self.driver, timeout, poll_frequency=poll_frequency)

        def still_loading(_driver):
            try:
                app_div = _driver.find_element(*APP__DIV)
                app_div_text = app_div.text
                # logger.debug(f'{self} {len(app_div.text)} {app_div_text}')
                _loading = any(text in app_div_text for text in LOADING__TEXTS)
            except (Exception, NoSuchElementException):
                _loading = True  # Assume loading if #app not found

            return _loading

        try:
            wait.until_not(still_loading)
            logger.info(f'[!] {self} WhatsApp finished loading.')
            return self.driver.find_element(*APP__DIV).text
        except (Exception, TimeoutException):
            logger.warning(f'[~] {self} WhatsApp did not finish loading in time.')
            return ''

    @timed
    def _is_login_page(self, timeout: int = 20) -> bool:
        """Check if WhatsApp Web is in a login page by looking for the login elements."""
        app_div_text = self._wait_for_whatsapp_loading(timeout=timeout)
        app_div_text = app_div_text.lower()
        login_page_texts = ['Log into WhatsApp Web', 'scan the QR code', 'Log in with phone number']
        return any(s.lower() in app_div_text for s in login_page_texts)


def ensure_deps() -> None:
    """
    Ensures the required dependencies are installed and up to date. The function checks
    if a marker file exists and whether a certain time period has elapsed since its
    last modification. If the specified time period has passed, the function updates
    pip and setuptools. Additionally, the function ensures the "undetected_chromedriver"
    and "selenium" packages are installed, installing them if necessary.

    Raises:
        subprocess.CalledProcessError: If any subprocess call to pip for
        installing/upgrading a package fails.
    """
    marker_file = Path('.last_dep_check')
    now = time.time()
    if not marker_file.exists() or now - marker_file.stat().st_mtime > 86400:
        logger.debug('[ * ] Checking and upgrading pip and setuptools...')

        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], stdout=subprocess.DEVNULL)
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', '--upgrade', 'setuptools'], stdout=subprocess.DEVNULL
        )
        # Update marker file timestamp
        marker_file.touch()
    else:
        logger.debug('[ * ] Dependencies were recently checked — skipping upgrade.')

    try:
        import undetected_chromedriver  # noqa: F401
    except ImportError:
        logger.info('[ > ] Installing undetected_chromedriver...')
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'undetected-chromedriver'])

    try:
        import selenium  # noqa: F401
    except ImportError:
        logger.info('[ > ] Installing selenium...')
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'selenium'])

    try:
        from faker import Faker  # noqa: F401
    except ImportError:
        logger.info('[ > ] Installing faker...')
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'faker'])


# noinspection PyUnresolvedReferences
def import_deps() -> None:
    """Imports the required dependencies."""
    global uc, By, WebDriverWait, EC, TimeoutException, WebDriverException, NoSuchElementException
    import undetected_chromedriver as uc
    from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Extract and verify WhatsApp contact numbers via WhatsApp Web')
    # fmt: off
    parser.add_argument(
        '--action', '-a',
        default='extract',
        choices=[
            'a', 'add', 'add-account',
            'e', 'ex', 'extract',
            'c', 'chk', 'check',
            'v', 'vcf', 'vcf-batch', 'generate-vcf', 'generate-vcf-batch',
        ],
        help="""Action: add-account/extract/check/vcf
        add-account:    Add new WhatsApp account(s) via QR login
        extract:        Extract WhatsApp contact numbers from WhatsApp Web
        check:          Check if numbers from input-file are valid WhatsApp users
        vcf:            generate vcf files of specified batch-size""",
    )
    parser.add_argument(
        '--mode', '-m',
        default='web-db',
        choices=['web-db', 'web-scrape', 'emulator', 'all'],
        help="""Extraction execution Mode: web-db/web-scrape/emulator
        web-db:         Extract WhatsApp contact numbers from WhatsApp Web IndexedDB
        web-scrape:     Extract WhatsApp contact numbers from WhatsApp Web by screen scraping
        emulator:       Extract WhatsApp contact numbers using an android emulator
        all:            Extract all data using both web-db and web-scrape method""",
    )
    parser.add_argument(
        '--input-file', '--input', '-i', help='Input file with phone numbers (one per line)'
    )
    parser.add_argument(
        '--batch-size', '--batch', '-b', type=int, default=5000, help='Number of vcf_contacts per batch'
    )
    parser.add_argument(
        '--output-dir', '--output', '-o', default=str(OUTPUT_DIR), help='Directory to save output files'
    )
    parser.add_argument(
        '--profile-dir', '--profile', '-p', default=str(PROFILE_DIR), help='Directory to save WhatsApp Web sessions'
    )
    parser.add_argument(
        '--delay', '-d', type=int, default=10, help='Base delay between checks (in seconds)'
    )
    parser.add_argument(
        '--proxies', '--proxy', nargs='*', help='Optional list of proxies (one per account)'
    )
    parser.add_argument(
        '--add-account', action='store_true', default=False, help='Add new WhatsApp account(s) via QR login'
    )
    parser.add_argument(
        '--check', action='store_true', help='Check if numbers from input-file are valid WhatsApp users'
    )
    parser.add_argument(
        '--extract', action='store_true', default=False, help='Extract valid WhatsApp contact numbers from WhatsApp Web'
    )
    parser.add_argument(
        '--generate-vcf', '--generate-vcf-batch',
        action='store_true', default=False,  help='Generate vcf files of specified batch-size',
    )
    parser.add_argument(
        '--contact-list', '--contacts', action='store_true', default=True, help='Process chat list too.'
    )
    parser.add_argument(
        '--chat-list', '--chatlist', '--chat', action='store_true', default=False, help='Process chat list too.'
    )
    parser.add_argument(
        '--db-name', '--wadb-name', '--wadb', '--db', type=str, default='model-storage', help='Process chat list too.'
    )
    parser.add_argument(
        '--headless', action='store_true', default=False, help='Run browser in headless mode'
    )
    parser.add_argument(
        '--verbose', '-v', action='store_true', default=False, help='Run in verbose mode (LogLevel=DBUG)'
    )
    # fmt: on
    args = parser.parse_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    # load fallback config if exists
    config = load_config_file()

    def get_config_or_prompt(key, prompt_text):
        return getattr(args, key) or config.get(key) or input(prompt_text).strip()

    args.profile_dir = args.profile_dir or get_config_or_prompt('profile_dir', 'Enter path to save WhatsApp sessions: ')
    args.output_dir = args.output_dir or get_config_or_prompt('output_dir', 'Enter path to output directory: ')
    args.batch_size = args.batch_size or config.get('batch_size', 5000)
    args.delay = args.delay or config.get('delay', 10)
    args.proxies = args.proxies or config.get('proxies', [])

    # update default values and paths in constant with the user-defined values
    ensure_output_dir(args.output_dir)
    ensure_output_dir(args.profile_dir)
    constants.OUTPUT_DIR = Path(args.output_dir)
    constants.WAMS_DB_PATH = constants.OUTPUT_DIR / 'wams_db.json'
    constants.PROFILE_DIR = Path(args.profile_dir)
    constants.VCF_BATCH_SIZE = args.batch_size

    if args.action in ['a', 'add', 'add-account']:
        args.add_account = True
    elif args.action in ['c', 'chk', 'check']:
        args.check = True
    elif args.action in ['e', 'ex', 'extract']:
        args.extract = True
    elif args.action in ['v', 'vcf', 'vcf-batch', 'generate-vcf', 'generate-vcf-batch']:
        args.generate_vcf = True

    if args.action in ['c', 'chk', 'check', 'v', 'vcf', 'vcf-batch', 'generate-vcf', 'generate-vcf-batch']:
        args.input_file = get_config_or_prompt(
            'input_file', 'Enter Input file path with phone numbers (one per line): '
        )
        if not args.input_file:
            logger.error('Input file is required for this action.')
            sys.exit(1)
        if not Path(args.input_file).exists():
            logger.error('Input file does not exist.')
            sys.exit(1)

    if args.action in ['a', 'add', 'add-account', 'c', 'chk', 'check', 'e', 'ex', 'extract']:

        def get_next_account_dir(base_dir=PROFILE_DIR, _i: int = 1) -> Path:
            while (base_dir / f'account{_i}').exists():
                _i += 1
            return base_dir / f'account{_i}'

        existing_profiles = sorted(p.name for p in PROFILE_DIR.iterdir() if p.is_dir() and p.name.startswith('account'))
        if args.add_account or not existing_profiles:
            if not existing_profiles:
                logger.warning('No WhatsApp accounts found. Starting one now...')

            while True:
                new_profile = get_next_account_dir()
                args.profile_dir = str(new_profile)
                args.account = str(new_profile)
                args.proxy = args.proxies[0] if args.proxies else None
                WhatsAppBot.add_account(args, _id=get_digits(str(new_profile)))

                choice = input('[ > ] Add another account? (y/n): ').strip().lower()
                if choice != 'y':
                    break

        existing_profiles = sorted(p.name for p in PROFILE_DIR.iterdir() if p.is_dir() and p.name.startswith('account'))
        args.accounts = [str(PROFILE_DIR / name) for name in existing_profiles]

    return args


def main():
    """Main function to handle the command line arguments and launch the appropriate action."""
    ensure_deps()
    import_deps()
    args = parse_args()

    if args.mode == 'emulator':
        logger.error('Emulator mode is not supported yet.')
        return

    if args.generate_vcf:
        constants.VCF_DIR = constants.OUTPUT_DIR / 'vcf_contacts'
        constants.VCF_DIR.mkdir(parents=True, exist_ok=True)
        generate_vcf_batches(args.input_file, args.batch_size)

    if args.extract or args.check:
        num_threads = len(args.accounts)
        proxy_list = args.proxies or [None] * num_threads
        if args.check:
            numbers = read_numbers_from_txt(args.input_file)
            number_chunks = chunk_list(numbers, num_threads)
            logger.info(f'[ + ] Checking {len(numbers)} numbers for WhatsApp users...')
        else:
            number_chunks = [[]] * num_threads

        logger.info(f'[ > ] Launching {num_threads} threads.')
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            for i, (account, chunk) in enumerate(zip(args.accounts, number_chunks, strict=False)):
                proxy = proxy_list[i] if i < len(proxy_list) else None
                args_copy = copy.deepcopy(args)
                args_copy.proxy = proxy
                args_copy.numbers = chunk
                args_copy.proxies = [proxy]
                args_copy.accounts = [account]
                args_copy.profile_dir = account
                executor.submit(WhatsAppBot.run, args_copy, i + 1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('\nInterrupted by user (Ctrl+C). Exiting gracefully.')
        sys.exit(0)
