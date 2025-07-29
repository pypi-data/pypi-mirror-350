from __future__ import annotations
from jaclang import *
import typing
from enum import Enum, auto
if typing.TYPE_CHECKING:
    from typing import Optional
else:
    Optional, = jac_import('typing', 'py', items={'Optional': None})
if typing.TYPE_CHECKING:
    from jivas.agent.memory.memory_walker import memory_walker
else:
    memory_walker, = jac_import('jivas.agent.memory.memory_walker', items={'memory_walker': None})
if typing.TYPE_CHECKING:
    from jivas.agent.memory.memory import Memory
else:
    Memory, = jac_import('jivas.agent.memory.memory', items={'Memory': None})

class delete_frame(memory_walker, Walker):
    session_id: str = field('')

    class __specs__(Obj):
        private: static[bool] = False

    @with_entry
    def on_memory(self, here: Memory) -> None:
        if not self.session_id:
            Jac.get_context().status = 400
            Jac.report('missing session_id')
            return
        deleted_nodes = here.purge(self.session_id)
        if not deleted_nodes:
            Jac.get_context().status = 500
            Jac.report(f'unable to delete frame with session_id {self.session_id}')
            return
        Jac.report(deleted_nodes)