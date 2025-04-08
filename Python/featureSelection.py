import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

windowSize = 40
stepSize = 20
columns = ["EMG1", "EMG2", "EMG3", "EMG4", "EMG5", "EMG6", "EMG7", "EMG8"]
columnsForTracker = ["TrackerX", "TrackerY", "TrackerZ"]
columnsForCubePos = ["ActivatedCube", "ActiveCubeX", "ActiveCubeY"]
np.set_printoptions(suppress=True)


def createDataFrameWithCalculationsTraining(windowSize, stepSize, filePath):
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
        currentGesture = data['GoalGesture'].iloc[0]

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
        goalGesture = ["GoalGesture"]

        minRows = mavSlopeDF.shape[0]
        mavDF = mavDF[:minRows]
        zeroCrossDF = zeroCrossDF[:minRows]
        sscDF = sscDF[:minRows]
        wflDF = wflDF[:minRows]
        trackerPos = trackerPos[:minRows]
        cubeDF = pd.DataFrame([activeCube] * minRows, columns=columnsForCubePos)
        activatedCubeString = cubeDF["ActivatedCube"]
        activatedCubeString = activatedCubeString.str.replace("Cube ", "", regex=True)
        activatedCubeString = activatedCubeString.astype(int)
        cubeDF.drop(["ActivatedCube"], axis=1, inplace=True)
        cubeDF.insert(0, "ActivatedCube", activatedCubeString)
        gestureDF = pd.DataFrame([currentGesture] * minRows)

        allFeatures = np.hstack([mavDF, mavSlopeDF, zeroCrossDF, sscDF, wflDF, cubeDF, trackerPos, gestureDF])
        allColumns = mavColumns + mavSlopeColumns + ZCColumns + sscDFColumns + wflDFColumns + activeCubeColumns \
                     + trackerColumns + goalGesture

        featuredDataSet = pd.DataFrame(allFeatures, columns=allColumns)
        processedData.append(featuredDataSet)

    combinedProcessedData = pd.concat(processedData, ignore_index=True)
    return combinedProcessedData


def createDataFrameWithCalculationsTest(dataframe):
    """
    Calculate features on a given dataframe

    :param dataframe: Dataframe to run calculations on
    :return dataframe: Dataframe with new values calculated
    """
    data = dataframe

    mavList = []
    zeroCrossingsList = []
    sscList = []
    wflList = []
    trackerPosList = []

    # Calculate the features (each returns a list of arrays, one array per feature)
    mav = calcMAV(data, columns)  # Returns a list of arrays for each feature
    mavList.append(mav)

    zeroCrossings = calcZeroCrossings(data, columns)  # List of arrays for each feature
    zeroCrossingsList.append(zeroCrossings)

    ssc = calcSSC(data, columns)  # List of arrays for each feature
    sscList.append(ssc)

    wfl = calcWFL(data, columns)  # List of arrays for each feature
    wflList.append(wfl)

    trackerMeanPos = calcAvgTracker(data, columnsForTracker)
    trackerPosList.append(trackerMeanPos)

    mavMatrix = np.vstack(mavList)
    mavDF = pd.DataFrame(mavMatrix)

    zeroCrossingsMatrix = np.vstack(zeroCrossingsList)
    zeroCrossDF = pd.DataFrame(zeroCrossingsMatrix)

    sscMatrix = np.vstack(sscList)
    sscDF = pd.DataFrame(sscMatrix)

    wflMatrix = np.vstack(wflList)
    wflDF = pd.DataFrame(wflMatrix)

    trackerPosMatrix = np.vstack(trackerPosList)
    trackerPos = pd.DataFrame(trackerPosMatrix)

    mavColumns = [f"EMG{i}MAV" for i in range(1, 9)]
    ZCColumns = [f"EMG{i}ZC" for i in range(1, 9)]
    sscDFColumns = [f"EMG{i}SSC" for i in range(1, 9)]
    wflDFColumns = [f"EMG{i}WFL" for i in range(1, 9)]
    trackerColumns = ["trackerX", "trackerY", "trackerZ"]

    allFeatures = np.hstack([mavDF, zeroCrossDF, sscDF, wflDF, trackerPos])
    allColumns = mavColumns + ZCColumns + sscDFColumns + wflDFColumns + trackerColumns

    calculatedDataSet = pd.DataFrame(allFeatures, columns=allColumns)

    return calculatedDataSet

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
    "Data_CleanUp_C/merged_file_extension_C_cleaned.csv",
    "Data_CleanUp_C/merged_file_fist_C_cleaned.csv",
    "Data_CleanUp_C/merged_file_flexion_C_cleaned.csv",
    "Data_CleanUp_C/merged_file_pinch_C_cleaned.csv",
    "Data_CleanUp_C/merged_file_pronation_C_cleaned.csv",
    "Data_CleanUp_C/merged_file_supination_C_cleaned.csv"
]

"""
finalFiles = []
for file in gesture_files:
    cleanData = createDataFrameWithCalculations(windowSize, stepSize, file)
    finalFiles.append(cleanData)

finalDataset = pd.concat(finalFiles, ignore_index=True)
le = LabelEncoder()
finalDataset["GoalGesture"] = le.fit_transform(finalDataset["GoalGesture"])
finalDataset = finalDataset.apply(pd.to_numeric)
print(finalDataset.dtypes)
finalDataset.to_csv("test Data set/testData_C.csv", index=False)
print("overall dataset created")
"""