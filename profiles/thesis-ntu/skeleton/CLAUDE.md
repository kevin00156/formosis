# 國立臺灣大學學位論文專案

本專案依〈國立臺灣大學碩、博士學位論文格式規範〉（112.10.20 版）撰寫，使用 [Formosis](https://github.com/kevin00156/formosis) 的 `thesis-ntu` profile 編譯。

## Claude Code Skill

本專案啟用 `ntu-paper-writer` skill。請依照 skill 中的**臺大學位論文格式規範**撰寫，
特別注意以下強制規範：

1. **章節錨點**：所有章節（`#` / `##` / `###` / `####`）後面必須加 `{#sec:...}` 標記
2. **禁用「——」破折號**：用頓號、逗號、括號或重新組句
3. **圖表編號**：用 `\label{}` + `\ref{}`，不要手寫「圖 1」、「表 2」；章的引用寫 `第\ref{sec:xxx}章`（不留空白）
4. **參考文獻**：用 `[@key]` 引用，文獻條目放在 `references.bib`
5. **目次、圖次、表次**：名稱不可改回「目錄」；所有前置頁都要列進目次
6. **摘要**：中、英文摘要各不超過三頁，關鍵詞 5–7 個

## 臺大特有：浮水印與 DOI 要自己加

- 浮水印：從 https://www.lib.ntu.edu.tw/doc/CL/watermark.pdf 下載，存成 `images/ntu-watermark.pdf`，在 `paper.md` YAML 取消註解 `watermark:` 那一行（學校浮水印檔不要推到公開 repo）
- DOI：從臺大博碩士論文提交系統複製（含 `doi:` 前綴），在 YAML 取消註解 `header-includes` 的 `\ThesisDOI` 並填入
- PDF 保全（限制編輯）要在編譯後另用 Acrobat 或計中 VDI 的 Foxit PDF Editor 設定
- 以英文撰寫論文時，YAML 的 `linestretch` 改為 2（規範：英文雙行間距）

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

1. 編輯 `paper.md` 開頭 YAML 區塊與封面區塊，替換所有 `<placeholder>` 為實際內容（學院、系所用完整名稱）
2. 設定文獻來源（三選一，詳見 Formosis docs/03）：只用 DOI 加文獻、或在 YAML 設 `zotero-collection:` 由 Zotero 管理、或再加裝 Zotero MCP 讓 Claude 直接操作文獻庫
3. 撰寫各章節，記得每個章節都加 `{#sec:...}` 錨點
4. 編譯產生 PDF，檢視排版；上傳前加入浮水印、DOI 並設定 PDF 保全
