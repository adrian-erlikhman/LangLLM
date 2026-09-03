"""Step 1 — write one native prompt per (schema, language) with a non-subject LLM.

No translation: the prompt writer (Llama, see config.yaml `prompt_writer`) is given the
schema fields and asked to write a prompt *as a native speaker would*, in the target
language, that fixes the same topic, stance and three sub-claims. English is produced by
the same route so all seven languages share one protocol.

Output: prompts/native/{lang}.json — a list of {id, lang, prompt, writer_model, ...}.
A human reader checks es / ru / zh (see prompts/native/REVIEW.md, created here).

    python -m langllm.prompts            # write all missing
    python -m langllm.prompts --lang es  # one language
    python -m langllm.prompts --force    # regenerate
"""
from __future__ import annotations
import argparse
import json
import datetime as dt
from .config import load_config, load_schemas, NATIVE_PROMPTS_DIR
from .openrouter import chat, text_of, usage_of

WRITER_SYSTEM = (
    "You write essay prompts for a research study. You write them the way a fluent, educated "
    "native speaker of the target language would write an assignment for another native speaker: "
    "natural phrasing, no translationese, no mention of any other language, no meta-commentary. "
    "Output ONLY the prompt text itself, nothing else."
)

WRITER_TEMPLATE = """Write an essay prompt in {name_en} ({native}).

The prompt must ask the reader to write a persuasive essay that:
- Topic: {topic}
- Position to argue: {stance_word} the proposition
- Must make exactly these three supporting points, in any order, each developed in its own paragraph:
  1. {c1}
  2. {c2}
  3. {c3}
- Written for {audience}
- Length: {length_hint}
- Prose only: continuous paragraphs. No headings, no bullet points, no numbered lists, no title, no tables.

Express all of this naturally in {name_en}, as a native speaker would phrase such an assignment. Do not translate this instruction literally; write the assignment fresh. Do not add any extra requirements. Output only the prompt."""

STANCE_WORD = {"for": "in favour of", "against": "against"}


def build_writer_messages(schema: dict, lang: str, cfg: dict) -> list[dict]:
    L = cfg["languages"][lang]
    user = WRITER_TEMPLATE.format(
        name_en=L["name_en"], native=L["native"], topic=schema["topic"],
        stance_word=STANCE_WORD[schema["stance"]],
        c1=schema["subclaims"][0], c2=schema["subclaims"][1], c3=schema["subclaims"][2],
        audience=cfg["fk_tiers"][schema["fk_tier"]], length_hint=L["length_hint"],
    )
    return [{"role": "system", "content": WRITER_SYSTEM}, {"role": "user", "content": user}]


def path_for(lang: str):
    return NATIVE_PROMPTS_DIR / f"{lang}.json"


def load_native(lang: str) -> dict[str, dict]:
    p = path_for(lang)
    if not p.exists():
        return {}
    with open(p, encoding="utf-8") as f:
        return {d["id"]: d for d in json.load(f)}


def write_prompts(langs: list[str], force: bool = False) -> None:
    cfg = load_config()
    schemas = load_schemas()
    writer = cfg["prompt_writer"]
    for lang in langs:
        have = {} if force else load_native(lang)
        out = []
        for s in schemas:
            if s["id"] in have:
                out.append(have[s["id"]])
                continue
            msgs = build_writer_messages(s, lang, cfg)
            resp = chat(writer, msgs, temperature=0.4, max_tokens=900, seed=0)
            out.append({
                "id": s["id"], "lang": lang, "prompt": text_of(resp),
                "schema": {k: s[k] for k in ("topic", "stance", "subclaims", "fk_tier")},
                "writer_model": writer, "writer_model_served": resp.get("model"),
                "usage": usage_of(resp), "written_at": dt.datetime.utcnow().isoformat() + "Z",
                "human_checked": False,
            })
            print(f"[{lang}] {s['id']} ok ({len(out[-1]['prompt'])} chars)")
        out.sort(key=lambda d: d["id"])
        NATIVE_PROMPTS_DIR.mkdir(parents=True, exist_ok=True)
        with open(path_for(lang), "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
    _write_review_sheet(cfg)


def _write_review_sheet(cfg: dict) -> None:
    """A checklist for the human reader (es / ru / zh) — flip `human_checked` in the JSON when done."""
    p = NATIVE_PROMPTS_DIR / "REVIEW.md"
    if p.exists():
        return
    p.write_text(
        "# Native prompt review\n\n"
        "Reader checks Spanish, Russian and Chinese prompts against the schema in `prompts/schemas.json`.\n"
        "For each prompt confirm: (1) same topic, (2) same stance, (3) all three sub-claims present and none added,\n"
        "(4) prose-only + length instruction present, (5) reads as native, not translated.\n"
        "Fix the text in `{lang}.json` directly if needed and set `human_checked: true`.\n\n"
        "| lang | reader | date | notes |\n|---|---|---|---|\n| es |  |  |  |\n| ru |  |  |  |\n| zh |  |  |  |\n",
        encoding="utf-8",
    )


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lang", nargs="*", help="language codes (default: all in config)")
    ap.add_argument("--force", action="store_true", help="regenerate even if a prompt exists")
    a = ap.parse_args()
    cfg = load_config()
    langs = a.lang or sorted(cfg["languages"], key=lambda k: cfg["languages"][k]["rank"])
    write_prompts(langs, force=a.force)


if __name__ == "__main__":
    main()
