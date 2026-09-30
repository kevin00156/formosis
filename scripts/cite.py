#!/usr/bin/env python3
"""Formosis cite — 文獻自動化，省掉 Zotero GUI 操作。

三層設計（詳見 docs/03-zotero-setup.md）：
  A. 不需 Zotero：`add` 以 DOI / arXiv ID 取得 BibTeX，去重後寫入 .bib
  B. Zotero + Better BibTeX：`sync` 在編譯前從本機 Better BibTeX 拉最新 .bib
     （取代 GUI 的「Export Collection → Keep updated」設定）
  C. Agent 操作文獻庫：paper.md 有 `zotero-collection:` 且裝了 zotero-cli 時，
     `add` 改把文獻加進 Zotero 的 collection，再 `sync` 拉回 Better BibTeX 的 citekey

不論哪一層，agent 都只要記一個指令：`cite.py add <ID> --md paper.md`。

用法：
  cite.py add <ID> [<ID> ...] [--md paper.md | --bib refs.bib] [--json]
      ID 可為 DOI（10.xxxx/...、doi:...、https://doi.org/...）或 arXiv ID
      （2301.12345、arXiv:2301.12345v2、https://arxiv.org/abs/...）。
      stdout 每行印出一個 citekey（可直接寫成 [@key]）；--json 改印 JSON 陣列。
  cite.py sync <paper.md> [--quiet]
      paper.md frontmatter 有 `zotero-collection:` 才動作，否則安靜略過。
      Zotero 沒開、找不到 collection 等狀況一律只警告並沿用現有 .bib，不擋編譯。

Exit code：0 成功（sync 永遠 0）；1 有任何 ID 失敗；2 用法錯誤。
只用標準函式庫，與 lint.py 一樣可在 build.sh / build.ps1 / CI 直接呼叫。
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lint import resolve_bib, split_frontmatter  # noqa: E402

USER_AGENT = "Formosis-cite (+https://github.com/kevin00156/formosis)"
FETCH_TIMEOUT_S = 20.0
# 編譯前的同步只是順手，Zotero 沒開時不該讓每次編譯多等好幾秒
SYNC_TIMEOUT_S = 3.0
BBT_DEFAULT_PORT = 23119
# zotero-cli 新增條目後，Better BibTeX 產生 citekey 需要一點時間
ZOTERO_KEY_WAIT_S = 6.0
ZOTERO_CLI_TIMEOUT_S = 90.0

# citekey 取題目第一個「有意義」的字時略過的虛詞
TITLE_STOPWORDS = {
    "a", "an", "the", "on", "of", "for", "in", "to", "with", "and", "or", "at", "by",
    "from", "is", "are", "via", "toward", "towards", "using", "into", "about",
}

# CSL-JSON type → BibTeX entry type（doi.org 不給 BibTeX 時的備援）
CSL_TYPES = {
    "article-journal": "article", "article": "article", "paper-conference": "inproceedings",
    "book": "book", "chapter": "incollection", "thesis": "thesis", "report": "report",
    "dissertation-thesis": "thesis",  # 華藝（Airiti）的非標準 type
}

# BibTeX 內建的月份巨集；來源給 month=June 這類裸字時 biber 不認得
MONTHS = ("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec")

# 這些欄位是文字，裸 & % # 會讓 LaTeX 出錯；doi / url 是 verbatim 欄位，不可跳脫
TEXT_FIELDS = {"title", "journal", "booktitle", "publisher", "institution", "school", "series"}

if sys.stderr.isatty():
    C_RED, C_YEL, C_GRN, C_NC = "\033[0;31m", "\033[0;33m", "\033[0;32m", "\033[0m"
else:
    C_RED = C_YEL = C_GRN = C_NC = ""


def info(msg: str) -> None:
    print(f"  {C_GRN}OK{C_NC}   {msg}", file=sys.stderr)


def warning(msg: str) -> None:
    print(f"  {C_YEL}WARN{C_NC} {msg}", file=sys.stderr)


def error(msg: str) -> None:
    print(f"  {C_RED}ERROR{C_NC} {msg}", file=sys.stderr)


class CiteError(Exception):
    """可直接顯示給使用者的錯誤訊息。"""


# ============================================================
# ID 辨識
# ============================================================

_DOI_RE = re.compile(r"(10\.\d{4,9}/[^\s\"<>]+)")
_ARXIV_NEW_RE = re.compile(r"^(\d{4}\.\d{4,5})(v\d+)?$")
_ARXIV_OLD_RE = re.compile(r"^([a-z\-]+(?:\.[A-Z]{2})?/\d{7})(v\d+)?$")
_ARXIV_DOI_RE = re.compile(r"^10\.48550/arxiv\.(.+)$", re.I)


def normalize_id(raw: str) -> tuple[str, str]:
    """把使用者給的 DOI / arXiv ID / 網址轉成 ("doi", DOI) 或 ("arxiv", arXiv ID)。

    無法辨識時丟 CiteError。arXiv 的 DOI（10.48550/arXiv.x）也視為 arXiv，
    因為 arXiv 自家的 BibTeX 比 DataCite 產生的完整（有 eprint / primaryClass）。
    """
    s = raw.strip()
    arxiv = re.sub(r"^(arxiv:|https?://(www\.)?arxiv\.org/(abs|pdf)/)", "", s, flags=re.I)
    arxiv = re.sub(r"\.pdf$", "", arxiv)
    for pat in (_ARXIV_NEW_RE, _ARXIV_OLD_RE):
        m = pat.match(arxiv)
        if m:
            return "arxiv", m.group(1)
    s = re.sub(r"^doi:\s*", "", s, flags=re.I)
    m = _DOI_RE.search(urllib.parse.unquote(s))
    if m:
        doi = m.group(1).rstrip(".,;)")
        am = _ARXIV_DOI_RE.match(doi)
        if am:
            return normalize_id(am.group(1))
        return "doi", doi
    raise CiteError(f"無法辨識「{raw}」：請提供 DOI（例 10.1109/CVPR.2016.90）或 arXiv ID（例 1706.03762）")


def canonical_doi(kind: str, value: str) -> str:
    """去重用的 DOI。arXiv 一律用官方的 DataCite DOI。"""
    return f"10.48550/arXiv.{value}" if kind == "arxiv" else value


# ============================================================
# BibTeX 解析與輸出（只處理本工具需要的子集）
# ============================================================

class BibEntry:
    def __init__(self, etype: str, key: str, fields: list[tuple[str, str]]):
        self.etype = etype
        self.key = key
        self.fields = fields  # [(小寫欄位名, 原始值字串，含外層 {} 或 "")]

    def get(self, name: str) -> str | None:
        for k, v in self.fields:
            if k == name:
                return strip_value(v)
        return None

    def set(self, name: str, value: str) -> None:
        self.fields = [(k, v) for k, v in self.fields if k != name] + [(name, value)]

    def render(self) -> str:
        lines = [f"@{self.etype}{{{self.key},"]
        for k, v in self.fields:
            lines.append(f"  {k} = {v},")
        lines.append("}")
        return "\n".join(lines)


def _read_value(text: str, i: int) -> tuple[str, int]:
    """從 text[i] 開始讀一個欄位值（{...}、"..." 或裸字），回傳 (原始值, 結束位置)。"""
    if text[i] == "{":
        depth, j = 0, i
        while j < len(text):
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
                if depth == 0:
                    return text[i:j + 1], j + 1
            j += 1
        raise CiteError("BibTeX 大括號不成對")
    if text[i] == '"':
        j = i + 1
        while j < len(text) and not (text[j] == '"' and text[j - 1] != "\\"):
            j += 1
        return text[i:j + 1], j + 1
    m = re.match(r"[^,}\s]+", text[i:])
    if not m:
        raise CiteError("BibTeX 欄位值格式錯誤")
    return m.group(0), i + m.end()


_FIELD_RE = re.compile(r"\s*([A-Za-z][\w\-]*)\s*=\s*")
_SEP_RE = re.compile(r"\s*,?")


def parse_entry(text: str) -> BibEntry:
    """解析單一 BibTeX 條目（doi.org / arXiv 回傳的那種）。"""
    m = re.search(r"@(\w+)\s*\{\s*([^,\s]*)\s*,", text)
    if not m:
        raise CiteError("回傳內容不是 BibTeX")
    etype, key, i = m.group(1).lower(), m.group(2), m.end()
    fields: list[tuple[str, str]] = []
    while True:
        fm = _FIELD_RE.match(text, i)
        if not fm:
            break
        value, i = _read_value(text, fm.end())
        fields.append((fm.group(1).lower(), value.strip()))
        i = _SEP_RE.match(text, i).end()
    return BibEntry(etype, key, fields)


def strip_value(v: str) -> str:
    v = v.strip()
    if (v.startswith("{") and v.endswith("}")) or (v.startswith('"') and v.endswith('"')):
        v = v[1:-1]
    return v.replace("{", "").replace("}", "").strip()


def ascii_fold(s: str) -> str:
    """去 LaTeX 指令與重音，只留小寫英數。中文等非拉丁字會被丟掉。"""
    s = re.sub(r"\\[a-zA-Z]+\s*|\\.", "", s)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", s.lower())


def first_author_surname(author: str | None) -> str:
    if not author:
        return ""
    first = re.split(r"\s+and\s+", author.strip(), maxsplit=1)[0]
    if "," in first:
        return ascii_fold(first.split(",")[0])
    parts = first.split()
    return ascii_fold(parts[-1]) if parts else ""


def first_title_word(title: str | None) -> str:
    for w in re.split(r"[\s\-:/]+", title or ""):
        folded = ascii_fold(w)
        if folded and folded not in TITLE_STOPWORDS:
            return folded
    return ""


def make_citekey(entry: BibEntry, taken: set[str]) -> str:
    """<第一作者姓><年><題目第一個實詞>，全小寫 ASCII，例 vaswani2017attention。

    與 docs/03 建議的 Better BibTeX 規則同精神（作者+年+題目），重複時加 a/b/c。
    """
    year = re.sub(r"\D", "", entry.get("year") or "")[:4]
    base = (first_author_surname(entry.get("author")) or "ref") + year + first_title_word(entry.get("title"))
    key, n = base, 0
    while key in taken:
        key = base + chr(ord("a") + n)
        n += 1
    return key


def tidy_fields(entry: BibEntry) -> None:
    """來源回傳的欄位小修：
    - 頁碼 en dash 改 --
    - url 若只是 doi 連結就捨去（DOI 已足夠）
    - 文字欄位的裸 & % # 跳脫，否則 XeLaTeX 報錯
    - month 統一成 jan..dec 巨集（Crossref 會給 month=June 裸字）
    - doi 去掉 https://doi.org/ 前綴（arXiv 舊式條目會給整條網址）
    """
    out = []
    for k, v in entry.fields:
        if k == "month":
            m = strip_value(v).lower()[:3]
            v = m if m in MONTHS else "{" + strip_value(v) + "}"
        if k == "doi":
            v = "{" + re.sub(r"^https?://(dx\.)?doi\.org/", "", strip_value(v), flags=re.I) + "}"
        if k == "pages":
            v = v.replace("\u2013", "--").replace("\u2014", "--")
        if k == "url" and "doi.org/" in v:
            continue
        if k in TEXT_FIELDS:
            v = re.sub(r"(?<!\\)([&%#])", r"\\\1", v)
        out.append((k, v))
    entry.fields = out


def csl_to_entry(csl: dict) -> BibEntry:
    """CSL-JSON（每個 DOI 註冊機構都支援）轉 BibTeX。華藝等不給 BibTeX 的 DOI 走這條。"""
    etype = CSL_TYPES.get(csl.get("type", ""), "misc")
    fields: list[tuple[str, str]] = []

    def put(name: str, value) -> None:
        if value not in (None, "", []):
            fields.append((name, "{" + str(value) + "}"))

    put("title", csl.get("title"))
    names = []
    for a in csl.get("author", []):
        if a.get("family"):
            names.append(f"{a['family']}, {a['given']}" if a.get("given") else a["family"])
        elif a.get("literal"):
            names.append("{" + a["literal"] + "}")
    put("author", " and ".join(names))
    container = csl.get("container-title")
    if isinstance(container, list):
        container = container[0] if container else None
    put({"article": "journal", "inproceedings": "booktitle",
         "incollection": "booktitle"}.get(etype, "howpublished"), container)
    publisher = csl.get("publisher")
    if etype == "thesis":  # 華藝的 publisher 是「國立台灣大學學位論文」，學校應放 institution
        put("institution", re.sub(r"學位論文$", "", publisher or ""))
    else:
        put("publisher", publisher)
    put("volume", csl.get("volume"))
    put("number", csl.get("issue"))
    put("pages", csl.get("page"))
    parts = (csl.get("issued") or {}).get("date-parts") or [[None]]
    put("year", parts[0][0] if parts and parts[0] else None)
    put("doi", csl.get("DOI"))
    put("url", csl.get("URL"))
    return BibEntry(etype, "", fields)


def existing_index(bib_text: str) -> tuple[set[str], dict[str, str]]:
    """回傳 (既有 citekey 集合, {小寫 DOI: citekey})。

    arXiv 條目若只有 eprint 沒有 doi（Better BibTeX 匯出常見），以 arXiv DOI 登記。
    """
    keys: set[str] = set()
    dois: dict[str, str] = {}
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", bib_text):
        if m.group(1).lower() in ("comment", "string", "preamble"):
            continue
        key = m.group(2)
        keys.add(key)
        nxt = bib_text.find("\n@", m.end())
        body = bib_text[m.end(): nxt if nxt != -1 else len(bib_text)]
        dm = re.search(r"\bdoi\s*=\s*[{\"]\s*([^}\"]+?)\s*[}\"]", body, flags=re.I)
        if dm:
            dois.setdefault(re.sub(r"^https?://(dx\.)?doi\.org/", "", dm.group(1)).lower(), key)
        em = re.search(r"\beprint\s*=\s*[{\"]\s*([^}\"]+?)\s*[}\"]", body, flags=re.I)
        if em:
            eprint = re.sub(r"v\d+$", "", em.group(1))
            dois.setdefault(f"10.48550/arxiv.{eprint}".lower(), key)
    return keys, dois


# ============================================================
# 網路
# ============================================================

def http_get(url: str, accept: str) -> str:
    req = urllib.request.Request(url, headers={"Accept": accept, "User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=FETCH_TIMEOUT_S) as resp:
        return resp.read().decode("utf-8", errors="replace")


def fetch_doi(doi: str) -> BibEntry:
    """doi.org content negotiation：先要 BibTeX，註冊機構不支援時退回 CSL-JSON。"""
    url = "https://doi.org/" + urllib.parse.quote(doi, safe="/:;()._-")
    try:
        return parse_entry(http_get(url, "application/x-bibtex; charset=utf-8"))
    except urllib.error.HTTPError as e:
        if e.code != 404 and e.code != 406:
            raise CiteError(f"{doi}：doi.org 回應 HTTP {e.code}") from e
    except CiteError:
        pass  # 回傳的不是 BibTeX，改要 CSL-JSON
    except OSError as e:  # URLError、逾時皆為 OSError 子類
        raise CiteError(f"{doi}：連線失敗（{getattr(e, 'reason', e)}），請確認網路") from e
    try:
        return csl_to_entry(json.loads(http_get(url, "application/vnd.citationstyles.csl+json")))
    except urllib.error.HTTPError as e:
        raise CiteError(f"{doi}：DOI 不存在，或其註冊機構不提供書目資料"
                        "（請改用 Zotero Connector 抓取）") from e
    except (OSError, ValueError, AttributeError) as e:
        raise CiteError(f"{doi}：無法取得書目資料（{e}）") from e


def arxiv_year(arxiv_id: str) -> str:
    """arXiv ID 的 YYMM 是首次提交年月（2301.12345、hep-th/9901001）。"""
    yy = int(re.search(r"(\d{2})\d{2}(\.|\d{3}$)", arxiv_id).group(1))
    return str(1900 + yy if yy >= 91 else 2000 + yy)


def fetch_entry(kind: str, value: str) -> BibEntry:
    if kind == "doi":
        return fetch_doi(value)
    try:
        entry = parse_entry(http_get(f"https://arxiv.org/bibtex/{value}", "text/plain"))
    except (OSError, CiteError):
        entry = fetch_doi(canonical_doi(kind, value))  # arXiv 暫時連不上時改走 DataCite
    # arXiv 的 BibTeX 給最新版本的年份（1706.03762 會變 2023）；引用慣例用首次提交年
    entry.set("year", "{" + arxiv_year(value) + "}")
    return entry


# ============================================================
# Zotero（Better BibTeX pull export、zotero-cli）
# ============================================================

def strip_yaml_comment(v: str) -> str:
    return re.sub(r"\s+#.*$", "", v).strip().strip('"').strip("'")


def zotero_collection(fm: dict) -> str:
    """frontmatter 的 zotero-collection:（去掉 YAML 行尾註解）。"""
    return strip_yaml_comment(fm.get("zotero-collection", ""))


def bbt_export_url(collection: str, library: str = "1", port: int = BBT_DEFAULT_PORT) -> str:
    """Better BibTeX pull export URL。巢狀 collection 用 / 分隔，例：碩論/第二章。"""
    path = "/".join(urllib.parse.quote(part, safe="") for part in collection.split("/"))
    return f"http://127.0.0.1:{port}/better-bibtex/collection?/{library}/{path}.bibtex"


def pull_bbt(fm: dict) -> str:
    """從 Better BibTeX 拉 collection 的 BibTeX。失敗丟 CiteError（訊息可直接顯示）。"""
    collection = zotero_collection(fm)
    library = strip_yaml_comment(fm.get("zotero-library", "1")) or "1"
    # 本機連線不經 proxy
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        with opener.open(bbt_export_url(collection, library), timeout=SYNC_TIMEOUT_S) as resp:
            body = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace") if e.fp else ""
        if "No endpoint" in detail:
            raise CiteError("Zotero 有開但沒有 Better BibTeX（或還在啟動中）") from e
        raise CiteError(f"Better BibTeX 找不到 collection「{collection}」（HTTP {e.code}）") from e
    except OSError as e:  # 連線被拒、逾時
        raise CiteError("連不到 Zotero（沒開？）") from e
    if "@" not in body:
        raise CiteError(f"collection「{collection}」是空的")
    return body


def sync_bib(md: Path, fm: dict, quiet: bool) -> bool:
    """把 Zotero collection 寫進 .bib。回傳是否成功。"""
    bib_path = md.parent / (fm.get("bibliography") or "references.bib")
    try:
        body = pull_bbt(fm)
    except CiteError as e:
        warning(f"{e}，沿用現有 {bib_path.name}")
        return False
    old = bib_path.read_text(encoding="utf-8") if bib_path.exists() else None
    if old == body:
        if not quiet:
            info(f"{bib_path.name} 已與 Zotero 同步")
        return True
    bib_path.write_text(body, encoding="utf-8")
    n = len(existing_index(body)[0])
    info(f"已從 Zotero「{zotero_collection(fm)}」同步 {n} 筆文獻到 {bib_path.name}")
    return True


def zotero_cli_add(cli: str, kind: str, value: str, collection: str) -> None:
    """用 zotero-cli（zotero-mcp-server 套件附帶）把文獻加進 Zotero collection。

    --if-exists file：已在文獻庫的條目不重複建立，只補放進 collection。
    """
    target = ["url", f"https://arxiv.org/abs/{value}"] if kind == "arxiv" else ["doi", value]
    cmd = [cli, "--json", "add", *target, "-c", collection,
           "--if-exists", "file", "--create-collections"]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                              timeout=ZOTERO_CLI_TIMEOUT_S)
    except (OSError, subprocess.TimeoutExpired) as e:
        raise CiteError(f"{value}：zotero-cli 執行失敗（{e}）") from e
    result = None
    for line in reversed(proc.stdout.strip().splitlines()):
        try:
            result = json.loads(line)
            break
        except ValueError:
            continue
    if not isinstance(result, dict) or not result.get("ok"):
        msg = (result or {}).get("error", {}).get("message") if isinstance(result, dict) else None
        raise CiteError(f"{value}：zotero-cli 新增失敗（{msg or proc.stderr.strip() or proc.returncode}）"
                        "；Zotero 10 以上請先執行一次 zotero-mcp authorize-local")


# ============================================================
# 子指令
# ============================================================

def resolve_target_bib(md: Path | None, bib: Path | None) -> tuple[Path, dict]:
    """決定要寫入哪個 .bib；同時回傳 frontmatter（用來判斷是否由 Zotero 管理）。"""
    fm: dict = {}
    if md is not None:
        fm, _ = split_frontmatter(md.read_text(encoding="utf-8", errors="replace").splitlines())
    if bib is not None:
        return bib, fm
    if md is not None:
        found = resolve_bib(md, fm)
        if found is not None:
            return found, fm
        return md.parent / (fm.get("bibliography") or "references.bib"), fm
    return Path("references.bib"), fm


def emit(results: list[dict], as_json: bool) -> None:
    if as_json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for r in results:
            if "key" in r:
                print(r["key"])


def add_to_bib(ids: list[str], bib_path: Path) -> list[dict]:
    """方式 A：直接寫入 .bib。"""
    text = bib_path.read_text(encoding="utf-8") if bib_path.exists() else ""
    keys, dois = existing_index(text)
    results, added = [], []
    for raw in ids:
        try:
            kind, value = normalize_id(raw)
            doi = canonical_doi(kind, value)
            if doi.lower() in dois:
                key = dois[doi.lower()]
                warning(f"{raw} 已在 {bib_path.name}，citekey = {key}")
                results.append({"id": raw, "doi": doi, "key": key, "status": "exists"})
                continue
            entry = fetch_entry(kind, value)
            tidy_fields(entry)
            if not entry.get("doi"):
                entry.fields.append(("doi", "{" + doi + "}"))
            entry.key = make_citekey(entry, keys)
            keys.add(entry.key)
            dois[doi.lower()] = entry.key
            added.append(entry.render())
            info(f"{entry.key} ← {raw}")
            results.append({"id": raw, "doi": doi, "key": entry.key, "status": "added"})
        except CiteError as e:
            error(str(e))
            results.append({"id": raw, "status": "error", "message": str(e)})
    if added:
        prefix = text if (not text or text.endswith("\n")) else text + "\n"
        sep = "\n" if prefix else ""
        bib_path.write_text(prefix + sep + "\n\n".join(added) + "\n", encoding="utf-8")
        info(f"已寫入 {bib_path}（新增 {len(added)} 筆）")
    return results


def add_via_zotero(ids: list[str], md: Path, fm: dict, bib_path: Path, cli: str) -> list[dict]:
    """方式 C：加進 Zotero collection，再從 Better BibTeX 拉回 citekey。"""
    collection = zotero_collection(fm)
    text = bib_path.read_text(encoding="utf-8") if bib_path.exists() else ""
    _, dois = existing_index(text)
    results, pending = [], []
    for raw in ids:
        try:
            kind, value = normalize_id(raw)
            doi = canonical_doi(kind, value)
            if doi.lower() in dois:
                results.append({"id": raw, "doi": doi, "key": dois[doi.lower()], "status": "exists"})
                warning(f"{raw} 已在 {bib_path.name}，citekey = {dois[doi.lower()]}")
                continue
            zotero_cli_add(cli, kind, value, collection)
            info(f"已加入 Zotero「{collection}」← {raw}")
            pending.append((raw, doi))
        except CiteError as e:
            error(str(e))
            results.append({"id": raw, "status": "error", "message": str(e)})
    # Better BibTeX 要一點時間替新條目產生 citekey；等到每篇都出現在匯出結果中
    deadline = time.monotonic() + ZOTERO_KEY_WAIT_S
    while pending:
        synced = sync_bib(md, fm, quiet=True)
        text = bib_path.read_text(encoding="utf-8") if bib_path.exists() else ""
        _, dois = existing_index(text)
        if all(d.lower() in dois for _, d in pending) or not synced or time.monotonic() > deadline:
            break
        time.sleep(1.0)
    for raw, doi in pending:
        key = dois.get(doi.lower())
        if key:
            results.append({"id": raw, "doi": doi, "key": key, "status": "added"})
        else:
            msg = f"{raw} 已加入 Zotero，但在 {bib_path.name} 找不到對應條目（Zotero 有開嗎？稍後執行 cite.py sync 再查）"
            error(msg)
            results.append({"id": raw, "doi": doi, "status": "error", "message": msg})
    return results


def cmd_add(ids: list[str], md: Path | None, bib: Path | None, as_json: bool) -> int:
    bib_path, fm = resolve_target_bib(md, bib)
    if zotero_collection(fm):
        cli = shutil.which("zotero-cli")
        if cli is None:
            error(f"{bib_path.name} 由 Zotero 同步管理（frontmatter 有 zotero-collection:），"
                  "直接寫入會在下次同步時被覆蓋。請用 Zotero Connector 抓取，"
                  "或安裝 zotero-cli（docs/03 方式 C）讓本指令自動加進 Zotero。")
            return 1
        results = add_via_zotero(ids, md, fm, bib_path, cli)
    else:
        results = add_to_bib(ids, bib_path)
    emit(results, as_json)
    return 1 if any(r["status"] == "error" for r in results) else 0


def cmd_sync(md: Path, quiet: bool) -> int:
    fm, _ = split_frontmatter(md.read_text(encoding="utf-8", errors="replace").splitlines())
    if zotero_collection(fm):
        sync_bib(md, fm, quiet)
    return 0


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__, file=sys.stderr)
        return 0 if argv else 2
    cmd, rest = argv[0], argv[1:]

    def opt(name: str) -> Path | None:
        if name in rest:
            i = rest.index(name)
            if i + 1 >= len(rest):
                raise SystemExit(f"{name} 需要一個路徑")
            val = rest.pop(i + 1)
            rest.pop(i)
            return Path(val)
        return None

    if cmd == "add":
        md, bib = opt("--md"), opt("--bib")
        as_json = "--json" in rest
        ids = [a for a in rest if not a.startswith("--")]
        if not ids:
            error("用法：cite.py add <DOI|arXiv ID> [...] [--md paper.md | --bib refs.bib]")
            return 2
        if md is not None and not md.exists():
            error(f"找不到 {md}")
            return 2
        return cmd_add(ids, md, bib, as_json)
    if cmd == "sync":
        args = [a for a in rest if not a.startswith("--")]
        if len(args) != 1 or not Path(args[0]).exists():
            error("用法：cite.py sync <paper.md>")
            return 2
        return cmd_sync(Path(args[0]), "--quiet" in rest)
    error(f"未知子指令：{cmd}（可用：add、sync）")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
