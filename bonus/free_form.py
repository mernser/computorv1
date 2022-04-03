from curses.ascii import isdigit
import collections
import sys
import re

# "4 + 4 * X = X + X^6 + 4"
# "4 * X^0 + 4 * X^1 = 1 * X^1 + 1 * X^6 - 4 * X^0"

# 4 * X -> 4 * X^1 done 
# 4     -> 4 * X^0 done
# X     -> 1 * X^1 done
# X^6   -> 1 * X^6 done

def main():
    if len(sys.argv) != 2:
        print("Please enter equation")
        exit()
    source = sys.argv[1]
    
    valid = []

    source = source.replace(' ', '')
    args = re.split("[-+=]",source)
    for i in args:
        if not i:
            continue
        if re.findall("\d+\*X\^\d+", i):
            valid.append(i)
        elif i == "0":
            valid.append("0")
        elif i.isdigit():
            valid.append(i + "*X^0")
        elif i == "X":
            valid.append("1*X^1")
        elif i.endswith("X"):
            valid.append(i + "^1")
        else:
            valid.append("1*" + i)
    

    final = []
    signs = re.findall("[\+\-\=]", source)
    start = 0
    
    if not source.startswith("-"):
        start = 1
        final.append(valid[0])
    if "=-" in source:
        signs[signs.index('=')] = '= -'
        signs.pop(signs.index('= -') + 1)
    for i, d in zip(signs, valid[start::]):
        final.append(i + " " + d)
    valid = " ".join(final)
    valid = valid.replace("*"," * ")
    print(valid)

if __name__ == '__main__':
    main()