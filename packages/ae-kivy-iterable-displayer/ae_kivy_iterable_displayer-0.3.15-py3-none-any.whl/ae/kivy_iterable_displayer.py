"""
iterable displayer widget
=========================

the popup widget provided by this ae namespace portion displays items and subitems of any type of iterables,
like dicts, lists, sets and tuples.


iterable displayer usage
------------------------

to open a popup displaying the keys/indexes and values of any iterable, create an instance of the class
:class:`IterableDisplayerPopup`. you can specify a popup window title string via the `title` kwarg and pass the iterable
to the `data` kwarg (or property)::

    dict_displayer = IterableDisplayerPopup(title="popup window title", data=iterable_data)

a widget will be automatically instantiated for each subitem of `iterable_data` to display the item key and value.
the used widget class is depending on the type of the subitem. for non-iterable subitems the `IterableDisplayerLabel`
widget will be used. if instead a subitem contains another iterable, then :class:`IterableDisplayerPopup` will use
the `IterableDisplayerButton` class, which when tapped displays another instance of :class:`IterableDisplayerPopup`
with the sub-subitems.

.. note::
    the string in the :attr:`~kivy.uix.popup.Popup.title` property may be shortened automatically by
    :class:`~ae.kivy.widgets.FlowPopup`, depending on the width of the popup layout and the `font_size` app state.

"""
from typing import Any, Union

from kivy.lang import Builder                               # type: ignore
from kivy.properties import ObjectProperty                  # type: ignore # pylint: disable=no-name-in-module

from ae.files import file_transfer_progress                 # type: ignore
from ae.gui.utils import id_of_flow                         # type: ignore
from ae.kivy.widgets import FlowPopup                       # type: ignore


__version__ = '0.3.15'


KEY_VAL_SEPARATOR = ": "


Builder.load_string('''
#: set KEY_VAL_SEPARATOR "''' + KEY_VAL_SEPARATOR + '''"

<IterableDisplayerPopup>
    optimal_content_height: content_box.minimum_height
    IterableDisplayerContent:
        id: content_box
        child_data_maps: root.compile_data_maps(root.data)
        size_hint_y: None
        height: root.optimal_content_height

<IterableDisplayerContent@DynamicChildrenBehavior+BoxLayout>
    orientation: 'vertical'

<IterableDisplayerLabel@BoxLayout>
    text: "." + KEY_VAL_SEPARATOR + "."
    size_hint: 1, None
    height: app.button_height
    ImageLabel:
        id: key
        size_hint_x: None
        width: root.width * .3
        text_size: root.width * .3, self.height
        halign: 'left'
        shorten: True
        shorten_from: 'right'
        text: root.text[:root.text.index(KEY_VAL_SEPARATOR)]
    ScrollView:
        size_hint: 1, None
        height: app.button_height
        do_scroll_y: False
        ImageLabel:
            id: val
            text: root.text[root.text.index(KEY_VAL_SEPARATOR) + len(KEY_VAL_SEPARATOR):]
            size_hint: None, None
            text_size: None, self.height
            size: self.texture_size

<IterableDisplayerButton@BoxLayout>
    size_hint: 1, None
    height: app.button_height
    text: "-" + KEY_VAL_SEPARATOR + "-"
    tap_flow_id: ""
    tap_kwargs: {}
    ImageLabel:
        size_hint_x: 0.3
        text_size: self.size
        halign: 'left'
        shorten: True
        shorten_from: 'right'
        text: root.text[:root.text.index(KEY_VAL_SEPARATOR)]
    FlowButton:
        size_hint_x: 0.69
        text_size: self.size
        halign: 'left'
        shorten: True
        shorten_from: 'right'
        text: root.text[root.text.index(KEY_VAL_SEPARATOR) + len(KEY_VAL_SEPARATOR):]
        tap_flow_id: root.tap_flow_id
        tap_kwargs: root.tap_kwargs
        square_fill_ink: app.main_app.read_ink[:3] + [0.18]
        square_fill_pos: self.pos
''')


class IterableDisplayerPopup(FlowPopup):
    """ FlowPopup displaying iterable data - useful for quick prototyping and debugging. """
    data = ObjectProperty()                 #: the iterable (dict, list, set, tuple) from which the items will be shown

    @staticmethod
    def compile_data_maps(data: Union[dict, list, set, tuple]):
        """ re-create data maps if the :attr:`~IterableDisplayerPopup.data` attribute changes.

        :param data:            dict/list/set/tuple data to display (==self.data binding).
        :return:                list of dicts to be assigned to self.child_data_maps.
        """
        if isinstance(data, dict):
            items = data.items()
        else:                               # if isinstance(data, (list, set, tuple)):
            items = enumerate(data)         # type: ignore # treat the other types like dicts with the index as the key

        cdm = []
        for key, val in items:
            text = (str(key) + KEY_VAL_SEPARATOR + str(val))[:963]  # cut long text preventing black texture kivy/gl bug
            if key in ('transferred_bytes', 'total_bytes') and val > 1024:
                text += " (" + file_transfer_progress(val) + ")"
            kwargs: dict[str, Any] = {'text': text}
            if isinstance(val, (dict, list, set, tuple)):
                cls = 'IterableDisplayerButton'
                kwargs['tap_flow_id'] = id_of_flow('open', 'iterable_displayer', text)
                kwargs['tap_kwargs'] = {'popup_kwargs': {'title': text, 'data': val}}
            else:
                cls = 'IterableDisplayerLabel'
            cdm.append({'cls': cls, 'attributes': kwargs})

        return cdm
