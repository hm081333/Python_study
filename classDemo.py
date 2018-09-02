# encoding: utf-8
class Bird(object):
    have_feather = True
    way_of_reproduction = 'egg'

    def move(self, dx, dy):
        print(self.way_of_reproduction)
        position = [0, 0]
        position[0] = position[0] + dx
        position[1] = position[1] + dy
        return position


class Chicken(Bird):
    way_of_move = 'walk'
    possible_in_KFC = True


class Oriole(Bird):
    way_of_move = 'fly'
    possible_in_KFC = False


class happyBird(Bird):
    def __init__(self, more_words):  # 类似构造函数
        print('We are happy birds.', more_words)


summer = happyBird('Happy,Happy!')
