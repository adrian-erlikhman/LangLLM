"""Load config.yaml and prompts/schemas.json; resolve paths relative to the repo root."""
from __future__ import annotations
import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "config.yaml"
SCHEMAS_PATH = ROOT / "prompts" / "schemas.json"
NATIVE_PROMPTS_DIR = ROOT / "prompts" / "native"
RAW_DIR = ROOT / "data" / "raw"
FEATURES_DIR = ROOT / "data" / "features"
RESULTS_DIR = ROOT / "results"
FIG_DIR = RESULTS_DIR / "figures"


def load_config() -> dict:
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_schemas() -> list[dict]:
    with open(SCHEMAS_PATH, encoding="utf-8") as f:
        return json.load(f)["schemas"]


def language_codes(cfg: dict | None = None) -> list[str]:
    """Language codes ordered by resource rank (English first)."""
    cfg = cfg or load_config()
    return sorted(cfg["languages"], key=lambda k: cfg["languages"][k]["rank"])


def resource_rank(cfg: dict | None = None) -> dict[str, int]:
    cfg = cfg or load_config()
    return {k: v["rank"] for k, v in cfg["languages"].items()}
