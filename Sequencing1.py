from gurobipy import *

Dt = range(1,251) # all possible positions
M = range(1,4) # models
d = [145,55,50] # demand for each bike type
t = [2450,2570,2620]
r = []
for i in d:
	r.append(1/250 * i)


#VARIABLES
m = Model('SEQ')
x = m.addVars(M,Dt,vtype=GRB.BINARY, name = "x_mk") #vtype=GRB.BINARY, # 1 if model m is produced in position k

#OBJECTIVE FCN
m.setObjective(quicksum((((x[1,k]*t[0] + x[2,k]*t[1] + x[3,k]*t[2] ) + (x[1,k-1]*t[0] + x[2,k-1]*t[1] + x[3,k-1]*t[2]) ) / 2  ) for k in Dt[2:]), GRB.MINIMIZE)

#CONSTRAINTS

for k in Dt:
	m.addConstr(quicksum(x[mm,k] for mm in M) == 1)

for mm in M:
	m.addConstr(quicksum(x[mm,k]/250 for k in Dt) == r[mm-1])

'''
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




