class ValidationError(Exception):
    pass


class SlideLayoutInvalid(Exception):
    """The slide layout doesn't match layouts
    present in the base presentation slides."""

class SlidePositionInvalid(Exception):
    """When the position attribute of a slide is too large.
    """


class PlaceholderNameInvalid(Exception):
    """The placeholder's name doesn't match names
    present in the base presentation."""


class PlaceholderTypeInvalid(Exception):
    """The placeholder's type doesn't match types
    'text', 'image' or 'table'."""

class PlaceholderContentInvalid(Exception):
    """When something is wrong with the content of a placeholder."""

class TooManyPlaceholder(Exception):
    """The slide has over 3 placeholders."""

class NoSuchImage(Exception):
    """When you try to add an image that doesn't exist"""

class InvalidMetadata(Exception):
    """When the presentation contains invalid metadata.""" 
