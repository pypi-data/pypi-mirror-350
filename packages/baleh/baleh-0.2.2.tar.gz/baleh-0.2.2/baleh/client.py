import aiohttp
import asyncio
import logging
import time
from typing import Optional, Callable, Any, List
from .objects import Message, Chat, User
from .utils import helpers

# تنظیم لاگ داخلی
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class BaleClient:
    def __init__(self, token: str, proxy: Optional[str] = None, timeout: int = 30):
        """ایجاد کلاینت با توکن، پروکسی، و زمان‌بندی"""
        self.token = token
        self.base_url = f"https://tapi.bale.ai/bot{token}"
        self.proxy = proxy
        self.timeout = timeout
        self.session: Optional[aiohttp.ClientSession] = None
        self.handlers: List[Callable] = []
        self.is_running = False
        self.last_update_id = 0
        self.scheduled_tasks: List[dict] = []  # برای زمان‌بندی پیام‌ها

    async def connect(self):
        """اتصال به API بله با تنظیمات پروکسی و لاگ"""
        try:
            connector = aiohttp.TCPConnector(verify_ssl=True)
            self.session = aiohttp.ClientSession(
                connector=connector,
                timeout=aiohttp.ClientTimeout(total=self.timeout),
                proxy=self.proxy
            )
            logger.info("اتصال به API بله با موفقیت برقرار شد.")
            return self
        except Exception as e:
            logger.error(f"خطا در اتصال به API: {str(e)}")
            raise

    async def disconnect(self):
        """قطع اتصال با مدیریت صحیح منابع"""
        if self.session:
            await self.session.close()
            self.session = None
            self.is_running = False
            logger.info("اتصال به API بله قطع شد.")
        for task in self.scheduled_tasks:
            task["task"].cancel()

    async def send_message(self, chat_id: int, text: str, parse_mode: Optional[str] = None) -> Message:
        """ارسال پیام متنی با پارامترهای پیشرفته"""
        data = {"chat_id": chat_id, "text": helpers.format_message(text)}
        if parse_mode:
            data["parse_mode"] = parse_mode
        try:
            async with self.session.post(
                f"{self.base_url}/sendMessage",
                json=data
            ) as resp:
                data = await resp.json()
                if data.get("ok"):
                    logger.info(f"پیام به {chat_id} ارسال شد: {text}")
                    return Message(**data["result"])
                raise Exception(f"Error sending message: {data}")
        except Exception as e:
            logger.error(f"خطا در ارسال پیام: {str(e)}")
            raise

    async def send_photo(self, chat_id: int, photo: str, caption: Optional[str] = None) -> Message:
        """ارسال عکس با کپشن"""
        data = {"chat_id": chat_id, "photo": photo}
        if caption:
            data["caption"] = caption
        try:
            async with self.session.post(
                f"{self.base_url}/sendPhoto",
                data=data
            ) as resp:
                data = await resp.json()
                if data.get("ok"):
                    logger.info(f"عکس به {chat_id} ارسال شد")
                    return Message(**data["result"])
                raise Exception(f"Error sending photo: {data}")
        except Exception as e:
            logger.error(f"خطا در ارسال عکس: {str(e)}")
            raise

    async def send_video(self, chat_id: int, video: str, caption: Optional[str] = None, duration: Optional[int] = None) -> Message:
        """ارسال ویدیو با کپشن و مدت زمان"""
        data = {"chat_id": chat_id, "video": video}
        if caption:
            data["caption"] = caption
        if duration:
            data["duration"] = duration
        try:
            async with self.session.post(
                f"{self.base_url}/sendVideo",
                data=data
            ) as resp:
                data = await resp.json()
                if data.get("ok"):
                    logger.info(f"ویدیو به {chat_id} ارسال شد")
                    return Message(**data["result"])
                raise Exception(f"Error sending video: {data}")
        except Exception as e:
            logger.error(f"خطا در ارسال ویدیو: {str(e)}")
            raise

    async def send_document(self, chat_id: int, document: str, caption: Optional[str] = None) -> Message:
        """ارسال فایل با کپشن"""
        data = {"chat_id": chat_id, "document": document}
        if caption:
            data["caption"] = caption
        try:
            async with self.session.post(
                f"{self.base_url}/sendDocument",
                data=data
            ) as resp:
                data = await resp.json()
                if data.get("ok"):
                    logger.info(f"فایل به {chat_id} ارسال شد")
                    return Message(**data["result"])
                raise Exception(f"Error sending document: {data}")
        except Exception as e:
            logger.error(f"خطا در ارسال فایل: {str(e)}")
            raise

    async def send_voice(self, chat_id: int, voice: str, caption: Optional[str] = None) -> Message:
        """ارسال صوت با کپشن"""
        data = {"chat_id": chat_id, "voice": voice}
        if caption:
            data["caption"] = caption
        try:
            async with self.session.post(
                f"{self.base_url}/sendVoice",
                data=data
            ) as resp:
                data = await resp.json()
                if data.get("ok"):
                    logger.info(f"صوت به {chat_id} ارسال شد")
                    return Message(**data["result"])
                raise Exception(f"Error sending voice: {data}")
        except Exception as e:
            logger.error(f"خطا در ارسال صوت: {str(e)}")
            raise

    async def send_sticker(self, chat_id: int, sticker: str) -> Message:
        """ارسال استیکر"""
        try:
            async with self.session.post(
                f"{self.base_url}/sendSticker",
                data={"chat_id": chat_id, "sticker": sticker}
            ) as resp:
                data = await resp.json()
                if data.get("ok"):
                    logger.info(f"استیکر به {chat_id} ارسال شد")
                    return Message(**data["result"])
                raise Exception(f"Error sending sticker: {data}")
        except Exception as e:
            logger.error(f"خطا در ارسال استیکر: {str(e)}")
            raise

    def on_message(self):
        """دکوراتور برای هندل کردن پیام‌ها با فیلترهای پیشرفته"""
        def decorator(handler: Callable):
            def wrapper(message: Message):
                if hasattr(message, "text") and message.text:
                    asyncio.create_task(handler(message))
            self.handlers.append(wrapper)
            return wrapper
        return decorator

    async def start_polling(self, allowed_updates: Optional[List[str]] = None):
        """شروع پولینگ با آپدیت‌های فیلترشده و مدیریت قطع ارتباط"""
        self.is_running = True
        offset = self.last_update_id
        while self.is_running:
            try:
                params = {"offset": offset, "timeout": self.timeout}
                if allowed_updates:
                    params["allowed_updates"] = allowed_updates
                async with self.session.get(
                    f"{self.base_url}/getUpdates",
                    params=params
                ) as resp:
                    data = await resp.json()
                    if not data.get("ok"):
                        logger.warning("پاسخ نادرست از سرور بله")
                        await asyncio.sleep(1)
                        continue
                    for update in data["result"]:
                        offset = update["update_id"] + 1
                        self.last_update_id = offset
                        message = Message(**update.get("message", {}))
                        for handler in self.handlers:
                            await handler(message)
                    await self._check_scheduled_tasks()
            except Exception as e:
                logger.error(f"خطا در پولینگ: {str(e)}")
                await asyncio.sleep(1)

    async def _check_scheduled_tasks(self):
        """بررسی و اجرای وظایف زمان‌بندی‌شده"""
        current_time = time.time()
        tasks_to_remove = []
        for task in self.scheduled_tasks:
            if current_time >= task["time"]:
                await self.send_message(task["chat_id"], task["text"])
                tasks_to_remove.append(task)
        for task in tasks_to_remove:
            self.scheduled_tasks.remove(task)

    def schedule_message(self, chat_id: int, text: str, delay_seconds: int):
        """زمان‌بندی ارسال پیام"""
        task_time = time.time() + delay_seconds
        task = {"chat_id": chat_id, "text": text, "time": task_time, "task": None}
        self.scheduled_tasks.append(task)
        logger.info(f"پیام برای {chat_id} در {delay_seconds} ثانیه زمان‌بندی شد")

    async def get_chat_member(self, chat_id: int, user_id: int) -> dict:
        """دریافت اطلاعات عضویت کاربر در چت"""
        try:
            async with self.session.post(
                f"{self.base_url}/getChatMember",
                json={"chat_id": chat_id, "user_id": user_id}
            ) as resp:
                data = await resp.json()
                if data.get("ok"):
                    return data["result"]
                raise Exception(f"Error getting chat member: {data}")
        except Exception as e:
            logger.error(f"خطا در دریافت اطلاعات عضویت: {str(e)}")
            raise

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.disconnect()

    def stop_polling(self):
        """توقف پولینگ"""
        self.is_running = False
        logger.info("پولینگ متوقف شد.")

# مثال برای تست (اختیاری، می‌تونی حذف کنی)
if __name__ == "__main__":
    async def handle_message(message):
        await message.reply_text(f"دریافت شد: {message.text}")

    async def main():
        client = BaleClient("YOUR_BLE_TOKEN")
        client.on_message()(handle_message)
        await client.connect()
        client.schedule_message(123456789, "پیام زمان‌بندی‌شده", 5)
        await client.start_polling()

    asyncio.run(main())