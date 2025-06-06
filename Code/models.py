from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
#=========================== Library Schema =====================================


class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String,unique=True,nullable=False)
    password = db.Column(db.String,nullable=False)
    user_type = db.Column(db.String,nullable=False)
    security_key =db.Column(db.String,nullable=False,unique=True)

class Book(db.Model):
    __tablename__ = "book"
    book_id = db.Column(db.Integer,primary_key=True)
    book_name = db.Column(db.String,nullable=False,unique=True)
    edition = db.Column(db.Integer,nullable=False)

class Author(db.Model):
    __tablename__ = "author"
    author_id = db.Column(db.Integer,primary_key=True)
    abook_id = db.Column(db.Integer,db.ForeignKey("book.book_id"))
    author_fname = db.Column(db.String,nullable=True)
    author_lname = db.Column(db.String)

class Section(db.Model):
    __tablename__ = "section"
    section_id = db.Column(db.Integer,primary_key=True)
    section_name = db.Column(db.String,nullable=False,unique=True)
    section_code = db.Column(db.String,unique=True,nullable=False)

class BookSection(db.Model):
    __tablename__ = 'book_section'
    book_section_id = db.Column(db.Integer,primary_key=True)
    bsbook_id = db.Column(db.Integer,db.ForeignKey("book.book_id"))
    bssection_id=db.Column(db.Integer,db.ForeignKey("section.section_id"))


class BookCopy(db.Model):
    __tablename__ = "book_copy"
    access_id = db.Column(db.Integer,primary_key=True)
    bcbook_id = db.Column(db.Integer,db.ForeignKey("book.book_id"))
    book_status = db.Column(db.String(1),nullable=False)

class IssuedBook(db.Model):
    __tablename__ = 'issued_book'
    issuedbook_id = db.Column(db.Integer,primary_key=True)
    ibuser_id = db.Column(db.Integer,db.ForeignKey('user.user_id'))
    ibbook_id = db.Column(db.Integer,db.ForeignKey('book.book_id'))
    ibaccess_id = db.Column(db.Integer,db.ForeignKey('book_copy.access_id'))


class Feedback(db.Model):
    feedback_id = db.Column(db.Integer,primary_key=True)
    fuser_id = db.Column(db.Integer,db.ForeignKey("user.user_id"))
    fbook_id = db.Column(db.Integer,db.ForeignKey("book.book_id"))
    feedback_description = db.Column(db.String,nullable=False)