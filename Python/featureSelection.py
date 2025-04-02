import numpy as np
import pandas as pd

windowSize = 40
stepSize = 20
filePath = "Data_CleanUp_C/merged_file_extension_C_cleaned.csv"
columns = ["EMG1", "EMG2", "EMG3", "EMG4", "EMG5", "EMG6", "EMG7", "EMG8"]
columnsForTracker = ["TrackerX", "TrackerY", "TrackerZ"]
columnsForCubePos = ["ActivatedCube", "ActiveCubeX", "ActiveCubeY"]
np.set_printoptions(suppress=True)


def createDataFrameWithCalculations(windowSize, stepSize, filePath):
    """
    Specify a window size to calculate features

    :param windowSize: The size of the window
    :param stepSize: How many steps to move per loop
    :param filePath: Reference to file
    :return:
    """
    data = pd.read_csv(filePath, sep=";")

    cubeDataFrames = []
    for cube in range(25):
        cubeName = f"Cube {cube}"
        activeCube = data[data['ActivatedCube'] == cubeName]
        cubeDataFrames.append(activeCube)

    processedData = []

    for dfs in cubeDataFrames:
        mavList = []
        zeroCrossingsList = []
        sscList = []
        wflList = []
        trackerPosList = []

        # Loop through the data using the window size and step size
        for start in range(0, len(dfs) - windowSize + 1, stepSize):
            # Extract the current window of data
            currentWindow = dfs[start:start + windowSize]

            # Calculate the features (each returns a list of arrays, one array per feature)
            mav = calcMAV(currentWindow, columns)  # Returns a list of arrays for each feature
            mavList.append(mav)

            zeroCrossings = calcZeroCrossings(currentWindow, columns)  # List of arrays for each feature
            zeroCrossingsList.append(zeroCrossings)

            ssc = calcSSC(currentWindow, columns)  # List of arrays for each feature
            sscList.append(ssc)

            wfl = calcWFL(currentWindow, columns)  # List of arrays for each feature
            wflList.append(wfl)

            trackerMeanPos = calcAvgTracker(currentWindow, columnsForTracker)
            trackerPosList.append(trackerMeanPos)

            activeCube = currentWindow.iloc[0]

        mavMatrix = np.vstack(mavList)
        mavDF = pd.DataFrame(mavMatrix)

        mavSlope = calcMAVslope(mavMatrix)
        mavSlopeDF = pd.DataFrame(mavSlope).round(3)

        zeroCrossingsMatrix = np.vstack(zeroCrossingsList)
        zeroCrossDF = pd.DataFrame(zeroCrossingsMatrix)

        sscMatrix = np.vstack(sscList)
        sscDF = pd.DataFrame(sscMatrix)

        wflMatrix = np.vstack(wflList)
        wflDF = pd.DataFrame(wflMatrix)

        trackerPosMatrix = np.vstack(trackerPosList)
        trackerPos = pd.DataFrame(trackerPosMatrix)

        mavColumns = [f"EMG{i}MAV" for i in range(1, 9)]
        mavSlopeColumns = [f"EMG{i}Slope" for i in range(1, 9)]
        ZCColumns = [f"EMG{i}ZC" for i in range(1, 9)]
        sscDFColumns = [f"EMG{i}SSC" for i in range(1, 9)]
        wflDFColumns = [f"EMG{i}WFL" for i in range(1, 9)]
        trackerColumns = ["trackerX", "trackerY", "trackerZ"]
        activeCubeColumns = ["activeCube", "activeCubeX", "activeCubeY"]

        minRows = mavSlopeDF.shape[0]
        mavDF = mavDF[:minRows]
        zeroCrossDF = zeroCrossDF[:minRows]
        sscDF = sscDF[:minRows]
        wflDF = wflDF[:minRows]
        trackerPos = trackerPos[:minRows]
        cubeDF = pd.DataFrame([activeCube] * minRows, columns=columnsForCubePos)

        allFeatures = np.hstack([mavDF, mavSlopeDF, zeroCrossDF, sscDF, wflDF, cubeDF, trackerPos])
        allColumns = mavColumns + mavSlopeColumns + ZCColumns + sscDFColumns + wflDFColumns + activeCubeColumns + trackerColumns

        featuredDataSet = pd.DataFrame(allFeatures, columns=allColumns)
        processedData.append(featuredDataSet)

    combinedProcessedData = pd.concat(processedData, ignore_index=True)
    return combinedProcessedData


