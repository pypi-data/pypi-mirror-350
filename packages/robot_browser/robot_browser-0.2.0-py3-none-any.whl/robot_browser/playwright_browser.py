import fnmatch
import os
import random
import re
import threading
import time
import typing

import playwright.sync_api
from playwright.sync_api import Page, BrowserContext, Locator
from playwright_stealth import StealthConfig, stealth_sync
from robot_base import ParamException
from robot_base.log_util import Logger

try:
    import ddddocr
except:
    pass

from .utils import get_element, get_frame

stealth_config = StealthConfig(
    webdriver=True,
    chrome_app=True,
    chrome_csi=True,
    chrome_load_times=True,
    chrome_runtime=True,
    navigator_languages=True,
    navigator_plugins=True,
    navigator_permissions=True,
    webgl_vendor=True,
    outerdimensions=True,
    navigator_hardware_concurrency=True,
    media_codecs=True,
)


class PlaywrightBrowser(object):
    p = None
    browser_map = {}

    def __init__(self, browser):
        self.browser: BrowserContext = browser
        self.page: typing.Optional[Page] = None
        self.browser_process = None

    @staticmethod
    def connect_browser(debug_port, timeout, browser_process=None):
        Logger.get_logger().info(f"正在执行:连接浏览器")
        timeout = int(timeout)
        if not PlaywrightBrowser.p:
            PlaywrightBrowser.p = playwright.sync_api.sync_playwright().start()
        browser = PlaywrightBrowser.p.chromium.connect_over_cdp(
            endpoint_url=f"http://127.0.0.1:{debug_port}", timeout=timeout
        )
        if len(browser.contexts) == 0:
            browser.new_context(
                ignore_https_errors=True,
                viewport={"width": 1920, "height": 1080},
                accept_downloads=True,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            )
        playwright_browser = PlaywrightBrowser(browser.contexts[0])
        playwright_browser.browser_process = browser_process

        def new_page_listener(page):
            stealth_sync(page, stealth_config)
            page.set_default_timeout(timeout)
            page.set_viewport_size({"width": 1920, "height": 1080})

        browser.contexts[0].on("page", new_page_listener)
        if len(browser.contexts[0].pages) == 0:
            playwright_browser.page = browser.contexts[0].new_page()
        else:
            playwright_browser.page = browser.contexts[0].pages[0]
        return playwright_browser

    @staticmethod
    def open_browser(
        url,
        executable_path,
        privacy_mode,
        user_data_dir,
        download_path,
        timeout,
        is_headless,
        is_stealth,
        extension_path,
        extra_args,
        viewport,
    ) -> "PlaywrightBrowser":
        if not PlaywrightBrowser.p:
            PlaywrightBrowser.p = playwright.sync_api.sync_playwright().start()
        if executable_path.__contains__("firefox"):
            browser_type = PlaywrightBrowser.p.firefox
        elif executable_path.__contains__("webkit"):
            browser_type = PlaywrightBrowser.p.webkit
        else:
            browser_type = PlaywrightBrowser.p.chromium
        os.makedirs(user_data_dir, exist_ok=True)
        args = [
            "--disable-infobars",
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        ]
        if not is_headless:
            args.append("--start-maximized")
        if extra_args and isinstance(extra_args, str) and extra_args != "":
            args.extend(extra_args.split(" "))
        if extra_args and isinstance(extra_args, list):
            args.extend(extra_args)
        if extension_path:
            args.append(f"--disable-extensions-except={extension_path}")
            args.append(f"--load-extension={extension_path}")
        ignore_args = ["--incognito", "--enable-automation"]
        timeout = int(timeout)
        if viewport == "auto":
            viewport_size = {"width": 1920, "height": 1080}
        else:
            viewport_size = {
                "width": int(viewport.split("x")[0]),
                "height": int(viewport.split("x")[1]),
            }
        if privacy_mode:
            browser = browser_type.launch(
                executable_path=executable_path,
                args=args,
                ignore_default_args=ignore_args,
                timeout=timeout,
                downloads_path=download_path,
                headless=is_headless,
            )
            browser = browser.new_context(
                ignore_https_errors=True,
                no_viewport=True if viewport == "auto" else False,
                viewport=viewport_size,
                accept_downloads=True,
            )
            browser.new_page()
        else:
            if user_data_dir in PlaywrightBrowser.browser_map:
                browser = PlaywrightBrowser.browser_map[user_data_dir]
            else:
                browser = browser_type.launch_persistent_context(
                    user_data_dir=user_data_dir,
                    executable_path=executable_path,
                    ignore_https_errors=True,
                    timeout=timeout,
                    no_viewport=True if viewport == "auto" else False,
                    viewport=viewport_size,
                    args=args,
                    ignore_default_args=ignore_args,
                    accept_downloads=True,
                    downloads_path=download_path,
                    headless=is_headless,
                )
                PlaywrightBrowser.browser_map[user_data_dir] = browser

        def new_page_listener(page):
            if is_stealth:
                stealth_sync(page, stealth_config)
            page.set_default_timeout(timeout)

        browser.on("page", new_page_listener)
        if url:
            time.sleep(0.5)
            browser.pages[0].goto(url, timeout=timeout)
        playwright_browser = PlaywrightBrowser(browser)
        playwright_browser.page = browser.pages[0]
        playwright_browser.page.set_default_timeout(timeout)
        return playwright_browser

    @staticmethod
    def simulate_mobile_browser(
        url,
        executable_path,
        mobile_type,
        user_data_dir,
        download_path,
        timeout,
        is_headless,
        is_stealth,
    ) -> "PlaywrightBrowser":
        timeout = int(timeout)
        if not PlaywrightBrowser.p:
            PlaywrightBrowser.p = playwright.sync_api.sync_playwright().start()
        if executable_path.__contains__("firefox"):
            browser_type = PlaywrightBrowser.p.firefox
        elif executable_path.__contains__("webkit"):
            browser_type = PlaywrightBrowser.p.webkit
        else:
            browser_type = PlaywrightBrowser.p.chromium
        os.makedirs(user_data_dir, exist_ok=True)
        args = ["--disable-infobars", "--disable-blink-features=AutomationControlled"]
        ignore_args = ["--incognito", "--enable-automation"]
        devices = PlaywrightBrowser.p.devices
        browser = browser_type.launch(
            executable_path=executable_path,
            args=args,
            headless=is_headless,
            timeout=timeout,
            downloads_path=download_path,
            ignore_default_args=ignore_args,
        ).new_context(**devices[mobile_type])
        if is_stealth:
            browser.add_init_script(
                path=os.path.join(
                    os.path.dirname(os.path.abspath(__file__)), r"stealth.min.js"
                )
            )
        if url:
            browser.new_page().goto(url, timeout=timeout)
        playwright_browser = PlaywrightBrowser(browser)
        playwright_browser.page = browser.pages[0]
        playwright_browser.page.set_default_timeout(timeout)
        return playwright_browser

    def new_page(self, url, timeout):
        timeout = int(timeout)
        page = self.browser.new_page()
        page.goto(url=url, timeout=timeout, wait_until="domcontentloaded")
        page.set_default_timeout(timeout)
        self.page = page

    def goto_url(self, url, timeout):
        timeout = int(timeout)
        self.page.goto(url, timeout=timeout, wait_until="domcontentloaded")

    def reload_page(self, timeout):
        timeout = int(timeout)
        self.page.reload(timeout=timeout, wait_until="domcontentloaded")

    def page_forward(self, timeout):
        timeout = int(timeout)
        self.page.go_forward(timeout=timeout, wait_until="domcontentloaded")

    def page_go_back(self, timeout):
        timeout = int(timeout)
        self.page.go_back(timeout=timeout, wait_until="domcontentloaded")

    def page_close(self):
        self.page.close()

    def page_pause(self):
        self.page.pause()

    def browser_close(self):
        try:
            self.browser.close()
        except:
            pass
        if self.browser_process:
            try:
                self.browser_process.kill()
            except:
                pass

    def page_screenshot(self, timeout, save_path, full_page):
        timeout = int(timeout)
        self.page.screenshot(timeout=timeout, path=save_path, full_page=full_page)

    def get_page_info(self, info_type):
        if info_type == "url":
            return self.page.url
        elif info_type == "title":
            return self.page.title()
        elif info_type == "content":
            return self.page.content()

    def switch_page(
        self, match_target, match_strategy, url, title, index, bring_to_front, **kwargs
    ):
        self.browser.pages[0].evaluate("1")
        if match_target == "title":
            if match_strategy == "equals":
                for current_page in self.browser.pages:
                    if current_page.title() == title:
                        self.page = current_page
                        if bring_to_front:
                            self.page.bring_to_front()
                        return
                raise Exception(f"{title}未找到")
            elif match_strategy == "contains":
                for current_page in self.browser.pages:
                    if current_page.title().__contains__(title):
                        self.page = current_page
                        if bring_to_front:
                            self.page.bring_to_front()
                        return
                raise Exception(f"{title}未找到")
            elif match_strategy == "fnmatch":
                for current_page in self.browser.pages:
                    if fnmatch.fnmatch(current_page.title(), title):
                        self.page = current_page
                        if bring_to_front:
                            self.page.bring_to_front()
                        return
                raise Exception(f"{title}未找到")
        elif match_target == "url":
            if match_strategy == "equals":
                for current_page in self.browser.pages:
                    if current_page.url == url:
                        self.page = current_page
                        if bring_to_front:
                            self.page.bring_to_front()
                        return
                raise Exception(f"{url}未找到")
            elif match_strategy == "contains":
                for current_page in self.browser.pages:
                    if current_page.url.__contains__(url):
                        self.page = current_page
                        if bring_to_front:
                            self.page.bring_to_front()
                        return
                raise Exception(f"{url}未找到")
            elif match_strategy == "fnmatch":
                for current_page in self.browser.pages:
                    if fnmatch.fnmatch(current_page.url, url):
                        self.page = current_page
                        if bring_to_front:
                            self.page.bring_to_front()
                        return
                raise Exception(f"{url}未找到")
        elif match_target == "index":
            index = int(index)
            if index > len(self.browser.pages) - 1:
                raise Exception(f"{index}未找到")
            else:
                self.page = self.browser.pages[index]
                if bring_to_front:
                    self.page.bring_to_front()

    def find_element(self, element_type, element_selector, highlight, **kwargs):
        element_locator = None
        if element_type == "pick":
            pick_element = kwargs.get("pick_element", {})
            if pick_element is None or "xpath" not in pick_element:
                raise ParamException("元素选择器不能为空")
            if "frameXpath" in pick_element and pick_element["frameXpath"]:
                frame_selector = get_frame(pick_element["frameXpath"], self.page)
                element_locator = get_element(
                    pick_element["xpath"], frame_selector
                ).first
            else:
                element_locator = get_element(pick_element["xpath"], self.page).first
        elif element_type == "locator":
            if "frame_selector" in kwargs and kwargs["frame_selector"]:
                frame_selector = get_frame(kwargs["frame_selector"], self.page)
                element_locator = get_element(element_selector, frame_selector).first
            else:
                element_locator = get_element(element_selector, self.page).first
        if element_locator is not None:
            if highlight:
                element_locator.highlight()
            return PlaywrightElement(element_locator)

    def find_elements(self, element_type, element_selector, highlight, **kwargs):
        elements = []
        element_locator = None
        if element_type == "pick":
            pick_element = kwargs.get("pick_element", {})
            if pick_element is None or "xpath" not in pick_element:
                raise ParamException("元素选择器不能为空")
            if "frameXpath" in pick_element and pick_element["frameXpath"]:
                frame_selector = get_frame(pick_element["frameXpath"], self.page)
                element_locator = get_element(pick_element["xpath"], frame_selector)
            else:
                element_locator = get_element(pick_element["xpath"], self.page)
        elif element_type == "locator":
            if "frame_selector" in kwargs and kwargs["frame_selector"]:
                frame_selector = get_frame(kwargs["frame_selector"], self.page)
                element_locator = get_element(element_selector, frame_selector)
            else:
                element_locator = get_element(element_selector, self.page)
        if highlight:
            element_locator.highlight()
        for element in element_locator.all():
            elements.append(PlaywrightElement(element))

        return elements

    def start_dialog_listen(self, dialog_message, accept, timeout, **kwargs):
        timeout = int(timeout)
        dialog_wrapper = PlaywrightDialogWrapper()
        dialog_wrapper.timeout = timeout

        def dialog_handler(dialog):
            if dialog.message.__contains__(dialog_message):
                if accept:
                    dialog.accept()
                else:
                    dialog.dismiss()
            else:
                if accept:
                    dialog.dismiss()
                else:
                    dialog.accept()
            dialog_wrapper.set_result(dialog.type, dialog.message, dialog.default_value)

        self.page.once("dialog", dialog_handler)
        return dialog_wrapper

    def start_download_listen(self, **kwargs):
        download_wrapper = PlaywrightDownloadWrapper()

        def download_handler(download: playwright.sync_api.Download):
            download_wrapper.set_result(download)

        self.page.once("download", download_handler)
        return download_wrapper

    @staticmethod
    def wait_download_end(
        download_wrapper: "PlaywrightDownloadWrapper",
        download_dir,
        timeout,
        **kwargs,
    ):
        timeout = int(timeout)
        download = download_wrapper.get_result(timeout)
        save_path = os.path.join(download_dir, download.suggested_filename)
        download.save_as(save_path)
        return save_path

    def start_upload_listen(self, upload_file, timeout, **kwargs):
        timeout = int(timeout)

        def filechooser_handler(filechooser: playwright.sync_api.FileChooser):
            filechooser.set_files(upload_file, timeout=timeout)

        self.page.once("filechooser", filechooser_handler)

    def mouse_move(self, x, y, steps, **kwargs):
        self.page.mouse.move(x=x, y=y, steps=steps)

    def mouse_up_down(self, mouse_type, button, click_count, **kwargs):
        if mouse_type == "down":
            self.page.mouse.down(button=button, click_count=click_count)
        else:
            self.page.mouse.up(button=button, click_count=click_count)

    def mouse_click(
        self,
        click_type,
        x,
        y,
        button,
        click_count,
        delay,
        **kwargs,
    ):
        if click_type == "single":
            self.page.mouse.click(
                x=x, y=y, button=button, click_count=click_count, delay=delay
            )
        else:
            self.page.mouse.dblclick(x=x, y=y, button=button, delay=delay)

    def mouse_scroll(self, delta_x, delta_y, **kwargs):
        self.page.mouse.wheel(delta_x=delta_x, delta_y=delta_y)

    def hotkey(self, key, delay, **kwargs):
        self.page.keyboard.press(key=key.replace(";", "+"), delay=delay)

    def keyboard_input(self, content, delay, **kwargs):
        self.page.keyboard.type(text=content, delay=delay)

    @property
    def current_url(self):
        return self.page.url

    @property
    def current_title(self):
        return self.page.title()

    def get_cookies(
        self, urls: typing.Optional[typing.Union[str, typing.Sequence[str]]] = None
    ):
        return self.browser.cookies(urls=urls)

    def add_cookies(self, cookies):
        return self.browser.add_cookies(cookies)


