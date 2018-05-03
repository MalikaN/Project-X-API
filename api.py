from flask import Flask
from flask_restful import Resource,Api,reqparse
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'malika'
app.config['MYSQL_DATABASE_DB'] = 'ItemListDb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)
api = Api(app)


class root(Resource):
    def get(self):
        return 'hello world'

class createUser(Resource):
    def post(self):
        try:
            parse = reqparse.RequestParser()
            parse.add_argument('email',type=str,help='Email to create user')
            parse.add_argument('password',type=str,help='Password to create user')

            args = parse.parse_args()
            __userEmail = args['email']
            __password = args['password']

            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.callproc('spCreateUser',(__userEmail,__password))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                return {'StatusCode':'200','Message': 'User creation success'}
            else:
                return {'StatusCode':'1000','Message': str(data[0])}
    
        except Exception as e :
            return {'error':str(e)}

class addItems(Resource):
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('itemname',type=str,help='Item Name')
        parse.add_argument('itemprice',type=float,help='Item price')
        parse.add_argument('itemqty',type=int,help='Item Qty')

        args = parse.parse_args()

        __itemName = args['itemname']
        __itemPrice = args['itemprice']
        __itemQty = args['itemqty']

        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.callproc('spAddItem',(__itemName,__itemPrice,__itemQty))
        data = cursor.fetchall()

        if len(data) is 0:
            conn.commit()
            return {'StatusCode':'200','Message': 'Item added Successfully'}
        else:
            return {'StatusCode':'1000','Message': 'Error Occured'}


class getAllItems(Resource):
    def get(self):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.callproc('spGetItems')
            data = cursor.fetchall()

            item_List = []

            for item in data:
                i = {
                    'ItemName' : item[0],
                    'itemPrice' : item[1],
                    'Itemqty' : item[2]
                }
                item_List.append(i)

            return {'StatusCode':'200','Items':item_List}
        except Exception as e :
            return {'error': str(e)}

class getItem(Resource):
    def get(self,id):
        try:
            parse = reqparse.RequestParser()
            parse.add_argument('id',type=int)

            # args = parse.parse_args()
            # args['id'] = str(id)
            __id = id

            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.callproc('spGetItem',__id,)
            data = cursor.fetchall()

            item = []

            for item in data:
                i = {
                     'ItemName' : item[0],
                    'itemPrice' : item[1],
                    'Itemqty' : item[2]
                }
                item.append(i)

            return {'StatusCode':'200','Items':item}

        except Exception as e :
            return {'error': str(e)}
            


api.add_resource(root,'/')
api.add_resource(createUser,'/createuser')
api.add_resource(addItems,'/additems')
api.add_resource(getAllItems,'/getallitems')
api.add_resource(getItem,'/getitem/<int:id>') #this raise error#

if __name__ == '__main__':
    app.run(debug=True)