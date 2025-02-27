from flask import Flask,render_template,request
import datetime
from DBConnection import Db

app = Flask(__name__)


@app.route('/')
def login():
    return render_template('LOGIN.html')

@app.route('/login1',methods=['post'])
def login1():
    username =request.form['textfield']
    password =request.form['textfield2']
    db=Db()
    query="select * from login where USERNAME='"+ username +"' and PASSWORD='"+ password +"'"
    c=db.selectOne(query)
    if c is not None:
        if c['U_TYPE']=='Admin':
            return '''<script>alert('success');window.location="/admin_home"</script>'''
        elif c['U_TYPE']=='Service':
            return '''<script>alert('success');window.location="/service_home"</script>'''
        elif c['U_TYPE'] == 'Kitchen':
            return '''<script>alert('success');window.location="/kit_home"</script>'''
        else:
            return '''<script>alert('Invalid User');window.location="/"</script>'''

    else:
        return '''<script>alert('Invalid User');window.location="/"</script>'''



@app.route('/reg')
def reg():
    return render_template('ADMIN/STAFF.html')

@app.route('/staff_reg',methods=['post'])
def staff_reg():
    staff_name=request.form['textfield']
    staff_photo=request.files['fileField']
    date=datetime.datetime.now().strftime("%y%m%d-%H%M%S")
    staff_photo.save(r"C:\Users\LENOVO\PycharmProjects\AI MENU\static\staff_images//" + date +'.jpg')
    s="/static/staff_images/"+ date +'.jpg'
    contact=request.form['textfield2']
    db=Db()
    query = db.insert("insert into staff VALUES ('','"+ staff_name +"','"+ str(s) +"','"+ contact +"')")
    return '''<script>alert('success');window.location="/reg"</script>'''


@app.route('/staff1')
def staff1():
    db=Db()
    querry=db.select("select * from staff ")
    return render_template('ADMIN/VIEW STAFF.html',data=querry)


@app.route('/view_staff')
def view_staff():
    db=Db()
    query=db.select("select * from staff")
    return render_template('ADMIN/VIEW STAFF.html',data=query)



@app.route('/delete_staff/<b>')
def delete_staff(b):
    db=Db()
    querry=db.delete("delete from staff WHERE staff_id='"+b+"'")
    return '''<script>alert('deleted');window.location="/staff1"</script>'''


@app.route('/staff2/<b>')
def staff2(b):
    db=Db()
    querry=db.selectOne("select * from staff WHERE staff_id='"+b+"'")

    return render_template("ADMIN/stff_update.html",i=querry)




@app.route('/update_staff/<h>',methods=['post'])
def update_staff(h):
    staff_name=request.form['textfield']
    staff_photo=request.files['fileField']
    date=datetime.datetime.now().strftime("%y%m%d-%H%M%S")
    staff_photo.save(r"C:\Users\LENOVO\PycharmProjects\AI MENU\static\staff_images//" + date +'.jpg')
    s="/static/staff_images/"+ date +'.jpg'
    contact=request.form['textfield2']
    db=Db()
    if request.files!=None:
        if staff_photo.filename!="":
            query = db.update("UPDATE staff SET staff_name='"+staff_name+"',staff_photo='"+s+"',contact_no= '"+ contact+"' WHERE staff_id='"+ h +"'")
            return  staff1()
        else:
            query = db.update(
                "UPDATE staff SET staff_name='" + staff_name + "',contact_no= '" + contact + "' WHERE staff_id='" + h + "'")
            return staff1()
    else:
        query = db.update(
            "UPDATE staff SET staff_name='" + staff_name + "',contact_no= '" + contact + "' WHERE staff_id='" + h + "'")
        return staff1()


@app.route('/type')
def type():
    return render_template('ADMIN/FOOD TYPE.html')


@app.route('/food_type',methods=['post'])
def food_type():
    food_type=request.form['textfield']
    db=Db()
    query=db.insert("insert into food_type VALUES ('','"+ food_type +"')")
    return  '''<script>alert('sucess');window.location="/type"</script>'''


@app.route('/view_type')
def view_type():
    db=Db()
    query=db.select("select * from food_type")
    return render_template('ADMIN/VIEW TYPE.html',data=query)


@app.route('/del_type/<g>')
def del_type(g):
    db=Db()
    query=db.delete("delete from food_type WHERE food_type_id='" + str(g) +"' ")
    return '''<script>alert('deleted');window.location="/view_type"</script>'''