def calcMAV(data, columns):
    """
    Calculate Mean Absolute Value for a given column in a given dataframe
    """
    mavResults = []
    for column in columns:
        mav = float(np.mean(np.abs(data[column])))
        mavResults.append(mav)

    return mavResults


def calcMAVslope(mav):
    """
    Calculate the Mean Absolute Value Slope. This is the difference between sums in adjacent segments, i and i+ 1.
    """
    mavSlope = (np.diff(mav, axis=0))
    return mavSlope


def calcZeroCrossings(data, columns):
    """
    Calcuate Zero crossings - How many times we cross zero
    """
    zeroCrossingsResults = []
    threshold = 0.01
    for column in columns:
        zeroCrossing = 0  # Reset count for each column
        values = data[column].values  # Convert to NumPy array for efficiency

        for i in range(len(values) - 1):  # Loop through rows
            if (values[i] > 0 > values[i + 1]) or (values[i] < 0 < values[i + 1]):
                if abs(values[i] - values[i + 1]) >= threshold:
                    zeroCrossing += 1

        zeroCrossingsResults.append(zeroCrossing)

    return zeroCrossingsResults


def calcSSC(data, columns):
    """
     Slope Sign Changes - provides the number of times the slope of the waveform changes sign.
    """
    threshold = 0.01
    sscCountResults = []
    for column in columns:
        sscCount = 0
        values = data[column].values
        for i in range(1, len(values) - 1):
            prev_slope = values[i] - values[i - 1]
            next_slope = values[i + 1] - values[i]

            # Check sign change condition
            if (prev_slope > 0 > next_slope) or (prev_slope < 0 < next_slope):
                # Apply threshold condition
                if (abs(values[i] - values[i + 1]) >= threshold) or (abs(values[i] - values[i - 1]) >= threshold):
                    sscCount += 1

        sscCountResults.append(sscCount)

    return sscCountResults


def calcWFL(data, columns):
    """
    Waveform Length - information on the waveform complexity in each segment.
    This is the cumulative length of the waveform over the time segment
    """
    wflResults = []
    for column in columns:
        wfl = int(np.sum(np.abs(np.diff(data[column]))))
        wflResults.append(wfl)

    return wflResults


def calcAvgTracker(data, columns):
    trackerPosList = []
    for column in columns:
        columnMean = round(data[column].mean(), 3)
        trackerPosList.append(columnMean)
    return trackerPosList


gesture_files = [
    "Data_CleanUp_L/merged_file_extension_L_cleaned.csv",
    "Data_CleanUp_L/merged_file_fist_L_cleaned.csv",
    "Data_CleanUp_L/merged_file_flexion_L_cleaned.csv",
    "Data_CleanUp_L/merged_file_pinch_L_cleaned.csv",
    "Data_CleanUp_L/merged_file_pronation_L_cleaned.csv",
    "Data_CleanUp_L/merged_file_supination_L_cleaned.csv"
]

finalFiles = []
for file in gesture_files:
    cleanData = createDataFrameWithCalculations(windowSize, stepSize, file)
    finalFiles.append(cleanData)

finalDataset = pd.concat(finalFiles, ignore_index=True)
finalDataset.to_csv("test Data set/testData_L.csv", index=False)
print("overall dataset created")


event_names = ["Cube 0", "Cube 1", "Cube 2", "Cube 3", "Cube 4", "Cube 5", "Cube 6", "Cube 7", "Cube 8", "Cube 9", "Cube 10", "Cube 11", "Cube 12"]

# Load DataFrame (assuming CSV is read into 'df')
df = pd.read_csv("test Data set/testData_C.csv", delimiter=",")  # Adjust delimiter if needed

# Create a dictionary to store counts
event_counts = {event: (df["activeCube"] == event).sum() for event in event_names}

print(event_counts)
