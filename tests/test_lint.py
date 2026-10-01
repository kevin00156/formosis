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


if __name__ == "__main__":
    unittest.main()
