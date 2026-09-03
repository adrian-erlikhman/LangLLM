"""Step 1c — repair flagged native prompts: regenerate with the reviewer's note as feedback,
re-review, repeat. Every revision is kept in the prompt record (`revisions`), so the
provenance of the final wording is auditable.

    python -m langllm.refine                 # up to 3 rounds over every flagged prompt
    python -m langllm.refine --rounds 5 --lang zh ja
"""
from __future__ import annotations
import argparse
import json
import datetime as dt
from concurrent.futures import ThreadPoolExecutor
from .config import load_config, load_schemas, NATIVE_PROMPTS_DIR, language_codes
from .openrouter import chat, text_of, usage_of
from .prompts import build_writer_messages, load_native, path_for
from .review import review_one, write_sheet

FEEDBACK = """

A previous version of this prompt failed an independent check. Reviewer note: "{note}"
Missing or wrong: {problems}
Write a fresh prompt that fixes this. Non-negotiable: state the topic and the position to argue unambiguously; name all three supporting points specifically (not "three reasons"), each to be developed in its own paragraph; state the length ({length_hint}); say explicitly that the essay must be continuous prose with no headings, bullet points or numbered lists. Do not mention any language, translation or this feedback."""


def _problems(rec: dict) -> str:
    m, ex, out = rec.get("match", {}), rec.get("extracted", {}), []
    if m.get("topic_match") is False:
        out.append("topic differs")
    if m.get("stance_match") is False:
        out.append("position to argue is wrong or unclear")
    sp = m.get("subclaims_present") or []
    for i, ok in enumerate(sp):
        if not ok:
            out.append(f"sub-claim {i + 1} missing or changed")
    if m.get("extra_claims"):
        out.append("extra points added beyond the three")
    if not ex.get("prose_only"):
        out.append("no explicit prose-only / no-lists instruction")
    if not ex.get("length_stated"):
        out.append("no length target")
    if (ex.get("native_quality") or 5) < 4:
        out.append("reads as translated, not native")
    return "; ".join(out) or "see note"


def regenerate(schema: dict, lang: str, cfg: dict, old: dict, rev: dict) -> dict:
    msgs = build_writer_messages(schema, lang, cfg)
    msgs[1]["content"] += FEEDBACK.format(note=rev.get("match", {}).get("note", ""), problems=_problems(rev),
                                          length_hint=cfg["languages"][lang]["length_hint"])
    n = len(old.get("revisions", [])) + 1
    resp = chat(cfg["prompt_writer"], msgs, temperature=0.6, max_tokens=900, seed=n)
    new = dict(old)
    new["revisions"] = old.get("revisions", []) + [{"prompt": old["prompt"], "flags": rev.get("flags"),
                                                    "note": rev.get("match", {}).get("note")}]
    new.update({"prompt": text_of(resp), "writer_model_served": resp.get("model"), "usage": usage_of(resp),
                "written_at": dt.datetime.now(dt.timezone.utc).isoformat(), "human_checked": False})
    return new


def refine(langs: list[str], rounds: int) -> None:
    cfg, schemas = load_config(), load_schemas()
    by_id = {s["id"]: s for s in schemas}
    for rnd in range(1, rounds + 1):
        todo = []
        for lang in langs:
            p = NATIVE_PROMPTS_DIR / f"review_{lang}.json"
            if not p.exists():
                continue
            for r in json.load(open(p, encoding="utf-8")):
                if r["verdict"] != "pass" and "reviewer_error" not in r.get("flags", []):
                    todo.append((lang, r))
        if not todo:
            print(f"round {rnd}: nothing flagged")
            break
        print(f"round {rnd}: regenerating {len(todo)} prompts")
        for lang in langs:
            items = [r for l, r in todo if l == lang]
            if not items:
                continue
            native = load_native(lang)
            with ThreadPoolExecutor(max_workers=6) as ex:
                new = list(ex.map(lambda r: regenerate(by_id[r["id"]], lang, cfg, native[r["id"]], r), items))
            for rec in new:
                native[rec["id"]] = rec
            with open(path_for(lang), "w", encoding="utf-8") as f:
                json.dump(sorted(native.values(), key=lambda d: d["id"]), f, ensure_ascii=False, indent=2)
            # re-review only the regenerated ones, merge into review file
            reviews = {r["id"]: r for r in json.load(open(NATIVE_PROMPTS_DIR / f"review_{lang}.json", encoding="utf-8"))}
            with ThreadPoolExecutor(max_workers=6) as ex:
                for r in ex.map(lambda rec: review_one(by_id[rec["id"]], rec, lang, cfg), new):
                    reviews[r["id"]] = r
            with open(NATIVE_PROMPTS_DIR / f"review_{lang}.json", "w", encoding="utf-8") as f:
                json.dump([reviews[k] for k in sorted(reviews)], f, ensure_ascii=False, indent=2)
        write_sheet(cfg)
    write_sheet(cfg)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lang", nargs="*")
    ap.add_argument("--rounds", type=int, default=3)
    a = ap.parse_args()
    refine(a.lang or language_codes(load_config()), a.rounds)


if __name__ == "__main__":
    main()
