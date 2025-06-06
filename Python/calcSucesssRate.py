import os
import pandas as pd

base_path="TestData"

all_data = []
sections = []

for folder in os.listdir(base_path):
    if folder.startswith("Participant "):
        participantNr = int(folder.split(" ")[1])
        file_path = os.path.join(base_path, folder, f"Test_log_{participantNr}.csv")
        data = pd.read_csv(file_path, sep=";")

        # Boolean mask for "InCube" == "InCube"
        mask = data["InCube"] == "InCube"

        # Identify group boundaries of consecutive "InCube" == "InCube" rows
        group = (mask != mask.shift()).cumsum()

        # Iterate through each group
        for g, group_df in data.groupby(group):
            if group_df["InCube"].iloc[0] == "InCube":
                sections.append(group_df)

    

    print(len(sections))