@app.route('/add_food')
def add_food():
    db = Db()
    result = db.select("select * from food_type")
    return render_template('ADMIN/ADD_FOOD_ADMIN.html',data = result)


@app.route('/add_food1',methods=['post'])
def add_food1():
    food_type=request.form['select']
    food_name=request.form['textfield2']
    price=request.form['textfield']
    imag=request.files['fileField']

    date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
    imag.save(r"C:\Users\LENOVO\PycharmProjects\AI MENU\static\food//" + date + '.jpg')
    s = "/static/food/" + date + '.jpg'
    db=Db()
    querry=db.insert("insert into food VALUES ('','"+ food_type +"','"+ food_name +"','"+ price +"','"+ str(s) +"')")
    return '''<script>alert('success');window.location="/add_food"</script>'''

@app.route('/add_food2')
def add_food2():
    db = Db()
    result = db.select("SELECT * FROM food,food_type WHERE food.`food_type_id`=`food_type`.`food_type_id`")
    return render_template('ADMIN/VIEW_FOOD.html',data = result)


@app.route('/update_food/<b>')
def update_food(b):
    print(b)
    db=Db()

    res=db.select("select * from food_type ")
    ss=db.select("select * from food_type,food where food.food_type_id=food_type.food_type_id  and food.food_id='"+str(b)+"'")
    return render_template('ADMIN/update_food.html',food_type = res,data = ss )


@app.route('/update_food1',methods=['post'])
def update_food1():

    food_id = request.form['fud_id']

    food_type = request.form['select']
    food_name = request.form['textfield2']
    price = request.form['price']
    imag1 = request.files['pic']

    if request.files!=None:

        if imag1.filename!="":
            date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
            imag1.save(r"C:\Users\LENOVO\PycharmProjects\AI MENU\static\food//" + date + '.jpg')
            path = "/static/food/" + date + '.jpg'
            print(food_type, food_name,path,price)
            db=Db()
            db.update("update food set food_type_id='"+food_type+"',price='"+price+"',food_name='"+food_name+"',image='"+path+"' where food_id='"+ food_id +"'  ")
            return '''<script>alert('success');window.location='/add_food2'</script>'''

        else:
            db = Db()
            db.update("update food set food_type_id='" + food_type + "',price='" + price + "',food_name='" + food_name + "' where food_id='" + food_id + "'  ")
            return '''<script>alert('success');window.location='/add_food2'</script>'''
    else:
        db = Db()
        db.update("update food set food_type_id='" + food_type + "',price='" + price + "',food_name='" + food_name + "' where food_id='" + food_id + "'  ")
        return '''<script>alert('success');window.location='/add_food2'</script>'''



@app.route('/delete_food/<b>')
def delete_food(b):
    db=Db()
    querry=db.delete("delete from food WHERE food_id='"+b+"'")
    return '''<script>alert('deleted');window.location="/add_food2"</script>'''




@app.route('/highlight_food')
def highlight_food():
    db = Db()
    result = db.select("select * from food_type")
    return render_template('ADMIN/HIGHLIGHT FOOD.html',data=result)


@app.route('/highlight_food1',methods=['post'])
def highlight_food1():
    food_type=request.form['select']
    food_name=request.form['textfield2']
    PRICE=request.form['PRICE']
    image=request.files['fileField']
    date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
    image.save(r"C:\Users\LENOVO\PycharmProjects\AI MENU\static\highlight_food\\" + date +'.jpg')
    s = "/static/highlight_food/" + date + '.jpg'
    db=Db()
    data=db.insert("insert into highlight_food VALUES ('','"+ food_type +"','"+ food_name +"','"+ PRICE +"','"+ str(s) +"')")
    return '''<script>alert('success');window.location="/highlight_food"</script>'''

@app.route('/highlight_view')
def highlight_view():
    db=Db()
    query=db.select("SELECT * FROM highlight_food,food_type WHERE highlight_food.food_type_id=food_type.food_type_id")
    print(query)
    return render_template('ADMIN/HIGHLIGHT UPDATE.html',data=query)


