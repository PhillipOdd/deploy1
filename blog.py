from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = '1234'  # Replace with a secure secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'  # SQLite database URL
db = SQLAlchemy(app)

# Define the BlogPost model
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"BlogPost(title='{self.title}', content='{self.content}')"

# Home page to display blog posts
@app.route('/')
def home():
    posts = BlogPost.query.all()
    return render_template('index.html', posts=posts)

# Create a new blog post
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title or not content:
            flash('Both title and content are required.', 'danger')
        else:
            new_post = BlogPost(title=title, content=content)
            db.session.add(new_post)
            db.session.commit()
            flash('Blog post created successfully!', 'success')
            return redirect(url_for('home'))

    return render_template('create.html')

# View a specific blog post
@app.route('/post/<int:id>')
def post(id):
    post = BlogPost.query.get(id)
    if not post:
        flash('Blog post not found.', 'danger')
        return redirect(url_for('home'))
    return render_template('post.html', post=post)

# Update an existing blog post
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    post = BlogPost.query.get(id)
    if not post:
        flash('Blog post not found.', 'danger')
        return redirect(url_for('home'))

    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        flash('Blog post updated successfully!', 'success')
        return redirect(url_for('post', id=post.id))

    return render_template('update.html', post=post)

# Delete an existing blog post
@app.route('/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get(id)
    if not post:
        flash('Blog post not found.', 'danger')
        return redirect(url_for('home'))
    
    db.session.delete(post)
    db.session.commit()
    flash('Blog post deleted successfully!', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    db.create_all()  # Create database tables if they don't exist
    app.run(debug=True)
