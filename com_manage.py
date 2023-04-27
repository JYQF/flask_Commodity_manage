import pymysql
from flask import Flask, render_template, request, redirect, url_for
#通过传递template_folder参数来指定包含视图函数渲染的HTML模板文件的路径
app = Flask(__name__, template_folder='templates')

#创建MySQL对象
class mysql:
    def __init__(self,host,user,password,database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        #变量conn初始化为none 确保连接数据库之前不使用conn变量
        self.conn = None

    def connect(self):
        self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password,database=self.database)

    def add(self, id, name, sum, price, data):
        cursor = self.conn.cursor()
        query = "insert into commodity values (%s,%s,%s,%s,%s)"
        cursor.execute(query,(id,name,sum,price,data))
        self.conn.commit()

    def update(self, name, sum, price,data,id):
        cursor = self.conn.cursor()
        query = "update commodity set name=%s,sum=%s,price=%s,data=%s where id=%s"
        cursor.execute(query,(name,sum,price,data,id))
        self.conn.commit()

    def delete(self,id):
        cursor = self.conn.cursor()
        query = "delete from commodity where id = %s"
        cursor.execute(query,(id))
        self.conn.commit()

#inquire处理查询结果、打印数据
    def inquire(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return results

    def show_single(self,id):
        cursor = self.conn.cursor()
        query = "select * from commodity where id =%s"
        cursor.execute(query,(id))
        result = cursor.fetchone()
        return result

    def show_all(self):
        query = "select * from commodity"
        result = self.inquire(query)
        return result

    def checkC(self,id):
        cursor = self.conn.cursor()
        #返回指定条件下满足查询条件的数据行数（即统计数量），而不是返回所有匹配的行
        query = "select count(*) from commodity where id = %s"
        cursor.execute(query,(id))
        result = cursor.fetchone()
        return result

    def checkSingle(self,id):
        cursor = self.conn.cursor()
        #返回所有匹配查询条件的行及其所有列的值
        query = "select * from commodity where id = %s"
        cursor.execute(query, (id))
        result = cursor.fetchone()
        return result

    def checkT(self):
        cursor = self.conn.cursor()
        query = "select * from commodity"
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def quit(self):
        if self.conn is not None:
            self.conn.close()

class commodity:
    def __init__(self, id, name, sum ,price, data):
        self.id = id
        self.name = name
        self.sum = sum
        self.price = price
        self.data = data

#@app.route()装饰器 定义路由 路由表示一个URL路径
@app.route('/')
def index():
    return render_template('index.html')

#创建mysql对象
mysql = mysql(host='localhost',user='root',password='wqwy041803160322',database='commodity')
#连接数据库
mysql.connect()


@app.route('/add', methods=['GET', 'POST'])
def add_com():
    if request.method == 'POST':
        id = request.form.get('id')
        name = request.form.get('name')
        sum = request.form.get('sum')
        price = request.form.get('price')
        data = request.form.get('data')
        result = mysql.checkC(id)
        if result[0] == 0:
            mysql.add(id, name, sum, price, data)
            return redirect(url_for('index'))
        else:
            return '此商品已经存在！'
    else:
        return render_template('add.html')

@app.route('/update', methods=['GET', 'POST'])
def update_com():
    if request.method == 'POST':
        id = request.form.get('id')
        name = request.form.get('name')
        sum = request.form.get('sum')
        price = request.form.get('price')
        data = request.form.get('data')
        result = mysql.checkC(id)
        if result[0] > 0:
            mysql.update(name, sum, price, data, id)
            return redirect(url_for('index'))
        else:
            return '此商品不存在！'
    else:
        return render_template('update.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete_com():
    if request.method == 'POST':
        id = request.form.get('id')
        result = mysql.checkC(id)
        if result[0] > 0:
            mysql.delete(id)
            return redirect(url_for('index'))
        else:
            return '此商品不存在！'
    else:
        return render_template('delete.html')

@app.route('/show_single', methods=['GET', 'POST'])
def show_single():
    if request.method == 'POST':
        id = request.form.get('id')
        result = mysql.checkSingle(id)
        if result is None:
            return '此商品不存在！'
        else:
            return render_template('single.html',commodity=result)
    else:
        return render_template('show_single.html')

@app.route('/show_all', methods=['GET', 'POST'])
def show_all():
    if request.method == 'GET':
        results = mysql.checkT()
        if len(results) == 0:
            return '商品信息为空！'
        else:
            return render_template('show_all.html',results = results)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

mysql.quit()