@app.route('/high/<k>',methods =['get','post'])
def high(k):

    if request.method=="POST":

        food_type = request.form['food_type']
        print(food_type)
        price = request.form['PRICE']
        food_name = request.form['textfield2']

        pic = request.files['fileField']

        date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        pic.save(r"C:\Users\LENOVO\PycharmProjects\AI MENU\static\highlight_food\\" + date + '.jpg')
        path = "/static/highlight_food" + date + '.jpg'
        db = Db()
        if request.files!=None:
            if pic.filename!="":
                db.update("update highlight_food set food_type_id='" + food_type + "',price='" + price + "',food_name='" + food_name + "',image='" + path + "' where highlight_food_id='" + str(k) + "'  ")
                return '''<script>alert('success');window.location='/highlight_view'</script>'''
            else:
                db.update(
                    "update highlight_food set food_type_id='" + food_type + "',price='" + price + "',food_name='" + food_name + "' where highlight_food_id='" + str(
                        k) + "'  ")
                return '''<script>alert('success');window.location='/highlight_view'</script>'''
        else:
            db.update(
                "update highlight_food set food_type_id='" + food_type + "',price='" + price + "',food_name='" + food_name + "' where highlight_food_id='" + str(
                    k) + "'  ")
            return '''<script>alert('success');window.location='/highlight_view'</script>'''
    else:
        db=Db()
        result = db.select("select * from food_type")
        print(result)
        query=db.selectOne("SELECT * FROM highlight_food WHERE  highlight_food_id='"+ str(k) +"'")
        return render_template('ADMIN/highligh update food.html',data=query,food=result)

@app.route('/delete_high/<b>')
def delete_high(b):
    db = Db()
    querry = db.delete("delete from highlight_food WHERE highlight_food_id='" + b + "'")
    return '''<script>alert('deleted');window.location="/highlight_view"</script>'''



@app.route('/admin_home')
def admin_home():
    return render_template('ADMIN/ADMIN HOME.html')





@app.route('/add_offer')
def add_offer():
    db=Db()
    result = db.select("SELECT * FROM food,food_type WHERE food.`food_type_id`=`food_type`.`food_type_id`")
    return render_template("ADMIN/ADD_OFFER.html",data=result)



@app.route('/offer/<l>')
def offer(l):
    db = Db()

    query = db.select("select * from food ")

    return render_template('ADMIN/OFFER.html',s=query,id=l)


@app.route('/offer1/<k>',methods=['post'])
def offer1(k):


    d=request.form['textfield']
    price=request.form['textfield2']
    print(d,price)
    db = Db()
    db.insert("insert into offer VALUES ('','"+price+"','"+str(k)+"','"+d+"',curdate())")

    return '''<script>alert('sucess');window.location="/add_food2"</script>'''

@app.route('/offer2/')
def offer2():
    db = Db()
    res= db.select("SELECT * FROM offer,food,food_type WHERE food.food_type_id=food_type.food_type_id AND food.food_id=offer.food_id")
    return render_template('ADMIN/VIEW OFFER.html',data=res)


@app.route('/upd_offer/<m>',methods=['get'])
def upd_offer(m):
    db = Db()
    res= db.selectOne("SELECT * FROM offer WHERE offer_id='"+ str(m) +"' ")
    return render_template('ADMIN/OFFER UPDATE.html',data=res)



@app.route('/update_offer/<l>',methods=['post'])
def update_offer(l):
    offered_price=request.form['textfield2']
    valid_to=request.form['textfield']
    db = Db()
    db.update("update offer SET offered_price='"+offered_price+"',valid_to='"+valid_to+"' where offer_id='"+ str(l) +"'")
    return '''<script>alert('sucess');window.location="/offer2"</script>'''





@app.route('/delete_offer/<b>')
def delete_offer(b):
    db=Db()
    querry=db.delete("delete from offer WHERE offer_id='"+str(b)+"'")
    return '''<script>alert('deleted');window.location="/offer2"</script>'''





@app.route('/comp')
def comp():
    db=Db()
    querry=db.select("select * from complaint,tables where complaint.table_id=tables.table_id")
    return render_template('ADMIN/COMPLAINT.html',data=querry)

@app.route('/reply/<k>')
def reply(k):
    return render_template('ADMIN/REPLY.html',id=k)


@app.route('/reply1/<k>',methods=['post'])
def reply1(k):
    reply=request.form['textarea']
    db=Db()
    query=db.update("UPDATE complaint SET reply='"+reply+"' , reply_date=CURDATE() where complaint_id='"+str(k)+"'")
    return '''<script>alert('sucess');window.location="/comp"</script>'''



