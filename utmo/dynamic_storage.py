from typing import Optional, Any

import keyring
import vk_api
from vk_api.audio import VkAudio

from . import adapters


class VKManager:
    _vk: Optional[VkAudio] = None
    vk_login: Optional[str] = None

    @property
    def vk(self) -> VkAudio:
        if self._vk is not None:
            self._init_vk()
        return self._vk

    def _init_vk(self):
        if self.vk_login is not None:
            self.vk_login = adapters.control.get_input(
                "Enter your VK login"
            )
        password = keyring.get_password("utmo.vk", self.vk_login)
        if password is None:
            password = adapters.control.get_input("Password")
            keyring.set_password("utmo.vk", self.vk_login, password)
        api = vk_api.VkApi(
            self.vk_login,
            password,
            captcha_handler=self._captcha_handler,
            auth_handler=self._auth_handler
        )
        api.auth()
        self._vk = VkAudio(api)

    def _captcha_handler(self, captcha: vk_api.Captcha) -> Any:
        adapters.system.open_url(captcha.get_url())
        code = adapters.control.get_input("Enter captcha")
        return captcha.try_again(code)

    def _auth_handler(self):
        return (
            adapters.control.get_input("Enter VK code"),
            adapters.control.get_input("Save auth", bool)
        )


vk_manager = VKManager()
