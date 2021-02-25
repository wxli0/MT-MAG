import sys 
import pandas as pd

MLDSP_prediction = pd.read_csv("outputs/MLDSP-prediction-full-path.csv", index_col=0, header=0)
everything = pd.read_excel("outputs/everything.xlsx", \
    index_col=0, header=0, sheet_name="everything_pred-t-p") 

preds = []
for index, row in MLDSP_prediction.iterrows():
    preds.append(everything.loc[index]['rejection-f'])

MLDSP_prediction['merged-pred'] = preds
print(MLDSP_prediction)

MLDSP_prediction.to_csv("outputs/MLDSP-prediction.csv")
