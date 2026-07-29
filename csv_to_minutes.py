import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(BASE_DIR, "commute_log.csv")
DEST_PATH = os.path.join(BASE_DIR, "commute_log_minutes.csv")

DURATION_COLUMNS = ["home_to_lpc", "home_to_loop", "lpc_to_home", "loop_to_home"]

with open(SRC_PATH, newline="") as src, open(DEST_PATH, "w", newline="") as dest:
    reader = csv.DictReader(src)
    writer = csv.DictWriter(dest, fieldnames=reader.fieldnames)
    writer.writeheader()
    for row in reader:
        for col in DURATION_COLUMNS:
            row[col] = round(int(row[col]) / 60, 1)
        writer.writerow(row)

print(f"Wrote {DEST_PATH}")
