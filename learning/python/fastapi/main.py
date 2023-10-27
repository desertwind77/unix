#!/usr/bin/env python3

from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import ( FastAPI, Path, Query, Body,
                      Request, Form, File, UploadFile,
                      Cookie, Header, WebSocket )
from pydantic import BaseModel, Field
from typing import List, Optional, Tuple
import datetime
import shutil
import uvicorn

app = FastAPI()

class Student( BaseModel ):
    id: int
    name: str = Field( None, title="The description of the item",
                       max_length=10 )
    subjects: List[str] = []

# GET       Sends data in unencrypted form to the server. Most common method.
# HEAD      Same as GET, but without the response body.
# POST      Used to send HTML form data to the server. Data received by the POST
#           method is not cached by the server.
# PUT       Replaces all current representations of the target resource with
#           the uploaded content.
# DELETE    Removes all current representations of the target resource given by a URL.
@app.get("/")
async def index():
    # We can return an Python object whih will be converted to JSON.
    return {"message": "Hello World"}

# Path parameter
# curl http://127.0.0.1:8000/hello1/ink/13
@app.get( "/hello1/{name}/{age}")
async def hello1( name, age ):
    return {"name": name, "age": age}

# Query paremeter : string after ? is the query
# which is a list of key-value pairs concatenated by &
# curl "http://127.0.0.1:8000/hello2?name=ink&age=20"
@app.get( "/hello2")
async def hello2( name : str, age : int ):
    return {"name": name, "age": age}

# curl "http://127.0.0.1:8000/hello3/ink?age=20"
@app.get( "/hello3/{name}")
async def hello3( name : str, age : int ):
    return {"name": name, "age": age}

# Parameter validation using Path and query validation using Query
# curl "http://127.0.0.1:8000/hello4/ink/20?percent=0"
@app.get( "/hello4/{name}/{age}")
async def hello4( *,
                  name : str = Path( ..., min_length=3, max_length=10 ),
                  age : int = Path( ..., ge=1, le=100 ),
                  percent : float = Query( ..., ge=0, le=100 ) ):
    return {"name": name, "age": age, "percent" : percent}

# Because of the post method, it receives an object of Student class as Body
# parameter from the client’s request.
#
# curl -X 'POST' 'http://127.0.0.1:8000/student/' -H 'accept: application/json'
#      -H 'Content-Type: application/json'
#      -d '{"id": 10,"name": "Athichart","subjects": [ "math", "Science" ]}'
# {"id":10,"name":"Athichart","subjects":["math","Science"]}
@app.post('/student1/')
async def student_data1( s1: Student ):
    return s1

# Use singular values to add attributes to it.
#
# curl -X 'POST' 'http://127.0.0.1:8000/student2'
#      -H 'accept: application/json'
#      -H 'Content-Type: application/json'
#      -d '{
#      "name": "string",
#      "marks": 0
#      }'
@app.post("/student2")
async def student_data2( name : str=Body(...), marks : int=Body(...) ):
    return {"name":name,"marks": marks}

# Declare an operation function to have path and/or query parameters along with
# request body
#
# curl -X 'POST' 'http://127.0.0.1:8000/student3/penn%20state?age=30'
#      -H 'accept: application/json'
#      -H 'Content-Type: application/json'
#      -d '{
#      "id": 17,
#      "name": "Athichart",
#      "subjects": [ "Math", "Science" ]
#      }'
@app.post("/student3/{college}")
async def student_data3( college : str, age : int, student:Student ):
    retval={"college":college, "age":age, **student.dict()}
    return retval

@app.get("/helloworld/")
async def hello_world():
    ret = '''
<html>
<body>
<h2>Hello World!</h2>
</body>
</html
'''
    return HTMLResponse( content=ret )

