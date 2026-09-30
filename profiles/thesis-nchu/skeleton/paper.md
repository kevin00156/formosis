---
profile: thesis-nchu  # Formosis 編譯時自動套用此 profile（可被 CLI --profile 覆寫）

# ============================================================
# === 中興大學論文基本資訊（請替換以下 placeholder） ===
# ============================================================
thesis-title-zh: "<您的論文中文題目（最多三行、60 字）>"
thesis-title-en: "<Your Thesis Title in English>"
department: "<系所全名，依本校組織規程，例如：機械工程學系>"
degree: "碩士學位論文"              # 或 "博士學位論文"
# 姓名後加上與護照相同的英文名（F2-65 貳一(一)4、5）
student: "<您的中文姓名> <English Name>"
advisor: "<指導教授中文姓名> <English Name>"
# 論文完成日期採中式數字（F2-65 貳一(一)6）
year: "<民國年，中式數字，例如：一百一十五>"
month: "<月份，中式數字，例如：六>"

# ============================================================
# === 圖片子圖支援 ===
# ============================================================
subfigure: true

# ============================================================
# === 紙張與邊界（F2-65 貳四(一)：上下左右各 3 cm） ===
# 頁碼頁尾置中；距紙緣 1.75 cm 依圖書館 Word 範本（條文未規定）
# 浮水印由圖書館系統加入，不要設 watermark:
# ============================================================
geometry: "top=3cm, bottom=3cm, left=3cm, right=3cm, footskip=1.25cm"
papersize: a4

# ============================================================
# === 字體設定（F2-65 貳四(一)2：中英文字型由各院所自行規定） ===
# 預設採封面規定的標楷體／Times New Roman；院所另有規定時請修改。
# ============================================================
# 若系統無「標楷體」（常見於 Linux/macOS），改用免費楷體 "AR PL UKai TW"（apt: fonts-arphic-ukai）
# 或國發會「全字庫正楷體」TW-Kai；論文要求楷體，勿用明體（如 Noto Serif）替代
mainfont: "Times New Roman"
CJKmainfont: "標楷體"
CJKoptions:
  - AutoFakeBold=2.5              # 標楷體沒有粗體字重，標題粗體以假粗體呈現
fontsize: 12pt
# 條文「每頁最少 32 行、每行最少 32 字」：1.4 倍行距每頁 33 行、每行 35 字
linestretch: 1.4

# ============================================================
# === 引用/參考文獻（biblatex + biber） ===
# 條文：參考書目格式依各學門習用者為準（F2-65 貳三(一)2）
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
# 大部分章節格式、頁碼、超連結、圖表編號等已由 profile thesis-nchu 的
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
<!-- 封面（F2-65 附錄一）：標楷體 20 點置中，上下左右各留 3 cm；   -->
<!-- 系所名在上緣 3 cm 處、論文題目在上緣 9 cm 處（版心頂端下 6 cm）； -->
<!-- 題目一行放不下時以倒三角形排列，最多三行；                   -->
<!-- 英文題目 Times New Roman 20 點。無頁碼。                      -->
<!-- ============================================================ -->

\pagestyle{empty}

\begin{titlepage}
\setstretch{1}
\begin{center}
\fontsize{20pt}{30pt}\selectfont

\UniversityZh\Department\par
\Degree\par

\vspace{3.9cm}

\ThesisTitleZh\par
\ThesisTitleEn\par

\vfill

指導教授：\AdvisorName\par
研\hspace{0.5em}究\hspace{0.5em}生：\StudentName\par

\vspace{1.5cm}

中華民國\ROCYear 年\ROCMonth 月\par

\end{center}
\end{titlepage}

<!-- 空白頁（題贈用，F2-65 壹(二)） -->

\null
\newpage

<!-- ============================================================ -->
<!-- 書名頁（中文）：內容、形式與封面相同，裝訂後加蓋系所戳章       -->
<!-- ============================================================ -->

\begin{titlepage}
\setstretch{1}
\begin{center}
\fontsize{20pt}{30pt}\selectfont

\UniversityZh\Department\par
\Degree\par

\vspace{3.9cm}

\ThesisTitleZh\par
\ThesisTitleEn\par

\vfill

指導教授：\AdvisorName\par
研\hspace{0.5em}究\hspace{0.5em}生：\StudentName\par

\vspace{1.5cm}

中華民國\ROCYear 年\ROCMonth 月\par

\end{center}
\end{titlepage}

