"""Environment check: Atlas, Gemini, torch (CPU) and every requirements.txt import."""
import importlib

import typer
from rich.console import Console
from rich.table import Table

from artifex import config

app = typer.Typer(add_completion=False)
console = Console()

# pip name -> import name, where they differ
IMPORT_NAMES = {
    "scikit-learn": "sklearn",
    "python-dotenv": "dotenv",
    "Pillow": "PIL",
    "pdfminer.six": "pdfminer",
    "fpdf2": "fpdf",
    "python-docx": "docx",
    "sentence-transformers": "sentence_transformers",
    "google-genai": "google.genai",
}


def check_atlas() -> tuple[bool, str]:
    if not config.MONGODB_URI:
        return False, "MONGODB_URI is empty in .env"
    from pymongo import MongoClient

    client = MongoClient(config.MONGODB_URI, serverSelectionTimeoutMS=8000)
    try:
        client.admin.command("ping")
        return True, "ping ok"
    finally:
        client.close()


def check_gemini() -> tuple[bool, str]:
    if not config.GEMINI_API_KEY:
        return False, "GEMINI_API_KEY is empty in .env"
    from google import genai

    client = genai.Client(api_key=config.GEMINI_API_KEY)
    names = [m.name for m in client.models.list()]
    short = {n.removeprefix("models/") for n in names}
    if config.GEMINI_MODEL.removeprefix("models/") in short:
        return True, f"key ok, {config.GEMINI_MODEL} available"
    flash = sorted(n for n in names if "flash" in n)
    console.print(f"[yellow]{config.GEMINI_MODEL} not found. Models containing 'flash':[/]")
    for n in flash:
        console.print(f"  {n}")
    return False, f"key ok, but {config.GEMINI_MODEL} not in model list"


def check_torch() -> tuple[bool, str]:
    import torch

    device = "cuda" if torch.cuda.is_available() else "cpu"
    return True, f"torch {torch.__version__}, device={device}"


def check_requirements() -> tuple[bool, str]:
    req_file = config.REPO_ROOT / "requirements.txt"
    packages = [line.strip() for line in req_file.read_text().splitlines()
                if line.strip() and not line.startswith("#")]
    failed = []
    for pkg in packages:
        try:
            importlib.import_module(IMPORT_NAMES.get(pkg, pkg))
        except Exception as exc:  # noqa: BLE001 - report any import failure
            failed.append(f"{pkg} ({type(exc).__name__})")
    if failed:
        return False, "failed: " + ", ".join(failed)
    return True, f"all {len(packages)} packages import"


CHECKS = [
    ("MongoDB Atlas ping", check_atlas),
    ("Gemini API key + model", check_gemini),
    ("torch (CPU)", check_torch),
    ("requirements.txt imports", check_requirements),
]


@app.command()
def main() -> None:
    """Run all environment checks and print a PASS/FAIL table."""
    table = Table(title=f"Artifex {config.TOOL_VERSION} environment check")
    table.add_column("Check")
    table.add_column("Result")
    table.add_column("Detail")
    all_ok = True
    for name, fn in CHECKS:
        try:
            ok, detail = fn()
        except Exception as exc:  # noqa: BLE001 - any failure is a FAIL row
            ok, detail = False, f"{type(exc).__name__}: {exc}"
        all_ok &= ok
        table.add_row(name, "[green]PASS[/]" if ok else "[red]FAIL[/]", detail)
    console.print(table)
    raise typer.Exit(code=0 if all_ok else 1)


if __name__ == "__main__":
    app()