# Using Jinja to generate response from a template
# {% %} – Statements
# {{ }} – Expressions to print to the template output
# {# #} − Comments which are not included in the template output
# # # # − Line statements
#
# Need to install aiofiles to return static files
#
# pip3 install aiofiles
templates = Jinja2Templates( directory="templates" )
app.mount( "/static", StaticFiles( directory="static" ), name="static" )
@app.get("/helloworld2/{name}", response_class=HTMLResponse )
async def hello_world2( request : Request, name : str ):
    return templates.TemplateResponse( "hello.html", { "request": request, "name": name } )

# HTML Form templates
@app.get("/login/", response_class=HTMLResponse)
async def login( request: Request ):
   return templates.TemplateResponse( "login.html", {"request": request} )

# FastAPI has a Form class to process the data received as a request by
# submitting an HTML form. However, you need to install the python-multipart
# module. It is a streaming multipart form parser for Python.
#
# pip3 install python-multipart

class User( BaseModel ):
    username : str
    password : str

@app.post("/submit/")
async def submit( nm: str = Form(...), pwd: str = Form(...) ):
    # return {"username": nm}
    # Populate and return Pydantic model with HTML form data
    return User( username=nm, password=pwd )

# Send a file to the server you need to use the HTML form’s enctype as
# multipart/form-data, and use the input type as the file to render a button,
# which when clicked allows you to select a file from the file system.
@app.get("/upload/", response_class=HTMLResponse)
async def upload( request: Request ):
    return templates.TemplateResponse("uploadfile.html", {"request": request})

@app.post("/uploader/")
async def create_upload_file(file: UploadFile = File(...)):
    with open("destination.png", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename}

# A cookie is one of the HTTP headers. The web server sends a response to the
# client, in addition to the data requested, it also inserts one or more
# cookies. A cookie is a very small amount of data, that is stored in the
# client’s machine. On subsequent connection requests from the same client,
# this cookie data is also attached along with the HTTP requests.
#
# The cookies are useful for recording information about client’s browsing.
# Cookies are a reliable method of retrieving stateful information in otherwise
# stateless communication by HTTP protocol.
@app.post("/cookie/")
def create_cookie():
    content = {"message": "cookie set"}
    response = JSONResponse(content=content)
    # The cookie parameter is set on the response object with the help of
    # set_cookie() method
    response.set_cookie(key="username", value="admin")
    return response

@app.get("/readcookie/")
async def read_cookie( username: str = Cookie( None ) ):
    return {"username": username}

# Read the values of an HTTP header that is a part of the client request. The
# name of the parameter should match with the HTTP header converted in
# camel_case. The "accept-language" header is to be retrieved. Since Python
# doesn’t allow "-" (dash) in the name of identifier, it is replaced by "_" )
@app.get("/headers/")
async def read_header(accept_language: Optional[str] = Header(None)):
    return {"Accept-Language": accept_language}

# Push custom as well as predefined headers in the response object. The
# operation function should have a parameter of Response type. In order to set
# a custom header, its name should be prefixed with "X"
@app.get("/rspheader/")
def set_rsp_headers():
    content = {"message": "Hello World"}
    # X-Web-Framework is a custom header and Content-Language is a pre-defined one.
    headers = {"X-Web-Framework": "FastAPI", "Content-Language": "en-US"}
    return JSONResponse(content=content, headers=headers)

class student(BaseModel):
    id: int
    name :str = Field(None, title="name of student", max_length=10)
    marks: List[int] = []
    percent_marks: float

class percent(BaseModel):
    id:int
    name :str = Field(None, title="name of student", max_length=10)
    percent_marks: float

# An operation function returns A JSON response to the client. The response can
# be in the form of Python primary types, i.e., numbers, string, list or dict,
# etc. It can also be in the form of a Pydantic model. For a function to return
# a model object, the operation decorator should declare a respone_model
# parameter.
#
# With the help of response_model, FastAPI Converts the output data to a
# structure of a model class. It validates the data, adds a JSON Schema for the
# response, in the OpenAPI path operation.
#
# One of the important advantages of response_model parameter is that we can
# format the output by selecting the fields from the model to cast the response
# to an output model.
@app.post("/marks", response_model=percent)
async def get_percent(s1:student):
    # This function receives a student object and return a percent object
    s1.percent_marks = sum(s1.marks)/2
    return s1

