---
profile: thesis-nthu  # Formosis 編譯時自動套用此 profile（可被 CLI --profile 覆寫）

# ============================================================
# === 清華論文基本資訊（請替換以下 placeholder） ===
# 封面各項中、英文並列（條例第三點）；英文系所、學號、英文姓名直接寫在下方封面區塊
# ============================================================
thesis-title-zh: "<填入：論文中文題目>"
thesis-title-en: "<Thesis title in English, to be filled>"
department: "<系所全名，例如：動力機械工程學系>"
degree: "碩士論文"                  # 或 "博士論文"
student: "<填入：研究生中文姓名>"
advisor: "<填入：指導教授中文姓名>"
year: "<民國年，例如：115>"         # 論文審定完成之年月；封面自動轉成中文數字（一一五）
month: "<月份，例如：6>"

# ============================================================
# === 浮水印：由清華博碩士論文庫在上傳後自動嵌入，不要自行加，勿設 watermark: ===
# ============================================================

# ============================================================
# === 圖片子圖支援 ===
# ============================================================
subfigure: true

# ============================================================
# === 紙張與邊距（條例第八點：上 3、下 2.5、左右各 3 公分） ===
# ============================================================
geometry: "top=3cm, bottom=2.5cm, left=3cm, right=3cm"
papersize: a4
classoption: [fleqn]

# ============================================================
# === 字體（條例第八點：中文 12 號標楷體、英文 12 號 Times New Roman，中英文皆 1.5 行距） ===
# ============================================================
# 若系統無「標楷體」（常見於 Linux/macOS），改用免費楷體 "AR PL UKai TW"（apt: fonts-arphic-ukai）
# 或國發會「全字庫正楷體」TW-Kai（清華官方 LaTeX 範本即用 TW-Kai）
mainfont: "Times New Roman"
CJKmainfont: "標楷體"
fontsize: 12pt
linestretch: 1.5

# ============================================================
# === 引用/參考文獻（biblatex + biber） ===
# 條例第十點：文中以括號夾註（作者，出版西元年份），格式可參考 APA 或系所指定格式
# ============================================================
bibliography: references.bib
# zotero-collection: "我的論文"   # 取消註解 = 由 Zotero 管理 .bib，編譯前自動從 Better BibTeX 同步
biblatex: true
biblio-style: apa                 # 系所指定其他格式時改這裡（例如 ieee）
suppress-bibliography: true       # 文末手動 \printbibliography 控制位置

# ============================================================
# === 頁碼與標題設定 ===
# ============================================================
numbersections: true
secnumdepth: 4                    # 編號最深到 #### 第四層
toc: false                        # 手動插入 \tableofcontents

# ============================================================
# === 自訂 LaTeX 設定 ===
# 章節格式、頁碼、圖表編號等已由 profile thesis-nthu 的 thesisprofile.sty 提供。
# 如需 override 或新增實驗數據變數，可加 header-includes 區塊：
#
# header-includes:
#   - |
#     ```{=latex}
#     \def\experimentTotal{1000}
#     ```
# ============================================================
---

```{=latex}
% ============================================================
% 封面（註冊組封面樣本：上下 2.54 公分、左右 3.18 公分）
% 校名、碩博士論文：置中 24 號、1.5 倍行高（字級不可改）
% 題目：置中 20–18 號、1.5 倍行高（題目太長可自行縮小）
% 系所別、學號、研究生、指導教授：左縮排 1.7 公分、18 號、1.5 倍行高
% 審定完成年月：置中 18 號、固定行高 24 點
% ============================================================
\newcommand{\NTHUCover}{%
\begin{titlepage}
\centering
\setstretch{1}

{\fontsize{24pt}{36pt}\selectfont \Spaced[1em]{\UniversityZh}\par
National Tsing Hua University\par}

\vspace{1.5cm}

{\fontsize{24pt}{36pt}\selectfont \Spaced[1em]{\Degree}\par
Master's Thesis\par}              % 博士論文改 Doctoral Dissertation

\vfill

{\fontsize{20pt}{30pt}\selectfont
\ThesisTitleZh\par
\ThesisTitleEn\par}

\vfill

{\raggedright\leftskip=1.7cm
\fontsize{18pt}{27pt}\selectfont
系所別：\Department\par
Dept./Grad. Inst.：<English Department Name>\par
學號 Student ID.：<學號>\par
研究生 Author：\StudentName\quad <English Name>\par
指導教授 Advisor：\AdvisorName\quad <Advisor English Name>\par}

\vfill

{\fontsize{18pt}{24pt}\selectfont
\Spaced[0.5em]{中華民國}\ \ZhYear{\ROCYear}\ 年\ \ZhMonth{\ROCMonth}\ 月\par
<June> <2026>\par}                % 英文月、西元年
\end{titlepage}}

% ============================================================
% 條例第一點：封面 → 1 頁空白頁 → 書名頁（內容同封面）
% ============================================================
\newgeometry{top=2.54cm, bottom=2.54cm, left=3.18cm, right=3.18cm}
\NTHUCover
\null\thispagestyle{empty}\newpage
\NTHUCover
\restoregeometry
\pagestyle{empty}
```

<!-- ============================================================ -->
<!-- 學位論文授權書、指導教授推薦書、考試委員審定書（條例第一點(四)～(六)） -->
<!-- 授權書至博碩士論文庫填寫列印、推薦書與審定書至校務資訊系統列印，簽名後掃描成 PDF， -->
<!-- 放進 images/ 並取消下方註解。這三份不編頁碼、不列入目次。 -->
<!-- ============================================================ -->

