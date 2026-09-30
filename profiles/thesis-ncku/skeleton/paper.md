---
profile: thesis-ncku  # Formosis 編譯時自動套用此 profile（可被 CLI --profile 覆寫）

# ============================================================
# === 成大論文基本資訊（請替換以下 placeholder） ===
# 封面須列：校名、系（所、學位學程）別、論文名稱、中英文題目、研究生、指導教授、
# 年月（學位考試通過日期）。英文姓名、學院等延伸摘要用的欄位在下方 raw LaTeX 區塊。
# ============================================================
thesis-title-zh: "<您的論文中文題目>"
thesis-title-en: "<Your Thesis Title in English>"
department: "<您的系（所、學位學程），例如：機械工程學系>"
degree: "碩士論文"                  # 或 "博士論文"
student: "<您的姓名>"
advisor: "<指導教授姓名> 博士"
year: "<學位考試通過之民國年，例如：115>"
month: "<學位考試通過之月份，例如：6>"

# ============================================================
# === 圖片子圖支援 ===
# ============================================================
subfigure: true

# ============================================================
# === 紙張與邊界（格式規範第一、六點） ===
# A4；內頁上 23 mm、下 35 mm（含頁碼）、左 30 mm、右 25 mm。封面邊界另訂，見封面區塊。
# 浮水印與 DOI 由圖書館系統在審核通過後加入，請勿自行加入（不要設 watermark:）。
# ============================================================
geometry: "top=23mm, bottom=35mm, left=30mm, right=25mm"
papersize: a4
classoption: [fleqn]

# ============================================================
# === 字體設定（校級規範未規定主文字型、字級與行距，以下為慣例，請與系所確認） ===
# ============================================================
# 若系統無「標楷體」（常見於 Linux/macOS），改用免費楷體 "AR PL UKai TW"（apt: fonts-arphic-ukai）
# 或國發會「全字庫正楷體」TW-Kai；論文要求楷體，勿用明體（如 Noto Serif）替代
mainfont: "Times New Roman"
CJKmainfont: "標楷體"
fontsize: 12pt
linestretch: 1.5

# ============================================================
# === 引用/參考文獻（biblatex + biber） ===
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
secnumdepth: 4                    # 編號最深到 #### 第四層
toc: false                        # 手動插入 \tableofcontents

# ============================================================
# === 自訂 LaTeX 設定 ===
# 章節格式、頁碼、圖表編號、英文延伸摘要環境等已由 profile thesis-ncku 的
# thesisprofile.sty（與共用的 twthesis.sty）提供，無需在此重抄。如需 override 或新增實驗數據變數，
# 可加 header-includes 區塊（會 append 在 profile 預設之後）：
#
# header-includes:
#   - |
#     ```{=latex}
#     \def\experimentTotal{1000}
#     \def\experimentCorrect{950}
#     \FPeval{\experimentAccuracy}{round(\experimentCorrect/\experimentTotal*100:2)}
#     ```
# ============================================================
---

<!-- ============================================================ -->
<!-- 英文資料（英文延伸摘要使用，請替換 placeholder） -->
<!-- ============================================================ -->

```{=latex}
\newcommand{\StudentNameEn}{<Author's Name in English>}
\newcommand{\AdvisorNameEn}{<Advisor's Name in English>}
\newcommand{\DepartmentCollegeEn}{<Department of ..., College of ...>}
```

<!-- ============================================================ -->
<!-- 封面（無頁碼；規範第二點：直式封面邊界上 23、下 30、左 20、右 20 mm） -->
<!-- 年月為學位考試通過日期（第四點）；規範未指定民國或西元，此處用民國 -->
<!-- ============================================================ -->

\newgeometry{top=23mm, bottom=30mm, left=20mm, right=20mm}

\begin{titlepage}
\begin{center}

\vspace*{1.5cm}

{\fontsize{24pt}{28pt}\selectfont\bfseries \Spaced[0.5em]{\UniversityZh}}

\vspace{1cm}

{\fontsize{18pt}{24pt}\selectfont \Department}

\vspace{0.5cm}

{\fontsize{18pt}{24pt}\selectfont \Spaced[0.5em]{\Degree}}

\vfill

{\fontsize{20pt}{30pt}\selectfont\bfseries \ThesisTitleZh\par}

\vspace{0.8cm}

{\fontsize{16pt}{24pt}\selectfont\bfseries \ThesisTitleEn\par}

\vfill

