#!/bin/bash
#
# setup.sh - 腾讯文档 MCP 鉴权脚本
#
# 用法：
#   bash setup.sh tdoc_check_and_start_auth   # 检查状态 / 发起授权
#   bash setup.sh tdoc_fetch_token            # 获取 Token
#

set -e

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
MCP_SERVICE="tencent-docs"
TOKEN_URL="https://docs.qq.com/scenario/open-claw.html"
CONFIG_KEY="TENCENT_DOCS_TOKEN"

# ──────────────────────────────────────────────
# 读取已配置的 Token（从 mcporter 配置中）
# ──────────────────────────────────────────────
get_configured_token() {
  local token=""
  # 尝试从环境变量读取
  if [ -n "$TENCENT_DOCS_TOKEN" ]; then
    token="$TENCENT_DOCS_TOKEN"
  fi
  echo "$token"
}

# ──────────────────────────────────────────────
# 调用 mcporter 工具的辅助函数
# ──────────────────────────────────────────────
mcp_call() {
  local tool="$1"
  local args="$2"
  mcporter call "$MCP_SERVICE" "$tool" --args "$args" 2>/dev/null
}

# ──────────────────────────────────────────────
# 步骤一：检查授权状态 / 发起授权
# ──────────────────────────────────────────────
cmd_check() {
  echo "检查腾讯文档授权状态..."

  # 尝试用一个无害的接口探测 Token 是否有效
  local res
  res=$(mcp_call "manage.search_file" '{"keyword":"_probe_token_"}' 2>&1) || true

  # 检查是否包含 token 相关错误
  if echo "$res" | grep -qi "400006\|token\|expired\|not_authorized"; then
    echo "AUTH_REQUIRED:$TOKEN_URL"
  elif echo "$res" | grep -qi "READY\|file_id\|error.*\".*:\|\"files\""; then
    echo "READY"
  else
    # 无法判断时，认为需要授权
    echo "AUTH_REQUIRED:$TOKEN_URL"
  fi
}

# ──────────────────────────────────────────────
# 步骤二：获取 Token（用户已在浏览器完成授权）
# ──────────────────────────────────────────────
cmd_fetch_token() {
  echo "正在获取腾讯文档 Token..."

  # 尝试调用一个需要认证的接口来验证 Token
  local res
  res=$(mcp_call "manage.search_file" '{"keyword":""}' 2>&1) || true

  if echo "$res" | grep -qi "error\|400006\|not_authorized"; then
    echo "ERROR:not_authorized"
    return 1
  fi

  echo "TOKEN_READY"
}

# ──────────────────────────────────────────────
# 主入口
# ──────────────────────────────────────────────
CMD="${1:-}"
case "$CMD" in
  tdoc_check_and_start_auth)
    cmd_check
    ;;
  tdoc_fetch_token)
    cmd_fetch_token
    ;;
  *)
    echo "用法:"
    echo "  bash setup.sh tdoc_check_and_start_auth   # 检查状态 / 发起授权"
    echo "  bash setup.sh tdoc_fetch_token            # 获取 Token"
    ;;
esac
