# 第5章: 開發工具

## 目錄
- [git - 版本控制](#git---版本控制)
- [docker - 容器化](#docker---容器化)
- [編譯和構建工具](#編譯和構建工具)
- [調試工具](#調試工具)

## git - 版本控制

### 初始配置

```bash
# 配置用戶信息
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# 查看配置
git config --list
git config --global user.name

# 編輯配置文件
git config --global --edit
```

### 基本工作流

```bash
# 初始化倉庫
git init                          # 本地倉庫
git clone URL                     # 克隆遠程倉庫

# 檢查狀態
git status                        # 查看工作區狀態
git status -s                     # 簡短格式

# 添加文件
git add file.txt                  # 添加特定文件
git add .                         # 添加所有更改
git add *.py                      # 添加特定類型文件
git add -A                        # 添加所有更改（包括刪除）

# 提交
git commit -m "commit message"    # 提交
git commit -am "message"          # 直接提交已跟蹤文件
git commit --amend                # 修改最後一次提交

# 推送
git push                          # 推送到默認分支
git push origin main              # 推送到特定分支
git push -u origin main           # 推送並設置上遊分支
git push origin --delete branch   # 刪除遠程分支

# 拉取
git pull                          # 拉取並合併
git pull --rebase                 # 拉取並變基
git fetch                         # 只拉取不合併
```

### 分支管理

```bash
# 查看分支
git branch                        # 本地分支
git branch -a                     # 所有分支
git branch -r                     # 遠程分支
git branch -v                     # 詳細信息

# 創建分支
git branch new_branch             # 創建分支
git branch -b new_branch          # 創建並切換
git checkout -b feature/new       # 創建並切換（舊語法）
git switch -c feature/new         # 創建並切換（新語法）

# 切換分支
git checkout main                 # 切換到 main
git switch main                   # 切換到 main（新語法）
git switch -                      # 切換到上一個分支

# 刪除分支
git branch -d branch              # 刪除本地分支
git branch -D branch              # 強制刪除
git push origin --delete branch   # 刪除遠程分支

# 合併分支
git merge branch                  # 合併到當前分支
git merge --no-ff branch          # 保留合併提交
git merge --squash branch         # 壓縮提交
```

### 查看歷史

```bash
# 查看日誌
git log                           # 完整日誌
git log --oneline                 # 簡短格式
git log --graph --oneline --all   # 圖形化顯示
git log -n 5                      # 最後5次提交
git log --since="2 weeks ago"     # 特定時間段

# 查看特定文件
git log file.txt                  # 特定文件的歷史
git log -p file.txt               # 包含變更內容

# 查看差異
git diff                          # 工作區與暫存區
git diff --cached                 # 暫存區與最後提交
git diff main                     # 與指定分支比較
git diff HEAD~1                   # 與上一次提交比較
git diff file.txt                 # 特定文件的差異

# 查看特定提交
git show commit_hash              # 查看提交詳情
git show commit_hash:file.txt     # 查看特定版本的文件
```

### 撤銷和重置

```bash
# 撤銷工作區更改
git restore file.txt              # 撤銷工作區更改（新語法）
git checkout -- file.txt          # 撤銷工作區更改（舊語法）

# 撤銷暫存
git restore --staged file.txt     # 撤銷暫存（新語法）
git reset file.txt                # 撤銷暫存（舊語法）

# 重置提交
git reset --soft HEAD~1           # 重置，保留工作區和暫存區
git reset --mixed HEAD~1          # 重置，保留工作區
git reset --hard HEAD~1           # 重置，丟棄所有更改

# 變基
git rebase main                   # 變基到 main
git rebase -i HEAD~3              # 交互式變基最後3次提交
git rebase --abort                # 中止變基

# 恢復刪除的提交
git reflog                        # 查看引用日誌
git recover commit_hash           # 恢復提交
```

### 遠程倉庫

```bash
# 管理遠程倉庫
git remote                        # 查看遠程倉庫
git remote -v                     # 詳細信息
git remote add origin URL         # 添加遠程倉庫
git remote remove origin          # 移除遠程倉庫
git remote set-url origin URL     # 修改 URL

# 追蹤遠程分支
git branch --set-upstream-to=origin/main  # 設置追蹤分支
git branch -u origin/main         # 簡短形式

# 工作流
git fetch origin                  # 更新遠程信息
git pull origin main              # 拉取並合併
git push origin main              # 推送
```

## docker - 容器化

### 基本概念

- **image** - 容器模板（如類定義）
- **container** - 運行的實例（如對象）
- **registry** - 存儲鏡像的倉庫（如 Docker Hub）

### 鏡像操作

```bash
# 查看鏡像
docker images                     # 列出本地鏡像
docker images -a                  # 包括中間鏡像
docker images --filter "dangling=true"  # 查看懸掛鏡像

# 搜索鏡像
docker search nginx               # 搜索 Docker Hub
docker search nginx --limit 5     # 限制結果數

# 拉取鏡像
docker pull nginx                 # 拉取最新版本
docker pull nginx:1.19            # 拉取特定版本
docker pull gcr.io/image:tag      # 拉取特定倉庫

# 刪除鏡像
docker rmi image_id               # 刪除鏡像
docker rmi $(docker images -q)    # 刪除所有鏡像
docker image prune                # 清理未使用的鏡像

# 構建鏡像
docker build -t myapp:1.0 .       # 構建鏡像
docker build -t myapp:latest .    # 構建並標記
docker build -f Dockerfile.prod . # 使用特定 Dockerfile

# 標記鏡像
docker tag myapp:1.0 myapp:latest
docker tag myapp:1.0 user/myapp:1.0

# 推送鏡像
docker push user/myapp:1.0
```

### 容器操作

```bash
# 運行容器
docker run image_name             # 基本運行
docker run -d image_name          # 後台運行
docker run -it image_name bash    # 交互式運行
docker run --name mycontainer image_name  # 指定名稱
docker run -p 8080:8080 image_name        # 端口映射
docker run -v /host/path:/container/path image_name  # 掛載卷
docker run -e VAR=value image_name        # 設置環境變量
docker run --rm image_name                # 退出後刪除容器

# 查看容器
docker ps                         # 運行中的容器
docker ps -a                      # 所有容器
docker ps -q                      # 只顯示容器 ID
docker container ls               # 同 docker ps

# 容器信息
docker inspect container_id       # 詳細信息
docker logs container_id          # 查看日誌
docker logs -f container_id       # 實時日誌
docker logs --tail 20 container_id  # 最後20行

# 進入容器
docker exec -it container_id bash     # 執行命令
docker attach container_id            # 進入容器

# 停止和刪除
docker stop container_id          # 停止容器
docker kill container_id          # 強制停止
docker restart container_id       # 重啟容器
docker rm container_id            # 刪除容器
docker rm -f container_id         # 強制刪除
docker rm $(docker ps -aq)        # 刪除所有容器

# 複製文件
docker cp file container_id:/path         # 複製到容器
docker cp container_id:/path/file .       # 從容器複製

# 提交更改
docker commit container_id myapp:2.0      # 將容器提交為鏡像
```

### Docker Compose

```bash
# 基本命令
docker-compose up                 # 啟動服務
docker-compose up -d              # 後台運行
docker-compose down               # 停止並刪除容器
docker-compose ps                 # 查看運行狀態
docker-compose logs               # 查看日誌
docker-compose logs -f service    # 實時日誌

# 重建和更新
docker-compose build              # 構建鏡像
docker-compose up --build         # 構建並啟動
docker-compose pull               # 拉取新鏡像
docker-compose up --force-recreate  # 強制重建

# 執行命令
docker-compose exec service bash  # 進入服務
docker-compose run service python manage.py migrate  # 運行命令

# 管理
docker-compose config             # 查看配置
docker-compose validate           # 驗證配置
docker-compose rm                 # 刪除容器
```

## 編譯和構建工具

### gcc/g++ - C/C++ 編譯器

```bash
# 基本編譯
gcc main.c -o program             # 編譯 C 程序
g++ main.cpp -o program           # 編譯 C++ 程序

# 編譯選項
gcc -Wall main.c -o program       # 顯示所有警告
gcc -O2 main.c -o program         # 優化等級 2
gcc -g main.c -o program          # 包含調試符號
gcc -c main.c                     # 只編譯不鏈接

# 多文件編譯
gcc main.c lib.c -o program
gcc -c main.c -o main.o
gcc -c lib.c -o lib.o
gcc main.o lib.o -o program

# 鏈接庫
gcc main.c -o program -lm         # 鏈接數學庫
gcc main.c -o program -L/usr/local/lib -lmylib -I/usr/local/include
```

### make - 構建自動化

```bash
# 基本使用
make                              # 執行 Makefile
make clean                        # 執行 clean 目標
make install                      # 執行 install 目標

# Makefile 示例
cat > Makefile << 'EOF'
CC = gcc
CFLAGS = -Wall -O2

program: main.o lib.o
	$(CC) $(CFLAGS) -o program main.o lib.o

main.o: main.c
	$(CC) $(CFLAGS) -c main.c

lib.o: lib.c
	$(CC) $(CFLAGS) -c lib.c

clean:
	rm -f *.o program
EOF
```

### cmake - 跨平台構建

```bash
# 基本使用
cmake .                           # 生成構建文件
make                              # 編譯
make install                      # 安裝

# 構建目錄中編譯
mkdir build && cd build
cmake ..
make
```

### npm - Node.js 包管理

```bash
# 項目管理
npm init                          # 初始化項目
npm install                       # 安裝依賴
npm install package               # 安裝特定包
npm install -g package            # 全局安裝

# 依賴管理
npm update                        # 更新依賴
npm uninstall package             # 卸載包
npm list                          # 列出依賴

# 運行腳本
npm run build                     # 運行 build 腳本
npm run dev                       # 運行 dev 腳本
npm start                         # 運行 start 腳本
npm test                          # 運行測試

# 發布
npm publish                       # 發布到 npm
npm version patch                 # 更新版本
```

### pip - Python 包管理

```bash
# 安裝
pip install package               # 安裝包
pip install package==1.0.0        # 安裝特定版本
pip install -r requirements.txt   # 從文件安裝

# 管理
pip list                          # 列出已安裝包
pip show package                  # 顯示包信息
pip uninstall package             # 卸載包
pip update package                # 更新包

# 虛擬環境
python -m venv venv               # 創建虛擬環境
source venv/bin/activate          # 激活虛擬環境
deactivate                        # 停用虛擬環境

# 導出依賴
pip freeze > requirements.txt
```

## 調試工具

### gdb - GNU 調試器

```bash
# 基本使用
gdb ./program                     # 啟動調試
gdb -args ./program arg1 arg2     # 帶參數調試

# 常用命令
run [args]                        # 運行程序
break main                        # 設置斷點
break file.c:10                   # 設置行號斷點
continue                          # 繼續執行
next                              # 下一行（不進入函數）
step                              # 下一行（進入函數）
list                              # 列出代碼
print variable                    # 打印變量
print *pointer                    # 打印指針內容
backtrace                         # 查看堆棧
frame n                           # 切換堆棧幀
quit                              # 退出調試
```

### strace - 系統調用追蹤

```bash
strace ./program                  # 跟蹤系統調用
strace -e open,read,write ./program  # 特定系統調用
strace -c ./program               # 統計信息
strace -o trace.log ./program     # 輸出到文件
strace -p PID                     # 追蹤運行中的進程
```

### valgrind - 內存檢查

```bash
valgrind ./program                # 檢查內存洩漏
valgrind --leak-check=full ./program
valgrind --track-origins=yes ./program   # 追蹤初始化
valgrind --tool=helgrind ./program      # 線程檢查
```

### lldb - LLVM 調試器（macOS）

```bash
lldb ./program
lldb -- ./program arg1 arg2
```

---

**上一章**: [網絡工具](04-network-tools.md) | **下一章**: [進階技巧](06-advanced.md)