<!--
\includepdf[pages=-, pagecommand={\thispagestyle{empty}}]{images/authorization.pdf}
\includepdf[pages=-, pagecommand={\thispagestyle{empty}}]{images/advisor-recommendation.pdf}
\includepdf[pages=-, pagecommand={\thispagestyle{empty}}]{images/committee-approval.pdf}
-->

<!-- ============================================================ -->
<!-- 前置頁（羅馬數字頁碼 i, ii, iii ...，目次樣本） -->
<!-- 順序：中文摘要、英文摘要、誌謝、目次、圖次、表次，全部列入目次（條例第六點） -->
<!-- ============================================================ -->

\newpage
\pagenumbering{roman}
\pagestyle{frontmatter}

\phantomsection
\addcontentsline{toc}{section}{中文摘要}

\begin{center}
{\Large\bfseries 摘要}
\end{center}

<請在此撰寫中文摘要，以不超過一頁為原則。內容包括論述重點、方法或程序、結果及結論。>

\vspace{1cm}

\noindent 關鍵詞：<關鍵詞 1>、<關鍵詞 2>、<關鍵詞 3>、<關鍵詞 4>、<關鍵詞 5>

\newpage

\phantomsection
\addcontentsline{toc}{section}{ABSTRACT}

\begin{center}
{\Large\bfseries ABSTRACT}
\end{center}

<Write the English abstract here, preferably no more than one page. It should mirror the Chinese abstract in content.>

\vspace{1cm}

\noindent Keywords: <Keyword 1>, <Keyword 2>, <Keyword 3>, <Keyword 4>, <Keyword 5>

\newpage

\phantomsection
\addcontentsline{toc}{section}{誌謝}

\begin{center}
{\Large\bfseries 誌謝}
\end{center}

<請在此撰寫序言或誌謝辭（若無可免，刪除本頁與上方目次條目）。>

\newpage

\phantomsection
\addcontentsline{toc}{section}{目次}
\tableofcontents

\newpage

<!-- 圖次、表次：若無可免（條例第一點） -->

\phantomsection
\addcontentsline{toc}{section}{圖次}
\listoffigures

\newpage

\phantomsection
\addcontentsline{toc}{section}{表次}
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

## 研究貢獻 {#sec:intro-contribution}

<請條列本論文的主要貢獻，建議 2-4 點。>

1. **<貢獻 1>**：<填入：貢獻內容>
2. **<貢獻 2>**：<填入：貢獻內容>
3. **<貢獻 3>**：<填入：貢獻內容>

## 論文架構 {#sec:intro-structure}

<說明本論文後續各章節的安排。範例：>

本論文共分為五章。第\ref{sec:literature}章回顧相關文獻；第\ref{sec:method}章說明所提方法；第\ref{sec:results}章呈現實驗結果與討論；第\ref{sec:conclusion}章總結本研究並提出未來工作方向。

# 文獻探討 {#sec:literature}

## <主題 1> {#sec:literature-topic1}

<請在此回顧該主題的相關研究。引用文獻範例：[@vaswani2017attention; @he2016resnet]。>

## <主題 2> {#sec:literature-topic2}

<請在此回顧另一個主題的相關研究。>

## 小結 {#sec:literature-summary}

<簡述文獻回顧的整體發現，以及本研究與既有研究的差異。>

# 研究方法 {#sec:method}

## 系統概述 {#sec:method-overview}

<請說明你的方法整體架構。可插入系統流程圖（圖題在圖下方）：>

![系統架構流程](images/system_overview.png){#fig:system-overview width=80%}

如圖 \ref{fig:system-overview} 所示，本研究的整體架構分為三個主要模組。

## <方法 1> {#sec:method-approach1}

<請說明第一個方法元件的細節。可插入公式：>

公式 \ref{eq:example-formula} 定義了核心運算：

\begin{equation}
y = f(x; \theta) + \epsilon
\label{eq:example-formula}
\end{equation}

## <方法 2> {#sec:method-approach2}

<請說明第二個方法元件。>

# 實驗結果與討論 {#sec:results}

## 實驗設定 {#sec:results-setup}

<請說明：資料集、評估指標、實驗環境、超參數設定。可用表格呈現（表題在表上方）：>

\begin{table}[htbp]
\centering
\caption{實驗超參數設定}
\label{tab:hyperparameters}
\begin{tabular}{ll}
\hline
\textbf{超參數} & \textbf{值} \\
\hline
學習率 (Learning Rate) & <值> \\
批次大小 (Batch Size)  & <值> \\
訓練週期 (Epochs)      & <值> \\
\hline
\end{tabular}
\end{table}

實驗超參數設定如表 \ref{tab:hyperparameters} 所示。

## 主要結果 {#sec:results-main}

<請呈現主要實驗結果。建議搭配表格與圖表。>

## 討論 {#sec:results-discussion}

<請分析結果背後的意義、與現有方法的比較、模型的限制等。>

# 結論與未來工作 {#sec:conclusion}

## 結論 {#sec:conclusion-summary}

<請總結本論文的研究成果與貢獻。>

## 未來工作 {#sec:conclusion-future}

<請說明本研究可能的延伸方向。>

<!-- ============================================================ -->
<!-- 參考文獻（列進目次） -->
<!-- ============================================================ -->

\newpage
\printbibliography[title=參考文獻, heading=bibintoc]

<!--
附錄（若有）：參考文獻之後另起一頁，標題不編號但列進目次，例如
# 附錄 {#sec:appendix .unnumbered}
-->
