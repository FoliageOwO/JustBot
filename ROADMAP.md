## 代办

- [x] 更便捷的 API
  * [x] MessageEvent#reply
  * [x] BotApplication#receiver
- [x] 加入权限系统, 允许设置对应权限执行
- [ ] 实现插件化
- [ ] 完全实现 `go-cqhttp` 适配器
  * [x] 完善 `NoticeEvent`
  * [ ] 完善 `API`
- [x] 统一化文档
- [ ] 使用 `WebSocket` 通信, 而不是 `HTTP`
- [ ] 在连接 `WebSocket` 的时候, 添加重连功能, 而不是直接退出程序
- [ ] 简化装饰器
- [ ] 自适应函数参数
- [ ] 添加 `BotApplication#to_me` 装饰器
- [x] 使用 `BotApplication#command`, `BotApplication#keyword` 装饰器代替 `BotApplication#matcher`
- [ ] 优化日志输出, 添加 `DEBUG` 模式
- [ ] 脚手架实现
- [ ] 更好的异常处理
- [ ] 匹配器重载
