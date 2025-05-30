#!/bin/bash

# 检查是否以 root 权限运行
if [ $EUID -ne 0 ]; then
    echo "请使用 root 权限执行脚本"
    exit 1
fi

# 检测操作系统类型
if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO=$ID
else
    echo "无法检测操作系统类型，请检查 /etc/os-release 文件"
    exit 1
fi

# 检测 Python3 是否安装
if [ ! command -v python3 &> /dev/null ] ; then
    echo "python3 未安装，现在安装 python3..."
    case "$DISTRO" in
        "ubuntu" | "debian")
            /usr/bin/apt update         
	    /usr/bin/apt install -y python3 python3-venv
            ;;
        "centos" | "rhel" | "fedora")
            dnf install python3 python3-venv -y
            ;;
        *)
            echo "未识别到支持的操作系统，请自行安装 Python3 后运行脚本"
            exit 1
            ;;
    esac
    # 验证 Python3 安装
    if [ ! command -v python3 &> /dev/null ] ; then
        echo "Python3 安装失败，请检查包管理器和网络"
        exit 1
    else
        echo "Python3 安装成功：$(python3 --version)"
    fi
else
    echo "Python3 已安装：$(python3 --version)"
fi

# 创建虚拟环境
ENV="LowEndTalk_env"
python3 -m venv "$ENV"
if [ -d "$ENV" ]; then
    echo "虚拟环境已创建：$(pwd)/$ENV"
else
    echo "虚拟环境创建失败"
    exit 1
fi

# 激活虚拟环境并安装依赖
source $ENV/bin/activate
if [ -f "requirements.txt" ]; then
    echo "正在安装 requirements.txt 中的依赖..."
    pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo "依赖安装成功"
    else
        echo "依赖安装失败，请检查 requirements.txt 或网络"
        deactivate
        exit 1
    fi
else
    echo "未找到 requirements.txt 文件，跳过依赖安装"
fi

# 提示
echo "虚拟环境已激活，位于：$(pwd)/$ENV"
deactivate

# cron 定时执行
# 定义定时任务
CRON_SCHEDULE="0,30 * * * *"
# 使用绝对路径，如果自定义路径，需要修改这里
SCRIPT_PATH="/opt/LowEndTalk/2_cron_lowendtalk.sh"
LOG_PATH="/opt/LowEndTalk/log/cron_app.log"
mkdir -p $(dirname "$LOG_PATH")
touch $LOG_PATH
chmod 644 $LOG_PATH
CRON_TASK="$CRON_SCHEDULE /bin/bash $SCRIPT_PATH > $LOG_PATH 2>&1"

# 检查定时任务脚本是否存在
if [ ! -f "$SCRIPT_PATH" ] ; then
	echo "脚本 $SCRIPT_PATH 不存在，请检查路径"
	exit 1
fi
# 检查脚本是否有执行权限
if [ ! -x "$SCRIPT_PATH" ] ; then
	echo "脚本 $SCRIPT_PATH 没有执行权限，现添加： "
	chmod +x $SCRIPT_PATH
	if [ $? -ne 0 ] ; then
		echo "无法使用脚本赋予执行权限，已退出"
		exit 1
	fi
	echo "已成功添加执行权限"
fi
# 将定时任务写入到crontab
CRON_BACKUP="/tmp/cron_back"
rm -rf "$CRON_BACKUP"
crontab -l > "$CRON_BACKUP" 2>/dev/null
if [ $? -ne 0 ] ; then
	echo "没有任务，这是第一个任务"
	touch $CRON_BACKUP
fi
# 检查是否重复定义同一个任务
if  grep -Fx "$CRON_TASK" "$CRON_BACKUP" > /dev/null ; then
	echo "任务 $CRON_TASK 已经存在，不需要再添加"
	rm -rf $CRON_BACKUP
	echo "脚本执行完成！"
	exit 0
fi
# 将任务追加到crontab
echo "$CRON_TASK" >> "$CRON_BACKUP"
crontab "$CRON_BACKUP"
if [ $? -eq 0 ] ; then
	echo "成功添加任务 $CRON_TASK"
else
	echo "添加任务 $CRON_TASK失败"
	rm -rf "$CRON_BACKUP"
	exit 1
fi

rm -rf "$CRON_BACKUP"



echo "脚本执行完成！"
