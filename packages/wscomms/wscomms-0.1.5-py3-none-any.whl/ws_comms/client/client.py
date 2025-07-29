# ====== Imports ======
# Standard Library Imports
import aiohttp
import asyncio

# Third-party library imports
from loggerplusplus import Logger

# Internal project imports
from ws_comms.client.client_route import WSclientRouteManager


# ====== Class Part ======
class WSclient:
    """
    This class is a client that can connect to a websocket server.
    * This client can connect to multiple routes.
    * It can also run background tasks in parallel with route listening.
    * It can send messages to the server.
    * It can receive messages from the server.
    """

    def __init__(
            self,
            host: str,
            port: int,
            logger: Logger = Logger(identifier="WSclient", follow_logger_manager_rules=True)
    ) -> None:
        self.logger: Logger = logger

        self.__host: str = host
        self.__port: int = port

        self.tasks: list[asyncio.coroutine] = []

        self.logger.info(f"Initialized with host: {self.__host}, port: {self.__port}")

    def __get_url(self, route: str) -> str:
        return f"ws://{self.__host}:{self.__port}{route}"

    async def __run_tasks(self) -> None:
        await asyncio.gather(*self.tasks)

    async def __route_handler_routine(self, route: str, handler: WSclientRouteManager):
        """
        This function is a coroutine that connects to a websocket server and binds a handler to it.
        It handles connection errors and try to reconnect to the server.
        :param route:
        :param handler:
        :return:
        """
        self.logger.info(f"WSclient [{route}] started, route url: [{self.__get_url(route)}]")
        while True:
            try:
                ws_url = f"{self.__get_url(route)}?sender={handler.sender.name}"
                self.logger.info(f"WSclient [{ws_url}] try to connect server...")

                async with aiohttp.ClientSession() as session:
                    async with session.ws_connect(ws_url) as ws:
                        self.logger.info(f"WSclient [{route}] connected !")
                        handler.set_ws(ws)
                        await handler.routine()

            except Exception as error:
                self.logger.error(f"WSclient [{route}] error: ({error}), try to reconnect...")
                await asyncio.sleep(0.5)  # Avoid to spam the server with connection requests

    def add_route_handler(
            self, route: str, route_manager: WSclientRouteManager
    ) -> None:
        """
        Add a new route to the client.
            - route is the path of url to bind to the handler.
            - route_manager is an object that manage the connection with the server. It establishes
            the connection with the server and allows to send and receive messages.
        :param route:
        :param route_manager:
        :return:
        """
        # Add the new routine to the client tasks list with its associated url
        self.tasks.append(self.__route_handler_routine(route, route_manager))

    def add_background_task(self, task: callable, *args, **kwargs) -> None:
        """
        Add a new background task to the client. It is useful to execute task in parallel with the client.
        * The task have to be a coroutine (async function).
        * The task will be created when the client will start.
        :param task:
        :return:
        """
        self.tasks.append(task(*args, **kwargs))

    def run(self) -> None:
        asyncio.run(self.__run_tasks())
