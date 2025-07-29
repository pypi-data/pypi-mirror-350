from __future__ import annotations
from jaclang import *
import typing
from enum import Enum, auto
if typing.TYPE_CHECKING:
    import os
else:
    os, = jac_import('os', 'py')
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
    from datetime import datetime, timedelta
else:
    datetime, timedelta = jac_import('datetime', 'py', items={'datetime': None, 'timedelta': None})
if typing.TYPE_CHECKING:
    from jivas.agent.core.agent_graph_walker import agent_graph_walker
else:
    agent_graph_walker, = jac_import('jivas.agent.core.agent_graph_walker', items={'agent_graph_walker': None})
if typing.TYPE_CHECKING:
    from jivas.agent.core.agent import Agent
else:
    Agent, = jac_import('jivas.agent.core.agent', items={'Agent': None})
if typing.TYPE_CHECKING:
    from jac_cloud.core.architype import NodeAnchor
else:
    NodeAnchor, = jac_import('jac_cloud.core.architype', 'py', items={'NodeAnchor': None})

class get_users_by_date(agent_graph_walker, Walker):
    start_date: str = field('')
    end_date: str = field('')
    timezone: str = field('UTC')
    logger: static[Logger] = logging.getLogger(__name__)

    class __specs__(Obj):
        private: static[bool] = False

    @with_entry
    def on_agent(self, here: Agent) -> None:
        start = datetime.strptime(f'{self.start_date}T00:00:00+00:00', '%Y-%m-%dT%H:%M:%S%z')
        end = datetime.strptime(f'{self.end_date}T00:00:00+00:00', '%Y-%m-%dT%H:%M:%S%z')
        end = end + timedelta(days=1) - timedelta(milliseconds=1)
        days = 1 if (end - start).days == 0 else (end - start).days
        try:
            collection = NodeAnchor.Collection.get_collection('interactions')
            pipeline = JacList([{'$match': {'agent_id': self.agent_id, 'time_stamp': {'$gte': self.start_date, '$lte': self.end_date}}}, {'$group': {'_id': {'$dateToString': {'format': '%Y-%m-%dT00:00:00.000Z' if days > 1 else '%Y-%m-%dT%H:00:00.000Z', 'date': {'$dateFromString': {'dateString': '$time_stamp'}}, 'timezone': self.timezone}}, 'unique_users': {'$addToSet': '$response.session_id'}}}, {'$project': {'_id': 0, 'date': '$_id', 'count': {'$size': '$unique_users'}}}, {'$sort': {'date': 1}}])
            result = list(collection.aggregate(pipeline))
            total = sum(JacList([doc['count'] for doc in result]))
            Jac.report({'total': total, 'data': result})
        except Exception as e:
            self.logger.error(f'an exception occurred, {traceback.format_exc()}')