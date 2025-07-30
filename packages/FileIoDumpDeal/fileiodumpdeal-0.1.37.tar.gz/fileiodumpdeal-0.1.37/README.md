# FileIoDumpDeal 文件方式导出提交任务

# 1 设计目的
通过文件IO的方式实现获取自然语言定义任务要求并提交执行结果。

# 2 安装指南

在Windows或Linux系统中，执行如下命令
```
uv tool install FileIoDumpDeal
```
即可得到 DumpDealFlarum 可执行文件，对应目录分别是
- 在Windows下，`%HOMEPATH%\.local\bin\DumpDealFlarum.exe`
- 在Linux下，`$HOME/.local/bin/DumpDealFlarum`

# 3 配置指南

1. 创建新的工作目录，假定是`<WorkDir>`
2. 在终端窗口进入到 `<WorkDir>`

## 3.1 配置LLM
编辑 `<WorkDir>/flarum.env`文件，以Ollama模型为例，配置如下：
```
FLARUM_URL=http://example.flarum.com
FLARUM_TOKEN=<token>
FLARUM_TAG_FOCUS=general
CRON_PARAM_DEFAULT=every 1h
```

# 4 运行命令

```
DumpDealFlarum <McpTaskDir> <WorkDir>
```