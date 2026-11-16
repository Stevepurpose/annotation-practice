
import json
import csv
from pathlib import Path

# Input and output files
input_file = Path("vehicle_annotations.json")
output_file = Path("vehicle_annotations.csv")

# Exclude cancelled annotations by default
INCLUDE_CANCELLED = False

with open(input_file, "r", encoding="utf-8") as file:
    tasks = json.load(file)

rows = []
excluded = 0

for task in tasks:

    filename = task.get("file_upload", "")

    # Remove Label Studio's upload ID prefix
    if "-" in filename:
        filename = filename.split("-", 1)[1]

    for annotation in task.get("annotations", []):

        if annotation.get("was_cancelled", False):
            if not INCLUDE_CANCELLED:
                excluded += 1
                continue

        for result in annotation.get("result", []):

            if result.get("type") != "rectanglelabels":
                continue

            value = result["value"]

            original_width = result["original_width"]
            original_height = result["original_height"]

            x = value["x"]
            y = value["y"]
            width = value["width"]
            height = value["height"]

            rows.append({
                "filename": filename,
                "label": value["rectanglelabels"][0],

                "x_percent": x,
                "y_percent": y,
                "width_percent": width,
                "height_percent": height,

                "x_pixels": x * original_width / 100,
                "y_pixels": y * original_height / 100,
                "width_pixels": width * original_width / 100,
                "height_pixels": height * original_height / 100,

                "original_width": original_width,
                "original_height": original_height
            })

# Write CSV
if rows:
    with open(output_file, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=rows[0].keys()
        )

        writer.writeheader()
        writer.writerows(rows)

print("Conversion completed!")
print(f"Images in export: {len(tasks)}")
print(f"Bounding boxes extracted: {len(rows)}")
print(f"Cancelled annotations excluded: {excluded}")
print(f"Output file: {output_file}")
