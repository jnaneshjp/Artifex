# Artifex

Digital evidence recovery: reorders and assesses fragments read from a disk image.
See `PROJECT.md` for the rules every module follows.

## Setup

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env      # then fill in MONGODB_URI and GEMINI_API_KEY
python -m artifex.tools.check_env
```
