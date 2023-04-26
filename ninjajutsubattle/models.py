from ninjajutsubattle import database, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    password = database.Column(database.String, nullable=False, )
    profile_pic = database.Column(database.String, default='default.jpg')
    posts = database.relationship('Post', backref='author', lazy=True)
    ninjas = database.relationship('Ninja', backref='creator', lazy=True)


    def count_posts(self):
        return len(self.posts)


class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String)
    body = database.Column(database.Text, nullable=False)
    creation_date = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)


association_table = database.Table('association',
    database.Column('ninja_id', database.Integer, database.ForeignKey('ninja.id')),
    database.Column('jutsu_id', database.Integer, database.ForeignKey('jutsu.id'))
)


class Jutsu(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(50), nullable=False)
    element_id = database.Column(database.Integer, database.ForeignKey('element.id'), nullable=True)
    kekkei_genkai_id = database.Column(database.Integer, database.ForeignKey('kekkei_genkai.id'), nullable=True)
    type = database.Column(database.String(50), nullable=False)
    rank = database.Column(database.String(1), nullable=False)
    cost = database.Column(database.String(50), nullable=False)
    range = database.Column(database.String(50), nullable=False)
    resistance = database.Column(database.String(50), nullable=False)
    hit_damage = database.Column(database.String(50), nullable=False)
    description = database.Column(database.Text)

    element = database.relationship('Element', backref=database.backref('element_jutsus', lazy=True))
    kekkei_genkai = database.relationship('KekkeiGenkai', backref=database.backref('kekkei_genkai_jutsus', lazy=True))

    @classmethod
    def get_jutsu_description(cls, jutsu_id):
        jutsu = cls.query.get(jutsu_id)
        description = f"Name: {jutsu.name}\nType: {jutsu.type}\nRank: {jutsu.rank}\nCost: {jutsu.cost}\nRange: {jutsu.range}\nResistance: {jutsu.resistance}\nHit Damage: {jutsu.hit_damage}\nDescription: {jutsu.description}"
        if jutsu.element:
            description += f"\nElement: {jutsu.element.name}"
        if jutsu.kekkei_genkai:
            description += f"\nKekkei Genkai: {jutsu.kekkei_genkai.name}"
        return description

class Element(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(50), nullable=False)
    jutsus = database.relationship('Jutsu', backref='element_')

    def get_jutsus(self):
        return self.jutsus

    def get_jutsus_by_rank(self, rank):
        return Jutsu.query.filter_by(element_=self, rank=rank).all()


class KekkeiGenkai(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(50), nullable=False)
    description = database.Column(database.Text)
    abilities = database.relationship('KekkeiGenkaiAbility', backref='kekkei_genkai')
    jutsus = database.relationship('Jutsu', backref='jutsus_kekkei_genkai')


class KekkeiGenkaiAbility(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(50), nullable=False)
    description = database.Column(database.Text)
    kekkei_genkai_id = database.Column(database.Integer, database.ForeignKey('kekkei_genkai.id'))


class Ninja(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(50), nullable=False, unique=True)
    speed = database.Column(database.Integer, nullable=False)
    body = database.Column(database.Integer, nullable=False)
    mind = database.Column(database.Integer, nullable=False)
    chakra = database.Column(database.Integer, nullable=False)
    rank = database.Column(database.String(1), nullable=False)
    element_primary_id = database.Column(database.Integer, database.ForeignKey('element.id'))
    element_secondary_id = database.Column(database.Integer, database.ForeignKey('element.id'))
    kekkei_genkai_id = database.Column(database.Integer, database.ForeignKey('kekkei_genkai.id'))
    experience = database.Column(database.Integer, nullable=False, default=0)
    equipment = database.Column(database.Text)
    details = database.Column(database.Text)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
    jutsus = database.relationship('Jutsu', secondary=association_table, backref='ninjas')

    def calculate_rank(self):
        total = self.speed + self.body + self.mind + self.chakra
        if total < 15:
            return 'D'
        elif total < 20:
            return 'C'
        elif total < 25:
            return 'B'
        elif total < 30:
            return 'A'
        else:
            return 'S'

    def __init__(self, name, speed, body, mind, chakra, element_primary_id, element_secondary_id, kekkei_genkai_id,
                 user_id, experience=0, equipment=None, details=None):
        self.name = name
        self.speed = speed
        self.body = body
        self.mind = mind
        self.chakra = chakra
        self.element_primary_id = element_primary_id
        self.element_secondary_id = element_secondary_id
        self.kekkei_genkai_id = kekkei_genkai_id
        self.experience = experience
        self.equipment = equipment
        self.details = details
        self.user_id = user_id
        self.rank = self.calculate_rank()

    @property
    def primary_element(self):
        return Element.query.filter_by(id=self.element_primary_id).first()

    @property
    def secondary_element(self):
        return Element.query.filter_by(id=self.element_secondary_id).first()

    @property
    def kekkei_genkai(self):
        return KekkeiGenkai.query.filter_by(id=self.kekkei_genkai_id).first()

