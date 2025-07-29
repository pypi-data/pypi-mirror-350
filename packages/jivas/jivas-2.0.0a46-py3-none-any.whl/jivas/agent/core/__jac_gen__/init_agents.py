from __future__ import annotations
from jaclang import *
import typing
from enum import Enum, auto
if typing.TYPE_CHECKING:
    import os
else:
    os, = jac_import('os', 'py')
if typing.TYPE_CHECKING:
    import yaml
else:
    yaml, = jac_import('yaml', 'py')
if typing.TYPE_CHECKING:
    import io
else:
    io, = jac_import('io', 'py')
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
    from agents import Agents
else:
    Agents, = jac_import('agents', items={'Agents': None})
if typing.TYPE_CHECKING:
    from agent_graph_walker import agent_graph_walker
else:
    agent_graph_walker, = jac_import('agent_graph_walker', items={'agent_graph_walker': None})
if typing.TYPE_CHECKING:
    from import_agent import import_agent
else:
    import_agent, = jac_import('import_agent', items={'import_agent': None})
if typing.TYPE_CHECKING:
    from jivas.agent.modules.agentlib.utils import Utils, jvdata_file_interface
else:
    Utils, jvdata_file_interface = jac_import('jivas.agent.modules.agentlib.utils', 'py', items={'Utils': None, 'jvdata_file_interface': None})

class init_agents(agent_graph_walker, Walker):
    reporting: bool = field(False)
    logger: static[Logger] = logging.getLogger(__name__)

    class __specs__(Obj):
        private: static[bool] = False
        excluded: static[list] = JacList(['agent_id'])

    @with_entry
    def on_agents(self, here: Agents) -> None:
        if (agent_nodes := here.get_all()):
            for agent_node in agent_nodes:
                try:
                    self.logger.info(f'initializing agent {agent_node.name}')
                    file_bytes = agent_node.get_file(agent_node.descriptor) or jvdata_file_interface.get_file(agent_node.descriptor)
                    if not file_bytes:
                        self.logger.error(f'agent descriptor not found: {agent_node.descriptor}')
                        continue
                    descriptor = ''
                    file = io.BytesIO(file_bytes)
                    descriptor = yaml.safe_load(file)
                    if descriptor:
                        here.spawn(import_agent(descriptor=descriptor, reporting=self.reporting))
                except Exception as e:
                    self.logger.error(f'an exception occurred, {traceback.format_exc()}')