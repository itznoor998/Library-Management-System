
from flask import Flask,render_template,request,redirect
import time,os

from models import *

app = Flask(__name__)
#======================================= App Routes =============================================================



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Authentication routes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.get('/')
def home():
    return render_template('home.html')
@app.route('/forgot_password', methods=["GET","POST"])
def forgot_pass():
    if request.method=="GET":
        return render_template('forgot.html')
    if request.method=="POST":
        try:
            username = request.form.get('username')
            key = request.form.get('key')
            new_pass = request.form.get('password')
            user = User.query.filter_by(user_name=username).first()
            if user.security_key==key:
                user.password = new_pass
                db.session.commit()
                return render_template('pass_changed.html')
            else:
                return render_template('wrong_input1.html')
        except:
            return render_template('wrong_input1.html')
@app.route('/registration', methods = ["GET","POST"])
def registration():
    if request.method=='GET':
        return render_template('registration.html')
    if request.method=='POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')
            user_type = request.form.get('type')
            key = username[:2]+str(int(time.time()))[-4:]+password[:2]
            user = User(user_name=username,password=password,user_type=user_type,security_key=key)
            db.session.add(user)
            db.session.commit()
            return render_template('welcome.html',user=user)
        except:
            return render_template('username_exist.html')

@app.route('/user/login', methods = ["GET","POST"])
def user_login():
    if request.method=='GET':
        return render_template('login.html')
    if request.method=='POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter_by(user_name=username).first()
            if user.password==password:
                path = "/dashboard/" + username
                return redirect(path)
            else:
                return render_template('wrong_input.html')
        except:
            return render_template('wrong_input.html')

@app.route('/admin/login', methods = ["GET","POST"])
def admin_login():
    if request.method=='GET':
        return render_template('adminlogin.html')
    if request.method=='POST':
        try:
            adminname = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter_by(user_name=adminname).first()
            if user.password==password:
                path = '/dashboard/admin/' + adminname
                return redirect(path)
            else:
                return render_template('wrong_input2.html')
        except:
            return render_template('wrong_input2.html')


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ main routes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~````



#================= user routes ==========================

@app.get('/dashboard/<username>')
def dashboard(username):
    books = Book.query.all()
    if len(books)==0:
        return render_template('no_user_book.html',username=username)
    authors = [ ]
    for book in books:
        book_id = book.book_id
        author = Author.query.filter_by(abook_id=book_id).first()
        authors.append(author)
    list_tuple = [ ]
    for i in range(len(books)):
        list_tuple.append((books[i],authors[i]))
    return render_template('user_dashboard.html',username=username,book_author_tuple=list_tuple)

@app.get('/mybook/<username>')
def mybook(username):
    user = User.query.filter_by(user_name=username).first()
    user_id = user.user_id
    issued_books = IssuedBook.query.filter_by(ibuser_id=user_id).all()
    if len(issued_books)==0:
        return render_template('empty_mybook.html',username=username)
    book_author_tuple = []
    for book in issued_books:
        book_id = book.ibbook_id
        ex_book = Book.query.get(book_id)
        author = Author.query.filter_by(abook_id=book_id).first()
        book_author_tuple.append((ex_book,book,author))
    return render_template('my_books.html',book_author_tuple=book_author_tuple,user=user,username=username)

@app.get('/myfeedback/<username>')
def my_feedback(username):
    user = User.query.filter_by(user_name=username).first()
    user_id = user.user_id
    feedbacks = Feedback.query.filter_by(fuser_id=user_id).all()
    if len(feedbacks)==0:
        return render_template('no_feedback.html',username=username)
    book_feedback_tuple = [ ]
    for feed in feedbacks:
        book_id = feed.fbook_id
        book = Book.query.get(book_id)
        book_feedback_tuple.append((book,feed))
    return render_template('my_feedback.html',book_feedback_tuple=book_feedback_tuple,username=username)

@app.get('/booksection/<username>')
def book_by_section(username):
    books_in_section = BookSection.query.all()
    if len(books_in_section)==0:
        return render_template('no_user_booksection.html',username=username)
    section_books = []
    d = {}
    for book in books_in_section:
        sec_id = book.bssection_id
        book_id  = book.bsbook_id
        section = Section.query.get(sec_id)
        book_ = Book.query.get(book_id)
        try:
            d[section].append(book_)
        except:
            d[section] = [book_]
    for section in d.keys():
        section_books.append((section,d[section]))
    return render_template('sections_user.html',section_books=section_books,username=username)

