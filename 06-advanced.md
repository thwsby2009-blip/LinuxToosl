# 第6章: 進階技巧

## 目錄
- [Shell 腳本編寫](#shell-腳本編寫)
- [性能優化](#性能優化)
- [系統調優](#系統調優)
- [自動化和計畫任務](#自動化和計畫任務)

## Shell 腳本編寫

### 基本結構

```bash
#!/bin/bash
# 腳本說明

# 設置錯誤處理
set -euo pipefail

# 常量定義
readonly CONFIG_FILE="/etc/app.conf"
readonly LOG_FILE="/var/log/app.log"

# 函數定義
function print_usage() {
    echo "Usage: $0 [options]"
    exit 1
}

# 主程序
main() {
    # 主邏輯
    echo "程序開始"
}

# 腳本入口
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
```

### 變量和數據類型

```bash
# 變量定義
NAME="value"                      # 字符串
COUNT=10                          # 數字
ARRAY=(1 2 3 4 5)               # 數組
ARRAY[0]=1

# 字符串操作
${VAR}                            # 展開變量
${VAR:0:5}                        # 子字符串
${VAR#pattern}                    # 刪除前綴
${VAR%pattern}                    # 刪除後綴
${VAR/old/new}                    # 替換
${VAR^^}                          # 轉為大寫
${VAR,,}                          # 轉為小寫
${VAR:-default}                   # 默認值

# 數組操作
${ARRAY[@]}                       # 所有元素
${ARRAY[0]}                       # 第一個元素
${#ARRAY[@]}                      # 數組長度
${ARRAY[@]:1:3}                   # 子數組

# 字典操作（關聯數組）
declare -A dict
dict[key]="value"
${dict[key]}
```

### 條件判斷

```bash
# if 語句
if [[ condition ]]; then
    # code
elif [[ condition ]]; then
    # code
else
    # code
fi

# 條件表達式
[[ -f file ]]                     # 文件存在且是普通文件
[[ -d directory ]]                # 目錄存在
[[ -x file ]]                     # 文件可執行
[[ -r file ]]                     # 文件可讀
[[ -w file ]]                     # 文件可寫
[[ -s file ]]                     # 文件非空
[[ -z string ]]                   # 字符串為空
[[ -n string ]]                   # 字符串非空
[[ $a == $b ]]                    # 字符串相等
[[ $a != $b ]]                    # 字符串不相等
[[ $a -eq $b ]]                   # 數字相等
[[ $a -ne $b ]]                   # 數字不相等
[[ $a -lt $b ]]                   # 小於
[[ $a -gt $b ]]                   # 大於
[[ $a -le $b ]]                   # 小於等於
[[ $a -ge $b ]]                   # 大於等於
[[ condition1 && condition2 ]]    # AND
[[ condition1 || condition2 ]]    # OR
[[ !condition ]]                  # NOT

# case 語句
case "$variable" in
    pattern1)
        # code
        ;;
    pattern2)
        # code
        ;;
    *)
        # 默認情況
        ;;
esac
```

### 循環

```bash
# for 循環
for i in 1 2 3 4 5; do
    echo $i
done

# for 循環（C 風格）
for ((i=0; i<10; i++)); do
    echo $i
done

# while 循環
while [[ $i -lt 10 ]]; do
    echo $i
    ((i++))
done

# until 循環
until [[ $i -ge 10 ]]; do
    echo $i
    ((i++))
done

# 遍歷文件
for file in *.txt; do
    echo "Processing $file"
done

# 遍歷目錄
for dir in */; do
    echo "Directory: $dir"
done
```

### 函數和參數

```bash
# 函數定義
function greet() {
    local name="$1"               # 第一個參數
    local greeting="$2"           # 第二個參數
    echo "$greeting, $name"
}

# 函數調用
greet "Alice" "Hello"

# 參數處理
function process_args() {
    echo "所有參數: $@"
    echo "參數個數: $#"
    echo "腳本名: $0"
    echo "第一個: $1"
    echo "第二個: $2"
}

# 帶返回值的函數
function add() {
    local result=$(($1 + $2))
    return $result
}
add 5 3
echo $?

# 參數驗證
function safe_func() {
    [[ $# -ne 2 ]] && { echo "需要2個參數"; return 1; }
    # 繼續處理
}
```

### 實例腳本

```bash
#!/bin/bash
# 備份腳本示例

set -euo pipefail

# 配置
BACKUP_DIR="/backup"
SOURCE_DIR="/data"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/backup_${DATE}.tar.gz"
LOG_FILE="/var/log/backup.log"

# 日誌函數
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

# 檢查目錄
check_requirements() {
    [[ ! -d "$SOURCE_DIR" ]] && { log "ERROR: 源目錄不存在"; exit 1; }
    [[ ! -d "$BACKUP_DIR" ]] && mkdir -p "$BACKUP_DIR"
}

# 執行備份
perform_backup() {
    log "開始備份 $SOURCE_DIR"
    if tar -czf "$BACKUP_FILE" -C "$(dirname "$SOURCE_DIR")" "$(basename "$SOURCE_DIR")"; then
        log "備份完成: $BACKUP_FILE"
        log "文件大小: $(du -h "$BACKUP_FILE" | cut -f1)"
    else
        log "ERROR: 備份失敗"
        return 1
    fi
}

# 清理舊備份
cleanup_old_backups() {
    local retention_days=7
    log "清理 $retention_days 天前的備份"
    find "$BACKUP_DIR" -name "backup_*.tar.gz" -mtime +${retention_days} -delete
}

# 主程序
main() {
    log "備份腳本開始"
    check_requirements
    perform_backup
    cleanup_old_backups
    log "備份腳本完成"
}

main "$@"
```

## 性能優化

### 系統性能分析

```bash
# CPU 分析
top                               # 實時 CPU 使用
vmstat 1 5                        # CPU 和內存統計
mpstat -P ALL 1 5                 # 多核 CPU 分析
pidstat -p PID 1 5                # 特定進程分析

# 內存分析
free -h                           # 內存使用
smem -s rss -r                    # 詳細內存統計
ps aux --sort=-%mem | head -10    # 內存使用最多的進程

# I/O 分析
iostat -x 1 5                     # I/O 統計
iotop                             # I/O 使用排序
dstat -ts --disk --net 1          # 綜合統計

# 網絡分析
iftop -i eth0                     # 帶寬使用
nethogs                           # 進程級帶寬統計
ss -s                             # Socket 統計
```

### 優化建議

```bash
# 1. 找出瓶頸進程
ps aux --sort=-%mem | head -5     # 內存消耗
ps aux --sort=-%cpu | head -5     # CPU 消耗

# 2. 使用 nice 調整優先級
nice -n 10 ./slow_program         # 降低優先級
renice -n -5 -p PID               # 提高已運行進程優先級

# 3. 批量操作優化
# 使用 xargs 並行處理
find . -name "*.log" | xargs -P 4 gzip

# 4. 編譯優化
gcc -O3 -march=native program.c   # 最高優化和本機優化
```

## 系統調優

### 核心參數調優

```bash
# 查看當前值
sysctl -a                         # 列出所有
sysctl net.ipv4.tcp_max_syn_backlog

# 臨時修改（重啟後失效）
sudo sysctl -w net.ipv4.ip_forward=1

# 永久修改（編輯 /etc/sysctl.conf）
echo "net.ipv4.ip_forward = 1" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p                    # 應用配置

# 常用調優參數
cat >> /etc/sysctl.conf << EOF
# 網絡調優
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_tw_recycle = 0
net.ipv4.tcp_keepalive_time = 600
net.ipv4.tcp_max_syn_backlog = 8096
net.core.somaxconn = 1024

# 文件描述符
fs.file-max = 2097152
EOF
```

### 限制設置

```bash
# 查看當前限制
ulimit -a

# 修改限制（臨時）
ulimit -n 65536                   # 打開文件數
ulimit -u 4096                    # 用戶進程數
ulimit -s unlimited               # 棧大小

# 永久修改（編輯 /etc/security/limits.conf）
echo "* soft nofile 65536" | sudo tee -a /etc/security/limits.conf
echo "* hard nofile 65536" | sudo tee -a /etc/security/limits.conf
echo "* soft nproc 4096" | sudo tee -a /etc/security/limits.conf
echo "* hard nproc 4096" | sudo tee -a /etc/security/limits.conf
```

### 磁盤性能

```bash
# 測試磁盤速度
dd if=/dev/zero of=test.img bs=1M count=1000
# 計算速度 = 1000MB / 耗時

# 測試隨機 I/O
fio --name=randread --ioengine=libaio --iodepth=16 \
    --rw=randread --bs=4k --direct=1 --size=1G --numjobs=4

# 查看磁盤使用
df -h                             # 文件系統使用
du -sh *                          # 目錄大小
lsblk                             # 磁盤分區

# 監控實時 I/O
dstat --disk --top-bio 1
```

## 自動化和計畫任務

### cron - 定時任務

```bash
# 編輯 crontab
crontab -e                        # 編輯當前用戶 crontab
crontab -e -u username            # 編輯特定用戶（root）

# 查看 crontab
crontab -l                        # 列出當前用戶
crontab -u username -l            # 列出特定用戶

# 刪除 crontab
crontab -r                        # 刪除當前用戶

# Crontab 語法
# 分 時 日 月 週 命令
# 分: 0-59
# 時: 0-23
# 日: 1-31
# 月: 1-12
# 週: 0-6 (0=周日)

# 示例
0 2 * * * /script/backup.sh       # 每天 2:00 執行
30 * * * * /script/check.sh       # 每小時 30 分執行
0 0 * * 0 /script/weekly.sh       # 每週日 0:00 執行
*/5 * * * * /script/heartbeat.sh  # 每 5 分鐘執行
0 9 1 * * /script/monthly.sh      # 每月 1 日 9:00 執行

# Crontab 重定向
0 2 * * * /script/backup.sh > /var/log/backup.log 2>&1

# 系統級 crontab
# 編輯: /etc/cron.d/
# 格式多一列：分 時 日 月 週 用戶 命令
0 2 * * * root /script/backup.sh
```

### systemd timer - 現代定時任務

```bash
# 創建 timer 文件
cat > /etc/systemd/system/myapp.service << EOF
[Unit]
Description=My Application
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/myapp
EOF

cat > /etc/systemd/system/myapp.timer << EOF
[Unit]
Description=My Application Timer
Requires=myapp.service

[Timer]
OnBootSec=5min
OnUnitActiveSec=1h
Persistent=true

[Install]
WantedBy=timers.target
EOF

# 啟用 timer
sudo systemctl daemon-reload
sudo systemctl enable myapp.timer
sudo systemctl start myapp.timer
sudo systemctl status myapp.timer

# 查看 timer 狀態
sudo systemctl list-timers
sudo systemctl list-timers --all
```

### at - 一次性任務

```bash
# 計畫一次性任務
at 14:30 tomorrow               # 明天 14:30
at 2:30 PM next Friday          # 下週五下午 2:30
at now + 2 hours               # 2小時後

# 輸入命令後按 Ctrl+D
echo "/script/backup.sh" | at 2:00 AM tomorrow

# 查看計畫任務
atq                             # 列出任務
at -l                           # 同上

# 刪除任務
atrm job_id                    # 刪除特定任務
```

### 監控和告警

```bash
# 監控系統資源
#!/bin/bash
# 如果 CPU 使用率超過 80%，發送告警

CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print int($2)}')
THRESHOLD=80

if [[ $CPU_USAGE -gt $THRESHOLD ]]; then
    echo "CPU 使用率過高: ${CPU_USAGE}%" | mail -s "告警" admin@example.com
fi

# 定期檢查服務
#!/bin/bash
# 檢查服務是否運行

SERVICE="nginx"
if ! systemctl is-active --quiet $SERVICE; then
    echo "$SERVICE 已停止，正在重啟..."
    sudo systemctl restart $SERVICE
    echo "$SERVICE 已重啟" | mail -s "服務告警" admin@example.com
fi
```

## 常用最佳實踐

### 系統監控清單

```bash
# 每日檢查
df -h                             # 磁盤空間
free -h                           # 內存
uptime                            # 運行時間和負載
systemctl status                  # 系統狀態
journalctl -n 50                  # 最後50條日誌

# 定期檢查
ps aux | sort -nrk 3,3 | head     # 高 CPU 進程
ps aux | sort -nrk 4,4 | head     # 高內存進程
netstat -an | grep ESTABLISHED | wc -l  # 連接數
```

### 備份策略

```bash
#!/bin/bash
# 完整備份策略

BACKUP_ROOT="/backup"
SOURCE="/data"
RETENTION_DAYS=30

# 完整備份（每週一）
if [[ $(date +%u) -eq 1 ]]; then
    tar -czf ${BACKUP_ROOT}/full_$(date +%Y%m%d).tar.gz $SOURCE
fi

# 增量備份（每天）
tar -czf ${BACKUP_ROOT}/incr_$(date +%Y%m%d).tar.gz \
    --newer-mtime ${BACKUP_ROOT}/.last_backup $SOURCE
touch ${BACKUP_ROOT}/.last_backup

# 清理舊備份
find ${BACKUP_ROOT} -name "*.tar.gz" -mtime +${RETENTION_DAYS} -delete
```

---

**上一章**: [開發工具](05-dev-tools.md)

## 下一步

- 持續學習和實踐
- 關注安全最佳實踐
- 探索 Kubernetes、雲計算等進階主題
- 貢獻回饋社區知識
