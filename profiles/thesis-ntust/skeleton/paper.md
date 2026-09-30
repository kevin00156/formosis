---
profile: thesis-ntust  # Formosis 編譯時自動套用此 profile（可被 CLI --profile 覆寫）

# ============================================================
# === 臺科大論文基本資訊（請替換以下 placeholder） ===
# ============================================================
thesis-title-zh: "<您的論文中文題目，請替換>"
thesis-title-en: "<Your thesis title in English, please replace>"
department: "<您的系所，例如：機械工程系>"
degree: "碩士論文"                  # 或 "博士論文"
student: "<研究生中文姓名，請替換>"
advisor: "<指導教授中文姓名，請替換> 博士"   # 學位名稱或職銜，例如「博士」「教授」
year: "<民國年，如115>"          # 7、8 月辦理離校者，封面年月印「○○年 6 月」
month: "<月，如6>"

# ============================================================
# === 封面英文資訊（YAML 沒有對應欄位，以 LaTeX 巨集定義） ===
# ============================================================
header-includes:
  - |
    ```{=latex}
    \newcommand{\DepartmentEn}{<Department of ...>}      % 或 Graduate Institute of ...
    \newcommand{\DegreeEn}{Master Thesis}                % 博士：Doctoral Dissertation
    \newcommand{\StudentNameEn}{<First-Name Last-Name>}
    \newcommand{\AdvisorNameEn}{<First-Name Last-Name> (Ph.D.)}   % (DEGREE) 或 (TITLE)
    \newcommand{\MonthYearEn}{<June 2026>}               % 英文月份 + 西元年
    ```

# ============================================================
# === 圖片子圖支援 ===
# ============================================================
subfigure: true

# ============================================================
# === 紙張與邊界（編排規則二(三)：上 3、下 2、左右各 3 cm；頁碼正下方置中） ===
# ============================================================
# 頁碼距底距離條文未規定，footskip 1cm 使頁碼基線距紙張底約 1 cm
geometry: "top=3cm, bottom=2cm, left=3cm, right=3cm, footskip=1cm"
papersize: a4
classoption: [fleqn]
# 浮水印：電子檔由圖書館系統自動加入，請勿設定 watermark:

# ============================================================
# === 字體設定（編排規則二(二)：中文標楷體或新細明體，英文 Times New Roman） ===
# ============================================================
# 若系統無「標楷體」（常見於 Linux/macOS），改用免費楷體 "AR PL UKai TW"（apt: fonts-arphic-ukai）
# 或國發會「全字庫正楷體」TW-Kai
mainfont: "Times New Roman"
CJKmainfont: "標楷體"
# 標楷體沒有粗體字重；條文要求章標題、摘要等標題、書名頁題目加粗，以 xeCJK 偽粗體呈現
CJKoptions:
  - "AutoFakeBold=2.5"
fontsize: 12pt                    # 內文 12pt 或 13pt 為原則（四(八)2）
linestretch: 1.5                  # 1.5 倍行高（四(八)2）

# ============================================================
# === 引用/參考文獻（biblatex + biber） ===
# 參考文獻寫法依系所或指導教授規定（APA、MLA、Chicago 等），全本須統一；請依規定改 biblio-style
# ============================================================
bibliography: references.bib
# zotero-collection: "我的論文"   # 取消註解 = 由 Zotero 管理 .bib，編譯前自動從 Better BibTeX 同步
biblatex: true
biblio-style: ieee
suppress-bibliography: true       # 文末手動 \printbibliography 控制位置

# ============================================================
# === 頁碼與標題設定 ===
# ============================================================
numbersections: true
secnumdepth: 5                    # 編號階層：第一章、一、(一)、1.、(1)，對應 # 到 #####
toc: false                        # 手動插入 \tableofcontents

# ============================================================
# === 自訂 LaTeX 設定 ===
# 章節格式、頁碼、圖表編號等已由 profile thesis-ntust 的 thesisprofile.sty
# （與共用的 twthesis.sty）提供，無需在此重抄。要新增實驗數據變數等，
# 加在上方 header-includes 的 latex 區塊內即可，例如：
#     \def\experimentTotal{1000}
#     \def\experimentCorrect{950}
#     \FPeval{\experimentAccuracy}{round(\experimentCorrect/\experimentTotal*100:2)}
# ============================================================
---

<!-- ============================================================ -->
<!-- 封面版型（編排規則附錄一，格式僅供參考，以各系所規定為準） -->
<!-- 上留白 4 cm、下留白 3 cm，各行置中；中文楷書、英文 Times New Roman -->
<!-- 參數 #1：題目字級。封面依附錄一 18pt；書名頁依二(二)「論文內頁之論文題目 24pt 加粗」 -->
<!-- ============================================================ -->

