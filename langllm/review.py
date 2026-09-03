"""Step 1b — automated fidelity review of every native prompt, all seven languages.

A second non-subject model (config `prompt_reviewer`, a different family from both the
subjects and the Llama writer) reads each native prompt *without seeing the schema*, and
reports back in English: the topic, the stance, every supporting point the prompt demands,
whether it forbids headings/lists, and whether it reads as native. The report is then
matched against the schema by a third call that sees both. Anything short of a clean match
is flagged in prompts/native/review_{lang}.json and summarised in prompts/native/REVIEW.md.

Human sign-off (`human_checked: true` in {lang}.json) stays optional on top of this.

    python -m langllm.review              # all languages
    python -m langllm.review --lang zh ja
"""
from __future__ import annotations
import argparse
import json
import re
import datetime as dt
from concurrent.futures import ThreadPoolExecutor
from .config import load_config, load_schemas, NATIVE_PROMPTS_DIR, language_codes
from .openrouter import chat, text_of, OpenRouterError
from .prompts import load_native

EXTRACT = """Below is an essay assignment written in {name_en}. Read it and answer in English, as JSON only, with keys:
"topic": one sentence, what the essay is about;
"stance": "for" or "against" the proposition the essay must defend, or "unclear";
"points": list of every specific supporting point the assignment tells the writer to make (verbatim meaning, translated to English);
"prose_only": true if it forbids headings, bullet points or numbered lists, else false;
"length_stated": true if a length target is given, else false;
"native_quality": 1-5, where 5 = reads like a fluent native speaker wrote it, 1 = obvious translation or broken;
"other_language_mentioned": true if the text mentions any language or translation.

Assignment:
<<<
{prompt}
>>>"""

MATCH = """Compare an intended essay schema with what a reviewer extracted from the written prompt. Answer in JSON only:
"topic_match": true/false, "stance_match": true/false,
"subclaims_present": list of three booleans (was each intended sub-claim requested, same meaning),
"extra_claims": list of extracted points that are NOT among the intended sub-claims (empty if none),
"verdict": "pass" if topic and stance match, all three sub-claims present, no extra claims; else "fail",
"note": one short sentence.

Intended schema:
topic: {topic}
stance: {stance}
sub-claims: 1) {c1} 2) {c2} 3) {c3}

Extracted from the prompt:
{extracted}"""


def _json(text: str) -> dict:
    """First JSON object in the reply (models add prose or code fences around it)."""
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.M)
    start = text.find("{")
    if start < 0:
        return {"_parse_error": text[:300]}
    try:
        obj, _ = json.JSONDecoder().raw_decode(text[start:])
        return obj if isinstance(obj, dict) else {"_parse_error": text[:300]}
    except json.JSONDecodeError:
        return {"_parse_error": text[:300]}


NO_REASONING = {"enabled": False}  # Qwen 3.7 is a reasoning model; without this it spends the whole budget thinking


def _ask(reviewer: str, content: str, max_tokens: int) -> dict:
    return _json(text_of(chat(reviewer, [{"role": "user", "content": content}], temperature=0.0,
                              max_tokens=max_tokens, seed=0, reasoning=NO_REASONING)))


def review_one(s: dict, p: dict | None, lang: str, cfg: dict) -> dict:
    reviewer, L = cfg["prompt_reviewer"], cfg["languages"][lang]
    if not p:
        return {"id": s["id"], "lang": lang, "verdict": "missing"}
    try:
        ex = _ask(reviewer, EXTRACT.format(name_en=L["name_en"], prompt=p["prompt"]), 900)
        mt = _ask(reviewer, MATCH.format(topic=s["topic"], stance=s["stance"], c1=s["subclaims"][0], c2=s["subclaims"][1],
                                         c3=s["subclaims"][2], extracted=json.dumps(ex, ensure_ascii=False)), 600)
    except OpenRouterError as e:  # network/API failure: record it, keep going, re-run later
        return {"id": s["id"], "lang": lang, "verdict": "flag", "flags": ["reviewer_error"], "error": str(e)[:300]}
    if True:
        flags = []
        if mt.get("verdict") != "pass":
            flags.append("content")
        if not ex.get("prose_only"):
            flags.append("no_prose_only_instruction")
        if not ex.get("length_stated"):
            flags.append("no_length")
        if (ex.get("native_quality") or 0) < 4:
            flags.append("non_native")
        if ex.get("other_language_mentioned"):
            flags.append("mentions_language")
        if "_parse_error" in ex or "_parse_error" in mt:
            flags.append("reviewer_parse_error")
        rec = {"id": s["id"], "lang": lang, "verdict": "pass" if not flags else "flag", "flags": flags,
               "extracted": ex, "match": mt, "reviewer_model": reviewer,
               "reviewed_at": dt.datetime.now(dt.timezone.utc).isoformat()}
        print(f"[{lang}] {s['id']}: {rec['verdict']} {flags or ''}", flush=True)
        return rec


def review_language(lang: str, cfg: dict, schemas: list[dict]) -> list[dict]:
    native = load_native(lang)
    with ThreadPoolExecutor(max_workers=6) as ex:
        out = list(ex.map(lambda s: review_one(s, native.get(s["id"]), lang, cfg), schemas))
    with open(NATIVE_PROMPTS_DIR / f"review_{lang}.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    return out


def write_sheet(cfg: dict) -> None:
    rows = []
    for lang in language_codes(cfg):
        p = NATIVE_PROMPTS_DIR / f"review_{lang}.json"
        if not p.exists():
            rows.append(f"| {lang} | not run | | | |")
            continue
        rev = json.load(open(p, encoding="utf-8"))
        flagged = [f"{r['id']}({','.join(r.get('flags', []))})" for r in rev if r["verdict"] != "pass"]
        human = all(d.get("human_checked") for d in load_native(lang).values()) if load_native(lang) else False
        rows.append(f"| {lang} | {sum(r['verdict']=='pass' for r in rev)}/{len(rev)} | {' '.join(flagged) or '—'} | {'yes' if human else 'no'} | |")
    (NATIVE_PROMPTS_DIR / "REVIEW.md").write_text(
        "# Native prompt review\n\n"
        f"Automated reviewer: `{cfg['prompt_reviewer']}` (not a subject, not the writer). It extracts topic / stance / "
        "sub-claims from each prompt blind, then matches them to the schema. Flags: `content` (topic, stance or sub-claim "
        "mismatch, or an extra claim), `no_prose_only_instruction`, `no_length`, `non_native` (quality < 4/5), "
        "`mentions_language`.\n\nFix flagged prompts by editing `{lang}.json` and re-running `python -m langllm.review --lang {lang}`. "
        "A fluent human reader may additionally set `human_checked: true` per prompt; that column is optional.\n\n"
        "| lang | auto pass | flagged | human checked | notes |\n|---|---|---|---|---|\n" + "\n".join(rows) + "\n",
        encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lang", nargs="*")
    a = ap.parse_args()
    cfg, schemas = load_config(), load_schemas()
    for lang in a.lang or language_codes(cfg):
        review_language(lang, cfg, schemas)
    write_sheet(cfg)
    print("wrote", NATIVE_PROMPTS_DIR / "REVIEW.md")


if __name__ == "__main__":
    main()
