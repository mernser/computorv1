import random
import math
import sys

def main():
    if len(sys.argv) != 2:
        print("Please enter number of arguments! (from 2 to 20)")
        exit()

    args_num = sys.argv[1]
    if not args_num.isdigit:
        print("not a number!")
        exit(1)
    args_num = int(args_num)
    if not 2 <= args_num <= 20:
        exit(1)
    
    max_power = 2
    min_power = 0
    valid = True
    eq = []
    for _ in range(args_num):
        eq.append(str(random.randint(0, 10)) + " * X^" + str(random.randint(min_power, max_power)))
    signs = ["+", "-"]
    final = []
    for d, z in zip(eq, range(args_num)):
        i = str(signs[random.randint(0, 1)])
        final.append(i + " " + d)
    eq_sign_pos = random.randint(1, round(args_num / 2))
    final.insert(eq_sign_pos, "=")
    final[eq_sign_pos + 1] = final[eq_sign_pos + 1].replace('+ ','')
    final[0] = final[0].replace('+ ','')
    
    final = " ".join(final)
    print("\"" + final + "\"")

if __name__ == '__main__':
    main()