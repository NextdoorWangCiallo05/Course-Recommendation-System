#!/bin/bash
# 检查云端数据库内容
mysql -u root -p123334123334Ww course_recommendation -e "SELECT COUNT(*) as user_count FROM users; SELECT COUNT(*) as major_count FROM majors; SELECT COUNT(*) as course_count FROM courses;"
