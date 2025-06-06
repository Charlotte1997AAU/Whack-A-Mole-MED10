import os
import pandas as pd
from collections import defaultdict

base_path = "TestData"

gesture_names = {
    0: "Extension",
    1: "Fist",
    2: "Flexion",
    3: "Pinch"
}

participant_gesture_counts = defaultdict(lambda: defaultdict(int))

for folder in os.listdir(base_path):
    if folder.startswith("Participant "):
        participantNr = int(folder.split(" ")[1])
        file_path = os.path.join(base_path, folder, f"Test_log_{participantNr}.csv")
        data = pd.read_csv(file_path, sep=";")

        # Boolean mask for "InCube" == "InCube"
        mask = data["InCube"] == "InCube"
        group = (mask != mask.shift()).cumsum()

        for _, section in data.groupby(group):
            if section["InCube"].iloc[0] == "InCube" and len(section) > 48:
                true_labels = section["GoalGesture"].astype(int).reset_index(drop=True)
                pred_labels = section["Prediction"].astype(int).reset_index(drop=True)

                gesture_id = true_labels.iloc[0]
                gesture_name = gesture_names.get(gesture_id, f"Unknown ({gesture_id})")

                match = (true_labels == pred_labels).astype(int)
                rolling_match = match.rolling(window=3).sum()

                # Check for any streak of 3 correct predictions
                if (rolling_match == 3).any():
                    participant_gesture_counts[participantNr][gesture_name] += 1

# Print the results
global_gesture_totals = {
    "Extension": 0,
    "Fist": 0,
    "Flexion": 0,
    "Pinch": 0
}
grand_total = 0

for participant in sorted(participant_gesture_counts.keys()):
    print(f"Participant {participant}:")
    participantTotal = 0

    for gesture_id in range(4):
        gesture_name = gesture_names[gesture_id]
        count = participant_gesture_counts[participant].get(gesture_name, 0)
        print(f"  {gesture_name}: {count}")
        participantTotal += count
        global_gesture_totals[gesture_name] += count
        grand_total += count

    print(f"  Total: {participantTotal}")

# Print global totals
print("\n=== Total Across All Participants ===")
for gesture_name in ["Extension", "Fist", "Flexion", "Pinch"]:
    print(f"{gesture_name}: {global_gesture_totals[gesture_name]} {round(global_gesture_totals[gesture_name]/162*100, 2)}")
print(f"Grand Total: {grand_total}")



