---
profile: thesis-nycu  # Formosis 編譯時自動套用此 profile（可被 CLI --profile 覆寫）

# ============================================================
# === 陽明交大論文基本資訊（請替換以下 placeholder） ===
# 英文姓名、英文系所與學位名稱在 YAML 之後的 raw LaTeX 區塊。
# year/month 為「上傳電子論文至圖書館論文系統」之年月（民國年、月份，填阿拉伯數字）；
# 封面與書名頁會自動轉成「中華民國一一五年六月」與「June 2026」。
# ============================================================
thesis-title-zh: "<您的論文中文題目>"
thesis-title-en: "<Your Thesis Title in English>"
department: "<您的系所，例如：資訊工程學系>"
degree: "碩士論文"                  # 或 "博士論文"
student: "<您的姓名>"
advisor: "<指導教授姓名>"
year: "<上傳論文之民國年，例如：115>"
month: "<上傳論文之月份，例如：6>"

# ============================================================
# === 圖片子圖支援 ===
# ============================================================
subfigure: true

# ============================================================
# === 紙張與邊界（格式規範三.1、三.2） ===
# A4；內文上 2.5、下 2.5、左 3、右 2 cm；頁碼在版面底端 1.5 cm 處置中
# （footskip=1cm：頁碼基線距紙張底端 2.5 − 1 = 1.5 cm）。封面、書名頁邊界另訂，見各頁區塊。
# ============================================================
geometry: "top=2.5cm, bottom=2.5cm, left=3cm, right=2cm, footskip=1cm"
papersize: a4
classoption: [fleqn]

# ============================================================
# === 浮水印（學生須自行加入） ===
# 圖書館規定自書名頁起至最後一頁每頁都要加浮水印（封面不加）。請從圖書館下載官方圖檔
# Thesis_mark.png（https://www.lib.nycu.edu.tw/nycu/download/6694；說明文件
# https://www.lib.nycu.edu.tw/nycu/download/6693），存成 images/nycu-watermark.png
# 後取消下一行註解。刷淡與大小已由 thesisprofile.sty 處理，不必自行調整圖檔。
# ============================================================
# watermark: images/nycu-watermark.png

# ============================================================
# === 字體設定（全校規範未訂內文字型、字級與行距，由系所另訂；以下為慣例，請與系所確認） ===
# 封面、書名頁依附件 1、2 用楷書與 Times New Roman。
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
# 章節格式、頁碼、圖表編號、年月換算、浮水印位置等已由 profile thesis-nycu 的
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
<!-- 英文資料（封面與書名頁使用，請替換 placeholder）                 -->
<!-- 英文姓名格式依附件 1、2 樣本為「姓, 名」。                        -->
<!-- 英文學位名稱須依註冊組「各學院、系所學位中英文名稱」。           -->
<!-- ============================================================ -->

```{=latex}
\newcommand{\StudentNameEn}{<Surname, Given-name>}
\newcommand{\AdvisorNameEn}{<Surname, Given-name>}
\newcommand{\DepartmentEn}{<Department of ...>}
\newcommand{\CollegeEn}{<College of ...>}
\newcommand{\DegreeTypeEn}{Master's Thesis}   % 博士：Doctoral Dissertation
\newcommand{\ThesisKindEn}{Thesis}            % 博士：Dissertation
\newcommand{\DegreeNameEn}{<Master of ...>}
\newcommand{\DegreeFieldEn}{<...>}
```

\pagestyle{empty}

<!-- ============================================================ -->
<!-- 封面（附件 1：上下留邊 3 cm、各行置中；封面不加浮水印）           -->
<!-- ============================================================ -->

\WatermarkOff
\newgeometry{top=3cm, bottom=3cm, left=3cm, right=2cm}

\begin{titlepage}
\begin{center}

{\fontsize{18pt}{21.6pt}\selectfont \UniversityZh\par \Department\par \Degree\par}

\vspace{1.5cm}

{\fontsize{14pt}{16.8pt}\selectfont \DepartmentEn\par}
{\fontsize{16pt}{19.2pt}\selectfont National Yang Ming Chiao Tung University\par \DegreeTypeEn\par}

\vfill

{\fontsize{18pt}{21.6pt}\selectfont \ThesisTitleZh\par \ThesisTitleEn\par}

\vfill

{\fontsize{18pt}{21.6pt}\selectfont 研究生：\StudentName（\StudentNameEn）\par
\vspace{0.5cm}
指導教授：\AdvisorName（\AdvisorNameEn）\par}

\vfill

{\fontsize{18pt}{21.6pt}\selectfont \NYCUDateZh\par \NYCUDateEn\par}

\end{center}
\end{titlepage}

\WatermarkOn

<!-- ============================================================ -->
<!-- 書名頁（附件 2：上下留邊 2 cm；自本頁起每頁加浮水印）             -->
<!-- ============================================================ -->

\newgeometry{top=2cm, bottom=2cm, left=3cm, right=2cm}

\begin{center}

{\fontsize{18pt}{21.6pt}\selectfont \ThesisTitleZh\par \ThesisTitleEn\par}

\vspace{1.5cm}

{\setstretch{1}\fontsize{14pt}{16.8pt}\selectfont
\begin{tabular}{l@{\hspace{3em}}l}
\Spaced[0.5em]{研究生}：\StudentName & Student：\StudentNameEn \\
指導教授：\AdvisorName & Advisor：\AdvisorNameEn \\
\end{tabular}\par}

\vfill

{\fontsize{14pt}{16.8pt}\selectfont \UniversityZh\par \Department\par \Degree\par}

\vfill

