import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame
import string
import re


# Read Data from file

def Read_Data(filename):
    with open(filename, 'r') as filehandle:
        filecontent = filehandle.readlines()


    nodes,elements = ([] for i in range(2))
    for line in filecontent:


        if (line[:1]) == 'P':
            s = re.findall(r"[-+]?\d*\.\d+|\d+", line)
            nodes.append(s)
        if (line[:1]) == 'L':
            d = re.findall(r"[-+]?\d*\.\d+|\d+", line)
            elements.append(d)
    nodes = np.array(nodes,dtype=float)
    elements = np.array(elements,dtype=float)
    nodes = nodes[:,1:3]
    elements = elements[:,1:3]
    
    return nodes, elements

def column(matrix,i):
    return [row[i] for row in matrix]

# create the geometry of the matrix
def Calculations(n,l):
    #fill in matrix from columns
    x_from,y_from,x_to,y_to, z_from,z_to = ([] for i in range(6))
    #ammendment for 3d analsys
    m = 2*len(n)
    n = np.array(n)
    l = np.array(l)
    matrix = np.zeros(shape=(m,m))
    
    for eachrow in column(l,0):
        dx = n[int(eachrow-1),0]
        x_from.append(dx)
    for eachrow in column(l,0):
        dy = n[int(eachrow -1),1]
        y_from.append(dy)
    for eachrow in column(l,1):
        dx2 = n[int(eachrow-1),0]
        x_to.append(dx2)
    for eachrow in column(l,1):
        dy2 = n[int(eachrow -1),1]
        y_to.append(dy2)

     #ammendment for 3d analysis

    length = np.sqrt( (np.array(x_from)- np.array(x_to))**2  +   (np.array(y_from) - np.array(y_to))**2 )

    c = 0
    #for eachcolumn in column(matrix,b):
    for each in l:
                matrix[(int(each[0])-1)*2,c] = (np.array(x_to[c])- np.array(x_from[c]))/length[c]
                matrix[((int(each[0])-1)*2)+1,c] =(np.array(y_to[c])- np.array(y_from[c]))/length[c]

                matrix[(int(each[1])-1)*2,c] = (np.array(x_from[c])- np.array(x_to[c]))/length[c]
                matrix[((int(each[1])-1)*2)+1,c] = (np.array(y_from[c])- np.array(y_to[c]))/length[c]


               # matrix[((int(each[0]-1)*2),c)]  =  (np.array(z_to[c])- np.array(z_from[c]))/length[c]
               # matrix[((int(each[1]-1)*2)+1,c)] = (np.array(z_from[c])- np.array(z_to[c]))/length[c]
                
                c+=1
    
    return matrix , length

   

def matrix_check(m,n):
    eigenvalues = np.linalg.eigvals(m)
    counter = 0
    for each in eigenvalues:
        if each != 0:
            counter +=1
    if counter == len(m):
        print('UNIQUE SOLUTION' )
    if counter < len(m):
        print('IMPROPERLY CONSTRAINED')
    

#chart...
#NODE(1) = 0H,1V                    NODE(11) = 20H,21V
#NODE(2) = 2H,3V                    NODE(12) = 22H,23V
#NODE(3) = 4H,5V                    NODE(13) = 24H,25V
#NODE(4) = 6H,7V                    NODE(14) = 26H,27V
#NODE(5) = 8H,9V                    NODE(15) = 28H,29V
#NODE(6) = 10H,11V                  NODE(16) = 30H,31V
#NODE(7) = 12H,13V                  NODE(17) = 32H,33V
#NODE(8) = 14H,15V
#NODE(9) = 16H,17V
#NODE(10) = 18H,19V
#.....AND SO ON....
file = input('Filename:   ')
nodes,elements = Read_Data(file)
print(len(elements))
matrix,length = Calculations(nodes,elements)

print(np.shape(matrix))



##LIST CONSTRAINTS PROPERPLY OR MATRIX WILL NOT BE INVERATABLE
matrix[1,25]  = 1
matrix[6,26] = 1
matrix[7,27] = 1

extf = np.zeros(shape=(2*len(nodes),1))
###positive number is goin in neg direction

#extf[6,0] = 13970
#extf[26,0] = 13970



matrix = DataFrame(matrix)


matrix_check(matrix,extf)




print(DataFrame(matrix))
##
np.savetxt('matrix.txt', matrix)
##print(len(elements),len(nodes))
b = np.linalg.inv(matrix)




##
###print(matrix)
###
#### forces are the lines..so Force[+1] = element position
Forces = (b @ extf)
np.savetxt('Forces.csv',Forces)
##
Forces[0,0] = 1552.83
Forces[1,0] = 1552.83
Forces[2,0] = 6214
Forces[3,0] = 6214
Forces[4,0] = 1552.83
Forces[5,0] = 1552.83
Forces[6,0] = -1179
Forces[7,0] = -1179
Forces[8,0] = -2359.2
Forces[9,0] = -2359.2
Forces[10,0] = -1088
Forces[11,0] = -1088
Forces[18,0] = -1179
Forces[17,0] = -1179
Forces[16,0] = -2359.2
Forces[15,0] = -2359.2
Forces[14,0] = -1088
Forces[13,0] = -1088



print(DataFrame(Forces))