@app.get('/bookauthor/<username>')
def book_by_author(username):
    books_in_author = Author.query.all()
    if len(books_in_author)==0:
        return render_template('no_user_bookauthor.html',username=username)
    author_books = []
    d = {}
    for author in books_in_author:
        name = author.author_fname+' '+author.author_lname
        book = Book.query.get(author.abook_id)
        try:
            d[name].append(book)
        except:
            d[name] = [book]
    for auth_name in d.keys():
        author_books.append((auth_name,d[auth_name]))
    return render_template('author_user.html',author_books=author_books,username=username)


@app.route('/feedback/book/<int:book_id>/<username>', methods=["GET","POST"])
def feedback(book_id,username):
    book = Book.query.get(book_id)
    user = User.query.filter_by(user_name=username).first()
    if request.method=="POST":
        feedback = request.form.get('feedback')
        feed = Feedback(fbook_id=book_id,fuser_id=user.user_id,feedback_description=feedback)
        db.session.add(feed)
        db.session.commit()
        path = '/myfeedback/'+username
        return redirect(path)
    return render_template('feedback_form.html',username=username,book=book)

#======================== Return,Request and Revoke Book ===============================================


@app.get('/request/book/<int:book_id>/<username>')
def request_book(book_id,username):
    path = '/mybook/'+username
    book = Book.query.get(book_id)
    user = User.query.filter_by(user_name=username).first()
    user_issued_books = IssuedBook.query.filter_by(ibuser_id=user.user_id).all()
    if len(user_issued_books)==5:
        return redirect(path)
    access = BookCopy.query.filter(BookCopy.bcbook_id==book_id and BookCopy.book_status=='Y').first()
    access.book_status='N'
    db.session.commit()
    issued = IssuedBook(ibbook_id=book_id,ibuser_id=user.user_id,ibaccess_id=access.access_id)
    db.session.add(issued)
    db.session.commit()
    username=username
    return redirect(path)

@app.get('/return/book/<int:issuedbook_id>/<username>')
def return_book(issuedbook_id,username):
    ibook = IssuedBook.query.get(issuedbook_id)
    user = User.query.filter_by(user_name=username).first()
    access_no = ibook.ibaccess_id
    access = BookCopy.query.get(access_no)
    access.book_status='Y'
    db.session.delete(ibook)
    db.session.commit()
    path = '/mybook/'+username
    return redirect(path)

@app.get('/revoke/book/<int:issuedbook_id>/<username>')
def revoke_book(issuedbook_id,username):
    issuedbook = IssuedBook.query.get(issuedbook_id)
    access_id = issuedbook.ibaccess_id
    user_id = issuedbook.ibuser_id
    bookcopy = BookCopy.query.get(access_id)
    db.session.delete(issuedbook)
    bookcopy.book_status='Y'
    db.session.commit()
    path = '/details/user/'+str(user_id)+'/'+username
    return redirect(path)

#================================ Book Details ========================================================

@app.get('/details/book/<int:book_id>/<username>')
def book_details(book_id,username):
    book = Book.query.get(book_id)
    user = User.query.filter_by(user_name=username).first()
    file_name = book.book_name+'.txt'
    f = open(file_name,'r')
    content = f.read()
    f.close()
    author = Author.query.filter_by(abook_id=book_id).first()
    link1 = '/manage/book/'
    link2 = '/dashboard/'
    if user.user_type=='Admin':
        return render_template('book_details.html',link=link1,book=book,author=author,content=content,username=username)
    return render_template('book_details.html',link=link2,book=book,author=author,content=content,username=username)

#============================= Author Details ==================================================================

@app.get('/details/author/<int:author_id>/<username>')
def author_details(author_id,username):
    author = Author.query.get(author_id)
    user = User.query.filter_by(user_name=username).first()
    authors = Author.query.filter(Author.author_fname==author.author_fname and Author.author_lname==author.author_lname).all()
    books = []
    for auth in authors:
        book_id = auth.abook_id
        book = Book.query.get(book_id)
        books.append(book)
    link1 = '/manage/book/'
    link2 = '/dashboard/'
    if user.user_type == 'Admin':
        return render_template('author_details.html',link=link1,author=author,books=books,username=username)
    return render_template('author_details.html',link=link2,author=author,books=books,username=username)

#==================== User Details ======================================================

@app.get('/details/user/<int:user_id>/<username>')
def user_details(user_id,username):
    user = User.query.get(user_id)
    issuedbooks = IssuedBook.query.filter_by(ibuser_id=user_id).all()
    books = []
    for ib in issuedbooks:
        book_id = ib.ibbook_id
        book = Book.query.get(book_id)
        books.append((book,ib))
    link = "/manage/user/"
    return render_template('user_details.html',user=user,books=books,username=username,link=link)

#=================================== Section Details ===============================================

