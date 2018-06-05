from flask import Flask
from apis import init_api
from settings import Config
from dao import init_db

app = Flask(__name__)

#配置app
app.config.from_object(Config)

#初始化api
init_api(app)

#初始化dao或db
init_db(app)


if __name__ == '__main__':
    app.run()
