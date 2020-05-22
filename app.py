from config.database.expired_callback import ExpiredCallback
from settings import PORT, HOST
from config.database import app, db
from cache import set_cache
from views import home, good, category, store, group, user, other, admin

app.register_blueprint(home)
app.register_blueprint(good)
app.register_blueprint(category)
app.register_blueprint(store)
app.register_blueprint(group)
app.register_blueprint(user)
app.register_blueprint(other)
app.register_blueprint(admin)


if __name__ == '__main__':
    db.create_all()
    set_cache()
    ExpiredCallback.monitor()
    app.run(host=HOST, port=PORT, debug=True)