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
    from app import App
else:
    App, = jac_import('app', items={'App': None})
if typing.TYPE_CHECKING:
    from agents import Agents
else:
    Agents, = jac_import('agents', items={'Agents': None})
if typing.TYPE_CHECKING:
    from graph_walker import graph_walker
else:
    graph_walker, = jac_import('graph_walker', items={'graph_walker': None})

class agent_graph_walker(graph_walker, Walker):
    agent_id: str = field('')
    logger: static[Logger] = logging.getLogger(__name__)

    @with_entry
    def on_app(self, here: App) -> None:
        if not self.visit(here.refs().filter(Agents, None)):
            self.logger.error('App graph not initialized. Import an agent and try again.')

    @with_entry
    def on_agents(self, here: Agents) -> None:
        if self.agent_id:
            try:
                if (agent_node := jobj(id=self.agent_id)):
                    if agent_node.published:
                        self.visit(agent_node)
                else:
                    Jac.get_context().status = 400
                    Jac.report('Invalid agent id')
                    return self.disengage()
            except Exception as e:
                Jac.get_context().status = 400
                Jac.report('Invalid agent id')
                return self.disengage()