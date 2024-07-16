# 用法

## 初始化 `BotApplication`

```python
config = OneBot11Config(ws_host='127.0.0.1', ws_port=6700,
                        http_host='127.0.0.1', http_port=5700, ws_reverse=False)
# 或直接默认配置
# config = OneBot11Config()
adapter = OneBot11Adapter(config)
app = BotApplication(adapter)
```

## 注册监听器

```python
@app.on([PrivateMessageEvent, GroupMessageEvent])
async def message_handler(event: MessageEvent, **kwargs):
    await app.send_msg(event.receiver, 'Hello, World!')
```

## 更简单地发送消息
```python
await app.send_msg(contact, MessageChain.create(Plain('hi'), Face(12))) # 原始创建消息链式
await app.send_msg(contact, [Plain('hi'), Face(12)]) # 列表式, 也可以用元组
await app.send_msg(contact, 'hello world') # 单个文字式
```

## 更多元素

```python
MessageChain.create([
    Plain('Hello, World!', '还可以有第二行!'),
    Face(138),
    Share('https://github.com/WindLeaf233/JustBot', 'Give a Star')
])
```

## 关键词匹配器 & 命令匹配器

```python
@app.matcher(KeywordMatcher(['你好', 'hello'])) # 关键词匹配
@app.on(PrivateMessageEvent)
async def keywords_handler(event: PrivateMessageEvent, **kwargs):
    await event.reply('你好呀！') # 支持快速回复

@app.matcher(CommandMatcher(['!hello'], # 匹配命令 `!hello`
             match_all_width=True)) # 允许半角和全角  如 `!hello` 和 `！hello` 都可触发)
@app.param_convert(dict) # 命令参数转换  如 `!hello world=1` 可以转成 {'world': '1'}
@app.on(PrivateMessageEvent)
async def command_handler(event: PrivateMessageEvent, **kwargs):
    world = kwargs.get('world') or ''
    await event.reply('hello from command~')
```

## 权限组限定

```python
@app.role([Role.ADMIN, Role.OWNER]) # 只允许管理员和群主执行此命令
@app.matcher(CommandMatcher('~dosomething'))
@app.on(GroupMessageEvent)
async def dosth(event: GroupMessageEvent, **kwargs):
    # do something
    ...

@app.role([Role.ADMIN],
    lambda event, *kw: event.reply('你没有权限执行此命令!')) # 允许传入一个异步函数  只接受 `event`, `message_chain`, `message` 三个参数
...
```

## 自然语言处理
```python
@app.nlp(c=80, keywords=['天气'], params={'city': 'ns', 'time': 't'})
@app.matcher(CommandMatcher('!weather'))
@app.on([GroupMessageEvent])
async def weather(event: GroupMessageEvent, city: str = '北京', time: str = '今天', **kwargs):
    await event.reply(f'{city}的{time}的天气是...')
```

## 开始运行

```python
if __name__ == '__main__':
    app.start_running()
```
