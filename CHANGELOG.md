# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
