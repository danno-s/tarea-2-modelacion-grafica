# coding: UTF-8
# clase que define las plataformas de un nivel


class Platform(object):
    def __init__(self, top, bottom, left, right, tag="Untagged"):
        self.tag = tag
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right

    def is_above(self, entity):
        # retorna True si la plataforma está sobre la entidad
        if (
            entity.center[0] > self.left - entity.width / 2 and
            entity.center[0] < self.right + entity.width / 2 and
            entity.center[1] >= self.bottom + entity.height / 2
        ):
            return True
        return False

    def is_below(self, entity):
        # retorna True si la plataforma está bajo la entidad
        if (
            entity.center[0] > self.left - entity.width / 2 and
            entity.center[0] < self.right + entity.width / 2 and
            entity.center[1] <= self.top - entity.height / 2
        ):
            return True
        return False

    def is_right(self, entity):
        # retorna True si la plataforma está a la derecha de la entidad
        if entity.center[0] <= self.left - entity.width / 2:
            return True
        return False

    def is_left(self, entity):
        # retorna True si la plataforma está a la izquierda de la entidad
        if entity.center[0] >= self.right + entity.width / 2:
            return True
        return False

    def is_beside(self, entity):
        # retorna True si la plataforma está a un lado de la entidad
        if (
            entity.center[1] > self.top - entity.height / 2 and
            entity.center[1] < self.bottom + entity.height / 2
        ):
            return True
        return False

    def intersects(self, entity):
        # retorna True si la entidad sobrelapa a la plataforma
        if (
            entity.center[0] > self.left - entity.width / 2 and
            entity.center[0] < self.right + entity.width / 2 and
            entity.center[1] > self.top - entity.height / 2 and
            entity.center[1] < self.bottom + entity.height / 2
        ):
            return True
        return False

    def __str__(self):
        # retorna string con el nombre de la plataforma
        # para debuggear
        return self.tag + " platform"
