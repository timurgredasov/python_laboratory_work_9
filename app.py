from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Конфигурация базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель книги
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f'<Book {self.name}>'

# Создание таблиц
with app.app_context():
    db.create_all()

# Главная страница
@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

# Добавление книги
@app.route('/add', methods=['POST'])
def add_book():
    author = request.form.get('author')
    name = request.form.get('name')
    
    if author and name:
        new_book = Book(author=author, name=name)
        db.session.add(new_book)
        db.session.commit()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=8081)