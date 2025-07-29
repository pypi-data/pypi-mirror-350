import functools
import os
from collections.abc import Iterator
from enum import Enum

import grpc
from openobd_protocol.Communication import CommunicationServices_pb2_grpc as grpcCommunicationService
from openobd_protocol.Communication.Messages import Isotp_pb2 as grpcIsotp
from openobd_protocol.Communication.Messages import Kline_pb2 as grpcKline
from openobd_protocol.Communication.Messages import Raw_pb2 as grpcRaw
from openobd_protocol.Communication.Messages import Terminal15_pb2 as grpcTerminal15
from openobd_protocol.Configuration import ConfigurationServices_pb2_grpc as grpcConfigurationService
from openobd_protocol.Configuration.Messages import BusConfiguration_pb2 as grpcBusConfiguration
from openobd_protocol.ConnectionMonitor import ConnectionMonitorServices_pb2_grpc as grpcConnectionMonitorService
from openobd_protocol.ConnectionMonitor.Messages import ConnectorInformation_pb2 as grpcConnectionInformation
from openobd_protocol.Function import FunctionServices_pb2_grpc as grpcFunctionService
from openobd_protocol.Function.Messages import Function_pb2 as grpcFunction
from openobd_protocol.FunctionBroker import FunctionBrokerServices_pb2_grpc as grpcFunctionBrokerServices
from openobd_protocol.FunctionBroker.Messages import FunctionBroker_pb2 as grpcFunctionBroker
from openobd_protocol.Messages import Empty_pb2 as grpcEmpty
from openobd_protocol.Messages.Empty_pb2 import EmptyMessage
from openobd_protocol.Session import SessionServices_pb2_grpc as grpcService
from openobd_protocol.Session.Messages import ServiceResult_pb2 as grpcServiceResult
from openobd_protocol.Session.Messages import Session_pb2 as grpcSession
from openobd_protocol.SessionController import SessionControllerServices_pb2_grpc as grpcSessionControllerService
from openobd_protocol.SessionController.Messages import SessionController_pb2 as grpcSessionController
from openobd_protocol.UserInterface import UserInterfaceServices_pb2_grpc as grpcUserInterfaceService
from openobd_protocol.UserInterface.Messages import UserInterface_pb2 as grpcUserInterface

from ._token import Token
from .openobd_exceptions import OpenOBDException


def _get_value_from_kwargs_or_env(kwargs, kwarg_key, env_key):
    if kwarg_key in kwargs:
        return kwargs[kwarg_key]
        return kwargs[kwarg_key]
    elif env_key in os.environ:
        return os.environ[env_key]
    else:
        raise AssertionError(f"Argument \"{kwarg_key}\" could not be found. Pass it explicitly, or ensure it is available as an environment variable named \"{env_key}\".")


