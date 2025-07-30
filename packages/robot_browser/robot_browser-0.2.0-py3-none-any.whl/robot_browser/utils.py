import os
import re
import sys
import typing

from playwright.sync_api import Page, FrameLocator


def is_xpath(selector):
    if selector.startswith("/"):
        return True
    else:
        return False


def get_frame_array(selector):
    return re.findall(r"(.*?/i?(?:frame(?!set))(?:\[.*?\])*)", selector, re.IGNORECASE)


def get_frame(selector, page: Page):
    if is_xpath(selector):
        frames = get_frame_array(selector)
        frame_locator = None
        for frame_selector in frames:
            if frame_locator is None:
                frame_locator = page.frame_locator(f"xpath={frame_selector}")
            else:
                frame_locator = frame_locator.frame_locator(f"xpath={frame_selector}")
        return frame_locator
    else:
        return page.frame_locator(selector)


def get_element(selector, page: typing.Union[Page, FrameLocator]):
    if is_xpath(selector):
        return page.locator(f"xpath={selector}")
    else:
        return page.locator(selector)


def get_chrome_path_from_registry():
    import winreg

    try:
        # 打开注册表中的相关键
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe",
        )
    except FileNotFoundError:
        try:
            # 如果上述路径不存在，尝试当前用户的注册表
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe",
            )
        except FileNotFoundError:
            return None

    # 从注册表中获取Chrome的路径
    value, _ = winreg.QueryValueEx(key, "")
    # 关闭注册表键
    winreg.CloseKey(key)
    return value


def get_chrome_path_from_env():
    program_files = os.getenv("PROGRAMFILES")
    program_files_x86 = os.getenv("PROGRAMFILES(X86)")

    # 常见的Chrome安装路径
    possible_paths = [
        os.path.join(program_files, "Google", "Chrome", "Application", "chrome.exe"),
        os.path.join(
            program_files_x86, "Google", "Chrome", "Application", "chrome.exe"
        ),
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None


def get_chrome_path():
    chrome_path = get_chrome_path_from_registry()
    if chrome_path is not None and os.path.exists(chrome_path):
        return chrome_path
    chrome_path = get_chrome_path_from_env()
    if chrome_path is not None and os.path.exists(chrome_path):
        return chrome_path
    possible_paths = {
        "win32": [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ],
        "darwin": ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"],
        "linux": ["/usr/bin/google-chrome", "/usr/bin/google-chrome-stable"],
    }

    platform = sys.platform
    for path in possible_paths.get(platform, []):
        if os.path.exists(path):
            return path
    return None


def get_edge_path_from_registry():
    import winreg

    try:
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe",
        )
    except FileNotFoundError:
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe",
            )
        except FileNotFoundError:
            print("Edge浏览器未安装或路径未添加到注册表")
            return None

    value, _ = winreg.QueryValueEx(key, "")
    winreg.CloseKey(key)
    return value


def get_edge_path_from_env():
    program_files = os.getenv("PROGRAMFILES")
    program_files_x86 = os.getenv("PROGRAMFILES(X86)")
    possible_paths = [
        os.path.join(program_files, "Microsoft", "Edge", "Application", "msedge.exe"),
        os.path.join(
            program_files_x86, "Microsoft", "Edge", "Application", "msedge.exe"
        ),
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None


def get_edge_path():
    edge_path = get_edge_path_from_registry()
    if edge_path is not None and os.path.exists(edge_path):
        return edge_path
    edge_path = get_edge_path_from_env()
    if edge_path is not None and os.path.exists(edge_path):
        return edge_path
    common_paths = [
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"D:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"D:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    ]
    for path in common_paths:
        if os.path.exists(path):
            return path
    return None
