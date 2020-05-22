from sqlalchemy.orm import relationship

from config.database import db

__all__ = ['Order']


class Order(db.Model):
    id = db.Column(db.String(32), nullable=True)
    oid = db.Column(db.String(32), primary_key=True, nullable=False)
    # 设置外键
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_phone = db.Column(db.String(20), nullable=False)
    user = relationship("User", backref="order_of_user")
    good_id = db.Column(db.String(32), nullable=False)
    count = db.Column(db.Integer, default=1)
    unit_price = db.Column(db.Float)
    total_price = db.Column(db.Float)
    discount_info = db.Column(db.String(100))
    create_time = db.Column(db.Integer)
    change_time = db.Column(db.Integer)
    status = db.Column(db.Integer, default=1)
    is_del = db.Column(db.Boolean, default=False)
    store_id = db.Column(db.String(32), default='0')

    phoneNum = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(10))
    address = db.Column(db.String(100))

    paymethod = db.Column(db.String(32))
    actual_price = db.Column(db.Float)
    paytime = db.Column(db.Integer)

    express = db.Column(db.String(32))
    delivery_time = db.Column(db.Integer)
    group_time = db.Column(db.Integer)
    confirm_time = db.Column(db.Integer)
    cancel_time = db.Column(db.Integer)
    text = db.Column(db.String(100))
    is_group = db.Column(db.Boolean, default=False, nullable=True)

    coupon_id = db.Column(db.String(32))
    coupon_name = db.Column(db.String(32))
    coupon_discount = db.Column(db.Float)

    integral_count = db.Column(db.Integer)
    integral_discount = db.Column(db.Float)

    def __init__(self, *args):
        self.id = args[0]
        self.oid = args[0]
        self.uid = args[1]
        self.user_phone = args[2]
        self.good_id = args[3]
        self.count = args[4]
        self.unit_price = args[5]
        self.total_price = args[6]
        self.create_time = args[7]
        self.status = args[8]
        self.store_id = args[9]
        self.phoneNum = args[10]
        self.name = args[11]
        self.address = args[12]

    __mapper_args__ = {"order_by": change_time.desc()}

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return '<Order %r>' % self.oid