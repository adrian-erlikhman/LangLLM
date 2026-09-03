"""Unit tests for the pure-Python feature helpers and the validation heuristics.
Stanza-dependent tests are skipped unless the English model is present (see README)."""
import math
import numpy as np
import pytest
from langllm.features import mattr, zipf_slope, burstiness, bigram_entropy, paragraphs, FEATURE_NAMES, FEATURE_GROUPS
from langllm.validate import word_equivalent, looks_like_refusal, structure_violations
from langllm.config import ROOT, load_config, load_schemas


def test_feature_registry_consistent():
    assert len(FEATURE_NAMES) == 21
    assert sorted(sum(FEATURE_GROUPS.values(), [])) == sorted(FEATURE_NAMES)


def test_schemas_balanced():
    s = load_schemas()
    assert len(s) == 12
    assert all(len(x["subclaims"]) == 3 for x in s)
    assert sum(x["stance"] == "for" for x in s) == 6
    tiers = [x["fk_tier"] for x in s]
    assert all(tiers.count(t) == 4 for t in ("general", "educated", "expert"))
    assert set(tiers) <= set(load_config()["fk_tiers"])


def test_config_languages_ranked():
    cfg = load_config()
    ranks = sorted(v["rank"] for v in cfg["languages"].values())
    assert ranks == list(range(1, 8))
    assert len(cfg["models"]) == 5


def test_mattr():
    assert mattr(list("abcde"), 50) == 1.0
    assert mattr(["a"] * 100, 10) == pytest.approx(0.1)
    assert mattr([], 10) != mattr([], 10)  # nan


def test_zipf_slope_is_negative_for_zipfian_sample():
    rng = np.random.default_rng(0)
    toks = [str(i) for i in rng.zipf(1.3, 5000) if i < 2000]
    assert -1.6 < zipf_slope(toks) < -0.5


def test_burstiness_bounds():
    assert burstiness([10, 10, 10, 10]) == pytest.approx(-1.0)
    b = burstiness([2, 40, 3, 50, 1])
    assert -1 <= b <= 1 and b > -0.5
    assert math.isnan(burstiness([5]))


def test_bigram_entropy_monotone():
    assert bigram_entropy("aaaaaaaaaa") < bigram_entropy("abcdefghij")


def test_paragraphs():
    assert paragraphs("a\n\nb\nc\n\n\n") == ["a", "b", "c"]


def test_word_equivalent_cjk():
    assert word_equivalent("one two three", "en") == 3
    assert word_equivalent("这是一个句子" * 10, "zh") == round(60 / 1.6)
    assert word_equivalent("これは文です" * 10, "ja") == round(60 / 2.2)


def test_refusal_detection():
    assert looks_like_refusal("I'm sorry, but I can't help with that.", "en", 200)
    assert looks_like_refusal("Lo siento, pero no puedo escribir eso.", "es", 200)
    assert looks_like_refusal("抱歉，我无法完成这个请求。", "zh", 200)
    assert not looks_like_refusal("Remote work is the better default for three reasons.", "en", 200)
    assert looks_like_refusal("short", "en", 3)


def test_structure_violations():
    assert structure_violations("Plain prose.\n\n# Heading\n- bullet\n1. item\nMore prose.") == 3


@pytest.mark.skipif(not (ROOT / "stanza_resources" / "en").exists(), reason="Stanza English model not downloaded")
def test_extract_english_ranges():
    from langllm.features import extract
    text = ("Remote work should be the default for office jobs. The commute disappears, and an hour a day is recovered. "
            "Companies can hire from anywhere; they are no longer limited to one city. Office costs fall — and that money "
            "can go to salaries.\n\nIs this realistic? I think it is. We have seen it work since 2020.")
    f = extract(text, "en")
    assert set(FEATURE_NAMES) <= set(f)
    assert f["n_sentences"] == 7 and f["para_count"] == 2
    assert 0 < f["mattr"] <= 1 and 0 < f["hapax_rate"] <= 1
    assert f["question_rate"] == pytest.approx(1 / 7)
    assert f["dash_per_1k"] > 0 and f["semicolon_per_1k"] > 0 and f["digit_rate"] > 0
    assert f["first_person_rate"] > 0 and 0.2 < f["func_word_ratio"] < 0.7
    assert -1 <= f["burstiness"] <= 1 and f["dep_depth"] >= 2
