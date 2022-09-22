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

@app.receiver([PrivateMessageEvent, GroupMessageEvent])
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

@app.matcher(KeywordsMatcher(['你好', 'hello'])) # 关键词匹配
@app.receiver(PrivateMessageEvent)
async def keywords_handler(event: PrivateMessageEvent, **kwargs):
    await event.reply('你好呀！') # 支持快速回复

@app.receiver(PrivateMessageEvent)
@app.matcher(CommandMatcher(['~hello'], # 匹配命令 `~hello`
             match_all_width=True)) # 允许半角和全角  如 `!hello` 和 `！hello` 都可触发)
@app.param_convert(dict) # 命令参数转换  如 `!hello world=1` 可以转成 {'world': 1}
async def command_handler(event: PrivateMessageEvent, parameters: list or dict, **kwargs):
    await event.reply('hello from command~')
```

## 权限组限定

```python
from JustBot.utils.role import Role

@app.role([Role.ADMIN, Role.OWNER]) # 只允许管理员和群主执行此命令
@app.matcher(CommandMatcher('~dosomething'))
@app.receiver(GroupMessageEvent)
async def dosth(event: GroupMessageEvent, **kwargs):
    # do something
    ...

@app.role([Role.ADMIN],
    lambda event, *kw: event.reply('你没有权限执行此命令!')) # 允许传入一个异步函数  只接受 `event`, `message_chain`, `message` 三个参数
...
```

## 开始运行

```python
if __name__ == '__main__':
    app.start_running()
```
