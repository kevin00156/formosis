---
profile: thesis-nccu  # Formosis 編譯時自動套用此 profile（可被 CLI --profile 覆寫）

# ============================================================
# === 政大論文基本資訊（請替換以下 placeholder） ===
# 系所名稱依校務系統，勿任意增減文字（規範 二(一)3）
# 英文欄位（系所、學位、姓名、年月）直接寫在下方書名頁區塊
# ============================================================
thesis-title-zh: "<填入：論文中文題目>"      # 非中文撰寫者仍須有中文題名（二(一)5）
thesis-title-en: "<Thesis title in English, to be filled>"
department: "<系所全名，例如：資訊科學系>"
degree: "碩士論文"                  # 或 "博士論文"（二(一)4）
student: "<填入：研究生中文姓名>"
advisor: "<填入：指導教授中文姓名>"
year: "<民國年，例如：115>"         # 論文出版年月，不可早於口試年月
month: "<月份，例如：6>"

# ============================================================
# === 圖片子圖支援 ===
# ============================================================
subfigure: true

# ============================================================
# === 紙張與邊界 ===
# 校級規範未規定紙張與邊界。依政大多數論文實際採用的 Word 中文版 A4 預設：
# 上下 2.54 cm、左右 3.17 cm；頁碼置中於正下方（規範 二(八)2），
# 基線距紙底 1.75 cm（footskip = 2.54 − 1.75）。系所另有規定時從系所。
# 浮水印由圖書館系統加入，不要設 watermark:
# ============================================================
geometry: "top=2.54cm, bottom=2.54cm, left=3.17cm, right=3.17cm, footskip=0.79cm"
papersize: a4

# ============================================================
# === 字體（規範 二(八)2：中文 12 號標楷體，英文 12 號 Times New Roman，行高 1.5） ===
# ============================================================
# 若系統無「標楷體」（常見於 Linux/macOS），改用免費楷體 "AR PL UKai TW"（apt: fonts-arphic-ukai）
# 或國發會「全字庫正楷體」TW-Kai；規範要求標楷體，勿用明體（如 Noto Serif）替代
mainfont: "Times New Roman"
CJKmainfont: "標楷體"
CJKoptions:
  - AutoFakeBold=2.5              # 標楷體沒有粗體字重，標題粗體以假粗體呈現
fontsize: 12pt
linestretch: 1.5

# ============================================================
# === 引用/參考文獻（biblatex + biber） ===
# 規範 二(九)：系所有規範從系所，否則依各學科領域慣用格式（例 APA 改 biblio-style: apa）
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
secnumdepth: 4                    # 第一章、第一節、一、、(一)
toc: false                        # 手動插入 \tableofcontents

# ============================================================
# === 自訂 LaTeX 設定 ===
# 大部分章節格式、頁碼、超連結、圖表編號等已由 profile thesis-nccu 的
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
<!-- 書名頁（規範 二(二)：與封面同；附件一）                         -->
<!-- 電子全文檔的首頁就是書名頁。紙本封面內容相同，以本頁印在封面紙上。 -->
<!-- 各行置中；系所、學位、指導教授、研究生、年月 18 號標楷體；        -->
<!-- 中文題目 20 號標楷體；英文題目 16 號 Times New Roman。無頁碼。     -->
<!-- ============================================================ -->

