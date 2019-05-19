import random

import attr

from z import Bclass


@attr.s(auto_attribs=True, cmp=False)
class Aclass:
    b: Bclass = None
