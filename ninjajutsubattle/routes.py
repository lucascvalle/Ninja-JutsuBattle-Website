from flask import render_template, redirect, url_for, flash, request, jsonify, abort
from ninjajutsubattle import app, database, bcrypt
from ninjajutsubattle.forms import LoginForm, RegisterForm, EditProfileForm, NinjaForm, PostForm, NinjaSheetForm
from ninjajutsubattle.models import User, Element, Jutsu, KekkeiGenkai, Ninja, Post
from flask_login import login_user, logout_user, current_user, login_required
import random

import secrets
import os
from PIL import Image



@app.route('/')
def home():
    return render_template('home.html')


@app.route('/community')
@login_required
def community():
    posts = Post.query.order_by(Post.id.desc())
    def ninja_count():
        for post in posts:
            ninjas = Ninja.query.filter_by(user_id=post.author.id).all()
            ninja_count = len(ninjas)
        return ninja_count
    return render_template('community.html', posts=posts, ninja_count=ninja_count)


@app.route("/download")
def download():
    return render_template('download.html')


@app.route("/basictechs")
def basic_techs():
    ninjutsu_c = Jutsu.query.filter((Jutsu.element == None) & (Jutsu.kekkei_genkai == None) & (Jutsu.type.like('%Ninjutsu%')) & (Jutsu.rank == 'C')).all()
    ninjutsu_b = Jutsu.query.filter((Jutsu.element == None) & (Jutsu.kekkei_genkai == None) & (Jutsu.type.like('%Ninjutsu%')) & (Jutsu.rank == 'B')).all()
    ninjutsu_a = Jutsu.query.filter((Jutsu.element == None) & (Jutsu.kekkei_genkai == None) & (Jutsu.type.like('%Ninjutsu%')) & (Jutsu.rank == 'A')).all()
    ninjutsu_s = Jutsu.query.filter((Jutsu.element == None) & (Jutsu.kekkei_genkai == None) & (Jutsu.type.like('%Ninjutsu%')) & (Jutsu.rank == 'S')).all()

    genjutsu_c = Jutsu.query.filter((Jutsu.element == None) & (Jutsu.kekkei_genkai == None) & (Jutsu.type.like('%Genjutsu%')) & (Jutsu.rank == 'C')).all()
    genjutsu_b = Jutsu.query.filter((Jutsu.element == None) & (Jutsu.kekkei_genkai == None) & (Jutsu.type.like('%Genjutsu%')) & (Jutsu.rank == 'B')).all()
    genjutsu_a = Jutsu.query.filter((Jutsu.element == None) & (Jutsu.kekkei_genkai == None) & (Jutsu.type.like('%Genjutsu%')) & (Jutsu.rank == 'A')).all()
    genjutsu_s = Jutsu.query.filter((Jutsu.element == None) & (Jutsu.kekkei_genkai == None) & (Jutsu.type.like('%Genjutsu%')) & (Jutsu.rank == 'S')).all()

    taijutsu_c = Jutsu.query.filter((Jutsu.element == None) & (Jutsu.kekkei_genkai == None) & (Jutsu.type.like('%Taijutsu%')) & (Jutsu.rank == 'C')).all()
    taijutsu_b = Jutsu.query.filter((Jutsu.element == None) & (Jutsu.kekkei_genkai == None) & (Jutsu.type.like('%Genjutsu%')) & (Jutsu.rank == 'B')).all()
    taijutsu_a = Jutsu.query.filter((Jutsu.element == None) & (Jutsu.kekkei_genkai == None) & (Jutsu.type.like('%Genjutsu%')) & (Jutsu.rank == 'A')).all()
    taijutsu_s = Jutsu.query.filter((Jutsu.element == None) & (Jutsu.kekkei_genkai == None) & (Jutsu.type.like('%Genjutsu%')) & (Jutsu.rank == 'S')).all()
    return render_template('basic_techniques.html', ninjutsu_c=ninjutsu_c, ninjutsu_b=ninjutsu_b, ninjutsu_a=ninjutsu_a, ninjutsu_s=ninjutsu_s, genjutsu_c=genjutsu_c, genjutsu_b=genjutsu_b, genjutsu_a=genjutsu_a, genjutsu_s=genjutsu_s, taijutsu_c=taijutsu_c, taijutsu_b=taijutsu_b, taijutsu_a=taijutsu_a, taijutsu_s=taijutsu_s)


