# 第2章: 系統管理工具

## 目錄
- [文件和目錄操作](#文件和目錄操作)
- [權限管理](#權限管理)
- [進程管理](#進程管理)
- [系統監控](#系統監控)

## 文件和目錄操作

### ls - 列出文件和目錄

```bash
# 基本用法
ls [選項] [路徑]

# 常用選項
ls -l          # 詳細列表
ls -la         # 包含隱藏文件的詳細列表
ls -h          # 人類可讀的文件大小
ls -R          # 遞歸列表（包含子目錄）
ls -t          # 按修改時間排序
ls -S          # 按文件大小排序
ls -r          # 逆序排序

# 實例
ls -lh ~/Documents         # 以 KB/MB 顯示大小
ls -lah                    # 所有文件，詳細信息，人類可讀
ls -lthr                   # 按修改時間逆序排列
```

### cd - 改變目錄

```bash
cd /path/to/dir    # 進入指定目錄
cd ~               # 進入用戶主目錄
cd ..              # 進入父目錄
cd -               # 進入前一個目錄
cd                 # 同 cd ~
```

### pwd - 列印工作目錄

```bash
pwd                # 顯示當前絕對路徑
```

### mkdir - 建立目錄

```bash
mkdir dir_name              # 建立單個目錄
mkdir -p /path/to/dir      # 遞歸建立目錄
mkdir -m 755 dir_name      # 建立目錄並設置權限
```

### cp - 複製文件

```bash
cp source dest              # 複製文件
cp -r source/ dest/        # 遞歸複製目錄
cp -i source dest          # 覆蓋前提示
cp -v source dest          # 詳細模式，顯示進度
cp -a source dest          # 保留屬性和完整複製
```

### mv - 移動或重命名

```bash
mv old_name new_name       # 重命名文件
mv file /path/to/dest      # 移動文件
mv -i source dest          # 交互模式
mv -v source dest          # 詳細模式
```

### rm - 刪除文件

```bash
rm file_name               # 刪除文件
rm -i file_name            # 交互模式（刪除前提示）
rm -r directory/           # 遞歸刪除目錄
rm -f file_name            # 強制刪除（不提示）
rm -rf directory/          # 強制遞歸刪除（危險！）

# ⚠️ 警告：rm -rf / 會刪除整個系統！
```

### find - 搜索文件

```bash
# 基本用法
find [路徑] [條件] [動作]

# 常用選項
find . -name "*.txt"                # 按名稱搜索
find . -type f                      # 搜索普通文件
find . -type d                      # 搜索目錄
find . -size +10M                   # 搜索大於 10MB 的文件
find . -mtime -7                    # 修改時間在7天內的文件
find . -perm 644                    # 按權限搜索
find . -name "*.log" -delete        # 搜索並刪除
find . -name "*.py" -exec cat {} \; # 搜索並執行命令

# 實例
find ~ -type f -name "*.pdf"        # 查找主目錄下所有 PDF
find /var/log -type f -mtime +30    # 查找30天前的日誌文件
```

## 權限管理

### chmod - 改變文件權限

```bash
# 符號模式
chmod u+x file              # 為所有者添加執行權限
chmod g+w file              # 為所有者組添加寫權限
chmod o-r file              # 為其他用戶移除讀權限
chmod a+r file              # 為所有人添加讀權限
chmod u=rwx,g=rx,o= file   # 設置完整權限

# 數字模式
chmod 755 file              # rwxr-xr-x
chmod 644 file              # rw-r--r--
chmod 700 file              # rwx------

# 遞歸改變
chmod -R 755 directory/     # 遞歸改變目錄及文件權限
chmod -c 755 file           # 顯示改變的文件
```

### chown - 改變所有者

```bash
chown user file             # 改變文件所有者
chown user:group file       # 同時改變所有者和組
chown -R user directory/    # 遞歸改變
chown -c user file          # 顯示改變的文件
```

### chgrp - 改變組

```bash
chgrp group file            # 改變文件組
chgrp -R group directory/   # 遞歸改變
```

## 進程管理

### ps - 列出進程

```bash
ps                          # 當前 Shell 的進程
ps aux                      # 所有進程詳細信息
ps -ef                      # 所有進程完整格式
ps -u username              # 特定用戶的進程
ps -C command_name          # 特定命令的進程

# 實例
ps aux | grep python        # 查找所有 Python 進程
ps -ef --forest             # 以樹形顯示進程關係
```

### kill - 終止進程

```bash
kill PID                    # 正常終止進程
kill -9 PID                 # 強制終止進程
kill -TERM PID              # 溫和地終止進程
killall process_name        # 終止所有同名進程
```

### top - 系統實時監控

```bash
top                         # 進入交互式實時監控
top -u username             # 特定用戶的進程
top -n 1                    # 只運行一次

# 在 top 中的常用快捷鍵
q                          # 退出
1                          # 顯示多個 CPU 核心
k                          # 終止進程
r                          # 改變優先級
```

### bg/fg - 後台和前台進程

```bash
# 後台運行命令
command &

# 列出後台進程
jobs

# 切換到前台
fg %1                       # 將後台進程 1 切到前台
bg %1                       # 將前台進程切到後台（Ctrl+Z 後）
```

## 系統監控

### df - 磁盤空間使用情況

```bash
df                          # 顯示所有文件系統
df -h                       # 人類可讀格式
df -T                       # 顯示文件系統類型
df -i                       # 顯示 inode 使用情況
df /path/to/check           # 檢查特定路徑所在文件系統
```

### du - 目錄使用空間

```bash
du directory                # 顯示目錄大小
du -h directory             # 人類可讀格式
du -s directory             # 只顯示總和
du -sh *                    # 當前目錄各項大小
du -sh /* | sort -rh        # 按大小排序（largest first）
```

### free - 內存使用情況

```bash
free                        # 顯示內存使用（以 bytes）
free -h                     # 人類可讀格式
free -m                     # 以 MB 顯示
free -g                     # 以 GB 顯示
free -t                     # 顯示總計
```

### vmstat - 虛擬內存統計

```bash
vmstat                      # 顯示一次統計
vmstat 1 5                  # 每秒統計一次，共5次
vmstat -s                   # 詳細統計信息
```

### iostat - I/O 統計

```bash
iostat                      # 需要安裝 sysstat 包
iostat -x 1 5               # 擴展信息，每秒一次，共5次
```

### systemctl - 服務管理

```bash
systemctl status service    # 查看服務狀態
systemctl start service     # 啟動服務
systemctl stop service      # 停止服務
systemctl restart service   # 重啟服務
systemctl enable service    # 設置開機自啟
systemctl disable service   # 禁用開機自啟
systemctl list-units --type service  # 列出所有服務

# 實例
systemctl status ssh        # 查看 SSH 服務狀態
systemctl restart nginx     # 重啟 Nginx
```

### journalctl - 查看系統日誌

```bash
journalctl                  # 查看所有日誌
journalctl -n 20            # 查看最後20行
journalctl -u service       # 查看特定服務的日誌
journalctl -f               # 實時跟蹤日誌
journalctl --since "2026-05-01"  # 查看特定日期之後的日誌
journalctl -p err           # 查看錯誤級別的日誌
```

## 常用工作流程

### 監控系統性能

```bash
# 方案1：使用 top
top -u user_name

# 方案2：組合命令
watch -n 1 'free -h && echo "---" && df -h'

# 方案3：詳細分析
ps aux | sort -nrk 3,3 | head -n 10  # CPU 使用最多的10個進程
ps aux | sort -nrk 4,4 | head -n 10  # 內存使用最多的10個進程
```

### 查找大文件

```bash
find / -type f -size +100M -exec ls -lh {} \;
du -sh /* | sort -rh | head -20
find ~/Documents -type f -size +50M
```

---

**上一章**: [基礎概念](01-basics.md) | **下一章**: [文本處理工具](03-text-tools.md)
