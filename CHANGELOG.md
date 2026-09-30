# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `twthesis.sty` 新選項：`chapnum=zhenum`（章號「一、」）、`secsep=-`（節號 1-1）、`fignum=section|subsection`（圖表分章／分章節編號），以及 YAML `watermark:` 浮水印（供要求學生自行加浮水印的學校）。預設值維持原行為，thesis-ncu skeleton 與 examples 的 PDF 逐像素不變。
- thesis-ncu 的 `profile.yaml` 新增 `source:`（已對照校方〈學位論文撰寫體例參考〉114.09.25 版），並註明預設章節／公式編號與條文的差異及切換方式。

### Fixed
- `chapnum=zh`（thesis-ccu）的章號在內文、目錄與 `\ref` 全部顯示為「零」：`\thesection` 改用可展開的 `\zhnum{section}`。
- `cite.py`：Crossref `month=June` 轉為 `jun` 巨集、arXiv 年份改用首次提交年、去掉 doi 欄位的網址前綴、華藝學位論文對應 `@thesis`。
- Release workflow 改用 `docker/paper.Dockerfile` 編譯範例（v0.1.0 首次發佈因缺 `lmodern` 失敗）。

## [0.1.0] - 2026-09-30

### Changed
- **Rebranded**：專案改名為 **Formosis（福爾摩稿）**。原名 PaperForge 與多個同領域專案撞名（含 PyPI `paperforge`）。Python 套件名、GHCR image（`formosis-paper` / `formosis-slides`）、release 檔名、環境變數前綴一併改名；GitHub repo 預期改為 `kevin00156/formosis`。
- 論文改為獨立 git repo：`scripts/new-thesis.{sh,ps1} <profile> <資料夾>` 在根目錄下建立論文資料夾並 `git init`，工具 repo 以 `.git/info/exclude` 忽略它，並寫入 `.claude/settings.json` 的 `claudeMdExcludes`，避免寫論文時載入工具開發用的 `CLAUDE.md`。
- `build.sh` / `build.ps1` 複製論文資料夾到暫存目錄時略過 `.git`。
- thesis-ccu 的 `profile.yaml` 新增 `source:`，註明格式依中正機械系論文實例，非校方正式規範。

### Added
- 新版提醒與一鍵更新 `scripts/update.py`：編譯時每天最多檢查一次 release（`git ls-remote --tags`，離線不出聲）；`make update` / `update.py apply` 以 fast-forward 更新並重裝 skill，工具檔案被改過時拒絕更新。

### Changed
- 學位論文 profile 改用共用模板：`shared/latex/thesis.latex`（Pandoc 模板）+ `shared/latex/twthesis.sty`（共用版面，選項 `chapnum` / `eqnum` / `caplabelsep` / `lofprefix` / `urldate`）。各校 `template.latex` 改為約 20 行的 `thesisprofile.sty`；`profile.yaml` 的 `template:` 欄位現在會被 build script 讀取。重構前後 thesis-ncu、thesis-ccu skeleton 與 examples 的 PDF 逐像素一致。
- thesis-ccu 補上 thesis-ncu 已有的 `\mathindent` 安全網（原本只修在 NCU 複本）。

### Added
- 文獻自動化 `scripts/cite.py`（只用 Python 標準函式庫）：
  - `cite.py add <DOI|arXiv ID>`：經 doi.org content negotiation 取得 BibTeX，產生 `作者年份題目` 格式 citekey、以 DOI 去重後寫入 `.bib`；不需安裝 Zotero。`make cite ID=... INPUT=...`
  - `cite.py sync paper.md`：YAML 有 `zotero-collection:` 時從本機 Better BibTeX 拉最新 `.bib`，取代 GUI 的 Keep updated 設定。`build.sh` / `build.ps1` 編譯前自動執行，Zotero 沒開時僅警告。
  - arXiv 優先取 arXiv 自家 BibTeX（含 eprint）；DOI 註冊機構不給 BibTeX 時（如華藝）退回 CSL-JSON 轉換。
  - 方式 C：YAML 有 `zotero-collection:` 且裝了 `zotero-cli`（zotero-mcp-server 套件）時，`cite.py add` 改把文獻加進 Zotero collection，再同步取回 Better BibTeX citekey。agent 不論哪種模式都只用同一個指令。
- 論文／報告 skeleton 的 `CLAUDE.md` 新增「文獻管理」規則：一律經 `cite.py add` 新增、禁止捏造 BibTeX。
- `docs/03` 改寫為 DOI／Zotero 同步／Zotero MCP 三種方式。
- `tests/test_cite.py` 單元測試，並在 `lint.yml` 執行。

### Changed
- **Breaking**：根目錄的 `build.ps1`、`build.sh`、`build-slides.ps1`、`build-slides.sh` 全部搬入 `scripts/`。呼叫方式從 `./build.sh paper.md` 改為 `./scripts/build.sh paper.md`（Windows 同理：`.\scripts\build.ps1`）。Makefile、CI、安裝腳本、profile skeleton 的 Makefile/CLAUDE.md 都已同步更新。
- **Rebranded**：專案改名為 **PaperForge**。原 `ncu_paper_writer` 是工具最初為 NCU 學位論文設計的暫用名；現在定位為跨學校／期刊／機關的「文件鍛造」框架，每個 profile（如 `thesis-ncu`）保留各自的命名與規範識別。Python 套件名 `ncu-paper-writer` → `paperforge`；GitHub repo 與 URL 預期改為 `kevin00156/paperforge`。框架名不滲透 profile 內容：`ncu-paper-writer` skill 與 `profiles/thesis-ncu/` 維持原名。
- **Breaking**：目錄結構改為 profile-based。每個學校/期刊樣式是一個 profile，位於 `profiles/<type>-<style>/`：
  - `templates/ncu.latex` → `profiles/thesis-ncu/template.latex`
  - `template/` → `profiles/thesis-ncu/skeleton/`
  - `skill/ncu-paper-writer/` → `profiles/thesis-ncu/skill/`
  - `cites/` → `shared/cites/`
- `build.{ps1,sh}` 新增 `--profile <name>` 參數（預設 `thesis-ncu`），自動解析模板與 skill 路徑。
- `install-skill.{ps1,sh}` 新增 `--profile <name>` 參數；安裝後的 skill 名稱由 `SKILL.md` 的 frontmatter 決定。
- CI workflow 路徑過濾器從 `templates/`、`cites/` 改為 `profiles/`、`shared/`。

### Added
- 專案初始版本：完整的 Markdown + Zotero + Pandoc 碩論寫作工作流
- NCU 論文 Pandoc LaTeX 模板（`profiles/thesis-ncu/template.latex`）
- IEEE 引用樣式（`shared/cites/ieee.csl`）
- 跨平台編譯腳本：`build.ps1`（Windows）、`build.sh`（Linux/macOS）、`Makefile`
- Windows / Linux / macOS 一鍵安裝腳本（`scripts/install.{ps1,sh}`）
- Claude Code Skill `ncu-paper-writer`，內含 NCU 論文格式規範與章節錨點強制規則
- 論文範本骨架（`profiles/thesis-ncu/skeleton/paper.md`）含完整 YAML metadata 與 `{#sec:...}` 錨點範例
- 完整可編譯範例：`examples/minimal/`（最簡）與 `examples/full/`（完整章節）
- GitHub Actions CI：每次 push 編譯範例驗證
- 詳細文件：安裝、寫作流程、Zotero 設定、Pandoc 語法、疑難排解、客製化

## [0.1.0] - TBD

第一版正式發佈
