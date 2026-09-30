# 03 — 文獻管理：DOI 自動補、Zotero 同步、Zotero MCP

PaperForge 用 `references.bib` 存放參考文獻，`paper.md` 以 `[@citekey]` 引用。維護這個檔案有三種方式，**由簡到繁、可以逐步升級**：

| 方式 | 需要安裝 | 適合 | 你要做的事 |
|------|----------|------|------------|
| **A. 只用 DOI** | 無 | 文獻多為英文期刊、會議、arXiv | 貼 DOI 或 arXiv ID，一行指令加入 |
| **B. Zotero 同步** | Zotero + Better BibTeX | 已有 Zotero 文獻庫、有中文文獻或書籍 | 用瀏覽器一鍵抓文獻，編譯時自動同步 |
| **C. Claude 操作文獻庫** | B + Zotero MCP | 想讓 Claude 自己找文獻、加入、引用 | 跟 Claude 說「幫我引用 ResNet 那篇」 |

> 💡 三種方式產生的都是同一個 `references.bib`，隨時可以升級。從 A 換到 B 時，把現有 `references.bib` 匯入 Zotero（`File` → `Import...`）即可。

## 方式 A：只用 DOI（不需 Zotero）

在論文資料夾外、PaperForge 根目錄執行：

```bash
# Linux/macOS
python3 scripts/cite.py add 10.1109/CVPR.2016.90 1706.03762 --md my-thesis/paper.md
# 或
make cite ID="10.1109/CVPR.2016.90 1706.03762" INPUT=my-thesis/paper.md

# Windows
python scripts\cite.py add 10.1109/CVPR.2016.90 1706.03762 --md my-thesis\paper.md
```

輸出：

```
  OK   he2016deep ← 10.1109/CVPR.2016.90
  OK   vaswani2017attention ← 10.48550/arXiv.1706.03762
  OK   已寫入 my-thesis/references.bib（新增 2 筆）
he2016deep
vaswani2017attention
```

最後兩行就是 citekey，直接在 `paper.md` 寫 `[@he2016deep]` 即可。

- **接受的格式**：DOI（`10.xxxx/...`、`doi:...`、`https://doi.org/...`）、arXiv ID（`1706.03762`、`arXiv:1706.03762v5`、`https://arxiv.org/abs/...`）
- **citekey 規則**：`第一作者姓 + 年份 + 題目第一個實詞`，全小寫；撞名時自動加 `a`、`b`
- **去重**：同一 DOI 已存在時不會重複加入，而是印出既有 citekey
- **限制**：沒有 DOI 的文獻（多數中文期刊、臺灣學位論文、書籍）無法用這個方式取得，請改用方式 B

## 方式 B：Zotero 同步

Zotero 是免費開源的文獻管理工具，搭配 Better BibTeX 擴充可產生穩定的 citekey。PaperForge 會在**每次編譯前**自動從 Zotero 拉最新的 `.bib`，不需要在 Zotero 裡設定匯出。

### Step 1：安裝 Zotero

從官網下載安裝：<https://www.zotero.org/download/>

支援 Windows、macOS、Linux。安裝後可選擇是否註冊 Zotero 帳號（建議註冊，可雲端同步）。

![Zotero 主畫面](images/03-01-zotero-main-page.png)

### Step 2：安裝 Better BibTeX

1. 到 Better BibTeX GitHub 頁面下載最新 .xpi 檔：<https://github.com/retorquere/zotero-better-bibtex/releases>

   ![Better BibTeX GitHub 下載頁](images/03-02-zotero-github-download-page.png)

2. 在 Zotero 中：`Tools` → `Add-ons`

   ![Tools → Add-ons 路徑](images/03-03-zotero-add-on-path.png)

3. 點右上齒輪 → `Install Add-on From File...`

   ![Add-on 安裝介面](images/03-04-zotero-add-on-install.png)

4. 選剛下載的 .xpi

   ![選擇 xpi 檔](images/03-05-zotero-add-on-choose-xpi.png)

5. 重啟 Zotero，確認 Better BibTeX 已出現在 Add-ons 清單中

   ![安裝完成](images/03-06-zotero-add-on-installed.png)

