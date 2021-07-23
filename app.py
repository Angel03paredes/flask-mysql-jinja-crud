from flask import Flask,render_template,request
from werkzeug.utils import redirect
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'flask_notes'
mysql = MySQL(app)

@app.route('/')
def main():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id,title,content FROM notes")
    data = cursor.fetchall()
    cursor.close()
    return render_template("index.html",notes = data)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/notes/update/<string:id>',methods=['POST'])
def update(id):
    title = request.form['title']
    content = request.form['content']
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE  notes SET title = %s , content = %s WHERE id = %s", (title,content,id))
    mysql.connection.commit()
    cursor.close()
    return redirect('/')

@app.route('/notes/delete/<string:id>',methods=['GET'])
def deleteNote(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM notes WHERE id = %s ", ( id))
    mysql.connection.commit()
    cursor.close()
    return redirect('/')


@app.route('/notes/create',methods = ['POST'])
def createNote():
    title = request.form['title']
    content = request.form['content']
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO notes (title, content) VALUES (%s,%s)", ( title, content))
    mysql.connection.commit()
    cursor.close()
    return redirect('/')
    


if __name__ == "__main__":
    app.run(debug=True)