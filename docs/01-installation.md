# 01 — 安裝教學

本文件詳細說明 Formosis 各平台的安裝步驟，以及常見安裝問題的排解。

## 系統需求

- **Windows 10/11**、**Ubuntu 22.04+**、**macOS 13+**
- **磁碟空間**：約 4 GB（TeX Live 完整安裝需要更多）
- **網路連線**：首次安裝下載依賴
- **管理員權限**：安裝套件需要

## 快速安裝（推薦）

### Windows

1. 開啟 PowerShell（建議「以系統管理員身分執行」）
2. Clone repo 並執行安裝腳本：
   ```powershell
   git clone https://github.com/kevin00156/formosis.git
   cd formosis
   .\scripts\install.ps1
   ```

如果 PowerShell 提示無法執行腳本，先執行：
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### Linux (Ubuntu / Debian / Fedora / Arch)

```bash
git clone https://github.com/kevin00156/formosis.git
cd formosis
bash scripts/install.sh
```

### macOS

確認已安裝 [Homebrew](https://brew.sh)，然後：
```bash
git clone https://github.com/kevin00156/formosis.git
cd formosis
bash scripts/install.sh
```

## 安裝腳本選項

`install.sh` / `install.ps1` 都支援以下旗標：

| 旗標 | 用途 |
|------|------|
| `--dry-run` / `-DryRun` | 只顯示要執行的指令，不實際安裝 |
| `--skip-tex` / `-SkipTex` | 跳過 TeX Live/MiKTeX 安裝（已裝就用這個） |
| `--skip-python` / `-SkipPython` | 跳過 Python 環境設置 |
| `--skip-skill` / `-SkipSkill` | 跳過 Claude Skill 安裝 |
| `--skip-test` / `-SkipTest` | 跳過編譯測試 |
| `--skill-only` / `-SkillOnly` | 只安裝 Skill（其他都跳過） |

範例：已有 Pandoc + LaTeX 環境，只想裝 Skill：
```bash
bash scripts/install.sh --skill-only
```

## 查看可用 profile

Formosis 以 **profile** 區分不同學校 / 機關的論文、報告、簡報格式。安裝完成後，用以下指令列出目前支援哪些 profile（會自動枚舉 `profiles/` 目錄，不必去翻原始碼）：

```bash
./scripts/build.sh --list-profiles      # Linux/macOS
.\scripts\build.ps1 -ListProfiles       # Windows
make list-profiles                       # 任一平台（需 make）
```

輸出會列出每個 profile 的 `NAME` / `TYPE` / `STYLE` / 說明。挑好之後，撰寫流程見 [02-writing-workflow.md](02-writing-workflow.md)。

## 手動安裝（不想用安裝腳本）

### 必要工具

| 工具 | 用途 | Windows | Linux | macOS |
|------|------|---------|-------|-------|
| Pandoc ≥3.0 | Markdown → LaTeX | `winget install JohnMacFarlane.Pandoc` | `apt install pandoc` | `brew install pandoc` |
| XeLaTeX | LaTeX → PDF | MiKTeX (winget) | `apt install texlive-xetex` | `brew install --cask mactex-no-gui` |
| xeCJK | 中文支援 | (MiKTeX 自動) | `apt install texlive-lang-cjk` | (MacTeX 內含) |
| biber | 處理 .bib | (MiKTeX 自動) | `apt install biber` | (MacTeX 內含) |
| 標楷體 / Noto CJK TC | 中文字體 | (Windows 內建) | `apt install fonts-noto-cjk` | (macOS 內建) |

### Skill 安裝

```bash
# Linux/macOS
bash scripts/install-skill.sh

# Windows
.\scripts\install-skill.ps1
```

預設安裝到 `~/.claude/skills/ncu-paper-writer/`，跨專案可用。

加上 `--project` / `-Project` 可改安裝到當前目錄的 `.claude/skills/`。

## 環境驗證

安裝完成後，執行健檢腳本確認：

```bash
# Linux/macOS
bash scripts/check-env.sh

# Windows
.\scripts\check-env.ps1
```

完整輸出應為：

```
通過: 10  警告: 0  失敗: 0
🎉 環境完整！可以開始撰寫論文了。
```

## 字體偵測

執行字體偵測腳本確認中文字體可用：

```bash
python scripts/check-fonts.py
```

正常輸出範例（Windows）：

```
=== NCU 論文字體檢查 (Windows) ===
偵測到 X 個中文字體

=== 推薦字體 ===
  ★ 標楷體
    細明體
    Noto Serif CJK TC

建議在 paper.md YAML 中設定：
    CJKmainfont: "標楷體"
```

如果沒有偵測到「標楷體」，請參考 [docs/05-troubleshooting.md](05-troubleshooting.md#中文字體缺失)。

## 更新

有新版本時，編譯時終端機會多印一行提醒（每天最多檢查一次，離線時不會出聲、也不會拖慢編譯）：

```
[UPDATE] Formosis v0.3.0 已發布（目前 v0.2.0）；執行 make update（或 python3 scripts/update.py apply）更新
```

更新指令：

```bash
make update                        # Linux/macOS
python3 scripts/update.py apply    # 同上
python scripts\update.py apply     # Windows
python3 scripts/update.py status   # 只看目前版本與最新版本
```

`update` 會：

1. 確認工具 repo 在 `main` 分支、且受版控的檔案沒被改過（改過就停下來，不會覆蓋你的修改）
2. 快轉（fast-forward）到最新 release
3. 如果這次更新改到 `profiles/` 或 `shared/`（論文格式相關），列出變動的檔案，提醒你重新編譯並檢查 PDF
4. 重新安裝各 profile 的 Claude Skill，讓撰寫規範與新模板一致

**不會自動更新**：只有你執行 `update` 時才會動作。快口試時如果不想冒格式變動的風險，看到提醒可以先不理會。

**你的論文不受影響**：用 `scripts/new-thesis` 建立的論文資料夾是獨立的 git repo，更新只動工具本身。

不想看到提醒：設定環境變數 `FORMOSIS_NO_UPDATE_CHECK=1`。

## 卸載

### 移除 Skill

```bash
# Linux/macOS
rm -rf ~/.claude/skills/ncu-paper-writer/

# Windows
Remove-Item -Recurse $env:USERPROFILE\.claude\skills\ncu-paper-writer\
```

### 移除 TeX Live / MiKTeX 等

- **Windows**：「應用程式與功能」中找到 MiKTeX 或 TeX Live 移除
- **Ubuntu/Debian**：`sudo apt remove --purge texlive-*`
- **macOS**：`brew uninstall --cask mactex-no-gui`

## 下一步

- 設定 Zotero：[docs/03-zotero-setup.md](03-zotero-setup.md)
- 開始寫論文：[docs/02-writing-workflow.md](02-writing-workflow.md)
- 遇到問題：[docs/05-troubleshooting.md](05-troubleshooting.md)
