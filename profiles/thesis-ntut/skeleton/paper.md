---
profile: thesis-ntut  # Formosis 編譯時自動套用此 profile（可被 CLI --profile 覆寫）

# ============================================================
# === 北科大論文基本資訊（請替換以下 placeholder） ===
# ============================================================
thesis-title-zh: "<您的論文中文題目>"
thesis-title-en: "<Your Thesis Title in English（選填，不需要就改成空字串）>"
department: "<您的系所全名，依圖書館「學位論文系所名稱參照表」，例如：機電整合研究所>"
degree: "碩士學位論文"              # 或 "博士學位論文"
student: "<您的姓名>"
advisor: "<指導教授姓名> 博士"
# 封面日期以中文數字書寫（零一二三四五六七八九十），為預計畢業年月
year: "<民國年，中文數字，例如：一百一十五>"
month: "<月份，中文數字，例如：六>"

# ============================================================
# === 圖片子圖支援 ===
# ============================================================
subfigure: true

# ============================================================
# === 紙張與邊界（J1 3.8、3.9） ===
# 上 2.5、下 2.75、左右 2.5 cm；頁碼在下方中央、距紙張下緣 1.75 cm
# ============================================================
geometry: "top=2.5cm, bottom=2.75cm, left=2.5cm, right=2.5cm, footskip=1cm"
papersize: a4

# ============================================================
# === 浮水印（學生須自行加入，J1 未規定、圖書館手冊 2.3） ===
# 從 https://cloud.ncl.edu.tw/ntut/download.php 下載校徽 Logo，存到 images/ 後取消註解。
# 預設置中、寬約版面 1/3；封面與審定書頁已在下方以 \WatermarkOff 排除。
# ============================================================
# watermark: images/ntut-watermark.png

# ============================================================
# === 字體設定（J1 3.4、3.5、3.7） ===
# ============================================================
# 若系統無「標楷體」（常見於 Linux/macOS），改用免費楷體 "AR PL UKai TW"（apt: fonts-arphic-ukai）
# 或國發會「全字庫正楷體」TW-Kai；論文要求楷體，勿用明體（如 Noto Serif）替代
mainfont: "Times New Roman"
CJKmainfont: "標楷體"
CJKoptions:
  - AutoFakeBold=2.5              # 標楷體沒有粗體字重；J1 的「粗標楷體」以假粗體呈現
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
secnumdepth: 4                    # 編號最深到 #### 第四層（1.1.1.1）
toc: false                        # 手動插入 \tableofcontents

# ============================================================
# === 自訂 LaTeX 設定 ===
# 大部分章節格式、頁碼、超連結、圖表編號等已由 profile thesis-ntut 的
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
<!-- 封面（紙本用；無頁碼、無浮水印）                              -->
<!-- 電子檔從書名頁開始：上傳圖書館前刪除封面與空白頁兩段。        -->
<!-- 版型依 J1 範例「封頁」：校名／系所／學位 24pt 粗、題目 24pt 粗、 -->
<!-- 英文題目 20pt、研究生／指導教授／日期 18pt 粗。                -->
<!-- ============================================================ -->

\WatermarkOff
\pagestyle{empty}

\begin{titlepage}
\setstretch{1}
\begin{center}

{\fontsize{24pt}{36pt}\selectfont\bfseries \UniversityZh\par \Department\par \Degree\par}

\vspace{4cm}

{\fontsize{24pt}{32pt}\selectfont\bfseries \ThesisTitleZh\par}

{\fontsize{20pt}{32pt}\selectfont \ThesisTitleEn\par}

\vfill

{\fontsize{18pt}{18pt}\selectfont\bfseries 研究生：\StudentName\par}

\vspace{3cm}

{\fontsize{18pt}{18pt}\selectfont\bfseries 指導教授：\AdvisorName\par}

\vspace{2.4cm}

{\fontsize{18pt}{18pt}\selectfont\bfseries 中華民國\ROCYear 年\ROCMonth 月\par}

\vspace{0.8cm}

\end{center}
\end{titlepage}

<!-- 空白頁（封面與書名頁之間，J1 2.2） -->

\null
\newpage

\WatermarkOn

<!-- ============================================================ -->
<!-- 書名頁（內容同封面，無頁碼，要有浮水印，J1 2.2）              -->
<!-- 電子檔的書名頁校名須改用學校 Logo＋校徽（圖書館手冊 5.3）：    -->
<!-- 把第一行的 \UniversityZh 換成 \includegraphics[height=1.6cm]{images/<logo 檔>} -->
<!-- ============================================================ -->

\begin{titlepage}
\setstretch{1}
\begin{center}

{\fontsize{24pt}{36pt}\selectfont\bfseries \UniversityZh\par \Department\par \Degree\par}

\vspace{4cm}

{\fontsize{24pt}{32pt}\selectfont\bfseries \ThesisTitleZh\par}

{\fontsize{20pt}{32pt}\selectfont \ThesisTitleEn\par}

\vfill

{\fontsize{18pt}{18pt}\selectfont\bfseries 研究生：\StudentName\par}

\vspace{3cm}

{\fontsize{18pt}{18pt}\selectfont\bfseries 指導教授：\AdvisorName\par}

\vspace{2.4cm}

{\fontsize{18pt}{18pt}\selectfont\bfseries 中華民國\ROCYear 年\ROCMonth 月\par}

