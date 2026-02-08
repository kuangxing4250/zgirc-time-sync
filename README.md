# ZGIRC时间同步

[![Python 3.7+](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Windows](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

专业的时间同步工具，支持图形界面、自动同步、开机自启动和一键更新。

## 功能特性

- **图形界面**：简洁直观的GUI设计
- **时间同步**：从Windows时间服务器获取准确时间
- **自动同步**：每小时自动校准系统时间
- **开机自启动**：支持开机自动运行（后台模式）
- **一键更新**：通过wget自动下载更新版本
- **详细日志**：完整的日志记录系统
- **管理员权限**：自动处理系统时间修改权限

## 系统要求

- 操作系统：Windows 7/8/10/11
- Python版本：3.7及以上
- 依赖组件：pywin32（用于系统启动项管理）

## 安装方式

### 方式一：pip安装（推荐）

```bash
# 克隆项目
git clone https://github.com/kuangxing4250/zgirc-time-sync.git
cd zgirc-time-sync

# 安装依赖
pip install -r requirements.txt

# 运行程序
python time.py
```

### 方式二：打包为EXE

```bash
# 安装pyinstaller
pip install pyinstaller

# 打包命令（前台版本）
pyinstaller --onefile --windowed --name "ZGIRC_TimeSync" time.py

# 打包命令（包含wget）
pyinstaller --onefile --windowed --add-data "wget.exe;." --name "ZGIRC_TimeSync" time.py
```

### 方式三：直接下载EXE

前往[Releases页面](https://github.com/你的用户名/zgirc-time-sync/releases)下载预编译的EXE文件。

## 使用说明

### 启动程序

- **前台模式**：直接运行程序，显示图形界面
- **后台模式**：使用参数 `--background`，程序在后台运行

```bash
# 前台模式
python time.exe

# 后台模式
python time.exe --background
```

### 界面功能

1. **立即同步**：点击按钮立即执行时间同步
2. **一键更新**：检查并下载最新版本
3. **开机自启动**：勾选启用系统启动项
4. **自动同步**：勾选启用每小时自动同步
5. **查看日志**：查看最近的运行日志

### 配置文件

程序会自动创建 `config.json` 配置文件：

```json
{
    "auto_sync": true,
    "interval": 3600
}
```

- `auto_sync`：是否启用自动同步
- `interval`：自动同步间隔（秒），默认为3600（1小时）

## 文件结构

```
zgirc-time-sync/
├── time.py           # 主程序文件
├── wget.exe          # 更新下载工具
├── requirements.txt  # Python依赖
├── setup.py          # 打包脚本
├── .gitignore        # Git忽略配置
├── README.md         # 项目说明
├── LICENSE           # 开源协议
├── log/              # 日志目录（自动创建）
└── config.json       # 配置文件（自动创建）
```

## 更新日志

### v4.1（当前版本）

- 全新GUI界面设计
- 支持前台/后台双模式运行
- 新增开机自启动管理
- 新增一键更新功能
- 改进日志系统
- 优化错误处理机制

## API说明

### 时间服务器

程序使用以下时间源：

- **主时间源**：`http://time.windows.com`（Windows时间服务器）
- **更新服务器**：`http://time.zgric.top/update/lastupdate_time.exe`

### 更新机制

1. 程序调用 `wget.exe` 从更新服务器下载最新版本
2. 自动备份当前版本为 `time_backup_当前版本号.exe`
3. 替换新版本后自动重启程序

## 常见问题

### Q: 提示需要管理员权限？

A: 请右键点击程序，选择"以管理员身份运行"，或者在启动项中设置管理员权限运行。

### Q: 后台模式如何退出？

A: 在任务管理器中找到"ZGIRC时间同步"进程，结束该进程即可。

### Q: 如何查看详细日志？

A: 点击界面上的"查看日志"按钮，或直接查看 `log/` 目录下的日志文件。

### Q: 同步失败怎么办？

A: 请检查：
1. 网络连接是否正常
2. 防火墙是否阻止了时间服务器访问
3. 是否有管理员权限

## 开发说明

### 添加新功能

1. Fork 本项目
2. 创建新分支：`git checkout -b feature/your-feature`
3. 提交修改：`git commit -m 'Add some feature'`
4. 推送到分支：`git push origin feature/your-feature`
5. 提交 Pull Request

### 代码规范

- 使用Python 3.7+语法
- 遵循PEP 8编码规范
- 添加必要的类型注解
- 编写清晰的注释说明

## 许可证

本项目采用 MIT 许可证开源，详情请参阅 [LICENSE](LICENSE) 文件。

## 贡献者

感谢以下贡献者的支持：

- 项目作者：ZGIRC Dev Team
- 社区贡献者

## 联系方式

- 项目主页：https://github.com/你的用户名/zgirc-time-sync
- 问题反馈：https://github.com/你的用户名/zgirc-time-sync/issues

---

**Power by ZGIRC Dev Team** | © 2024 ZGIRC
