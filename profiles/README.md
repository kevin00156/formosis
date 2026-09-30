# profiles/

每個 profile 對應「**文件類型 × 機構／期刊／單位樣式**」的一種組合，命名格式 `<type>-<style>`：

| Profile | Type | Style |
|---------|------|-------|
| `thesis-ncu` | thesis | 國立中央大學 |
| `slides-ncu` | slides | 國立中央大學 |
| `thesis-ntu`（未來） | thesis | 國立臺灣大學 |
| `journal-ieee`（未來） | journal | IEEE |
| `report-gov-tw`（未來） | report | 政府機關報告書（台灣） |

## Type 與目錄結構

不同 type 的 profile 內含檔案略有差異，但都有 `profile.yaml` / `skeleton/` / `skill/`。

### `type: thesis`（Pandoc + XeLaTeX，共用模板）

學位論文 profile 共用 `shared/latex/thesis.latex`（Pandoc 模板）與 `shared/latex/twthesis.sty`（共用版面）。
各校只放與共用設定不同之處：

```
profiles/thesis-<school>/
├── profile.yaml         # template: ../../shared/latex/thesis.latex
├── thesisprofile.sty    # 學校差異：twthesis 選項 + 校名預設值 + 其他覆寫
├── skeleton/            # 封面、書名頁、前置頁順序（raw LaTeX）與使用者起點
│   ├── paper.md
│   ├── references.bib
│   ├── images/
│   └── CLAUDE.md
└── skill/
    └── SKILL.md
```

`twthesis.sty` 選項（在 `thesisprofile.sty` 以 `\RequirePackage[...]{twthesis}` 指定）：

| 選項 | 值 | 效果 |
|------|----|------|
| `chapnum` | `arabic` / `zh` / `zhenum` | 第1章 / 第一章 / 一、 |
| `secsep` | `.` / `-` | 節號 1.1 / 1-1 |
| `eqnum` | `section` / `continuous` | (1-1) / (1) |
| `fignum` | `continuous` / `section` / `subsection` | 圖1 / 圖1-1（分章）/ 圖1-1-1（分章節） |
| `caplabelsep` | `space` / `period` | 圖1 標題 / 圖1. 標題 |
| `lofprefix` | `true` / `false` | 圖目錄條目前加「圖 」「表 」 |
| `urldate` | `true` / `false` | `false` 時參考文獻不印瀏覽日期 |

學校要求**學生自行加浮水印**時（臺大、陽明交大、北科大、中正等），在 paper.md YAML 設 `watermark: <圖檔>`；預設置中、寬為紙寬 1/3，位置不同的學校在 `thesisprofile.sty` 重新定義 `\TwthesisWatermarkPlace`，不該有浮水印的頁面前後用 `\WatermarkOff` / `\WatermarkOn`。由圖書館系統加浮水印的學校不要設。

改 `twthesis.sty` 會影響所有學校：CI 會編譯每個 profile 的 skeleton，但版面是否仍正確要人工看過 PDF。

### `type: journal` / `report`（Pandoc + XeLaTeX）

```
profiles/<profile>/
├── profile.yaml         # 元資料：name, type, style, defaults
├── template.latex       # Pandoc LaTeX 模板（profile.yaml 的 template: 欄位可改指其他路徑）
├── skeleton/            # 使用者 cp -r 當論文起點
│   ├── paper.md
│   ├── references.bib
│   ├── images/
│   └── CLAUDE.md
└── skill/
    └── SKILL.md         # 撰寫規範（章節錨點、字型、禁用語法等）
```

編譯：`./scripts/build.sh --profile <name> path/to/paper.md`

### `type: slides`（Marp）

```
profiles/<profile>/
├── profile.yaml         # 元資料：name, type, style, defaults
├── theme.css            # Marp 主題 CSS（保守學術配色）
├── skeleton/            # 使用者 cp -r 當簡報起點
│   ├── slides.md
│   ├── theme.css        # 個人化主題微調（@import 主題後 override）
│   ├── assets/
│   ├── Makefile
│   └── CLAUDE.md
└── skill/
    └── SKILL.md         # 撰寫規範（頁數上限、字數限制、視覺優先等）
```

編譯：`./scripts/build-slides.sh --profile <name> path/to/slides.md`

## 格式來源（`source:`）

各校、各系所甚至各實驗室的論文規範常有差異，profile 必須寫明它依據什麼：

```yaml
source:
  status: derived        # verified = 已對照校方正式條文；derived = 依實際論文或系所範本推得
  basis: 國立中正大學機械工程學系實驗室學長通過口試之論文 Word 檔
  url: <規範文件網址，若有>
  note: 非校方正式規範，其他系所請與系辦確認。
```

分層原則：

- **學校**：`thesisprofile.sty` + skeleton，放在本 repo
- **系所**：有正式文件時才另開 profile（例 `thesis-ccu-me`），只需約 20 行的 `thesisprofile.sty` 加一份 skeleton
- **實驗室／個人慣例**：寫在自己論文 `paper.md` 的 `header-includes`，不進本 repo

## 新增一個 profile

### 新增論文 profile（例：thesis-ntu）

1. `cp -r profiles/thesis-ncu profiles/thesis-ntu`
2. 編輯 `profile.yaml` 的 `name`、`style`、`description`
3. 改 `thesisprofile.sty`：`\ProfileUniversityZh` 校名、`twthesis` 選項；共用選項表達不了的差異（例如章標題字級）直接寫在選項之後覆寫
4. 改 `skeleton/paper.md` 的封面 raw LaTeX 區塊與 YAML（邊界、字型、行距）
5. 改 `skill/SKILL.md` 的字型 / 封面 / 格式規範與 frontmatter `name:`
6. 用 `./scripts/build.sh --profile thesis-ntu profiles/thesis-ntu/skeleton/paper.md` 測試

### 新增簡報 profile（例：slides-ntu）

1. `cp -r profiles/slides-ncu profiles/slides-ntu`
2. 編輯 `profile.yaml` 的 `name`、`style`、`description`
3. 改 `theme.css` 的配色與字型
4. 改 `skeleton/slides.md` 的 frontmatter（footer、title）
5. 改 `skill/SKILL.md` 的口試 / 報告規範與 frontmatter `name:`
6. 用 `./scripts/build-slides.sh --profile slides-ntu profiles/slides-ntu/skeleton/slides.md` 測試