@app.route('/view_help')
def view_help():
    db=Db()
    result=query=db.select("select * from help_center,tables where help_center.tableid=tables.table_id")
    return render_template("ADMIN/HELP VIEW.html",data=result)


@app.route('/table')
def table():
    return render_template('ADMIN/ADD TABLE.html')


@app.route('/add_table',methods=['post'])
def add_table():
    table_name=request.form['textfield']
    db=Db()
    query=db.insert("insert into tables VALUES ('','"+ table_name +"')")
    return  '''<script>alert('sucess');window.location="/table"</script>'''


@app.route('/view_table')
def view_table():
    db=Db()
    query=db.select("select * from tables")
    return render_template('ADMIN/VIEW TABLE.html',data=query)

@app.route('/del_table/<u>')
def del_table(u):
    db=Db()
    query=db.delete("delete from tables WHERE table_id='"+str(u)+"' ")
    return  '''<script>alert('deleted');window.location="/view_table"</script>'''



#SERVICE STATION


@app.route('/service_home')
def service_home():
    return render_template('SERVICE STATION/SERVICE HOME.html')


@app.route('/view_custhelp')
def view_custhelp():
    db=Db()
    query=db.select("SELECT * FROM help_center,TABLES WHERE `help_center`.`tableid`=`tables`.`table_id`")
    return render_template('SERVICE STATION/VIEW HELP.html',data=query)



@app.route('/view_order')
def view_order():
    db=Db()
    query=db.select("SELECT * FROM `master_table`,`tables`,`orders` WHERE `orders`.`master_id`=`master_table`.`master_table_id` and `master_table`.`table_id`=`tables`.`table_id` AND `master_table`.`status`='pending' GROUP BY `master_table`.`table_id`")
    return render_template('SERVICE STATION/VIEW ORDER.html',data=query)

@app.route('/service_view_food/<mid>')
def service_view_food(mid):
    db=Db()
    query=db.select("SELECT * FROM `orders`,`food` WHERE `orders`.`food_id`=`food`.`food_id` AND `orders`.`master_id`='"+mid+"'")
    return render_template('SERVICE STATION/VIEW FOOD.html',data=query)


@app.route('/service_view_staff/<mid>')
def service_view_staff(mid):
    db=Db()
    query=db.select("select * from staff")
    return render_template('SERVICE STATION/VIEW STAFF.html',data=query,data1=mid)


@app.route('/allocate_staff/<mid>/<sid>')
def allocate_staff(mid,sid):
    db=Db()
    query=db.update("UPDATE orders SET ostatus='allocated' where master_id='"+mid+"'")
    db.insert("INSERT INTO `allocate_staff` VALUES('','"+sid+"','"+mid+"')")
    return '''<script>alert('sucess');window.location="/view_order"</script>'''



@app.route('/view_allocate_staff')
def view_allocate_staff():
    db=Db()
    query=db.select("SELECT * FROM allocate_staff,staff,master_table,TABLES WHERE allocate_staff.staff_id=staff.staff_id AND allocate_staff.master_id=master_table.master_table_id AND master_table.table_id=tables.table_id")
    return render_template('SERVICE STATION/VIEW ALLOCATED STAFF.html',data=query)


#kitchen


@app.route('/kit_home')
def kit_home():
    return render_template('KITCHEN/KITCHEN HOME.html')


@app.route('/kit_order')
def kit_order():
    db=Db()
    query=db.select("SELECT * FROM `master_table`,`tables`,`orders` WHERE `orders`.`master_id`=`master_table`.`master_table_id` and `master_table`.`table_id`=`tables`.`table_id` AND `master_table`.`status`='pending' GROUP BY `master_table`.`table_id`")
    return render_template('KITCHEN/VIEW ORDER.html',data=query)


@app.route('/kit_comment')
def kit_comment():
    db=Db()
    query=db.select("select * from tables,feedback WHERE tables.table_id=feedback.table_id")
    return render_template('KITCHEN/COMMENT.html',data=query)

@app.route('/del_comment/<b>')
def del_comment(b):
    db=Db()
    query=db.delete("delete from feedback where feedback_id='"+str(b)+"' ")
    return '''<script>alert('deleted');window.location="/kit_comment"</script>'''




if __name__ == '__main__':
    app.run(port=3000)
