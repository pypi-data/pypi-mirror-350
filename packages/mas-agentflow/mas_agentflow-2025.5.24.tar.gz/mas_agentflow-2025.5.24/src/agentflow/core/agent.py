import inspect
from logging import Logger
import queue
import threading
import time 
from typing import final
import uuid

from agentflow.core.parcel import Parcel

from agentflow.broker import BrokerType
from agentflow.broker.notifier import BrokerNotifier
from agentflow.broker.broker_maker import BrokerMaker
from agentflow.core import config
from agentflow.core.config import EventHandler
from agentflow.core.agent_worker import Worker, ProcessWorker, ThreadWorker


logger:Logger = __import__('agentflow').get_logger()



class Agent(BrokerNotifier):
    def __init__(self, name:str, agent_config:dict={}):
        logger.debug(f'name: {name}, agent_config: {agent_config}')
        
        self.agent_id = str(uuid.uuid4()).replace("-", "")
        logger.debug(f'agent_id: {self.agent_id}')
        self.__init_config(agent_config)
        self.name = name
        self.tag = f'{self.agent_id[:4]}'
        self.name_tag = f'{name}:{self.tag}'
        # self.parent_name = name.rsplit('.', 1)[0] if '.' in name else None
        self.parent_name = name.split('.', 1)[1] if '.' in name else None
        self.interval_seconds = 0
        self.__agent_worker: Worker = None
        
        self._children: dict = {}
        self._parents: dict = {}
        
        self._message_broker = None
        self.__topic_handlers: dict[str, function] = {}
        

# ==================
#  Agent Initializing
# ==================
        
    def __init_config(self, agent_config):
        self.config = config.default_config.copy()
        self.config.update(agent_config)
        logger.debug(f'self.config: {self.config}')
            
            
    def __create_worker(self):
        if 'process' == self.config[config.CONCURRENCY_TYPE]:
            return ProcessWorker(self)
        else:
            return ThreadWorker(self)
        
        
    def _get_worker(self):
        if not self.__agent_worker:
            self.__agent_worker = self.__create_worker()
        return self.__agent_worker


    def start(self):
        if not config.CONCURRENCY_TYPE in self.config:
            self.config[config.CONCURRENCY_TYPE] = 'process'
        logger.info(self.M(f"self.config: {self.config}"))
        self.work_process = self._get_worker().start()
        
        self._on_start()
        
        
    def _on_start(self):
        pass
        
        
    def start_process(self):
        self.config[config.CONCURRENCY_TYPE] = 'process'
        self.start()
        
        
    def start_thread(self):
        self.config[config.CONCURRENCY_TYPE] = 'thread'
        self.start()


    def terminate(self):
        logger.info(self.M(f"self.__agent_worker: {self.__agent_worker}"))
        
        if self.__agent_worker:
            self.__agent_worker.stop()
        else:
            logger.warning(self.M(f"The agent might not have started yet."))



