# 第3章: 文本處理工具

## 目錄
- [grep - 文本搜索](#grep---文本搜索)
- [sed - 流編輯器](#sed---流編輯器)
- [awk - 文本分析工具](#awk---文本分析工具)
- [其他文本工具](#其他文本工具)

## grep - 文本搜索

### 基本用法

```bash
grep [選項] 模式 [文件]

# 常用選項
grep -i pattern file        # 忽略大小寫
grep -v pattern file        # 反向匹配（不包含）
grep -n pattern file        # 顯示行號
grep -c pattern file        # 計算匹配行數
grep -r pattern dir/        # 遞歸搜索目錄
grep -E pattern file        # 使用擴展正則表達式
grep -F pattern file        # 使用固定字符串（不作為正則）
grep -l pattern file        # 只顯示文件名
grep -A 3 pattern file      # 顯示匹配行及之後的3行
grep -B 3 pattern file      # 顯示匹配行及之前的3行
grep -C 3 pattern file      # 顯示匹配行及前後各3行
grep -w pattern file        # 匹配完整單詞
grep -o pattern file        # 只顯示匹配的部分
```

### 實例

```bash
# 基本搜索
grep "error" log.txt
grep "ERROR" *.log

# 忽略大小寫搜索
grep -i "warning" system.log

# 不包含某個模式
grep -v "success" status.txt

# 搜索多個模式
grep -E "error|warning|fail" log.txt

# 計算匹配數
grep -c "failed" system.log

# 遞歸搜索目錄
grep -r "TODO" src/

# 搜索且顯示上下文
grep -C 2 "critical" errors.log

# 只顯示文件名
grep -l "bug" *.py

# 顯示不匹配的行
grep -v "^#" config.conf    # 排除註釋行
```

### 正則表達式基礎

| 符號 | 含義 |
|------|------|
| `.` | 匹配任意單個字符 |
| `*` | 匹配前一個字符0次或多次 |
| `+` | 匹配前一個字符1次或多次 |
| `?` | 匹配前一個字符0次或1次 |
| `^` | 匹配行開始 |
| `$` | 匹配行結尾 |
| `[]` | 字符集 |
| `\|` | 或（在 grep 中需要轉義）或用 `\|` |
| `()` | 分組（在 grep 中需要轉義或使用 -E）|

```bash
# 正則表達式範例
grep "^Error" file.txt                # 以 Error 開頭
grep "error$" file.txt                # 以 error 結尾
grep "^[0-9]" file.txt                # 以數字開頭
grep "[a-z]\{3\}" file.txt            # 3個小寫字母
grep "error.*occurred" file.txt       # error 後面跟任意字符和 occurred
grep "\.txt$" files.txt               # 以 .txt 結尾的文件名
grep "^$" file.txt                    # 空行
```

## sed - 流編輯器

### 基本用法

```bash
sed [選項] '命令' [文件]

# 常用選項
sed -n '5p' file            # 只打印第5行
sed -i 's/old/new/' file    # 就地編輯文件
sed -e 's/a/b/' file        # 執行多個編輯命令
sed -f script.sed file      # 從腳本文件讀取命令
sed '2,5d' file             # 刪除第2到5行
```

### 常用命令

| 命令 | 說明 |
|------|------|
| `s` | 替換（substitute） |
| `d` | 刪除（delete） |
| `p` | 打印（print） |
| `a` | 附加（append） |
| `i` | 插入（insert） |
| `c` | 改變（change） |
| `y` | 轉換字符（translate） |

### 替換 (s) 命令

```bash
# 基本語法
sed 's/pattern/replacement/' file

# 常見選項
sed 's/old/new/' file               # 每行第一個匹配
sed 's/old/new/g' file              # 全局替換（整行所有匹配）
sed 's/old/new/2' file              # 替換每行第2個匹配
sed 's/old/new/gi' file             # 全局替換，忽略大小寫
sed -i 's/old/new/g' file           # 就地編輯

# 使用不同分隔符
sed 's|/path/old|/path/new|g' file  # 使用 | 作分隔符
sed 's@old@new@g' file              # 使用 @ 作分隔符

# 特殊字符
sed 's/\$/dollar/' file             # 轉義特殊字符
sed 's/.*/[&]/' file                # & 代表整個匹配的字符串
sed 's/\(.*\) \(.*\)/\2 \1/' file  # 交換字段
```

### 實例

```bash
# 替換
sed 's/foo/bar/' file.txt           # 替換每行第一個 foo
sed 's/foo/bar/g' file.txt          # 替換所有 foo
sed -i 's/old/new/g' file.txt       # 修改文件

# 刪除
sed '1d' file.txt                   # 刪除第1行
sed '1,5d' file.txt                 # 刪除第1到5行
sed '/pattern/d' file.txt           # 刪除包含 pattern 的行
sed '/^$/d' file.txt                # 刪除空行

# 打印
sed -n '5p' file.txt                # 只顯示第5行
sed -n '1,3p' file.txt              # 顯示第1到3行
sed -n '/pattern/p' file.txt        # 只顯示包含 pattern 的行

# 插入和附加
sed '2a\new line' file.txt          # 在第2行後附加
sed '2i\new line' file.txt          # 在第2行前插入
sed '/pattern/a\new line' file.txt  # 在匹配行後附加

# 轉換行
sed 'y/abc/xyz/' file.txt           # a→x, b→y, c→z
```

## awk - 文本分析工具

### 基本用法

```bash
awk [選項] 'pattern { action }' [文件]

# 常用選項
awk -F: '...' file         # 設置字段分隔符
awk -v var=value '...' file    # 設置變量
```

### 內置變量

| 變量 | 說明 |
|------|------|
| `NF` | 字段數 |
| `NR` | 行號 |
| `FS` | 字段分隔符（默認空格） |
| `OFS` | 輸出字段分隔符 |
| `ORS` | 輸出行分隔符 |
| `FILENAME` | 當前文件名 |
| `FNR` | 文件行號 |

### 字段訪問

```bash
# 訪問字段
awk '{print $1}' file              # 打印第1個字段
awk '{print $2, $3}' file          # 打印第2、3個字段
awk '{print NF}' file              # 打印字段數
awk '{print $NF}' file             # 打印最後一個字段
awk '{print $(NF-1)}' file         # 打印倒數第2個字段

# 使用分隔符
awk -F: '{print $1}' /etc/passwd   # 使用 : 作分隔符
awk -F, '{print $2}' data.csv      # 使用 , 作分隔符
```

### 模式和動作

```bash
# 模式範例
awk 'NR==5' file                   # 只處理第5行
awk '/pattern/' file               # 處理包含 pattern 的行
awk 'NR>1' file                    # 跳過第1行
awk 'NR%2==0' file                 # 處理偶數行
awk 'BEGIN {...} END {...}' file   # 開始和結束

# 實例
awk 'BEGIN {print "開始"}
    {count++} 
    END {print "總共: " count}' file
```

### 常用操作

```bash
# 計算和統計
awk '{sum += $1} END {print sum}' numbers.txt    # 求和
awk '{count++} END {print count}' file           # 計數
awk '{if ($1 > 0) count++} END {print count}' file  # 條件計數

# 字段操作
awk '{print $1, $2}' file                        # 打印前兩個字段
awk '{print NF, $0}' file                        # 打印字段數和整行
awk '{$1 = "modified"; print}' file              # 修改字段

# 字符串操作
awk '{print toupper($1)}' file                   # 大寫
awk '{print tolower($1)}' file                   # 小寫
awk '{print length($0)}' file                    # 行長度
awk '{print substr($0, 1, 5)}' file              # 子字符串
```

### 實例

```bash
# 解析 CSV
awk -F, '{print $1, $3}' data.csv

# 處理日誌文件
awk '{print $1}' access.log | sort | uniq -c    # 計數 IP

# 提取特定列
awk -F: '{print $1, $3}' /etc/passwd             # 用戶名和 UID

# 條件篩選
awk '$3 > 100' numbers.txt                       # 打印第3列大於100的行
awk '$1 ~ /error/' log.txt                       # 包含 error 的行

# 複雜操作
awk -F: 'NR>1 {sum+=$3} END {print "平均:", sum/(NR-1)}' file
```

## 其他文本工具

### cut - 提取列

```bash
cut -d: -f1 /etc/passwd            # 提取 : 分隔的第1列
cut -d, -f1,3 data.csv             # 提取逗號分隔的第1、3列
cut -c1-10 file.txt                # 提取每行前10個字符
cut -b1-5 file.txt                 # 提取每行前5個字節
```

### tr - 轉換字符

```bash
tr 'a-z' 'A-Z' < input.txt         # 小寫轉大寫
tr -d '[:digit:]' < input.txt      # 刪除所有數字
tr -s ' ' < input.txt              # 壓縮多個空格為一個
echo "hello" | tr 'h' 'H'          # 替換字符
```

### sort - 排序

```bash
sort file.txt                      # 排序
sort -r file.txt                   # 逆序排序
sort -n file.txt                   # 數字排序
sort -u file.txt                   # 去重排序
sort -t: -k3n /etc/passwd          # 按第3列數字排序
sort -k2 file.txt                  # 按第2列排序
```

### uniq - 去重

```bash
uniq file.txt                      # 去除連續重複
uniq -c file.txt                   # 計數
uniq -d file.txt                   # 只顯示重複的行
uniq -u file.txt                   # 只顯示唯一的行
sort file.txt | uniq               # 先排序再去重
```

### wc - 計數

```bash
wc file.txt                        # 行數、單詞數、字節數
wc -l file.txt                     # 行數
wc -w file.txt                     # 單詞數
wc -c file.txt                     # 字節數
wc -m file.txt                     # 字符數
```

### head 和 tail - 查看文件開頭和結尾

```bash
head file.txt                      # 前10行
head -n 5 file.txt                 # 前5行
tail file.txt                      # 後10行
tail -n 5 file.txt                 # 後5行
tail -f file.txt                   # 實時跟蹤
tail -n +6 file.txt                # 從第6行開始
```

## 文本處理工作流程

### 日誌分析

```bash
# 查看最常見的錯誤
grep "error" app.log | awk '{print $5}' | sort | uniq -c | sort -rn

# 統計不同狀態碼
grep "HTTP" access.log | awk '{print $9}' | sort | uniq -c

# 查找時間段內的錯誤
grep "2026-05-13" app.log | grep -i error
```

### 數據轉換

```bash
# CSV 轉換為格式化輸出
awk -F, '{printf "%-20s %-20s %-20s\n", $1, $2, $3}' data.csv

# 反轉行
awk '{a[NR]=$0} END {for (i=NR; i>0; i--) print a[i]}' file.txt

# 每行添加行號
awk '{print NR": "$0}' file.txt
```

### 批量替換

```bash
# 替換多個文件
sed -i 's/old/new/g' *.txt

# 在特定目錄下替換
find . -name "*.py" -type f -exec sed -i 's/old/new/g' {} \;
```

---

**上一章**: [系統管理工具](02-system-tools.md) | **下一章**: [網絡工具](04-network-tools.md)
