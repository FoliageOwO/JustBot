# JustBot

一个轻量的 qqbot 简易框架

## 适配器

- [x] <90%> `CQHttpAdapter`: 对 [`go-cqhttp`](https://github.com/Mrs4s/go-cqhttp) 的实现

- [ ] <20%> `MiraiAdapter`: 对 [`mirai-api-http`](https://github.com/project-mirai/mirai-api-http) 的实现

- [ ] <0%> `TelegramAdapter`: 对[`telegram-bot-api`](https://github.com/eternnoir/pyTelegramBotAPI) 的实现

## 待办

- [ ] 更便捷的 API
  * [ ] MessageEvent#reply
- [ ] 加入权限系统, 允许设置对应权限执行
- [ ] 实现插件化
- [ ] 完全实现 `go-cqhttp` 适配器
  * [ ] 完善 `NoticeEvent`
  * [ ] 完善 `API`
- [ ] 统一化文档

## 用法

见 [`USAGE.md`](USAGE.md).

## 关于

此项目只是闲暇时间的随手之作, 可能包含让人呕血的代码, 也包含一些 `shitcode`.

部分实现参考了 `GraiaApplication`.

### 相关项目

- [GraiaProject/Application](https://github.com/GraiaProject/Application)
- [Mrs4s/go-cqhttp](https://github.com/Mrs4s/go-cqhttp)
- [mamoe/mirai](https://github.com/mamoe/mirai)
  * [project-mirai/mirai-api-http](https://github.com/project-mirai/mirai-api-http)
