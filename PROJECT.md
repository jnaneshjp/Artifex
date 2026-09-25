# PROJECT.md — Artifex rules

Every later prompt begins with "Read PROJECT.md first".

1. The system REORDERS and ASSESSES bytes read from the disk image. It NEVER
   synthesizes, interpolates, or fills missing bytes. Destroyed regions are
   reported as gaps.
2. LLM output is commentary only, always stored and displayed with provenance
   "INFERRED", and never written into recovered file bytes.
3. manifest.json files are ground truth. They may be read ONLY by training code
   (classifier, adjacency, thresholds, calibration) and by tools/metrics.py.
   Recovery code must never read a manifest.
4. Training uses data/images/train_*.raw only. Evaluation uses test_*.raw only.
5. Every module has a typer CLI under `if __name__ == "__main__":` and runs with
   `python -m artifex.<dotted.path>` from the repo root.
6. The schema in db/schema.py is frozen once written. Do not add, remove, or
   rename fields unless explicitly told to.
7. All randomness uses config.RANDOM_SEED.
