from flask import Blueprint, render_template, request, session, redirect

from app.utils.md5 import md5
from app.utils import sqlhelper


acc_bp = Blueprint('acc_bp', __name__)


@acc_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    用户登录
    """
    if request.method == 'GET':
        return render_template('login.html')
    name = request.form.get('username')
    password = request.form.get('pwd')

    # 连接数据库，查询用户是否存在
    sql = 'select id,name from users where name=%s and password=%s'
    user_obj = sqlhelper.fetch_one(sql, [name, md5(password)])

    print(user_obj)
    # 用户不存在，则重新登录
    if not user_obj:
        return render_template('login.html', error='用户名密码错误')

    # 用户存在，注入session
    session['userInfo'] = user_obj

    return redirect('/index')


@acc_bp.route('/logout')
def logout():
    """
    用户注销
    """
    if 'userInfo' in session:
        del session['userInfo']
    return redirect('/login')
