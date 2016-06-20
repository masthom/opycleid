# -*- coding: utf-8 -*-

################################################
###### Copyright (c) 2016, Alexandre Popoff 
###

import numpy as np

################################################
###### GENERIC CLASS FOR MONOID ACTION
###

class MonoidAction:
    def __init__(self):
        self.objects = {}
        self.generators = {}
        self.operations = {}
        self.SIMPLY_TRANSITIVE=None

	############
	###### TRANSFORMATIONAL MUSIC THEORY METHODS

    def apply_operation(self,operation_name,element_name):
        idx_element = self.objects[element_name]
        op = self.operations[operation_name]
        list_indices = np.where(op[:,idx_element])[0]
        return [x for x in self.objects.keys() for y in list_indices if self.objects[x]==y]

    def get_operation(self,elem_1,elem_2):
        idx_1 = self.objects[elem_1]
        idx_2 = self.objects[elem_2]

        return [op for op in self.operations if self.operations[op][idx_2,idx_1] ]

	############
	###### MONOID STRUCTURE

    def add_generator(self,gen_name,gen_matrix):
        self.generators[gen_name] = gen_matrix

    def mult(self,op_2,op_1):
        m = (self.operations[op_2].dot(self.operations[op_1])>0)
        for x in self.operations:
            if np.array_equal(m,self.operations[x]):
                return x

    def generate_monoid(self):
        self.operations = self.generators
        self.operations["e"] = np.eye(len(self.objects),dtype=bool)
        new_liste = self.generators
        added_liste = self.generators

        while(len(added_liste)>0):
            added_liste = {}
            for name_x in new_liste.keys():
                for name_g in self.generators.keys():
                    elem_name = name_g+name_x
                    elem_matrix = (self.generators[name_g].dot(new_liste[name_x])>0)
                    c=0
                    for name_y in self.operations.keys():
                        if np.array_equal(self.operations[name_y],elem_matrix):
                            c=1
                    if c==0:
                        added_liste[elem_name] = elem_matrix
                        self.operations[elem_name] = elem_matrix
            new_liste = added_liste


	############
	###### ALGEBRAIC STRUCTURE AND GREEN'S RELATIONS

    def is_leftIdeal(self,S):
        for m in S.keys():
            for f in self.operations.keys():
                t = self.mult(f,m)
                if not t in S:
                    return False
        return True
	
    def element_Rclass(self,op_name):
        list_Req = []
        I1 = np.unique([self.mult(op_name,x) for x in self.operations.keys()])
        for op in self.operations.keys():
            I2 = np.unique([self.mult(op,x) for x in self.operations.keys()])
            if sorted(I2) == sorted(I1):
                list_Req.append(op)
        return list_Req

    def element_Lclass(self,op_name):
        list_Req = []
        I1 = np.unique([self.mult(x,op_name) for x in self.operations.keys()])
        for op in self.operations.keys():
            I2 = np.unique([self.mult(x,op) for x in self.operations.keys()])
            if sorted(I2) == sorted(I1):
                list_Req.append(op)
        return list_Req

    def get_Rclasses(self):
        list_op = self.operations.keys()
        R_classes = []
        for x in list_op:
            R_class = self.element_Rclass(x)
            R_classes.append(R_class)
            for y in R_class:
                list_op.remove(y)
        return R_classes

    def get_Lclasses(self):
        list_op = self.operations.keys()
        L_classes = []
        for x in list_op:
            L_class = self.element_Lclass(x)
            L_classes.append(L_class)
            for y in L_class:
                list_op.remove(y)
        return L_classes


################################################
###### NOLL MONOID
###

class Noll_Monoid(MonoidAction):
    def __init__(self):
        self.objects = {"C":0,"Cs":1,"D":2,"Eb":3,"E":4,"F":5,"Fs":6,"G":7,"Gs":8,"A":9,"Bb":10,"B":11}

        F = np.zeros((12,12),dtype=bool)
        for i in range(12):
            F[(3*i+7)%12,i] = True

        G = np.zeros((12,12),dtype=bool)
        for i in range(12):
            G[(8*i+4)%12,i] = True
        
        self.generators = {"f":F,"g":G}
        self.generate_monoid()


################################################
###### TI GROUP FOR PITCH CLASSES
###

class TI_Group_PC(MonoidAction):
    def __init__(self):
        self.objects = {"C":0,"Cs":1,"D":2,"Eb":3,"E":4,"F":5,"Fs":6,"G":7,"Gs":8,"A":9,"Bb":10,"B":11}
        self.SIMPLY_TRANSITIVE=False

        T = np.zeros((12,12),dtype=bool)
        for i in range(12):
                T[(i+1)%12,i]=True

        I = np.zeros((12,12),dtype=bool)
        for i in range(12):
                I[(-i)%12,i]=True
        
        self.generators = {"T":T,"I^0":I}
        self.operations = {"e":np.eye(12,dtype=bool),"I^0":I}
        for i in range(1,12):
                x = self.operations['e']
                for j in range(i):
                        x = x.dot(T)
                self.operations["T^"+str(i)] = x
                self.operations["I^"+str(i)] = x.dot(I)


