
class Field:
    """ Field Used for HTML transforming to Python Data

    :attributes:
        :source_key: the location of the field within the source, using dot notation for dict keys and list indexes
            ex. zoro_categories.0.level_1
        :transform_func: the name of the Transformer method used to transform this field
        :default: an optional default value for this field
    """

    def __init__(self, data, transform_func, default=None):
        self.data = data
        self.transform_func = transform_func
        self.default = default
