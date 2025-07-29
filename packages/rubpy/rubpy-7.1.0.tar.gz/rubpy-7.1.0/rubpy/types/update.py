import asyncio
from typing import Literal, Union, List, Dict, Any, Optional
from pathlib import Path
from json import dumps
import rubpy

class Update:
    """کلاس برای مدیریت آپدیت‌های دریافتی از API روبیکا."""

    def __init__(self, update: Dict[str, Any], *args, **kwargs) -> None:
        """
        مقداردهی اولیه شیء Update.

        پارامترها:
        - update: دیکشنری حاوی داده‌های آپدیت.
        - args, kwargs: آرگومان‌های اضافی.
        """
        self.client: "rubpy.Client" = update.get('client')
        self.original_update: Dict[str, Any] = update

    def __str__(self) -> str:
        """تبدیل آپدیت به رشته JSON."""
        return self.jsonify(indent=2)

    def __getattr__(self, name: str) -> Any:
        """دریافت مقدار کلید با استفاده از نام ویژگی."""
        return self.find_keys(name)

    def __setitem__(self, key: str, value: Any) -> None:
        """تنظیم مقدار در دیکشنری آپدیت."""
        self.original_update[key] = value

    def __getitem__(self, key: str) -> Any:
        """دریافت مقدار از دیکشنری آپدیت."""
        return self.original_update[key]

    def _process_list(self, items: List[Any]) -> List[Any]:
        """پردازش لیست‌ها به صورت بازگشتی برای تبدیل دیکشنری‌ها به Update."""
        return [
            self._process_list(item) if isinstance(item, list) else
            Update(item) if isinstance(item, dict) else item
            for item in items
        ]

    def jsonify(self, indent: Optional[int] = None) -> str:
        """
        تبدیل آپدیت به رشته JSON.

        پارامترها:
        - indent: تعداد فاصله برای فرمت JSON.

        خروجی:
        رشته JSON حاوی داده‌های آپدیت.
        """
        result = self.original_update.copy()
        result['original_update'] = 'dict{...}'
        return dumps(result, indent=indent, ensure_ascii=False, default=str)

    def find_keys(self, keys: Union[str, List[str]], original_update: Any = None) -> Any:
        """
        جستجوی کلیدها در آپدیت به صورت بازگشتی.

        پارامترها:
        - keys: کلید یا لیست کلیدها برای جستجو.
        - original_update: داده اولیه برای جستجو (پیش‌فرض original_update).

        خروجی:
        مقدار پیدا شده یا None.
        """
        if original_update is None:
            original_update = self.original_update

        keys = [keys] if isinstance(keys, str) else keys

        if isinstance(original_update, dict):
            for key in keys:
                if key in original_update:
                    value = original_update[key]
                    return Update(value) if isinstance(value, dict) else \
                           self._process_list(value) if isinstance(value, list) else value
            original_update = original_update.values()

        for value in original_update if isinstance(original_update, (dict, list)) else []:
            result = self.find_keys(keys, value)
            if result is not None:
                return result
        return None

    # ویژگی‌های عمومی
    @property
    def command(self) -> Any:
        """دستور موجود در آپدیت."""
        return self.find_keys('command')

    @property
    def to_dict(self) -> Dict[str, Any]:
        """دیکشنری خام آپدیت."""
        return self.original_update

    @property
    def message(self) -> Optional['Update']:
        """پیام موجود در آپدیت."""
        return self.find_keys('message')

    @property
    def is_me(self) -> bool:
        """آیا آپدیت توسط کاربر فعلی ارسال شده است."""
        return self.author_guid == self.client.guid

    @property
    def status(self) -> Any:
        """وضعیت آپدیت."""
        return self.find_keys('status')

    @property
    def action(self) -> Optional[str]:
        """اقدام مرتبط با آپدیت."""
        return self.original_update.get('action') if 'action' in self.original_update else None

    @property
    def is_edited(self) -> bool:
        """آیا پیام ویرایش شده است."""
        message = self.message
        return message is not None and message.is_edited

    @property
    def type(self) -> Any:
        """نوع آپدیت یا نویسنده."""
        return self.find_keys(['type', 'author_type'])

    @property
    def title(self) -> Optional[str]:
        """عنوان آپدیت."""
        return self.find_keys('title')

    @property
    def is_forward(self) -> bool:
        """آیا پیام فوروارد شده است."""
        message = self.message
        return message is not None and 'forwarded_from' in message.original_update

    @property
    def forward_type_from(self) -> Any:
        """نوع منبع فوروارد."""
        message = self.message
        return message.find_keys('type_from') if message else None

    @property
    def is_event(self) -> bool:
        """آیا آپدیت یک رویداد است."""
        message = self.message
        return message is not None and message.type == 'Event'

    @property
    def event_data(self) -> Any:
        """داده‌های رویداد."""
        return self.message.find_keys('event_data') if self.is_event else None

    @property
    def is_file_inline(self) -> bool:
        """آیا پیام شامل فایل درون‌خطی است."""
        message = self.message
        return message is not None and message.type in ['FileInline', 'FileInlineCaption']

    @property
    def file_inline(self) -> Optional['Update']:
        """فایل درون‌خطی موجود در آپدیت."""
        return self.find_keys('file_inline')

    @property
    def music(self) -> bool:
        """آیا فایل درون‌خطی موسیقی است."""
        return self.file_inline is not None and self.file_inline.type == 'Music'

    @property
    def file(self) -> bool:
        """آیا فایل درون‌خطی یک فایل عمومی است."""
        return self.file_inline is not None and self.file_inline.type == 'File'

    @property
    def photo(self) -> bool:
        """آیا فایل درون‌خطی تصویر است."""
        return self.file_inline is not None and self.file_inline.type == 'Image'

    @property
    def video(self) -> bool:
        """آیا فایل درون‌خطی ویدیو است."""
        return self.file_inline is not None and self.file_inline.type == 'Video'

    @property
    def voice(self) -> bool:
        """آیا فایل درون‌خطی صدا است."""
        return self.file_inline is not None and self.file_inline.type == 'Voice'

    @property
    def contact(self) -> bool:
        """آیا فایل درون‌خطی مخاطب است."""
        return self.file_inline is not None and self.file_inline.type == 'Contact'

    @property
    def location(self) -> bool:
        """آیا فایل درون‌خطی مکان است."""
        return self.file_inline is not None and self.file_inline.type == 'Location'

    @property
    def poll(self) -> bool:
        """آیا فایل درون‌خطی نظرسنجی است."""
        return self.file_inline is not None and self.file_inline.type == 'Poll'

    @property
    def gif(self) -> bool:
        """آیا فایل درون‌خطی گیف است."""
        return self.file_inline is not None and self.file_inline.type == 'Gif'

    @property
    def sticker(self) -> Optional['Update']:
        """استیکر موجود در آپدیت."""
        return self.find_keys('sticker')

    @property
    def text(self) -> Optional[str]:
        """متن پیام."""
        message = self.message
        return message.text if message else None

    @property
    def message_id(self) -> Any:
        """شناسه پیام یا پیام پین‌شده."""
        return self.find_keys(['message_id', 'pinned_message_id'])

    @property
    def reply_message_id(self) -> Any:
        """شناسه پیام پاسخ‌داده‌شده."""
        message = self.message
        return message.find_keys('reply_to_message_id') if message else None

    @property
    def is_group(self) -> bool:
        """آیا آپدیت مربوط به گروه است."""
        return self.type == 'Group'

    @property
    def is_channel(self) -> bool:
        """آیا آپدیت مربوط به کانال است."""
        return self.type == 'Channel'

    @property
    def is_private(self) -> bool:
        """آیا آپدیت مربوط به چت خصوصی است."""
        return self.type == 'User'

    @property
    def object_guid(self) -> Any:
        """GUID شیء (گروه، کانال یا کاربر)."""
        return self.find_keys(['group_guid', 'object_guid', 'channel_guid'])

    @property
    def author_guid(self) -> Any:
        """GUID نویسنده پیام."""
        message = self.message
        return message.author_object_guid if message else None

    @property
    def is_text(self) -> bool:
        """آیا پیام متنی است."""
        message = self.message
        return message is not None and message.type == 'Text'

    def guid_type(self, object_guid: Optional[str] = None) -> str:
        """
        تعیین نوع شیء بر اساس GUID.

        پارامترها:
        - object_guid: GUID شیء (پیش‌فرض object_guid آپدیت).

        خروجی:
        نوع شیء ('Channel'، 'Group' یا 'User').
        """
        object_guid = object_guid or self.object_guid
        if object_guid.startswith('c0'):
            return 'Channel'
        elif object_guid.startswith('g0'):
            return 'Group'
        return 'User'

    # متدهای ناهمگام
    async def pin(self, object_guid: Optional[str] = None, message_id: Optional[str] = None, action: str = 'Pin') -> Dict:
        """
        پین کردن پیام.

        پارامترها:
        - object_guid: GUID شیء (پیش‌فرض object_guid آپدیت).
        - message_id: شناسه پیام (پیش‌فرض message_id آپدیت).
        - action: نوع اقدام ('Pin' یا 'Unpin').

        خروجی:
        نتیجه عملیات پین.
        """
        object_guid = object_guid or self.object_guid
        message_id = message_id or self.message_id
        return await self.client.set_pin_message(object_guid, message_id, action)

    async def unpin(self, object_guid: Optional[str] = None, message_id: Optional[str] = None) -> Dict:
        """
        حذف پین پیام.

        پارامترها:
        - object_guid: GUID شیء (پیش‌فرض object_guid آپدیت).
        - message_id: شناسه پیام (پیش‌فرض message_id آپدیت).

        خروجی:
        نتیجه عملیات حذف پین.
        """
        return await self.pin(object_guid, message_id, 'Unpin')

    async def edit(self, text: str, object_guid: Optional[str] = None, message_id: Optional[str] = None, *args, **kwargs) -> Dict:
        """
        ویرایش پیام.

        پارامترها:
        - text: متن جدید پیام.
        - object_guid: GUID شیء (پیش‌فرض object_guid آپدیت).
        - message_id: شناسه پیام (پیش‌فرض message_id آپدیت).

        خروجی:
        نتیجه عملیات ویرایش.
        """
        object_guid = object_guid or self.object_guid
        message_id = message_id or self.message_id
        return await self.client.edit_message(object_guid, message_id, text, *args, **kwargs)

    async def copy(self, to_object_guid: str, from_object_guid: Optional[str] = None, message_ids: Optional[Union[str, List[str]]] = None, *args, **kwargs) -> 'Update':
        """
        کپی پیام‌ها به شیء دیگر.

        پارامترها:
        - to_object_guid: GUID مقصد.
        - from_object_guid: GUID مبدا (پیش‌فرض object_guid آپدیت).
        - message_ids: شناسه پیام‌ها (پیش‌فرض message_id آپدیت).

        خروجی:
        شیء Update حاوی نتیجه عملیات.
        """
        from_object_guid = from_object_guid or self.object_guid
        message_ids = [message_ids or self.message_id] if isinstance(message_ids, str) else message_ids or [self.message_id]
        
        result = await self.client.get_messages_by_id(from_object_guid, message_ids)
        messages = []

        for message in result.messages:
            file_inline = message.file_inline
            sticker = message.sticker
            text = message.text

            if sticker:
                messages.append(await self.client.send_message(to_object_guid, sticker=sticker.to_dict))
            elif file_inline:
                kwargs.update(file_inline.to_dict)
                if file_inline.type not in ['Gif', 'Sticker']:
                    file_inline = await self.download(file_inline)
                messages.append(await self.client.send_message(to_object_guid, text, file_inline=file_inline, *args, **kwargs))
            else:
                messages.append(await self.client.send_message(to_object_guid, text, *args, **kwargs))

        return Update({'status': 'OK', 'messages': messages})

    async def seen(self, seen_list: Optional[Dict[str, str]] = None) -> Dict:
        """
        علامت‌گذاری چت‌ها به عنوان دیده‌شده.

        پارامترها:
        - seen_list: دیکشنری حاوی GUID شیء و شناسه پیام‌ها (پیش‌فرض {object_guid: message_id}).

        خروجی:
        نتیجه عملیات.
        """
        seen_list = seen_list or {self.object_guid: self.message_id}
        return await self.client.seen_chats(seen_list)

    async def reply(self, text: Optional[str] = None, object_guid: Optional[str] = None, reply_to_message_id: Optional[str] = None,
                    file_inline: Optional[Union[Path, bytes, str]] = None, auto_delete: Optional[int] = None, type: Optional[str] = None, *args, **kwargs) -> Dict:
        """
        پاسخ به پیام.

        پارامترها:
        - text: متن پاسخ (اختیاری).
        - object_guid: GUID شیء (پیش‌فرض object_guid آپدیت).
        - reply_to_message_id: شناسه پیام پاسخ‌داده‌شده (پیش‌فرض message_id آپدیت).
        - file_inline: فایل برای ارسال (اختیاری).
        - auto_delete: زمان حذف خودکار (اختیاری).
        - type: نوع فایل (اختیاری).

        خروجی:
        نتیجه عملیات پاسخ.
        """
        object_guid = object_guid or self.object_guid
        reply_to_message_id = reply_to_message_id or self.message_id
        if type:
            kwargs['type'] = type
        return await self.client.send_message(object_guid, text, reply_to_message_id=reply_to_message_id,
                                             file_inline=file_inline, auto_delete=auto_delete, *args, **kwargs)

    async def reply_document(self, document: Union[str, bytes, Path], caption: Optional[str] = None, auto_delete: Optional[int] = None,
                             object_guid: Optional[str] = None, reply_to_message_id: Optional[str] = None, *args, **kwargs) -> Dict:
        """پاسخ با سند."""
        return await self.reply(caption, object_guid, reply_to_message_id, document, auto_delete, type='File', *args, **kwargs)

    async def reply_photo(self, photo: Union[str, bytes, Path], caption: Optional[str] = None, auto_delete: Optional[int] = None,
                          object_guid: Optional[str] = None, reply_to_message_id: Optional[str] = None, *args, **kwargs) -> Dict:
        """پاسخ با تصویر."""
        return await self.reply(caption, object_guid, reply_to_message_id, photo, auto_delete, type='Image', *args, **kwargs)

    async def reply_video(self, video: Union[str, bytes, Path], caption: Optional[str] = None, auto_delete: Optional[int] = None,
                          object_guid: Optional[str] = None, reply_to_message_id: Optional[str] = None, *args, **kwargs) -> Dict:
        """پاسخ با ویدیو."""
        return await self.reply(caption, object_guid, reply_to_message_id, video, auto_delete, type='Video', *args, **kwargs)

    async def reply_music(self, music: Union[str, bytes, Path], caption: Optional[str] = None, auto_delete: Optional[int] = None,
                          object_guid: Optional[str] = None, reply_to_message_id: Optional[str] = None, *args, **kwargs) -> Dict:
        """پاسخ با موسیقی."""
        return await self.reply(caption, object_guid, reply_to_message_id, music, auto_delete, type='Music', *args, **kwargs)

    async def reply_voice(self, voice: Union[str, bytes, Path], caption: Optional[str] = None, auto_delete: Optional[int] = None,
                          object_guid: Optional[str] = None, reply_to_message_id: Optional[str] = None, *args, **kwargs) -> Dict:
        """پاسخ با صدا."""
        return await self.reply(caption, object_guid, reply_to_message_id, voice, auto_delete, type='Voice', *args, **kwargs)

    async def reply_gif(self, gif: Union[str, bytes, Path], caption: Optional[str] = None, auto_delete: Optional[int] = None,
                        object_guid: Optional[str] = None, reply_to_message_id: Optional[str] = None, *args, **kwargs) -> Dict:
        """پاسخ با گیف."""
        return await self.reply(caption, object_guid, reply_to_message_id, gif, auto_delete, type='Gif', *args, **kwargs)

    async def reply_video_message(self, video: Union[str, bytes, Path], caption: Optional[str] = None, auto_delete: Optional[int] = None,
                                  object_guid: Optional[str] = None, reply_to_message_id: Optional[str] = None, *args, **kwargs) -> Dict:
        """پاسخ با پیام ویدیویی."""
        return await self.reply(caption, object_guid, reply_to_message_id, video, auto_delete, type='VideoMessage', *args, **kwargs)

    async def forward(self, to_object_guid: str) -> Dict:
        """
        فوروارد پیام.

        پارامترها:
        - to_object_guid: GUID مقصد.

        خروجی:
        نتیجه عملیات فوروارد.
        """
        return await self.forwards(to_object_guid, self.object_guid, [self.message_id])

    async def forwards(self, to_object_guid: str, from_object_guid: Optional[str] = None, message_ids: Optional[Union[str, List[str]]] = None) -> Dict:
        """
        فوروارد پیام‌ها.

        پارامترها:
        - to_object_guid: GUID مقصد.
        - from_object_guid: GUID مبدا (پیش‌فرض object_guid آپدیت).
        - message_ids: شناسه پیام‌ها (پیش‌فرض message_id آپدیت).

        خروجی:
        نتیجه عملیات فوروارد.
        """
        from_object_guid = from_object_guid or self.object_guid
        message_ids = [message_ids or self.message_id] if isinstance(message_ids, str) else message_ids or [self.message_id]
        return await self.client.forward_messages(from_object_guid, to_object_guid, message_ids)

    async def download(self, file_inline: Optional[Dict] = None, save_as: Optional[str] = None, *args, **kwargs) -> Union[bytes, str]:
        """
        دانلود فایل.

        پارامترها:
        - file_inline: اطلاعات فایل (پیش‌فرض file_inline آپدیت).
        - save_as: مسیر ذخیره فایل (اختیاری).
        - args, kwargs: پارامترهای اضافی برای دانلود.

        خروجی:
        داده باینری فایل یا مسیر فایل ذخیره‌شده.
        """
        file_inline = Update(file_inline) if isinstance(file_inline, dict) else file_inline or self.file_inline
        return await self.client.download(file_inline, save_as=save_as, *args, **kwargs)

    async def get_author(self, author_guid: Optional[str] = None, *args, **kwargs) -> Dict:
        """
        دریافت اطلاعات نویسنده یا کاربر.

        پارامترها:
        - author_guid: GUID نویسنده (پیش‌فرض author_guid آپدیت).

        خروجی:
        اطلاعات نویسنده یا کاربر.
        """
        author_guid = author_guid or self.author_guid
        return await self.get_object(author_guid, *args, **kwargs)

    async def get_object(self, object_guid: Optional[str] = None) -> Dict:
        """
        دریافت اطلاعات شیء.

        پارامترها:
        - object_guid: GUID شیء (پیش‌فرض object_guid آپدیت).

        خروجی:
        اطلاعات شیء.
        """
        object_guid = object_guid or self.object_guid
        guid_type = self.guid_type(object_guid)
        if guid_type == 'User':
            return await self.client.get_user_info(object_guid)
        elif guid_type == 'Group':
            return await self.client.get_group_info(object_guid)
        elif guid_type == 'Channel':
            return await self.client.get_channel_info(object_guid)
        return {}

    async def get_messages(self, object_guid: Optional[str] = None, message_ids: Optional[Union[str, List[str]]] = None) -> Dict:
        """
        دریافت پیام‌ها.

        پارامترها:
        - object_guid: GUID شیء (پیش‌فرض object_guid آپدیت).
        - message_ids: شناسه پیام‌ها (پیش‌فرض message_id آپدیت).

        خروجی:
        پیام‌های دریافت‌شده.
        """
        object_guid = object_guid or self.object_guid
        message_ids = [message_ids or self.message_id] if isinstance(message_ids, str) else message_ids or [self.message_id]
        return await self.client.get_messages_by_id(object_guid, message_ids)

    async def delete(self) -> Dict:
        """
        حذف پیام.

        خروجی:
        نتیجه عملیات حذف.
        """
        return await self.delete_messages(self.object_guid, [self.message_id])

    async def delete_messages(self, object_guid: Optional[str] = None, message_ids: Optional[Union[str, List[str]]] = None) -> Dict:
        """
        حذف پیام‌ها.

        پارامترها:
        - object_guid: GUID شیء (پیش‌فرض object_guid آپدیت).
        - message_ids: شناسه پیام‌ها (پیش‌فرض message_id آپدیت).

        خروجی:
        نتیجه عملیات حذف.
        """
        object_guid = object_guid or self.object_guid
        message_ids = [message_ids or self.message_id] if isinstance(message_ids, str) else message_ids or [self.message_id]
        return await self.client.delete_messages(object_guid, message_ids)

    async def reaction(self, reaction_id: int, object_guid: Optional[str] = None, message_id: Optional[str] = None) -> Dict:
        """
        افزودن واکنش به پیام.

        پارامترها:
        - reaction_id: شناسه واکنش.
        - object_guid: GUID شیء (پیش‌فرض object_guid آپدیت).
        - message_id: شناسه پیام (پیش‌فرض message_id آپدیت).

        خروجی:
        نتیجه عملیات واکنش.
        """
        object_guid = object_guid or self.object_guid
        message_id = message_id or self.message_id
        return await self.client.action_on_message_reaction(object_guid, message_id, 'Add', reaction_id)

    async def ban_member(self, object_guid: Optional[str] = None, user_guid: Optional[str] = None) -> Dict:
        """
        بن کردن عضو.

        پارامترها:
        - object_guid: GUID شیء (پیش‌فرض object_guid آپدیت).
        - user_guid: GUID کاربر (پیش‌فرض author_guid آپدیت).

        خروجی:
        نتیجه عملیات بن.
        """
        object_guid = object_guid or self.object_guid
        user_guid = user_guid or self.author_guid
        if object_guid.startswith('g0'):
            return await self.client.ban_group_member(object_guid, user_guid)
        elif object_guid.startswith('c0'):
            return await self.client.ban_channel_member(object_guid, user_guid)
        return {}

    async def unban_member(self, object_guid: Optional[str] = None, user_guid: Optional[str] = None) -> Dict:
        """
        رفع بن عضو.

        پارامترها:
        - object_guid: GUID شیء (پیش‌فرض object_guid آپدیت).
        - user_guid: GUID کاربر (پیش‌فرض author_guid آپدیت).

        خروجی:
        نتیجه عملیات رفع بن.
        """
        object_guid = object_guid or self.object_guid
        user_guid = user_guid or self.author_guid
        if object_guid.startswith('g0'):
            return await self.client.ban_group_member(object_guid, user_guid, 'Unset')
        elif object_guid.startswith('c0'):
            return await self.client.ban_channel_member(object_guid, user_guid, 'Unset')
        return {}

    async def send_activity(self, activity: Literal['Typing', 'Uploading', 'Recording'] = 'Typing', object_guid: Optional[str] = None) -> Dict:
        """
        ارسال فعالیت چت.

        پارامترها:
        - activity: نوع فعالیت ('Typing'، 'Uploading' یا 'Recording').
        - object_guid: GUID شیء (پیش‌فرض object_guid آپدیت).

        خروجی:
        نتیجه عملیات ارسال فعالیت.
        """
        object_guid = object_guid or self.object_guid
        return await self.client.send_chat_activity(object_guid, activity)

    async def is_admin(self, object_guid: Optional[str] = None, user_guid: Optional[str] = None) -> Dict:
        """
        بررسی ادمین بودن کاربر.

        پارامترها:
        - object_guid: GUID شیء (پیش‌فرض object_guid آپدیت).
        - user_guid: GUID کاربر (پیش‌فرض author_guid آپدیت).

        خروجی:
        نتیجه بررسی ادمین.
        """
        object_guid = object_guid or self.object_guid
        user_guid = user_guid or self.author_guid
        return await self.client.user_is_admin(object_guid, user_guid)

    async def block(self, user_guid: Optional[str] = None) -> Dict:
        """
        بلاک کردن کاربر.

        پارامترها:
        - user_guid: GUID کاربر (پیش‌فرض author_guid یا object_guid اگر کاربر باشد).

        خروجی:
        نتیجه عملیات بلاک.
        """
        user_guid = user_guid or (self.object_guid if self.guid_type(self.object_guid) == 'User' else self.author_guid)
        return await self.client.set_block_user(user_guid)

    async def get_reply_author(self, object_guid: Optional[str] = None, reply_message_id: Optional[str] = None) -> Dict:
        """
        دریافت اطلاعات نویسنده پیام پاسخ‌داده‌شده.

        پارامترها:
        - object_guid: GUID شیء (پیش‌فرض object_guid آپدیت).
        - reply_message_id: شناسه پیام پاسخ‌داده‌شده (پیش‌فرض reply_message_id آپدیت).

        خروجی:
        اطلاعات نویسنده.
        """
        result = await self.get_messages(object_guid, reply_message_id)
        return await self.client.get_info(result.messages[0].author_object_guid)

    async def get_reply_message(self, object_guid: Optional[str] = None, reply_message_id: Optional[str] = None) -> 'Update':
        """
        دریافت پیام پاسخ‌داده‌شده.

        پارامترها:
        - object_guid: GUID شیء (پیش‌فرض object_guid آپدیت).
        - reply_message_id: شناسه پیام پاسخ‌داده‌شده (پیش‌فرض reply_message_id آپدیت).

        خروجی:
        شیء Update حاوی پیام.
        """
        result = await self.get_messages(object_guid, reply_message_id)
        return result.messages[0]