"""Pre-flight for main.tex: every \\Macro{} used is defined in numbers.tex, every \\cite key is in
references.bib, and no dash/arrow glyphs sit in the source. Run before uploading to Overleaf."""
import re
from pathlib import Path

HERE = Path(__file__).parent
tex = (HERE / "main.tex").read_text(encoding="utf-8")
nums = (HERE / "numbers.tex").read_text(encoding="utf-8")
bib = (HERE / "references.bib").read_text(encoding="utf-8")

defined = set(re.findall(r"newcommand\{\\(\w+)\}", nums))
used = set(re.findall(r"\\([A-Z][A-Za-z0-9]+)\{\}", tex))
missing = sorted(u for u in used if u not in defined and not u.startswith("IEEE"))
keys = set(re.findall(r"@\w+\{(\w+),", bib))
cited = {k.strip() for grp in re.findall(r"\\cite\{([^}]+)\}", tex) for k in grp.split(",")}
body = tex.split("\\maketitle")[1].split("\\bibliographystyle")[0]
words = len(re.sub(r"\\[a-zA-Z]+(\[[^\]]*\])?(\{[^}]*\})?", " ", body).split())
print("macros used:", len(used), "| missing:", missing)
print("cites:", len(cited), "| missing from bib:", sorted(cited - keys), "| uncited bib keys:", sorted(keys - cited))
print("body words (approx):", words)
bad = sorted({ch for ch in tex if ch in "\u2014\u2013\u2192"})
print("dash/arrow glyphs in source:", bad)
