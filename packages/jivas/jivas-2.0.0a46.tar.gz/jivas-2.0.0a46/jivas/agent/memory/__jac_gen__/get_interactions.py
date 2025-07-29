from __future__ import annotations
from jaclang import *
import typing
from enum import Enum, auto
if typing.TYPE_CHECKING:
    from jivas.agent.memory.memory_walker import memory_walker
else:
    memory_walker, = jac_import('jivas.agent.memory.memory_walker', items={'memory_walker': None})
if typing.TYPE_CHECKING:
    from jivas.agent.memory.interaction import Interaction
else:
    Interaction, = jac_import('jivas.agent.memory.interaction', items={'Interaction': None})
if typing.TYPE_CHECKING:
    from jivas.agent.memory.advance import Advance
else:
    Advance, = jac_import('jivas.agent.memory.advance', items={'Advance': None})
if typing.TYPE_CHECKING:
    from jivas.agent.memory.memory import Memory
else:
    Memory, = jac_import('jivas.agent.memory.memory', items={'Memory': None})
if typing.TYPE_CHECKING:
    from jivas.agent.memory.frame import Frame
else:
    Frame, = jac_import('jivas.agent.memory.frame', items={'Frame': None})

class get_interactions(memory_walker, Walker):
    session_id: str = field('')

    class __specs__(Obj):
        private: static[bool] = False

    @with_entry
    def on_memory(self, here: Memory) -> None:
        if self.session_id:
            self.visit(here.refs().filter(Frame, None).filter(None, lambda item: item.session_id == self.session_id))
        else:
            self.visit(here.refs().filter(Frame, None))

    @with_entry
    def on_frame(self, here: Frame) -> None:
        self.visit(here.refs(Advance).filter(Interaction, None))

    @with_entry
    def on_interaction(self, here: Interaction) -> None:
        Jac.report(here.export())
        self.visit(here.refs(Advance).filter(Interaction, None))