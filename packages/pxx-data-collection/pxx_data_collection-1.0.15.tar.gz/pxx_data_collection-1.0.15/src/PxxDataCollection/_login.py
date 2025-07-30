"""
处理商家后台登录逻辑
"""

import json
from contextlib import suppress

from DrissionPage import Chromium
from DrissionPage._pages.mix_tab import MixTab
from DrissionPage.errors import ContextLostError, ElementLostError

from ._types import Urls
from ._utils import Utils


class Login:
    def __init__(self, browser: Chromium):
        self._browser = browser

    def _get__logined_account_name(self, page: MixTab):
        """通过 local_storage 获取已登录的账号"""

        new_userinfo = page.local_storage('new_userinfo')
        if not new_userinfo:
            return

        new_userinfo_dict: dict = json.loads(new_userinfo)
        return new_userinfo_dict.get('username')

    def _check__login_captcha(self, page: MixTab, timeout: float = None):
        """
        检查登录时的验证码

        Args:
            page: 浏览器标签页
            timeout: 超时时间, 默认为 10 分钟
        """

        send_captcha_btn = page.ele('获取验证码', timeout=5)
        if not send_captcha_btn:
            return

        _timeout = timeout if isinstance(timeout, (int, float)) else 10 * 60

        print(f'等待 {_timeout} 秒输入验证码...')

        with suppress(ContextLostError, ElementLostError):
            # 如果元素因页面刷新而不存在时还调用其方法将会抛出异常, 此时可认为验证码输入完成后自动跳转
            login_center = page.ele('c:div.login-center', timeout=3)
            login_center_is_disabled = login_center.wait.disabled_or_deleted(
                timeout=_timeout
            )
            if not login_center_is_disabled:
                raise RuntimeError('等待验证码输入超时, 请重试')

    def login(
        self,
        account: str,
        password: str,
        wait_captcha: float = None,
    ):
        """
        商家后台登录, 如果登录成功则返回操作的浏览器标签页

        Args:
            account: 登陆账号
            password: 登陆密码
            wait_captcha: 等待验证码输入时间, 默认为 10 分钟
        Returns:
            登录时操作的浏览器标签页对象
        """

        page = self._browser.latest_tab

        if not Utils.same_url(page.url, Urls.login):
            page.get(Urls.home)

        if Utils.same_url(page.url, Urls.home):
            logined_account_name = self._get__logined_account_name(page=page)
            if logined_account_name == account:
                return page

            raise RuntimeError(
                f'当前已登录的用户 [{logined_account_name}] 与目标用户 [{account}] 不一致'
            )

        account_login_mode_text = '账号登录'
        switch_account_mode_btn = page.ele(account_login_mode_text, timeout=8)
        if not switch_account_mode_btn:
            raise RuntimeError(f'登录页面未找到 [{account_login_mode_text}] 按钮')
        switch_account_mode_btn.click()

        account_input = page.ele('c:input#usernameId', timeout=3)
        password_input = page.ele('c:input#passwordId', timeout=3)

        if not account_input or not password_input:
            input_ele_state = [
                ele is not None for ele in [account_input, password_input]
            ]
            raise RuntimeError(f'登录页面的账号或密码输入框未找到. {input_ele_state}')

        account_input.input(account)
        password_input.input(password)

        login_btn_text = '登录'
        login_btn = page.ele(f'@text()={login_btn_text}', timeout=3)
        if not login_btn:
            raise RuntimeError(f'未找到 [{login_btn_text}] 按钮')
        login_btn.click()

        self._check__login_captcha(page=page, timeout=wait_captcha)

        if not Utils.same_url(page.url, Urls.home):
            raise RuntimeError(f'[{account}] 登录失败')

        return page
