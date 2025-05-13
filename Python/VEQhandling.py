import pandas as pd

df = pd.read_csv("EMQuestionnaire/EmbodimentQuestionnaire.csv", sep=";")


avg_q1_3 = df[["s_1", "s_2",  "s_3"]].mean(axis=1)
avg_q4_7 = df[["s_4", "s_5", "s_6", "s_7"]].mean(axis=1)
avg_q8_10 = df [["s_8", "s_9", "s_10"]].mean(axis=1)

result_df = pd.DataFrame({
    'Acceptance/Body ownership': avg_q1_3,
    'Control/Agency': avg_q4_7,
    'Change': avg_q8_10
})

overallMeans = result_df.mean()
print(overallMeans)