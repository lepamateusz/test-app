from flask import Flask, request
from flask_restful import Resource, Api
import json, re


app = Flask(__name__)
api = Api(app)

def validation(expression):
    
    if isinstance(expression, str) != True:
        raise Exception("Only strings!")
    elif len(expression) == 0:
        raise Exception("Not empty string!")
    elif bool(re.search(r'[^0-9+-/(/)/*//]',expression)):
        raise Exception("Without illegal characters!")
    else:
        pass

def standardExpr(expression):
    expression.replace(" ", "")
    pattern = r'([+-///*/(/)]|\d+)'
    return re.sub(pattern, r' \1', expression)
    
def changeToPostfix(expression):
    
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
    if sign == "*": return num1 * num2
    elif sign == "/": return num1 / num2
    elif sign == "+": return num1 + num2
    else: return num1 - num2

class Welcome(Resource):
    def get(self):
        return("Welcome to Parallel calculator Usage:")


class Evaluate(Resource):
        
    def get(self, num):
        return {"result" : num*10}

    def post(self):
        some_json = request.get_json()
        expression = some_json['expression']
        validation(expression)
                    
        result = standardExpr(expression)
        result = changeToPostfix(result)
        result = postfixEvaluation(result)
        return {"result": result }
    
api.add_resource(Welcome, '/')
api.add_resource(Evaluate, '/evaluate')

usage = """

Wrong endpoint!

Avaliable endpoints:

POST /evaluate
GET /welcome

"""

@app.errorhandler(404)
def invalud_route(e):
    return usage

if __name__ == '__main__':
    app.run(debug=True)
