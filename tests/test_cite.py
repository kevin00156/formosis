"""scripts/cite.py 的單元測試（不連網：doi.org 與 Better BibTeX 皆以 mock 取代）。

執行：python3 -m unittest discover -s tests
"""

from __future__ import annotations

import io
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import cite  # noqa: E402

# doi.org（Crossref）實際回傳的格式：單行、欄位名大小寫混雜、頁碼用 en dash
CROSSREF_RESNET = (
    " @inproceedings{He_2016, title={Deep Residual Learning for Image Recognition}, "
    "url={http://dx.doi.org/10.1109/CVPR.2016.90}, DOI={10.1109/cvpr.2016.90}, "
    "booktitle={2016 IEEE Conference on Computer Vision and Pattern Recognition (CVPR)}, "
    "publisher={IEEE}, author={He, Kaiming and Zhang, Xiangyu and Ren, Shaoqing and Sun, Jian}, "
    "year={2016}, month=jun, pages={770–778} }\n"
)

# DataCite（arXiv DOI）回傳的格式：多行、作者為「名 姓」
DATACITE_ATTENTION = """@misc{https://doi.org/10.48550/arxiv.1706.03762,
  doi = {10.48550/ARXIV.1706.03762},
  url = {https://arxiv.org/abs/1706.03762},
  author = {Vaswani, Ashish and Shazeer, Noam},
  title = {Attention Is All You Need},
  publisher = {arXiv},
  year = {2017},
}
"""


class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class NormalizeIdTest(unittest.TestCase):
    def test_doi_forms(self):
        for raw in ("10.1109/CVPR.2016.90", "doi:10.1109/CVPR.2016.90",
                    "https://doi.org/10.1109/CVPR.2016.90", "https://dx.doi.org/10.1109/CVPR.2016.90."):
            self.assertEqual(cite.normalize_id(raw), "10.1109/CVPR.2016.90", raw)

    def test_arxiv_forms(self):
        for raw in ("1706.03762", "arXiv:1706.03762v5", "https://arxiv.org/abs/1706.03762",
                    "https://arxiv.org/pdf/1706.03762v2.pdf"):
            self.assertEqual(cite.normalize_id(raw), "10.48550/arXiv.1706.03762", raw)
        self.assertEqual(cite.normalize_id("hep-th/9901001"), "10.48550/arXiv.hep-th/9901001")

    def test_unrecognized(self):
        with self.assertRaises(cite.CiteError):
            cite.normalize_id("Attention is all you need")


class ParseAndKeyTest(unittest.TestCase):
    def test_crossref_entry(self):
        e = cite.parse_entry(CROSSREF_RESNET)
        self.assertEqual(e.etype, "inproceedings")
        self.assertEqual(e.get("doi"), "10.1109/cvpr.2016.90")
        self.assertEqual(e.get("month"), "jun")
        cite.tidy_fields(e)
        self.assertEqual(e.get("pages"), "770--778")
        self.assertIsNone(e.get("url"))  # 只是 doi 連結，捨去
        self.assertEqual(cite.make_citekey(e, set()), "he2016deep")

    def test_key_collision_and_stopwords(self):
        e = cite.parse_entry(DATACITE_ATTENTION)
        self.assertEqual(cite.make_citekey(e, set()), "vaswani2017attention")
        self.assertEqual(cite.make_citekey(e, {"vaswani2017attention"}), "vaswani2017attentiona")
        e2 = cite.BibEntry("article", "x", [("author", "{Ashish Vaswani}"), ("year", "{2017}"),
                                            ("title", "{On the {Transformer}}")])
        self.assertEqual(cite.make_citekey(e2, set()), "vaswani2017transformer")

    def test_cjk_author_falls_back(self):
        e = cite.BibEntry("article", "x", [("author", "{王小明}"), ("year", "{2020}"),
                                           ("title", "{深度學習}")])
        self.assertEqual(cite.make_citekey(e, set()), "ref2020")

    def test_existing_index(self):
        keys, dois = cite.existing_index("@comment{x}\n" + CROSSREF_RESNET + DATACITE_ATTENTION)
        self.assertEqual(keys, {"He_2016", "https://doi.org/10.48550/arxiv.1706.03762"})
        self.assertEqual(dois["10.1109/cvpr.2016.90"], "He_2016")


class AddCommandTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)

    def run_add(self, ids, md=None, bib=None):
        responses = {"10.1109/CVPR.2016.90": CROSSREF_RESNET,
                     "10.48550/arXiv.1706.03762": DATACITE_ATTENTION}
        out = io.StringIO()
        with mock.patch.object(cite, "fetch_bibtex", side_effect=lambda d: responses[d]), \
                mock.patch("sys.stdout", out), mock.patch("sys.stderr", io.StringIO()):
            code = cite.cmd_add(ids, md, bib, as_json=False)
        return code, out.getvalue().split()

    def test_add_then_dedupe(self):
        bib = self.dir / "references.bib"
        bib.write_text("@article{old2020x,\n  title = {Old},\n}", encoding="utf-8")  # 無結尾換行
        code, keys = self.run_add(["10.1109/CVPR.2016.90", "1706.03762"], bib=bib)
        self.assertEqual((code, keys), (0, ["he2016deep", "vaswani2017attention"]))
        text = bib.read_text(encoding="utf-8")
        self.assertIn("@article{old2020x,\n  title = {Old},\n}\n\n@inproceedings{he2016deep,", text)
        self.assertIn("  pages = {770--778},", text)
        # 再加一次同一篇（大小寫不同的 DOI）→ 不重複寫入，回報既有 key
        code, keys = self.run_add(["https://doi.org/10.1109/cvpr.2016.90"], bib=bib)
        self.assertEqual((code, keys), (0, ["he2016deep"]))
        self.assertEqual(bib.read_text(encoding="utf-8"), text)

    def test_add_resolves_bib_from_md(self):
        md = self.dir / "paper.md"
        md.write_text("---\nbibliography: refs.bib\n---\n# A {#sec:a}\n", encoding="utf-8")
        code, _ = self.run_add(["1706.03762"], md=md)
        self.assertEqual(code, 0)
        self.assertIn("vaswani2017attention", (self.dir / "refs.bib").read_text(encoding="utf-8"))

    def test_refuses_zotero_managed_bib(self):
        md = self.dir / "paper.md"
        md.write_text("---\nzotero-collection: 我的碩論  # 由 Zotero 管理\n---\n", encoding="utf-8")
        code, keys = self.run_add(["1706.03762"], md=md)
        self.assertEqual((code, keys), (1, []))
        self.assertFalse((self.dir / "references.bib").exists())

    def test_partial_failure(self):
        bib = self.dir / "references.bib"
        with mock.patch("sys.stderr", io.StringIO()):
            code, keys = self.run_add(["not-an-id", "1706.03762"], bib=bib)
        self.assertEqual((code, keys), (1, ["vaswani2017attention"]))


class SyncCommandTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)
        self.md = self.dir / "paper.md"
        self.bib = self.dir / "references.bib"
        self.bib.write_text("@misc{keep,\n}\n", encoding="utf-8")

    def run_sync(self, frontmatter, response="", exc=None):
        self.md.write_text(f"---\n{frontmatter}\n---\n", encoding="utf-8")
        opener = mock.Mock()
        if exc is not None:
            opener.open.side_effect = exc
        else:
            opener.open.return_value = FakeResponse(response.encode("utf-8"))
        with mock.patch("urllib.request.build_opener", return_value=opener), \
                mock.patch("sys.stderr", io.StringIO()):
            code = cite.cmd_sync(self.md, quiet=True)
        return code, opener

    def test_no_collection_is_noop(self):
        code, opener = self.run_sync("profile: thesis-ncu")
        self.assertEqual(code, 0)
        opener.open.assert_not_called()

    def test_pulls_collection(self):
        code, opener = self.run_sync('zotero-collection: "碩論/第二章"', DATACITE_ATTENTION)
        self.assertEqual(code, 0)
        url = opener.open.call_args[0][0]
        self.assertEqual(url, "http://127.0.0.1:23119/better-bibtex/export/collection?/1/"
                              "%E7%A2%A9%E8%AB%96/%E7%AC%AC%E4%BA%8C%E7%AB%A0.bibtex")
        self.assertEqual(self.bib.read_text(encoding="utf-8"), DATACITE_ATTENTION)

    def test_zotero_down_keeps_bib(self):
        code, _ = self.run_sync("zotero-collection: 碩論", exc=urllib.error.URLError("refused"))
        self.assertEqual(code, 0)
        self.assertEqual(self.bib.read_text(encoding="utf-8"), "@misc{keep,\n}\n")

    def test_empty_collection_keeps_bib(self):
        code, _ = self.run_sync("zotero-collection: 碩論", "")
        self.assertEqual(code, 0)
        self.assertEqual(self.bib.read_text(encoding="utf-8"), "@misc{keep,\n}\n")


if __name__ == "__main__":
    unittest.main()
