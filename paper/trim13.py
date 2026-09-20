"""Remove the two self-citations of the under-review CompLLM paper."""
from pathlib import Path
p = Path(__file__).with_name("main.tex"); s = p.read_text(encoding="utf-8")
R = [
(r"; RQ6 repeats that task in seven languages, and a companion study examines self-recognition in English~\cite{erlikhman2026compllm}.",
 r"; RQ6 repeats that task in seven languages."),
(r"; it holds in all seven languages here, and a side-by-side lineup with reasoning enabled raises the same judges~\cite{erlikhman2026compllm}.",
 r"; it holds in all seven languages here. Judges shown several texts side by side, or allowed extended reasoning, may do better; neither was tested."),
]
for a, b in R:
    assert a in s, "NOT FOUND: " + a[:70]
    s = s.replace(a, b)
assert "erlikhman2026compllm" not in s
p.write_text(s, encoding="utf-8"); print("self-citations removed")
