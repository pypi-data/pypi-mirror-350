"""Transport abstract class.

Serves as an abstract for communication channels.
"""
from abc import ABC, abstractmethod
from typing import Callable, Optional
from iqrfpy.irequest import IRequest
from iqrfpy.iresponse import IResponse
from iqrfpy.confirmation import Confirmation


class ITransport(ABC):
    """Abstract class providing interface for communication channels."""

    @abstractmethod
    def initialize(self) -> None:
        """Initialize transport and create a connection if applicable.

        Raises:
            NotImplementedError: Abstract method not implemented.
        """
        raise NotImplementedError("Abstract method not implemented.")

    @abstractmethod
    def terminate(self, force: bool = False) -> None:
        """Terminates transport.

        Args:
            force (bool): Force terminate transport.

        Raises:
            NotImplementedError: Abstract method not implemented.
        """
        raise NotImplementedError("Abstract method not implemented.")

    @abstractmethod
    def send(self, request: IRequest) -> None:
        """Serialize passed request to format acceptable by the communication channel and send request.

        Args:
            request (IRequest): Request message to send.

        Raises:
            NotImplementedError: Abstract method not implemented.
        """
        raise NotImplementedError("Abstract method not implemented.")

    @abstractmethod
    def send_and_receive(self, request: IRequest, timeout: Optional[float] = None) -> IResponse:
        """Serialize request to format acceptable by the communication channel, send request and receive response synchronously.

        Args:
            request (IRequest): Request message to send.
            timeout (float, optional): Response timeout.

        Returns:
            :obj:`IResponse`: Response message object.

        Raises:
            NotImplementedError: Abstract method not implemented.
        """
        raise NotImplementedError("Abstract method not implemented.")

    @abstractmethod
    def receive(self, timeout: Optional[float] = None) -> IResponse:
        """Receive and return response synchronously.

        Args:
            timeout (float, optional): Response timeout.

        Returns:
            :obj:`IResponse`: Response message object.

        Raises:
            NotImplementedError: Abstract method not implemented.
        """
        raise NotImplementedError("Abstract method not implemented.")

    @abstractmethod
    def confirmation(self) -> Confirmation:
        """Receive and return confirmation synchronously.

        Returns:
            :obj:`Confirmation`: Confirmation message object.

        Raises:
            NotImplementedError: Abstract method not implemented.
        """
        raise NotImplementedError("Abstract method not implemented.")

    @abstractmethod
    def set_receive_callback(self, callback: Callable[[IResponse], None]) -> None:
        """Set callback to handle asynchronously received messages.

        Args:
            callback (Callable[[IResponse], None]): Function to call once a message has been received and successfully
                                                    deserialized.

        Raises:
            NotImplementedError: Abstract method not implemented.
        """
        raise NotImplementedError("Abstract method not implemented.")
