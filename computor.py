from curses.ascii import isdigit
import collections
import sys
import re

import matplotlib.pyplot as plt
import numpy as np

class Poly:
    def __init__(self, equation):
        self.power = {}
        self.source = equation
        self.left = ""
        self.right = ""
        self.left_args = []
        self.right_args = []
        self.power_left = []
        self.power_right = []
        self.poly_degree = None

def change_sign(lst):
    return [-i for i in lst]


def main():
    plot = 0
    step = 0
    if len(sys.argv) == 1 or len(sys.argv) > 3:
        print("Please enter equation and/or one of following modes: plot, step")
        exit()
    elif len(sys.argv) == 3:
        if sys.argv[2] == "plot":
            plot = 1
        elif sys.argv[2] == "step":
            step = 1
        else:
            print("Incorrect mode name, proceeding with default behavior")


    # part 1 cutting spaces
    eq = Poly(sys.argv[1].replace(' ', ''))

    # part 2 splitting into left / right side (sign '=' disspaears)
    eq.left, eq.right = eq.source.split('=')
    if (step):
        print("\033[92mSplitting into left / right side (sign '=' dissapears):\033[0m")
        print(eq.left, eq.right)

    # part 3 fixing signs of first numbers (simplify sign processing)
    if not eq.right.startswith('-'):
        eq.right = "+" + eq.right
    if not eq.left.startswith('-'):
        eq.left = "+" + eq.left


    # part 4 parsing args to lists
    eq.left_args = re.findall("(\-?\d+(?:\.\d+)?)\*", eq.left)
    eq.right_args = re.findall("(\-?\d+(?:\.\d+)?)\*", eq.right)

    eq.left_args = list(map(float, eq.left_args))
    eq.right_args = list(map(float, eq.right_args))
    if (step):
        print ("\033[92mArguments of the equation:\033[0m")
        print (eq.left_args, eq.right_args)
    
    # part 5 changing signs of right side
    eq.right_args = change_sign(eq.right_args)

    if (step):
        print ("\033[92mChanging signs of right side:\033[0m")
        print (eq.left_args, eq.right_args)

    # part 6 finding powers of X and finding Polynomial Degree
    # (?<=123-)((apple|banana)(?=-456)|(?=456))
    
    eq.power_left = re.findall("(?<=X\^)\d", eq.left)
    eq.power_right = re.findall("(?<=X\^)\d", eq.right)
    if (step):
        print ("\033[92mPowers of X\033[0m")
        print (eq.power_left, eq.power_right)


    # part 7 grouping args according to their powers
    for i, d in zip(eq.power_left, eq.left_args):
        if i not in eq.power:
            eq.power[i] = []
            eq.power[i].append(d)
        else:
            eq.power[i].append(d)
    for i, d in zip(eq.power_right, eq.right_args):
        if i not in eq.power:
            eq.power[i] = []
            eq.power[i].append(d)
        else:
            eq.power[i].append(d)
    
    if (step):
        print ("\033[92mGrouped args according to their powers\033[0m")
        print (eq.power)

    # part 8 summing every args for reduced form
    for i in eq.power:
        eq.power[i] = sum(eq.power[i])
    if (step):
        print ("\033[92mSumming every args for reduced form\033[0m")
        print (eq.power)

    # part 9 downgrading floats to int where its possible
    for i in eq.power:
        if eq.power[i].is_integer():
            eq.power[i] = int(eq.power[i])
    if (step):
        print ("\033[92mDowngrading floats to int where its possible\033[0m")
        print (eq.power)

    # part 10 printing reduced form, also sorting dict by keys:

    eq.power = dict(collections.OrderedDict(sorted(eq.power.items())))
    if (step):
        print ("\033[92mSorting dict with powers\033[0m")
        print (dict(eq.power.items()))
    
    print("Reduced form: ", end='')
    for i in eq.power:
        if eq.power[i] < 0:
            print("-", str(eq.power[i]).replace('-', ''), end = '')
        else:
            if i == min(eq.power.items())[0]:
                print(str(eq.power[i]).replace('+', ''), end = '')
            else:
                print("+", str(eq.power[i]).replace('+', ''), end = '')
        print(" *", "X^" + str(i), end =' ', sep=' ')
    if not eq.power:
        print("0")
    print("= 0")

    # part 10.5 checking if powers has 0 coefecient (must be removed) ex. 0 * X^2
    zero_coef_power = []
    for i in eq.power:
        if not eq.power[i]:
            zero_coef_power.append(i)
    
    for i in zero_coef_power:
        del eq.power[i]
    
    if not eq.power:
        print ("Each real numbers is a solution.")
        exit()
    eq.poly_degree = max(eq.power)
    
    # zaglushka hehehe
    if "0" not in eq.power:
        eq.power["0"] = 0
    if "1" not in eq.power:
        eq.power["1"] = 0
    if "2" not in eq.power:
        eq.power["2"] = 0

    # part 11 validation polynonomial degree
    if int(eq.poly_degree) > 2:
        print ("The polynomial degree is strictly greater than 2, I can't solve.")
        exit(0)
    else:
        print ("Polynomial Degree:", eq.poly_degree)

    # part 12 calculating solution

    # ax^2 + bx + с = 0
    # D = b^2 - 4 * a * c
    # x = (-b +- D^2)/2a

    discriminant = None
    root_one = None
    root_two = None

    if eq.poly_degree == "2":
        discriminant = eq.power["1"] ** 2 - 4 * eq.power["2"] * eq.power["0"]
        if (step):
            print("Discriminant is:", discriminant)
        if discriminant > 0:
            root_one = (-1 * eq.power["1"] + discriminant ** 0.5) / (2 * eq.power["2"])
            root_two = (-1 * eq.power["1"] - discriminant ** 0.5) / (2 * eq.power["2"])
            print ("Discriminant is strictly positive, the two solutions are:", root_one, root_two, sep = '\n')
        elif discriminant < 0:
            root_one = (-1 * eq.power["1"] + discriminant ** 0.5) / (2 * eq.power["2"])
            root_two = (-1 * eq.power["1"] - discriminant ** 0.5) / (2 * eq.power["2"])
            print("The discriminant is strictly negative, the two solutions are:",
             str(root_one).replace(')', '').replace('(', ""), str(root_two).replace(')', '').replace('(', ""), sep = '\n')
            exit()
        else:
            root_one = (-1 * eq.power["1"]) / (2 * eq.power["2"])
            print ("The discriminant is zero, the solution is:", root_one)
    elif eq.poly_degree == "1":
        root_one = -1 * eq.power["0"] / eq.power["1"]
        print ("The solution is:", root_one)
    else:
        if "0" in eq.power and eq.power["0"] == 0:
            print ("Each real numbers is a solution.")
            exit()
        else:
            print ("There is no solution.")
            exit()

    if plot:
        x = np.arange(-100, 100, 0.1)
        y = eq.power["2"] * x ** 2 + eq.power["1"] * x + eq.power["0"]
        plt.grid(True, which='both')
        plt.axhline(y=0, color='k')
        plt.axvline(x=0, color='k')
        plt.plot(x,y)
        plt.show()

if __name__ == '__main__':
    main()