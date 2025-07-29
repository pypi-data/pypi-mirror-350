import logging
import os
import sys
import time
from abc import ABC, abstractmethod
from contextlib import suppress
from typing import Literal

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait

from .meta import IBotMeta


class IBot(ABC, metaclass=IBotMeta):
    def __init__(
        self,
        options: Options | None = None ,
        service: Service | None = None,
        keep_alive: bool = False,
        timeout: float = 5,
        retry_interval: float = 0.5,
        log_name: str = __name__,
        log_format:str = "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        log_level: Literal["DEBUG","INFO","WARNING","ERROR","CRITICAL"] = "INFO",
        log_file: str | None = None
    ):
        """
        Khởi tạo bot tự động hóa sử dụng trình duyệt Chrome với cấu hình logging tùy chỉnh.
        Args:
            options (Options, optional): Các tùy chọn cấu hình cho trình duyệt Chrome. Mặc định là ChromeOptions() mặc định.
            service (Service, optional): Đối tượng service điều khiển ChromeDriver. Mặc định là ChromeService() mặc định.
            keep_alive (bool, optional): Giữ kết nối trình duyệt sống sau khi script kết thúc hay không. Mặc định là False.
            timeout (float, optional): Thời gian timeout (giây) chờ các thao tác Selenium. Mặc định là 5 giây.
            retry_interval (float, optional): Khoảng thời gian chờ giữa các lần thử lại thao tác (polling interval). Mặc định là 0.5 giây.
            log_name (str, optional): Tên logger sử dụng để phân biệt nguồn log (thường là tên class/module). Mặc định là tên module hiện tại (__name__).
            log_format (str, optional): Định dạng của dòng log, theo chuẩn của logging.Formatter. Mặc định là thời gian - cấp độ - tên logger - message.
            log_level (Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], optional): Mức độ log mong muốn. Mặc định là "INFO".
            log_file (str | None, optional): Đường dẫn file để ghi log. Nếu là None thì chỉ in log ra console. Mặc định là None.
        Note:
            Cấu hình logging của các IBot sẽ bị ghi đè nếu ứng dụng chính hoặc module cha đã thiết lập cấu hình logging riêng trước đó.
        """
        # ------ # 
        self.timeout = timeout
        self.authenticated = False
        self.retry_interval = retry_interval
        # ------ # 
        self.options = options
        self.service = service
        self.browser = webdriver.Chrome(
            options=self.options,
            service=self.service,
            keep_alive=keep_alive,
        )
        self.browser.maximize_window()
        self.wait = WebDriverWait(
            driver=self.browser,
            timeout=self.timeout,
            poll_frequency=self.retry_interval,
        )
        self.root_window = self.browser.window_handles[0]
        # ------ # 
        self.logger = logging.getLogger(log_name)
        if not self.logger.hasHandlers():
            self.logger.setLevel(log_level)
            formatter = logging.Formatter(log_format)
            # -- Console Logging
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
            # -- File Logging
            if log_file:
                os.makedirs(os.path.dirname(os.path.abspath(log_file)), exist_ok=True)
                file_handler = logging.FileHandler(log_file, encoding="utf-8")
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)
        # ------ # 
        prefs = getattr(self.options, "experimental_options", {}).get("prefs", {}) if self.options else {}
        self.download_directory = prefs.get(
            "download.default_directory",
            os.path.join(os.path.expanduser("~"), "downloads"),
        )
        os.makedirs(self.download_directory, exist_ok=True)
        # ------ # 
        self.logger.info(f"Initiating {self.__class__.__name__}")

    def __del__(self):
        with suppress(Exception):
            self.browser.quit()
                
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.browser.quit()
        
    def navigate(self, url, wait_for_complete: bool = True):
        time.sleep(self.retry_interval)
        self.browser.execute_script("window.stop()")
        time.sleep(self.retry_interval)
        self.browser.get(url)
        time.sleep(self.retry_interval)
        if wait_for_complete:
            while (
                self.browser.execute_script("return document.readyState") != "complete"
            ):
                time.sleep(self.retry_interval)
        time.sleep(self.retry_interval)

    @abstractmethod
    def _authentication(self, **kwargs) -> bool:
        """Abstract method to implement authentication"""
        pass

    def open_new_tab(self) -> int:
        before_windows = self.browser.window_handles
        self.browser.execute_script("window.open('');")
        after_windows = self.browser.window_handles
        return list(set(after_windows) - set(before_windows))[0]

    def wait_for_download_to_start(self) -> list[str]:
        while True:
            downloading_files = [
                filename
                for filename in os.listdir(self.download_directory)
                if filename.endswith(".crdownload")
            ]
            if downloading_files:
                return downloading_files

    def wait_for_download_to_finish(self) -> tuple[str, str]:
        window_id = self.open_new_tab()
        self.browser.switch_to.window(window_id)
        self.navigate("chrome://downloads")
        download_items: list[WebElement] = self.browser.execute_script(
            """
            return document.
                querySelector("downloads-manager").shadowRoot
                .querySelector("#mainContainer #downloadsList #list")
                .querySelectorAll("downloads-item")
        """
        )
        item_id = download_items[0].get_attribute("id")
        while self.browser.execute_script(
            f"""
            return document
                .querySelector("downloads-manager").shadowRoot
                .querySelector("#downloadsList #list")
                .querySelector("#{item_id}").shadowRoot
                .querySelector("#content #details #progress")
            """
        ):  # Progess
            time.sleep(self.retry_interval)
        name = self.browser.execute_script(
            f"""
            return document
                .querySelector("downloads-manager").shadowRoot
                .querySelector("#downloadsList")
                .querySelector("#list")
                .querySelector("#{item_id}").shadowRoot
                .querySelector("#content")
                .querySelector("#details")
                .querySelector("#title-area")
                .querySelector("#name")
                .getAttribute("title")
            """
        )
        tag = self.browser.execute_script(
            f"""
            return document
                .querySelector("downloads-manager").shadowRoot
                .querySelector("#downloadsList")
                .querySelector("#list")
                .querySelector("#{item_id}").shadowRoot
                .querySelector("#content")
                .querySelector("#details")
                .querySelector("#title-area")
                .querySelector("#tag")
                .textContent.trim();
            """
        )
        self.browser.close()
        self.browser.switch_to.window(self.root_window)
        return name, tag