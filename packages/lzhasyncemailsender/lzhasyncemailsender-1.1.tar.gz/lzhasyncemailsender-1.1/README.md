# baidu translate
带有队列的异步邮件发送模块

## 示例
```python
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

## 安装 - [PyPI](https://pypi.org/project/lzhasyncemailsender/)
```bash
pip install lzhasyncemailsender
```

## API
[Document](https://zhhtdm.github.io/async-email-sender/)


