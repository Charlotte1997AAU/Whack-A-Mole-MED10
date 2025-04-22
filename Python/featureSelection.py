import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
pd.set_option('future.no_silent_downcasting', True)
pd.options.mode.copy_on_write = True

windowSize = 40
stepSize = 20
sensitivityFactor = 1.5
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
    data = filePath
    cubeDataFrames = []
    if data['GoalGesture'].iloc[0] != "Resting":
        for cube in range(9):
            cubeName = f"Cube {cube}"
            activeCube = data[data['ActivatedCube'] == cubeName]
            cubeDataFrames.append(activeCube)
    else:
        cubeDataFrames.append(data)


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
        if data['GoalGesture'].iloc[0] != "Resting":
            activatedCubeString = cubeDF["ActivatedCube"]
            activatedCubeString = activatedCubeString.str.replace("Cube ", "", regex=True)
            activatedCubeString = activatedCubeString.astype(int)
            cubeDF.drop(["ActivatedCube"], axis=1, inplace=True)
            cubeDF.insert(0, "ActivatedCube", activatedCubeString)
        else:
            cubeDF.drop(["ActivatedCube"], axis=1, inplace=True)
            cubeDF.insert(0, "ActivatedCube", -1) 
        gestureDF = pd.DataFrame([currentGesture] * minRows)

        allFeatures = np.hstack([mavDF, mavSlopeDF, zeroCrossDF, sscDF, wflDF, cubeDF, trackerPos, gestureDF])
        allColumns = mavColumns + mavSlopeColumns + ZCColumns + sscDFColumns + wflDFColumns + activeCubeColumns \
                     + trackerColumns + goalGesture

        featuredDataSet = pd.DataFrame(allFeatures, columns=allColumns)
        processedData.append(featuredDataSet)

    combinedProcessedData = pd.concat(processedData, ignore_index=True)
    print(f"Calculated features for gesture: {data['GoalGesture'].iloc[0]}")
    return combinedProcessedData


def calculateDeltaFeatures(data):
    mav_columns = [f"EMG{i}MAV" for i in range(1, 9)]
    slope_columns = [f"EMG{i}Slope" for i in range(1, 9)]
    zc_columns = [f"EMG{i}ZC" for i in range(1, 9)]
    ssc_columns = [f"EMG{i}SSC" for i in range(1, 9)]
    wfl_columns = [f"EMG{i}WFL" for i in range(1, 9)]

    mavDelta = round(data[mav_columns].diff(), 3)
    slopeDelta = round(data[slope_columns].diff(), 3)
    zcDelta = round(data[zc_columns].diff(), 3)
    wflDelta = round(data[wfl_columns].diff(), 3)
    sscDelta = round(data[ssc_columns].diff(), 3)

    mavDelta.columns = [col.replace("MAV", "DELTAMAV") for col in mavDelta.columns]
    slopeDelta.columns = [col.replace("Slope", "DELTASlope") for col in slopeDelta.columns]
    zcDelta.columns = [col.replace("ZC", "DELTAZC") for col in zcDelta.columns]
    wflDelta.columns = [col.replace("WFL", "DELTAWFL") for col in wflDelta.columns]
    sscDelta.columns = [col.replace("SSC", "DELTASSC") for col in sscDelta.columns]

    mavDelta = mavDelta.dropna().reset_index(drop=True)
    slopeDelta = slopeDelta.dropna().reset_index(drop=True)
    zcDelta = zcDelta.dropna().reset_index(drop=True)
    wflDelta = wflDelta.dropna().reset_index(drop=True)
    sscDelta = sscDelta.dropna().reset_index(drop=True)

    deltaList = [mavDelta, slopeDelta, zcDelta, wflDelta, sscDelta]
    deltaDf = pd.concat(deltaList, axis=1)

    # Compute max absolute delta per feature group
    deltaDf["mav_max"] = deltaDf[mavDelta.columns].abs().max(axis=1)
    deltaDf["slope_max"] = deltaDf[slopeDelta.columns].abs().max(axis=1)
    deltaDf["zc_max"] = deltaDf[zcDelta.columns].abs().max(axis=1)
    deltaDf["wfl_max"] = deltaDf[wflDelta.columns].abs().max(axis=1)
    deltaDf["ssc_max"] = deltaDf[sscDelta.columns].abs().max(axis=1)

    mavThresh = deltaDf["mavTresh"] = (
        deltaDf["mav_max"].rolling(window=10, min_periods=1).mean() +
        sensitivityFactor * deltaDf["mav_max"].rolling(window=10, min_periods=1).std()
    )
    slopeThresh = deltaDf["slopeTresh"] = (
        deltaDf["slope_max"].rolling(window=10, min_periods=1).mean() +
        sensitivityFactor * deltaDf["slope_max"].rolling(window=10, min_periods=1).std()
    )

    zcThresh = deltaDf["zcTresh"] = (
            deltaDf["zc_max"].rolling(window=10, min_periods=1).mean() +
            sensitivityFactor * deltaDf["zc_max"].rolling(window=10, min_periods=1).std()
    )

    wflThresh = deltaDf["wflTresh"] = (
            deltaDf["wfl_max"].rolling(window=10, min_periods=1).mean() +
            sensitivityFactor * deltaDf["wfl_max"].rolling(window=10, min_periods=1).std()
    )

    sscThresh = deltaDf["sscTresh"] = (
        deltaDf["ssc_max"].rolling(window=10, min_periods=1).mean() +
        sensitivityFactor * deltaDf["ssc_max"].rolling(window=10, min_periods=1).std()
    )



    deltaDf["onsetFlag"] = (
            (deltaDf["mav_max"] > mavThresh) |
            (deltaDf["slope_max"] > slopeThresh) |
            (deltaDf["zc_max"] > zcThresh) |
            (deltaDf["wfl_max"] > wflThresh) |
            (deltaDf["ssc_max"] > sscThresh)
    )

    deltaDf.drop(["mav_max", "slope_max", "zc_max", "wfl_max", "ssc_max"], axis=1, inplace=True)
    newDataFrame = [data, deltaDf]
    data = pd.concat(newDataFrame, axis=1)

    data["gestureStart"] = data["onsetFlag"] & ~data["onsetFlag"].shift(1).fillna(False)
    trainingWindows = data[data["gestureStart"] == True]
    trainingWindows.drop(["onsetFlag", "gestureStart"], axis=1, inplace=True)
    return trainingWindows


