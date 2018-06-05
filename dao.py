# coding:utf-8
from flask_sqlalchemy import SQLAlchemy, BaseQuery

db=SQLAlchemy()

#初始化db
def init_db(app):
    db.init_app(app)

def query(cls) -> BaseQuery:    #通过 -> 来声明函数返回的类型
    return db.session.query(cls)

def quertAll(cls):
    return query(cls).all()

def queryById(cls,id):  #根据id查找 数据
    return query(cls).get(int(id))

def add(obj):   #添加和更新
    db.session.add(obj)
    db.session.commit()

def delete(cls,id):
    try:
        obj = queryById(cls,id)
        db.session.delete(obj)
        db.session.commit()
        return True
    except:
        return False
def queryByKey(cls,key):
    # clsId = query(cls).filter(cls.id == key)
    # if clsId:
    #     return clsId.first()
    # clsName = query(cls).filter(cls.name == key)
    # if clsName:
    #     return clsName.first()
    # clsPhone = query(cls).filter(cls.phone == key)
    # if clsPhone:
    #     return clsPhone.first()
    # return False
    clsKey = query(cls).filter(db.or_(cls.id==key,cls.name==key,cls.phone==key))
    if clsKey.count():
        return clsKey.first()
    return False