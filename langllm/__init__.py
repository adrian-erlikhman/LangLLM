"""LangLLM: interpretable stylometric attribution of LLM output across a language-resource gradient."""
import sys

__version__ = "0.1.0"

# Windows consoles default to cp1252; every step prints non-Latin text or Greek letters.
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