def split_string_by_spaced_pipe(s):
    # 正则表达式匹配左右各有一个空格的 | 字符
    pipe_pattern = r"\s\|(?=\s)"
    return re.split(pipe_pattern, s)


class PlaywrightElement(object):

    def __init__(self, locator: Locator):
        self.locator = locator

    def find_child_element(self, element_selector, highlight):
        locator = self.locator.first.locator(element_selector)
        if highlight:
            locator.highlight()
        return PlaywrightElement(locator)

    def wait_element(self, display, timeout, **kwargs):
        timeout = int(timeout)
        start = time.perf_counter()
        while True:
            try:
                if display == "display" and self.locator.count() > 0:
                    return True
                if display != "display" and (self.locator.count() == 0):
                    return False
                remain = start + timeout - time.perf_counter()
                if remain > 0:
                    time.sleep(min(remain, 0.5))
                else:
                    return self.locator.count() > 0
            except:
                pass

    def click(
        self,
        *,
        modifiers=None,
        position=None,
        x=0,
        y=0,
        delay=0,
        button=None,
        click_count=1,
        force=False,
        timeout=30000,
    ):
        timeout = int(timeout)
        if position:
            box = self.locator.bounding_box()
            if position == "center":
                position = {"x": box["width"] / 2, "y": box["height"] / 2}
            elif position == "random":
                position = {
                    "x": random.randint(1, int(box["width"])),
                    "y": random.randint(1, int(box["height"])),
                }
            else:
                position = {"x": int(x), "y": int(y)}
        self.locator.click(
            modifiers=modifiers,
            position=position,
            delay=delay,
            button=button,
            click_count=click_count,
            force=force,
            timeout=timeout,
        )

    def tap(self, *, modifiers=None, x=0, y=0, position=None, force=False):
        if position:
            box = self.locator.bounding_box()
            if position == "center":
                position = {"x": box["width"] / 2, "y": box["height"] / 2}
            elif position == "random":
                position = {
                    "x": random.randint(1, int(box["width"])),
                    "y": random.randint(1, int(box["height"])),
                }
            else:
                position = {"x": int(x), "y": int(y)}
        self.locator.tap(modifiers=modifiers, position=position, force=force)

    def hover(self, *, modifiers=None, x=0, y=0, position=None, force=False):
        if position:
            box = self.locator.bounding_box()
            if position == "center":
                position = {"x": box["width"] / 2, "y": box["height"] / 2}
            elif position == "random":
                position = {
                    "x": random.randint(1, int(box["width"])),
                    "y": random.randint(1, int(box["height"])),
                }
            else:
                position = {"x": int(x), "y": int(y)}
        self.locator.hover(modifiers=modifiers, position=position, force=force)

    def fill(self, content, clear, simulate, delay):
        if not clear:
            content = self.locator.input_value() + content
        if simulate:
            self.locator.clear()
            self.locator.press_sequentially(content, delay=delay)
        else:
            self.locator.fill(content)

    def get_content(self, content_type):
        if content_type == "text":
            return self.locator.inner_text()
        elif content_type == "html":
            return self.locator.inner_html()
        elif content_type == "value":
            return self.locator.input_value()
        else:
            raise Exception(f"不支持的类型{content_type}")

    def capture(self, save_path):
        self.locator.screenshot(path=save_path)

    def get_attribute(self, attribute_name):
        return self.locator.get_attribute(name=attribute_name)

    def set_attribute(self, attribute_name, attribute_value):
        self.locator.evaluate(
            "(node, obj) => node.setAttribute(obj[0],obj[1])",
            [attribute_name, attribute_value],
        )

    def remove_attribute(self, attribute_name):
        self.locator.evaluate(
            "(node, attribute_name) => node.removeAttribute(attribute_name)",
            attribute_name,
        )

    def select_option(
        self,
        select_type,
        select_value: typing.Optional[typing.Union[str, typing.List[str], None]],
    ):
        if select_type == "by_value":
            self.locator.select_option(value=select_value)
        elif select_type == "by_label":
            self.locator.select_option(label=select_value)
        else:
            if isinstance(select_value, list):
                select_value = [int(value) for value in select_value]
            else:
                select_value = int(select_value)
            self.locator.select_option(index=select_value)

    def upload_file(
        self,
        file: typing.Optional[typing.Union[str, typing.List[str], None]],
        timeout=30000,
    ):
        timeout = int(timeout)
        with self.locator.page.expect_file_chooser(timeout=timeout) as file_info:
            self.locator.click()
        file_chooser = file_info.value
        file_chooser.set_files(file)

    def down_file(self, folder, timeout=30000):
        timeout = int(timeout)
        self.locator.click(trial=True)
        with self.locator.page.expect_download(timeout=timeout) as download_info:
            self.locator.click()
        download = download_info.value
        download.save_as(os.path.join(folder, download.suggested_filename))
        download.delete()
        return os.path.join(folder, download.suggested_filename)

    def verification_code_identification(self, **kwargs):
        image = self.locator.screenshot()
        ocr = ddddocr.DdddOcr()
        return ocr.classification(image)

    def scroll_into_view_if_needed(self):
        self.locator.scroll_into_view_if_needed()

    def bounding_box(self, **kwargs):
        return self.locator.bounding_box()

    @property
    def is_visible(self):
        return self.locator.is_visible()

    @property
    def is_enabled(self):
        return self.locator.is_enabled()

    @property
    def count(self):
        return self.locator.count()


