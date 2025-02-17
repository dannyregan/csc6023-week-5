import numpy as np

A = np.array([[2,4,5],[1,2,4],[8,0,3]])
b = np.array([300,200,300])
x = np.linalg.inv(A).dot(b)

def table(var, coef, const, limits):
    variables = []
    for v in range(1, var+1):
        variables.append(f"Variable {v}")
    print(variables)

def main():
    variables = int(input("How many variables are there? "))
    coefficients = input("What are the coefficients of each variable? Separate the coefficients by spaces (e.g.: 3000 2000 3000): ")
    constraints = input("Enter the constraints for each item in the square matrix. Separate each constraint by a space and each item by a comma (e.g.: 2 1 8,4 2 0,5 4 3): ")
    constraintLimits = input("Enter the constraint limits. Separate each value by a space (e.g.: 300 200 300): ")
    print(table(variables, coefficients, constraints, constraintLimits))

main()
# print(x)