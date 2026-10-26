"""Run train.py on Modal (CPU). The current models run locally in about a minute;
this exists so heavier sweeps can move to Modal unchanged.

    modal run modal_app.py --source bbref

Results come back to the local results/ directory. This creates billable Modal usage.
"""

from pathlib import Path

import modal

ROOT = Path(__file__).resolve().parent

image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install("numpy>=1.26", "pandas>=2.1", "scikit-learn>=1.4")
    .add_local_python_source("nba_per")
    .add_local_file(ROOT / "train.py", "/root/train.py")
)
app = modal.App("nba-per", image=image)


@app.function(cpu=4, memory=4096, timeout=1800)
def train_remote(source: str, test_from: int | None) -> dict:
    import sys

    sys.path.insert(0, "/root")
    import train

    return train.main(source, test_from, out_dir=Path("/tmp/results"))


@app.local_entrypoint()
def main(source: str = "bbref", test_from: int = 0):
    import train

    res = train_remote.remote(source, test_from or None)
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / f"{source}.modal.md").write_text(train.to_markdown(res))
    print(train.to_markdown(res))