\newcommand{\DepartmentEn}{<Department of ..., College of ...>}
\newcommand{\DegreeEn}{Master's Thesis}
\newcommand{\AdvisorNameEn}{<Advisor English Name>}
\newcommand{\StudentNameEn}{<Student English Name>}
\newcommand{\MonthYearEn}{<Month Year, e.g. June 2026>}

\pagestyle{empty}

\begin{titlepage}
\setstretch{1.2}
\begin{center}
\fontsize{18pt}{27pt}\selectfont

\UniversityZh\Department\par
\DepartmentEn\par
\Degree\par
\DegreeEn\par

\vfill

{\fontsize{20pt}{30pt}\selectfont\ThesisTitleZh\par}
\vspace{0.5cm}
{\fontsize{16pt}{24pt}\selectfont\ThesisTitleEn\par}

\vfill

指導教授（Advisor）：\AdvisorName\ 博士\par
\AdvisorNameEn\par
\vspace{0.5cm}
研究生（Student）：\StudentName\ 撰\par
\StudentNameEn\par

\vfill

中華民國\ \ROCYear\ 年\ \ROCMonth\ 月\par
\MonthYearEn\par

\end{center}
\end{titlepage}

<!-- ============================================================ -->
<!-- 紙本才有的頁面（規範 一、二(三)(四)）：授權書、論文口試委員簽名頁  -->
<!-- 兩者都「請勿置於電子全文檔內」，簽名頁另外上傳。                  -->
<!-- 印紙本時把掃描檔放進 images/ 並取消下列註解；上傳電子檔前改回註解。 -->
<!-- 授權書須在系統審核通過後列印，不得更改字體字型，列印成一頁。      -->
<!-- ============================================================ -->

<!--
\includepdf{images/<授權書>.pdf}
\includepdf{images/<口試委員簽名頁>.pdf}
-->

<!-- ============================================================ -->
<!-- 誌謝（選填，原則不超過一頁，規範 二(五)；不編頁碼）             -->
<!-- ============================================================ -->

\section*{謝辭}

<請在此撰寫謝辭，內容力求簡單扼要，以不超過一頁為原則。>

<!-- ============================================================ -->
<!-- 中文摘要及關鍵詞（附件二；中英摘要以不超過二頁為原則）           -->
<!-- 頁碼：校級未規定，依系所慣例自摘要起用小寫羅馬數字 i, ii ...      -->
<!-- ============================================================ -->

\newpage
\pagenumbering{roman}
\pagestyle{frontmatter}

\section*{摘要}
\phantomsection
\addcontentsline{toc}{section}{摘要}

<請在此撰寫中文摘要。非中文撰寫的論文仍須有中文摘要。>

\vspace{1cm}

\noindent 關鍵詞：<關鍵詞1>、<關鍵詞2>、<關鍵詞3>

<!-- ============================================================ -->
<!-- Abstract（英文摘要及 Keywords）                                -->
<!-- ============================================================ -->

\section*{Abstract}
\phantomsection
\addcontentsline{toc}{section}{Abstract}

<Write the English abstract here.>

\vspace{1cm}

\noindent Keywords: <Keyword1>, <Keyword2>, <Keyword3>

<!-- ============================================================ -->
<!-- 目次、表次、圖次（附件三；圖次、表次在電子檔非必備）             -->
<!-- ============================================================ -->

\tableofcontents

\clearpage
\phantomsection
\addcontentsline{toc}{section}{表次}
\listoftables

\clearpage
\phantomsection
\addcontentsline{toc}{section}{圖次}
\listoffigures

\newpage

<!-- ============================================================ -->
<!-- 論文正文（附件四）：第一章起阿拉伯數字頁碼                       -->
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

<請說明你的方法整體架構。可插入系統流程圖（圖號與標題在圖下方置中；位置校級未規定，採慣例）：>

<!--
範例：插入單張圖片
![系統架構流程](images/system_overview.png){#fig:system-overview width=80%}

範例：插入單張大圖（精確控制尺寸）
\begin{figure}[!htbp]
\centering
\includegraphics[width=1\textwidth,height=0.8\textheight,keepaspectratio]{images/system_overview.png}
\caption{系統架構流程}
\label{fig:system-overview}
\end{figure}
-->

系統架構見圖 \ref{fig:system-overview}，整體分為三個主要模組。

## <方法一> {#sec:method-approach1}

<請說明第一個方法元件的細節。可插入公式：>

公式 \eqref{eq:example-formula} 定義了核心運算：

\begin{equation}
y = f(x; \theta) + \epsilon
\label{eq:example-formula}
\end{equation}

## <方法二> {#sec:method-approach2}

<請說明第二個方法元件。>

# 實驗結果與討論 {#sec:results}

## 實驗設定 {#sec:results-setup}

<請說明：資料集、評估指標、實驗環境、超參數設定。可用表格呈現（表號與標題在表上方置中，資料來源在表下方靠左；位置校級未規定，採慣例）：>

<!--
範例 LaTeX 表格：
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

\raggedright\footnotesize 資料來源：<來源說明>
\end{table}
-->

實驗超參數設定見表 \ref{tab:hyperparameters}。

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
<!-- 參考文獻（另起一頁，頁次接續正文；系所有規範從系所，規範 二(九)） -->
<!-- ============================================================ -->

\printbibliography[title=參考文獻,heading=bibintoc]

<!-- ============================================================ -->
<!-- 附錄（非必備；參考文獻之後另起一頁，頁次接續）。不需要就保持註解。 -->
<!-- ============================================================ -->

<!--
\section*{附錄一　<附錄名稱>}
\phantomsection
\addcontentsline{toc}{section}{附錄一　<附錄名稱>}

<附錄內容，例如原始資料、訪問記錄或問卷。>
-->
