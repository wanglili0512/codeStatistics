import os
import uuid

from flask import Blueprint, render_template, session, redirect, request


index_bp = Blueprint('index_bp', __name__)


@index_bp.before_request
def process_request():
    if not session.get('userInfo'):
        return redirect('/login')
    return None


@index_bp.route('/index')
def index():
    """
    首页
    """
    return render_template('index.html')


@index_bp.route('/userlist')
def userlist():
    """
    用户列表
    """
    # 连接数据库，查询用户列表
    import pymysql
    config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': '',
        'db': 'wll',
        'charset': 'utf8'
    }
    conn = pymysql.connect(**config)
    cur = conn.cursor(pymysql.cursors.DictCursor)
    sql = 'select id,name from users'
    cur.execute(sql)
    user_list = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('userlist.html', user_list=user_list)


@index_bp.route('/detail/<int:nid>')
def detail(nid):
    """
    用户代码提交详情
    :param nid: 用户id
    """
    print(nid)
    # 连接数据库，查询用户代码详情
    import pymysql
    config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': '',
        'db': 'wll',
        'charset': 'utf8'
    }
    conn = pymysql.connect(**config)
    cur = conn.cursor(pymysql.cursors.DictCursor)
    sql = 'select id,line,ctime from record where user_id=%s'
    cur.execute(sql, (nid,))
    detail_list = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('detail.html', detail_list=detail_list)


@index_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    """
    上传代码压缩包
    """
    if request.method == 'GET':
        return render_template('upload.html')
    # 获取上传文件信息
    file_obj = request.files.get('codeZip')  # file_obj是FileStorage的实例化对象，有save()方法
    print(file_obj.filename, file_obj.stream)   # 前者是文件名，后者是文件数据流
    print(type(file_obj))   # <class 'werkzeug.datastructures.FileStorage'>

    # 1.验证是否是zip压缩文件
    name_ext = file_obj.filename.rsplit('.', 1)
    if len(name_ext) != 2:
        return '请上传zip压缩文件'
    if name_ext[1] != 'zip':
        return '请上传zip压缩文件'

    # 2.解压zip文件
    import shutil
    target_path = os.path.join('upfiles', str(uuid.uuid4()))
    shutil.unpack_archive(file_obj.stream, target_path, 'zip')   # 解压缩zip文件 unpack_archive()方法

    # 3.统计代码
    file_list = os.walk(target_path)      # walk() 方法递归遍历该目录下所有文件
    total_num = 0
    for file_path, folder, file in file_list:       # 结果的每一项包含  (目录，目录下的文件夹列表，目录下的文件列表)
        for f in file:
            file_name = os.path.join(file_path, f)
            file_ext = file_name.rsplit('.', 1)
            if len(file_ext) != 2:
                continue
            if file_ext[1] != 'py':
                continue
            line_num = 0
            with open(file_name, 'rb') as f:
                for line in f:
                    line = line.strip()
                    if len(line) == 0:
                        continue
                    if line.startswith(b'#'):
                        continue
                    line_num += 1
            total_num += line_num
    print(total_num)

    # 4.获取当前时间
    import datetime
    ctime = datetime.date.today()

    user_id = session['userInfo']['id']

    # 5.验证今天是否上传过
    import pymysql
    config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': '',
        'db': 'wll',
        'charset': 'utf8'
    }
    conn = pymysql.connect(**config)
    cur = conn.cursor(pymysql.cursors.DictCursor)
    sql = 'select id from record where ctime=%s and user_id=%s'
    cur.execute(sql, (ctime, user_id))
    data_obj = cur.fetchone()
    cur.close()
    conn.close()

    if data_obj:
        return '今天已经上传，不能重复上传'

    # 6.连接数据库，写入上传记录
    import pymysql
    config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': '',
        'db': 'wll',
        'charset': 'utf8'
    }
    conn = pymysql.connect(**config)
    cur = conn.cursor(pymysql.cursors.DictCursor)
    sql = 'insert into record(line,ctime,user_id) values(%s,%s,%s)'
    cur.execute(sql, (total_num, ctime, user_id))
    conn.commit()    # 增、删、改 必须要提交
    cur.close()
    conn.close()

    return '上传成功'
