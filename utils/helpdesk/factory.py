# from inspect import signature
from random import randint

from faker import Faker


def rand_ratio():
    return randint(840, 900), randint(473, 573)


fake = Faker('pt_BR')
# print(signature(fake.random_number))


def make_recipe():
    return {
        'ticketid': fake.random_number(digits=5, fix_len=True),
        'description': fake.sentence(nb_words=8),
        'situacao': fake.sentence(nb_words=1),
        'preparation_steps': fake.text(3000),
        'created_at': fake.date_time(),
        'author': {
            'first_name': fake.first_name(),
        },
        'category': {
            'name': fake.word()
        }
    }


if __name__ == '__main__':
    from pprint import pprint
    pprint(make_recipe())
