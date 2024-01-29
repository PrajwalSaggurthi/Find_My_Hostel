from flask import Flask, render_template, url_for, session, request, redirect
import auth1
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/homef/<user>', methods = ['POST', 'GET'])
def homef(user):
    data = getHostels()
    return render_template('homef.html', data=data, user = user)

def getHostels():
    data = auth1.databasep()
    users = []
    h = []
    e = []
    info =[]
    for i in data:
        users.append(i)
        for k, j in data[i].items():
            for x, y in data[i][k].items():
                if x == 'Hostel Name':
                    h.append(y)
                if x == 'Email':
                    e.append(y)
    p=[]
    r=[]
    for i in users:
        temp=getDet(i) 
        p.append(temp[1])
        r.append(temp[0])
    for i in range(len(users)):
        info.append(([h[i]]+[e[i]]+[r[i]]+[p[i]]))
    return info
@app.route('/info/<user>')
def info(user):
    return render_template('info.html')

@app.route('/homep/<user>', methods=['POST','GET'])
def homep(user):
    data = getDet(user)
    Price = data[1]
    Rooms = data[0]
    if request.method == 'POST':
        return redirect(url_for('update', user = user))
    return render_template('homep.html', p = Price, r=Rooms,user=user)

def getDet(user):
    data = auth1.database(user)
    data = [data['Price'], data['Rooms']]
    return data

@app.route('/update/<user>', methods = ['POST', 'GET'])
def update(user):
    if request.method == 'POST':
        Price = request.form['Price']
        Rooms = request.form['Rooms']
        auth1.updateProvider(user, Price, Rooms)
        return redirect(url_for('homep', user=user))
    return render_template('updatep.html')

@app.route('/loginp', methods=['POST','GET'])
def loginp():
    if request.method == 'POST':
        userName = request.form['userName']
        userPassword = request.form['userPassword']

        status = auth1.login(userName, userPassword)
        if status == 'Error Loggin in!!':
            return 'Error'
        else:
            user = status['localId']
            return redirect(url_for('homep', user=user))
    return render_template('loginp.html')

@app.route('/loginf', methods = ['POST', 'GET'])
def loginf():
    if request.method == 'POST':
        userNamef = request.form['userNamef']
        userPasswordf = request.form['userPasswordf']

        status = auth1.login(userNamef, userPasswordf)

        if status == 'Error Loggin in!!':
            return 'Error'
        else:
            user=status['localId']
            return redirect(url_for('homef', user=user))

    return render_template('loginf.html')


@app.route('/registerp', methods = ['POST', 'GET'])
def registerp():
    if request.method == 'POST':
        HName=request.form['Hostel_Name']
        FName=request.form['First_Name']
        LName=request.form['Last_Name']
        Email=request.form['Email']
        Phone=request.form['Phone']
        userPassword = request.form['userPassword']

        status = auth1.createUser(Email, userPassword)
        if status == 'Error Creating User':
            return 'ERROR'
            pass
        else:
            info = [status['localId'],HName,FName,LName,Email,Phone]
            auth1.pushProvider(info)
            auth1.updateProvider(status['localId'], 0, 0)
            return redirect(url_for('loginp'))
            pass
    return render_template('registerp.html')

@app.route('/registerf', methods = ['POST', 'GET'])
def registerf():
    if request.method == 'POST':
        FName=request.form['First_Name']
        LName=request.form['Last_Name']
        Email=request.form['Email']
        Phone=request.form['Phone']
        userPassword = request.form['userPassword']

        status = auth1.createUser(Email, userPassword)
        if status == 'Error Creating User':
            return 'Error Creating User'
            pass
        else:
            info = [status['localId'],FName,LName,Email,Phone]
            auth1.pushFinder(info)
            return redirect(url_for('loginf'))
            pass
    return render_template('registerf.html')


if __name__ == '__main__':
    app.run(debug = True)