{\setstretch{1}\fontsize{14pt}{16.8pt}\selectfont
A \ThesisKindEn\par
Submitted to \DepartmentEn\par
\CollegeEn\par
National Yang Ming Chiao Tung University\par
in Partial Fulfillment of the Requirements\par
for the Degree of\par
\DegreeNameEn\par
in\par
\DegreeFieldEn\par}

\vfill

{\setstretch{1}\fontsize{14pt}{16.8pt}\selectfont
\NYCUDateEn\par
Taiwan, Republic of China\par
\vspace{0.8cm}
\NYCUDateZh\par}

\end{center}

\restoregeometry
\newpage

<!-- ============================================================ -->
<!-- 博碩士論文電子檔著作權授權書：論文上傳後由系統下載，上傳的 PDF 不需放入。 -->
<!-- 博士論文指導教授推薦書（碩士免附，由各所自定）：需要時在此加一頁。       -->
<!-- ============================================================ -->

<!-- ============================================================ -->
<!-- 學位論文審定同意書（附件 3）：紙本論文須裝訂；圖書館上傳手冊說明上傳的 -->
<!-- PDF 不需放入。以簽名後的掃描檔取代本頁，例如：                        -->
<!--   \includegraphics[width=\textwidth]{images/approval.pdf}              -->
<!-- ============================================================ -->

\begin{center}
{\Large\bfseries 學位論文審定同意書}
\end{center}

\vspace{2cm}

\begin{center}
<請以口試委員、指導教授、所長簽名後之審定同意書（附件 3）掃描檔取代本頁>
\end{center}

\newpage

<!-- ============================================================ -->
<!-- 誌謝（自由撰寫，以不超過一頁為原則；規範的羅馬頁碼自中文摘要起算，本頁不編頁碼） -->
<!-- ============================================================ -->

\begin{center}
{\Large\bfseries 誌謝}
\end{center}

<請在此撰寫誌謝詞。建議依序感謝：指導教授、口試委員、實驗室同學、家人。>

\newpage

<!-- ============================================================ -->
<!-- 中文摘要（規範三.4：中文摘要至圖表目錄用小寫羅馬數字 i, ii, iii ...） -->
<!-- ============================================================ -->

\pagenumbering{roman}
\pagestyle{frontmatter}

\begin{center}
{\Large\bfseries 摘要}
\end{center}
\phantomsection\addcontentsline{toc}{section}{中文摘要}

<請在此撰寫中文摘要，以不超過一頁為原則。內容應包含：論述重點、方法或程序、結果等。>

\vspace{1cm}

\noindent\textbf{關鍵詞：<關鍵詞1>、<關鍵詞2>、<關鍵詞3>、<關鍵詞4>、<關鍵詞5>}

<!-- 規範要求關鍵詞 5–7 個 -->

\newpage

<!-- ============================================================ -->
<!-- 英文摘要（以不超過一頁為原則；Keywords 5–7 個） -->
<!-- ============================================================ -->

\begin{center}
{\Large\bfseries Abstract}
\end{center}
\phantomsection\addcontentsline{toc}{section}{英文摘要}

<Write the English abstract here, limited to one page. Should mirror the Chinese abstract in content.>

\vspace{1cm}

\noindent\textbf{Keywords: <Keyword1>, <Keyword2>, <Keyword3>, <Keyword4>, <Keyword5>}

<!-- ============================================================ -->
<!-- 目錄、圖目錄、表目錄（附件 4；規範次序為圖目錄在表目錄之前） -->
<!-- ============================================================ -->

\clearpage
\phantomsection
\addcontentsline{toc}{section}{目錄}
\tableofcontents

\clearpage
\phantomsection
\addcontentsline{toc}{section}{圖目錄}
\listoffigures

\clearpage
\phantomsection
\addcontentsline{toc}{section}{表目錄}
\listoftables

<!-- ============================================================ -->
<!-- 論文正文（規範三.4：第一章至附錄用阿拉伯數字 1, 2, 3 ...） -->
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
<!-- 參考文獻（規範二.13：置於正文之後，獨立另起一頁） -->
<!-- ============================================================ -->

\printbibliography[title=參考文獻, heading=bibintoc]

<!-- ============================================================ -->
<!-- 附錄（規範二.14：大量數據、推導等，各附錄可另起一頁；無附錄可刪除） -->
<!-- ============================================================ -->

# 附錄 {#sec:appendix .unnumbered}

<請在此放置大量數據、推導或其他補充資料。>

<!-- ============================================================ -->
<!-- 學位論文發表形式確認書（附件 5）：必須納入論文並上傳論文系統，不可刪除。 -->
<!-- 以簽名、蓋系所戳章後的掃描檔取代本頁，例如：                            -->
<!--   \includegraphics[width=\textwidth]{images/format-form.pdf}            -->
<!-- ============================================================ -->

\clearpage
\thispagestyle{empty}

\begin{center}
{\Large\bfseries 國立陽明交通大學學位論文發表形式確認書}
\end{center}

\vspace{2cm}

\begin{center}
<請以簽名並蓋系所戳章後之學位論文發表形式確認書（附件 5）掃描檔取代本頁>
\end{center}

<!-- ============================================================ -->
<!-- 以下依情況加入（不適用者免附），均須納入論文並上傳論文系統：             -->
<!-- 附件 6：著作彙編之學位論文資訊及彙編學術著作之共同作者貢獻聲明書        -->
<!--         （採著作彙編形式者）                                             -->
<!-- 附件 7：學位論文使用投稿中學術著作聲明書（使用投稿中學術著作者）       -->
<!-- 每份另起一頁，例如：                                                     -->
<!--   \clearpage\thispagestyle{empty}                                        -->
<!--   \includegraphics[width=\textwidth]{images/co-author-statement.pdf}     -->
<!-- ============================================================ -->
