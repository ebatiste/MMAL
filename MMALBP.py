from parameter import parameter
from gurobipy import *


S = 19 # Number of Stations
C = 170 # Cycle time in seconds
M = 3
models = range(M)
stations = range(1,S+1)

# BIKE 1
tasks1 = parameter()[0]
t1 = parameter()[1]
preds1 = parameter()[2]
CT1 = sum(list(t1.values())) / S

# BIKE 2
tasks2 = parameter()[3]
t2 = parameter()[4]
preds2 = parameter()[5]
CT2 = sum(list(t2.values())) / S

# BIKE 3
tasks3 = parameter()[6]
t3 = parameter()[7]
preds3 = parameter()[8]
CT3 = sum(list(t3.values())) / S


#VARIABLES
mm = Model('MMAL')
#mm.params.NonConvex = 2
x1 = mm.addVars(tasks1, stations, vtype=GRB.BINARY, name="x1_ij")  # 1 if model1 task i is performed at station j, 0 o.w.
x2 = mm.addVars(tasks2, stations, vtype=GRB.BINARY, name="x2_ij")  # 1 if model2 task i is performed at station j, 0 o.w.
x3 = mm.addVars(tasks3, stations, vtype=GRB.BINARY, name="x3_ij")  # 1 if model3 task i is performed at station j, 0 o.w.

st1 = mm.addVars(stations, name="st1_j")  # processing time at station j for model 1
st2 = mm.addVars(stations, name="st2_j")  # processing time at station j for model 2
st3 = mm.addVars(stations, name="st3_j")  # processing time at station j for model 3
ST = mm.addVars(stations, name="ST_j")  # total processing time at station j


D1 = mm.addVars(stations, name="D1_j")  # Difference from Takt time at station j for model 1
D2 = mm.addVars(stations, name="D2_j")  # Difference from Takt time at station j for model 2
D3 = mm.addVars(stations, name="D3_j")  # Difference from Takt time at station j for model 3
DA1 = mm.addVars(stations, name="D1_j")  # ABS(Difference from Takt time at station j for model 1)
DA2 = mm.addVars(stations, name="D2_j")  # ABS(Difference from Takt time at station j for model 2)
DA3 = mm.addVars(stations, name="D3_j")  # ABS(Difference from Takt time at station j for model 3)


#OBJECTIVE FUNCTION 1

mm.setObjective(quicksum(DA1[j] + DA2[j] + DA3[j] for j in stations), GRB.MINIMIZE)


#OBJECTIVE FUNCTION 2

'''
mm.setObjective(quicksum(C-st1[j] for j in stations) +\
				quicksum(C-st2[j] for j in stations) +\
				quicksum(C-st3[j] for j in stations), GRB.MINIMIZE)

'''

#OBJECTIVE FUNCTION 3
'''
mm.setObjective(1/M * (quicksum(CT1-st1[j] for j in stations)/S +\
					   quicksum(CT2-st2[j] for j in stations)/S +\
					   quicksum(CT3-st3[j] for j in stations)/S), GRB.MINIMIZE)
'''

#****************************CONSTRAINTS*********************************************

for j in stations:
	mm.addConstr(quicksum(x1[i, j] * t1[i] for i in tasks1) == st1[j])
	mm.addConstr(quicksum(x2[i, j] * t2[i] for i in tasks2) == st2[j])
	mm.addConstr(quicksum(x3[i, j] * t3[i] for i in tasks3) == st3[j])
	mm.addConstr(st1[j] + st2[j] + st3[j] == ST[j])

	mm.addConstr(st1[j] <= 190)
	mm.addConstr(st2[j] <= 190)
	mm.addConstr(st3[j] <= 190)

	mm.addConstr(C - st1[j] == D1[j])
	mm.addConstr(C - st2[j] == D2[j])
	mm.addConstr(C - st3[j] == D3[j])
	mm.addConstr(DA1[j] == abs_(D1[j]))
	mm.addConstr(DA2[j] == abs_(D2[j]))
	mm.addConstr(DA3[j] == abs_(D3[j]))


	#mm.addConstr(st1[j] >= 1)
	#mm.addConstr(st2[j] >= 1)
	#mm.addConstr(st3[j] >= 1)


for i in tasks1:
	mm.addConstr(quicksum(x1[i,j] for j in stations) == 1)
for i in tasks2:
	mm.addConstr(quicksum(x2[i,j] for j in stations) == 1)
for i in tasks3:
	mm.addConstr(quicksum(x3[i,j] for j in stations) == 1)



for i in tasks1:
	for h in preds1[i]:
		for k in stations:
			mm.addConstr(quicksum(x1[int(h),j] for j in range(1,k+1)) >= x1[i,k])
for i in tasks2:
	for h in preds2[i]:
		for k in stations:
			mm.addConstr(quicksum(x2[int(h),j] for j in range(1,k+1)) >= x2[i,k])
for i in tasks3:
	for h in preds3[i]:
		for k in stations:
			mm.addConstr(quicksum(x3[int(h),j] for j in range(1,k+1)) >= x3[i,k])

# OPTIMIZE
mm.optimize()


# Print the result
status_code = {1:'LOADED', 2:'OPTIMAL', 3:'INFEASIBLE', 4:'INF_OR_UNBD', 5:'UNBOUNDED'}

status = mm.status
print('The optimization status is {}'.format(status_code[status]))
if status == 2:
# Retrieve variables value
	print('Optimal solution:')
	for v in mm.getVars():
		print('%s = %g' % (v.varName, v.x))
	print('Optimal objective value:\n{}'.format(mm.objVal))




#_______________________________________________________________________________________________________________________________________