def createDataFrameWithCalculationsTest(dataframe, windowSize=5, stepSize=1):
    data = dataframe

    mavList = []
    zeroCrossingsList = []
    sscList = []
    wflList = []
    trackerPosList = []

    for start in range(0, len(data) - windowSize + 1, stepSize):
        currentWindow = data[start:start + windowSize]

        mavList.append(calcMAV(currentWindow, columns))
        zeroCrossingsList.append(calcZeroCrossings(currentWindow, columns))
        sscList.append(calcSSC(currentWindow, columns))
        wflList.append(calcWFL(currentWindow, columns))
        trackerPosList.append(calcAvgTracker(currentWindow, columnsForTracker))

    mavMatrix = np.vstack(mavList)
    zeroCrossingsMatrix = np.vstack(zeroCrossingsList)
    sscMatrix = np.vstack(sscList)
    wflMatrix = np.vstack(wflList)
    trackerPosMatrix = np.vstack(trackerPosList)

    mavSlope = calcMAVslope(mavMatrix)

    # Convert all to DataFrames
    mavDF = pd.DataFrame(mavMatrix)
    mavSlopeDF = pd.DataFrame(mavSlope).round(3)
    zeroCrossDF = pd.DataFrame(zeroCrossingsMatrix)
    sscDF = pd.DataFrame(sscMatrix)
    wflDF = pd.DataFrame(wflMatrix)
    trackerPos = pd.DataFrame(trackerPosMatrix)

    # Clip all to match the length of mavSlopeDF
    minRows = mavSlopeDF.shape[0]
    mavDF = mavDF[:minRows]
    zeroCrossDF = zeroCrossDF[:minRows]
    sscDF = sscDF[:minRows]
    wflDF = wflDF[:minRows]
    trackerPos = trackerPos[:minRows]

    # Columns
    mavColumns = [f"EMG{i}MAV" for i in range(1, 9)]
    mavSlopeColumns = [f"EMG{i}Slope" for i in range(1, 9)]
    ZCColumns = [f"EMG{i}ZC" for i in range(1, 9)]
    sscDFColumns = [f"EMG{i}SSC" for i in range(1, 9)]
    wflDFColumns = [f"EMG{i}WFL" for i in range(1, 9)]
    trackerColumns = ["trackerX", "trackerY", "trackerZ"]

    allFeatures = np.hstack([mavDF, mavSlopeDF, zeroCrossDF, sscDF, wflDF, trackerPos])
    allColumns = mavColumns + mavSlopeColumns + ZCColumns + sscDFColumns + wflDFColumns + trackerColumns

    return pd.DataFrame(allFeatures, columns=allColumns)


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




