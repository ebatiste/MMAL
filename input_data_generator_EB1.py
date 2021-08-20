import json
import pandas as pd
from random import *

j_son = []
j_son_1 = []
d = []
##################### Bike 1 ###################

int_dpt = []
int_id = []
value = [] #Predecessor List

AVO_0 = []
AVO_1 = []
AVO_2 = []
##################### Bike 2 ###################
int_dpt2 = []
int_id2 = []
value2 = [] #Predecessor List

AVO_02 = []
AVO_12 = []
AVO_22 = []

##################### Bike 3 ###################
int_dpt3 = []
int_id3 = []
value3 = [] #Predecessor List

AVO_03 = []
AVO_13 = []
AVO_23 = []


###############################
###############################
###### I - N - P - U - T ######
###############################
###############################


DATA_FILE = 'ALLBIKEDATA.xlsx'
DATA_FILE1 = 'Sequencing1.xlsx'

#################################   Read Excel data    #########################################

df = pd.read_excel(DATA_FILE, sheet_name='Work Plan', header=0,converters={'internal_depth':int,'internal_id':int,'internal_depth.1':int,'internal_id.1':int,'internal_depth.2':int,'internal_id.2':int})
prcd = pd.read_excel(DATA_FILE, sheet_name='Precedences', header=0)
seq1 = pd.read_excel(DATA_FILE1, sheet_name='Sequence1-Optimal',header=0)
seq2 = pd.read_excel(DATA_FILE1, sheet_name='Sequence2-Min Avg',header=0)
seq3 = pd.read_excel(DATA_FILE1, sheet_name='Sequence2-Random',header=0)


############# Sequencing Options ###########
pos1 = [x for x in seq1["pos"].tolist()]
biketype1 = [x for x in seq1["biketype"].tolist()]
sequence1 = [(x,y) for x,y in zip(pos1,biketype1)]

pos2 = [x for x in seq2["pos"].tolist()]
biketype2 = [x for x in seq2["biketype"].tolist()]
sequence2 = [(x,y) for x,y in zip(pos2,biketype2)]

pos3 = [x for x in seq3["pos"].tolist()]
biketype3 = [x for x in seq3["biketype"].tolist()]
sequence3 = [(x,y) for x,y in zip(pos3,biketype3)]


no_jobs = len(sequence1)  # int(input("How many jobs should be created?"))
mode = 1  # 1=auto, 2=manual  #Variantenauswahl

#################################     BIKE 1 Data      ########################################
for i in range(0,len(df)):
    int_dpt.append(df.iloc[i,0])
    int_id.append(df.iloc[i,1])
    value.append(df.iloc[i,2])

for i in range(1,len(prcd)):
    AVO_0.append(prcd.iloc[i,0])
    AVO_1.append(prcd.iloc[i,2])


for i in AVO_1:
    dummy = ''.join(str(e) for e in AVO_1)
    dummy.split()
    AVO_2.append(dummy)
    dummy = []

#################################     BIKE 2 Data      ########################################
for i in range(0,len(df)):
    int_dpt2.append(df.iloc[i,5])
    int_id2.append(df.iloc[i,6])
    value2.append(df.iloc[i,7])

for i in range(1,len(prcd)):
    AVO_02.append(prcd.iloc[i,4])
    AVO_12.append(prcd.iloc[i,6])


for i in AVO_12:
    dummy = ''.join(str(e) for e in AVO_12)
    dummy.split()
    AVO_22.append(dummy)
    dummy = []

#################################     BIKE 3 Data      ########################################
for i in range(0,len(df)):
    int_dpt3.append(df.iloc[i,10])
    int_id3.append(df.iloc[i,11])
    value3.append(df.iloc[i,12])

for i in range(1,len(prcd)):
    AVO_03.append(prcd.iloc[i,8])
    AVO_13.append(prcd.iloc[i,10])


for i in AVO_13:
    dummy = ''.join(str(e) for e in AVO_13)
    dummy.split()
    AVO_23.append(dummy)
    dummy = []



####################### Build List ################################################################################################

od = [None] * no_jobs #Leere Order-Liste mit der Länge "Anzahl Aufträge" erstellen

for n in sequence1: #CHANGE SEQUENCE HERE

    indices_1 = []
    values = []

    if n[1] == 'R':
        values = list(value)
        indices_1 = [i for i, x in enumerate(int_dpt) if x == 1]
        indices_1.append(len(int_dpt))

        t_id = []
        for i in indices_1[0:-1]:
            t_id.append(int_id[i])
    elif n[1] == 'M':
        values =  list(value2)
        indices_1 = [i for i, x in enumerate(int_dpt2) if x == 1]  # Indexe der AVOs (No.1)
        indices_1.append(len(int_dpt2))

        t_id = []
        for i in indices_1[0:-1]:
            t_id.append(int_id2[i])
    else :
        values = list(value3)
        indices_1 = [i for i, x in enumerate(int_dpt3) if x == 1]  # Indexe der AVOs (No.1)
        indices_1.append(len(int_dpt3))

        t_id = []
        for i in indices_1[0:-1]:
            t_id.append(int_id3[i])

    machines=[]
    durations=[]
    materials=[]
