from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField, IntegerField, HiddenField, RadioField
from wtforms.validators import Length, Email, EqualTo, Required, URL, NumberRange
from simpledu.models import db, User, Course, Live
import json
from simpledu.handlers.ws import redis


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码', validators=[Required(), Length(6, 24)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交') 

    def validate_email(self, field):
        if field.data and not User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱未注册')

    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')



class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[Required(), Length(3, 24)])
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码', validators=[Required(), Length(6, 24)])
    repeat_password = PasswordField('重复密码', validators=[Required(), EqualTo('password')])
    submit = SubmitField('提交') 

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经存在')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经存在')


    def create_user(self):
        user = User(username=self.username.data,
                    email=self.email.data,
                    password=self.password.data)
        db.session.add(user)
        db.session.commit()
        return user


class CourseForm(FlaskForm):
    name = StringField('课程名称', validators=[Required(), Length(5, 32)])
    description = TextAreaField('课程简介', validators=[Required(), Length(20, 256)])
    image_url = StringField('封面图片地址', validators=[Required(), URL()])
    author_id = IntegerField('作者ID', validators=[Required(), NumberRange(min=1, message='无效的用户ID')])
    submit = SubmitField('提交')

    def validate_author_id(self, field):
        if not User.query.get(self.author_id.data):
            raise ValidationError('用户不存在')

    def create_course(self):
        course = Course()
        self.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return course

    def update_course(self, course):
        self.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return course

class UserForm(RegisterForm):
    role = RadioField('权限', choices=[(10, 'USER'), (20, 'STAFF'), (30, 'ADMIN')], coerce=int, validators=[Required()])
    submit = SubmitField('提交')

    def create_user(self):
        user = User(
                username=self.username.data,
                email=self.email.data,
                password=self.password.data,
                role=self.role.data
                )
        db.session.add(user)
        db.session.commit()
        return user

class EditUserForm(RegisterForm):
    id = HiddenField('')
    role = RadioField('权限', choices=[(10, 'USER'), (20, 'STAFF'), (30, 'ADMIN')], coerce=int, validators=[Required()])
    submit = SubmitField('提交')
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).filter(User.id != self.id.data).first():
            raise ValidationError('用户名已存在')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).filter(User.id != self.id.data).first():
            raise ValidationError('邮箱已占用')
    
    def update_user(self, user):
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user



class LiveForm(FlaskForm):
    livename = StringField('课程名称', validators=[Required(), Length(5, 32)])
    user_id = IntegerField('作者ID', validators=[Required(), NumberRange(min=1, message='无效的用户ID')])
    submit = SubmitField('提交')

    def validate_user_id(self, field):
        if not User.query.get(self.user_id.data):
            raise ValidationError('用户不存在')
    
    def validate_user_name(self, field):
        if not User.query.get(self.user_name.data):
            raise ValidationError('用户不存在')

    def create_live(self):
        live = Live()
        self.populate_obj(live)
        db.session.add(live)
        db.session.commit()
        return live


class MessageForm(FlaskForm):
    message = TextAreaField('系统消息', validators=[Required(), Length(6, 256)])
    submit = SubmitField('提交')

    def send_message(self):
        message = {
                'username': 'System',
                'text': self.message.data
                }
        redis.publish('chat', json.dumps(message))
