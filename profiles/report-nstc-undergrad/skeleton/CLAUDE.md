# 國科會大專學生研究計畫成果報告專案

本專案使用 [PaperForge](https://github.com/kevin00156/paperforge) 的 `report-nstc-undergrad` profile 工作流撰寫。

## Claude Code Skill

本專案啟用 `nstc-undergrad-report-writer` skill。請依照 skill 中的 **國科會大專生報告格式規範**撰寫，
特別注意以下強制規範：

1. **章節錨點**：所有章節（`#` / `##` / `###` / `####`）後面必須加 `{#sec:...}` 標記
2. **禁用「——」破折號**：用頓號、逗號、括號或重新組句
3. **圖表編號**：用 `\label{}` + `\ref{}`，不要手寫「圖 1-1」、「表 3-2」（編號為「章-序號」格式，由模板自動處理）
4. **章節引用**：章用「第 \ref{sec:x} 章」，節用「\ref{sec:y} 節」
5. **不要寫英文摘要與致謝**：國科會大專生報告通常僅有中文摘要
6. **參考文獻**：用 `[@key]` 引用，文獻條目放在 `references.bib`

## 編譯

從 PaperForge 專案根目錄執行（假設此報告資料夾在 PaperForge 子目錄）：

- Windows: `..\scripts\build.ps1 paper.md --profile report-nstc-undergrad`
- Linux/macOS: `../scripts/build.sh paper.md --profile report-nstc-undergrad`

或使用 VS Code 任務面板（Ctrl+Shift+B）。

## 文獻管理

新增或引用文獻時依下列優先序處理，**絕不憑記憶捏造 BibTeX 條目或 citekey**（以下 `python3` 在 Windows 上改用 `python`）：

1. **有 Zotero MCP 工具可用時**（工具名稱含 `zotero`）：
   - 先在文獻庫搜尋是否已有該文獻；有的話取其 Better BibTeX citekey 直接引用
   - 沒有的話依 DOI / arXiv ID / ISBN 新增到 `paper.md` YAML `zotero-collection:` 指定的 collection
   - 新增後執行 `python3 ../scripts/cite.py sync paper.md` 把 `references.bib` 拉回（編譯時也會自動同步）
2. **沒有 Zotero MCP**：
   - YAML 有 `zotero-collection:`：`references.bib` 由 Zotero 管理，不可直接修改；請使用者用 Zotero Connector 抓取後執行 `cite.py sync`
   - YAML 沒有 `zotero-collection:`：執行 `python3 ../scripts/cite.py add <DOI 或 arXiv ID> --md paper.md`，stdout 印出的 citekey 即可寫成 `[@key]`
3. **只有標題、沒有 DOI**：先上網查出 DOI，確認標題、作者、年份都相符再走 1 或 2；查不到 DOI 的文獻（多數中文期刊、學位論文）請使用者用 Zotero Connector 抓取
4. 加完引用後編譯，lint 會檢查每個 `[@key]` 都存在於 `references.bib`

## 開始撰寫

1. 編輯 `paper.md` 開頭 YAML 區塊，替換所有 `<placeholder>` 為實際內容（計畫名稱、計畫編號、執行單位等）
2. 設定文獻來源（三選一，詳見 PaperForge docs/03）：只用 DOI 加文獻、或在 YAML 設 `zotero-collection:` 由 Zotero 管理、或再加裝 Zotero MCP 讓 Claude 直接操作文獻庫
3. 撰寫各章節，記得每個章節都加 `{#sec:...}` 錨點
4. 編譯產生 PDF，檢視外封、內封與正文排版
