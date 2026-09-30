"""scripts/cite.py 的單元測試（不連網：doi.org 與 Better BibTeX 皆以 mock 取代）。

執行：python3 -m unittest discover -s tests
"""

from __future__ import annotations

import io
import json
import subprocess
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
            self.assertEqual(cite.normalize_id(raw), ("doi", "10.1109/CVPR.2016.90"), raw)

    def test_arxiv_forms(self):
        for raw in ("1706.03762", "arXiv:1706.03762v5", "https://arxiv.org/abs/1706.03762",
                    "https://arxiv.org/pdf/1706.03762v2.pdf", "10.48550/arXiv.1706.03762"):
            self.assertEqual(cite.normalize_id(raw), ("arxiv", "1706.03762"), raw)
        self.assertEqual(cite.normalize_id("hep-th/9901001"), ("arxiv", "hep-th/9901001"))
        self.assertEqual(cite.canonical_doi("arxiv", "1706.03762"), "10.48550/arXiv.1706.03762")

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
        responses = {("doi", "10.1109/CVPR.2016.90"): CROSSREF_RESNET,
                     ("arxiv", "1706.03762"): DATACITE_ATTENTION}
        out = io.StringIO()
        fetch = lambda k, v: cite.parse_entry(responses[(k, v)])  # noqa: E731
        with mock.patch.object(cite, "fetch_entry", side_effect=fetch), \
                mock.patch("shutil.which", return_value=None), \
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
        self.assertEqual(url, "http://127.0.0.1:23119/better-bibtex/collection?/1/"
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


class FetchFallbackTest(unittest.TestCase):
    CSL = {"type": "article-journal", "title": "臺灣 & 深度學習", "DOI": "10.6342/X",
           "author": [{"family": "王", "given": "小明"}, {"literal": "某研究團隊"}],
           "container-title": ["臺灣期刊"], "issued": {"date-parts": [[2021, 5]]},
           "volume": "3", "issue": "2", "page": "1-10"}

    def test_csl_json_fallback(self):
        calls = []

        def fake_get(url, accept):
            calls.append(accept)
            if "x-bibtex" in accept:
                raise urllib.error.HTTPError(url, 406, "Not Acceptable", {}, None)
            return json.dumps(self.CSL)

        with mock.patch.object(cite, "http_get", side_effect=fake_get):
            e = cite.fetch_doi("10.6342/X")
        self.assertEqual(len(calls), 2)
        cite.tidy_fields(e)
        self.assertEqual(e.etype, "article")
        self.assertIn(("title", r"{臺灣 \& 深度學習}"), e.fields)
        self.assertEqual(e.get("author"), "王, 小明 and 某研究團隊")
        self.assertEqual(e.get("journal"), "臺灣期刊")
        self.assertEqual((e.get("year"), e.get("number"), e.get("doi")), ("2021", "2", "10.6342/X"))

    def test_arxiv_prefers_arxiv_bibtex(self):
        arxiv_bib = ("@misc{vaswani2017attention,\n  title={Attention Is All You Need},\n"
                     "  author={Ashish Vaswani},\n  year={2017},\n  eprint={1706.03762},\n}")
        with mock.patch.object(cite, "http_get", return_value=arxiv_bib) as get:
            e = cite.fetch_entry("arxiv", "1706.03762")
        self.assertEqual(get.call_args[0][0], "https://arxiv.org/bibtex/1706.03762")
        self.assertEqual(e.get("eprint"), "1706.03762")

    def test_arxiv_falls_back_to_datacite(self):
        def fake_get(url, accept):
            if "arxiv.org" in url:
                raise urllib.error.URLError("down")
            return DATACITE_ATTENTION
        with mock.patch.object(cite, "http_get", side_effect=fake_get):
            e = cite.fetch_entry("arxiv", "1706.03762")
        self.assertEqual(e.get("title"), "Attention Is All You Need")

    def test_eprint_counts_as_arxiv_doi(self):
        _, dois = cite.existing_index("@article{v17,\n  eprint = {1706.03762v5},\n}\n")
        self.assertEqual(dois, {"10.48550/arxiv.1706.03762": "v17"})


class ZoteroCliTest(unittest.TestCase):
    """方式 C：frontmatter 有 zotero-collection 且裝了 zotero-cli 時，add 改加進 Zotero。"""

    BBT_EXPORT = "@inproceedings{heDeepResidualLearning2016,\n  doi = {10.1109/CVPR.2016.90},\n}\n"

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)
        self.md = self.dir / "paper.md"
        self.md.write_text('---\nzotero-collection: "碩論"\n---\n', encoding="utf-8")

    def run_add(self, cli_stdout, bbt_body):
        proc = subprocess.CompletedProcess([], 0, stdout=cli_stdout, stderr="")
        opener = mock.Mock()
        opener.open.side_effect = lambda *a, **k: FakeResponse(bbt_body.encode("utf-8"))
        out = io.StringIO()
        with mock.patch("shutil.which", return_value="/usr/bin/zotero-cli"), \
                mock.patch("subprocess.run", return_value=proc) as run, \
                mock.patch("urllib.request.build_opener", return_value=opener), \
                mock.patch.object(cite, "ZOTERO_KEY_WAIT_S", 0), \
                mock.patch("sys.stdout", out), mock.patch("sys.stderr", io.StringIO()):
            code = cite.cmd_add(["https://doi.org/10.1109/CVPR.2016.90"], self.md, None, as_json=False)
        return code, out.getvalue().split(), run

    def test_adds_to_zotero_and_returns_bbt_key(self):
        ok = '{"ok": true, "command": "add doi", "schema": 1, "data": {"text": "added"}}'
        code, keys, run = self.run_add(ok, self.BBT_EXPORT)
        self.assertEqual((code, keys), (0, ["heDeepResidualLearning2016"]))
        cmd = run.call_args[0][0]
        self.assertEqual(cmd[:5], ["/usr/bin/zotero-cli", "--json", "add", "doi", "10.1109/CVPR.2016.90"])
        self.assertIn("碩論", cmd)
        self.assertEqual((self.dir / "references.bib").read_text(encoding="utf-8"), self.BBT_EXPORT)

    def test_cli_failure_reported(self):
        bad = '{"ok": false, "command": "add doi", "schema": 1, "error": {"message": "write denied"}}'
        code, keys, _ = self.run_add(bad, self.BBT_EXPORT)
        self.assertEqual((code, keys), (1, []))


if __name__ == "__main__":
    unittest.main()
