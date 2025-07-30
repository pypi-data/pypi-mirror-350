from sympy.sets.fancysets import Reals as _R, Complexes as _C


class Field:
    """
    pass
    """
    pass


class Reals(Field, _R):
    """
    pass
    """

    def __repr__(self):
        return 'R'
    
    def __str__(self):
        return self.__repr__()
    
    def __contains__(self, other):
        try:
            return super().__contains__(other)
        except Exception:
            return False


class Complexes(Field, _C):
    """
    pass
    """

    def __repr__(self):
        return 'C'
    
    def __str__(self):
        return self.__repr__()
    
    def __contains__(self, other):
        try:
            return super().__contains__(other)
        except Exception:
            return False


R = Reals()
C = Complexes()