@app.route("/bloodlinetechs")
def bloodline_techs():
    kekkei_genkais = KekkeiGenkai.query.all()
    return render_template('bloodline_techniques.html', kekkei_genkais=kekkei_genkais)


@app.route("/bloodlines")
def bloodlines():
    kekkei_genkais = KekkeiGenkai.query.all()
    return render_template('bloodlines.html', kekkei_genkais=kekkei_genkais)


@app.route("/elementaltechs")
def elemental_techs():
    elements = Element.query.all()
    jutsu_class = Jutsu
    return render_template('elemental_techniques.html', elements=elements, jutsu_class=jutsu_class)


@app.route("/elements")
def elements():
    return render_template('elements.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = LoginForm()
    form_register = RegisterForm()
    if form_login.validate_on_submit() and 'login_submit' in request.form:
        user = User.query.filter_by(email=form_login.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form_login.password.data):
            login_user(user, remember=form_login.remember_me.data)
            flash(f'{form_login.email.data} logged successfully', 'alert-success')
            next_parameter = request.args.get('next')
            if next_parameter:
                return redirect(next_parameter)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Login failed. Check E-mail or Password', 'alert-danger')
    if form_register.validate_on_submit() and 'register_submit' in request.form:
        password_encrypt = bcrypt.generate_password_hash(form_register.password.data).decode("utf-8")
        user = User(username=form_register.username.data, email=form_register.email.data, password=password_encrypt)
        database.session.add(user)
        database.session.commit()
        flash(f'Account created for the e-mail: {form_register.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('login.html', form_login=form_login, form_register=form_register)


@app.route('/logout')
def logout():
    logout_user()
    flash(f'Logout successful', 'alert-success')
    return redirect(url_for('home'))


@app.route('/profile')
@login_required
def profile():
    profile_pic = url_for('static', filename='profile_pics/{}'.format(current_user.profile_pic))
    ninjas = Ninja.query.filter_by(user_id=current_user.id).all()
    ninja_count = len(ninjas)
    return render_template('profile.html', profile_pic=profile_pic, ninjas=ninjas, ninja_count=ninja_count)


@app.route('/post/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, author=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post created successfully', 'alert-success')
        return redirect(url_for('community'))

    return render_template('createpost.html', form=form)


def save_image(image):
    code = secrets.token_hex(8)
    name, extension = os.path.splitext(image.filename)
    file_fullname = name + code + extension
    full_path = os.path.join(app.root_path, 'static/profile_pics', file_fullname)
    size = (200, 200)
    resized_image = Image.open(image)
    resized_image.thumbnail(size)
    resized_image.save(full_path)
    return file_fullname


@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.profile_pic.data:
            image_name = save_image(form.profile_pic.data)
            current_user.profile_pic = image_name
        database.session.commit()
        flash(f'Profile updated successfully', 'alert-success')
        return redirect(url_for('profile'))
    elif request.method == "GET":
        form.email.data = current_user.email
        form.username.data = current_user.username
    profile_pic = url_for('static', filename='profile_pics/{}'.format(current_user.profile_pic))
    return render_template('editprofile.html', profile_pic=profile_pic, form=form)

@app.route('/roll_dice')
def roll_dice():
    rolls = [random.randint(1, 10) for _ in range(5)]
    rolls.remove(min(rolls))
    total = sum(rolls)
    return jsonify({'rolls': rolls, 'total': total})

@app.route('/jutsus/<rank>')
def get_jutsus(rank):
    jutsus = Jutsu.query.filter_by((Jutsu.element == None) & (Jutsu.kekkei_genkai == None), rank=rank).all()
    jutsu_options = []
    for jutsu in jutsus:
        jutsu_options.append('<option value="{0}">{1}</option>'.format(jutsu.id, jutsu.name))
    return jsonify({'options': jutsu_options})

@app.route('/ninja/create', methods=['GET', 'POST'])
@login_required
def create_ninja():
    form = NinjaForm()

    if request.method == 'POST' and form.validate_on_submit():
        ninja = Ninja(name=form.name.data,
                      speed=form.speed.data,
                      body=form.body.data,
                      mind=form.mind.data,
                      chakra=form.chakra.data,
                      element_primary_id=form.element_primary.data,
                      element_secondary_id=form.element_secondary.data,
                      kekkei_genkai_id=form.kekkei_genkai.data,
                      user_id=current_user.id)

        c_rank_jutsus = form.c_rank_jutsus.data
        b_rank_jutsus = form.b_rank_jutsus.data
        a_rank_jutsus = form.a_rank_jutsus.data
        s_rank_jutsus = form.s_rank_jutsus.data

        jutsus = []
        jutsus.extend(Jutsu.query.filter_by(rank='C', element=None, kekkei_genkai=None).filter(Jutsu.id.in_(c_rank_jutsus)).all())
        jutsus.extend(Jutsu.query.filter_by(rank='B', element=None, kekkei_genkai=None).filter(Jutsu.id.in_(b_rank_jutsus)).all())
        jutsus.extend(Jutsu.query.filter_by(rank='A', element=None, kekkei_genkai=None).filter(Jutsu.id.in_(a_rank_jutsus)).all())
        jutsus.extend(Jutsu.query.filter_by(rank='S', element=None, kekkei_genkai=None).filter(Jutsu.id.in_(s_rank_jutsus)).all())
        ninja.jutsus.extend(jutsus)

        # Adiciona um novo ninja ao banco de dados
        database.session.add(ninja)
        database.session.commit()

        flash('Ninja criado com sucesso!', 'alert-success')
        return redirect(url_for('profile'))

    return render_template('create_ninja.html', form=form)


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def show_post(post_id):
    post = Post.query.get(post_id)
    ninjas = Ninja.query.filter_by(user_id=post.author.id).all()
    ninja_count = len(ninjas)
    if current_user == post.author:
        form = PostForm()
        if request.method == 'GET':
            form.title.data = post.title
            form.body.data = post.body
        elif form.validate_on_submit():
            post.title = form.title.data
            post.body = form.body.data
            database.session.commit()
            flash('Post updated successfully', 'alert-success')
            return redirect(url_for('community'))
    else:
        form = None

    return render_template('post.html', post=post, ninja_count=ninja_count, form=form)

@app.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.author:
        database.session.delete(post)
        database.session.commit()
        flash('Post deleted', 'alert-danger')
        return redirect(url_for('community'))
    else:
        abort(403)


@app.route('/ninja/<int:ninja_id>', methods=['GET', 'POST'])
@login_required
def show_ninja(ninja_id):
    ninja = Ninja.query.get(ninja_id)
    form = NinjaSheetForm()

    if request.method == 'GET':
        form.speed.data = ninja.speed
        form.body.data = ninja.body
        form.mind.data = ninja.mind
        form.chakra.data = ninja.chakra
        form.experience.data = ninja.experience
        form.equipment.data = ninja.equipment
        form.details.data = ninja.details

    elif request.method == 'POST' and form.validate_on_submit():
        ninja.speed = form.speed.data
        ninja.body = form.body.data
        ninja.mind = form.mind.data
        ninja.chakra = form.chakra.data
        ninja.experience = form.experience.data
        ninja.equipment = form.equipment.data
        ninja.details = form.details.data
        database.session.commit()
        flash('Ninja updated successfully', 'alert-success')
        return redirect(url_for('show_ninja', ninja_id=ninja.id))

    return render_template('ninja_sheet.html', form=form, ninja=ninja)

@app.route('/ninja/<int:ninja_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_ninja(ninja_id):
    ninja = Ninja.query.get(ninja_id)
    if current_user.id == ninja.user_id:
        database.session.delete(ninja)
        database.session.commit()
        flash('Ninja deleted', 'alert-danger')
        return redirect(url_for('profile'))
    else:
        abort(403)
