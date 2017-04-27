# coding: UTF-8
# clase que define las plataformas de un nivel


class Platform(object):
    def __init__(self, top, bottom, left, right, tag=""):
        self.tag = tag
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right

    def is_above(self, entity):
        if (
            entity.center[0] > self.left - entity.width / 2 and
            entity.center[0] < self.right + entity.width / 2 and
            entity.center[1] >= self.bottom + entity.height / 2
        ):
            return True
        return False

    def is_below(self, entity):
        if (
            entity.center[0] > self.left - entity.width / 2 and
            entity.center[0] < self.right + entity.width / 2 and
            entity.center[1] <= self.top - entity.height / 2
        ):
            return True
        return False

    def is_right(self, entity):
        if entity.center[0] <= self.left - entity.width / 2:
            return True
        return False

    def is_left(self, entity):
        if entity.center[0] >= self.right + entity.width / 2:
            return True
        return False

    def is_beside(self, entity):
        if (
            entity.center[1] > self.top - entity.height / 2 and
            entity.center[1] < self.bottom + entity.height / 2
        ):
            return True
        return False

    def __str__(self):
        return self.tag
