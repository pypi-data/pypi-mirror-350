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
    from agent_graph_walker import agent_graph_walker
else:
    agent_graph_walker, = jac_import('agent_graph_walker', items={'agent_graph_walker': None})
if typing.TYPE_CHECKING:
    from jivas.agent.core.agent import Agent
else:
    Agent, = jac_import('jivas.agent.core.agent', items={'Agent': None})

class update_agent(agent_graph_walker, Walker):
    agent_data: dict = field(gen=lambda: {})
    with_actions: bool = field(False)
    reporting: bool = field(True)
    logger: static[Logger] = logging.getLogger(__name__)

    class __specs__(Obj):
        private: static[bool] = False

    @with_entry
    def on_agent(self, here: Agent) -> None:
        if (agent_node := here.update(data=self.agent_data, with_actions=self.with_actions)):
            if agent_node:
                if self.reporting:
                    Jac.report(agent_node.get_descriptor())
            else:
                self.logger.error('unable to update agent')
                if self.reporting:
                    Jac.get_context().status = 500
                    Jac.report('unable to update agent')