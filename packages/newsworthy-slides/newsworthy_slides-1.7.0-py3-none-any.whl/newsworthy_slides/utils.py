from newsworthy_slides.validationerror import SlideLayoutInvalid, PlaceholderNameInvalid

def get_slide_layout(layout_name, pres):
    """Get a slide layout by name in a given presentation.

    This is a method you'd expect to find in pptx.Presentation.
    """
    _layout_names = []
    for slide_layout in pres.slide_layouts:
        if slide_layout.name == layout_name:
            return slide_layout
        _layout_names.append(slide_layout.name)

    raise SlideLayoutInvalid(f"{layout_name} is not a valid slide layout in this "
                             f"presentation. Try one of {_layout_names}.")


def get_placeholder(placeholder_name, slide_obj):
    """Get a placeholder by name in a given slide.

    This is a method you'd expect to find in pptx.Presentation.
    """
    _placeholder_names = []
    for placeholder in slide_obj.placeholders:
        if placeholder.name == placeholder_name:
            return placeholder
        _placeholder_names.append(placeholder.name)

    raise PlaceholderNameInvalid(f"{placeholder_name} is not a valid placeholder"
                                 f" name. Try one of {_placeholder_names}.")

def move_slide(presentation, old_index, new_index):
    """As python-pptx does not support positioning of new slides.

    This function is borrowed from
    https://github.com/scanny/python-pptx/issues/68#issuecomment-129491554
    """
    xml_slides = presentation.slides._sldIdLst  # pylint: disable=W0212
    slides = list(xml_slides)
    xml_slides.remove(slides[old_index])
    xml_slides.insert(new_index, slides[old_index])


def inner_html(soup_elem):
    return soup_elem.decode_contents()
