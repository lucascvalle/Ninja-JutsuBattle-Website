from ninjajutsubattle.models import Element, Jutsu, KekkeiGenkai
from ninjajutsubattle import app, database
import random

def get_element_choices():
    with app.app_context():
        elements = Element.query.all()
        choices = [(e.id, e.name) for e in elements]
    return choices


def get_jutsu_choices(rank):
    with app.app_context():
        jutsus = Jutsu.query.filter_by(element=None, kekkei_genkai=None, rank=rank).all()
        choices = [(j.id, j.name) for j in jutsus]
    return choices

def get_kekkei_genkai_choices():
    with app.app_context():
        kekkei_genkais = KekkeiGenkai.query.all()
        choices = [(e.id, e.name) for e in kekkei_genkais]
    return choices

