#####################################################################################


class Property:
    def __init__(self, owner: object, field: str, title="noname", reset=False):
        self._owner = owner
        self._field = field
        self.title = title
        self.reset = reset

    def get(self):
        return getattr(self._owner, self._field)

    def let(self, value):
        setattr(self._owner, self._field, value)

    def __str__(self):
        resetable = "R " if self.reset else ""
        return f"{resetable}'{self.title}'"

    def __repr__(self):
        return str(self)


######################################################################################


class NumericProperty(Property):
    def __init__(self, *vargs, min=0.0, max=1.0, count=1, **kwargs):
        super().__init__(*vargs, **kwargs)
        self.min = min
        self.max = max
        self.count = count

    def __str__(self):
        prefix = super().__str__()
        return f"{prefix} = {self.get()}. Numeric {self.min} .. {self.max}"


######################################################################################


class BooleanProperty(Property):
    def __init__(self, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)

    def __str__(self):
        prefix = super().__str__()
        return f"{prefix} = {self.get()}"


######################################################################################


class ListProperty(Property):
    def __init__(self, *vargs, values=[], **kwargs):
        assert len(values) > 0
        super().__init__(*vargs, **kwargs)
        self.values = values

    def get(self):
        value = getattr(self._owner, self._field)
        assert value in self.values
        return value

    def let(self, value):
        assert value in self.values
        setattr(self._owner, self._field, value)

    def get_index(self, value=None):
        if value is None:
            value = self.get()
        return next((n for n, v in enumerate(self.values) if v == value))

    def let_index(self, index):
        self.let(self.values[index])

    def __str__(self):
        prefix = super().__str__()
        choices = ", ".join(f"{n}: `{v}`" for n, v in enumerate(self.values))
        return f"{prefix} = {self.get()}. One of {choices}"


######################################################################################


class PropertiesCollection:
    def __init__(self, props:list[Property]):
        self._props = props
        self._extract_names()

    def _extract_names(self):
        self._names = { p.title:n for n, p in enumerate(self._props) }

    def _resolve(self, key):
        if isinstance(key, str):
            if key not in self._names:
                raise KeyError(f"Property `{key}` does not exist.")
            return self._names[key]
        if isinstance(key, int):
            N = len(self._props)
            if not (0<=key<N):
                raise KeyError(f"Property index `{key}` does not belong to 0..{N}.")
            return key
        raise KeyError(f"Key type `{type(key)}` is not int or str.")

    def prop(self, key) -> Property:
        return self._props[self._resolve[key]]

    def __getitem__(self, key):
        return self._props[self._resolve(key)].get()

    def __setitem__(self, key, value):
        self._props[self._resolve(key)].let(value)

    def __str__(self):
        return ', '.join(f"{n}:'{k}'" for k, n in self._names)

    def __repr__(self):
        return str(self)


######################################################################################