{\fontsize{16pt}{22pt}\selectfont 研究生：\StudentName}

\vspace{0.4cm}

{\fontsize{16pt}{22pt}\selectfont 指導教授：\AdvisorName}

\vfill

{\fontsize{16pt}{22pt}\selectfont 中華民國\ROCYear 年\ROCMonth 月}

\vspace*{1cm}

\end{center}
\end{titlepage}

\restoregeometry

<!-- ============================================================ -->
<!-- 學位考試合格證明（規範第五點：裝訂於論文第二頁，無頁碼） -->
<!-- 請以考試委員、指導教授簽名後的證明掃描檔取代本頁，例如：            -->
<!--   \includegraphics[width=\textwidth]{images/approval.pdf}          -->
<!-- ============================================================ -->

\newpage
\thispagestyle{empty}

\begin{center}
{\Large\bfseries 學位考試合格證明}
\end{center}

\vspace{2cm}

\begin{center}
<請以系所提供、經考試委員與指導教授簽名之學位考試合格證明掃描檔取代本頁>
\end{center}

\newpage

<!-- ============================================================ -->
<!-- 中文摘要（羅馬數字頁碼 i, ii, iii ...；頁碼編法規範未規定，依慣例） -->
<!-- ============================================================ -->

\pagenumbering{roman}
\pagestyle{frontmatter}

\begin{center}
{\Large\bfseries 摘要}
\end{center}
\phantomsection\addcontentsline{toc}{section}{摘要}

<請在此撰寫中文摘要。摘要應包含：研究背景與動機、研究問題、所提方法、實驗結果與結論。>

\vspace{1cm}

\noindent\textbf{關鍵字：<關鍵字1>、<關鍵字2>、<關鍵字3>、<關鍵字4>、<關鍵字5>}

<!-- ============================================================ -->
<!-- 英文延伸摘要（規範備註三：中文撰寫之論文須附 800–1200 字，取代一頁英文摘要，   -->
<!-- 置於中文摘要之後）。格式：Times New Roman、單行間距、題目 14 pt 粗體、內文 12 pt； -->
<!-- 建議次序：Title、Author、Advisor、Department & College、SUMMARY（250 字內含    -->
<!-- 關鍵字，最多 5 個）、INTRODUCTION、MATERIALS AND METHODS、RESULTS AND        -->
<!-- DISCUSSION、CONCLUSION；可依領域慣例調整。                                     -->
<!-- 論文以英文撰寫時不需延伸摘要：刪除本區塊，改寫一頁英文 Abstract 即可。        -->
<!-- 圖的寫法（Figure 標題在圖下方，不列入圖目錄）：                               -->
<!--   \begin{figure}[H]\centering                                                 -->
<!--   \includegraphics[width=0.6\textwidth]{images/system_overview.png}           -->
<!--   \caption{<Figure caption>}\end{figure}                                       -->
<!-- ============================================================ -->

\begin{ExtendedAbstract}
\phantomsection\addcontentsline{toc}{section}{Extended Abstract}

\EATitle{\ThesisTitleEn}{\StudentNameEn}{\AdvisorNameEn}{\DepartmentCollegeEn}

\EAHeading{Summary}

<Summary of no more than 250 words: scope and objectives, methods, results, and principal conclusions. Do not cite references.>

Key words: <Key word 1>, <Key word 2>, <Key word 3>, <Key word 4>, <Key word 5>

\EAHeading{Introduction}

<Background, nature and scope of the problem, related literature, and main results of the study.>

\EAHeading{Materials and Methods}

<Methods or theories employed, in enough detail that the results could be reproduced.>

\EASubheading{<Subheading>}

<Details of one component of the method.>

\EAHeading{Results and Discussion}

<Research findings and their analysis. Refer to tables and figures by number, e.g., Table 1.>

\begin{table}[H]
\centering
\caption{<Table caption>}
\begin{tabular}{lc}
\hline
<Item> & <Value> \\
\hline
<Item> & <Value> \\
\hline
\end{tabular}
\end{table}

\EAHeading{Conclusion}

<Main points and their significance, limitations, relation to previous work, and implications.>

\end{ExtendedAbstract}

<!-- ============================================================ -->
<!-- 誌謝 -->
<!-- ============================================================ -->

\begin{center}
{\Large\bfseries 誌謝}
\end{center}
\phantomsection\addcontentsline{toc}{section}{誌謝}

<請在此撰寫誌謝詞。建議依序感謝：指導教授、口試委員、實驗室同學、家人。>

