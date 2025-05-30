这是一个python 爬虫仓库

learn中是静态页面爬虫，例如requests库等操作
selenium中是动态页面爬虫，包含了如何过验证码检测等代码，里面 CalculateDistance.py 包含了一个自动检测滑动验证码区域的类，可以直接使用，可以看我的另一个仓库，有深度学习预测滑块验证码位置


小项目中有各种各样的项目，监控脚本、下载脚本等等

## 2025年5月30日更新：
1. 新做了一个LowEndTalk优惠信息监控网站，接入telegram机器人，当该网站每一天有新的offer时，会自动通过脚本发送给telegram机器人
2. 该脚本每半小时爬取一次网站（通过cron定时任务，你可以修改定时）。 
#### 安装方式
1. 将LowEndTalk目录下的所有内容克隆到你的服务器的/opt/LowEndTalk/文件夹下，你也可以自定义，你需要修改1_LowEndTalk.sh中的SCRIPT_PATH与LOG_PATH为你的自定义目录（别修改文件名）
2. 去env/LowEndTalk中配置机器人Token和chat_id（必须）
3. 运行1_LowEndTalk.sh，将进行全自动安装（你也可以手动安装）
3. 再运行2_cron_lowendtalk.sh，你可以直接获取到当天截止到目前的所有offer信息。
4. 完毕

# 有什么好的项目可以联系我邮箱，有时间我会考虑开发：mengta6664@gmail.com
