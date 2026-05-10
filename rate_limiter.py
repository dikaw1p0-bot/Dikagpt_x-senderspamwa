# sender.py - WhatsApp message sending logic

import uiautomator2 as u2
import asyncio
import random
from config import DEFAULT_DELAY_JITTER

class WhatsAppSender:
    def __init__(self):
        self.device = None
        self.loop = asyncio.get_event_loop()
    
    def connect(self):
        """Connect to local Android device via uiautomator2."""
        self.device = u2.connect()
        print(f"[+] Connected: {self.device.info}")
        return self.device
    
    async def open_chat(self, phone: str):
        """Open WhatsApp chat with given phone number."""
        if self.device is None:
            self.connect()
        self.device.app_start("com.whatsapp")
        await asyncio.sleep(2)
        self.device(resourceId="com.whatsapp:id/fab").click()
        await asyncio.sleep(1)
        self.device(resourceId="com.whatsapp:id/contactpicker_search_input").set_text(phone)
        await asyncio.sleep(2)
        self.device(textContains=phone).click()
        await asyncio.sleep(2)
    
    async def send_message(self, message: str, add_jitter: bool = True):
        """Type and send a single message via UI."""
        if self.device is None:
            raise RuntimeError("Not connected. Call connect() first.")
        # Optional jitter to mimic human timing (defense evasion research)
        if add_jitter:
            await asyncio.sleep(random.uniform(0, DEFAULT_DELAY_JITTER))
        # uiautomator2 operations are blocking -> run in executor
        def _ui_ops():
            self.device(resourceId="com.whatsapp:id/entry").set_text(message)
            self.device(resourceId="com.whatsapp:id/send").click()
        await self.loop.run_in_executor(None, _ui_ops)
        print(f"[+] Sent: {message[:40]}")
    
    async def close(self):
        """Press back twice to exit chat."""
        if self.device:
            self.device.press("back")
            self.device.press("back")
