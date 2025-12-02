import argparse
import json
import os

from extractor import extract_tasks
from utils import clean_text

# OPTIONAL: Uncomment to enable Whisper STT
# from stt import audio_to_text_whisper as audio_to_text

def load_team(team_path):
    with open(team_path, 'r') as f:
        return json.load(f)

def load_transcript(path):
    with open(path, 'r') as f:
        return f.read()

def save_outputs(tasks, out_dir):
    os.makedirs(out_dir, exist_ok=True)

    json_path = os.path.join(out_dir, "extracted_tasks.json")
    csv_path = os.path.join(out_dir, "extracted_tasks.csv")

    with open(json_path, "w") as f:
        json.dump(tasks, f, indent=2)

    import csv
    keys = ["id", "description", "assigned_to", "deadline", "priority", "dependencies", "inferred_skills"]
    with open(csv_path, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for t in tasks:
            row = {k: (", ".join(t[k]) if isinstance(t[k], list) else t[k]) for k in keys}
            writer.writerow(row)

    print(f"✔ Saved JSON: {json_path}")
    print(f"✔ Saved CSV : {csv_path}")

def main():
    parser = argparse.ArgumentParser(description="Meeting Task Assignment System")
    parser.add_argument("--team", required=True)
    parser.add_argument("--transcript", required=True)
    parser.add_argument("--out", default="outputs")
    args = parser.parse_args()

    team = load_team(args.team)

    if args.transcript.startswith("audio:"):
        audio_path = args.transcript.split("audio:", 1)[1]
        # Uncomment to use Whisper:
        # transcript = audio_to_text(audio_path)
        raise RuntimeError("Audio mode enabled, but STT is not uncommented.")
    else:
        transcript = load_transcript(args.transcript)

    transcript = clean_text(transcript)
    tasks = extract_tasks(transcript, team)

    save_outputs(tasks, args.out)

if __name__ == "__main__":
    main()
