import abc
from collections.abc import Callable
import typing
from typing import ClassVar
from functools import wraps

import dearpygui.dearpygui as dpg  # type: ignore
from dpgmagictag.magictag import MagicTag

from dpgcontainers.exceptions import UnrenderedException


CONFIGURE_ITEM_KEYS = (
    'callback', 'drag_callback', 'drop_callback', 'enabled', 'filter_key',
    'height', 'indent', 'label', 'payload_type', 'show', 'source',
    'track_offset', 'tracked', 'use_internal_label', 'user_data', 'width',
)


def is_rendered(instance: 'DPGContainersBase'):
    return hasattr(instance, 'id_')

def assert_rendered(method) -> Callable:
    @wraps(method)
    def _inner(*args, **kwargs):
        if not is_rendered(args[0]):
            raise UnrenderedException()
        return method(*args, **kwargs)
    return _inner


class DPGContainersBase(abc.ABC):
    dpg_function_name: ClassVar[str]
    dpg_arguments: ClassVar[tuple[str, ...]]
    dpg_function_cache: ClassVar[Callable | None] = None
    dpg_value_cast: ClassVar[type | None] = None
    rendered_by_id: ClassVar[dict[int, 'DPGContainersBase']] = dict()

    @property
    def dpg_function(self):
        if self.dpg_function_cache is None:
            self.dpg_function_cache = getattr(dpg, self.dpg_function_name)
        return self.dpg_function_cache

    @property
    def children(self) -> list['DPGContainersBase']:
        if not hasattr(self, '_children'):
            self._children: list[DPGContainersBase] = []
        return self._children

    @property
    def tagged_entities(self) -> dict[str, typing.Self]:
        if not hasattr(self, '_tagged_entities'):
            self._tagged_entities: dict[str, typing.Self] = {}
            if hasattr(self, 'tag') and self.tag:
                self._tagged_entities[self.tag] = self
        return self._tagged_entities

    @property
    def named_child_indexes(self) -> dict[str, int]:
        if not hasattr(self, '_named_child_indexes'):
            self._named_child_indexes: dict[str, int] = {}
        return self._named_child_indexes

    def __call__(self, *children, **named_children):
        self.children.extend(children)
        if named_children:
            named_indexes = range(len(self.children), len(self.children)+len(named_children))
            self.children.extend(named_children.values())
            self.named_child_indexes.update(zip(named_children, named_indexes))
        for child in self.children:
            self.tagged_entities.update(child.tagged_entities)
        return self

    def render(self, parent: int|str|None = None, tag_prefix: MagicTag | None = None):
        if not hasattr(self, 'id_'):
            dpg_kwargs = {
                arg: getattr(self, arg)
                for arg in self.dpg_arguments
            }
            if parent is not None:
                dpg_kwargs['parent'] = parent
            if tag_prefix is not None:
                if dpg_kwargs['tag'] != 0:
                    dpg_kwargs['tag'] = tag_prefix / dpg_kwargs['tag']
            id_ = self.dpg_function(**dpg_kwargs)
            self.id_ = id_
            self.rendered_by_id[id_] = self

        for child in self.children:
            child.render(parent=self.id_, tag_prefix=tag_prefix)

        return self

    @assert_rendered
    def delete(self):
        dpg.delete_item(self.id_)

    @property
    @assert_rendered
    def configuration(self):
        return dpg.get_item_configuration(self.id_)

    @property
    def value(self):
        return dpg.get_value(self.id_)

    @value.setter
    def value(self, value):
        if self.dpg_value_cast is not None:
            value = self.dpg_value_cast(value)
        dpg.set_value(self.id_, value)

    @assert_rendered
    def configure(self, **kwargs):
        dpg.configure_item(self.id_, **kwargs)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if is_rendered(self):
            if key in CONFIGURE_ITEM_KEYS:
                kwargs = {key: value}
                dpg.configure_item(self.id_, **kwargs)

    @assert_rendered
    def __enter__(self):
        dpg.push_container_stack(self.id_)

    def __exit__(self, exc_type, exc_value, traceback):
        dpg.pop_container_stack()
