# coding:utf-8
import os
import uuid

from flask import request, session
from flask_restful import Api, Resource, marshal_with, fields, marshal, reqparse
from sqlalchemy import or_
from werkzeug.datastructures import FileStorage

import settings
from models import *
from dao import query, quertAll, add, delete, queryByKey, queryById

api = Api()


def init_api(app):
    api.init_app(app)


class UserApi(Resource):  # 声明User资源
    def get(self):  # 查看资源
        # 从数据库中查询所有的用户
        key = queryByKey(User, request.args.get('key'))
        print(key)
        users = quertAll(User)
        print([user for user in users])
        print('---------')
        if not key:
            print('ooo')
            return {'static': 'ok',
                    'msg': '查询用户不存在',
                    'data': [user for user in users]}
        else:
            print(key)
            return {'static': 'ok',
                    'msg': '查询成功',
                    'user': key.json,
                    'data': [user.json for user in users]}

    def post(self):
        # 从上传的form对象中取出name和phone
        name = request.form.get('name')
        phone = request.form.get('phone')
        print(name, phone)
        user = User()
        user.name = name
        user.phone = phone

        add(user)  # 添加到数据库

        return {'static': 'ok',
                'msg': '添加{}用户成功！'.format(name)}

    def delete(self):
        id = request.args.get('id')
        flog = delete(User, id)

        return {'static': flog,
                'msg': '删除用户成功!'}

    def put(self):
        id = request.form.get('id')
        user = queryById(User, id)
        user.name = request.form.get('name')
        user.phone = request.form.get('phone')
        add(user)
        return {'msg': user.name + '修改成功!'}


class ImageApi(Resource):
    # 设置图片Image对象输出的字段
    img_fields = {"id": fields.Integer,
                  "name": fields.String,
                  "img_url": fields.String(attribute='url'),
                  "size": fields.Integer(default=0)}
    # 定义返回字段
    get_out_fields = {
        "static": fields.String(default='ok'),
        "data": fields.Nested(img_fields),
        "size": fields.Integer(default=1)
    }

    # 输入定制
    parser = reqparse.RequestParser()
    parser.add_argument('id',
                        type=int,  # 参数类型
                        required=False,  # 是否必要
                        help='请提供id参数',  # 必须的参数提示
                        action='append',  # 如果有多个相同key的参数，则把这些值追加进一个列表
                        dest='public_name')  # 修改字段名，引用的时候使用public_name

    # @marshal_with(get_out_fields)  #使用marshal时需屏蔽
    def get(self):

        args = self.parser.parse_args()  # 解析参数，如果参数不满足，则会直接返回
        # args['id']

        id = request.args.get('id')
        print('---------', id)
        if id:
            image = query(Image).filter(Image.id == id).first()
            # return {'data':image}
            return marshal(image, self.img_fields)
        else:

            images = quertAll(Image)
            data = {'data': images,
                    "size": len(images)}
            # 向session中存入一个用户名
            session['login_name'] = 'disen'
            return marshal(data, self.get_out_fields)

    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, help='必须提供图片名称参数')
    parser.add_argument('url', required=True, help='必须提供已上传图片路径参数')

    #@marshal_with(get_out_fields)
    def post(self):
        args = self.parser.parse_args()
        print(args.get('name'),'323332')
        # 保存数据
        img = Image()
        img.name = args.get('name')
        print('sdfwefsadvew',img.name)
        img.url = args.get('url')
        print('wefwefwef',img.url)

        add(img) #添加数据库中

        return {'msg': '添加图片成功！'}


class MusicApi(Resource):
    # 定义music输出的字段
    music_fields = {'id': fields.Integer,
                    'name': fields.String,
                    'music_url': fields.String(attribute='url'),
                    'msg': fields.String(default='获取成功!')}
    # 定义各个请求返回的数据字段
    get_out_fields = {'static': fields.String(default='ok'),
                      'musics': fields.Nested(music_fields),
                      'msg': fields.String(default='获取成功!')}

    # 创建request输入参数解析器
    parser = reqparse.RequestParser()

    # 向参数解析器中添加请求参数说明
    parser.add_argument('key', dest='name', type=str, required=True, help='必须提供name搜索的关键字')
    parser.add_argument('id', type=int, help='请确定id参数是否为数值类型')
    parser.add_argument('tag', action='append', required=True, help='至少提供一个tag标签')
    parser.add_argument('session', location='cookies', required=True, help='cookies中不存在session')

    # @marshal_with(get_out_fields)   #设置默认返回数据
    def get(self):
        # id = request.args.get('id')
        # if id:
        #     music = queryById(User, id)
        #     return marshal(music, self.music_fields)
        # else:
        #     print('--------')
        #     musics = quertAll(Music)
        #     print(type(musics))
        #     print(musics[0].name)
        #     musics = {'musics': musics}
        #     # marshal的第一个参数必须是{}字典类型，且字典中的key，第二个参数中必须存在，否则不会显示
        #     return marshal(musics, self.get_out_fields)

        # 按name搜索
        # 通过request参数解析器，开始解析请求参数
        # 如果请求参数不能满足条件，则直接返回参数相关的help说明
        args = self.parser.parse_args()
        # 从args中读取name请求参数的值
        name = args.get('name')
        print(name)
        print(type(name))
        tags = args.get('tag')
        print(type(tags))
        # 从args中读取session
        session = args.get('session')
        print(session)

        musics = query(Music).filter(or_(Music.name.like('%{}%'.format(name))))
        if musics.count():
            data = {'musics': musics.all()}
            return marshal(data, self.get_out_fields)
        return {'msg': 'sereach {} no exist,tags:{}'.format(name, tags)}

    # def post(self):


class UploadfileApi(Resource):
    # 定制输入参数
    parser = reqparse.RequestParser()
    parser.add_argument("img", type=FileStorage, location='files', required=True,
                        help='必须提供一个名为img的File表单参数')

    def post(self):
        # 验证请求参数是否满足条件
        args = self.parser.parse_args()

        # 保存上传的文件
        upFile: FileStorage = args.get('img')
        print('上传的文件名:', upFile.filename)
        # 重新命名文件名
        newFile = str(uuid.uuid4()).replace('-', '') + '.' + upFile.filename.rsplit('.')[1]
        upFile.save(os.path.join(settings.MEDIA_DIR, newFile))

        return {'msg': '上传成功！', 'path': '/static/uploads/{}'.format(newFile)}


# 将资源添加api对象中，并声明uri
# -------------------------------
api.add_resource(UserApi, '/user/')
api.add_resource(ImageApi, '/images/')
api.add_resource(MusicApi, '/musics/')
api.add_resource(UploadfileApi, '/upload/')
