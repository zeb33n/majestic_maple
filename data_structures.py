from collections import namedtuple

Card = namedtuple('Card', ['species', 'value'])
Move = namedtuple('Move', ['play_card', 'placement', 'discard_card'])
