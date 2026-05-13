# 第4章: 網絡工具

## 目錄
- [SSH - 遠程連接](#ssh---遠程連接)
- [curl 和 wget - 下載工具](#curl-和-wget---下載工具)
- [網絡診斷](#網絡診斷)
- [防火牆和連接](#防火牆和連接)

## SSH - 遠程連接

### 基本連接

```bash
ssh user@host               # 基本連接
ssh -p 2222 user@host      # 指定端口
ssh -i ~/.ssh/key user@host    # 使用特定密鑰

# 更詳細的信息
ssh -v user@host            # 詳細模式
ssh -vvv user@host          # 超級詳細模式
```

### 密鑰認證設置

```bash
# 生成 SSH 密鑰對
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""

# 其他密鑰類型
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519

# 複製公鑰到遠程服務器
ssh-copy-id -i ~/.ssh/id_rsa.pub user@host
# 或手動複製
cat ~/.ssh/id_rsa.pub | ssh user@host "cat >> ~/.ssh/authorized_keys"

# 設置正確的權限
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
```

### SSH 配置文件

```bash
# 編輯 ~/.ssh/config
nano ~/.ssh/config

# 配置示例
Host myserver
    HostName 192.168.1.100
    User myuser
    IdentityFile ~/.ssh/id_rsa
    Port 22

Host dev_server
    HostName dev.example.com
    User developer
    Port 2222
    IdentityFile ~/.ssh/dev_key

# 然後直接使用配置中的別名
ssh myserver
ssh dev_server
```

### 高級 SSH 用法

```bash
# 執行遠程命令
ssh user@host 'command'
ssh user@host 'ps aux | grep python'

# 端口轉發（本地轉發）
ssh -L 8080:localhost:3000 user@host    # 本地8080→遠程3000

# 端口轉發（遠程轉發）
ssh -R 9000:localhost:8080 user@host    # 遠程9000←本地8080

# SOCKS 代理
ssh -D 1080 user@host                   # 本地1080作為代理

# 後台運行
ssh -N -f user@host -L 8080:localhost:3000

# 傳輸文件
scp file.txt user@host:/path/to/
scp user@host:/path/to/file.txt ~/
scp -r directory user@host:/path/to/    # 遞歸複製目錄
```

### SSH 故障排除

```bash
# 檢查 SSH 服務狀態
systemctl status ssh

# 重啟 SSH 服務
sudo systemctl restart ssh

# 生成主機密鑰
sudo ssh-keygen -A

# 測試連接
ssh -vvv user@host 2>&1 | head -20
```

## curl 和 wget - 下載工具

### curl - 多功能傳輸工具

```bash
# 基本用法
curl URL                           # 顯示頁面內容
curl -o filename URL              # 保存為文件
curl -O URL                       # 使用遠程文件名
curl -L URL                       # 跟隨重定向
curl -i URL                       # 顯示響應頭

# HTTP 方法
curl -X GET URL
curl -X POST URL
curl -X PUT URL
curl -X DELETE URL

# 發送數據
curl -d "param1=value1&param2=value2" URL      # POST 數據
curl -d @file.json URL                         # 從文件讀取 POST 數據
curl -H "Content-Type: application/json" -d '{"key":"value"}' URL

# 設置請求頭
curl -H "Authorization: Bearer token" URL
curl -H "User-Agent: MyApp/1.0" URL
curl -H "X-Custom-Header: value" URL

# 認證
curl -u username:password URL
curl --basic -u username:password URL
curl --digest -u username:password URL

# 高級選項
curl -v URL                       # 詳細模式
curl --trace-ascii dump.txt URL   # 追蹤信息
curl -m 10 URL                    # 超時 10 秒
curl -A "Mozilla/5.0" URL         # 設置 User-Agent
curl -b "cookie.txt" URL          # 使用 Cookie
curl -c "cookie.txt" URL          # 保存 Cookie
curl -x proxy.com:8080 URL        # 使用代理

# 並行下載
curl -o file1.txt URL1 & curl -o file2.txt URL2 & wait
```

### wget - 遞歸下載工具

```bash
# 基本用法
wget URL                          # 下載文件
wget -O filename URL              # 指定輸出文件名
wget -q URL                       # 安靜模式
wget -v URL                       # 詳細模式

# 遞歸下載
wget -r URL                       # 遞歸下載整個網站
wget -r -l 2 URL                  # 限制遞歸深度為 2
wget -r -np URL                   # 不進入父目錄
wget -r -R "*.exe" URL            # 排除特定文件類型

# 下載設置
wget -c URL                       # 繼續未完成的下載
wget -O - URL                     # 輸出到標準輸出
wget --timeout=10 URL             # 超時設置

# 認證和代理
wget --user=username --password=password URL
wget -e http_proxy=proxy:8080 URL

# 其他選項
wget -U "Mozilla/5.0" URL         # 設置 User-Agent
wget -b URL                       # 後台下載
wget -i urls.txt                  # 從文件讀取 URL 列表
wget --limit-rate=100k URL        # 限制速度
```

## 網絡診斷

### ping - 測試連接

```bash
ping host                         # 持續 ping
ping -c 5 host                    # ping 5 次後停止
ping -i 2 host                    # 每2秒發送一次
ping -t 3 host                    # TTL 為 3

# 實例
ping -c 3 8.8.8.8                # 測試到 Google DNS
ping -c 3 -W 1000 host           # 1秒超時
```

### traceroute - 跟蹤路由

```bash
traceroute host                   # 基本用法
traceroute -m 15 host             # 最多15跳
traceroute -w 3 host              # 3秒超時
traceroute -I host                # 使用 ICMP
traceroute -T host                # 使用 TCP
traceroute -U host                # 使用 UDP（默認）

# macOS 上是 traceroute
# 部分 Linux 可能需要 traceroute 或 tracepath
tracepath host
```

### nslookup 和 dig - DNS 查詢

```bash
# nslookup
nslookup example.com              # 正向查詢
nslookup 8.8.8.8                  # 反向查詢
nslookup example.com 8.8.8.8      # 使用特定 DNS 服務器

# dig（推薦）
dig example.com                   # 基本查詢
dig example.com A                 # 查詢 A 記錄
dig example.com MX                # 查詢 MX 記錄
dig example.com NS                # 查詢 NS 記錄
dig example.com TXT               # 查詢 TXT 記錄
dig @8.8.8.8 example.com          # 使用特定 DNS 服務器
dig +short example.com            # 簡潔輸出
dig +trace example.com            # 跟蹤完整查詢路徑
```

### netstat - 網絡統計

```bash
netstat                           # 顯示所有連接
netstat -a                        # 所有連接（包括監聽）
netstat -i                        # 顯示網卡統計
netstat -s                        # 協議統計
netstat -r                        # 顯示路由表

# 常用選項
netstat -an                       # 數字格式，不反向解析
netstat -ant                      # TCP 連接
netstat -anup                     # UDP 連接
netstat -tlnp                     # 監聽的 TCP 端口
netstat -tulnp                    # 所有監聽的端口

# 查看特定進程
netstat -anp | grep :8080         # 查看占用 8080 端口的進程

# 現代替代品：ss
ss -a                             # 所有 socket
ss -l                             # 監聽 socket
ss -tlnp                          # 監聽的 TCP 端口
```

### ifconfig 和 ip - 網絡配置

```bash
# ifconfig（傳統，某些系統已棄用）
ifconfig                          # 顯示所有網卡
ifconfig eth0                     # 顯示特定網卡
ifconfig eth0 192.168.1.100       # 配置 IP 地址

# ip command（推薦）
ip addr                           # 顯示 IP 地址
ip addr show eth0                 # 顯示特定網卡
ip route                          # 顯示路由表
ip link                           # 顯示鏈路層信息

# 配置網絡
sudo ip addr add 192.168.1.100/24 dev eth0   # 添加 IP
sudo ip route add default via 192.168.1.1    # 添加默認網關
```

### tcpdump - 數據包捕獲

```bash
sudo tcpdump                      # 捕獲所有流量
sudo tcpdump -i eth0              # 捕獲特定網卡
sudo tcpdump -c 10                # 捕獲 10 個包
sudo tcpdump -w capture.pcap      # 保存到文件
sudo tcpdump -r capture.pcap      # 讀取文件
sudo tcpdump -n                   # 不反向解析

# 過濾
sudo tcpdump port 8080            # 特定端口
sudo tcpdump src 192.168.1.100    # 源 IP
sudo tcpdump dst 192.168.1.1      # 目標 IP
sudo tcpdump tcp                  # TCP 流量
sudo tcpdump udp                  # UDP 流量
sudo tcpdump -A                   # 顯示 ASCII 內容
sudo tcpdump -X                   # 顯示十六進制和 ASCII
```

## 防火牆和連接

### 測試端口連接

```bash
# nc（netcat）
nc -zv host 22                    # 測試 SSH 端口
nc -zv -w 3 host 8080             # 測試 Web 端口，3秒超時
nc -l 8080                        # 監聽端口

# telnet
telnet host 22                    # 測試連接
telnet 192.168.1.1 8080           # 測試服務器和端口

# 使用 bash 測試
cat < /dev/null > /dev/tcp/host/port   # 成功返回，失敗報錯
cat < /dev/null > /dev/tcp/192.168.1.1/22
```

### iptables/ufw - 防火牆配置

```bash
# 使用 ufw（簡單的防火牆）
sudo ufw status                   # 查看狀態
sudo ufw enable                   # 啟用防火牆
sudo ufw disable                  # 禁用防火牆
sudo ufw default deny incoming    # 默認拒絕入站
sudo ufw default allow outgoing   # 默認允許出站
sudo ufw allow 22                 # 允許 SSH
sudo ufw allow 80/tcp             # 允許 HTTP
sudo ufw allow 443/tcp            # 允許 HTTPS
sudo ufw deny 8080                # 拒絕 8080 端口
sudo ufw delete allow 22          # 刪除規則

# iptables（更強大）
sudo iptables -L                  # 列出規則
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT    # 允許 SSH
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT    # 允許 HTTP
sudo iptables -D INPUT -p tcp --dport 22 -j ACCEPT    # 刪除規則
sudo iptables-save                # 保存規則
```

## 網絡故障排除工作流程

### 連接診斷

```bash
# 1. 測試本地連接
ping 127.0.0.1

# 2. 測試網關連接
ping $(ip route | grep default | awk '{print $3}')

# 3. 測試外部連接
ping 8.8.8.8

# 4. 查看路由
ip route
traceroute 8.8.8.8

# 5. 檢查 DNS
nslookup example.com
dig example.com
```

### 服務連接檢查

```bash
# 檢查特定服務
netstat -tlnp | grep :22          # SSH
netstat -tlnp | grep :80          # HTTP
netstat -tlnp | grep :443         # HTTPS
netstat -tlnp | grep :3306        # MySQL

# 測試連接
curl http://localhost:8080
curl -I https://example.com       # 只顯示頭部
```

### 性能監控

```bash
# 監控網絡狀態
watch -n 1 "ss -tulnp"
iftop -i eth0                     # 實時帶寬監控

# 查看連接統計
ss -s
netstat -s
```

---

**上一章**: [文本處理工具](03-text-tools.md) | **下一章**: [開發工具](05-dev-tools.md)
