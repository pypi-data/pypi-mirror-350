# ====== Imports ======
# Standard Library Imports
import asyncio
import aiohttp

# Third-party library imports
from loggerplusplus import Logger

# Internal project imports
from ws_comms.message import WSmsg


# ====== Class Part ======
class WSreceiver:
    """
    This class is used to receive messages from the server.
    It has a routine which listen every incoming message from its associated route.
    It stores them a queue or just save the last state.
    * It only manipulates WSmsg objects (not WSMessage).
    * It is completely dedicated to work with the determined message format.
    """

    def __init__(
            self,
            use_queue: bool = False,
            keep_memory: bool = False,
            logger: Logger = Logger(identifier="WSreceiver", follow_logger_manager_rules=True),
    ) -> None:
        self.logger: Logger = logger

        self.use_queue: bool = use_queue
        self.keep_memory: bool = keep_memory

        self.queue: asyncio.Queue = asyncio.Queue()
        self.last_state: WSmsg = WSmsg()  # Set a default WSmsg object as default value
        self.logger.info(f"Initialized: use_queue: {self.use_queue}, keep_memory: {self.keep_memory}")

    async def routine(self, msg: aiohttp.WSMessage) -> None:
        """
        Coroutine to read received messages and add them in queues (one for each task).
        """
        retyped_msg = WSmsg.from_aiohttp_message(msg)

        if self.use_queue:
            await self.queue.put(retyped_msg)

        if not self.use_queue or self.keep_memory:
            self.last_state = retyped_msg

        self.logger.info(f"New message received: {retyped_msg}")

    async def get(self, skip_queue: bool = False, wait_msg: bool = False) -> WSmsg:
        """
        Get state received. This method allows to skip_queue (get directly the last received state) / to wait_msg
        if the queue is empty, it will wait a new message and return it / to keep_memory if this option is True,
        this methode will save the last_state and return it on ask. If it's False, when a value is get, it will be deleted
        (next value is Empty WSmsg).
        :param skip_queue:
        :param wait_msg:
        :return:
        """
        if self.use_queue and not skip_queue:
            if wait_msg:
                self.logger.debug("Waiting for a new message...")
                return await self.queue.get()
            elif not self.queue.empty():
                self.logger.debug("The queue is not empty, getting the older message available...")
                return await self.queue.get()
        if self.keep_memory:
            self.logger.debug("The keep_memory is enable, getting the last saved message...")
            return self.last_state

        state = self.last_state
        self.last_state = WSmsg()
        self.logger.debug("keep_memory and use_queue are not enabled, getting the last state and reset it.")
        return state

    def get_queue_size(self) -> int:
        """
        Get the size of the queue. Return 0 if the queue is not used.
        :return:
        """
        if self.use_queue:
            return self.queue.qsize()
        return 0
