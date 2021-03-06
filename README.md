# Parallel Calculator

Tha app is an implementation of a calculator that evaluates given mathematical expression in parallel.

The microservice:
* is implemented in Python
* handle the input via HTTP and respond with suitable answer
* supports only operations: +,-,/,*,(,)

# Requirements

* python == 3.7
* Flask == 1.1.1
* Flask-RESTful == 0.3.8

# Start

How to starts microservice

```
$flask app.py
```

# About usage

In order to use calculator use POST method on appropriate endpoint. By default it should be:
```
http://localhost:5000/evaluate
```
The app allows to use only POST metod on /evaluate. Other endpoints or method are not allowed!

To use the calculator pass in POST method appropriate arguments. Post field "expression" equal to mathematical equation you want to solve (only as a string), for instance:
```
-d ' {"expression":"(1-1)*2+3*(5+4)+5/2"} '
```
Bare in mind that only numbers and signs: 
* "+",
* "-",
* "/",
* "*",
* "(",
* ")" 

are allowed.


# Example usage

input:
```
$curl -H " Content-Type: application/json " -X POST -d ' {"expression":"(1-1)*2+3*(1-3+4)+10/2"} ' http://localhost:5000/evaluate
```
respond:
```
{ "result" : 11 }
```

