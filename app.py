
from flask import Flask,jsonify,request
import pymysql

app=Flask(__name__)
app.config.from_object('config.Config')

db_host=app.config['MYSQL_DATABASE_HOST']
db_port=app.config['MYSQL_DATABASE_PORT']
db_user=app.config['MYSQL_DATABASE_USER']
db_pass=app.config['MYSQL_DATABASE_PASSWORD']
db_database=app.config['MYSQL_DATABASE_DB']


@app.route('/')
def hello_world():
#    db=pymysql.connect(host=db_host,port=db_port,user=db_user,password=db_pass,database=db_database)

    return 'Hello World'

@app.route('/invoice/<n_invoice>',methods=['GET'])
def queryInvoice(n_invoice):
    db=pymysql.connect(host=db_host,port=db_port,user=db_user,password=db_pass,database=db_database)
    cur=db.cursor()
    query='''SELECT n_invoice,DATE_FORMAT(date_invoice,'%%Y-%%m-%%d %%T.%%f'),id_client,type_invoice  FROM '''+db_database+'.invoice   where n_invoice=%s;'
    cur.execute(query,(n_invoice))
    resultset=cur.fetchall()
    res=[]

    for row in resultset:
        res.append({'n_invoice':row[0],'date_invoice':row[1],'id_client':row[2],'type_invoice':row[3]})
    
    return jsonify({'res':res})



@app.route('/invoice',methods=['GET'])
def queryInvoiceAll():
    db=pymysql.connect(host=db_host,port=db_port,user=db_user,password=db_pass,database=db_database)
    cur=db.cursor()
    query='''SELECT n_invoice,DATE_FORMAT(date_invoice,'%Y-%m-%d %T.%f'),id_client,type_invoice  FROM '''+db_database+'.invoice;'
    cur.execute(query)
    resultset=cur.fetchall()
    res=[]

    for row in resultset:
        res.append({'n_invoice':row[0],'date_invoice':row[1],'id_client':row[2],'type_invoice':row[3]})

    return jsonify({'res':res})


@app.route('/add/invoice',methods=['POST'])
def addInvoice():
    jsInvoice=request.json
    client=jsInvoice['id_client']
    t_invoice=jsInvoice['type_invoice']
    db=pymysql.connect(host=db_host,port=db_port,user=db_user,password=db_pass,database=db_database)
    cur=db.cursor()
    query='''INSERT INTO '''+db_database+'''.invoice (date_invoice,id_client,type_invoice) VALUES(NOW(),%s,%s);'''
    cur.execute(query,(client,t_invoice))
    db.commit()
    resp=jsonify("Invoice add succesfully")
    return resp


@app.route('/update/item',methods=['PUT'])
def updateItem():
    jsInvoice=request.json
    item=jsInvoice['item']
    n_invoice=jsInvoice['n_invoice']
    quantity=jsInvoice['quantity']
    db=pymysql.connect(host=db_host,port=db_port,user=db_user,password=db_pass,database=db_database)
    cur=db.cursor()
    query='''UPDATE '''+db_database+'''.item_invoice SET quantity=%s WHERE n_invoice=%s AND item_product=%s;'''
    cur.execute(query,(quantity,n_invoice,item))
    db.commit()
    resp=jsonify("Invoice update succesfully")
    return resp


@app.route('/delete/invoice/<n_invoice>')
def deleteInvoice(n_invoice):
    db=pymysql.connect(host=db_host,port=db_port,user=db_user,password=db_pass,database=db_database)
    cur=db.cursor()
    query='''DELETE FROM '''+db_database+'''.invoice WHERE n_invoice=%s;'''
    cur.execute(query,(n_invoice))
    db.commit()
    resp=jsonify("Invoice delete succesfully")
    return resp

if __name__=="__main__":
   app.run(host ='0.0.0.0', port = 5000, debug = True)  


