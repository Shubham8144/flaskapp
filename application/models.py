from datetime import datetime
from application import db, login_manager
from flask_login import UserMixin
import enum


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class UserStatusEnum(enum.Enum):
    customer = 'customer'
    supplier = 'supplier'

user_config = db.Table('user_config',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('widget_id', db.Integer, db.ForeignKey('widget.id'))
)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    user_status = db.Column(db.Enum(UserStatusEnum),default=UserStatusEnum.customer.value,nullable=False)
    customer = db.relationship('Shipment', backref='customer', lazy='dynamic', foreign_keys='Shipment.customerid')
    supplier = db.relationship('Shipment', backref='supplier', lazy='dynamic', foreign_keys='Shipment.supplierid')
    widgets = db.relationship('Widget', secondary=user_config, backref='followers')

    def __repr__(self):
        return f"User('{self.username})"

class ShipmentStatusEnum(enum.Enum):
        Sending = "sending"
        Pending = "Pending"
        Packed = "Pack"
        Shipped = "Shipped"
        In_way = "In way"
        Arrived_Destination = "Arrived Destination"
        Received = "Received"

class Shipment(db.Model):
    __tablename__ = "shipment"
    id = db.Column(db.Integer, primary_key=True)
    orderid = db.Column(db.String(20), unique=True, nullable=False)
    product_name = db.Column(db.String(20))
    quantity = db.Column(db.Integer)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    delivery_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum(ShipmentStatusEnum),default=ShipmentStatusEnum.Pending,nullable=False)
    shipping_address = db.Column(db.String(20))
    order_amount = db.Column(db.Integer)
    customerid = db.Column(db.Integer, db.ForeignKey("user.id"))
    supplierid = db.Column(db.Integer, db.ForeignKey("user.id"))
    
    def __str__(self):
        return f"{self.product_name}"

class WidgetEnum(enum.Enum):
        Chart = "Chart"
        Info = "Info"
        List = "List"
        Statistic = "Statistic"


class Widget(db.Model):
    __tablename__ = "widget"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Enum(WidgetEnum), nullable=False)
    # name = db.Column(db.String(20), unique=True, nullable=False)

