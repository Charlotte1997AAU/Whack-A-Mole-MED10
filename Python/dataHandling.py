import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

df = pd.read_csv("Data_CleanUp_C/merged_file_cleaned.csv", delimiter=";")

def plot_emg_with_states(df, states_to_include, color_shading=True, show_lines=True):
    """
    Plots EMG signals over time with optional color-coded state regions and vertical lines.

    Parameters:
    df (DataFrame): The dataset containing EMG and state information.
    states_to_include (list): List of states to include in visualization.
    color_shading (bool): If True, colors background regions for selected states.
    show_lines (bool): If True, shows vertical dashed lines at state change points.
    """

    # Convert Timestamp column to datetime format
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    # Identify state change points
    state_changes = df[(df["State"] != df["State"].shift()) & (df["State"].isin(states_to_include))]

    # Plot EMG signals
    plt.figure(figsize=(12, 6))
    for i in range(1, 9):  # EMG1 to EMG8
        plt.plot(df["Timestamp"], df[f"EMG{i}"], label=f"EMG{i}")

    # Find min and max EMG values for better text positioning
    min_emg_value = df.iloc[:, 1:9].min().min()
    max_emg_value = df.iloc[:, 1:9].max().max()

    # Define colors for different states
    state_colors = {
        "MVC": "red",
        "In box": "blue",
        "Moving to Box": "green",
        "Resting": "lightyellow",
        "Moving to rest position": "gold",
    }

    # Add color-shaded regions
    if color_shading:
        prev_state = None
        start_time = None
        for _, row in df.iterrows():
            current_state = row["State"]
            if current_state in states_to_include:
                if prev_state != current_state:
                    if start_time is not None:
                        plt.axvspan(start_time, row["Timestamp"], color=state_colors.get(prev_state, "gray"), alpha=0.3)
                    start_time = row["Timestamp"]
                prev_state = current_state
        if start_time is not None:
            plt.axvspan(start_time, df["Timestamp"].iloc[-1], color=state_colors.get(prev_state, "gray"), alpha=0.3)

    # Add vertical dashed lines at state change points
    if show_lines:
        for _, row in state_changes.iterrows():
            plt.axvline(x=row["Timestamp"], color="black", linestyle="--", alpha=0.6)
            plt.text(row["Timestamp"], min_emg_value - 10, row["State"],
                     rotation=90, verticalalignment='bottom', fontsize=10, color="black", fontweight='bold')  # Bolder text here

    # Formatting the plot
    plt.xlabel("Time", fontsize=14, fontweight='bold')  # Bold label for x-axis
    plt.ylabel("EMG Signal", fontweight='bold')  # Bold label for y-axis
    plt.title("EMG Signals Over Time with State Annotations", fontsize=16, fontweight='bold')
    plt.legend()
    plt.grid(True)

    # Remove the timestamp from the x-axis by hiding the xticks
    plt.xticks([])  # This removes the x-axis tick labels

    # Make y-axis ticks bold and larger
    plt.tick_params(axis='y', labelsize=12, labelcolor='black', width=2)  # Change size and boldness
    plt.yticks(fontweight='bold', fontsize=14)  # Bold and larger font for y-ticks

    # Show the plot
    plt.show()

# Choose which states to include
states_to_include = ["MVC", "In box", "Moving to Box", "Resting", "Moving to rest position"]

# Call function with color_shading=True to enable shaded regions, or False for vertical lines
plot_emg_with_states(df, states_to_include, color_shading=True)
