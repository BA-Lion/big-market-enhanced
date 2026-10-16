#!/usr/bin/env sh
set -eu
# 先在仓库根目录完成 Maven 打包；从任意工作目录调用本脚本。
cd "$(dirname "$0")"
docker build -t big-market-enhanced:local -f Dockerfile .