class PlaywrightDialogWrapper(object):
    def __init__(self):
        self.dialog_result: typing.Optional[PlaywrightDialogResult] = None
        self.cond = threading.Condition()
        self.timeout = 10
        self.flag = False

    def get_result(self):
        if self.flag:
            return self.dialog_result
        else:
            try:
                self.cond.acquire()
                self.cond.wait(self.timeout)
                if self.flag:
                    return self.dialog_result
                else:
                    raise Exception("等待弹窗超时")
            finally:
                self.cond.release()

    def set_result(self, dialog_type, message, default_value):
        try:
            self.cond.acquire()
            self.dialog_result = PlaywrightDialogResult(
                dialog_type, message, default_value
            )
            self.flag = True
            self.cond.notify()
        finally:
            self.cond.release()


class PlaywrightDialogResult(object):
    def __init__(self, dialog_type, message, default_value):
        self.dialog_type = dialog_type
        self.message = message
        self.default_value = default_value

    def set_dialog_type(self, dialog_type):
        self.dialog_type = dialog_type

    def set_message(self, message):
        self.message = message

    def set_default_value(self, default_value):
        self.default_value = default_value

    def get_message(self):
        return self.message

    def get_default_value(self):
        return self.default_value

    def get_dialog_type(self):
        return self.dialog_type


class PlaywrightDownloadWrapper(object):
    def __init__(self):
        self.cond = threading.Condition()
        self.flag = False
        self.download: typing.Optional[playwright.sync_api.Download] = None

    def get_result(self, timeout=30):
        if self.flag:
            return self.download
        else:
            try:
                self.cond.acquire()
                self.cond.wait(timeout)
                if self.flag:
                    return self.download
                else:
                    raise Exception("等待下载超时")
            finally:
                self.cond.release()

    def set_result(self, download: playwright.sync_api.Download):
        try:
            self.cond.acquire()
            self.download = download
            self.flag = True
            self.cond.notify()
        finally:
            self.cond.release()
