#!/bin/bash
# 检查 MySQL 用户认证方式
mysql -u root -p123334123334Ww -e "SELECT user, host, plugin FROM mysql.user WHERE user='root';"
