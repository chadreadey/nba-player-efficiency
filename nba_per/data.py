"""Data download and loading.

Raw files are downloaded by script into data/raw/ and never committed.
Two sources are supported:

- ``legacy``: Kaggle drgilermo/nba-players-stats (Seasons_Stats.csv, 1950-2017),
  the dataset used by the 2023 notebook.
- ``bbref``: Kaggle sumitrodatta/nba-aba-baa-stats (Basketball-Reference-derived,
  1947 to the 2025-26 season). Season ``2026`` means the 2025-26 season.
"""

from __future__ import annotations

import hashlib
import shutil
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

# Pinned Kaggle versions; the archive checksum is verified on every load.
KAGGLE_DATASETS = {
    "legacy": {
        "slug": "drgilermo/nba-players-stats", "version": 2,
        "sha256": "04876c15d43bf65734e60321207d9d5567c091e6cd37a4bbfe719945cca6e7e4",
    },
    "bbref": {
        "slug": "sumitrodatta/nba-aba-baa-stats", "version": 56,  # updated 2026-04-13
        "sha256": "5be35c2837020214a98148f42c21f90bfba0ea1c75d2b3ab8ff6b91baaa4917f",
    },
}
KAGGLE_URL = "https://www.kaggle.com/api/v1/datasets/download/{slug}?datasetVersionNumber={version}"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

# Box-score totals shared by both sources (bbref column names).
TOTALS = [
    "fg", "fga", "x3p", "x3pa", "x2p", "x2pa", "ft", "fta",
    "orb", "drb", "trb", "ast", "stl", "blk", "tov", "pf", "pts",
]
# Advanced composites built from the same box score as PER.
COMPOSITES = ["ows", "dws", "ws", "ws_48", "obpm", "dbpm", "bpm", "vorp"]
RATES = [
    "ts_percent", "x3p_ar", "f_tr", "orb_percent", "drb_percent", "trb_percent",
    "ast_percent", "stl_percent", "blk_percent", "tov_percent", "usg_percent",
]

LEGACY_RENAME = {
    "Year": "season", "Player": "player", "Pos": "pos", "Age": "age", "Tm": "team",
    "G": "g", "GS": "gs", "MP": "mp", "PER": "per", "TS%": "ts_percent",
    "3PAr": "x3p_ar", "FTr": "f_tr", "ORB%": "orb_percent", "DRB%": "drb_percent",
    "TRB%": "trb_percent", "AST%": "ast_percent", "STL%": "stl_percent",
    "BLK%": "blk_percent", "TOV%": "tov_percent", "USG%": "usg_percent",
    "OWS": "ows", "DWS": "dws", "WS": "ws", "WS/48": "ws_48", "OBPM": "obpm",
    "DBPM": "dbpm", "BPM": "bpm", "VORP": "vorp", "FG": "fg", "FGA": "fga",
    "FG%": "fg_percent", "3P": "x3p", "3PA": "x3pa", "3P%": "x3p_percent",
    "2P": "x2p", "2PA": "x2pa", "2P%": "x2p_percent", "eFG%": "e_fg_percent",
    "FT": "ft", "FTA": "fta", "FT%": "ft_percent", "ORB": "orb", "DRB": "drb",
    "TRB": "trb", "AST": "ast", "STL": "stl", "BLK": "blk", "TOV": "tov",
    "PF": "pf", "PTS": "pts",
}


def download(source: str, raw_dir: Path = RAW_DIR) -> Path:
    """Download, verify and unzip a pinned public Kaggle dataset (no credentials needed)."""
    spec = KAGGLE_DATASETS[source]
    out, zpath = raw_dir / source, raw_dir / f"{source}.zip"
    if zpath.exists() and sha256(zpath) == spec["sha256"] and out.exists() and any(out.iterdir()):
        return out
    raw_dir.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(KAGGLE_URL.format(**spec), zpath)
    got = sha256(zpath)
    if got != spec["sha256"]:
        raise RuntimeError(f"{source}: sha256 {got} != pinned {spec['sha256']} (v{spec['version']})")
    shutil.rmtree(out, ignore_errors=True)
    with zipfile.ZipFile(zpath) as z:
        z.extractall(out)
    return out


def load_legacy_raw(raw_dir: Path = RAW_DIR) -> pd.DataFrame:
    """Seasons_Stats.csv exactly as the 2023 notebook read it."""
    return pd.read_csv(download("legacy", raw_dir) / "Seasons_Stats.csv")


def load(source: str, raw_dir: Path = RAW_DIR) -> pd.DataFrame:
    """One row per player-season; traded players keep only their combined row.

    Columns use bbref names plus ``player_key`` (a stable player identifier).
    """
    if source == "legacy":
        df = load_legacy_raw(raw_dir).rename(columns=LEGACY_RENAME)
        df = df.dropna(subset=["season", "player", "age"])
        df["player"] = df["player"].str.replace("*", "", regex=False)
        # No player id in this file; name + birth year separates most namesakes.
        df["player_key"] = df["player"] + "_" + (df["season"] - df["age"]).astype(int).astype(str)
        df["is_combined"] = df["team"] == "TOT"
    elif source == "bbref":
        path = download("bbref", raw_dir)
        adv = pd.read_csv(path / "Advanced.csv")
        tot = pd.read_csv(path / "Player Totals.csv")
        keys = ["season", "lg", "player_id", "team"]
        tot = tot[keys + [c for c in tot.columns if c not in adv.columns]]
        df = adv.merge(tot, on=keys, how="inner", validate="one_to_one")
        df = df[df["lg"] == "NBA"].copy()
        df["player_key"] = df["player_id"]
        df["is_combined"] = df["team"].str.fullmatch(r"\dTM|TOT").fillna(False)
    else:
        raise ValueError(f"unknown source {source!r}")

    # Traded players have a combined row plus one row per team; keep the combined one.
    traded = df.groupby(["player_key", "season"])["is_combined"].transform("any")
    df = df[~traded | df["is_combined"]]
    df = df.drop_duplicates(["player_key", "season"])
    df["season"] = df["season"].astype(int)
    return df.reset_index(drop=True)