class supplier(BaseModel):
    supplierID : int
    supplierName : str

class product(BaseModel):
    productID : int
    prodname : str
    price : int
    supp : supplier

class customer(BaseModel):
    custID : int
    custname : str
    prod : Tuple[product]

@app.post('/invoice')
async def getInvoice(c1:customer):
    return c1

# Event handlers are the functions to be executed when a certain identified
# event occurs. In FastAPI, two such events are identified − startup and
# shutdown. FastAPI’s application object has on_event() decorator that uses one
# of these events as an argument. The startup event occurs before the
# development server starts and the registered function is typically used to
# perform certain initialization tasks, establishing connection with the
# database etc.
@app.on_event("startup")
async def startup_event():
    print('Server started :', datetime.datetime.now())

@app.on_event("shutdown")
async def shutdown_event():
    print('server Shutdown :', datetime.datetime.now())

subapp = FastAPI()

# Access this via http://127.0.0.1:8000/subapp/sub
@subapp.get("/sub")
def subindex():
    return {"message": "Hello World from sub app"}

# If you have two independent FastAPI apps, one of them can be mounted on top
# of the other. The one that is mounted is called a sub-application. The
# app.mount() method adds another completely "independent" application in a
# specific path of the main app. It then takes care of handling everything
# under that path, with the path operations declared in that sub-application.
#
# Both the main and sub application will have its own docs as can be inspected
# using Swagger UI.
#
# http://localhost:8000/docs
# http://localhost:8000/subapp/docs
app.mount("/subapp", subapp)

# A middleware is a function that is processed with every request (before being
# processed by any specific path operation) as well as with every response
# before returning it. This function takes each request that comes to your
# application. It may perform some process with the request by running a code
# defined in it and then passes the request to be processed by the
# corresponding operation function. It can also process the response generated
# by the operation function before returning it.
#
# Following are some of the middleware available in FastAPI library :
# CORSMiddleware, HTTPSRedirectMiddleware, TrustedHostMiddleware,
# GZipMiddleware
#
# In addition to the above integrated middleware, it is possible to define a
# custom middleware. The function has two parameters, the HTTP request object,
# and the call_next() function that will send the API request to its
# corresponding path and return a response.
@app.middleware("http")
async def addmiddleware(request: Request, call_next):
    #  For each request made by the browser, the middleware output (Middleware
    #  works!) will appear in the console log before the response output.
    print("Middleware works!")
    response = await call_next(request)
    return response

# A WSGI application written in Flask or Django framework can be wrapped in
# WSGIMiddleware and mounted it on a FastAPI app to make it ASGI compliant.
#
# pip3 install flask
from flask import Flask
flask_app = Flask( __name__ )

@flask_app.route("/")
def index_flask():
    return "Hello World from Flask!"

from fastapi.middleware.wsgi import WSGIMiddleware
# The Flask sub application is mounted at the URL http://localhost:8000/flask.
app.mount("/flask", WSGIMiddleware(flask_app))

# Dependency injection refers to the mechanism where an object receives other
# objects that it depends on. The other objects are called dependencies.
# Dependency injection has the following advantages:
# - reuse the same shared logic
# - share database connections
# - enforce authentication and security features
from fastapi import Depends
from fastapi import HTTPException

async def dependency1( id: str, name: str, age: int ):
    return { 'id': id, 'name': name, 'age': age }

# curl -X 'GET' 'http://127.0.0.1:8000/user1?id=ink&name=ink&age=20'
@app.get("/user1")
async def user1( dep: dict = Depends( dependency1 ) ):
    return dep

# curl -X 'GET' 'http://127.0.0.1:8000/admin1?id=ink&name=ink&age=20'
@app.get("/admin1")
async def admin1( dep: dict = Depends( dependency1 ) ):
    return dep

