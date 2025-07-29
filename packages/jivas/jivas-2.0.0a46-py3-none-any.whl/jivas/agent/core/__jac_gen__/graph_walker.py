from __future__ import annotations
from jaclang import *
import typing
from enum import Enum, auto
if typing.TYPE_CHECKING:
    import logging
else:
    logging, = jac_import('logging', 'py')
if typing.TYPE_CHECKING:
    import traceback
else:
    traceback, = jac_import('traceback', 'py')
if typing.TYPE_CHECKING:
    from logging import Logger
else:
    Logger, = jac_import('logging', 'py', items={'Logger': None})
if typing.TYPE_CHECKING:
    from jivas.agent.modules.agentlib.utils import Utils
else:
    Utils, = jac_import('jivas.agent.modules.agentlib.utils', 'py', items={'Utils': None})
if typing.TYPE_CHECKING:
    from app import App
else:
    App, = jac_import('app', items={'App': None})

class graph_walker(Walker):
    reporting: bool = field(True)
    logger: static[Logger] = logging.getLogger(__name__)

    class __specs__(Obj):
        private: static[bool] = True

    @with_entry
    def on_root(self, here: Root) -> None:
        if not self.visit(here.refs().filter(App, None)):
            self.logger.error('App graph not initialized. Import an agent and try again.')

    def export(self, ignore_keys: list=JacList(['__jac__'])) -> None:
        node_export = Utils.export_to_dict(self, ignore_keys)
        return node_export

    def update(self, data: dict={}) -> graph_walker:
        if data:
            for attr in data.keys():
                if hasattr(self, attr):
                    self.attr = data[attr]
        self.post_update()
        return self

    def post_update(self) -> None:
        pass