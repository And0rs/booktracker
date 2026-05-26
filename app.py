from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    books = db.relationship('Book', backref='author', lazy='dynamic')
    reviews = db.relationship('Review', backref='user', lazy='dynamic')
    reading_statuses = db.relationship('ReadingStatus', backref='user', lazy='dynamic')

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author_name = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer)
    language = db.Column(db.String(50))
    description = db.Column(db.Text)
    cover_url = db.Column(db.String(500))
    added_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    created_at = db.Column(db.DateTime, default=db.func.now())
    reviews = db.relationship('Review', backref='book', lazy='dynamic')
    reading_statuses = db.relationship('ReadingStatus', backref='book', lazy='dynamic')

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id', ondelete='CASCADE'), nullable=False)
    rating = db.Column(db.String(20), nullable=False)
    text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.now())
    __table_args__ = (db.UniqueConstraint('user_id', 'book_id'),)

class ReadingStatus(db.Model):
    __tablename__ = 'reading_statuses'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id', ondelete='CASCADE'), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    updated_at = db.Column(db.DateTime, default=db.func.now())
    __table_args__ = (db.UniqueConstraint('user_id', 'book_id'),)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/book/<int:id>', methods=['GET', 'POST'])
def book_page(id):
    book = Book.query.get_or_404(id)
    reviews = Review.query.filter_by(book_id=id).order_by(Review.created_at.desc()).all()
    status = None
    if current_user.is_authenticated:
        status = ReadingStatus.query.filter_by(
            user_id=current_user.id, book_id=id
        ).first()
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'review' and current_user.is_authenticated:
            existing = Review.query.filter_by(
                user_id=current_user.id, book_id=id
            ).first()
            if not existing:
                review = Review(
                    user_id=current_user.id,
                    book_id=id,
                    rating=request.form['rating'],
                    text=request.form.get('text', '')
                )
                db.session.add(review)
                db.session.commit()
                return redirect(url_for('book_page', id=id))
        elif action == 'status' and current_user.is_authenticated:
            if status:
                status.status = request.form['status']
                status.updated_at = db.func.now()
            else:
                status = ReadingStatus(
                    user_id=current_user.id,
                    book_id=id,
                    status=request.form['status']
                )
                db.session.add(status)
            db.session.commit()
            return redirect(url_for('book_page', id=id))
        elif action == 'delete_review' and current_user.is_admin:
            review = Review.query.get_or_404(request.form.get('review_id', type=int))
            db.session.delete(review)
            db.session.commit()
            return redirect(url_for('book_page', id=id))
    your_review = current_user.is_authenticated and Review.query.filter_by(
        user_id=current_user.id, book_id=id
    ).first()
    return render_template('book.html', book=book, reviews=reviews, status=status, your_review=bool(your_review))

@app.route('/add-book', methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == 'POST':
        book = Book(
            title=request.form['title'],
            author_name=request.form['author_name'],
            year=request.form.get('year', type=int),
            language=request.form.get('language', ''),
            description=request.form.get('description', ''),
            cover_url=request.form.get('cover_url', ''),
            added_by=current_user.id
        )
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('book_page', id=book.id))
    return render_template('add_book.html')

@app.route('/profile')
@login_required
def profile():
    want = ReadingStatus.query.filter_by(
        user_id=current_user.id, status='want_to_read'
    ).all()
    reading = ReadingStatus.query.filter_by(
        user_id=current_user.id, status='reading'
    ).all()
    read = ReadingStatus.query.filter_by(
        user_id=current_user.id, status='read'
    ).all()
    reviews_count = Review.query.filter_by(user_id=current_user.id).count()
    return render_template(
        'profile.html',
        want=want,
        reading=reading,
        read=read,
        reviews_count=reviews_count
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'register':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            if User.query.filter_by(username=username).first():
                return render_template('login.html', error='Пользователь уже существует')
            if User.query.filter_by(email=email).first():
                return render_template('login.html', error='Email уже используется')
            user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password)
            )
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('index'))
        elif action == 'login':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if not user or not check_password_hash(user.password_hash, password):
                return render_template('login.html', error='Неверный логин или пароль')
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

