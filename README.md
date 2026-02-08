# ZGIRC时间同步

[![Python 3.7+](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Windows](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

简洁的时间同步工具，支持图形界面、开机自启动和一键更新。

## 功能特性

- **图形界面**：简洁直观的GUI设计
- **时间同步**：使用阿里云NTP服务器同步时间
- **开机自启动**：支持开机自动运行
- **一键更新**：自动下载并替换最新版本
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
# 运行EXE
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

### v4.2（当前版本）

- 移除每小时自动同步功能
- 改用阿里云NTP服务器同步时间
- 重写更新机制，直接下载并替换主程序EXE
- 优化日志保存位置到程序同级目录
- 添加中文注释，代码更易读
- 修复多处Bug

### v4.1

- 全新GUI界面设计
- 支持前台/后台双模式运行
- 新增开机自启动管理
- 新增一键更新功能
- 改进日志系统

## 技术说明

### 时间服务器

程序使用阿里云NTP服务器：

- time1.aliyun.com ~ time6.aliyun.com
- ntp1.aliyun.com ~ ntp2.aliyun.com

### 更新机制

1. 从更新服务器下载最新EXE文件
2. 保存为 `time_new.exe`
3. 备份当前EXE为 `time_old.exe`
4. 替换主程序文件
5. 3秒后自动重启

更新服务器：`http://time.zgric.top/update/lastupdate_time.exe`

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

## 许可证

本项目采用 MIT 许可证开源。

## 联系方式

- 项目主页：https://github.com/kuangxing4250/zgirc-time-sync
- 问题反馈：https://github.com/kuangxing4250/zgirc-time-sync/issues

---

**Powered by kuangxing4250** | © 2024 ZGIRC
