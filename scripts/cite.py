#!/usr/bin/env python3
"""PaperForge cite — 文獻自動化，省掉 Zotero GUI 操作。

三層設計（詳見 docs/03-zotero-setup.md）：
  A. 不需 Zotero：`add` 以 DOI / arXiv ID 取得 BibTeX，去重後寫入 .bib
  B. Zotero + Better BibTeX：`sync` 在編譯前從本機 Better BibTeX 拉最新 .bib
     （取代 GUI 的「Export Collection → Keep updated」設定）
  C. Agent 操作文獻庫：由 Zotero MCP server 負責（見 docs/03），完成後以 `sync` 拉回 .bib

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
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lint import resolve_bib, split_frontmatter  # noqa: E402

USER_AGENT = "PaperForge-cite (+https://github.com/kevin00156/paperforge)"
FETCH_TIMEOUT_S = 20.0
# 編譯前的同步只是順手，Zotero 沒開時不該讓每次編譯多等好幾秒
SYNC_TIMEOUT_S = 3.0
BBT_DEFAULT_PORT = 23119

# citekey 取題目第一個「有意義」的字時略過的虛詞
TITLE_STOPWORDS = {
    "a", "an", "the", "on", "of", "for", "in", "to", "with", "and", "or", "at", "by",
    "from", "is", "are", "via", "toward", "towards", "using", "into", "about",
}

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


def normalize_id(raw: str) -> str:
    """把使用者給的 DOI / arXiv ID / 網址轉成 DOI。無法辨識時丟 CiteError。

    arXiv 論文一律轉成 arXiv 官方的 DataCite DOI（10.48550/arXiv.<id>），
    這樣兩種 ID 都走同一條 doi.org content negotiation 路徑。
    """
    s = raw.strip()
    arxiv = re.sub(r"^(arxiv:|https?://(www\.)?arxiv\.org/(abs|pdf)/)", "", s, flags=re.I)
    arxiv = re.sub(r"\.pdf$", "", arxiv)
    for pat in (_ARXIV_NEW_RE, _ARXIV_OLD_RE):
        m = pat.match(arxiv)
        if m:
            return f"10.48550/arXiv.{m.group(1)}"
    s = re.sub(r"^doi:\s*", "", s, flags=re.I)
    m = _DOI_RE.search(urllib.parse.unquote(s))
    if m:
        return m.group(1).rstrip(".,;)")
    raise CiteError(f"無法辨識「{raw}」：請提供 DOI（例 10.1109/CVPR.2016.90）或 arXiv ID（例 1706.03762）")


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


def parse_entry(text: str) -> BibEntry:
    """解析單一 BibTeX 條目（doi.org 回傳的那種）。"""
    m = re.search(r"@(\w+)\s*\{\s*([^,\s]*)\s*,", text)
    if not m:
        raise CiteError("回傳內容不是 BibTeX")
    etype, key, i = m.group(1).lower(), m.group(2), m.end()
    fields: list[tuple[str, str]] = []
    while True:
        fm = re.compile(r"\s*([A-Za-z][\w\-]*)\s*=\s*").match(text, i)
        if not fm:
            break
        value, i = _read_value(text, fm.end())
        fields.append((fm.group(1).lower(), value.strip()))
        sep = re.compile(r"\s*,?").match(text, i)
        i = sep.end()
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
    surname = first.split(",")[0] if "," in first else first.split()[-1] if first.split() else ""
    return ascii_fold(surname)


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
    """doi.org 回傳的欄位小修：頁碼 en dash 改 --；url 若只是 doi 連結就捨去（DOI 已足夠）。"""
    out = []
    for k, v in entry.fields:
        if k == "pages":
            v = v.replace("\u2013", "--").replace("\u2014", "--")
        if k == "url" and "doi.org/" in v:
            continue
        out.append((k, v))
    entry.fields = out


def existing_index(bib_text: str) -> tuple[set[str], dict[str, str]]:
    """回傳 (既有 citekey 集合, {小寫 DOI: citekey})。"""
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
            dois[dm.group(1).lower()] = key
    return keys, dois


# ============================================================
# 網路
# ============================================================

def fetch_bibtex(doi: str) -> str:
    url = "https://doi.org/" + urllib.parse.quote(doi, safe="/:;()._-")
    req = urllib.request.Request(url, headers={
        "Accept": "application/x-bibtex; charset=utf-8",
        "User-Agent": USER_AGENT,
    })
    try:
        with urllib.request.urlopen(req, timeout=FETCH_TIMEOUT_S) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise CiteError(f"{doi}：DOI 不存在，或其註冊機構不支援自動取得 BibTeX"
                            "（請改用 Zotero Connector 抓取）") from e
        raise CiteError(f"{doi}：doi.org 回應 HTTP {e.code}") from e
    except OSError as e:  # URLError、逾時皆為 OSError 子類
        raise CiteError(f"{doi}：連線失敗（{getattr(e, 'reason', e)}），請確認網路") from e


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


def cmd_add(ids: list[str], md: Path | None, bib: Path | None, as_json: bool) -> int:
    bib_path, fm = resolve_target_bib(md, bib)
    if zotero_collection(fm):
        error(f"{bib_path.name} 由 Zotero 同步管理（frontmatter 有 zotero-collection:），"
              "直接寫入會在下次同步時被覆蓋。請改用 Zotero Connector 或 Zotero MCP 新增，"
              "再執行 cite.py sync。")
        return 1
    text = bib_path.read_text(encoding="utf-8") if bib_path.exists() else ""
    keys, dois = existing_index(text)
    results, failed, added = [], False, []
    for raw in ids:
        try:
            doi = normalize_id(raw)
            if doi.lower() in dois:
                key = dois[doi.lower()]
                warning(f"{raw} 已在 {bib_path.name}，citekey = {key}")
                results.append({"id": raw, "doi": doi, "key": key, "status": "exists"})
                continue
            entry = parse_entry(fetch_bibtex(doi))
            tidy_fields(entry)
            if not entry.get("doi"):
                entry.fields.append(("doi", "{" + doi + "}"))
            entry.key = make_citekey(entry, keys)
            keys.add(entry.key)
            dois[doi.lower()] = entry.key
            added.append(entry.render())
            info(f"{entry.key} ← {doi}")
            results.append({"id": raw, "doi": doi, "key": entry.key, "status": "added"})
        except CiteError as e:
            error(str(e))
            failed = True
            results.append({"id": raw, "status": "error", "message": str(e)})
    if added:
        prefix = text if (not text or text.endswith("\n")) else text + "\n"
        sep = "\n" if prefix else ""
        bib_path.write_text(prefix + sep + "\n\n".join(added) + "\n", encoding="utf-8")
        info(f"已寫入 {bib_path}（新增 {len(added)} 筆）")
    if as_json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for r in results:
            if "key" in r:
                print(r["key"])
    return 1 if failed else 0


def zotero_collection(fm: dict) -> str:
    """frontmatter 的 zotero-collection:（去掉 YAML 行尾註解）。"""
    v = fm.get("zotero-collection", "")
    return re.sub(r"\s+#.*$", "", v).strip().strip('"').strip("'")


def bbt_export_url(collection: str, library: str = "1", port: int = BBT_DEFAULT_PORT) -> str:
    """Better BibTeX pull export URL。巢狀 collection 用 / 分隔，例：碩論/第二章。"""
    path = "/".join(urllib.parse.quote(part, safe="") for part in collection.split("/"))
    return f"http://127.0.0.1:{port}/better-bibtex/export/collection?/{library}/{path}.bibtex"


def cmd_sync(md: Path, quiet: bool) -> int:
    lines = md.read_text(encoding="utf-8", errors="replace").splitlines()
    fm, _ = split_frontmatter(lines)
    collection = zotero_collection(fm)
    if not collection:
        return 0
    library = re.sub(r"\s+#.*$", "", fm.get("zotero-library", "1")).strip() or "1"
    bib_path = md.parent / (fm.get("bibliography") or "references.bib")
    url = bbt_export_url(collection, library)
    # 本機連線不經 proxy
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        with opener.open(url, timeout=SYNC_TIMEOUT_S) as resp:
            body = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        warning(f"Better BibTeX 找不到 collection「{collection}」（HTTP {e.code}），沿用現有 {bib_path.name}")
        return 0
    except OSError:  # 連線被拒、逾時
        warning(f"連不到 Zotero（沒開？或未裝 Better BibTeX），沿用現有 {bib_path.name}")
        return 0
    if "@" not in body:
        warning(f"collection「{collection}」是空的，沿用現有 {bib_path.name}")
        return 0
    old = bib_path.read_text(encoding="utf-8") if bib_path.exists() else None
    if old == body:
        if not quiet:
            info(f"{bib_path.name} 已與 Zotero 同步")
        return 0
    bib_path.write_text(body, encoding="utf-8")
    n = len(existing_index(body)[0])
    info(f"已從 Zotero「{collection}」同步 {n} 筆文獻到 {bib_path.name}")
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