```{=latex}
\newcommand{\NtustCover}[1]{%
\begin{titlepage}
\linespread{1.5}% 封面各行 1.5 倍行高，不受 YAML linestretch 影響
\begin{center}
\vspace*{1cm}% 上邊界 3 cm + 1 cm = 上留白 4 cm
{\fontsize{18pt}{21.6pt}\selectfont \UniversityZh\Department\par
\Degree\par}
{\fontsize{14pt}{16.8pt}\selectfont \DepartmentEn\par}
{\fontsize{16pt}{19.2pt}\selectfont National Taiwan University of Science and Technology\par
\DegreeEn\par}
\vfill
{#1\ThesisTitleZh\par}
{#1\ThesisTitleEn\par}
\vfill
{\fontsize{18pt}{21.6pt}\selectfont \StudentName\par
\StudentNameEn\par
\vspace{18pt}
指導教授：\AdvisorName\par
Advisor: \AdvisorNameEn\par}
\vfill
{\fontsize{18pt}{21.6pt}\selectfont 中華民國\ROCYear 年\ROCMonth 月\par
\MonthYearEn\par}
\vspace*{1cm}% 下邊界 2 cm + 1 cm = 下留白 3 cm
\end{center}
\end{titlepage}}
% 紙本論文：封面 > 書名頁 > 推薦書 > 審定書（編排規則第三點）
% 上傳電子檔：圖書館要求前三頁依序為封面 > 推薦書 > 審定書，中間不得有空白頁，
%             請把下一行改成 \printversionfalse 以略過書名頁
\newif\ifprintversion
\printversiontrue
```

<!-- 封面（無頁碼） -->

\NtustCover{\fontsize{18pt}{21.6pt}\selectfont}

<!-- 書名頁：內容同封面，題目 24pt 加粗（上傳電子檔時略過，見上方 \printversionfalse） -->

```{=latex}
\ifprintversion
\NtustCover{\fontsize{24pt}{28.8pt}\selectfont\bfseries}
\fi
```

<!-- ============================================================ -->
<!-- 指導教授推薦書、學位考試委員審定書（附錄二、三）：由學生資訊系統產生並簽名後， -->
<!-- 掃描成 A4 圖檔或 PDF 替換下列佔位頁，例如 -->
<!-- \noindent\includegraphics[width=\textwidth]{images/recommendation.pdf} -->
<!-- 這兩頁不印頁碼 -->
<!-- ============================================================ -->

\thispagestyle{empty}

\begin{center}
<請以學生資訊系統產生、所有指導教授簽名之指導教授推薦書替換此頁>
\end{center}

\newpage

\thispagestyle{empty}

\begin{center}
<請以學生資訊系統產生、全體委員簽名之學位考試委員審定書替換此頁>
\end{center}

\newpage

<!-- ============================================================ -->
<!-- 中文摘要至圖表目錄：大寫羅馬數字頁碼 I, II, III ...（二(三)） -->
<!-- ============================================================ -->

\pagenumbering{Roman}
\pagestyle{frontmatter}

<!-- 中文摘要（附錄四）：關鍵詞 5–7 個，不超過 500 字或一頁 -->

\phantomsection
\addcontentsline{toc}{section}{中文摘要}

\begin{center}
{\fontsize{16pt}{19.2pt}\selectfont \ThesisTitleZh\par}
\vspace{6pt}
研究生：\StudentName\par
指導教授：\AdvisorName\par
時間：\ROCYear 年\ROCMonth 月\par
\end{center}

\section*{論文摘要}

<請在此撰寫中文摘要，不超過 500 字或一頁為原則。內容應包含論述重點、研究方法、研究內容及研究結果等。>

\vspace{1cm}

\noindent 關鍵詞：<關鍵詞 1>、<關鍵詞 2>、<關鍵詞 3>、<關鍵詞 4>、<關鍵詞 5>

\newpage

<!-- 英文摘要（附錄五） -->

\phantomsection
\addcontentsline{toc}{section}{英文摘要}

\begin{center}
{\fontsize{16pt}{19.2pt}\selectfont \ThesisTitleEn\par}
\end{center}

\section*{ABSTRACT}

<Write the English abstract here, one page in principle. It should mirror the Chinese abstract.>

\vspace{1cm}

\noindent Keywords: <Keyword 1>, <Keyword 2>, <Keyword 3>, <Keyword 4>, <Keyword 5>

\newpage

<!-- 誌謝（附錄六） -->

\phantomsection
\addcontentsline{toc}{section}{誌謝}
\section*{誌\quad 謝}

<請在此撰寫誌謝詞。所有對於研究提供協助之人或機構，都可在此表達感謝之意。>

\newpage

<!-- 目錄（附錄七） -->

\tableofcontents

\newpage

<!-- 符號索引（有使用符號時）：取消註解使用 -->
<!--
\phantomsection
\addcontentsline{toc}{section}{符號索引}
\section*{符號索引}

\newpage
-->

<!-- 圖目錄、表目錄：全文圖表五個以上（含）才須製作（四(七)），不足時可刪除 -->

\phantomsection
\addcontentsline{toc}{section}{圖目錄}
\listoffigures

