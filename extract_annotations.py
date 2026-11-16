import json
import csv
from collections import Counter

# Name of the Label Studio JSON export
json_file = "vehicle_annotations.json"

# Name of the CSV file to create
csv_file = "vehicle_annotations.csv"


# Read the JSON file
with open(json_file, "r", encoding="utf-8") as file:
    tasks = json.load(file)


# Store extracted annotations
annotations = []

for task in tasks:

    # Get the image filename
    filename = task.get("file_upload", "Unknown")

    # Get the annotation
    task_annotations = task.get("annotations", [])

    if not task_annotations:
        continue

    for annotation in task_annotations:

        results = annotation.get("result", [])

        for result in results:

            # Extract the assigned label
            labels = result.get("value", {}).get("choices", [])

            for label in labels:
                annotations.append({
                    "filename": filename,
                    "label": label
                })


# Count the labels
label_counts = Counter(
    item["label"] for item in annotations
)


# Display the results
print("ANNOTATION SUMMARY")
print("------------------")
print(f"Total annotations: {len(annotations)}")

for label, count in label_counts.items():
    print(f"{label}: {count}")


# Export to CSV
with open(csv_file, "w", newline="", encoding="utf-8") as file:

    fieldnames = ["filename", "label"]

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(annotations)


print(f"\nCSV file created: {csv_file}")
