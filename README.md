# ZGIRC时间同步

[![Python 3.7+](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Windows](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

简洁的时间同步工具，支持图形界面、开机自启动和GitHub一键更新。

## 功能特性

- **图形界面**：简洁直观的GUI设计
- **时间同步**：使用阿里云NTP服务器同步时间
- **开机自启动**：支持开机自动运行
- **一键更新**：从GitHub下载并自动替换更新
- **日志管理**：支持保存日志、清理过期日志
- **管理员权限**：自动处理系统时间修改

## 系统要求

- 操作系统：Windows 7/8/10/11
- Python版本：3.7及以上

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

# 打包命令
pyinstaller --onefile --windowed --name "ZGIRC_TimeSync" time.py
```

### 方式三：直接下载EXE

前往[Releases页面](https://github.com/kuangxing4250/zgirc-time-sync/releases)下载预编译的EXE文件。

## 使用说明

### 启动程序

直接运行EXE文件，显示图形界面：

```bash
ZGIRC_TimeSync.exe
```

### 界面功能

1. **立即同步**：点击按钮立即执行时间同步
2. **一键更新**：检查并下载最新版本
3. **开机自启动**：勾选启用系统启动项
4. **保存日志**：勾选是否保存日志文件
5. **清理日志**：一键清理7天前的日志文件
6. **查看日志**：查看最近的运行日志

### 配置文件

程序会自动创建 `config.json` 配置文件：

```json
{
    "auto_check_update": true,
    "save_log": true,
    "log_days": 7
}
```

- `auto_check_update`：启动时自动检查更新
- `save_log`：是否保存日志到文件
- `log_days`：日志保留天数

## 文件结构

```
zgirc-time-sync/
├── time.py              # 主程序文件
├── README.md            # 项目说明
├── LICENSE              # 开源协议
└── 运行时生成/
    ├── ZGIRC_TimeSync.exe   # 主程序EXE
    ├── log/                  # 日志目录
    └── config.json           # 配置文件
```

## 更新日志

### v0.0.2-beta.0（当前版本）

- 改用阿里云NTP服务器同步时间
- 从GitHub主分支下载更新，支持加速网站
- 使用批处理脚本更新，解决文件占用问题
- 添加中文注释，代码更易读

### v0.0.1-beta.0

- 初始测试版本
- 基础时间同步功能
- 图形界面

## 技术说明

### 时间服务器

程序使用阿里云NTP服务器：

- time1.aliyun.com ~ time6.aliyun.com
- ntp1.aliyun.com ~ ntp2.aliyun.com

### 更新机制

1. 从GitHub下载最新EXE文件（支持加速网站）
2. 保存为 `time_new.exe`
3. 创建更新脚本 `update.bat`
4. 程序自动退出
5. 批处理脚本执行：删除旧EXE，移动新EXE，启动程序
6. 清理更新脚本

### 下载地址

- **加速网站**：`https://gh.jasonzeng.dev/github.com/kuangxing4250/zgirc-time-sync/blob/main/dist/ZGIRC_TimeSync.exe`
- **GitHub直连**：`https://raw.githubusercontent.com/kuangxing4250/zgirc-time-sync/main/dist/ZGIRC_TimeSync.exe`

## 常见问题

### Q: 提示需要管理员权限？

A: 请右键点击程序，选择"以管理员身份运行"。

### Q: 如何退出程序？

A: 点击界面上的"退出"按钮，或在任务管理器中结束进程。

### Q: 如何查看详细日志？

A: 点击界面上的"查看日志"按钮，或直接查看程序同级目录下的 `log/` 目录。

### Q: 同步失败怎么办？

A: 请检查：
1. 网络连接是否正常
2. 防火墙是否阻止了NTP服务器访问（UDP端口123）
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
- 添加中文注释说明

### 发布新版本

1. 修改 `time.py` 中的 `VERSION` 版本号
2. 打包EXE：`pyinstaller --onefile --windowed --name "ZGIRC_TimeSync" time.py`
3. 将 `dist/ZGIRC_TimeSync.exe` 上传到GitHub `dist/` 目录
4. 提交代码并打标签

## 许可证

本项目采用 MIT 许可证开源。

## 联系方式

- 项目主页：https://github.com/kuangxing4250/zgirc-time-sync
- 问题反馈：https://github.com/kuangxing4250/zgirc-time-sync/issues

---

**Powered by kuangxing4250** | © 2024 ZGIRC
