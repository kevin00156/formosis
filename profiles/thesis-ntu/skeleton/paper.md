---
profile: thesis-ntu  # Formosis 編譯時自動套用此 profile（可被 CLI --profile 覆寫）

# ============================================================
# === 臺大論文基本資訊（請替換以下 placeholder） ===
# 英文欄位（系所、學院、姓名、指導教授、年月）直接寫在下方封面區塊
# 學院、系所用完整名稱，中英對照見 https://www.ntu.edu.tw/academics/academics_list.html
# ============================================================
thesis-title-zh: "<填入：論文中文題目>"
thesis-title-en: "<Thesis title in English, to be filled>"
college: "<學院全名，例如：工學院>"
department: "<系所全名，例如：機械工程學系>"
degree: "碩士論文"                  # 或 "博士論文"
student: "<填入：撰者中文姓名>"
advisor: "<填入：指導教授姓名> 博士"      # 須加稱謂（學位名稱或職銜）
year: "<民國年，例如：115>"         # 不得早於口試月份，且與英文年月一致
month: "<月份，例如：6>"

# ============================================================
# === 浮水印（臺大規定學生自行加入，全文含封面） ===
# 從臺大圖書館下載標準圖檔 https://www.lib.ntu.edu.tw/doc/CL/watermark.pdf
# 存成 images/ntu-watermark.pdf 後取消下一行註解。
# 位置依上傳手冊：距頂 2.5 cm、距右 2.5 cm、比例 50%、不透明度 50%。
# ============================================================
# watermark: images/ntu-watermark.pdf

# ============================================================
# === 圖片子圖支援 ===
# ============================================================
subfigure: true

# ============================================================
# === 紙張與邊距（規範第十點：上 3、下 2、左右各 3 公分） ===
# ============================================================
geometry: "top=3cm, bottom=2cm, left=3cm, right=3cm"
papersize: a4
classoption: [fleqn]

# ============================================================
# === 字體（規範第十點：中文 12 號楷書／細明體，英文 12 號 Times New Roman） ===
# ============================================================
# 若系統無「標楷體」（常見於 Linux/macOS），改用免費楷體 "AR PL UKai TW"（apt: fonts-arphic-ukai）
# 或國發會「全字庫正楷體」TW-Kai
mainfont: "Times New Roman"
CJKmainfont: "標楷體"
fontsize: 12pt
linestretch: 1.5                  # 中文撰寫 1.5 倍；英文撰寫的論文改 2（雙行間距）

# ============================================================
# === 引用/參考文獻（biblatex + biber） ===
# 臺大校級規範未指定引用格式，系所另有規定（如 APA）時改 biblio-style
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
# DOI：從臺大博碩士論文提交系統複製（須含 doi: 前綴），取消下方兩行註解並填入，
# 每頁距底 1 cm、距右 1 cm 自動印出。其他 override 或實驗數據變數也可加在這裡。
# ============================================================
# header-includes:
#   - \newcommand{\ThesisDOI}{doi:10.6342/NTU20XXXXXXXX}
---

```{=latex}
% ============================================================
% 封面／書名頁（規範附件 1、2：上留白 4 公分、下留白 3 公分，各行置中、1.5 倍行高）
% 電子檔只放這一頁封面，不含側邊；紙本外封面（含側邊，不加浮水印與 DOI）另行印製。
% ============================================================
\newgeometry{top=4cm, bottom=3cm, left=3cm, right=3cm}
\begin{titlepage}
\centering
\setstretch{1}

{\fontsize{18pt}{27pt}\selectfont \UniversityZh\College\Department\par
\Degree\par}

{\fontsize{14pt}{21pt}\selectfont
Department of <English Department Name>\par
College of <English College Name>\par}

{\fontsize{16pt}{24pt}\selectfont
National Taiwan University\par
Master's Thesis\par}              % 博士論文改 Doctoral Dissertation

\vfill

{\fontsize{18pt}{27pt}\selectfont
\ThesisTitleZh\par
\ThesisTitleEn\par}

\vfill

{\fontsize{18pt}{27pt}\selectfont
\StudentName\par
<Given-name Family-name>\par}     % 先名後姓不加逗號；先姓後名則姓後加逗號

\vfill

{\fontsize{18pt}{27pt}\selectfont
指導教授：\AdvisorName\par
Advisor: <Advisor Name>, Ph.D.\par}

\vfill

{\fontsize{18pt}{27pt}\selectfont
中華民國 \ROCYear{} 年 \ROCMonth{} 月\par
<June> <2026>\par}                % 英文月、西元年
\end{titlepage}
\restoregeometry
```

<!-- ============================================================ -->
<!-- 前置頁（羅馬數字頁碼 i, ii, iii ...） -->
<!-- 規範第一點順序：審定書、謝辭、中文摘要、英文摘要、目次、圖次、表次 -->
<!-- 所有前置頁都要列進目次（115.2.3 函：目次、圖次、表次本身也要列） -->
<!-- ============================================================ -->

\pagenumbering{roman}
\pagestyle{frontmatter}

<!--
口試委員會審定書（規範附件 3）：電子檔可不附；要附就放已簽名的掃描 PDF，
不可放空白審定書。不附時整段保持註解，目次也就不會出現這個標題。

\phantomsection
\addcontentsline{toc}{section}{口試委員會審定書}
\includepdf[pages=1, pagecommand={\thispagestyle{frontmatter}}]{images/certificate.pdf}
-->

\phantomsection
\addcontentsline{toc}{section}{誌謝}

\begin{center}
{\Large\bfseries 誌謝}
\end{center}

<請在此撰寫誌謝詞，以不超過一頁為原則。建議依序感謝：指導教授、口試委員、實驗室同學、家人。>

\newpage

\phantomsection
\addcontentsline{toc}{section}{中文摘要}

\begin{center}
{\Large\bfseries 摘要}
\end{center}

<請在此撰寫中文摘要，不超過三頁。內容應包含論述重點、方法或程序、結果與討論及結論。以英文撰寫論文者仍須附中文摘要。>

\vspace{1cm}

\noindent 關鍵詞：<關鍵詞 1>、<關鍵詞 2>、<關鍵詞 3>、<關鍵詞 4>、<關鍵詞 5>

\newpage

\phantomsection
\addcontentsline{toc}{section}{英文摘要}

\begin{center}
{\Large\bfseries Abstract}
\end{center}

<Write the English abstract here, no more than three pages. It should mirror the Chinese abstract in content.>

\vspace{1cm}

\noindent Keywords: <Keyword 1>, <Keyword 2>, <Keyword 3>, <Keyword 4>, <Keyword 5>

\newpage

\phantomsection
\addcontentsline{toc}{section}{目次}
\tableofcontents

\newpage

\phantomsection
\addcontentsline{toc}{section}{圖次}
\listoffigures

\newpage

\phantomsection
\addcontentsline{toc}{section}{表次}
\listoftables

\newpage

<!-- ============================================================ -->
<!-- 正文開始（「第一章」自第 1 頁起，阿拉伯數字頁碼） -->
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

<請說明你的方法整體架構。可插入系統流程圖（圖若擷取自參考文獻，須在圖說標註來源）：>

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

<請說明：資料集、評估指標、實驗環境、超參數設定。可用表格呈現：>

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
