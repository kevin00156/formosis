#!/usr/bin/env bash
# ============================================================
# Formosis — 建立一份新論文／報告／簡報（獨立 git repo）
# ============================================================
#
# 用法：
#   ./scripts/new-thesis.sh <profile> <資料夾名稱>
#
# 例：
#   ./scripts/new-thesis.sh thesis-ncu my-thesis
#   ./scripts/new-thesis.sh slides-ncu my-defense
#
# 做的事：
#   1. 把 profiles/<profile>/skeleton/ 複製到 Formosis 根目錄下的 <資料夾名稱>/
#   2. 在該資料夾 git init，成為你自己的論文 repo（與工具 repo 分開，更新工具不會動到論文）
#   3. 在工具 repo 的 .git/info/exclude 忽略該資料夾（只影響本機，不改動任何受版控的檔案）
#   4. 寫入 .claude/settings.json，讓在論文資料夾開的 Claude Code 不載入工具開發用的 CLAUDE.md
#
# 論文資料夾必須直接放在 Formosis 根目錄下：skeleton 內的指令以 ../scripts/ 呼叫編譯腳本。
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

if [[ -t 1 ]]; then
    GREEN='\033[0;32m' YELLOW='\033[0;33m' RED='\033[0;31m' NC='\033[0m'
else
    GREEN='' YELLOW='' RED='' NC=''
fi
log_ok()    { echo -e "${GREEN}[OK]${NC}    $*"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*" >&2; }

usage() {
    sed -n '/^# 用法/,/^# ===/p' "$0" | sed 's/^# \?//'
    exit "${1:-0}"
}

[[ "${1:-}" == "-h" || "${1:-}" == "--help" ]] && usage 0
[[ $# -eq 2 ]] || usage 1

PROFILE="$1"
NAME="$2"
SKELETON="${REPO_ROOT}/profiles/${PROFILE}/skeleton"
TARGET="${REPO_ROOT}/${NAME}"

if [[ ! -d "$SKELETON" ]]; then
    log_error "找不到 profile：${PROFILE}（可用清單：./scripts/build.sh --list-profiles）"
    exit 1
fi
if [[ ! "$NAME" =~ ^[A-Za-z0-9._-]+$ ]]; then
    log_error "資料夾名稱只能用英數字、點、底線、連字號（中文或空白路徑會讓部分 LaTeX 工具出錯）：${NAME}"
    exit 1
fi
case "$NAME" in
    profiles|shared|scripts|docs|examples|docker|tests|.git|.github)
        log_error "「${NAME}」是 Formosis 自己的資料夾，請換個名字"; exit 1 ;;
esac
if [[ -e "$TARGET" ]]; then
    log_error "${TARGET} 已存在"
    exit 1
fi

# 1. 複製 skeleton
cp -r "$SKELETON"/. "$TARGET"/
log_ok "已從 profiles/${PROFILE}/skeleton/ 建立 ${NAME}/"

# 2. 論文 repo 的 .gitignore（編譯產物）
cat > "${TARGET}/.gitignore" <<'EOF'
# 編譯產物（需要保存 PDF 時可 git add -f paper.pdf）
*.pdf
*.tex
*.aux
*.bbl
*.bcf
*.blg
*.log
*.out
*.run.xml
*.toc
*.lof
*.lot
*.xdv
slides.html
.DS_Store
Thumbs.db
EOF

# 3. 在論文資料夾開 Claude Code 時，不載入上層工具 repo 的開發用 CLAUDE.md
#    （Claude Code 會載入所有上層目錄的 CLAUDE.md；工具開發規則對寫論文沒有用、還會誤導）
mkdir -p "${TARGET}/.claude"
root_name="$(basename "$REPO_ROOT")"
cat > "${TARGET}/.claude/settings.json" <<EOF
{
  "claudeMdExcludes": [
    "**/${root_name}/CLAUDE.md"
  ]
}
EOF

# 4. 工具 repo 忽略論文資料夾（本機設定，不改動受版控的檔案）
if command -v git &> /dev/null && git -C "$REPO_ROOT" rev-parse --git-dir &> /dev/null; then
    exclude="$(git -C "$REPO_ROOT" rev-parse --git-path info/exclude)"
    [[ "$exclude" = /* ]] || exclude="${REPO_ROOT}/${exclude}"
    mkdir -p "$(dirname "$exclude")"
    grep -qxF "/${NAME}/" "$exclude" 2>/dev/null || echo "/${NAME}/" >> "$exclude"
    log_ok "Formosis repo 已忽略 ${NAME}/（寫在 .git/info/exclude）"
fi

# 5. 論文資料夾成為獨立 git repo
if command -v git &> /dev/null; then
    git -C "$TARGET" init -q
    git -C "$TARGET" symbolic-ref HEAD refs/heads/main
    git -C "$TARGET" add -A
    if git -C "$TARGET" commit -q -m "chore: 以 Formosis ${PROFILE} 建立" 2> /dev/null; then
        log_ok "已初始化 ${NAME}/ 為獨立 git repo（分支 main）"
    else
        log_warn "已 git init，但第一次 commit 失敗（多半是還沒設定 git user.name / user.email）"
        log_warn "設定後在 ${NAME}/ 內執行：git commit -m \"chore: 初始化\""
    fi
else
    log_warn "找不到 git，略過版本控制初始化"
fi

main_md="paper.md"
[[ -f "${TARGET}/slides.md" ]] && main_md="slides.md"
cat <<EOF

下一步：
  cd ${NAME}
  # 編輯 ${main_md} 開頭的 YAML，替換 <placeholder>
  ../scripts/build.sh ${main_md}

要備份到 GitHub：在 GitHub 建一個 private repo，然後在 ${NAME}/ 內執行
  git remote add origin <你的 repo 網址>
  git push -u origin main
EOF
