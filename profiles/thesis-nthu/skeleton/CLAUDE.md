# 國立清華大學學位論文專案

本專案依〈國立清華大學研究生畢業論文格式條例〉（114.05.29 修正）撰寫，使用 [Formosis](https://github.com/kevin00156/formosis) 的 `thesis-nthu` profile 編譯。

## Claude Code Skill

本專案啟用 `nthu-paper-writer` skill。請依照 skill 中的**清華學位論文格式規範**撰寫，
特別注意以下強制規範：

1. **章節錨點**：所有章節（`#` / `##` / `###` / `####`）後面必須加 `{#sec:...}` 標記
2. **禁用「——」破折號**：用頓號、逗號、括號或重新組句
3. **圖表編號**：用 `\label{}` + `\ref{}`，不要手寫「圖 3-1-2」；圖表放在某一節（`##`）之下，圖題在圖下、表題在表上；章的引用寫 `第\ref{sec:xxx}章`（不留空白）
4. **參考文獻**：用 `[@key]`（括號夾註）或 `@key`（作者當主詞）引用，文獻條目放在 `references.bib`，格式為 APA（作者，年份）
5. **摘要**：中、英文摘要各以一頁為原則，關鍵詞 5–7 個；誌謝在摘要之後

## 清華特有：浮水印由系統加

論文上傳博碩士論文庫後，系統會自動嵌入浮水印。**不要**在 `paper.md` 設 `watermark:`，也不要自行用其他工具加浮水印。
授權書（論文庫列印）、指導教授推薦書與考試委員審定書（校務資訊系統列印）簽名掃描後放進 `images/`，取消 `paper.md` 裡 `\includepdf` 那幾行的註解。

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

1. 編輯 `paper.md` 開頭 YAML 區塊與封面區塊，替換所有 `<placeholder>` 為實際內容（年月填阿拉伯數字，封面自動轉中文數字）
2. 設定文獻來源（三選一，詳見 Formosis docs/03）：只用 DOI 加文獻、或在 YAML 設 `zotero-collection:` 由 Zotero 管理、或再加裝 Zotero MCP 讓 Claude 直接操作文獻庫
3. 撰寫各章節，記得每個章節都加 `{#sec:...}` 錨點
4. 編譯產生 PDF，檢視排版，並檢查參考文獻中的中文作者姓名