class dependency2:
    def __init__(self, id: str, name: str, age: int):
        self.id = id
        self.name = name
        self.age = age

# curl -X 'GET' 'http://127.0.0.1:8000/user2?id=ink&name=ink&age=20'
@app.get("/user2")
async def user2( dep: dependency2 = Depends( dependency2 ) ):
    return dep

# curl -X 'GET' 'http://127.0.0.1:8000/admin2?id=ink&name=ink&age=20'
@app.get("/admin2")
async def admin2( dep: dependency2 = Depends( dependency2 ) ):
    return dep

# Use dependency injection as operation decoration instead of operation
# funciton
async def validate( dep: dependency2 = Depends( dependency2 ) ):
   if dep.age > 18:
      raise HTTPException( status_code=400, detail="You are not eligible" )

# curl -X 'GET' 'http://127.0.0.1:8000/user3?id=ink&name=ink&age=20'
@app.get( "/user3", dependencies=[ Depends( validate ) ] )
async def user3():
   return { "message": "You are eligible" }

# CRUD operations : create, read, update, delete
# This is equivalent to POST, GET, PUT, DELETE methods
class Book( BaseModel ):
    id: int
    title: str
    author: str
    publisher: str

data = []

@app.post( '/book' )
def add_book( book: Book ):
    data.append( book.dict() )
    return data

@app.get( '/list' )
def get_books():
    return data

@app.get( '/book/{id}' )
def get_book( id: int ):
    return data[ id - 1 ]

@app.put( '/book/{id}' )
def add_book( id: int, book: Book ):
    data[ id - 1 ] = book
    return data

@app.delete( '/book/{id}' )
def delete_book( id: int ):
    data.pop( id - 1 )
    return data

# Skip the following
# https://www.tutorialspoint.com/fastapi/fastapi_sql_databases.htm
# https://www.tutorialspoint.com/fastapi/fastapi_using_mongodb.htm
# https://www.tutorialspoint.com/fastapi/fastapi_using_graphql.htm

# WebSocket
# A WebSocket is a persistent connection between a client and server to provide
# bidirectional, full-duplex communication between the two. The communication
# takes place over HTTP through a single TCP/IP socket connection. One of the
# limitations of HTTP is that it is a strictly half-duplex or unidirectional
# protocol. WebSocket uses HTTP as the initial transport mechanism, but keeps
# the TCP connection alive the connection after the HTTP response is received.
# Same connection object it can be used two-way communication between client
# and server. Thus, real-time applications can be built using WebSocket APIs.

# This is the index page
@app.get( "/socket", response_class=HTMLResponse )
async def socket( request: Request ):
    return templates.TemplateResponse( "socket.html", {"request": request} )

# As the JavaScript code is loaded, it creates a websocket listening at
# "ws://localhost:8000/ws". The sendMessage() function directs the input
# message to the WebSocket URL.
#
# This route invokes the websocket_endpoint() function in the application code.
# The incoming connection request is accepted and the incoming message is
# echoed on the client browser.
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")

if __name__ == "__main__":
    # We need to install Uvicorn because FastAPI doesn't contain any
    # built-in development server. Uvicorn implements ASGI (Asynchronous
    # Server Gateway Interface). The old standard WSGI servers
    # (Web Server Gateway Interface) are not suitable for asyncio applications.
    #
    # Uvicorn uses uvloop and httptools libraries. It also provides support for
    # HTTP/2 and WebSockets, which cannot be handled by WSGI. uvloop id similar to
    # the built-in asyncio event loop. httptools library handles the http
    # protocols.
    #
    # "pip3 install uvicorn(standard)" will install cython based dependencies
    # along with other additional libraries e.g. WebSockets and PyYAML.
    #
    # To run the app:
    #   uvicorn main:app –reload
    #
    # The --reload option enables the debug mode so that any changes in app.pywill
    # be automatically reflected and the display on the client browser will be
    # automatically refreshed
    uvicorn.run( "main:app", host="127.0.0.1", port=8000, reload=True )
