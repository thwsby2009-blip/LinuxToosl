# 第7章: 高級主題

## 目錄
- [系統內核優化](#系統內核優化)
- [系統安全加固](#系統安全加固)
- [高性能網絡優化](#高性能網絡優化)
- [容器編排和 Kubernetes](#容器編排和-kubernetes)
- [系統故障排查](#系統故障排查)
- [虛擬化技術](#虛擬化技術)

## 系統內核優化

### 編譯自定義內核

```bash
# 下載內核源碼
wget https://www.kernel.org/pub/linux/kernel/v6.x/linux-6.1.tar.xz
tar -xf linux-6.1.tar.xz
cd linux-6.1

# 獲取當前內核配置
zcat /proc/config.gz > .config
# 或複製現有配置
cp /boot/config-$(uname -r) .config

# 配置內核
make menuconfig          # 交互式配置
make config              # 逐項詢問
make defconfig           # 使用默認配置
make localmodconfig      # 僅編譯加載的模塊

# 編譯內核
make -j$(nproc)          # 使用所有 CPU 核心並行編譯
make modules             # 編譯模塊
sudo make modules_install    # 安裝模塊
sudo make install        # 安裝內核

# 生成 initramfs
sudo mkinitramfs -o /boot/initrd.img-6.1 6.1

# 更新 GRUB
sudo update-grub

# 重啟
sudo reboot
```

### 內核模塊管理

```bash
# 查看加載的模塊
lsmod                    # 列出模塊
lsmod | grep module_name # 查找特定模塊
modinfo module_name      # 模塊信息

# 加載和卸載模塊
sudo modprobe module_name           # 加載模塊及依賴
sudo modprobe -r module_name        # 卸載模塊
sudo insmod /path/to/module.ko      # 直接加載模塊

# 模塊參數
modinfo -p module_name              # 查看可用參數
sudo modprobe module_name param=value   # 帶參數加載

# 永久加載模塊
echo "module_name" | sudo tee /etc/modules-load.d/custom.conf
sudo modprobe -r module_name
sudo modprobe module_name

# 禁用模塊
echo "blacklist module_name" | sudo tee /etc/modprobe.d/blacklist.conf
```

### 性能調優參數

```bash
# CPU 調頻和電源管理
cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_driver    # 查看當前驅動
cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor  # 查看 governor

# 設置 governor
echo "performance" | sudo tee /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
# 或使用 cpupower
sudo cpupower frequency-set -g performance

# CPU 隔離
# 編輯 /etc/default/grub
# GRUB_CMDLINE_LINUX="isolcpus=1,2,3 nohz_full=1,2,3"
sudo update-grub
sudo reboot

# 查看隔離狀態
cat /proc/cmdline | grep isolcpus
```

## 系統安全加固

### SELinux 和 AppArmor

```bash
# SELinux（Red Hat 系列）
getenforce              # 查看當前模式
setstatus              # 詳細狀態

# 修改 SELinux 模式
sudo semanage permissive -a httpd_t    # 設置寬容模式
sudo semanage permissive -d httpd_t    # 移除寬容設置
sudo semanage boolean -l | grep httpd  # 查看 httpd 相關 boolean

# 生成 SELinux 策略
sudo audit2allow -a -M custom_policy   # 根據 audit 日誌生成策略
sudo semodule -i custom_policy.pp

# AppArmor（Ubuntu 系列）
sudo aa-status                         # 查看狀態
sudo aa-enforce /etc/apparmor.d/profile_name    # 啟用配置
sudo aa-complain /etc/apparmor.d/profile_name   # 寬容模式
sudo aa-disable /etc/apparmor.d/profile_name    # 禁用配置

# 審計日誌
grep "apparmor" /var/log/syslog | tail -20
```

### 審計和日誌監控

```bash
# auditd - 內核審計
sudo auditctl -l                      # 列出當前規則
sudo auditctl -w /etc/passwd -p wa -k passwd_changes
sudo auditctl -a always,exit -F arch=b64 -S open,openat -F uid=1000 -k user_opens

# 查看審計日誌
sudo ausearch -k passwd_changes       # 查看特定日誌
sudo aureport -u                      # 用戶活動報告
sudo aureport --file                  # 文件訪問報告

# 配置持久化
cat | sudo tee /etc/audit/rules.d/custom.rules << EOF
-w /etc/passwd -p wa -k passwd_changes
-w /etc/shadow -p wa -k shadow_changes
-a always,exit -F arch=b64 -S execve -F uid=0 -k root_commands
EOF

sudo service auditd restart
```

### 加密和密鑰管理

```bash
# 磁盤加密（LUKS）
sudo cryptsetup luksFormat /dev/sda1
sudo cryptsetup luksOpen /dev/sda1 encrypted_volume
sudo mkfs.ext4 /dev/mapper/encrypted_volume
sudo mount /dev/mapper/encrypted_volume /mnt/secure

# 文件加密
gpg --symmetric file.txt              # 對稱加密
gpg --encrypt --recipient user file.txt  # 公鑰加密
gpg file.txt.gpg                      # 解密

# SSH 密鑰加密
ssh-keygen -t ed25519 -N "passphrase" -f ~/.ssh/id_ed25519

# 系統密鑰存儲
sudo keyctl add user mykey "secret" @u   # 添加密鑰
sudo keyctl list @u                      # 列出密鑰
sudo keyctl request user mykey           # 獲取密鑰
```

## 高性能網絡優化

### 網絡棧優化

```bash
# TCP 優化
cat >> /etc/sysctl.conf << EOF
# TCP 優化
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_tw_recycle = 0
net.ipv4.tcp_fin_timeout = 30
net.ipv4.tcp_keepalive_time = 300
net.ipv4.tcp_max_syn_backlog = 8192
net.core.somaxconn = 4096
net.ipv4.ip_local_port_range = 10000 65000
net.ipv4.tcp_max_tw_buckets = 2000000

# 緩衝區優化
net.core.rmem_max = 134217728
net.core.wmem_max = 134217728
net.ipv4.tcp_rmem = 4096 87380 134217728
net.ipv4.tcp_wmem = 4096 65536 134217728

# 連接跟蹤優化
net.netfilter.nf_conntrack_max = 2000000
net.netfilter.nf_conntrack_tcp_timeout_established = 600
EOF

sudo sysctl -p
```

### 網絡監控和分析

```bash
# 實時網絡監控
iftop -i eth0                    # 帶寬監控
nethogs                          # 進程級帶寬
nload -i eth0                    # 簡潔帶寬顯示

# 連接統計和分析
ss -s                            # Socket 統計
ss -M                            # 內存統計
ss -i                            # TCP 信息
ss -tulnp                        # 監聽端口

# 詳細連接分析
ss -aetnp | awk 'NR>1 {print $5}' | cut -d: -f1 | sort | uniq -c | sort -rn

# TCP 連接狀態統計
ss -tan | awk 'NR>1 {print $1}' | sort | uniq -c

# 性能測試
iperf3 -s                        # 服務器模式
iperf3 -c server_ip              # 客戶端模式
iperf3 -c server_ip -R           # 反向測試
iperf3 -c server_ip -P 4         # 4 個並行連接
```

### DPDK 和高性能網絡

```bash
# DPDK 編譯
git clone http://dpdk.org/git/dpdk
cd dpdk
meson build
ninja -C build
sudo ninja -C build install

# 環境設置
export RTE_SDK=/path/to/dpdk
export RTE_TARGET=x86_64-native-linux-gcc

# 預留 hugepages
echo 1024 | sudo tee /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages
sudo mkdir -p /mnt/hugepages
sudo mount -t hugetlbfs nodev /mnt/hugepages

# 綁定網卡到 DPDK
./usertools/dpdk-devbind.py --status
sudo ./usertools/dpdk-devbind.py -b vfio-pci 0000:01:00.0
```

## 容器編排和 Kubernetes

### Kubernetes 基礎操作

```bash
# 集群信息
kubectl cluster-info               # 集群信息
kubectl nodes                      # 查看節點
kubectl get nodes -o wide          # 詳細節點信息
kubectl describe node node_name     # 節點詳情

# Pod 管理
kubectl get pods                   # 列出 Pod
kubectl get pods -o wide           # 詳細信息
kubectl get pods -A                # 所有命名空間
kubectl describe pod pod_name       # Pod 詳情
kubectl logs pod_name              # 查看日誌
kubectl logs -f pod_name           # 實時日誌
kubectl exec -it pod_name bash     # 進入 Pod

# Deployment 管理
kubectl apply -f deployment.yaml    # 創建部署
kubectl set image deployment/myapp myapp=myapp:2.0  # 更新鏡像
kubectl rollout history deployment/myapp   # 版本歷史
kubectl rollout undo deployment/myapp      # 回滾

# Service 和 Ingress
kubectl get services               # 列出服務
kubectl expose pod pod_name --port=8080 --target-port=8000  # 暴露端口
kubectl get ingress                # 列出 Ingress
kubectl apply -f ingress.yaml      # 創建 Ingress

# 資源管理
kubectl top nodes                  # 節點資源使用
kubectl top pods                   # Pod 資源使用
kubectl describe node node_name | grep -A 5 "Allocated resources"
```

### Kubernetes 故障排查

```bash
# 檢查集群健康
kubectl get cs                     # 組件狀態
kubectl get events --all-namespaces --sort-by='.lastTimestamp'  # 事件

# 節點診斷
kubectl debug node/node_name -it --image=ubuntu   # 交互式節點調試

# Pod 診斷
kubectl describe pod pod_name      # 事件和狀態
kubectl logs pod_name              # 應用日誌
kubectl logs pod_name --previous   # 前一個容器日誌（如果崩潰）
kubectl get pod pod_name -o yaml   # 完整配置

# 網絡診斷
kubectl run -it --image=nicolaka/netshoot debug --rm -- bash
# 在 Pod 中執行
ping service_name
nslookup service_name
curl service_name:port

# 資源配額和限制檢查
kubectl get resourcequota --all-namespaces
kubectl describe resourcequota quota_name
```

### Helm - 包管理

```bash
# Helm 基本操作
helm repo add myrepo https://charts.example.com
helm repo update
helm search repo myrepo

# 安裝和管理 Chart
helm install myrelease myrepo/mychart    # 安裝
helm upgrade myrelease myrepo/mychart    # 升級
helm rollback myrelease 1                # 回滾到版本 1
helm uninstall myrelease                 # 卸載
helm list                                # 列出安裝的 release

# 自定義值
helm install myrelease myrepo/mychart -f values.yaml
helm install myrelease myrepo/mychart --set key=value

# 創建自定義 Chart
helm create mychart
helm package mychart                     # 打包
helm template mychart                    # 渲染模板
```

## 系統故障排查

### 性能故障分析

```bash
# 全面性能監控
perf stat ./program                # 性能統計
perf record -p PID                 # 記錄性能數據
perf report                        # 分析性能報告
perf list                          # 查看可用事件

# 火焰圖
perf record -F 99 -p PID -g -- sleep 30
perf script > out.perf
./stackcollapse-perf.pl out.perf > out.folded
./flamegraph.pl out.folded > out.svg

# 具體模塊性能分析
perf top -p PID                    # 實時 CPU 使用函數
perf record -C 0 -g sleep 5        # 特定 CPU 核心分析
```

### 內存泄漏檢測

```bash
# Valgrind 詳細檢查
valgrind --leak-check=full --show-leak-kinds=all \
    --track-origins=yes --verbose ./program

# 查看詳細報告
valgrind --leak-check=full --log-file=valgrind.log ./program
cat valgrind.log

# 特定參數檢查
valgrind --tool=memcheck --track-origins=yes ./program
valgrind --tool=helgrind ./program     # 線程競爭檢查
valgrind --tool=cachegrind ./program   # 緩存分析
```

### I/O 瓶頸分析

```bash
# 磁盤 I/O 分析
iostat -x 1 10                     # 詳細 I/O 統計
iotop -o                           # 只顯示有 I/O 的進程
blktrace -d /dev/sda -o - | blkparse -i -  # 追蹤塊設備 I/O

# 文件系統分析
fstrim -v /                        # 觸發 TRIM
tune2fs -l /dev/sda1               # 檢查文件系統信息
e4defrag /dev/sda1                 # 碎片整理

# 查找問題進程
lsof +D /path                      # 查看訪問特定目錄的進程
fuser -v /path                     # 查看使用該文件的進程
```

### 網絡問題診斷

```bash
# MTU 問題診斷
ping -M do -s 1472 host            # 測試 MTU（1500 - 28 = 1472）
tracepath host                     # 自動檢測 MTU

# 丟包分析
mtr -r host                        # 多次跟蹤結果
tcpdump -i eth0 -n 'tcp' | grep -i syn,ack | wc -l

# 延遲分析
netperf -H host                    # 網絡性能測試
iperf3 -c host -R -T 30            # 反向吞吐量測試

# DNS 性能
dig @nameserver domain +stats      # DNS 查詢統計
time host domain 8.8.8.8          # 測試 DNS 解析時間
```

## 虛擬化技術

### KVM/QEMU 管理

```bash
# 檢查虛擬化支持
grep -E 'vmx|svm' /proc/cpuinfo   # Intel 或 AMD

# 創建虛擬機
qemu-img create -f qcow2 disk.qcow2 20G    # 創建磁盤
qemu-system-x86_64 -m 2G -smp 2 -hda disk.qcow2 -cdrom ubuntu.iso  # 啟動

# 使用 libvirt
sudo virsh list                    # 列出 VM
sudo virsh dominfo vm_name         # VM 信息
sudo virsh start vm_name           # 啟動
sudo virsh stop vm_name            # 停止
sudo virsh snapshot-create vm_name # 創建快照

# 虛擬機遷移
virsh migrate --live vm_name qemu+ssh://dest_host/system
```

### Libvirt 和 virt-manager

```bash
# 使用 virt-manager GUI
sudo virt-manager

# 命令行操作
virt-install --name ubuntu --memory 2048 --vcpus 2 \
    --cdrom ubuntu.iso --disk size=20

# 查看虛擬機資源
virsh dumpxml vm_name              # 配置文件
virsh vcpuinfo vm_name             # CPU 信息
virsh domifstat vm_name            # 網絡統計
```

## 高級監控和告警

### Prometheus 和 Grafana

```bash
# Prometheus 配置
cat > /etc/prometheus/prometheus.yml << EOF
global:
  scrape_interval: 15s
scrape_configs:
  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
EOF

# 啟動 Prometheus
docker run -d -p 9090:9090 \
    -v /etc/prometheus:/etc/prometheus \
    prom/prometheus

# Node Exporter
docker run -d -p 9100:9100 \
    -v /proc:/host/proc:ro \
    -v /sys:/host/sys:ro \
    prom/node-exporter

# PromQL 查詢
node_cpu_seconds_total
increase(node_cpu_seconds_total[5m])
rate(node_cpu_seconds_total[5m])
```

### 自定義監控腳本

```bash
#!/bin/bash
# 綜合監控腳本

ALERT_EMAIL="admin@example.com"
THRESHOLD_CPU=80
THRESHOLD_MEM=85
THRESHOLD_DISK=90

check_cpu() {
    CPU=$(top -bn1 | grep "Cpu(s)" | awk '{print int($2)}')
    if [[ $CPU -gt $THRESHOLD_CPU ]]; then
        echo "告警: CPU 使用率 ${CPU}%" | mail -s "CPU 告警" $ALERT_EMAIL
    fi
}

check_memory() {
    MEM=$(free | grep Mem | awk '{print int($3/$2 * 100)}')
    if [[ $MEM -gt $THRESHOLD_MEM ]]; then
        echo "告警: 內存使用率 ${MEM}%" | mail -s "內存告警" $ALERT_EMAIL
    fi
}

check_disk() {
    DISK=$(df / | tail -1 | awk '{print int($5)}')
    if [[ $DISK -gt $THRESHOLD_DISK ]]; then
        echo "告警: 磁盤使用率 ${DISK}%" | mail -s "磁盤告警" $ALERT_EMAIL
    fi
}

check_services() {
    for service in ssh nginx mysql; do
        if ! systemctl is-active --quiet $service; then
            echo "告警: $service 服務未運行" | mail -s "服務告警" $ALERT_EMAIL
        fi
    done
}

# 執行檢查
check_cpu
check_memory
check_disk
check_services
```

## 常見高級應用場景

### 高可用性集群配置

```bash
# HAProxy + Keepalived
apt-get install haproxy keepalived

# HAProxy 配置示例
cat > /etc/haproxy/haproxy.cfg << EOF
global
    log stdout local0
    maxconn 4096
    
defaults
    mode http
    timeout connect 5000
    timeout client 50000
    timeout server 50000

frontend webserver
    bind *:80
    default_backend servers

backend servers
    balance roundrobin
    server web1 10.0.0.1:8080 check
    server web2 10.0.0.2:8080 check
EOF

# Keepalived 虛擬 IP
cat > /etc/keepalived/keepalived.conf << EOF
vrrp_script check_apiserver {
    script "/etc/keepalived/check_service.sh"
    interval 3
    weight -20
}

vrrp_instance VI_1 {
    state MASTER
    interface eth0
    virtual_router_id 51
    priority 101
    authentication {
        auth_type PASS
        auth_pass secret
    }
    virtual_ipaddress {
        10.0.0.10/24
    }
    track_scripts {
        check_apiserver
    }
}
EOF
```

### 日誌聚合和分析

```bash
# ELK Stack 部署
docker-compose up -d elasticsearch logstash kibana

# Logstash 配置
cat > /etc/logstash/conf.d/syslog.conf << EOF
input {
    syslog {
        port => 514
        type => syslog
    }
}

filter {
    if [type] == "syslog" {
        grok {
            match => { "message" => "%{SYSLOGLINE}" }
        }
    }
}

output {
    elasticsearch {
        hosts => ["localhost:9200"]
        index => "syslog-%{+YYYY.MM.dd}"
    }
}
EOF

# 查詢日誌
curl -X GET "localhost:9200/syslog-*/_search?q=error"
```

---

**上一章**: [進階技巧](06-advanced.md)

## 推薦進階學習路徑

1. **Linux 內核開發** - 深入學習內核源碼和驅動程序開發
2. **系統性能優化** - 成為性能優化專家
3. **雲原生技術** - Kubernetes、服務網格、無服務器計算
4. **安全研究** - 漏洞分析和安全加固
5. **開源貢獻** - 貢獻到 Linux 內核或主流項目

---

**版本**: 1.0 | **最後更新**: 2026年5月 | **難度**: 高級
