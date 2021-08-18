from gurobipy import *

positions = range(1,251) # all possible positions
stations = range(1,19)
C = 172.8
M = range(1,4) # models
d = [145,55,50] # demand for each bike type
t = [2450,2570,2620]
b1 = [170,150,140,90,120,130,160,170,120,120,70,150,150,150,60,170,70,120]
b2 = [170,150,140,90,120,130,160,170,120,120,170,150,150,150,60,170,70,120]
b3 = [170,150,140,90,120,130,160,170,120,120,190,150,150,150,160,170,70,120]
r = []
for x in d:
	r.append(x/250)

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

'''
for s in stations:
	for p in positions:
		for t in b1:
			m.addConstr(spm[s,p,1] == b1[t])

for s in stations:
	for p in positions:
		for t in b2:
			m.addConstr(spm[s,p,2] == b2[t])

for s in stations:
	for p in positions:
		for t in b3:
			m.addConstr(spm[s,p,3] == b3[t])

abs_((x[1,k]*it[s,k,1] + x[2,k]*it[s,k,2] + x[3,k]*it[s,k,3]) + (x[1,k-1]*it[s,k,1] + x[2,k-1]*it[s,k,2] + x[3,k-1]*it[s,k,3]))


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