def raises_openobd_exceptions(func):
    """
    If the wrapped function raises a gRPC exception, it will be cast and raised as an OpenOBDException.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if isinstance(e, grpc.Call):
                # Encountered an exception raised by gRPC, so cast it to an OpenOBDException
                raise OpenOBDException(details=e.details(), status=e.code().value[0], status_description=e.code().value[1]) from None
            else:
                # The exception wasn't raised by gRPC, so just raise it as is
                raise e

    return wrapper


class GrpcChannel:

    grpc_host = None
    grpc_port = 443
    connected = False
    channel = None

    def _connect(self):
        if not self.connected:
            ''' Check if local grpc-proxy is running '''
            if self.grpc_port == 443:
                self.channel = grpc.secure_channel(self.grpc_host, grpc.ssl_channel_credentials())
            else:
                ''' NOTE: Only use this for development purposes '''
                self.channel = grpc.insecure_channel('{}:{}'.format(self.grpc_host, self.grpc_port))

            ''' TODO: Exceptions and stuff '''
            self.connected = True


class ContextVariableType(Enum):
    FUNCTION = 1
    GLOBAL = 2
    CONNECTION = 3


class OpenOBDSession(GrpcChannel):

    AUTH_TOKEN      = 1
    MONITOR_TOKEN   = 2
    SESSION_TOKEN   = 3

    def __init__(self, session_info: grpcSessionController.SessionInfo, grpc_port=443):
        """
        An object that represents an openOBD session. Can be used to make session-specific gRPC calls.

        :param session_info: a SessionInfo object received from a gRPC call.
        :param grpc_port: the default value of 443 should be used to make gRPC calls using SSL.
        """
        self.active = True
        self.session_info = session_info

        '''Initially the session context is not initialized (will be initialized when starting a new context)'''
        self.function_context = None    # type: grpcFunction.FunctionContext | None

        '''Initially the session token is the authentication token for the session'''
        self.session_token = self.session_info.authentication_token

        self.grpc_host = self.session_info.grpc_endpoint
        self.grpc_port = grpc_port
        self._connect()

        self.session = grpcService.sessionStub(self.channel)
        self.function = grpcFunctionService.functionStub(self.channel)
        self.config = grpcConfigurationService.configStub(self.channel)
        self.can = grpcCommunicationService.canStub(self.channel)
        self.kline = grpcCommunicationService.klineStub(self.channel)
        self.terminal15 = grpcCommunicationService.terminal15Stub(self.channel)
        self.ui = grpcUserInterfaceService.userInterfaceStub(self.channel)
        self.connector_monitor = grpcConnectionMonitorService.connectionMonitorStub(self.channel)

    def id(self):
        return self.session_info.id

    def _metadata(self, token=AUTH_TOKEN):
        bearer_token = ""
        if token == self.AUTH_TOKEN:
            bearer_token = self.session_token
        elif token == self.MONITOR_TOKEN:
            if self.function_context is not None:
                bearer_token = self.function_context.monitor_token
        elif token == self.SESSION_TOKEN:
            bearer_token = self.session_token

        '''Construct the metadata for the gRPC call'''
        metadata = []
        metadata.append(("authorization", "Bearer {}".format(bearer_token)))
        metadata = tuple(metadata)
        return metadata

    def update_session_token(self, session_token):
        """
        Replaces the session token used for gRPC calls.

        :param session_token: the new session token to use.
        """
        self.session_token = session_token

    @raises_openobd_exceptions
    def configure_bus(self, bus_configurations: Iterator[grpcBusConfiguration.BusConfiguration]) -> grpcEmpty.EmptyMessage:
        """
        Configures all given buses so that they can be used for communication. Overwrites any previous bus
        configurations.

        :param bus_configurations: BusConfiguration messages representing the buses that need to be configured.
        :return: an EmptyMessage, indicating that no problems occurred.
        """
        return self.config.configureBus(bus_configurations, metadata=self._metadata())

    @raises_openobd_exceptions
    def open_isotp_stream(self, isotp_messages: Iterator[grpcIsotp.IsotpMessage]) -> Iterator[grpcIsotp.IsotpMessage]:
        """
        Opens a bidirectional stream for ISO-TP communication with the channel specified in the given IsotpMessage.

        :param isotp_messages: each IsotpMessage that should be sent to the specified channel.
        :return: IsotpMessages sent by the specified channel.
        """
        return self.can.openIsotpStream(isotp_messages, metadata=self._metadata())

    @raises_openobd_exceptions
    def open_raw_stream(self, raw_frames: Iterator[grpcRaw.RawFrame]) -> Iterator[grpcRaw.RawFrame]:
        """
        Opens a bidirectional stream for raw frame communication with the channel specified in the given RawFrame.

        :param raw_frames: each RawFrame that should be sent to the specified channel.
        :return: RawFrames sent by the specified channel.
        """
        return self.can.openRawStream(raw_frames, metadata=self._metadata())

    @raises_openobd_exceptions
    def open_kline_stream(self, kline_messages: Iterator[grpcKline.KlineMessage]) -> Iterator[grpcKline.KlineMessage]:
        """
        Opens a bidirectional stream for K-Line communication with the channel specified in the given KlineMessage.

        :param kline_messages: each KlineMessage that should be sent to the specified channel.
        :return: KlineMessages sent by the specified channel.
        """
        return self.kline.openKlineStream(kline_messages, metadata=self._metadata())

    @raises_openobd_exceptions
    def open_terminal15_stream(self, empty_message: EmptyMessage) -> Iterator[grpcTerminal15.Terminal15Message]:
        """
        Opens a stream for Terminal15 communication .

        :return: Terminal15 messages sent by the remote.
        """
        return self.terminal15.openTerminal15Stream(empty_message, metadata=self._metadata())

    @raises_openobd_exceptions
    def open_control_stream(self, user_interface_messages: Iterator[grpcUserInterface.Control]) -> Iterator[grpcUserInterface.Control]:
        """
        Opens a stream that displays given Control messages to the customer or operator, and returns their response.

        :param user_interface_messages: Control messages that need to be displayed on the user interface.
        :return: Control messages containing the user's response, depending on which Control type was sent.
        """
        return self.ui.openControlStream(user_interface_messages, metadata=self._metadata())

    @raises_openobd_exceptions
    def get_connector_information(self, request: grpcEmpty.EmptyMessage | None = None) -> grpcConnectionInformation.ConnectorInformation:
        """
        Retrieves information on the current status of the connection with the connector.

        :return: a ConnectorInformation message containing the current status of the connection.
        """
        if request is None:
            request = grpcEmpty.EmptyMessage()
        return self.connector_monitor.getConnectorInformation(request=request, metadata=self._metadata())

    @raises_openobd_exceptions
    def open_connector_information_stream(self, request: grpcEmpty.EmptyMessage | None = None) -> Iterator[grpcConnectionInformation.ConnectorInformation]:
        """
        Opens a stream which receives a ConnectorInformation message each second, containing the status of the
        connection with the connector.

        :return: ConnectorInformation messages containing the current status of the connection.
        """
        if request is None:
            request = grpcEmpty.EmptyMessage()
        return self.connector_monitor.openConnectorInformationStream(request=request, metadata=self._metadata())

    @raises_openobd_exceptions
    def authenticate(self, request: grpcEmpty.EmptyMessage | None = None) -> grpcSession.SessionToken:
        """
        Authenticates a newly created session. This needs to be done once for each session and is required to make any
        other gRPC calls for this session.

        :return: a session token, valid for 5 minutes, which is required to make gRPC calls for this session.
        """
        if request is None:
            request = grpcEmpty.EmptyMessage()
        return self.session.authenticate(request=request, metadata=self._metadata())

    @raises_openobd_exceptions
    def open_session_token_stream(self, request: grpcEmpty.EmptyMessage | None = None) -> Iterator[grpcSession.SessionToken]:
        """
        Starts a stream which receives a new session token every 2 minutes, each of which is valid for 5 minutes. A
        valid session token is required to make gRPC calls.

        :return: session tokens required to keep the session valid.
        """
        if request is None:
            request = grpcEmpty.EmptyMessage()
        return self.session.openSessionTokenStream(request=request, metadata=self._metadata())

    @raises_openobd_exceptions
    def start_context(self, request: grpcEmpty.EmptyMessage | None = None) -> grpcFunction.FunctionContext:
        """
        Starts a new function context within the session. This creates a new context with its own isolated variables.

        :return: a session context, including a context uuid and context token, valid for 5 minutes
        """
        if request is None:
            request = grpcEmpty.EmptyMessage()
        function_context = self.function.startFunctionContext(request=request, metadata=self._metadata()) # type: grpcFunction.FunctionContext

        '''Update the session information, we are now running within a context'''
        self.function_context = function_context

        '''
        Update the authentication token for this session, so we could continue with this session when it is desired.
        But in most cases we want to pass on the updated session info to another openOBD function executor, while this
        proces is monitoring (using monitor tokens) when this execution is finished.
        '''
        self.session_token = function_context.authentication_token

        '''Update the session info, so it can be passed on to another openOBD executor'''
        self.session_info.authentication_token = function_context.authentication_token

        return function_context

    @raises_openobd_exceptions
    def set_context_variable(self, key: str, value, variable_type = ContextVariableType.FUNCTION) -> None:
        if variable_type == ContextVariableType.GLOBAL:
            mem_type = grpcFunction.ContextType.GLOBAL_CONTEXT
        elif variable_type == ContextVariableType.CONNECTION:
            mem_type = grpcFunction.ContextType.CONNECTION_CONTEXT
        else:
            mem_type = grpcFunction.ContextType.FUNCTION_CONTEXT

        if isinstance(value, str):
            self.function.setVariable(
                grpcFunction.Variable(memory=mem_type, key=key, value=value),
                metadata=self._metadata())
        else:
            self.function.setVariable(
                grpcFunction.Variable(memory=mem_type, key=key, object=value),
                metadata=self._metadata())

    @raises_openobd_exceptions
    def get_context_variable(self, key: str, variable_type = ContextVariableType.FUNCTION):
        if variable_type == ContextVariableType.GLOBAL:
            mem_type = grpcFunction.ContextType.GLOBAL_CONTEXT
        elif variable_type == ContextVariableType.CONNECTION:
            mem_type = grpcFunction.ContextType.CONNECTION_CONTEXT
        else:
            mem_type = grpcFunction.ContextType.FUNCTION_CONTEXT

        return self.function.getVariable(
            grpcFunction.Variable(memory=mem_type, key=key),
            metadata=self._metadata())

    @raises_openobd_exceptions
    def delete_context_variable(self, key: str, variable_type = ContextVariableType.FUNCTION):
        if variable_type == ContextVariableType.GLOBAL:
            mem_type = grpcFunction.ContextType.GLOBAL_CONTEXT
        elif variable_type == ContextVariableType.CONNECTION:
            mem_type = grpcFunction.ContextType.CONNECTION_CONTEXT
        else:
            mem_type = grpcFunction.ContextType.FUNCTION_CONTEXT

        return self.function.deleteVariable(
            grpcFunction.Variable(memory=mem_type, key=key),
            metadata=self._metadata())

    @raises_openobd_exceptions
    def set_function_argument(self, key: str, value):
        self.function.setFunctionArgument(
            grpcFunction.Variable(key=key, value=value),
            metadata=self._metadata())

    @raises_openobd_exceptions
    def set_function_result(self, key: str, value):
        self.function.setFunctionResult(
            grpcFunction.Variable(key=key, value=value),
            metadata=self._metadata())

    @raises_openobd_exceptions
    def monitor_function_context(self, request: grpcFunction.FunctionContext | None = None) -> Iterator[grpcFunction.FunctionContext]:
        """
        Starts a stream which receives a new monitor token every 2 minutes, each of which is valid for 5 minutes. A
        valid monitor token is required to keep monitoring the context until it finishes.

        :return: session context containing monitor tokens and eventually a new authentication token
        """
        if request is None:
            request = grpcFunction.FunctionContext()
        return self.function.monitorFunctionContext(request=request, metadata=self._metadata(token=OpenOBDSession.MONITOR_TOKEN))

    @raises_openobd_exceptions
    def register_function_details(self, function_details: grpcFunction.FunctionDetails | None = None) -> grpcEmpty.EmptyMessage:
        """
        Registers information about what function is running in the current context.

        :param function_details: a FunctionDetails message detailing what function is running in this context.
        :return: an EmptyMessage, indicating that no problems occurred.
        """
        return self.function.registerFunctionDetails(request=function_details, metadata=self._metadata())

    @raises_openobd_exceptions
    def get_function_details(self, request: grpcEmpty.EmptyMessage | None = None) -> grpcFunction.FunctionDetails:
        """
        Retrieves the function details that have been registered in the current context.

        :return: the current context's FunctionDetails.
        """
        if request is None:
            request = grpcEmpty.EmptyMessage()
        return self.function.getFunctionDetails(request=request, metadata=self._metadata())

    @raises_openobd_exceptions
    def finish(self, service_result: grpcServiceResult.ServiceResult) -> grpcEmpty.EmptyMessage:
        """
        Gracefully closes the openOBD session by changing the session's state to "finished" and preventing further
        communication with the session. The given ServiceResult indicates the success or failure reason of the executed
        service.

        :param service_result: a ServiceResult message representing the result of the executed service.
        :return: an EmptyMessage, indicating that no problems occurred.
        """
        self.active = False
        return self.session.finish(service_result, metadata=self._metadata())

    def __str__(self):
        return (f"ID: {self.session_info.id}, "
                f"state: {self.session_info.state}, "
                f"created at: {self.session_info.created_at}, "
                f"gRPC endpoint: {self.session_info.grpc_endpoint}, "
                f"authentication token: {self.session_info.authentication_token}")


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class OpenOBD(metaclass=SingletonMeta):

    def __init__(self, **kwargs):
        """
        A singleton that allows for the starting and managing of openOBD sessions using the provided Partner API
        credentials. The credentials are retrieved from the environment variables unless explicitly given as kwargs
        on first initialization.

        :keyword client_id: the identifier of the created credential set.
        :keyword client_secret: the secret of the created credential set.
        :keyword cluster_id: the ID of the cluster on which openOBD sessions should be managed (001=Europe, 002=USA).
        :keyword grpc_host: the address to which gRPC calls should be sent.
        :keyword grpc_port: the port used by gRPC calls, which needs to be 443 to use SSL.
        """
        self.session_controller = OpenOBDSessionController(**kwargs)
        self.function_broker = OpenOBDFunctionBroker(**kwargs)

    @raises_openobd_exceptions
    def start_session_on_ticket(self, ticket_id: str) -> OpenOBDSession:
        """
        Starts an openOBD session on the given ticket.

        :param ticket_id: the ticket number (or identifier) on which a session should be started.
        :return: an OpenOBDSession object representing the started session, which can be used to make gRPC calls.
        """
        response = self.session_controller.start_session_on_ticket(grpcSessionController.TicketId(value=ticket_id))
        return OpenOBDSession(response)

    @raises_openobd_exceptions
    def start_session_on_connector(self, connector_id: str) -> OpenOBDSession:
        """
        Starts an openOBD session on the given connector.

        :param connector_id: the UUID of the connector on which a session should be started.
        :return: an OpenOBDSession object representing the started session, which can be used to make gRPC calls.
        """
        response = self.session_controller.start_session_on_connector(grpcSessionController.ConnectorId(value=connector_id))
        return OpenOBDSession(response)

    @raises_openobd_exceptions
    def get_session(self, session_id: grpcSessionController.SessionId) -> grpcSessionController.SessionInfo:
        """
        Retrieves the requested openOBD session. Raises an OpenOBDException if the session does not exist.

        :param session_id: the identifier of the session to be retrieved.
        :return: a SessionInfo object representing the requested session.
        """
        return self.session_controller.get_session(session_id)

    @raises_openobd_exceptions
    def interrupt_session(self, session_id: grpcSessionController.SessionId) -> grpcSessionController.SessionInfo:
        """
        Forcefully closes the given openOBD session. This changes the session's state to "interrupted" and prevents
        further communication with the session.

        :param session_id: the identifier of the session to be interrupted.
        :return: a SessionInfo object representing the interrupted session.
        """
        return self.session_controller.interrupt_session(session_id)

    @raises_openobd_exceptions
    def get_session_list(self) -> grpcSessionController.SessionInfoList:
        """
        Retrieves all (recently) active openOBD sessions for this partner.

        :return: a SessionInfoList object containing an iterable of SessionInfo objects under its "sessions" attribute.
        """
        return self.session_controller.get_session_list()

    @raises_openobd_exceptions
    def open_function_stream(self, function_update_messages: Iterator[grpcFunctionBroker.FunctionUpdate]) -> Iterator[grpcFunctionBroker.FunctionUpdate]:
        """
        Opens a stream in which functions can be made available for function callers, and through which function calls
        will be forwarded.

        :param function_update_messages: a FunctionUpdate message for each function that needs to be registered.
        :return: FunctionUpdate messages containing acknowledgements of registrations, pings, and function calls.
        """
        return self.function_broker.open_function_stream(function_update_messages)

    @raises_openobd_exceptions
    def run_function(self, function_id: str, session_info: grpcSessionController.SessionInfo) -> grpcFunctionBroker.FunctionUpdate:
        """
        Execute a function that has been registered by a function launcher.

        :param function_id: the UUID of the function to call.
        :param session_info: the session to run the function in.
        :return: a FunctionUpdate object defining whether the function has been successfully launched.
        """
        return self.function_broker.run_function(grpcFunctionBroker.FunctionCall(id=function_id, session_info=session_info))

    @raises_openobd_exceptions
    def get_function_registration(self, function_id: str) -> grpcFunctionBroker.FunctionRegistration:
        """
        Retrieves information about the requested function. For instance, whether the function is online or not.

        :param function_id: the UUID of the function to request info on.
        :return: a FunctionRegistration object containing details on the requested function.
        """
        return self.function_broker.get_function_registration(grpcFunction.FunctionId(value=function_id))

    @raises_openobd_exceptions
    def generate_function_id(self) -> grpcFunction.FunctionId:
        """
        Generates a new function ID and signature, which are used when registering an openOBD function.

        :return: a FunctionId object containing a new function ID and its corresponding signature.
        """
        return self.function_broker.generate_function_id()


class OpenOBDSessionController(GrpcChannel):

    def __init__(self, **kwargs):
        """
        Used exclusively for starting and managing openOBD sessions. Retrieves the Partner API credentials from the
        environment variables unless explicitly given as kwargs.

        :keyword client_id: the identifier of the created credential set.
        :keyword client_secret: the secret of the created credential set.
        :keyword cluster_id: the ID of the cluster on which openOBD sessions should be managed (001=Europe, 002=USA).
        :keyword grpc_host: the address to which gRPC calls should be sent.
        :keyword grpc_port: the port used by gRPC calls, which needs to be 443 to use SSL.
        """
        self.client_id = _get_value_from_kwargs_or_env(kwargs, "client_id", "OPENOBD_PARTNER_CLIENT_ID")
        self.client_secret = _get_value_from_kwargs_or_env(kwargs, "client_secret", "OPENOBD_PARTNER_CLIENT_SECRET")
        self.cluster_id = _get_value_from_kwargs_or_env(kwargs, "cluster_id", "OPENOBD_CLUSTER_ID")

        self.grpc_host = _get_value_from_kwargs_or_env(kwargs, "grpc_host", "OPENOBD_GRPC_HOST")
        self.grpc_port = kwargs.get('grpc_port') if 'grpc_port' in kwargs else 443
        self._connect()

        self.session_controller = grpcSessionControllerService.sessionControllerStub(self.channel)
        self.session_controller_token = Token(self._request_session_controller_token, 7200)

    def _metadata(self):
        metadata = [("authorization", "Bearer {}".format(self.session_controller_token.get_value()))]
        metadata = tuple(metadata)
        return metadata

    @raises_openobd_exceptions
    def _request_session_controller_token(self):
        return self.session_controller.getSessionControllerToken(
            grpcSessionController.Authenticate(
                client_id=self.client_id,
                client_secret=self.client_secret,
                cluster_id=self.cluster_id
            )
        ).value

    @raises_openobd_exceptions
    def start_session_on_ticket(self, ticket_id: grpcSessionController.TicketId) -> grpcSessionController.SessionInfo:
        """
        Starts an openOBD session on the given ticket.

        :param ticket_id: the ticket number (or identifier) on which a session should be started.
        :return: a SessionInfo object representing the started session.
        """
        return self.session_controller.startSessionOnTicket(ticket_id, metadata=self._metadata())

    @raises_openobd_exceptions
    def start_session_on_connector(self, connector_id: grpcSessionController.ConnectorId) -> grpcSessionController.SessionInfo:
        """
        Starts an openOBD session on the given connector.

        :param connector_id: the UUID of the connector on which a session should be started.
        :return: a SessionInfo object representing the started session.
        """
        return self.session_controller.startSessionOnConnector(connector_id, metadata=self._metadata())

    @raises_openobd_exceptions
    def get_session(self, session_id: grpcSessionController.SessionId) -> grpcSessionController.SessionInfo:
        """
        Retrieves the requested openOBD session. Raises an OpenOBDException if the session does not exist.

        :param session_id: the identifier of the session to be retrieved.
        :return: a SessionInfo object representing the requested session.
        """
        return self.session_controller.getSession(session_id, metadata=self._metadata())

    @raises_openobd_exceptions
    def interrupt_session(self, session_id: grpcSessionController.SessionId) -> grpcSessionController.SessionInfo:
        """
        Forcefully closes the given openOBD session. This changes the session's state to "interrupted" and prevents
        further communication with the session.

        :param session_id: the identifier of the session to be interrupted.
        :return: a SessionInfo object representing the interrupted session.
        """
        return self.session_controller.interruptSession(session_id, metadata=self._metadata())

    @raises_openobd_exceptions
    def get_session_list(self) -> grpcSessionController.SessionInfoList:
        """
        Retrieves all (recently) active openOBD sessions for this partner.

        :return: a SessionInfoList object containing an iterable of SessionInfo objects under its "sessions" attribute.
        """
        return self.session_controller.getSessionList(request=grpcEmpty.EmptyMessage(), metadata=self._metadata())


class OpenOBDFunctionBroker(GrpcChannel):

    def __init__(self, **kwargs):
        """
        Used for hosting and running third-party openOBD functions.
        Retrieves the Partner API credentials from the environment variables unless explicitly given as kwargs.

        :keyword client_id: the identifier of the created credential set.
        :keyword client_secret: the secret of the created credential set.
        :keyword cluster_id: the ID of the cluster on which openOBD functions should be managed (001=Europe, 002=USA).
        :keyword grpc_host: the address to which gRPC calls should be sent.
        :keyword grpc_port: the port used by gRPC calls, which needs to be 443 to use SSL.
        """
        self.client_id = _get_value_from_kwargs_or_env(kwargs, "client_id", "OPENOBD_PARTNER_CLIENT_ID")
        self.client_secret = _get_value_from_kwargs_or_env(kwargs, "client_secret", "OPENOBD_PARTNER_CLIENT_SECRET")
        self.cluster_id = _get_value_from_kwargs_or_env(kwargs, "cluster_id", "OPENOBD_CLUSTER_ID")

        self.grpc_host = _get_value_from_kwargs_or_env(kwargs, "grpc_host", "OPENOBD_GRPC_HOST")
        self.grpc_port = kwargs.get("grpc_port") if "grpc_port" in kwargs else 443
        self._connect()

        self.function_broker = grpcFunctionBrokerServices.functionBrokerStub(self.channel)
        self.function_broker_token = Token(self._request_function_broker_token, 300)

    def _metadata(self):
        metadata = [("authorization", "Bearer {}".format(self.function_broker_token.get_value()))]
        metadata = tuple(metadata)
        return metadata

    @raises_openobd_exceptions
    def _request_function_broker_token(self):
        """
        Requests a new function broker token. A valid function broker token is required to make any of the other calls
        to the function broker.
        """
        return self.function_broker.getFunctionBrokerToken(
            grpcSessionController.Authenticate(
                client_id=self.client_id,
                client_secret=self.client_secret,
                cluster_id=self.cluster_id
            )
        ).value

    @raises_openobd_exceptions
    def open_function_stream(self, function_update_messages: Iterator[grpcFunctionBroker.FunctionUpdate]) -> Iterator[grpcFunctionBroker.FunctionUpdate]:
        """
        Opens a stream in which functions can be made available for function callers, and through which function calls
        will be forwarded.

        :param function_update_messages: a FunctionUpdate message for each function that needs to be registered.
        :return: FunctionUpdate messages containing acknowledgements of registrations, pings, and function calls.
        """
        return self.function_broker.openFunctionStream(function_update_messages, metadata=self._metadata())

    @raises_openobd_exceptions
    def run_function(self, function_call: grpcFunctionBroker.FunctionCall) -> grpcFunctionBroker.FunctionUpdate:
        """
        Execute a function that has been registered by a function launcher.

        :param function_call: a FunctionCall defining which function to call, and the session to run the function in.
        :return: a FunctionUpdate object defining whether the function has been successfully launched.
        """
        return self.function_broker.runFunction(request=function_call, metadata=self._metadata())

    @raises_openobd_exceptions
    def get_function_registration(self, function_id: grpcFunction.FunctionId) -> grpcFunctionBroker.FunctionRegistration:
        """
        Retrieves information about the requested function. For instance, whether the function is online or not.

        :param function_id: the UUID of the function to request info on.
        :return: a FunctionRegistration object containing details on the requested function.
        """
        return self.function_broker.getFunctionRegistration(request=function_id, metadata=self._metadata())

    @raises_openobd_exceptions
    def generate_function_id(self, request: grpcEmpty.EmptyMessage | None = None) -> grpcFunction.FunctionId:
        """
        Generates a new function ID and signature, which are used when registering an openOBD function.

        :return: a FunctionId object containing a new function ID and its corresponding signature.
        """
        if request is None:
            request = grpcEmpty.EmptyMessage()
        return self.function_broker.generateFunctionSignature(request=request, metadata=self._metadata())
