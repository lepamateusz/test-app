from flask import Flask, request
from flask_restful import Resource, Api
import json, re


def validation(expression):
    """Basic validation of user input"""  

    if isinstance(expression, str) != True:
        raise Exception("Only <string> is allowed as an input !")
    elif len(expression) == 0:
        raise Exception("Empty string is not a valid input!")
    elif bool(re.search(r'[^0-9+-/(/)/*//\s]',expression)):
        raise Exception("Some of characters are invalid! Please use only numbers or '+','-','/','*','(',')'")
    else:
        pass

def standardExpr(expression):
    """Standarisation of input that add space before number or sign """
    
    expression.replace(" ", "")
    pattern = r'([+-///*/(/)]|\d+)'
    return re.sub(pattern, r' \1', expression)
    
def changeToPostfix(expression):
    """Changing infix expression into postfix expression"""
    
    level = {'*': 3, '/': 3, '+': 2, '-': 2, '(': 1}
    stack = []
    postList = []
    tokenList = expression.split()

    for token in tokenList:
        if token.isnumeric():
            postList.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            topToken = stack.pop()
            while topToken != '(':
                postList.append(topToken)
                topToken = stack.pop()
        else:
            while (len(stack) != 0) and (level[stack[-1]] >= level[token]):
                  postList.append(stack.pop())
            stack.append(token)

    while len(stack) != 0:
        postList.append(stack.pop())
    return " ".join(postList)


def postfixEvaluation(expression):
    """Evaluation of postfix expression"""
    
    stack = []
    tokenList = expression.split()

    for token in tokenList:
        if token.isnumeric():
            stack.append(int(token))
        else:
            number2 = stack.pop()
            number1 = stack.pop()
            result = evaluation(token,number1,number2)
            stack.append(result)
    return stack.pop()

def evaluation(sign, num1, num2):
    """Execute operation based on sign"""
    
    if sign == "*": return num1 * num2
    elif sign == "/": return num1 / num2
    elif sign == "+": return num1 + num2
    else: return num1 - num2

class Evaluate(Resource):
    """Class which carry out main task of microservice"""
        
    def post(self):
        some_json = request.get_json()
        expression = some_json['expression']
        validation(expression)
        
        
        standResult = standardExpr(expression)
        postfixResult = changeToPostfix(standResult)
        result = postfixEvaluation(postfixResult)
            
        return {"result": result }

app = Flask(__name__)
api = Api(app)

api.add_resource(Evaluate, '/evaluate')

usage = """

###Usage instruction###

You can curl respond only by:

POST -d '{"expression":"<expression>"}'  http://localhost:5000/evaluate

Usage example:
$ curl -H "Content-Type: application/json" -X POST -d '{"expression":"(1+1)*3-5*(4/5)"}'  http://localhost:5000/evaluate

"""

@app.errorhandler(404)
def invalud_route(e):
    return usage

if __name__ == '__main__':
    app.run(debug=True)