################################################
###### TI GROUP FOR TRIADS
###

class TI_Group_Triads(MonoidAction):
    def __init__(self):
        self.objects = {"C":0,"Cs":1,"D":2,"Eb":3,"E":4,"F":5,"Fs":6,"G":7,"Gs":8,"A":9,"Bb":10,"B":11,
                                        "c":12,"cs":13,"d":14,"eb":15,"e":16,"f":17,"fs":18,"g":19,"gs":20,"a":21,"bb":22,"b":23}
        self.SIMPLY_TRANSITIVE=True

        T = np.zeros((24,24),dtype=bool)
        for i in range(12):
                T[(i+1)%12,i]=True
                T[12+(i+1)%12,i+12]=True

        I = np.zeros((24,24),dtype=bool)
        for i in range(12):
                I[(5-i)%12 + 12,i]=True
                I[(5-i)%12, i+12]=True
        
        self.generators = {"T":T,"I^0":I}
        self.operations = {"e":np.eye(24,dtype=bool),"I^0":I}
        for i in range(1,12):
                x = self.operations['e']
                for j in range(i):
                        x = x.dot(T)
                self.operations["T^"+str(i)] = x
                self.operations["I^"+str(i)] = x.dot(I)

################################################
###### PRL GROUP
###

class PRL_Group(MonoidAction):
    def __init__(self):
        self.objects = {"C":0,"Cs":1,"D":2,"Eb":3,"E":4,"F":5,"Fs":6,"G":7,"Gs":8,"A":9,"Bb":10,"B":11,
                                        "c":12,"cs":13,"d":14,"eb":15,"e":16,"f":17,"fs":18,"g":19,"gs":20,"a":21,"bb":22,"b":23}
        self.SIMPLY_TRANSITIVE=True

        L = np.zeros((24,24),dtype=bool)
        for i in range(12):
                L[(i+4)%12 + 12,i]=True
                L[(i+8)%12,12+i]=True

        R = np.zeros((24,24),dtype=bool)
        for i in range(12):
                R[(i+9)%12 + 12,i]=True
                R[(i+3)%12,12+i]=True
        
        self.generators = {"L":L,"R":R}
        self.operations = {"e":np.eye(24,dtype=bool),"R":R}
        RL = R.dot(L)
        for i in range(1,12):
                x = self.operations['e']
                for j in range(i):
                        x = x.dot(RL)
                self.operations["(RL)^"+str(i)] = x
                self.operations["(RL)^"+str(i)+"R"] = x.dot(R)

################################################
###### LEFT Z3Q8 GROUP FOR TRIADS
###

class Left_Z3Q8_Group(MonoidAction):
    def __init__(self):
        self.objects = {"C":0,"Cs":1,"D":2,"Eb":3,"E":4,"F":5,"Fs":6,"G":7,"Gs":8,"A":9,"Bb":10,"B":11,
                                        "c":12,"cs":13,"d":14,"eb":15,"e":16,"f":17,"fs":18,"g":19,"gs":20,"a":21,"bb":22,"b":23}
        self.SIMPLY_TRANSITIVE=True

        T = np.zeros((24,24),dtype=bool)
        for i in range(12):
                T[(i+1)%12,i]=True
                T[12+(i+1)%12,i+12]=True

        J = np.zeros((24,24),dtype=bool)
        for i in range(12):
                J[(-i)%12 + 12,i]=True
                J[(-i+6)%12, i+12]=True
        
        self.generators = {"T":T,"J^0":J}
        self.operations = {"e":np.eye(24,dtype=bool),"J^0":J}
        for i in range(1,12):
                x = self.operations['e']
                for j in range(i):
                        x = x.dot(T)
                self.operations["T^"+str(i)] = x
                self.operations["J^"+str(i)] = x.dot(J)

################################################
###### RIGHT Z3Q8 GROUP FOR TRIADS
###

class Right_Z3Q8_Group(MonoidAction):
    def __init__(self):
        self.objects = {"C":0,"Cs":1,"D":2,"Eb":3,"E":4,"F":5,"Fs":6,"G":7,"Gs":8,"A":9,"Bb":10,"B":11,
                                        "c":12,"cs":13,"d":14,"eb":15,"e":16,"f":17,"fs":18,"g":19,"gs":20,"a":21,"bb":22,"b":23}
        self.SIMPLY_TRANSITIVE=True

        T = np.zeros((24,24),dtype=bool)
        for i in range(12):
                T[(i+1)%12,i]=True
                T[12+(i-1)%12,i+12]=True

        J = np.zeros((24,24),dtype=bool)
        for i in range(12):
                J[i + 12,i]=True
                J[(i+6)%12, i+12]=True
        
        self.generators = {"T":T,"J^0":J}
        self.operations = {"e":np.eye(24,dtype=bool),"J^0":J}
        for i in range(1,12):
                x = self.operations['e']
                for j in range(i):
                        x = x.dot(T)
                self.operations["T^"+str(i)] = x
                self.operations["J^"+str(i)] = x.dot(J)