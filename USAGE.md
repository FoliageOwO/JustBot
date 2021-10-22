# 用法

## 初始化 `BotApplication`

```python
from JustBot import BotApplication, CQHttpAdapter, CQHttpConfig,

config = CQHttpConfig(ws_host='127.0.0.1', ws_port=6700,
                      http_host='127.0.0.1', http_port=5700, ws_reverse=False))
adapter = CQHttpAdapter(config)

bot = BotApplication(adapter)
```

## 注册监听器

```python
from JustBot import PrivateMessageEvent, GroupMessageEvent,
from JustBot import Event, MessageChain
from JustBot.adapters.cqhttp import Text

@adapter.receiver([PrivateMessageEvent, GroupMessageEvent])
async def message_handler(event: Event, message: str):
    await app.send_msg(event.sender_type, event.receiver,
        MessageChain.create([Text('Hello, World!')])
    )
```

## 更多元素

```python
from JustBot.adapters.cqhttp import Text, Face, Share

MessageChain.create([
    Text('Hello, World!', 'Second line of Message.'),
    Face(138),
    Share('https://github.com/', 'Github Website')
])
```

## 关键词匹配器和命令匹配器

```python
from JustBot import KeywordsMatcher, CommandMatcher

@adapter.receiver([PrivateMessageEvent], matcher=KeywordsMatcher(['你好', 'hello']))
async def keywords_handler(event: Event, message: str):
    await app.send_msg(event.sender_type, event.receiver,
        MessageChain.create([Text('你好!')])
    )

@adapter.receiver([PrivateMessageEvent],
                  matcher=CommandMatcher(['~hello'], match_all_width=True), parameters_convert=dict)
async def command_handler(event: Event, command: str, parameters: list or dict):
    await app.send_msg(event.sender_type, event.receiver,
        MessageChain.create([Text('Hello, World!')])
    )
```

## 开始运行

```python
if __name__ == '__main__':
    app.start_running()
```
