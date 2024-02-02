#!/bin/bash

# 脚本: url_check.sh
# 用途: 检查文件A中的URL是否在文件B中，并计算找到和未找到的数量
# 使用方法: ./url_check.sh path/to/fileA.txt path/to/fileB.txt

fileA="$1"  # 第一个参数：文件A的路径
fileB="$2"  # 第二个参数：文件B的路径

if [ ! -f "$fileA" ]; then
    echo "FileA not found: $fileA"
    exit 1
fi

if [ ! -f "$fileB" ]; then
    echo "FileB not found: $fileB"
    exit 1
fi

found=0
not_found=0

while read url; do
    if grep -Fxq "$url" "$fileB"; then
        #echo "$url found in '$fileB'"
        ((found++))
    else
        echo "$url"
        # echo "$url not found in '$fileB'"
        ((not_found++))
    fi
done < "$fileA"

echo "Total found: $found"
echo "Total not found: $not_found"

