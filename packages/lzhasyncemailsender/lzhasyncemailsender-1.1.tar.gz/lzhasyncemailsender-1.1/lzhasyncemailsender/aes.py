import asyncio
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import aiosmtplib
from lzhgetlogger import get_logger

logger = get_logger()

class AsyncEmailSender:
    """
    带有队列的异步邮件发送模块
    ```python
    # 示例
    import asyncio
    from lzhasyncemailsender import AsyncEmailSender
    
    async def main():
        sender = AsyncEmailSender('smtp.example.com', 587, 'you@example.com', 'yourpassword')
        await sender.send('target@example.com', 'Subject', '<h1>Hello World</h1>')  # 发送给一个邮箱地址
        await sender.send(['target1@example.com','target2@example.com'], 'Subject', '<h1>Hello World</h1>')  # 发送给一个邮箱地址列表
        await asyncio.sleep(10)
        await sender.stop()
        
    asyncio.run(main())
    ```
    """
    def __init__(self, smtp_server:str, smtp_port:int, sender:str, password:str):
        """
        - `smtp_server` : SMTP Server
        - `smtp_port` : SMTP Port
        - `sender` : 发送者邮箱帐号
        - `password` : 发送者邮箱密码 (如果使用`Gmail`, 建议[创建应用专用密码](https://support.google.com/mail/answer/185833))
        """
        self._smtp_server = smtp_server
        self._smtp_port = smtp_port
        self._sender = sender
        self._password = password

        self._queue = asyncio.Queue()
        self._running = True
        self._client = None
        self._loop_task = asyncio.create_task(self._process_queue())

    async def _connect(self):
        if self._client:
            try:
                await self._client.noop()
                return True
            except:
                self._client = None

        try:
            self._client = aiosmtplib.SMTP(hostname=self._smtp_server, port=self._smtp_port, start_tls=True)
            await self._client.connect()
            await self._client.login(self._sender, self._password)
            logger.debug("Connected and logged in to SMTP server.")
            return True
        except Exception as e:
            self._client = None
            logger.error(f"Failed to connect/login to SMTP server: {e}")
            return False

    async def _send_email(self, to, subject, body):
        if not await self._connect():
            return False

        msg = MIMEMultipart()
        msg['From'] = self._sender
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        try:
            await self._client.send_message(msg)
            logger.info(f"Sent email to {to}, subject: {subject}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            self._client = None
            return False

    async def _process_queue(self):
        while self._running:
            email_data = await self._queue.get()
            retry = 3
            while retry > 0 and not await self._send_email(**email_data):
                retry -= 1
                logger.warning(f"Retrying to send email ({3 - retry}/3)...")
            self._queue.task_done()

    async def send(self, to:str|list[str], subject:str, body:str):
        """
        将邮件信息`put`至发送队列
        - `to` : 接收者邮箱或邮箱列表
        - `subject` : 邮件主题
        - `body` : 邮件内容，可以是`html`字符串
        """
        _tos = []
        if isinstance(to, list):
            _tos = to
        else :
            _tos.append(to)
        for _to in _tos:
            await self._queue.put({
                'to': _to,
                'subject': subject,
                'body': body
            })

    async def stop(self):
        self._running = False
        if self._client:
            await self._client.quit()

if __name__ == "__main__":
    async def main():
        sender = AsyncEmailSender('smtp.example.com', 587, 'you@example.com', 'yourpassword')
        await sender.send('target@example.com', 'Subject', '<h1>Hello World</h1>')  # 发送给一个邮箱地址
        await sender.send(['target1@example.com','target2@example.com'], 'Subject', '<h1>Hello World</h1>')  # 发送给一个邮箱地址列表
        await asyncio.sleep(10)
        await sender.stop()
        
    asyncio.run(main())
