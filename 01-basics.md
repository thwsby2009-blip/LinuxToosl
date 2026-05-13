# 第1章: 基礎概念

## 目錄
- [Linux 文件系統](#linux-文件系統)
- [Shell 基礎](#shell-基礎)
- [用戶和權限](#用戶和權限)
- [環境變量](#環境變量)

## Linux 文件系統

### 文件系統層次結構

```
/
├── bin/          # 基本命令
├── boot/         # 啟動文件
├── dev/          # 設備文件
├── etc/          # 配置文件
├── home/         # 用戶主目錄
├── lib/          # 系統庫
├── media/        # 移動媒體
├── mnt/          # 臨時掛載點
├── opt/          # 可選軟件
├── proc/         # 進程信息
├── root/         # root 用戶主目錄
├── run/          # 運行時數據
├── srv/          # 服務數據
├── sys/          # 系統信息
├── tmp/          # 臨時文件
├── usr/          # 用戶程序和數據
└── var/          # 可變數據
```

### 重要目錄說明

| 目錄 | 用途 |
|------|------|
| `/home` | 普通用戶的主目錄 |
| `/root` | root 用戶的主目錄 |
| `/etc` | 系統配置文件 |
| `/var/log` | 系統日誌文件 |
| `/tmp` | 臨時文件，重啟後清空 |
| `/opt` | 第三方應用程序 |

## Shell 基礎

### 什麼是 Shell？

Shell 是與操作系統內核交互的命令解釋器。常見的 Shell：

- **bash** - GNU Bourne Again Shell（最常用）
- **sh** - Bourne Shell
- **zsh** - 功能豐富的 Shell
- **fish** - 友好的交互式 Shell

### 基本命令結構

```bash
command [options] [arguments]
```

### 常用快捷鍵

| 快捷鍵 | 功能 |
|--------|------|
| `Ctrl+C` | 中斷當前命令 |
| `Ctrl+D` | 退出 Shell |
| `Ctrl+L` | 清空屏幕 |
| `Ctrl+A` | 游標移到行首 |
| `Ctrl+E` | 游標移到行尾 |
| `Tab` | 命令補全 |

### 重定向和管道

```bash
# 重定向標準輸出到文件
command > file.txt

# 追加到文件
command >> file.txt

# 重定向標準錯誤
command 2> error.txt

# 重定向標準輸出和標準錯誤
command &> output.txt

# 管道：將一個命令的輸出作為另一個的輸入
command1 | command2
```

## 用戶和權限

### 用戶類型

- **root** - 超級用戶，UID 為 0，擁有所有權限
- **系統用戶** - 用於運行特定服務，通常 UID < 1000
- **普通用戶** - 普通用戶，通常 UID >= 1000

### 權限基礎

```bash
-rw-r--r-- 1 user group 1024 May 1 10:00 file.txt
```

分解說明：
- 第一個字符：文件類型（`-` 普通文件，`d` 目錄，`l` 符號鏈接）
- 接下來三個字符：所有者權限（`r` 讀，`w` 寫，`x` 執行）
- 中間三個字符：所有者組的權限
- 最後三個字符：其他用戶的權限

### 權限數字表示

```
r (讀)    = 4
w (寫)    = 2
x (執行)  = 1

755 = rwxr-xr-x  # 所有者完全權限，其他用戶只讀執行
644 = rw-r--r--  # 所有者可讀寫，其他用戶只讀
700 = rwx------  # 只有所有者有完全權限
```

## 環境變量

### 常見系統環境變量

| 變量 | 說明 |
|------|------|
| `PATH` | 命令搜索路徑 |
| `HOME` | 用戶主目錄 |
| `USER` | 當前用戶名 |
| `SHELL` | 當前使用的 shell |
| `PWD` | 當前工作目錄 |
| `LANG` | 系統語言和字符集 |
| `LOGNAME` | 登錄用戶名 |

### 查看和設置環境變量

```bash
# 查看所有環境變量
env
printenv

# 查看特定環境變量
echo $PATH
echo $HOME

# 設置環境變量（僅當前 Shell 會話）
export MYVAR="value"

# 永久設置環境變量
# 編輯 ~/.bashrc 或 ~/.bash_profile 文件
echo 'export MYVAR="value"' >> ~/.bashrc
source ~/.bashrc
```

---

**下一章**: [系統管理工具](02-system-tools.md)
