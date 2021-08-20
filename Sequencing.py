import pandas as pd
from gurobipy import *
import math

positions = range(1,251) # all possible positions
stations = range(1,19)
C = 172.8
M = range(1,4) # models
d = [145,55,50] # demand for each bike type

file = 'ALLBIKEDATA.xlsx'
xl = pd.ExcelFile(file)
df = xl.parse('Sequencing.py Data')

b1 = [int(x) for x in df["Race Bike"].tolist() if math.isnan(x) == False]
b2 = [int(x) for x in df["Mountain Bike"].tolist() if math.isnan(x) == False]
b3 = [int(x) for x in df["Ebike"].tolist() if math.isnan(x) == False]



#VARIABLES
m = Model('SEQ')
x = m.addVars(M,positions,vtype=GRB.BINARY, name = "x_mk") #vtype=GRB.BINARY, # 1 if model m is produced in position p
#spm = m.addVars(stations,positions,M, name = "spm") #station time for position x and model m
it = m.addVars(stations,positions,M, name = "it") #idle time
itt = m.addVars(stations,positions, name = "itt") #idle time
itta = m.addVars(stations,positions, name = "itta") #idle time abs after addition


#OBJECTIVE FCN
m.setObjective(quicksum(quicksum( itta[s,k] for s in stations) for k in positions), GRB.MINIMIZE)
#m.setObjective(12, GRB.MINIMIZE)


#CONSTRAINTS
for k in positions:
	m.addConstr(quicksum(x[mm,k] for mm in M) == 1)

for mm in M:
	m.addConstr(quicksum(x[mm,k] for k in positions) == d[mm-1])

'''
##### IDLE TIME ######
for s in stations:
	for p in positions:
		m.addConstr(it[s,p,1] == (C - b1[s-1]) * x[1,p])
for s in stations:
	for p in positions:
		m.addConstr(it[s,p,2] == (C - b2[s-1]) * x[2,p])
for s in stations:
	for p in positions:
		m.addConstr(it[s,p,3] == (C - b3[s-1]) * x[3,p])

'''

for p in positions[2:]:
	for s in stations:
		m.addConstr(itt[s,p-1] == ((C - b1[s-1]) * x[1,p] + (C - b2[s-1]) * x[2,p] + (C - b3[s-1]) * x[3,p-1]) + ((C - b1[s-1]) * x[1,p-1] + (C - b2[s-1]) * x[2,p-1] + (C - b3[s-1]) * x[3,p-1]))
		m.addGenConstrAbs(itta[s,p-1],itt[s,p-1],"absconstr")


'''
for p in positions[2:]:
	for s in stations:
		m.addConstr(itt[s,p-1] == (it[s,p,1]+it[s,p,2]+it[s,p,3]) + (it[s,p-1,1]+it[s,p-1,2]+it[s,p-1,3]))
		m.addGenConstrAbs(itta[s,p-1],itt[s,p-1],"absconstr")


for mm in M:
	for k in Dt[2:]:
		m.addConstr(x[mm,k]-x[mm,k-1] <= 1)
		m.addConstr(x[mm,k]-x[mm,k-1] >= 0)

'''
#_______________________________________________________________________________________________________________________________________
# OPTIMIZE
m.optimize()


# Print the result
status_code = {1:'LOADED', 2:'OPTIMAL', 3:'INFEASIBLE', 4:'INF_OR_UNBD', 5:'UNBOUNDED'}

status = m.status
print('The optimization status is {}'.format(status_code[status]))
if status == 2:
# Retrieve variables value
	print('Optimal solution:')
	for v in m.getVars():
		print('%s = %g' % (v.varName, v.x))
	print('Optimal objective value:\n{}'.format(m.objVal))


