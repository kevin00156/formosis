"""scripts/lint.py 的單元測試（不需 pandoc；預期值以 pandoc 3.7 實測的 Cite / Raw 判定為準）。

執行：python3 -m unittest discover -s tests
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import lint  # noqa: E402


def cited(text: str) -> list[str]:
    """回傳 lint 認定的引用 key（以 check_citations 對一份臨時文件實跑）。"""
    with tempfile.TemporaryDirectory() as d:
        md, bib = Path(d) / "paper.md", Path(d) / "references.bib"
        md.write_text(text, encoding="utf-8")
        bib.write_text("", encoding="utf-8")
        lines = text.splitlines()
        return [f.msg.split("[@")[1].split("]")[0]
                for f in lint.check_citations(md, {}, lines, 0) if f.severity == "error"]


class RawLatexCitationTest(unittest.TestCase):
    def test_markdown_citation_is_checked(self):
        self.assertEqual(cited("見 [@he2016] 與 @vaswani2017。"), ["he2016", "vaswani2017"])

    def test_latex_environment_is_raw_block(self):
        # KEV-17：表格註解裡的「PLA @BBL A1」，pandoc 原樣輸出，不是引用
        text = ("\\begin{table}[htbp]\n"
                "\\footnotesize \\textit{註：Polymaker PolyTerra PLA @BBL A1 預設值}\n"
                "\\end{table}\n")
        self.assertEqual(cited(text), [])

    def test_nested_environment_ends_at_matching_end(self):
        text = ("\\begin{figure}\n\\begin{figure}\n@a\n\\end{figure}\n@b\n\\end{figure}\n"
                "之後 @c\n")
        self.assertEqual(cited(text), ["c"])

    def test_inline_command_arguments_are_raw(self):
        for raw in ("\\textit{a @k b}", "a\\footnote{see @k} b", "\\textcolor{red}{@k}",
                    "\\cmd[opt]{@k}", "\\textit{a {nested @k} b}"):
            self.assertEqual(cited(raw), [], raw)

    def test_text_after_command_is_markdown(self):
        self.assertEqual(cited("\\SI{3}{\\milli\\metre} @k"), ["k"])
        self.assertEqual(cited("見 \\cite{x} 與 @k"), ["k"])
        self.assertEqual(cited("\\\\ @k"), ["k"])  # \\ 是換行，不是帶參數的指令

    def test_multiline_command_argument(self):
        self.assertEqual(cited("正文\\footnote{跨行\n仍在註腳 @a}\n之後 @b"), ["b"])


def unused_warns(fm: dict, text: str = "見 [@a]。") -> list[str]:
    """bib 有 a、b、c 三筆，回傳 check_citations 的 warn 訊息。"""
    with tempfile.TemporaryDirectory() as d:
        md, bib = Path(d) / "paper.md", Path(d) / "references.bib"
        md.write_text(text, encoding="utf-8")
        bib.write_text("".join(f"@article{{{k},\n  title={{t}}\n}}\n" for k in "abc"),
                       encoding="utf-8")
        return [f.msg for f in lint.check_citations(md, fm, text.splitlines(), 0)
                if f.severity == "warn"]


class UnusedBibEntryTest(unittest.TestCase):
    def test_hand_written_bib_reports_each_entry(self):
        msgs = unused_warns({})
        self.assertEqual(len(msgs), 2)
        self.assertTrue(all("死引用" in m for m in msgs))

    def test_zotero_collection_collapses_to_one_line(self):
        # FMS-9：collection 整包匯出，未引用條目併成一行摘要
        self.assertEqual(unused_warns({"zotero-collection": "我的論文"}),
                         ["Zotero collection 中 2 筆未引用"])

    def test_zotero_collection_with_trailing_comment(self):
        self.assertEqual(len(unused_warns({"zotero-collection": '"碩論"   # 註解'})), 1)

    def test_empty_zotero_collection_is_hand_written(self):
        self.assertEqual(len(unused_warns({"zotero-collection": "# 只有註解"})), 2)

    def test_zotero_collection_all_cited_no_warn(self):
        self.assertEqual(unused_warns({"zotero-collection": "x"}, "[@a] [@b] [@c]"), [])


if __name__ == "__main__":
    unittest.main()