@app.get('/details/section/<int:section_id>/<username>')
def section_details(section_id,username):
    section = Section.query.get(section_id)
    booksection = BookSection.query.filter_by(bssection_id=section_id).all()
    books = [ ]
    for bs in booksection:
        book_id = bs.bsbook_id
        book = Book.query.get(book_id)
        author = Author.query.filter_by(abook_id=book_id).first()
        books.append((book,author))
    link='/manage/section/'
    return render_template('section_details.html',link=link,tuple_=books,section=section,username=username)

#=============================== Type of User ==================================================

@app.get('/details/type/<user_type>/<username>')
def user_type(user_type,username):
    users = User.query.filter_by(user_type=user_type).all()
    link = "/manage/user/"
    return render_template('type_details.html',users=users,username=username,type=user_type,link=link)



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Admin routes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.get('/dashboard/admin/<adminname>')
def admin_dashboard(adminname):
    username = adminname
    user = User.query.filter_by(user_name=username).first()
    if user.user_type != "Admin":
        return redirect('/user/login')
    return render_template('admin_dashboard.html',username=username)


@app.get('/available/books/<username>')
def books_avail(username):
    books = Book.query.all()
    if len(books)==0:
        return render_template('no_available.html',username=username)
    books_available = [ ]
    for book in books:
        copies = BookCopy.query.filter(BookCopy.bcbook_id==book.book_id).all()
        available = [ ]
        for copy in copies:
            if copy.book_status=='Y':
                available.append(copy)
        books_available.append((book,len(available)))
    return render_template('avail_books.html',available_books=books_available,username=username)


@app.route('/add/book/<username>',methods=["GET","POST"])
def addbook(username):
    if request.method=="POST":
        book_name=request.form.get('book_name')
        author_fname = request.form.get('author_fname')
        author_lname = request.form.get('author_lname')
        edition = request.form.get('edition')
        n = request.form.get('copies')
        content = request.form.get('book_content')
        file_name = book_name+'.txt'
        try:
            book = Book(book_name=book_name,edition=edition)
            db.session.add(book)
            db.session.commit()
            book=Book.query.filter_by(book_name=book_name).first()
            book_id = book.book_id
            print(book_id)
            author = Author(abook_id=book_id,author_fname=author_fname,author_lname=author_lname)
            db.session.add(author)
            f = open(file_name,'w')
            f.write(content)
            f.close()
            for i in range(int(n)):
                copy_book = BookCopy(bcbook_id=book_id,book_status='Y')
                db.session.add(copy_book)
                db.session.commit()
            return render_template('success_bookadd.html',username=username)
        except:
            path = '/add/book/'+username
            return redirect(path)
    return render_template('addbook.html',username=username)

@app.route('/add/section/<username>',methods=["GET","POST"])
def addsection(username):
    if request.method=="POST":
        username=username
        name = request.form.get('section_name')
        code = request.form.get('section_code')
        try:
            section = Section(section_name=name,section_code=code)
            db.session.add(section)
            db.session.commit()
            return render_template('success_section.html',username=username)
        except:
            path = '/add/section/'+username
            return redirect(path)
    return render_template('add_section.html',username=username)

@app.get('/manage/book/<username>')
def manage_book(username):
    books = Book.query.all()
    if len(books)==0:
        return render_template('no_book_manage.html',username=username)
    return render_template('manage_book.html',books=books,username=username)

@app.route('/update/book/<int:book_id>/<username>',methods=["GET","POST"])
def update_book(book_id,username):
    book = Book.query.get(book_id)
    author = Author.query.filter_by(abook_id=book_id).first()
    file_name = book.book_name+'.txt'
    f = open(file_name,'r')
    book_content = f.read()
    f.close()
    if request.method=="POST":
        name = request.form.get('book_name')
        edition = request.form.get('edition')
        author_fname = request.form.get('author_fname')
        author_lname = request.form.get('author_lname')
        content = request.form.get('book_content')
        try:
            book.book_name=name
            book.edition=edition
            author.author_fname=author_fname
            author.author_lname=author_lname
            db.session.commit()
            f = open(file_name,'w')
            f.write(content)
            f.close()
            old_path = file_name
            new_file_name = name+'.txt'
            dir_path = os.path.dirname(old_path)
            new_path = os.path.join(dir_path,new_file_name)
            os.rename(old_path,new_path)
            path1 = '/manage/book/'+username
            return redirect(path1)
        except:
            path2 = '/update/book/'+str(book_id)+'/'+username
            return redirect(path2)
    return render_template('updatebook.html',username=username,book=book,author=author,book_content=book_content)

