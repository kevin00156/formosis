# 國立臺灣科技大學學位論文專案

本專案依〈國立臺灣科技大學學位論文撰寫、編排規則及注意事項〉（113.12.24 第218次教務會議通過）撰寫，
以 [Formosis](https://github.com/kevin00156/formosis) 的 `thesis-ntust` profile 編譯。
系所另有規定（封面、字級、行距、參考文獻格式等）時，以系所規定為準。

## Claude Code Skill

本專案啟用 `ntust-paper-writer` skill。請依照 skill 中的**臺科大論文格式規範**撰寫，
特別注意以下強制規範：

1. **章節錨點**：所有章節（`#` / `##` / `###` / `####`）後面必須加 `{#sec:...}` 標記
2. **禁用「——」破折號**：用頓號、逗號、括號或重新組句
3. **圖表編號**：用 `\label{}` + `\ref{}`，不要手寫「圖 1」、「表 2」
4. **參考文獻**：用 `[@key]` 引用，文獻條目放在 `references.bib`；寫法依系所或指導教授規定，全本統一
5. **章節階層**：`#` 第一章、`##` 一、、`###` (一)、`####` 1.、`#####` (1)；引用寫 `第\ref{sec:method}章第\ref{sec:method-overview}節`
6. **圖表標題不得使用縮寫**，文中須指明編號（如「見表1-1」）
7. **不要加浮水印**：電子檔由圖書館系統自動設定，YAML 不要設 `watermark:`
8. **上傳電子檔前**：在 `paper.md` 把 `\printversiontrue` 改為 `\printversionfalse`，讓前三頁依序為封面、推薦書、審定書
9. **生成式 AI**：用 AI 生成論文內容（單純文字潤飾除外）須明確標註使用內容、動機與範圍

## 編譯

從 Formosis 專案根目錄執行（假設此論文資料夾在 Formosis 子目錄）：

- Windows: `..\scripts\build.ps1 paper.md`
- Linux/macOS: `../scripts/build.sh paper.md`

或使用 VS Code 任務面板（Ctrl+Shift+B）。

## 文獻管理

新增或引用文獻一律遵守（以下 `python3` 在 Windows 上改用 `python`）：

1. **絕不憑記憶捏造 BibTeX 條目或 citekey**，也不要手動編輯 `references.bib`
2. 先在 `references.bib` 找是否已有該文獻（比對 DOI 或標題）；有就直接用它的 citekey
3. 沒有的話，用 DOI 或 arXiv ID 加入：

   ```bash
   python3 ../scripts/cite.py add <DOI 或 arXiv ID> --md paper.md
   ```

   stdout 印出的就是 citekey，寫成 `[@key]`。同一指令會自動判斷：YAML 有 `zotero-collection:` 且裝了 `zotero-cli` 時加進使用者的 Zotero 文獻庫，否則直接寫入 `references.bib`
4. **只有標題、沒有 DOI**：先上網查出 DOI，確認標題、作者、年份都相符再執行步驟 3；若有 `zotero-cli` 也可用 `zotero-cli --json search <關鍵字>` 查使用者的文獻庫
5. 查不到 DOI 的文獻（多數中文期刊、臺灣學位論文、書籍）：請使用者用 Zotero Connector 抓取，再執行 `python3 ../scripts/cite.py sync paper.md`
6. `cite.py add` 回報錯誤時，把錯誤訊息轉告使用者，不要改用手寫條目繞過

## 開始撰寫

1. 編輯 `paper.md` 開頭 YAML 區塊，替換所有 `<placeholder>` 為實際內容（封面英文資訊在 `header-includes` 內）
2. 指導教授推薦書、學位考試委員審定書由學生資訊系統產生，簽名後以掃描檔替換 `paper.md` 內的佔位頁
3. 設定文獻來源（三選一，詳見 Formosis docs/03）：只用 DOI 加文獻、或在 YAML 設 `zotero-collection:` 由 Zotero 管理、或再加裝 Zotero MCP 讓 Claude 直接操作文獻庫
4. 撰寫各章節，記得每個章節都加 `{#sec:...}` 錨點
5. 編譯產生 PDF，檢視排版
