"""Central configuration: .env loading, data paths and global constants."""
import os
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(REPO_ROOT / ".env")

# Data directories (absolute)
DATA_DIR = REPO_ROOT / "data"
CORPUS_DIR = DATA_DIR / "corpus"
CORPUS_TRAIN_DIR = CORPUS_DIR / "train"
CORPUS_TEST_DIR = CORPUS_DIR / "test"
IMAGES_DIR = DATA_DIR / "images"
MODELS_DIR = DATA_DIR / "models"
OUT_DIR = DATA_DIR / "out"

# Constants
BLOCK_SIZE = 4096
RANDOM_SEED = 1337
TOOL_VERSION = "0.1.0"

# Environment
MONGODB_URI = os.getenv("MONGODB_URI", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-latest")
ARTIFEX_LLM = os.getenv("ARTIFEX_LLM", "on").strip().lower() == "on"


if __name__ == "__main__":
    import typer

    app = typer.Typer(add_completion=False)

    @app.command()
    def show() -> None:
        """Print resolved configuration (secrets masked)."""
        for name in ["REPO_ROOT", "DATA_DIR", "CORPUS_TRAIN_DIR", "CORPUS_TEST_DIR",
                     "IMAGES_DIR", "MODELS_DIR", "OUT_DIR", "BLOCK_SIZE",
                     "RANDOM_SEED", "TOOL_VERSION", "GEMINI_MODEL", "ARTIFEX_LLM"]:
            print(f"{name} = {globals()[name]}")
        print(f"MONGODB_URI set = {bool(MONGODB_URI)}")
        print(f"GEMINI_API_KEY set = {bool(GEMINI_API_KEY)}")

    app()