\vspace{0.8cm}

\end{center}
\end{titlepage}

<!-- ============================================================ -->
<!-- 學位論文口試委員會審定書（無頁碼、無浮水印，J1 2.4）          -->
<!-- 請以簽名後的掃描檔取代本頁（例：在 header-includes 加           -->
<!-- \usepackage{pdfpages}，此處改成 \includepdf{images/<審定書>.pdf}） -->
<!-- ============================================================ -->

\WatermarkOff

\begin{center}
{\fontsize{18pt}{27pt}\selectfont\bfseries \UniversityZh\par <研究所>碩士學位論文口試委員會審定書\par}
\end{center}

\vspace{2cm}

\begin{center}
（此頁放置委員、指導教授及所長簽名後之審定書）
\end{center}

\newpage

\WatermarkOn

<!-- ============================================================ -->
<!-- 摘要（小寫羅馬數字頁碼 i, ii, iii ...，J1 3.9）                -->
<!-- 前置頁標題 20pt 粗體、上下各空一行，由 \section* 自動套用      -->
<!-- ============================================================ -->

\pagenumbering{roman}
\pagestyle{frontmatter}

\section*{摘要}
\phantomsection
\addcontentsline{toc}{section}{中文摘要}

<請在此撰寫中文摘要，不超過 500 字或一頁，內容包括問題的描述與所得到的結果；不得有參考文獻或引用圖表（J1 2.5）。自 113-2 學年度起，摘要內不需填寫論文名稱、頁數、校所別、畢業時間、學位、研究生及指導教授姓名。>

\vspace{1cm}

\noindent 關鍵詞：<關鍵詞1>、<關鍵詞2>、<關鍵詞3>

<!-- ============================================================ -->
<!-- ABSTRACT（英文摘要） -->
<!-- ============================================================ -->

\section*{ABSTRACT}
\phantomsection
\addcontentsline{toc}{section}{英文摘要}

<Write the English abstract here. It should mirror the Chinese abstract in content.>

\vspace{1cm}

\noindent Keywords: <Keyword1>, <Keyword2>, <Keyword3>

<!-- ============================================================ -->
<!-- 誌謝 -->
<!-- ============================================================ -->

\section*{誌謝}
\phantomsection
\addcontentsline{toc}{section}{誌謝}

<請在此撰寫誌謝。>

<!-- ============================================================ -->
<!-- 目錄、表目錄、圖目錄（表目錄在圖目錄之前，J1 第 2 章）         -->
<!-- 表或圖只有一、兩個時，對應的目錄可省略（J1 2.8、2.9）            -->
<!-- ============================================================ -->

\clearpage
\phantomsection
\addcontentsline{toc}{section}{目錄}
\tableofcontents

\clearpage
\phantomsection
\addcontentsline{toc}{section}{表目錄}
\listoftables

\clearpage
\phantomsection
\addcontentsline{toc}{section}{圖目錄}
\listoffigures

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

<請說明你的方法整體架構。可插入系統流程圖（圖標題在圖下方置中，J1 3.10.4）：>

<!--
範例：插入單張圖片
![系統架構流程](images/system_overview.png){#fig:system-overview width=80%}

範例：插入單張大圖（精確控制尺寸）
\begin{figure}[!htbp]
\centering
\includegraphics[width=1\textwidth,height=0.9\textheight,keepaspectratio]{images/system_overview.png}
\caption{系統架構流程}
\label{fig:system-overview}
\end{figure}
-->

如圖 \ref{fig:system-overview} 所示，本研究的整體架構分為三個主要模組。

## <方法一> {#sec:method-approach1}

<請說明第一個方法元件的細節。可插入公式（逐章編號，編號靠右，J1 3.11）：>

(\ref{eq:example-formula}) 式定義了核心運算：

\begin{equation}
y = f(x; \theta) + \epsilon ,
\label{eq:example-formula}
\end{equation}

## <方法二> {#sec:method-approach2}

<請說明第二個方法元件。>

# 實驗結果與討論 {#sec:results}

## 實驗設定 {#sec:results-setup}

<請說明：資料集、評估指標、實驗環境、超參數設定。可用表格呈現（表標題在表上方置中，J1 3.10.4）：>

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
\end{table}
-->

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
<!-- 參考文獻（Pandoc + biblatex 自動產生，列入目錄）               -->
<!-- ============================================================ -->

\printbibliography[title=參考文獻,heading=bibintoc]

<!-- ============================================================ -->
<!-- 附錄與符號彙編（不需要就保持註解）                            -->
<!-- 附錄以 A、B、C 編號，標題 12pt 粗體靠左、下方空一行；           -->
<!-- 符號彙編放在附錄之後，標題格式同附錄（J1 2.12）。               -->
<!-- 頁碼接續正文，不另起（圖書館手冊 5.3）。                        -->
<!-- ============================================================ -->

<!--
\clearpage
\phantomsection
\addcontentsline{toc}{section}{附錄 A　<附錄名稱>}
\noindent\textbf{附錄 A　<附錄名稱>}

\vspace{\baselineskip}

<附錄內容>

\clearpage
\phantomsection
\addcontentsline{toc}{section}{符號彙編}
\noindent\textbf{符號彙編}

\vspace{\baselineskip}

\noindent
\begin{tabular}{ll}
Symbol & Meaning \\
$\Theta$ & <符號說明> \\
\end{tabular}
-->