# ==================
#  Agent Activating
# ==================
    def get_config(self, key:str, default=None):
        return self.config.get(key, default)
        
    
    def set_config(self, key:str, value):
        self.config[key] = value
        
    
    def get_config2(self, key:str, key2:str, default=None):
        return self.config[key].get(key2, default)
        
    
    def set_config2(self, key:str, key2:str, value):
        self.config[key][key2] = value


    def is_active(self):
        return self.__agent_worker.is_working()
    
    
    def on_activate(self):
        pass


    def on_terminating(self):
        pass


    def on_terminated(self):
        pass


    def on_begining(self):
        pass


    def on_began(self):
        pass


    def on_interval(self):
        pass
        
        
    def start_interval_loop(self, interval_seconds):
        logger.debug(f"{self.agent_id}> Start interval loop.")
        self.interval_seconds = interval_seconds

        def interval_loop():
            while self.is_active() and self.interval_seconds > 0:
                self.on_interval()
                time.sleep(self.interval_seconds)
            self.interval_seconds = 0
        threading.Thread(target=interval_loop).start()
        
        
    def stop_interval_loop(self):
        self.interval_seconds = 0


    def __activating(self):
        self.__data = {}
        self.__data_lock = threading.Lock()
        self.__connected_event = threading.Event()

        self.on_begining()

        # Create broker with retry
        broker_config_all = self.get_config("broker", {'broker_type': BrokerType.Empty})
        logger.debug(self.M(f"broker_config_all: {broker_config_all}"))
        broker_name = broker_config_all['broker_name']
        broker_config = broker_config_all[broker_name]
        
        retry_count = 0
        max_retries = 1  # 可根據需求調整或設為 None 表示無限重試
        retry_interval = 5  # 每次重試間隔秒數

        is_success = False
        while not is_success and (max_retries is None or retry_count < max_retries):
            try:
                logger.debug(self.M("Creating broker..."))
                self._broker = BrokerMaker().create_broker(
                    BrokerType(broker_config['broker_type'].lower()), self)
                logger.debug(self.M("Ready to start broker.."))
                self._broker.start(options=broker_config)
                is_success = True
            except ConnectionRefusedError as e:
                logger.error(self.M(f"Broker startup failed (ConnectionRefusedError). Retrying...\n{e}"))
            except Exception as e:
                logger.error(self.M(f"Broker startup failed. Retrying...\n{e}"))

            if not is_success:
                logger.debug(self.M("Waiting for retry..."))
                retry_count += 1
                for _ in range(retry_interval):
                    if self.__terminate_event.is_set():
                        return False
                    time.sleep(1)

        if is_success:
            self.__connected_event.wait()
            logger.info(self.M("Broker started successfully."))
        else:
            logger.error(self.M(f"Broker startup failed after {max_retries} retries."))

        return is_success


    def _activate(self, config):
        self.config = config
        self.__terminate_event = threading.Event()

        if self.__activating():
            logger.verbose(self.M('__activating'))
            sig = inspect.signature(self.on_activate)
            if len(sig.parameters) == 0:
                logger.verbose(self.M("Invoke on_activate 1"))
                self.on_activate()
            elif isinstance(sig.parameters.get('self'), Agent):
                logger.verbose(self.M("Invoke on_activate 2"))
                self.on_activate(self)
            else:
                logger.verbose(self.M("Invoke on_activate 3"))
                self.on_activate(self.config)

            # Waiting for termination.
            logger.info(self.M("Running.."))
            work_queue = config['work_queue']
            while not self.__terminate_event.is_set():
                try:
                    data = work_queue.get(timeout=1)
                    self._on_worker_data(data)
                except queue.Empty:
                    continue
                except KeyboardInterrupt:
                    self._terminate()
        else:
            self.__terminate_event.set()

        self.__deactivating()
        
        
    def _on_worker_data(self, data):
        logger.info(self.M(data))
        if 'terminate' == data:
            self._terminate()
            
            
    def _terminate(self):
        logger.warning(self.M('Terminating..'))
        
        self._notify_children('terminate')
        def stop():
            time.sleep(1)
            self.__terminate_event.set()
        threading.Thread(target=stop).start()          


    def __deactivating(self):        
        logger.verbose(f"begin")
        self.on_terminating()
            
        self._broker.stop()
        
        self.on_terminated()
        logger.verbose(f"end")
        

# ============
#  Agent Data 
# ============
    @final
    def get_data(self, key:str):
        return self.__data.get(key)


    @final
    def pop_data(self, key:str):
        data = None
        self.__data_lock.acquire()
        if key in self.__data:
            data = self.__data.pop(key)
        self.__data_lock.release()
        return data


    @final
    def put_data(self, key:str, data):
        self.__data.acquire()
        self.__data[key] = data
        self.__data.release()