### Step 3：設定 Citation Key 命名規則

`Edit` → `Preferences` → `Better BibTeX` → `Citation Keys` 標籤

![進入 Preferences](images/03-07-zotero-settings-path.png)

建議的 Citation key formula：

```
authEtAl + year + shorttitle(2,2)
```

範例結果：
- `vaswani2017AttentionAll` (Attention Is All You Need)
- `heResNet2016DeepResidual` (Deep Residual Learning for Image Recognition)

也可以選簡單版：

```
auth.lower + year
```

範例：
- `vaswani2017`
- `he2016`

注意如果同年多篇可能重複，會自動加 `a/b/c`。

![Better BibTeX / Citation Keys 設定介面](images/03-08-zotero-better-bibtex-setting.png)

設定完後，**右鍵點選現有文獻** → `Better BibTeX` → `Refresh BibTeX key`，把舊條目套用新規則。

### Step 4：建立論文 Collection

在 Zotero 主介面：

1. 左側欄右鍵 → `New Collection`

   ![新增 Collection](images/03-09-zotero-new-collection.png)

2. 命名（例如：「我的碩論」）

   ![Collection 命名](images/03-10-zotero-new-collection-naming.png)

3. 把所有要引用的文獻拖進此 collection（下一步會教如何用瀏覽器擴充快速抓取）

### Step 5：新增第一篇文獻到 Collection

> ⚠️ **重要**：Better BibTeX **不會匯出空的 Collection**，所以請先確保 Collection 至少有一篇文獻，再進行下一步。