@app.route('/remove/book/<int:book_id>/<username>',methods=["GET","POST"])
def remove_book(book_id,username):
    book = Book.query.get(book_id)
    file_name = book.book_name+'.txt'
    if os.path.exists(file_name):
        os.remove(file_name)
    else:
        pass
    copies = BookCopy.query.filter_by(bcbook_id=book_id).all()
    feedbacks = Feedback.query.filter_by(fbook_id=book_id).all()
    issuedbooks = IssuedBook.query.filter_by(ibbook_id=book_id).all()
    for copy in copies:
        db.session.delete(copy)
        db.session.commit()
    for feed in feedbacks:
        db.session.delete(feed)
        db.session.commit()
    for ibook in issuedbooks:
        db.session.delete(ibook)
        db.session.commit()
    author = Author.query.filter_by(abook_id=book_id).first()
    db.session.delete(book)
    db.session.delete(author)
    db.session.commit()
    path = '/manage/book/'+username
    return redirect(path)


@app.get('/manage/section/<username>')
def manage_section(username):
    sections = Section.query.all()
    if len(sections)==0:
        return render_template('no_section_manage.html',username=username)
    section_no_book = [ ]
    for section in sections:
        section_id = section.section_id
        books = BookSection.query.filter_by(bssection_id=section_id).all()
        section_no_book.append((section,len(books)))
    return render_template('manage_section.html',sections_tuple=section_no_book,username=username)

@app.route('/update/section/<int:section_id>/<username>',methods=["GET","POST"])
def update_section(section_id,username):
    section = Section.query.get(section_id)
    if request.method=='POST':
        try:
            name = request.form.get('section_name')
            code = request.form.get('section_code')
            section.section_name=name
            section.section_code=code
            db.session.commit()
            path1 = '/manage/section/'+username
            return redirect(path1)
        except:
            path2 = '/update/section/'+str(section_id)+'/'+username
            return redirect(path2)
    return render_template('update_section.html',username=username,section=section)

@app.route('/remove/section/<int:section_id>/<username>',methods=["GET","POST"])
def remove_section(section_id,username):
    section = Section.query.get(section_id)
    booksections = BookSection.query.filter_by(bssection_id=section.section_id).all()
    for booksection in booksections:
        db.session.delete(booksection)
        db.session.commit()
    db.session.delete(section)
    db.session.commit()
    path = '/manage/section/'+username
    return redirect(path)

@app.route('/add/booksection/<username>',methods=["GET","POST"])
def add_booksection(username):
    if request.method=="POST":
        sname = request.form.get('section_name')
        bname = request.form.get('book_name')
        try:
            section = Section.query.filter_by(section_name=sname).first()
            book = Book.query.filter_by(book_name=bname).first()
            booksection = BookSection(bsbook_id=book.book_id,bssection_id=section.section_id)
            db.session.add(booksection)
            db.session.commit()
            path = '/manage/section/'+username
            return redirect(path)
        except:
            return render_template('no_book_section.html',username=username)
    return render_template('manage_booksection.html',username=username)

@app.get('/manage/user/<username>')
def manage_user(username):
    users = User.query.all()
    if len(users)==0:
        return render_template('no_user.html',username=username)
    return render_template('manage_user.html',users=users,username=username)


@app.get('/remove/user/<int:user_id>/<username>')
def remove_user(user_id,username):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    try:
        issuedbooks = IssuedBook.query.filter_by(ibuser_id=user_id).all()
        feedbacks = Feedback.query.filter_by(fuser_id=user_id).all()
        for feed in feedbacks:
            db.session.delete(feed)
            db.session.commit()
        for book in issuedbooks:
            access_id=book.ibaccess_id
            copy = BookCopy.query.get(access_id)
            copy.book_status='Y'
            db.session.commit()
            db.session.delete(book)
            db.session.commit()
        path = '/manage/user/'+username
        return redirect(path)
    except:
        path = '/manage/user/'+username
        return redirect(path)


#=================== search =================================================

@app.route('/search/<username>',methods=["GET","POST"])
def search(username):
    user = User.query.filter_by(user_name=username).first()
    if user.user_type=='Admin':
        if request.method=='POST':
            search = request.form.get('search')
            books = Book.query.filter(Book.book_name.like('%'+search+'%')).all()
            authors = Author.query.filter(Author.author_fname.like('%'+search+'%')).all()
            sections = Section.query.filter(Section.section_name.like('%'+search+'%')).all()
            return render_template ('admin_search.html',username=username,books=books,authors=authors,sections=sections)
        return render_template("avail_books.html",username=username)
    if request.method=='POST':
        search = request.form.get('search')
        books = Book.query.filter(Book.book_name.like('%'+search+'%')).all()
        authors = Author.query.filter(Author.author_fname.like('%'+search+'%')).all()
        sections = Section.query.filter(Section.section_name.like('%'+search+'%')).all()
        return render_template ('user_search.html',username=username,books=books,authors=authors,sections=sections)
    return render_template("user_dashboard.html",username=username)