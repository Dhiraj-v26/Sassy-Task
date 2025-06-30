def calculate(num1,num2,opr):
    if opr == "+":
        return num1+num2
    elif opr == "-":
        return num1-num2
    elif opr == "*":
        return num1*num2
    else:
        if num2 != 0:
            return num1/num2
        else:
            print("ZERO DIVISION ERROR"),400
