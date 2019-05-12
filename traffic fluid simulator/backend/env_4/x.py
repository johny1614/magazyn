import attr


def empty_dic():
    return {}


d = {}


@attr.s()
class A(object):
    dic = attr.ib(default=attr.Factory((empty_dic)))
a = A()
a2 = A()
a.dic['dupa'] = 4
print(a.dic['dupa'])
print(a2.dic['dupa'])
