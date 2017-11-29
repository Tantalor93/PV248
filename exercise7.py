import numpy

data = numpy.loadtxt('matrix.txt')
print("matrix: \n" + str(data))
print("determinant: " + str(numpy.linalg.det(data)))
print("inverse matrix: \n" + str(numpy.linalg.inv(data)))

print("--------------------------------------------------")

f = open('equation.txt', 'r', encoding='utf-8')
print('equations:')
for line in f:
    print(line, end='')