<!-- 書名頁（英文）：非必備，由系所決定（F2-65 貳一(四)）。需要時取消註解並填入英文系所名稱。 -->
<!--
\begin{titlepage}
\setstretch{1}
\begin{center}
\fontsize{20pt}{30pt}\selectfont
Department of <Department Name>\par
National Chung Hsing University\par
Master Thesis\par
\vspace{3.9cm}
\ThesisTitleEn\par
\vfill
Advisor: <English Name>\par
Student: <English Name>\par
\vspace{1.5cm}
<Month> <Year>\par
\end{center}
\end{titlepage}
-->

<!-- ============================================================ -->
<!-- 審核頁（口試委員、指導教授簽名，樣式由系所提供，無頁碼）       -->
<!-- 請以簽名後的掃描檔取代（例：header-includes 加 \usepackage{pdfpages}， -->
<!-- 此處改成 \includepdf{images/<審核頁>.pdf}）                    -->
<!-- ============================================================ -->

\begin{center}
{\fontsize{16pt}{24pt}\selectfont\bfseries \UniversityZh\Department\par \Degree\par}

\vspace{2cm}

（此頁放置口試委員及指導教授簽名後之審核頁）
\end{center}

\newpage

<!-- ============================================================ -->
<!-- 授權頁（國立中興大學學位論文授權書，無頁碼）                   -->
<!-- ============================================================ -->

\begin{center}
{\fontsize{16pt}{24pt}\selectfont\bfseries 國立中興大學學位論文授權書\par}

\vspace{2cm}

（此頁放置簽名後之學位論文授權書）
\end{center}

\newpage

<!-- ============================================================ -->
<!-- 誌謝辭（非必備；一頁為原則，最多兩頁；不編頁碼）               -->
<!-- ============================================================ -->

\section*{誌謝}

<請在此撰寫誌謝辭，表達對師長、受訪者、同學、家人等的感謝之意。>

<!-- ============================================================ -->
<!-- 中文摘要（小寫羅馬數字頁碼 i, ii, iii ...，F2-65 貳四(二)2）   -->
<!-- ============================================================ -->

\newpage
\pagenumbering{roman}
\pagestyle{frontmatter}

\section*{摘要}
\phantomsection
\addcontentsline{toc}{section}{中文摘要}

<請在此撰寫中文摘要，一頁為原則，最多不超過兩頁；簡要說明研究動機、研究方法與設計、資料收集與分析、研究結果及討論建議等。>

\vspace{1cm}

\noindent 關鍵字：<關鍵字1>、<關鍵字2>、<關鍵字3>

<!-- ============================================================ -->
<!-- Abstract（英文摘要） -->
<!-- ============================================================ -->

\section*{Abstract}
\phantomsection
\addcontentsline{toc}{section}{英文摘要}

<Write the English abstract here. Keep it to one page where possible and check the translation of technical terms.>

\vspace{1cm}

\noindent Keywords: <Keyword1>, <Keyword2>, <Keyword3>

<!-- ============================================================ -->
<!-- 目次、表目次、圖目次（表在前、圖在後，F2-65 貳一(十一)）        -->
<!-- 圖或表總數超過 10 個時分列兩頁；未超過可只留一頁「圖表目次」。   -->
<!-- ============================================================ -->

\tableofcontents

\clearpage
\phantomsection
\addcontentsline{toc}{section}{表目次}
\listoftables

\clearpage
\phantomsection
\addcontentsline{toc}{section}{圖目次}
\listoffigures

\newpage

<!-- ============================================================ -->
<!-- 正文開始（第一章至附錄阿拉伯數字連續編碼，F2-65 貳四(二)3）     -->
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

<請說明你的方法整體架構。可插入系統流程圖（圖號與標題在圖下方置中，F2-65 貳二(二)3）：>

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

<請說明：資料集、評估指標、實驗環境、超參數設定。可用表格呈現（表號與標題在表上方置中，資料來源在表下方靠左，F2-65 貳二(二)2、4）：>

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
<!-- 參考書目（另起一頁，頁次接續正文；先中文後西文，F2-65 貳三(一)） -->
<!-- ============================================================ -->

\printbibliography[title=參考書目,heading=bibintoc]

<!-- ============================================================ -->
<!-- 附錄（參考書目之後另起一頁，頁次接續，F2-65 貳三(二)）。不需要就保持註解。 -->
<!-- ============================================================ -->

<!--
\section*{附錄一　<附錄名稱>}
\phantomsection
\addcontentsline{toc}{section}{附錄一　<附錄名稱>}

<附錄內容，例如原始資料、訪問記錄或問卷。>
-->
