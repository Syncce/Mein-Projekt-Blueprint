from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError

from . import login_manager, SessionLocal
from .models import User, Post
from .forms import RegisterForm, LoginForm, PostForm

main_bp = Blueprint("main", __name__)

@login_manager.user_loader
def load_user(user_id: str):
    with SessionLocal() as db:
        return db.get(User, int(user_id))

@main_bp.route("/")
def index():
    # Posts + Author laden
    with SessionLocal() as db:
        posts = db.execute(
            select(Post)
            .options(selectinload(Post.author))
            .order_by(Post.created_at.desc())
            .limit(5)
        ).scalars().all()
    return render_template("index.html", posts=posts)

@main_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RegisterForm()
    if form.validate_on_submit():
        with SessionLocal() as db:
            u = User(username=form.username.data, email=form.email.data)
            u.set_password(form.password.data)
            try:
                db.add(u)
                db.commit()
            except IntegrityError:
                db.rollback()
                # Falls UNIQUE-Constraint greift (Username/Email doppelt)
                flash("Benutzername oder E-Mail existiert bereits.", "danger")
                return render_template("register.html", form=form)
        flash("Registrierung erfolgreich. Bitte einloggen.", "success")
        return redirect(url_for("main.login"))
    return render_template("register.html", form=form)

@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        with SessionLocal() as db:
            u = db.execute(
                select(User).where(
                    or_(User.username == form.identifier.data, User.email == form.identifier.data)
                )
            ).scalar_one_or_none()
            if u and u.check_password(form.password.data):
                login_user(u)
                flash("Willkommen zurück!", "success")
                return redirect(request.args.get("next") or url_for("main.index"))
        flash("Ungültige Anmeldedaten.", "danger")
    return render_template("login.html", form=form)

@main_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Abgemeldet.", "info")
    return redirect(url_for("main.index"))

@main_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = PostForm()
    if form.validate_on_submit():
        with SessionLocal() as db:
            p = Post(title=form.title.data, body=form.body.data, author_id=current_user.id)
            db.add(p)
            db.commit()
        flash("Beitrag veröffentlicht.", "success")
        return redirect(url_for("main.posts"))
    return render_template("create_post.html", form=form)

@main_bp.route("/posts")
def posts():
    # Eager load Author, sonst DetachedInstanceError in posts.html
    with SessionLocal() as db:
        items = db.execute(
            select(Post)
            .options(selectinload(Post.author))
            .order_by(Post.created_at.desc())
        ).scalars().all()
    return render_template("posts.html", posts=items)

@main_bp.route("/post/<int:post_id>")
def post_detail(post_id: int):
    # Eager load Author auch im Detail
    with SessionLocal() as db:
        post = db.execute(
            select(Post).options(selectinload(Post.author)).where(Post.id == post_id)
        ).scalar_one_or_none()
    if not post:
        flash("Beitrag nicht gefunden.", "warning")
        return redirect(url_for("main.posts"))
    return render_template("post_detail.html", post=post)


@main_bp.route("/post/<int:post_id>/edit", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    with SessionLocal() as db:
        post = db.get(Post, post_id)
        if not post:
            flash("Beitrag nicht gefunden.", "danger")
            return redirect(url_for('main.posts'))

        if post.author_id != current_user.id:
            flash("Du kannst nur deine eigenen Beiträge bearbeiten.", "danger")
            return redirect(url_for('main.posts'))

        form = PostForm()
        if form.validate_on_submit():
            post.title = form.title.data
            post.body = form.body.data
            db.commit()
            flash("Beitrag erfolgreich aktualisiert!", "success")
            return redirect(url_for('main.post_detail', post_id=post.id))

        if request.method == 'GET':
            form.title.data = post.title
            form.body.data = post.body

        return render_template('edit_post.html', form=form, post=post)


@main_bp.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    with SessionLocal() as db:
        post = db.get(Post, post_id)
        if not post:
            flash("Beitrag nicht gefunden.", "danger")
            return redirect(url_for('main.posts'))

        if post.author_id != current_user.id:
            flash("Du kannst nur deine eigenen Beiträge löschen.", "danger")
            return redirect(url_for('main.posts'))

        db.delete(post)
        db.commit()
        flash("Beitrag erfolgreich gelöscht!", "success")
        return redirect(url_for('main.posts'))
