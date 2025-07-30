import os
import platform
import subprocess
import time
import typing

import psutil
import robot_base
from pyrect import Rect
from robot_base import ParamException

from .browser_extension import ExtensionBrowser
from .playwright_browser import PlaywrightBrowser
from .utils import get_chrome_path, get_edge_path


@robot_base.log_decorator
@robot_base.func_decorator
def open_browser(
    url,
    browser_type,
    executable_path,
    privacy_mode,
    is_headless,
    is_stealth,
    extra_args,
    viewport="auto",
    timeout=30000,
    driver_type="playwright",
    **kwargs,
):
    timeout = int(timeout)
    if "user_data_dir" in kwargs and kwargs["user_data_dir"] != "":
        user_data_dir = kwargs["user_data_dir"]
    else:
        user_data_dir = os.path.join(
            os.path.expanduser("~"), ".gobot", "browser", browser_type
        )
        if not os.path.exists(user_data_dir):
            os.makedirs(user_data_dir)

    if "download_path" in kwargs and kwargs["download_path"] != "":
        download_path = kwargs["download_path"]
    else:
        download_path = os.path.join(os.path.expanduser("~"), ".gobot", "tmp")
        if not os.path.exists(download_path):
            os.makedirs(download_path)

    if "extension_path" in kwargs and kwargs["extension_path"] != "":
        extension_path = kwargs["extension_path"]
    else:
        if "execute_path" in os.environ:
            execute_path = os.environ["execute_path"]
            extension_path = os.path.join(
                execute_path, "browser", browser_type + "-extension"
            )
        else:
            extension_path = ""
    if browser_type == "chrome":
        executable_path = get_chrome_path()
    elif browser_type == "edge":
        executable_path = get_edge_path()
    if executable_path is None or not os.path.exists(executable_path):
        raise ParamException(f"{browser_type}浏览器未找到")
    if driver_type == "playwright":
        return PlaywrightBrowser.open_browser(
            url=url,
            executable_path=executable_path,
            user_data_dir=user_data_dir,
            privacy_mode=privacy_mode,
            download_path=download_path,
            timeout=timeout,
            is_headless=is_headless,
            is_stealth=is_stealth,
            extension_path=extension_path,
            extra_args=extra_args,
            viewport=viewport,
        )
    else:
        browser = ExtensionBrowser()
        browser.open_browser(
            url=url,
            executable_path=executable_path,
            user_data_dir=user_data_dir,
            privacy_mode=privacy_mode,
            download_path=download_path,
            timeout=timeout,
            is_headless=is_headless,
            is_stealth=is_stealth,
            extension_path=extension_path,
            extra_args=extra_args,
            viewport=viewport,
        )
        return browser


@robot_base.log_decorator
@robot_base.func_decorator
def simulate_mobile_browser(
    url,
    mobile_type,
    browser_type,
    executable_path,
    is_headless,
    is_stealth,
    timeout=30000,
    **kwargs,
):
    timeout = int(timeout)
    if "user_data_dir" in kwargs and kwargs["user_data_dir"] is not None:
        user_data_dir = kwargs["user_data_dir"]
    else:
        user_data_dir = os.path.join(
            os.path.expanduser("~"), "GoBot", "browser", browser_type
        )
        if not os.path.exists(user_data_dir):
            os.makedirs(user_data_dir)

    if "download_path" in kwargs and kwargs["download_path"] is not None:
        download_path = kwargs["download_path"]
    else:
        download_path = os.path.join(os.path.expanduser("~"), "GoBot", "tmp")
        if not os.path.exists(download_path):
            os.makedirs(download_path)

    return PlaywrightBrowser.simulate_mobile_browser(
        url=url,
        mobile_type=mobile_type,
        executable_path=executable_path,
        user_data_dir=user_data_dir,
        download_path=download_path,
        timeout=timeout,
        is_headless=is_headless,
        is_stealth=is_stealth,
    )