最快的方式是使用 Zotero 的瀏覽器擴充（[Zotero Connector](https://www.zotero.org/download/connectors)）：

- **抓取論文頁面**（arXiv、IEEE、ACM、Springer 等學術資料庫）：點瀏覽器右上的 Zotero 圖示，它會自動辨識為論文並抓取完整 metadata（標題、作者、年份、DOI、PDF）

  ![瀏覽器擴充抓取論文](images/03-16-zotero-browser-plugin-usage-for-paper.png)

- **抓取一般網頁**：圖示會變成網頁／書本圖樣，可儲存為 webpage 或 book section

  ![瀏覽器擴充抓取一般網頁](images/03-15-zotero-browser-plugin-usage-for-common-page.png)

抓取時可在彈出視窗指定目標 Collection；若沒指定則先進 `My Library`，再手動拖進剛建立的 Collection 即可。

### Step 6：在 paper.md 指定 Collection

打開 `paper.md` 開頭的 YAML，把 `zotero-collection:` 那行取消註解，填入 Step 4 建立的 Collection 名稱：

```yaml
bibliography: references.bib
zotero-collection: "我的碩論"
```

- 子 Collection 用 `/` 分隔，例如 `"碩論/第二章"`
- 使用群組文獻庫（Group Library）時，另外加一行 `zotero-library: <群組 library ID>`；預設 `1` 是個人文獻庫

設定後：

- **每次編譯前**，`build.sh` / `build.ps1` 會從 Better BibTeX 拉這個 Collection 的最新內容，覆寫 `references.bib`
- **Zotero 沒開**時只會印一行警告，沿用現有的 `references.bib` 繼續編譯
- 想不編譯、只同步：`python3 scripts/cite.py sync my-thesis/paper.md`（或 `make cite-sync INPUT=my-thesis/paper.md`）

> ⚠️ 設了 `zotero-collection:` 後，`references.bib` 就歸 Zotero 管：手動修改或用方式 A 加入的條目，下次同步都會被覆蓋。`cite.py add` 偵測到這個設定時會直接拒絕寫入並提醒你。

### Step 7：驗證同步

1. 確認 Zotero 已開啟
2. 用瀏覽器擴充再抓一篇論文，存進你的 Collection
3. 在 `paper.md` 中用 `[@citation-key]` 引用它（citekey 可在 Zotero 條目右側資訊欄最上方看到）
4. 編譯，確認終端機印出「已從 Zotero 同步 N 筆文獻」，且 PDF 中出現引用編號與參考文獻列表

### 替代做法：Keep updated 自動匯出

如果你不想每次編譯時都要開著 Zotero，可以改用 Better BibTeX 的自動匯出：Zotero 在背景把 Collection 寫到 `references.bib`，編譯時完全不需要 Zotero。**使用這個做法時不要設定 `zotero-collection:`**。

1. 右鍵剛建立的 Collection → `Export Collection...`

   ![Export Collection 路徑](images/03-11-zotero-export-collection-path.png)

2. Format 選 **Better BibTeX**（不是 Better BibLaTeX）
3. 勾選 **Keep updated**
4. 點 OK

   ![Export Collection 設定](images/03-12-zotero-export-collection-setting.png)

   ![設定完成](images/03-13-zotero-export-collection-setting-complete.png)

5. 在彈出的儲存對話框中，導航到你的論文資料夾 `my-thesis/`，存檔名為 `references.bib`

   ![選擇路徑](images/03-14-zotero-export-collection-choose-path.png)

設定完成後，**每次在 Zotero 中新增/編輯文獻，`references.bib` 會自動更新**，無需手動操作。

> 💡 如果這一步跳出「Cannot export empty collection」或類似警告，代表 Step 5 還沒做完，回去先抓一篇文獻進 Collection 再回來匯出。

## 方式 C：讓 Claude 直接操作文獻庫（Zotero MCP）

讓 Claude 直接搜尋、新增、整理你的 Zotero 文獻庫：你說「幫我引用 ResNet 那篇」，Claude 會先查文獻庫裡有沒有，沒有就依 DOI 加進你的 Collection，同步 `.bib` 後寫入 `[@citekey]`。整個過程不必切到 Zotero 視窗。

PaperForge 推薦 [zotero-mcp](https://github.com/54yyyu/zotero-mcp)（MIT 授權、社群最活躍的 Zotero MCP 專案）。它有兩種介面：

| 介面 | 適合 | 說明 |
|------|------|------|
| **`zotero-cli` + skill**（推薦） | Claude Code | Claude 用命令列操作 Zotero，只在需要時載入說明，幾乎不佔 context |
| MCP server | Claude Desktop 等沒有終端機的 AI 工具 | 約 40 個工具常駐，每次對話都佔用約 13k token |

### 前置條件

- 完成方式 B（Zotero + Better BibTeX，且 `paper.md` 已設定 `zotero-collection:`）
- **Zotero 10 以上**（Zotero 10 起本機 API 才能寫入；更舊的版本只能透過雲端 Web API 寫入，見下方 FAQ）
- `uv`（`scripts/install.*` 已經幫你裝好；用 `uv --version` 確認）

### Step 1：開啟 Zotero 本機 API

Zotero → `Settings`（macOS 為 `Preferences`）→ `Advanced` → 勾選 **Allow other applications on this computer to communicate with Zotero**。

### Step 2：安裝 zotero-mcp

```bash
uv tool install zotero-mcp-server
```

> ⚠️ 套件名是 **`zotero-mcp-server`**。PyPI 上的 `zotero-mcp` 是另一個只能讀取的專案，不要裝錯。

### Step 3：授權寫入（一次性）

Zotero 開著的狀態下執行：

```bash
zotero-mcp authorize-local
```

Zotero 會跳出授權對話框，按 **Always Allow**。之後可用 `zotero-mcp authorize-local --status` 確認狀態。

### Step 4：讓 Claude 知道怎麼用

```bash
zotero-mcp install-skill --target claude-user
```

會在 `~/.claude/skills/zotero-cli/` 放入說明檔（與 PaperForge 各 profile 的 skill 放在同一處），Claude Code 在需要操作文獻庫時會自動讀取。只想對單一論文啟用時，改在論文資料夾執行 `zotero-mcp install-skill --target claude`。

### Step 5：驗證

```bash
zotero-cli config                       # 應該印出 Zotero 設定，而不是錯誤
python3 ../scripts/cite.py add 10.1109/CVPR.2016.90 --md paper.md
```

第二行指令偵測到 `zotero-collection:` 與 `zotero-cli` 後，會把論文加進你的 Zotero Collection，接著從 Better BibTeX 同步 `.bib`，最後印出 **Better BibTeX 產生的 citekey**。到 Zotero 裡應該能看到這篇論文。

> 💡 **不論用哪種方式，Claude 都只需要記一個指令 `cite.py add`**：沒設 Zotero 時寫進 `.bib`（方式 A），有 Zotero 與 zotero-cli 時加進文獻庫（方式 C）。各 profile 的 `CLAUDE.md` 已寫好這條規則。Zotero MCP / zotero-cli 另外提供搜尋文獻庫、讀 PDF 全文與註記等功能，Claude 會在你要求時使用。

### 替代：MCP server 設定

如果你用的是 Claude Desktop 這類沒有終端機的工具，改用 MCP server：

```bash
# Claude Code（僅限此論文專案）
claude mcp add zotero --scope project -e ZOTERO_LOCAL=true -- zotero-mcp serve
```

其他工具的設定可執行 `zotero-mcp setup-info` 查詢。

### 方式 C 常見問題

- **Zotero 9 以下能用嗎？** 讀取可以；寫入需要 Zotero 雲端的 API key：到 <https://www.zotero.org/settings/keys> 建立有寫入權限的 key，再執行 `zotero-mcp setup --no-local --api-key <KEY> --library-id <你的 userID>`。此時新增的條目會先進雲端，Zotero 桌面版同步後 Better BibTeX 才拿得到。建議直接升級到 Zotero 10。
- **`cite.py add` 說「已加入 Zotero，但找不到對應條目」**：Better BibTeX 產生 citekey 需要一點時間，稍等幾秒後執行 `cite.py sync paper.md`，再查 `references.bib`。
- **群組文獻庫（`zotero-library:` 不是 1）**：zotero-cli 預設操作個人文獻庫，群組文獻庫請用 Zotero Connector 新增。

## 進階：路徑包含中文

如果論文資料夾路徑含中文（例如 `D:\我的論文\`），某些版本 Better BibTeX 可能匯出失敗。建議：

- 把論文資料夾移到全英文路徑（推薦）
- 或在 Zotero `Preferences` → `Advanced` → `Config Editor` 中搜尋 `better-bibtex.autoExportDelay`，調大延遲時間

## 進階：多人協作論文

如果是多人合著、需共享 `.bib`：

1. **方案 A**：用 Git 追蹤 `references.bib`，每人各自 Zotero 匯出自己負責的部分
2. **方案 B**：用 Zotero Group Library，多人共用一個 Collection，分別在自己機器設定自動匯出
3. **方案 C**：把 `references.bib` 放到雲端（Dropbox/OneDrive），但只一人負責 Better BibTeX 匯出，其他人 read-only

## 常見問題

### Q: Better BibTeX 匯出的 .bib 中有 `file = {...}` 路徑欄位，會洩漏我的本機路徑

A: 在 `Preferences` → `Better BibTeX` → `Export` → `Fields` 中，把 `file` 加入 `omit fields` 清單。

或者在匯出後手動處理：

```bash
# 移除 file 欄位的簡單腳本
sed -i '/^\s*file\s*=/d' references.bib
```

### Q: Citation key 經常變動

A: 確保已在 Preferences 中勾選 `Citation Keys` → `On item change` → `Keep key when adding new items`。

### Q: 中文期刊條目顯示亂碼

A: 確認 .bib 檔以 UTF-8 編碼儲存（Better BibTeX 預設正確，但若手動編輯需注意）。

### Q: Pandoc 編譯時找不到引用

A: 確認 `paper.md` 的 YAML 中 `bibliography: references.bib` 路徑正確（相對於 paper.md 的位置）。

### Q: 匯出時跳「Cannot export empty collection」警告

A: Better BibTeX 不允許匯出空的 Collection。先依 Step 5 加入至少一篇文獻再匯出即可。

## 下一步

- 開始撰寫：[02-writing-workflow.md](02-writing-workflow.md)
- Pandoc 引用語法：[04-pandoc-syntax.md](04-pandoc-syntax.md#引用)
