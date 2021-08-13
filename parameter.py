import pandas as pd
import math


def parameter():
	file = 'ALLBIKEDATA.xlsx'
	xl = pd.ExcelFile(file)
	df = xl.parse('Precedences')

# Bike 1
	tasks_b1 = [x for x in df["Tasks"].tolist() if math.isnan(x) == False]
	timelist1 = [x for x in df["Time"].tolist() if math.isnan(x) == False]
	time_b1 = {x:y for (x,y) in zip(tasks_b1,timelist1)}
	predlist1 = [str(x).split(",") if str(x) != 'nan' else [] for x in df["Precessor"].tolist()]
	pred_b1 = {x:y for (x,y) in zip(tasks_b1,predlist1)}

# Bike 2
	tasks_b2 = [x for x in df["Tasks.1"].tolist() if math.isnan(x) == False]
	timelist2 = [x for x in df["Time.1"].tolist() if math.isnan(x) == False]
	time_b2 = {x:y for (x,y) in zip(tasks_b2,timelist2)}
	predlist2 = [str(x).split(",") if str(x) != 'nan' else [] for x in df["Precessor.1"].tolist()]
	pred_b2 = {x:y for (x,y) in zip(tasks_b2,predlist2)}

# Bike 3
	tasks_b3 = [x for x in df["Tasks.2"].tolist() if math.isnan(x) == False]
	timelist3 = [x for x in df["Time.2"].tolist() if math.isnan(x) == False]
	time_b3 = {x:y for (x,y) in zip(tasks_b3, timelist3)}
	predlist3 = [str(x).split(",") if str(x) != 'nan' else [] for x in df["Precessor.2"].tolist()]
	pred_b3 = {x:y for (x,y) in zip(tasks_b3,predlist3)}



#_______________________________________________________________________________________________

	return tasks_b1,time_b1,pred_b1,tasks_b2,time_b2,pred_b2,tasks_b3,time_b3,pred_b3