@robot_base.log_decorator
@robot_base.func_decorator
def connect_browser(
    browser_type,
    executable_path,
    debug_port,
    user_data_dir,
    timeout,
    extra_args="",
    **kwargs,
):
    if browser_type == "chrome":
        executable_path = get_chrome_path()
    elif browser_type == "edge":
        executable_path = get_edge_path()
    if executable_path is None or not os.path.exists(executable_path):
        raise ParamException(f"{browser_type}浏览器未找到")
    debug_port = int(debug_port)
    timeout = int(timeout)
    try:
        return PlaywrightBrowser.connect_browser(debug_port=debug_port, timeout=timeout)
    except:
        file_name = os.path.basename(executable_path)
        file_name_without_extension, _ = os.path.splitext(file_name)
        pids = psutil.pids()
        for pid in pids:
            pro = psutil.Process(pid)
            if (
                file_name_without_extension == pro.name()
                or file_name_without_extension + ".exe" == pro.name()
            ):
                pro.kill()
        params = f"--start-maximized --remote-debugging-port={debug_port}"
        if user_data_dir is not None and user_data_dir != "":
            params += f" --user-data-dir={user_data_dir}"
        if extra_args is not None and extra_args != "":
            params += f" {extra_args}"
        browser_process = None
        if platform.system() == "Windows":
            import win32con
            from win32comext.shell import shellcon
            from win32comext.shell.shell import ShellExecuteEx

            ShellExecuteEx(
                fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
                hwnd=None,
                lpFile=executable_path,
                nShow=win32con.SW_SHOWMAXIMIZED,
                lpParameters=params,
            )
        else:
            params += " --disable-gpu"
            browser_process = subprocess.Popen(
                [executable_path] + params.split(" "),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

        time.sleep(2)

        return PlaywrightBrowser.connect_browser(
            debug_port=debug_port, timeout=timeout, browser_process=browser_process
        )


@robot_base.log_decorator
@robot_base.func_decorator
def get_cookies(browser, urls, **kwargs):
    return browser.get_cookies(urls)


@robot_base.log_decorator
@robot_base.func_decorator
def add_cookies(browser, cookies, **kwargs):
    browser.add_cookies(cookies)


@robot_base.log_decorator
@robot_base.func_decorator
def new_page(browser, url, timeout, **kwargs):
    timeout = int(timeout)
    browser.new_page(url, timeout)


@robot_base.log_decorator
@robot_base.func_decorator
def goto_url(browser, url, timeout, **kwargs):
    timeout = int(timeout)
    browser.goto_url(url, timeout)


@robot_base.log_decorator
@robot_base.func_decorator
def reload_page(browser, timeout, **kwargs):
    timeout = int(timeout)
    browser.reload_page(timeout)


@robot_base.log_decorator
@robot_base.func_decorator
def page_forward(browser, timeout, **kwargs):
    timeout = int(timeout)
    browser.page_forward(timeout)


@robot_base.log_decorator
@robot_base.func_decorator
def page_go_back(browser, timeout, **kwargs):
    timeout = int(timeout)
    browser.page_go_back(timeout)


@robot_base.log_decorator
@robot_base.func_decorator
def page_close(browser, **kwargs):
    browser.page_close()


@robot_base.log_decorator
@robot_base.func_decorator
def page_pause(browser, **kwargs):
    browser.page_pause()


@robot_base.log_decorator
@robot_base.func_decorator
def browser_close(browser, **kwargs):
    browser.browser_close()


@robot_base.log_decorator
@robot_base.func_decorator
def page_screenshot(browser, timeout, save_path, full_page, **kwargs):
    timeout = int(timeout)
    browser.page_screenshot(timeout=timeout, save_path=save_path, full_page=full_page)


@robot_base.log_decorator
@robot_base.func_decorator
def switch_page(
    browser, match_target, match_strategy, url, title, index, bring_to_front, **kwargs
):
    browser.switch_page(
        match_strategy=match_strategy,
        match_target=match_target,
        url=url,
        title=title,
        index=index,
        bring_to_front=bring_to_front,
        **kwargs,
    )


@robot_base.log_decorator
@robot_base.func_decorator
def get_page_info(browser, info_type, **kwargs):
    return browser.get_page_info(info_type=info_type)


@robot_base.log_decorator
@robot_base.func_decorator
def find_element(browser, element_type, element_selector, highlight, **kwargs):
    return browser.find_element(
        element_type=element_type,
        element_selector=element_selector,
        highlight=highlight,
        **kwargs,
    )


@robot_base.log_decorator
@robot_base.func_decorator
def find_child_element(parent_element, element_selector, highlight, **kwargs):
    return parent_element.find_child_element(
        element_selector=element_selector, highlight=highlight
    )


@robot_base.log_decorator
@robot_base.func_decorator
def find_elements(browser, element_type, element_selector, highlight, **kwargs):
    return browser.find_elements(
        element_type=element_type,
        element_selector=element_selector,
        highlight=highlight,
        **kwargs,
    )


@robot_base.log_decorator
@robot_base.func_decorator
def start_dialog_listen(browser, dialog_message, accept, timeout, **kwargs):
    timeout = int(timeout)
    return browser.start_dialog_listen(
        dialog_message=dialog_message, accept=accept, timeout=timeout, **kwargs
    )


@robot_base.log_decorator
@robot_base.func_decorator
def start_download_listen(browser, **kwargs):
    return browser.start_download_listen(**kwargs)


@robot_base.log_decorator
@robot_base.func_decorator
def wait_download_end(browser, download_wrapper, download_dir, timeout, **kwargs):
    timeout = int(timeout)
    return browser.wait_download_end(
        download_wrapper=download_wrapper,
        download_dir=download_dir,
        timeout=timeout,
        **kwargs,
    )


@robot_base.log_decorator
@robot_base.func_decorator
def start_upload_listen(browser, upload_file, timeout, **kwargs):
    timeout = int(timeout)
    return browser.start_upload_listen(
        upload_file=upload_file, timeout=timeout, **kwargs
    )


@robot_base.log_decorator
@robot_base.func_decorator
def mouse_move(browser, x, y, steps, **kwargs):
    steps = int(steps)
    return browser.mouse_move(x=x, y=y, steps=steps, **kwargs)


@robot_base.log_decorator
@robot_base.func_decorator
def mouse_up_down(browser, mouse_type, button, click_count, **kwargs):
    return browser.mouse_up_down(
        mouse_type=mouse_type, button=button, click_count=click_count, **kwargs
    )


@robot_base.log_decorator
@robot_base.func_decorator
def mouse_click(browser, click_type, x, y, button, click_count, delay, **kwargs):
    x = int(x)
    y = int(y)
    delay = int(delay)
    click_count = int(click_count)
    return browser.mouse_click(
        click_type=click_type,
        x=x,
        y=y,
        button=button,
        click_count=click_count,
        delay=delay,
        **kwargs,
    )


@robot_base.log_decorator
@robot_base.func_decorator
def mouse_scroll(browser, delta_x, delta_y, **kwargs):
    delta_x = int(delta_x)
    delta_y = int(delta_y)
    return browser.mouse_scroll(delta_x=delta_x, delta_y=delta_y, **kwargs)


@robot_base.log_decorator
@robot_base.func_decorator
def hotkey(browser, key, delay, **kwargs):
    delay = float(delay)
    return browser.hotkey(key=key, delay=delay, **kwargs)


@robot_base.log_decorator
@robot_base.func_decorator
def keyboard_input(browser, content, delay, **kwargs):
    delay = float(delay)
    return browser.keyboard_input(content=content, delay=delay, **kwargs)


@robot_base.log_decorator
@robot_base.func_decorator
def wait_element(browser, element_type, element, display, timeout, **kwargs):
    timeout = int(int(timeout) / 1000)
    if element_type == "locator" or element_type == "pick":
        element_selector = kwargs.pop("element_selector")
        element = browser.find_element(
            element_type=element_type,
            element_selector=element_selector,
            highlight=False,
            **kwargs,
        )
    return element.wait_element(display=display, timeout=timeout, **kwargs)


@robot_base.log_decorator
@robot_base.func_decorator
def element_click(
    element_type,
    browser,
    element,
    modifiers=None,
    position=None,
    x=0,
    y=0,
    delay=0,
    button=None,
    click_count=1,
    force=False,
    timeout=30000,
    **kwargs,
):
    timeout = int(timeout)
    click_count = int(click_count)
    if modifiers:
        modifiers = modifiers.split(";")
    else:
        modifiers = None
    if element_type == "locator" or element_type == "pick":
        element_selector = kwargs.pop("element_selector")
        element = browser.find_element(
            element_type=element_type,
            element_selector=element_selector,
            highlight=False,
            **kwargs,
        )
    element.click(
        modifiers=modifiers,
        position=position,
        x=x,
        y=y,
        delay=delay,
        button=button,
        timeout=timeout,
        click_count=click_count,
        force=force,
    )


@robot_base.log_decorator
@robot_base.func_decorator
def element_hover(
    element_type,
    browser,
    element,
    modifiers=None,
    x=0,
    y=0,
    position=None,
    force=False,
    **kwargs,
):
    if modifiers:
        modifiers = modifiers.split(";")
    else:
        modifiers = None
    if element_type == "locator" or element_type == "pick":
        element_selector = kwargs.pop("element_selector")
        element = browser.find_element(
            element_type=element_type,
            element_selector=element_selector,
            highlight=False,
            **kwargs,
        )
    element.hover(modifiers=modifiers, position=position, x=x, y=y, force=force)


@robot_base.log_decorator
@robot_base.func_decorator
def element_tap(
    element_type,
    browser,
    element,
    modifiers=None,
    x=0,
    y=0,
    position=None,
    force=False,
    **kwargs,
):
    if modifiers:
        modifiers = modifiers.split(";")
    else:
        modifiers = None
    if element_type == "locator" or element_type == "pick":
        element_selector = kwargs.pop("element_selector")
        element = browser.find_element(
            element_type=element_type,
            element_selector=element_selector,
            highlight=False,
            **kwargs,
        )
    element.tap(modifiers=modifiers, position=position, x=x, y=y, force=force)


@robot_base.log_decorator
@robot_base.func_decorator
def element_fill(
    element_type, browser, element, content, clear, simulate, delay, **kwargs
):
    delay = float(delay)
    if element_type == "locator" or element_type == "pick":
        element_selector = kwargs.pop("element_selector")
        element = browser.find_element(
            element_type=element_type,
            element_selector=element_selector,
            highlight=False,
            **kwargs,
        )
    element.fill(content=content, clear=clear, simulate=simulate, delay=delay)


@robot_base.log_decorator
@robot_base.func_decorator
def element_content(element_type, browser, element, content_type, **kwargs):
    if element_type == "locator" or element_type == "pick":
        element_selector = kwargs.pop("element_selector")
        element = browser.find_element(
            element_type=element_type,
            element_selector=element_selector,
            highlight=False,
            **kwargs,
        )
    return element.get_content(content_type=content_type)


@robot_base.log_decorator
@robot_base.func_decorator
def element_capture(element_type, browser, element, save_path, **kwargs):
    if element_type == "locator" or element_type == "pick":
        element_selector = kwargs.pop("element_selector")
        element = browser.find_element(
            element_type=element_type,
            element_selector=element_selector,
            highlight=False,
            **kwargs,
        )
    return element.capture(save_path=save_path)


@robot_base.log_decorator
@robot_base.func_decorator
def get_element_attribute(element_type, browser, element, attribute_name, **kwargs):
    if element_type == "locator" or element_type == "pick":
        element_selector = kwargs.pop("element_selector")
        element = browser.find_element(
            element_type=element_type,
            element_selector=element_selector,
            highlight=False,
            **kwargs,
        )
    return element.get_attribute(attribute_name=attribute_name)


@robot_base.log_decorator
@robot_base.func_decorator
def set_element_attribute(
    element_type, browser, element, attribute_name, attribute_value, **kwargs
):
    if element_type == "locator" or element_type == "pick":
        element_selector = kwargs.pop("element_selector")
        element = browser.find_element(
            element_type=element_type,
            element_selector=element_selector,
            highlight=False,
            **kwargs,
        )
    return element.set_attribute(
        attribute_name=attribute_name, attribute_value=attribute_value
    )


@robot_base.log_decorator
@robot_base.func_decorator
def remove_element_attribute(element_type, browser, element, attribute_name, **kwargs):
    if element_type == "locator" or element_type == "pick":
        element_selector = kwargs.pop("element_selector")
        element = browser.find_element(
            element_type=element_type,
            element_selector=element_selector,
            highlight=False,
            **kwargs,
        )
    return element.remove_attribute(attribute_name=attribute_name)


@robot_base.log_decorator
@robot_base.func_decorator
def select_option(
    element_type,
    browser,
    element,
    select_type,
    select_value: typing.Optional[typing.Union[str, typing.List[str], None]],
    **kwargs,
):
    if element_type == "locator" or element_type == "pick":
        element_selector = kwargs.pop("element_selector")
        element = browser.find_element(
            element_type=element_type,
            element_selector=element_selector,
            highlight=False,
            **kwargs,
        )
    return element.select_option(select_type=select_type, select_value=select_value)


@robot_base.log_decorator
@robot_base.func_decorator
def upload_file(
    element_type,
    browser,
    element,
    file: typing.Optional[typing.Union[str, typing.List[str], None]],
    timeout=30000,
    **kwargs,
):
    timeout = float(timeout)
    if element_type == "locator" or element_type == "pick":
        element_selector = kwargs.pop("element_selector")
        element = browser.find_element(
            element_type=element_type,
            element_selector=element_selector,
            highlight=False,
            **kwargs,
        )
    return element.upload_file(file=file, timeout=timeout)


@robot_base.log_decorator
@robot_base.func_decorator
def down_file(element_type, browser, element, folder, timeout=None, **kwargs):
    if element_type == "locator" or element_type == "pick":
        element_selector = kwargs.pop("element_selector")
        element = browser.find_element(
            element_type=element_type,
            element_selector=element_selector,
            highlight=False,
            **kwargs,
        )
    return element.down_file(folder=folder, timeout=timeout)


@robot_base.log_decorator
@robot_base.func_decorator
def verification_code_identification(element_type, browser, element, **kwargs):
    if element_type == "locator" or element_type == "pick":
        element_selector = kwargs.pop("element_selector")
        element = browser.find_element(
            element_type=element_type,
            element_selector=element_selector,
            highlight=False,
            **kwargs,
        )
    return element.verification_code_identification()


@robot_base.log_decorator
@robot_base.func_decorator
def get_element_location(element_type, browser, element, **kwargs):
    if element_type == "locator" or element_type == "pick":
        element_selector = kwargs.pop("element_selector")
        element = browser.find_element(
            element_type=element_type,
            element_selector=element_selector,
            highlight=False,
            **kwargs,
        )
    return Rect(
        element.bounding_box()["x"],
        element.bounding_box()["y"],
        element.bounding_box()["width"],
        element.bounding_box()["height"],
        enableFloat=True,
    )


@robot_base.log_decorator
@robot_base.func_decorator
def scroll_into_view_if_needed(element_type, browser, element, **kwargs):
    if element_type == "locator" or element_type == "pick":
        element_selector = kwargs.pop("element_selector")
        element = browser.find_element(
            element_type=element_type,
            element_selector=element_selector,
            highlight=False,
            **kwargs,
        )
    return element.scroll_into_view_if_needed()
