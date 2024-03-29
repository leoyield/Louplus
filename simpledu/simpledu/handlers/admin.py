from flask import Blueprint, render_template, request, current_app, redirect, url_for, flash
from simpledu.decorators import admin_required
from simpledu.models import Course, User, db, Live
from simpledu.forms import CourseForm, UserForm, EditUserForm, LiveForm, MessageForm

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
@admin_required
def index():
    return render_template('admin/index.html')


@admin.route('/courses')
@admin_required
def courses():
    page = request.args.get('page', default=1, type=int)
    pagination = Course.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/courses.html', pagination=pagination)


@admin.route('/courses/create', methods=['GET', 'POST'])
@admin_required
def create_course():
    form = CourseForm()
    if form.validate_on_submit():
        form.create_course()
        flash('课程创建成功', 'success')
        return redirect(url_for('admin.courses'))
    return render_template('admin/create_course.html', form=form)


@admin.route('/courses/<int:course_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    form = CourseForm(obj=course)
    if form.validate_on_submit():
        form.update_course(course)
        flash('课程更新成功', 'success')
        return redirect(url_for('admin.courses'))
    return render_template('admin/edit_course.html', form=form, course=course)

@admin.route('/course/<int:course_id>/delete')
@admin_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    flash('删除课程成功', 'success')
    return redirect(url_for('admin.courses'))

@admin.route('/users')
@admin_required
def users():
    page = request.args.get('page', default=1, type=int)
    pagination = User.query.paginate(
            page = page,
            per_page = current_app.config['ADMIN_PER_PAGE'],
            error_out = False
            )
    return render_template('admin/users.html', pagination=pagination)

@admin.route('/users/create', methods=['GET', 'POST'])
@admin_required
def create_users():
    form = UserForm()
    if form.validate_on_submit():
        form.create_user()
        flash('用户创建成功', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/create_users.html', form=form)

@admin.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_users(user_id):
    user = User.query.get_or_404(user_id) 
    form = EditUserForm(user_id=user_id, obj=user)
    if form.validate_on_submit():
        form.update_user(user)
        flash('用户修改成功', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/edit_users.html', form=form, user=user)

@admin.route('/users/<int:user_id>/delete')
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('成功删除用户', 'success')
    return redirect(url_for('admin.users'))


@admin.route('/lives')
@admin_required
def lives():
    page = request.args.get('page', default=1, type=int)
    pagination = Live.query.paginate(
            page = page,
            per_page = current_app.config['ADMIN_PER_PAGE'],
            error_out = False
            )
    return render_template('admin/lives.html', pagination=pagination)

@admin.route('/lives/create', methods=['GET', 'POST'])
@admin_required
def create_lives():
    form = LiveForm()
    if form.validate_on_submit():
        form.create_live()
        flash('直播创建成功', 'success')
        return redirect(url_for('admin.lives'))
    return render_template('admin/create_lives.html', form=form)


@admin.route('/lives/<int:live_id>/delete')
@admin_required
def delete_lives(live_id):
    live = Live.query.get_or_404(live_id)
    db.session.delete(live)
    db.session.commit()
    flash('成功删除用户', 'success')
    return redirect(url_for('admin.lives'))

@admin.route('/message', methods=['GET', 'POST'])
@admin_required
def send_message():
    form = MessageForm()
    if form.validate_on_submit():
        form.send_message()
        flash('消息发送成功', 'success')
        return redirect(url_for('admin.send_message'))
    return render_template('admin/send_message.html', form=form)