###############################################################################
    for i in range(0,len(indices_1)-1):  #### ITERIERE ÜBER TASKS
        int_dpt_temp_1 = []
        int_id_temp_1 = []
        value_temp_1 = []
        #AVO-Bereiche bilden
        if n[1] == 'R':
            int_dpt_temp_1 = int_dpt[indices_1[i]:indices_1[i+1]]
            int_id_temp_1 = int_id[indices_1[i]:indices_1[i+1]]
            value_temp_1 = values[indices_1[i]:indices_1[i+1]]
        elif n[1] == 'M':
            int_dpt_temp_1 = int_dpt2[indices_1[i]:indices_1[i + 1]]
            int_id_temp_1 = int_id2[indices_1[i]:indices_1[i + 1]]
            value_temp_1 = values[indices_1[i]:indices_1[i + 1]]
        else:
            int_dpt_temp_1 = int_dpt3[indices_1[i]:indices_1[i + 1]]
            int_id_temp_1 = int_id3[indices_1[i]:indices_1[i + 1]]
            value_temp_1 = values[indices_1[i]:indices_1[i + 1]]

        #Anzahl Ausstattungsvarianten und deren Bereiche bilden
        indices_2 = [i for i, x in enumerate(int_dpt_temp_1) if x == 2] #Indexe der Ausstattungsvarianten (No.2)
        materials_dummy = []
        amount_mat = []

        #Wahl der Ausstattungsvariante
        if len(indices_2) > 0: # Wenn >1 AVO-Varianten

            #### BEREICH 2 (AVO) AUSWÄHLEN
            if mode == 1:
                var=(randint(1, len(indices_2)))-1

            elif mode == 2:
                print("Es gibt " + str(len(indices_2)) + " verschiedene Ausstattungsvarianten: ")
                for j in range(0, len(indices_2)):
                    print("(" + str(j) + ") " + str(value_temp_1[indices_2[j]]))
                var=int(input("Welche Ausstattungsvariante willst Du?")) #Gewählte Ausstattungsvariante
            else:
                pass

            indices_2.append(len(int_dpt_temp_1)) #Zum Ende hin verlängern, damit drüber bis zum Ende interiert werden kann

            #AB HIER IN BEREICH 2 (AUSSTATTUNGSVARIANTE REINGEHEN, UM BAUTEIL AUSZUSUCHEN) -> Nach else in der Schleife auch nochmal machen
            #Prüfen, ob es zur Ausstattungsvarianten verschiedene Bauteile gibt!
            int_dpt_temp_2=int_dpt_temp_1[indices_2[var]:indices_2[var+1]]
            int_id_temp_2 = int_id_temp_1[indices_2[var]:indices_2[var+1]]
            value_temp_2 = value_temp_1[indices_2[var]:indices_2[var+1]]


            indices_5 = [i for i, x in enumerate(int_dpt_temp_2) if x == 5]  # Indexe der Ausstattungsvarianten (No.2)


            for i in range(1,len(int_dpt_temp_2)-1):

                #MACHINES RAUSSCHREIBEN
                if int_dpt_temp_2[i] == 3:
                    machines.append(value_temp_2[i])
                else:
                    pass

                #DURATIONS RAUSSCHREIBEN
                if int_dpt_temp_2[i]==4:
                    durations.append(value_temp_2[i])
                else:
                    pass

            ###########################################
            #MATERIALS & MATERIAL AMOUNTS RAUSSCHREIBEN
            indices_5_temp=[]
            indices_5_temp.append([])
            j=0


            #####################  INDICES 5 UMSCHREIBEN ZU INDICES 5 TEMP  ###################
            if len(indices_5)>0:

                if len(indices_5)==1:
                    indices_5_temp.append(indices_5)
                    indices_5_temp.remove([])

                for i in range(0, len(indices_5)-1):
                    if indices_5[i]+1==indices_5[i+1]:
                        indices_5_temp[j].append(indices_5[i])
                    else:
                        pass

                    if indices_5[i]+1<indices_5[i+1]:
                        indices_5_temp[j].append(indices_5[i])
                        j=j+1
                        indices_5_temp.append([])
                    else:
                        pass

                    if i==len(indices_5)-2:
                        indices_5_temp[j].append(indices_5[-1])
                    else:
                        pass

            #################   AUSWAHL MATERIAL (MATERIALS_DUMMY FÜLLEN)   #######################
                for i in range(0,len(indices_5_temp)):
                    if len(indices_5_temp[i])>1:

                        if mode == 1:
                            var = (randint(1, len(indices_5_temp[i]))) - 1
                        elif mode==2:
                            k = 0
                            print("Es gibt verschiedene Bauteile/Qualitäten/Hersteller:")
                            for j in indices_5_temp[i]:
                                print("(" + str(k) + ")" + str(value_temp_2[j]))
                                k = k + 1
                            var = int(input("Welche willst Du?"))  # Gewählte Variante
                        else:
                            pass

                        # GEWÄHLTE VARIANTE TEMPORÄR FESTHALTEN


                        materials_dummy.append(int_id_temp_2[(indices_5_temp[i][0]+var)])

                    elif len(indices_5_temp[i])==1:
                        materials_dummy.append(int_id_temp_2[(indices_5_temp[i][0])])
                    else:
                        pass


                    # MENGE ZUR VARIANTE FESTHALTEN
                    if int_dpt_temp_2[(indices_5_temp[i][-1]+1)] == 6:
                        amount_mat.append(value_temp_2[(indices_5_temp[i][-1]+1)])
                    else:
                       pass

            else:
                materials_dummy.append([])
                amount_mat.append([])
                ################################################################

            for i in range(0, len(materials_dummy)):
                d.append(materials_dummy[i])
                d.append(amount_mat[i])

            materials.append(d)
            d = []

        else: #Wenn nur 1 AVO-Variante

            indices_5 = [i for i, x in enumerate(int_dpt_temp_1) if x == 5]  # Indizes der Ausstattungsvarianten (No.2)


            for i in range(1, len(int_dpt_temp_1) - 1):

                # MACHINES RAUSSCHREIBEN
                if int_dpt_temp_1[i] == 3:
                    machines.append(value_temp_1[i])
                else:
                    pass

                # DURATIONS RAUSSCHREIBEN
                if int_dpt_temp_1[i] == 4:
                    # Hier No 3 rausschreiben
                    # Hier No 4 rausschreiben
                    durations.append(value_temp_1[i])
                else:
                    pass

            # MATERIALS & MATERIAL AMOUNTS RAUSSCHREIBEN
            indices_5_temp = []
            indices_5_temp.append([])
            j = 0


            if len(indices_5)>0: #Wenn Materialien notwendig sind für den AVO

                if len(indices_5)==1:
                    indices_5_temp.append(indices_5)
                    indices_5_temp.remove([])

                for i in range(0, len(indices_5) - 1):
                    if indices_5[i] + 1 == indices_5[i + 1]:
                        indices_5_temp[j].append(indices_5[i])
                    else:
                        pass

                    if indices_5[i] + 1 < indices_5[i + 1]:
                        indices_5_temp[j].append(indices_5[i])
                        j = j + 1
                        indices_5_temp.append([])
                    else:
                        pass

                    if i == len(indices_5) - 2:
                        indices_5_temp[j].append(indices_5[-1])
                    else:
                        pass


                    if len(indices_5)==1:
                        indices_5_temp.append(indices_5[0])
                    else:
                        pass


                for i in range(0, len(indices_5_temp)):
                    if len(indices_5_temp[i]) > 1:

                        if mode==1:
                            var = (randint(1, len(indices_5_temp[i]))) - 1
                        elif mode==2:
                            k = 0
                            print("Es gibt verschiedene Bauteile/Qualitäten/Hersteller:")
                            for j in indices_5_temp[i]:
                                print("(" + str(k) + ")" + str(value_temp_2[j]))
                                k = k + 1
                            var = int(input("Welche willst Du?"))  # Gewählte Variante
                        else:
                            pass

                        # GEWÄHLTE VARIANTE TEMPORÄR FESTHALTEN
                        materials_dummy.append(int_id_temp_1[(indices_5_temp[i][0] + var)])

                    elif len(indices_5_temp[i]) == 1:
                        materials_dummy.append(int_id_temp_1[(indices_5_temp[i][0])])

                    else:
                        pass

                    # MENGE ZUR VARIANTE FESTHALTEN

                    if int_dpt_temp_1[(indices_5_temp[i][-1] + 1)] == 6:
                        amount_mat.append(value_temp_1[(indices_5_temp[i][-1] + 1)])

                    else:
                        pass
            else:
                materials_dummy.append([])
                amount_mat.append([])


            for i in range(0, len(materials_dummy)):
                d.append(materials_dummy[i])
                d.append(amount_mat[i])

                #print("222 " + "d= " + str(d) + " | amount_mat= " + str(amount_mat) + " | i= " + str(i))

            materials.append(d)
            #print("materials2: " + str(materials))
            d = []

    j_son_0 = []

    #Speichern der json-Datei :: 7/22 CHANGED RANGE from len(t_id) to len(t_id)-1 ....8/10 CHANGED RANGE from len(t_id)-1 to len(t_id)-4
    for i in range(0,len(t_id)-4):
        j_son_0.append({"t_id": t_id[i],"machines": [machines[i]], "duration":[durations[i]], "material":materials[i]})
    #print("FÜR EINZELNE ORDER: " + str(j_son_0))

    #print("INSGESAMT: ")
    j_son_1.append({"o_id":n[0],"tasks":j_son_0})

j_son.append({"orders":j_son_1})
print(j_son)

Dateiname = "Input_File_Bike_Production.json"
with open(Dateiname, "w") as write_file:
   json.dump(j_son, write_file, indent=4, separators=(",", ": "))