# =====================
#  Publish / Subscribe
# =====================
    class DataEvent:
        def __init__(self, event):
            self.event = event
            self.data = None



    @final
    def publish(self, topic, data=None):
        # logger.verbose(self.M(f"topic: {topic}, data: {data}"))
        
        pcl = data if isinstance(data, Parcel) else Parcel.from_content(data)      
        logger.verbose(self.M(f"topic: {topic}, pcl: {str(pcl)[:400]}.."))   
        try:
            self._broker.publish(topic, pcl.payload())
        except Exception as ex:
            logger.exception(ex)

        
    def __generate_return_topic(self, topic):
        return f'{self.tag}-{int(time.time()*1000)}/{topic}'


    @final
    def publish_sync(self, topic, data=None, topic_wait=None, timeout=30)->Parcel:
        logger.verbose(self.M(f"topic: {topic}, data: {str(data)[:200]}.., topic_wait: {topic_wait}"))

        if isinstance(data, Parcel):
            pcl = data
            if pcl.topic_return:
                if topic_wait:
                    logger.warning(f"The passed parameter topic_wait: {topic_wait} has been replaced with '{pcl.topic_return}'.")
            elif topic_wait:
                pcl.topic_return = topic_wait
            else:
                pcl.topic_return = self.__generate_return_topic(topic)
        else:
            pcl = Parcel.from_content(data)
            pcl.topic_return = topic_wait if topic_wait else self.__generate_return_topic(topic)

        data_event = Agent.DataEvent(self._get_worker().create_event())

        def handle_response(topic_resp, pcl_resp:Parcel):
            # logger.verbose(self.M(f"topic_resp: {topic_resp}, data_resp: {str(pcl_resp)[:400]}.."))
            data_event.data = pcl_resp
            data_event.event.set()

        self.subscribe(pcl.topic_return, topic_handler=handle_response)
        self.publish(topic, pcl)

        logger.verbose(self.M(f"Waitting for event: {data_event}"))
        if data_event.event.wait(timeout):
            logger.verbose(self.M(f"Waitted the event: {data_event}, event.data: {str(data_event.data)[:400]}.."))
            return data_event.data
        else:
            raise TimeoutError(f"No response received within timeout period for topic: {pcl.topic_return}.")


    @final
    def subscribe(self, topic, data_type:str="str", topic_handler=None):
        logger.debug(self.M(f"topic: {topic}, data_type:{data_type}"))
        
        if not isinstance(data_type, str):
            raise TypeError(f"Expected data_type to be of type 'str', but got {type(data_type).__name__}. The subscribtion of topic '{topic}' is failed.")
        
        if topic_handler:
            if topic in self.__topic_handlers:
                logger.warning(self.M(f"Exist the handler for topic: {topic}"))
            self.__topic_handlers[topic] = topic_handler

        return self._broker.subscribe(topic, data_type)
    
    
    def __register_child(self, child_id:str, child_info:dict):
        child_info['parent_id'] = self.agent_id
        self._children[child_id] = child_info
        logger.info(self.M(f"Add a child: {child_id}, total: {len(self._children)}"))
        self.on_register_child(child_id, child_info)


    def on_register_child(self, child_id, child_info:dict):
        logger.verbose(f"child_id: {child_id}, child_info: {child_info}")
    
    
    def __register_parent(self, parent_id:str, parent_info):
        parent_info['child_id'] = self.agent_id
        self._parents[parent_id] = parent_info
        logger.info(self.M(f"Add a parent: {parent_id}, total: {len(self._parents)}"))
        self.on_register_parent(parent_id, parent_info)


    def on_register_parent(self, parent_id, parent_info):
        logger.verbose(f"parent_id: {parent_id}, parent_info: {parent_info}")
    
    
    def _handle_children(self, topic, pcl:Parcel):
        child = pcl.content
        logger.debug(f"topic: {topic}, child: {child}")
        # {
        #     'child_id': agent_id,
        #     'child_name': child.name,
        #     'subject': subject,
        #     'data': data,
        #     'target_parents': [parent_id, ..] # optional
        # }
        
        if target_parents := child.get('target_parents'):
            if self.agent_id not in target_parents:
                return
        child_id = child.get('child_id')

        if "register_child" == child['subject']:
            self.__register_child(child_id, child)
            self._notify_child(child_id, 'register_parent')
            
        return self.on_children_message(topic, child)


    def on_children_message(self, topic, info):
        logger.verbose(f"topic: {topic}, info: {info}")
    
    
    def _handle_parents(self, topic, pcl:Parcel):
        parent = pcl.content
        logger.debug(self.M(f"topic: {topic}, data type: {type(parent)}, data: {parent}"))
        # {
        #     'parent_id': agent_id,
        #     'subject': subject,
        #     'data': data,
        #     'target_children': [child_id, ..]
        # }
        
        if target_children := parent.get('target_children'):
            if not self.agent_id in target_children:
                return  # Not in the target children.
        
        if "terminate" == parent['subject']:
            self._terminate()
        elif "register_parent" == parent['subject']:
            self.__register_parent(parent.get('parent_id'), parent)
            
        return self.on_parents_message(topic, parent)


    def on_parents_message(self, topic, parent):
        logger.verbose(f"topic: {topic}, parent: {parent}")
    
    
    def _notify_child(self, child_id, subject, data=None):
        logger.debug(f"child_id: {child_id}, subject: {subject}, data: {data}")

        if self._children and child_id in self._children:
            self.publish(f'{child_id}.to_child.{self.name}', {
                'parent_id': self.agent_id,
                'subject': subject,
                'data': data
            })
        else:
            logger.error("The child does not exist.")
    
    
    def _notify_children(self, subject, data=None, target_children=None, target_child_name=None):
        logger.debug(self.M(f"subject: {subject}, data: {data}"))
        
        if not self._children:
            logger.verbose(self.M('No child.'))
            return
        
        topic = f'to_child.{self.name}'
        data_send = {
            'parent_id': self.agent_id,
            'subject': subject,
            'data': data,
            }

        if target_children:
            logger.debug(self.M(f"target_children: {target_children}"))
            data_send['target_children'] = target_children
        
        if target_child_name:
            logger.debug(self.M(f"target_child_name: {target_child_name}"))
            topic = f'to_child.{target_child_name}'

        self.publish(topic, data_send)
    
    
    def _notify_parent(self, parent_id, subject, data=None):
        logger.debug(self.M(f"parent_id: {parent_id}, subject: {subject}, data: {data}"))

        if self._parents and parent_id in self._parents:
            self.publish(f'{parent_id}.to_parent.{self.parent_name}', {
                'child_id': self.agent_id,
                'subject': subject,
                'data': data
            })
        else:
            logger.error("The parent does not exist.")
    
    
    def _notify_parents(self, subject, data=None, target_parents=None):
        logger.debug(f"subject: {subject}, data: {data}")
        
        if self.parent_name:
            self.publish(f'to_parent.{self.parent_name}', data={
                'child_id': self.agent_id,
                'child_name': self.name,
                'subject': subject,
                'data': data,
                'target_parents': target_parents
            })
        else:
            logger.error(f"No any parent.")
        
        
    def _on_connect(self):
        for event in EventHandler:
            attr_name = str(event).lower()[len('EventHandler.'):]
            setattr(self, attr_name, self.get_config(event, getattr(self, attr_name, None)))

        self.subscribe(f'to_parent.{self.name}', topic_handler=self._handle_children)  # All the parents were notified by the children.
        self.subscribe(f'{self.agent_id}.to_parent.{self.name}', topic_handler=self._handle_children)  # I was the only parent notified by a child.  
        
        # logger.verbose(f"self.parent_name: {self.parent_name}")
        if self.parent_name:
            self.subscribe(f'to_child.{self.parent_name}', topic_handler=self._handle_parents) # All the children were notified by the parents.
            self.subscribe(f'to_child.{self.name}', topic_handler=self._handle_parents)    # All the children with the same name were notified by the parents.
            self.subscribe(f'{self.agent_id}.to_child.{self.parent_name}', topic_handler=self._handle_parents)    # Only this child notified by a parent.
            self._notify_parents("register_child")

        def handle_connected():
            time.sleep(1)
            self.__connected_event.set()
            self.on_connected()
        threading.Thread(target=handle_connected).start()
        # try:
        #     self.on_connected()
        # except Exception as ex:
        #     logger.exception(ex)


    @final
    def _on_message(self, topic:str, data):
        logger.verbose(self.M(f"topic: {topic}, data: {data[:200]}.."))
        pcl = Parcel.from_payload(data)
        # logger.verbose(self.M(f"managed_data: {str(pcl.managed_data)[:200]}.."))

        topic_handler = self.__topic_handlers.get(topic, self.on_message)
        logger.verbose(self.M(f"Invoke handler: {topic_handler}"))
        
        def handle_message(topic_handler, topic, p:Parcel):
            if p.topic_return:
                try:
                    data_resp = topic_handler(topic, p)
                except Exception as ex:
                    logger.exception(ex)
                    p.error = str(ex)
                    p.content = None
                    data_resp = p
                    logger.debug(data_resp)
                finally:
                    self.publish(pcl.topic_return, data_resp)
            else:
                try:
                    topic_handler(topic, p)
                except Exception as ex:
                    logger.exception(ex)
                
        threading.Thread(target=handle_message, args=(topic_handler, topic, pcl)).start()
        # def handle_message(topic_handler, topic, content):
        #     data_resp = topic_handler(topic, content)
        #     if pcl.topic_return:
        #         self._publish(pcl.topic_return, data_resp)
        # threading.Thread(target=handle_message, args=(topic_handler, topic, pcl.content)).start()


    def on_connected(self):
        logger.debug(self.M('on_connected'))


    def on_message(self, topic:str, data):
        pass
        
        
    def M(self, message=None):
        return f'{self.name_tag} {message}' if message else self.name_tag
            