\newpage

<!-- ============================================================ -->
<!-- 目錄、表目錄、圖目錄（規範第七點：表目錄在圖目錄之前） -->
<!-- ============================================================ -->

\tableofcontents

\clearpage
\phantomsection
\addcontentsline{toc}{section}{表目錄}
\listoftables

\clearpage
\phantomsection
\addcontentsline{toc}{section}{圖目錄}
\listoffigures

<!-- ============================================================ -->
<!-- 符號說明（規範第七點列於圖目錄之後、主文之前；無符號可刪除本頁） -->
<!-- ============================================================ -->

\clearpage

\begin{center}
{\Large\bfseries 符號說明}
\end{center}
\phantomsection\addcontentsline{toc}{section}{符號說明}

\begin{center}
\begin{tabular}{ll}
\hline
符號 & 說明 \\
\hline
$x$ & <輸入變數> \\
$\theta$ & <模型參數> \\
$\epsilon$ & <雜訊項> \\
\hline
\end{tabular}
\end{center}

<!-- ============================================================ -->
<!-- 主文開始（阿拉伯數字頁碼） -->
<!-- ============================================================ -->

\clearpage
\pagenumbering{arabic}
\pagestyle{mainmatter}

# 緒論 {#sec:intro}

## 研究背景 {#sec:intro-background}

<請在此撰寫研究背景。簡述問題領域的現況、重要性，以及為什麼這個題目值得研究。可引用文獻：[@example-key]。>

## 研究動機與目的 {#sec:intro-motivation}

<請說明研究動機（觀察到什麼問題、現有方法的不足）與研究目的（你想解決什麼、達成什麼）。>

## 研究貢獻 {#sec:intro-contribution}

<請條列本論文的主要貢獻，建議 2-4 點。>

1. **<貢獻一>**：<簡述貢獻內容>
2. **<貢獻二>**：<簡述貢獻內容>
3. **<貢獻三>**：<簡述貢獻內容>

## 論文架構 {#sec:intro-structure}

<說明本論文後續各章節的安排。範例：>

本論文共分為五章。第\ref{sec:literature}章回顧相關文獻；第\ref{sec:method}章說明所提方法；第\ref{sec:results}章呈現實驗結果與討論；第\ref{sec:conclusion}章總結本研究並提出未來工作方向。

# 文獻探討 {#sec:literature}

## <第一個主題> {#sec:literature-topic1}

<請在此回顧該主題的相關研究。引用文獻範例：[@vaswani2017attention; @he2016resnet]。>

## <第二個主題> {#sec:literature-topic2}

<請在此回顧另一個主題的相關研究。>

## 小結 {#sec:literature-summary}

<簡述文獻回顧的整體發現，以及本研究與既有研究的差異。>

# 研究方法 {#sec:method}

## 系統概述 {#sec:method-overview}

<請說明你的方法整體架構。可插入系統流程圖：>

![系統架構流程](images/system_overview.png){#fig:system-overview width=80%}

如圖 \ref{fig:system-overview} 所示，本研究的整體架構分為三個主要模組。

## <方法一> {#sec:method-approach1}

<請說明第一個方法元件的細節。可插入公式：>

公式 \ref{eq:example-formula} 定義了核心運算：

\begin{equation}
y = f(x; \theta) + \epsilon
\label{eq:example-formula}
\end{equation}

## <方法二> {#sec:method-approach2}

<請說明第二個方法元件。>

# 實驗結果與討論 {#sec:results}

## 實驗設定 {#sec:results-setup}

<請說明：資料集、評估指標、實驗環境、超參數設定。可用表格呈現：>

\begin{table}[htbp]
\centering
\caption{<實驗超參數設定>}
\label{tab:hyperparameters}
\begin{tabular}{ll}
\hline
\textbf{超參數} & \textbf{值} \\
\hline
學習率 (Learning Rate) & <1e-4> \\
批次大小 (Batch Size)  & <32> \\
訓練週期 (Epochs)      & <100> \\
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
<!-- 參考文獻（Pandoc + biblatex 自動產生；排列方式依系所慣例，規範第七點附註） -->
<!-- ============================================================ -->

\printbibliography[title=參考文獻, heading=bibintoc]

<!-- ============================================================ -->
<!-- 附錄（無附錄可刪除） -->
<!-- ============================================================ -->

# 附錄 {#sec:appendix .unnumbered}

<請在此放置大量數據、推導或其他補充資料。>
