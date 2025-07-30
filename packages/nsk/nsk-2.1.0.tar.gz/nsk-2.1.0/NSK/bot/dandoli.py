import time
from contextlib import suppress
from typing import List
from urllib.parse import urljoin

from selenium import webdriver
from selenium.common.exceptions import (ElementClickInterceptedException,
                                        StaleElementReferenceException,
                                        TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
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
        if 'timeout' not in kwargs or kwargs['timeout'] < 10:
            kwargs['timeout'] = 10 # Min Timeout is 10s
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
        ),
        failure_return=False,
    )
    def _switch_place(self,name:str,company:str = "") -> bool:
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
        time.sleep(self.retry_interval)
        self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.popover.bottom.in[role='tooltip'][id^='popover']"))
        )
        time.sleep(self.retry_interval)
        xpath = (
            f"//a[contains(@class, 'popover__switchablePlaceListLink js-switch-place') and "
            f".//div[contains(@class, 'popover__switchablePlaceListName') and contains(., '{name}')] and "
            f".//div[contains(@class, 'popover__switchableCompanyName') and contains(., '{company}')]]"
        )
        places:List[WebElement]  = self.wait.until(
            EC.presence_of_all_elements_located((By.XPATH, xpath))
        )
        if len(places) != 1:
            raise RuntimeError(f"Expected exactly 1 place {name} of company '{company}', but found {len(places)}: {places}")
        # -- Redirect --
        self.browser.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
            places[0]
        )
        self.logger.info("Switch place {name}, {company}".format(
            name = places[0].find_element(By.CSS_SELECTOR,"div[class='popover__switchablePlaceListName']").text.split("\n")[0].strip(),
            company = places[0].find_element(By.CSS_SELECTOR,"div[class='popover__switchableCompanyName']").text.strip()
        ))
        time.sleep(self.retry_interval)
        switching_btn = places[0].find_element(By.TAG_NAME,'span')
        self.wait.until(EC.element_to_be_clickable(switching_btn)).click()
        with suppress(TimeoutException):
            self.wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='loader-container']"))
            )
            self.wait.until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, "div[class='loader-container']"))
            )
        time.sleep(self.retry_interval)
        # -- Check Place --
        current_place = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='placeSwitchButton__placeName']"))
        )
        return name in current_place.text
    
    @retry_if_exception(
        exceptions=(
          StaleElementReferenceException,
          ElementClickInterceptedException,  
        ),
        failure_return=[]
    )
    def find_place(self,place:str) -> List[dict[str,str]]:
        places = []
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
        time.sleep(self.retry_interval)
        self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.popover.bottom.in[role='tooltip'][id^='popover']"))
        )
        time.sleep(self.retry_interval)
        found:List[WebElement]  = self.wait.until(
            EC.presence_of_all_elements_located((By.XPATH, (
                f"//a[contains(@class, 'popover__switchablePlaceListLink js-switch-place') and "
                f".//div[contains(@class, 'popover__switchablePlaceListName') and contains(., '{place}')]]"
            )))
        )
        for p in found:
            places.append({
                'name': p.find_element(By.CSS_SELECTOR,"div[class='popover__switchablePlaceListName']").text.split("\n")[0].strip(),
                'company': p.find_element(By.CSS_SELECTOR,"div[class='popover__switchableCompanyName']").text.strip(),
            })
        return places

    @retry_if_exception(
        exceptions=(
            StaleElementReferenceException,
            ElementClickInterceptedException,
        ),
        failure_return={},
    )
    def get_building_info(self,name:str,place:str,company:str="", keywords: list[str] = []) -> dict[str,str]:
        """
        Retrieves information about a construction/building project based on the provided details.

        Args:
            name (str): Name of the building or project.
            place (str): Location of the building or project.
            company (str, optional): Name of the associated company. Defaults to an empty string.
            keywords (list[str], optional): Additional keywords to refine the search or filter the results. Defaults to an empty list.

        Returns:
            dict[str, str]: A dictionary containing relevant building information, such as address, contractor, status, etc.
        """
        self.logger.info(
            f"Getting {keywords} from building '{name}' located in '{place}' (company: '{company}')"
        )
        result: dict[str,str] = {}
        if not self._switch_place(
            name=place,
            company=company
        ):
            if sites := self.find_place(place):
                for site in sites:
                    if result := self.get_building_info(
                        name=name,
                        place=site['name'],
                        company=site['company'],
                        keywords=keywords
                    ):
                        return result
            raise RuntimeError(f"Get Building Info Failed: {site}")
        nav_site = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[id='nav-sites']"))
        )
        redirect_url=urljoin(self.url,nav_site.get_attribute('href'))
        self.navigate(redirect_url)
        self.logger.info(f"Search {name}")
        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='keyword'][type='text']"))
        ).send_keys(name)
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
            raise RuntimeError("Found more than one building.")
        if rows[0].get_attribute("class") == "empty":
            raise RuntimeError(f"The building {name} is not found.")
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
            try:
                value = self.wait.until(
                    EC.visibility_of_element_located((By.XPATH, f"//th[contains(normalize-space(text()), '{keyword}')]/following-sibling::td[1]"))
                )
                self.browser.execute_script(
                    "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                    value
                )
                time.sleep(self.retry_interval)
                value = value.text.strip()
            except TimeoutException:
                value = None
            self.logger.info(f"Found {value} for {keyword}")
            result[keyword] = value
        return result
            
        