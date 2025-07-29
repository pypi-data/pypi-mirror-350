# game_werewolf for ChatGPT-Mirai-QQ-Bot

本项目是 [ChatGPT-Mirai-QQ-Bot](https://github.com/lss233/chatgpt-mirai-qq-bot) 的一个插件，用于狼人杀游戏，使用开始触发游戏，数字进行游戏操作和投票。例如工作流的配置是”#狼人杀“触发，则用户输入"#狼人杀开始"，工作流中替换"#狼人杀"后,"开始"触发了游戏的初始化，后续用户继续输入"#狼人杀1"或者"#狼人杀{你的发言}"进行交互。

## 安装

```bash
pip install chatgpt-mirai-qq-bot-game-werewolf
```

## 使用

在 chatgpt-mirai-qq-bot的web_ui中配置
使用示例请参考 [game_werewolf/example/werewolf.yml](game_werewolf/example/werewolf.yaml)
安装此插件会自动生成一个狼人杀游戏工作流，仅供参考

## 开源协议

本项目基于 [ChatGPT-Mirai-QQ-Bot](https://github.com/lss233/chatgpt-mirai-qq-bot) 开发，遵循其 [开源协议](https://github.com/lss233/chatgpt-mirai-qq-bot/blob/master/LICENSE)

## 感谢

感谢 [ChatGPT-Mirai-QQ-Bot](https://github.com/lss233/chatgpt-mirai-qq-bot) 的作者 [lss233](https://github.com/lss233) 提供框架支持


