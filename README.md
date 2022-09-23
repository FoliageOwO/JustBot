# JustBot

![](https://img.shields.io/github/repo-size/WindLeaf233/JustBot)
![](https://img.shields.io/pypi/v/jbot)
![](https://img.shields.io/github/license/WindLeaf233/JustBot)
![](https://img.shields.io/badge/made%20with-%E2%9D%A4-important)

一个轻量的异步 QQ 机器人框架.

---

## 适配器

- [x] <90%> `CQHTTPAdapter`: 对 [`go-cqhttp`](https://github.com/Mrs4s/go-cqhttp) 的实现

- [ ] <20%> `MiraiAdapter`: 对 [`mirai-api-http`](https://github.com/project-mirai/mirai-api-http) 的实现

- [ ] <0%> `TelegramAdapter`: 对[`telegram-bot-api`](https://github.com/eternnoir/pyTelegramBotAPI) 的实现

## 开始使用

```shell
$ pip install jbot
```

用法见 [`USAGE.md`](USAGE.md).

## 待办

- [x] 更便捷的 API
  * [x] MessageEvent#reply
  * [x] BotApplication#receiver
- [x] 加入权限系统, 允许设置对应权限执行
- [ ] 实现插件化
- [ ] 完全实现 `go-cqhttp` 适配器
  * [x] 完善 `NoticeEvent`
  * [ ] 完善 `API`
- [ ] 统一化文档
- [ ] 使用 `WebSocket` 通信, 而不是 `HTTP`

## 关于

此项目只是闲暇时间的随手之作, 可能包含让人呕血的代码, 也包含一些 `shitcode`.

部分实现参考了 `GraiaApplication`.

### 相关项目

- [GraiaProject/Application](https://github.com/GraiaProject/Application)
- [Mrs4s/go-cqhttp](https://github.com/Mrs4s/go-cqhttp)
- [mamoe/mirai](https://github.com/mamoe/mirai)
  * [project-mirai/mirai-api-http](https://github.com/project-mirai/mirai-api-http)
