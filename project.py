import numpy as np
import math # Used only for rounding

def gatherUserInput():
    """
    Summary: Gathers user inputs.

    Inputs: NA

    Outputs:
        - variables: the number of variables
        - coefficients: the coefficients, or profits, of each variable
        - constraints: the constraints, or required resources, for each variable
        - constrainLimits: the total amount of each resource available.

    """
    # Get the number of variables
    while True:
        try:
            variables = int(input("How many variables are there? Or enter 0 to exit: "))
            if variables == 0:
                return 0,0,0,0
            if variables > 0:
                break
            print("Enter a positive integer.")
        except:
            print("Invalid inputs.")

    # Get the coefficients
    while True:
        try:    
            coefficients = input("What are the coefficients of each variable? Separate the coefficients by spaces (e.g.: 3000 2000 2000): ")
            coefficients = coefficients.split(" ")
            coefficients = [int(coefficients[n]) for n in range(len(coefficients))]
            if len(coefficients) != variables:
                print(f"Enter exactly {variables} coefficients.")
                continue
            break
        except:
            print("Invalid inputs.")

    # Get the constraints
    while True:
        try:
            constraints = input("Enter the constraints for each item in the square matrix. Separate each constraint by a space and each item by a comma (e.g.: 2 1 8,4 2 0,5 4 3): ")
            constraints = constraints.split(",")
            for i in range(len(constraints)):
                constraints[i] = constraints[i].split(" ")
            break
        except:
            print("Invalid inputs.")

    # Get the constraint limits
    constraintLimits = input("Enter the constraint limits. Separate each value by a space (e.g.: 300 200 300): ")
    constraintLimits = constraintLimits.split(" ")

    return variables, coefficients, constraints, constraintLimits

def table(var, coef, const, limits):
    """
    Summary: Print a table that describes the variables, constraints, coefficients, and constraint limits.

    Input:
        - var (int): the number of variables
        - coef (array of int): the coefficients
        - const (array of arrays of strings): the constraints
        - limits (array of strings): the constraint limits

    Output: Prints a table to the terminal with headers, the constraints and coefficient of each variable, and the availability of the constraints.
    """
    availabilities = ["Availability"]
    for limit in limits:
        availabilities.append(f"    {limit}     ")

    variables = []
    rows = []
    for v in range(1, var+1): # Create a row for each variable with relevant info
        variables.append(f"Variable {v}")
        rows.append([f" Variable {v} ", f"     {"       ,       ".join(const[v-1])}      ", f"${coef[v-1]:.2f}"])
    
    headers = ["   Supply   "]
    for v in range(1, var+1):
        headers.append(f"Constraint {v}")
    headers.append("Profit")
    print(headers) # Print the header
    
    for row in rows:
        print(row) # Print a row for each variable
    
    print(availabilities) # Print the constraint limits

def singleVariable(profits, constraints, constraintLimits):
    """
    Summary: Determine the profit if only one variable is produced

    Inputs:
        - profits (array of int): the coefficients
        - constraints (array of arrays of strings): the constraints
        - constraintLimits (array of strings): the constraint limits

    Outputs:
        - profit (float): the profit that would result in the product being sold
        - limitingFactor (float): the number of units that would be sold
    """
    limitingFactor = float("inf")

    for i in range(len(constraints)):
        constraint_value = float(constraints[i])
        limit = float(constraintLimits[i]) / constraint_value if constraint_value != 0 else float("inf")

        if limit < limitingFactor:
            limitingFactor = limit

    limitingFactor = math.floor(limitingFactor)
    profit = float(profits) * limitingFactor

    return profit, limitingFactor

def balanced(constraints, constraintLimits):
    """
    Summary: Solves the linear equation system to determine the circumstance where a combination of the variables is sold to maximize profit.

    Inputs:
        - constraints (array of arrays of strings): the constraints
        - constraintLimits (array of strings): the constraint limits
    
    Outputs: The number of units of each variable needed to maximize profits for the balanced option.
    """
    A = np.array(constraints, dtype=float).T  # Transpose matrix and convert values to floats
    b = np.array(constraintLimits, dtype=float)
    x = np.linalg.inv(A).dot(b)
    units = []
    for n in x:
        units.append(math.floor(n))
    return units

def determineOption(options):
    """
    Summary: Determines which option is the most profitable out of either a single variable being sold or a combination of variables being sold.
    
    Inputs:
        - options (integer array): the value of selling all of one type of variable and the value of selling a mix of the variables
    
    Outputs:
        - A string naming whether tha balanced option or the single variable option is more profitable
        - A float stating the value of that option
    """
    best = 0
    index = None
    for i, option in enumerate(options):
        if option > best:
            best = option
            index = i
    if index == len(options)-1:
        return "BALANCED", options[index]
    else:
        return f"VARIABLE {index+1}", options[index]

def main():
    """
    Summary: Provides the functionality of the user interface and calls helper functions to determine the best option for maximizing profits in a linear equation system.
    
    Inputs: NA
    
    Outputs: A variety of print statements that create a table and inform the user of the value and number of units possible given the information the user provided about the linear equation system.
    """
    t = True
    while t:
        try:
            variables, coefficients, constraints, constraintLimits = gatherUserInput()
            if variables == 0:
                print("Thank you. Goodbye!")
                return False

            print('\n')
            table(variables, coefficients, constraints, constraintLimits)
            print('\n')

            options = []
            for v in range(variables):
                profit, units = singleVariable(coefficients[v], constraints[v], constraintLimits)
                print(f"If only Variable {v+1} was made, the profit would be ${profit:.2f}. It would produce {units} units.")
                options.append(profit)
            
            units = balanced(constraints, constraintLimits)
            balancedProfit = 0
            for i in range(len(units)):
                balancedProfit += units[i]*coefficients[i]
            options.append(balancedProfit)

            print(f"The balanced option would profit ${balancedProfit:.2f}. It would require:")
            for i in range(len(units)):
                print(f"  - {units[i]} units of Variable {i+1}")

            bestOption, price = determineOption(options)
            print('\n')
            print(f"The best option is the {bestOption} option that is worth ${price:.2f}.")
            print('\n')
            t = False
        except:
            print("Invalid inputs. Try again")

# ===============================================================================
main()



"""

How many variables are there? Or enter 0 to exit: 2
What are the coefficients of each variable? Separate the coefficients by spaces (e.g.: 3000 2000 2000): 50 40
Enter the constraints for each item in the square matrix. Separate each constraint by a space and each item by a comma (e.g.: 2 1 8,4 2 0,5 4 3): 1 2,1.5 1
Enter the constraint limits. Separate each value by a space (e.g.: 300 200 300): 750 1000


['   Supply   ', 'Constraint 1', 'Constraint 2', 'Profit']
[' Variable 1 ', '     1       ,       2      ', '$50.00']
[' Variable 2 ', '     1.5       ,       1      ', '$40.00']
['Availability', '    750     ', '    1000     ']


If only Variable 1 was made, the profit would be $25000.00. It would produce 500 units.
If only Variable 2 was made, the profit would be $20000.00. It would produce 500 units.
The balanced option would profit $28750.00. It would require:
  - 375 units of Variable 1
  - 250 units of Variable 2


The best option is the BALANCED option that is worth $28750.00.

"""