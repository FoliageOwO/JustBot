# 用法

## 初始化 `BotApplication`

```python
from JustBot import BotApplication, Adapter, CQHTTPConfig,

config = CQHTTPConfig(ws_host='127.0.0.1', ws_port=6700,
                      http_host='127.0.0.1', http_port=5700, ws_reverse=False))
adapter = CQHTTPAdapter(config)

app = BotApplication(adapter)
```

## 注册监听器

```python
from JustBot import PrivateMessageEvent, GroupMessageEvent, MessageEvent
from JustBot import MessageChain
from JustBot.adapters.cqhttp import Plain

@app.receiver(event=[PrivateMessageEvent, GroupMessageEvent])
async def message_handler(event: MessageEvent, **kwargs):
    await app.send_msg(event.receiver,
        MessageChain.create(Plain('Hello, World!'))
    )
```

## 更简单地发送消息
```python
await app.send_msg(contact, MessageChain.create(Plain('hi'), Face(12))) # 创建消息链式
await app.send_msg(contact, [Plain('hi'), Face(12)]) # 列表式, 也可以用元组
await app.send_msg(contact, 'hello world') # 单个文字式
```

## 更多元素

```python
from JustBot.adapters.cqhttp import Plain, Face, Share

MessageChain.create([
    Plain('Hello, World!', '还可以有第二行!'),
    Face(138),
    Share('https://github.com/WindLeaf233/JustBot', 'Give a Star')
])
```

## 关键词匹配器 & 命令匹配器

```python
from JustBot import KeywordsMatcher, CommandMatcher

@app.receiver(event=[PrivateMessageEvent],
              matcher=KeywordsMatcher(['你好', 'hello'])) # 关键词匹配
async def keywords_handler(event: PrivateMessageEvent, **kwargs):
    await app.send_msg(event.receiver,
        MessageChain.create(Plain('你好!'))
    )

@app.receiver(event=[PrivateMessageEvent],
              matcher=CommandMatcher(['~hello'], # 命令匹配
              match_all_width=True), # 允许半角和全角  如 `!hello` 和 `！hello` 都可触发
              parameters_convert=dict) # 命令参数转换
async def command_handler(event: PrivateMessageEvent, parameters: list or dict, **kwargs):
    await app.send_msg(event.receiver,
        MessageChain.create(Plain('Hello, World!'))
    )
```

## 开始运行

```python
if __name__ == '__main__':
    app.start_running()
```
