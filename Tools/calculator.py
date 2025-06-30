from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/calc', methods=['GET', 'POST'])
def calc():
    if request.method == 'POST':
        num1 = int(request.form.get('num1'))
        num2 = int(request.form.get('num2'))
        operator = request.form.get('operator')

        # if num1.strip() == '' or num2.strip() == '':
        #     return "<h1>Invalid number. Please enter a number.</h1>"
        
        if operator == "+":
            ans = num1 + num2
        elif operator == "-":
            ans = num1 - num2
        elif operator == "*":
            ans = num1*num2
        else:
            if num2 != 0:
                ans = num1 / num2
            else:
                raise ZeroDivisionError
        
        
        return {"ans":ans}
    else:
        return render_template('calc.html')
    
    
    
if __name__ == '__main__':
    app.run()

# def add(num1, num2):
#     return num1 + num2

# def sub(num1,num2):
#     return num1 - num2

# def mul(num1, num2):
#     return num1*num2

# def div(num1, num2):
#     return num1/num2