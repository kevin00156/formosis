# 陽明交大論文專案

本專案使用 [Formosis](https://github.com/kevin00156/formosis) 的 `thesis-nycu` profile（國立陽明交通大學）工作流撰寫。

## Claude Code Skill

本專案啟用 `nycu-paper-writer` skill。請依照 skill 中的**國立陽明交通大學學位論文格式規範**撰寫，
特別注意以下強制規範：

1. **章節錨點**：所有章節（`#` / `##` / `###` / `####`）後面必須加 `{#sec:...}` 標記
2. **禁用「——」破折號**：用頓號、逗號、括號或重新組句
3. **圖表編號**：用 `\label{}` + `\ref{}`，不要手寫「圖 1」、「表 2」
4. **參考文獻**：用 `[@key]` 引用，文獻條目放在 `references.bib`
5. **浮水印須自行加入**：自書名頁起每頁都要。從陽明交大圖書館下載 `Thesis_mark.png`（https://www.lib.nycu.edu.tw/nycu/download/6694），存成 `images/nycu-watermark.png`，再取消 `paper.md` YAML 中 `# watermark:` 的註解；封面不加（skeleton 已用 `\WatermarkOff` 處理）
6. **封面與書名頁是兩種版型**（附件 1、附件 2），年月為上傳電子論文之年月，民國與西元並列（由 YAML `year`、`month` 自動換算）
7. **前置頁順序**依陽明交大規範：封面、書名頁、審定同意書、誌謝、中文摘要、英文摘要、目錄、圖目錄、表目錄、正文；附錄之後必須放**學位論文發表形式確認書**（附件 5）

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

1. 編輯 `paper.md` 開頭 YAML 區塊與其後的英文資料 raw LaTeX 區塊（英文姓名、英文系所、英文學位名稱），替換所有 `<placeholder>` 為實際內容
2. 設定文獻來源（三選一，詳見 Formosis docs/03）：只用 DOI 加文獻、或在 YAML 設 `zotero-collection:` 由 Zotero 管理、或再加裝 Zotero MCP 讓 Claude 直接操作文獻庫
3. 撰寫各章節，記得每個章節都加 `{#sec:...}` 錨點
4. 編譯產生 PDF，檢視排版
5. 全校規範未訂內文字型、字級、行距與圖表格式，本骨架採慣例值；系所另有規定時以系所為準
