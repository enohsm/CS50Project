from .imports import *


adminbp = Blueprint('admin', __name__, url_prefix='/dashboard/admin')

# ENG: Admin interface route
# TR: Admin arayüzü rotası
@adminbp.route('/')
@x.login_required('admin')
def admin_db():
    return render_template('admin_dashboard.html')


# ENG: Route for setting user permissions
# TR: Kullanıcı yetki ayarlama rotası
@adminbp.route('/roles')
@x.login_required('admin')
def set_roles():
    return render_template('roles.html')


# ENG: Route to fetch roles from the database
# TR: Yetkileri (rolleri) veritabanından alma rotası
@adminbp.route('/get_roles')
@x.login_required('admin')
def get_roles():
    # ENG: Fetch username from request arguments
    # TR: Kullanıcı adını fetch'ten al
    username = request.args.get('username', '')

    # ENG: If 'all' is entered, return all users and their roles
    # TR: Eğer 'all' girişi yapıldıysa tüm kullanıcı ve yetkilerini döndür
    if username.upper() == 'ALL':
        roles = DataBase.execute('SELECT users.id, users.username, users.name, users.surname, roles.role FROM users JOIN roles ON users.id = roles.user_id')
    
    # ENG: Return all users and roles matching the entered username
    # TR: Giriş yapılan kullanıcı adıyla eşleşen tüm kullanıcıları ve yetkilerini döndür
    else:
        roles = DataBase.execute('SELECT users.id, users.username, users.name, users.surname, roles.role FROM users JOIN roles ON users.id = roles.user_id WHERE users.username LIKE ?', '%' + username + '%')
    return jsonify(roles)


# ENG: Route for updating user permissions
# TR: Kullanıcı yetkisini değiştirme işlemleri için rota
@adminbp.route('/set_roles', methods = ['GET', 'POST'])
@x.login_required('admin')
def update_roles():
    if request.method == 'POST':
        user_id = request.args.get('id')
        if not user_id or not user_id.isdigit():
            return jsonify({'status':'error'})
        
        is_exist_user = DataBase.execute('SELECT users.id, roles.role FROM users JOIN roles ON users.id = roles.user_id WHERE users.id = ? AND role = 0', user_id)
        if not is_exist_user:
            flash('The user could not found or already updated.')
            return jsonify({'status':'error'})
        
        try:
            DataBase.execute('UPDATE roles SET role = 1 WHERE user_id = ? AND role = 0', user_id)
            return jsonify({'status':'ok'})
        
        except ValueError:
            return jsonify({'status':'error'})
    
    else:
        return redirect(url_for('admin.set_roles'))
    

# ENG: Posts route
# TR: Gönderiler rotası
@adminbp.route('/posts')
@x.login_required('admin')
def posts_route():
    # ENG: Query posts
    # TR: Gönderileri sorgula
    posts = DataBase.execute('SELECT * FROM posts')

    return render_template('posts.html', posts = posts)

    
# ENG: Route for creating a new post
# TR: Yeni gönderi ekleme rotası
@adminbp.route('/posts/new', methods = ['GET', 'POST'])
@x.login_required('admin')
def new_post():
    if request.method == 'POST':
        
        # ENG: Get data from the form
        # TR: Verileri formdan al
        title = request.form.get('title')
        if not title:
            return x.apology('Invalid title.', 'admin.new_post')
        
        content = request.form.get('content')
        
        if not content:
            return x.apology('Invalid content.', 'admin.new_post')
        
        post_type = request.form.get('type')
        if not post_type or not post_type in ['news', 'announcement']:
            return x.apology('Invalid post type.', 'admin.new_post')
        
        # ENG: Save the post to the database
        # TR: Gönderiyi veritabanına kaydet
        try:
            DataBase.execute('INSERT INTO posts (type, title, content) VALUES(?, ?, ?)', post_type.capitalize(), title.capitalize(), content)
            return x.apology(f'New post ({post_type}) has been successfully created.', 'admin.posts_route')

        except ValueError:
            return x.apology('An error occurred.', 'admin.new_post')
    
    else:

        return render_template('new_post.html')
    

@adminbp.route('/posts/modify', methods = ['GET', 'POST'])
@x.login_required('admin')
def modify_post():
    if request.method == 'POST':

        # ENG: Get the Post ID
        # TR: Post ID al
        postid = request.form.get('id')
        if not postid or not postid.isdigit():
            return redirect(url_for('admin.posts_route'))
        
        # ENG: Get title from form
        # TR: Title formdan al
        title = request.form.get('title')
        if not title:
            return x.apology('Invalid title.', 'admin.modify_post', id = postid)
        
        # ENG: Get content from form
        # TR: İçeriği formdan al
        content = request.form.get('content')
        if not content:
            return x.apology('Invalid content.', 'admin.modify_post', id = postid)

        # ENG: Get type from the form
        # TR: Türü formdan al
        post_type = request.form.get('type')
        if not post_type or post_type not in ['News', 'Announcement']:
            return x.apology('Invalid post type.', 'admin.modify_post', id = postid)

        # ENG: Update the database
        # TR: Veritabanını güncelle
        try:
            DataBase.execute('UPDATE posts SET title = ?, content = ?, type = ? WHERE id = ?', title.capitalize(), content, post_type.capitalize(), postid)
            return x.apology('The post has been successfully updated.', 'admin.posts_route')
                
        except ValueError:
            return x.apology('An error occurred.', 'admin.posts_route')
        
    else:

        # ENG: Get Post ID from the form
        # TR: Post ID formdan al
        post_id = request.args.get('id')
        if not post_id or not post_id.isdigit():
            return redirect('admin.posts_route')

        post_data = DataBase.execute('SELECT * FROM posts WHERE id = ?', post_id)
        if not post_data or len(post_data) != 1:
            return x.apology('The post could not found.', 'admin.posts_route')
        
        return render_template('modify_post.html', p_data = post_data[0], types = ['News', 'Announcement'])


@adminbp.route('/posts/delete', methods = ['POST'])
@x.login_required('admin')
def delete_post():
        
        # ENG: Get Post ID
        # TR: Post ID al
        post_id = request.args.get('id')
        if not post_id or not post_id.isdigit():
            return url_for('admin.posts_route')

        # ENG: Delete the post
        # TR: Duyuruyu sil
        try:
            DataBase.execute('DELETE FROM posts WHERE id = ?', post_id)
            flash('The post has been successfully removed.')
            return url_for('admin.posts_route')
        
        except ValueError:
            flash('An error occurred.')
            return url_for('admin.posts_route')