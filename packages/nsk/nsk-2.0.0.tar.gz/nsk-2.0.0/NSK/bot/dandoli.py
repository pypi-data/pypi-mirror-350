import time
from contextlib import suppress
from urllib.parse import urljoin

from selenium import webdriver
from selenium.common.exceptions import (ElementClickInterceptedException,
                                        StaleElementReferenceException,
                                        TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from NSK.bot.base import IBot
from NSK.utils import retry_if_exception


class Dandoli(IBot):
    def __init__(
        self,
        url: str,
        username: str,
        password: str,
        **kwargs,
    ):
        if 'options' not in kwargs:
            kwargs['options'] = webdriver.ChromeOptions()
        prefs = kwargs['options'].experimental_options.get("prefs", {})
        prefs["profile.password_manager_leak_detection"] = False # Disable 'Change the password'
        kwargs['options'].add_experimental_option("prefs", prefs)
        # ----- Init -----
        super().__init__(**kwargs)
        self.url = url
        self.authenticated = self._authentication(username, password)
        if not self.authenticated:
            raise ConnectionRefusedError("The username or password is incorrect.")
    
    def navigate(self, url, wait_for_complete = True):
        super().navigate(url, wait_for_complete)
        with suppress(TimeoutException):
            self.wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='loader-container']"))
            )
            self.wait.until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, "div[class='loader-container']"))
            )
        
    @retry_if_exception(
        exceptions=(
            StaleElementReferenceException,
            ElementClickInterceptedException,
        ),
        failure_return=False,
    )
    def _authentication(self, username: str, password: str) -> bool:
        self.navigate(self.url)
        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']"))
        ).send_keys(username)
        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[id='password']"))
        ).send_keys(password)
        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='btn login-btn']"))
        ).click()
        time.sleep(self.retry_interval)
        while self.browser.execute_script("return document.readyState") != "complete":
            time.sleep(self.retry_interval)
        with suppress(TimeoutException):
            message = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[id='field-message']"))
            )
            self.logger.error(message.text.replace("\n", ""))
            return False
        while self.browser.execute_script("return document.readyState") != "complete":
            time.sleep(self.retry_interval)
        self.wait.until(
            method = EC.element_to_be_clickable((By.CSS_SELECTOR, "div[id='header-account']")),
            message="Not Found Header Account",
        )
        self.logger.info("Authenticated")
        return True
    

    @retry_if_exception(
        exceptions=(
            StaleElementReferenceException,
            ElementClickInterceptedException,
            TimeoutException,
        ),
        failure_return=False,
    )
    def _switch_place(self,place:str) -> bool:
        self.logger.info(f"Switch Place {place}")
        self.navigate(self.url)
        while True:
            with suppress(TimeoutException):
                self.wait.until(
                    method = EC.element_to_be_clickable((By.CSS_SELECTOR, "span[class='placeSwitchButton']")),
                    message="Not Found SwitchButton",
                ).click()
                time.sleep(self.retry_interval)
                self.wait.until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "div.popover.bottom.in[role='tooltip'][id^='popover']"))
                )
                break
        self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.popover.bottom.in[role='tooltip'][id^='popover']"))
        )
        XPATH = f"//div[contains(@class,'popover__switchablePlaceListName') and contains(text(), '{place}')]"
        places = self.wait.until(
            EC.presence_of_all_elements_located((By.XPATH, XPATH))
        )
        if len(places) != 1:
            self.logger.error(f"Found {len(places)} places")
            return False       
        self.browser.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
            places[0],
        )
        time.sleep(self.retry_interval)
        self.wait.until(EC.element_to_be_clickable(places[0])).click()
        self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='loader-container']"))
        )
        self.wait.until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "div[class='loader-container']"))
        )
        time.sleep(self.retry_interval)
        current_place = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='placeSwitchButton__placeName']"))
        )
        return place in current_place.text
    
    @retry_if_exception(
        exceptions=(
            StaleElementReferenceException,
            ElementClickInterceptedException,
        ),
    )
    def get_site_info(self,place:str,site:str,keywords: list[str] = []) -> dict[str,str]:
        result: dict[str,str] = {}
        if not self._switch_place(place):
            raise RuntimeError(f"The place {place} is not found or is not available.")
        nav_site = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[id='nav-sites']"))
        )
        redirect_url=urljoin(self.url,nav_site.get_attribute('href'))
        self.navigate(redirect_url)
        self.logger.info(f"Search {site}")
        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='keyword'][type='text']"))
        ).send_keys(site)
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and text()='検索']"))
        ).click()
        while True:
            request_message = self.wait.until(
                method= EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div[class='pageContentSite__requestingMessage js-requesting-message']")
                ),
                message="Not Found requestMessage"
            )
            if request_message.get_attribute("style") == "display: none;":
                break
            time.sleep(self.retry_interval)
        rows = self.wait.until(
            EC.presence_of_all_elements_located((
                By.XPATH,
                '//div[contains(@class, "pageContentSite__tableBodyWrap")]//tr'
            ))
        )
        if len(rows) != 1:
            return result
        if rows[0].get_attribute("class") == "empty":
            return result
        self.wait.until(
            EC.element_to_be_clickable(rows[0])
        ).click()
        with suppress(TimeoutException):
            self.wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='loader-container']"))
            )
            self.wait.until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, "div[class='loader-container']"))
            )
        for keyword in keywords:
            self.logger.info(f"Get {keyword}")
            try:
                value = self.wait.until(
                    EC.visibility_of_element_located((By.XPATH, f"//th[contains(normalize-space(text()), '{keyword}')]/following-sibling::td[1]"))
                ).text.strip()
            except TimeoutException:
                value = None
            result[keyword] = value
        return result
            
        