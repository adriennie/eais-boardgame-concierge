"""Your scorer: how many of a run's requests did your system answer right?

Run it on a run folder, from this folder:

    python score.py runs/single-1

You see how many of the run's requests are right, then the id of each request that's wrong:

    6 of 10 right
    P003
    P007
    ...

Write score() below, and keep main() as it is. When we grade your scorer, we call your score() on test runs of
our own.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from p1.io import read_jsonl


def score(run_dir: str, answers: str = "data/public_answers.jsonl") -> tuple[int, int, list[str]]:
    """Score the run in run_dir against the answers file. Return (right, total, wrong_ids): the number of right
    answers, the number of requests in the run, and the ids of the wrong ones, in the run's order."""
    
    # 1. Build lookup map from ground truth file: {request_id: list_of_correct_letters}
    correct_map = {}
    for entry in read_jsonl(answers):
        correct_map[entry["id"]] = entry.get("correct", [])

    # 2. Locate answers.jsonl whether run_dir is a folder or direct file path
    run_path = Path(run_dir)
    answers_file = run_path / "answers.jsonl" if run_path.is_dir() else run_path

    right = 0
    total = 0
    wrong_ids = []

    # 3. Check each request answer against the ground truth map
    for record in read_jsonl(answers_file):
        total += 1
        req_id = record.get("id")
        pick = record.get("pick")

        # Runtime errors or missing IDs count as wrong
        if "error" in record or req_id not in correct_map:
            wrong_ids.append(req_id)
            continue

        acceptable_picks = correct_map[req_id]

        # A pick is right if in acceptable_picks; null is right if acceptable_picks is empty
        if pick in acceptable_picks or (pick is None and len(acceptable_picks) == 0):
            right += 1
        else:
            wrong_ids.append(req_id)

    return right, total, wrong_ids


def main() -> None:
    ap = argparse.ArgumentParser(description="Score a run: how many of its requests are right.")
    ap.add_argument("run_dir", help="a run folder, e.g. runs/single-1")
    ap.add_argument("--answers", default="data/public_answers.jsonl", help="the right answers (default: %(default)s)")
    args = ap.parse_args()
    right, total, wrong = score(args.run_dir, args.answers)
    print(f"{right} of {total} right")
    for request_id in wrong:
        print(request_id)


if __name__ == "__main__":
    main()