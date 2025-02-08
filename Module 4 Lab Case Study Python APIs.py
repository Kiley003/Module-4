from flask import Flask
app=Flask(__name__)
from flask_sqlalchemy import SQLAchemy
db = SQLAchemy(app)

app.config['SQLACHEMY_DATABASE_URI'] = 'squlite:///data.db'
app.app_context()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    book_name = db.Column(db.String(90), nullable=False) 
    author = db.Column(db.String(90), nullable=False) 
    publisher = db.Column(db.String(90), nullable=False) 
    
    def __repr__(self): 
        return f"{self.id} - {self.book_name} - {self.author} - {self.publisher}"
    
@app.route('/books')
def get_books():
    books=Book.query.all()

    output=[]
    for book in books:
        book_data={'book_name':book.book_name,'author':book.author, 'publisher':book.publisher}
        output.append(book_data)
    return{"books":output}

@app.route('/books/ <id>')
def get_book(id):
    book=Book.query.get_or_404(id)
    return {'book_name':book.book_name,'author':book.author, 'publisher':book.publisher}

@app.route('/books', methods=['POST'])
def add_book():
    book=Book(book_name=request.json['book_name'], author=request.json['author'], publisher=request.json['publisher'])
    db.session.add(book)
    db.session.commit()
    return{'id': book.id}

@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    book=Book.query.get(id)
    if book is None:
        return{"error": "not found"}
    db.session.delete(book)
    db.session.commit()
    return {"message": "Goodbye"}