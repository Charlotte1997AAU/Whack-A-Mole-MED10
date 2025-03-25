import pandas as pd
import matplotlib.pyplot as plt


def plot_emg_with_states(gesture_name, states_to_include, emg_signals_to_include=None, color_shading=True,
                         show_lines=True):
    """
    Plots selected EMG signals over time with optional color-coded state regions and vertical lines.
    The CSV file is dynamically loaded based on the gesture name.

    Parameters:
    gesture_name (str): The name of the gesture to focus on (e.g., "pinch").
    states_to_include (list): List of states to include in visualization.
    emg_signals_to_include (list): List of EMG signals to plot (e.g., [1, 3, 5] to plot EMG1, EMG3, and EMG5).
    color_shading (bool): If True, colors background regions for selected states.
    show_lines (bool): If True, shows vertical dashed lines at state change points.
    """

    # Load the appropriate CSV file based on the gesture_name
    file_path = f"Data_CleanUp_C/merged_file_{gesture_name}_C_cleaned.csv" #Change to Data_CleanUp_L and to "L" after the gesture name
    df = pd.read_csv(file_path, delimiter=";")

    # Convert Timestamp column to datetime format
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    # Identify state change points
    state_changes = df[(df["State"] != df["State"].shift()) & (df["State"].isin(states_to_include))]

    # Plot EMG signals
    plt.figure(figsize=(12, 6))

    # If emg_signals_to_include is None, include all EMG signals (EMG1 to EMG8)
    emg_signals_to_include = emg_signals_to_include or list(range(1, 9))  # Default to all 8 signals if not specified

    # Plot only the selected EMG signals
    for i in emg_signals_to_include:  # Loop through the selected EMG signals
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
                     rotation=90, verticalalignment='bottom', fontsize=10, color="black", fontweight='bold')

    # Formatting the plot
    plt.xlabel("Time", fontsize=14, fontweight='bold')  # Bold label for x-axis
    plt.ylabel("EMG Signal", fontweight='bold')  # Bold label for y-axis
    plt.title(f"EMG Signals Over Time with State Annotations ({gesture_name.capitalize()} Gesture)", fontsize=16,
              fontweight='bold')  # Dynamic title based on gesture
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

# Choose which EMG signals to include, e.g., plot only EMG1, EMG3, and EMG5
emg_signals_to_include = [1, 2, 3, 4, 5, 6, 7, 8]

# Example usage:
gesture_name = "supination"  # choose which gesture to look at. "extension", "fist", "flexion", "pinch", "pronation" or "supination"
plot_emg_with_states(gesture_name,
                     states_to_include,
                     emg_signals_to_include=emg_signals_to_include,
                     color_shading=True)