\newpage

\phantomsection
\addcontentsline{toc}{section}{表目錄}
\listoftables

\newpage

<!-- ============================================================ -->
<!-- 正文開始（阿拉伯數字頁碼） -->
<!-- ============================================================ -->

\pagenumbering{arabic}
\pagestyle{mainmatter}

# 緒論 {#sec:intro}

## 研究背景 {#sec:intro-background}

<請在此撰寫研究背景。簡述問題領域的現況、重要性，以及為什麼這個題目值得研究。可引用文獻：[@vaswani2017attention]。>

## 研究動機與目的 {#sec:intro-motivation}

<請說明研究動機（觀察到什麼問題、現有方法的不足）與研究目的（你想解決什麼、達成什麼）。>

### 研究動機 {#sec:intro-motivation-why}

<第三層標題編號為 (一)。>

#### 現有方法的不足 {#sec:intro-motivation-why-gap}

<第四層標題編號為 1.，第五層（#####）為 (1)。>

### 研究目的 {#sec:intro-motivation-goal}

<請說明本研究要解決的問題與預期成果。>

## 研究貢獻 {#sec:intro-contribution}

<請條列本論文的主要貢獻，建議 2-4 點。>

1. **<貢獻一，請替換>**：<簡述貢獻內容，請替換>
2. **<貢獻二，請替換>**：<簡述貢獻內容，請替換>
3. **<貢獻三，請替換>**：<簡述貢獻內容，請替換>

## 論文架構 {#sec:intro-structure}

本論文共分為五章。第\ref{sec:literature}章回顧相關文獻；第\ref{sec:method}章說明所提方法；第\ref{sec:results}章呈現實驗結果與討論；第\ref{sec:conclusion}章總結本研究並提出未來工作方向。

# 文獻探討 {#sec:literature}

## 相關主題一 {#sec:literature-topic1}

<請在此回顧該主題的相關研究。引用文獻範例：[@vaswani2017attention; @he2016resnet]。>

## 相關主題二 {#sec:literature-topic2}

<請在此回顧另一個主題的相關研究。>

## 小結 {#sec:literature-summary}

<簡述文獻回顧的整體發現，以及本研究與既有研究的差異。>

# 研究方法 {#sec:method}

## 系統概述 {#sec:method-overview}

<請說明你的方法整體架構。可插入系統流程圖：>

<!--
範例：插入單張圖片（圖名在圖下方）

![系統架構流程](images/system_overview.png){#fig:system-overview width=80%}

範例：插入單張大圖（精確控制尺寸）
\begin{figure}[!htbp]
\centering
\includegraphics[width=1\textwidth,height=0.9\textheight,keepaspectratio]{images/system_overview.png}
\caption{系統架構流程}
\label{fig:system-overview}
\end{figure}
-->

如圖\ref{fig:system-overview}所示，本研究的整體架構分為三個主要模組。

## 方法一 {#sec:method-approach1}

<請說明第一個方法元件的細節。可插入公式：>

公式\ref{eq:example-formula}定義了核心運算：

\begin{equation}
y = f(x; \theta) + \epsilon
\label{eq:example-formula}
\end{equation}

## 方法二 {#sec:method-approach2}

<請說明第二個方法元件。>

# 實驗結果與討論 {#sec:results}

## 實驗設定 {#sec:results-setup}

<請說明：資料集、評估指標、實驗環境、超參數設定。可用表格呈現：>

<!--
範例 LaTeX 表格（表名在表上方）：
\begin{table}[htbp]
\centering
\caption{實驗超參數設定}
\label{tab:hyperparameters}
\small
\begin{tabular}{ll}
\hline
\textbf{超參數} & \textbf{值} \\
\hline
學習率 (Learning Rate) & 1e-4 \\
批次大小 (Batch Size)  & 32 \\
訓練週期 (Epochs)      & 100 \\
最佳化器 (Optimizer)   & AdamW \\
\hline
\end{tabular}
\end{table}
-->

實驗超參數設定如表\ref{tab:hyperparameters}所示。

## 主要結果 {#sec:results-main}

<請呈現主要實驗結果。建議搭配表格與圖表。>

## 消融研究 {#sec:results-ablation}

<請說明各元件對性能的貢獻。>

## 討論 {#sec:results-discussion}

<請分析結果背後的意義、與現有方法的比較、模型的限制等。>

# 結論與未來工作 {#sec:conclusion}

## 結論 {#sec:conclusion-summary}

<請總結本論文的研究成果與貢獻。>

## 未來工作 {#sec:conclusion-future}

<請說明本研究可能的延伸方向。>

<!-- ============================================================ -->
<!-- 參考文獻（Pandoc + biblatex 自動產生，列入目錄） -->
<!-- ============================================================ -->

\newpage
\printbibliography[title=參考文獻, heading=bibintoc]

<!-- 附錄（選填）。電子檔請勿放自傳、電話、Email 等個資 -->
