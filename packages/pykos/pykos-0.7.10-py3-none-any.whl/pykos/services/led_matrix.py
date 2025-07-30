"""LED Matrix service client."""

from typing import NotRequired, TypedDict, Unpack

import grpc
import grpc.aio
from google.protobuf.empty_pb2 import Empty

from kos_protos import common_pb2, led_matrix_pb2, led_matrix_pb2_grpc
from pykos.services import AsyncClientBase


class MatrixInfo(TypedDict):
    """Information about the LED matrix.

    Args:
        width: Width in pixels
        height: Height in pixels
        brightness_levels: Number of brightness levels supported (1 for binary on/off)
        color_capable: Whether the matrix supports color
        bits_per_pixel: Number of bits used to represent each pixel
        error: Optional error information
    """

    width: int
    height: int
    brightness_levels: int
    color_capable: bool
    bits_per_pixel: int
    error: NotRequired[common_pb2.Error | None]


class ImageData(TypedDict):
    """Image data to be written to the LED matrix.

    Args:
        buffer: Raw image data bytes
        width: Image width in pixels
        height: Image height in pixels
        format: Pixel format specification (e.g. 'RGB888', 'BGR888', 'RGB565', 'MONO8')
        brightness: Global brightness level (0-255)
    """

    buffer: bytes
    width: int
    height: int
    format: str
    brightness: int


class LEDMatrixServiceClient(AsyncClientBase):
    """Client for the LEDMatrixService.

    This service allows controlling an LED matrix display.
    """

    def __init__(self, channel: grpc.aio.Channel) -> None:
        """Initialize the LED matrix service client.

        Args:
            channel: gRPC channel to use for communication.
        """
        super().__init__()

        self.stub = led_matrix_pb2_grpc.LEDMatrixServiceStub(channel)

    async def get_matrix_info(self) -> MatrixInfo:
        """Get information about the LED matrix including dimensions and capabilities.

        Returns:
            MatrixInfo containing:
                width: Width in pixels
                height: Height in pixels
                brightness_levels: Number of brightness levels supported
                color_capable: Whether the matrix supports color
                bits_per_pixel: Number of bits used to represent each pixel
                error: Optional error information
        """
        return await self.stub.GetMatrixInfo(Empty())

    async def write_buffer(self, buffer: bytes) -> common_pb2.ActionResponse:
        """Write binary on/off states to the LED matrix.

        The buffer should be width * height / 8 bytes long, where each bit
        represents one LED's on/off state.

        Args:
            buffer: Binary buffer containing LED states

        Returns:
            ActionResponse indicating success/failure of the write operation.
        """
        request = led_matrix_pb2.WriteBufferRequest(buffer=buffer)
        return await self.stub.WriteBuffer(request)

    async def write_color_buffer(self, **kwargs: Unpack[ImageData]) -> common_pb2.ActionResponse:
        """Write image data to the LED matrix.

        Args:
            **kwargs: Image data containing the raw bytes, dimensions and format
                buffer: Raw image data bytes
                width: Image width in pixels
                height: Image height in pixels
                format: Pixel format specification (e.g. 'RGB888', 'BGR888', 'RGB565', 'MONO8')
                brightness: Global brightness level (0-255)

        Returns:
            ActionResponse indicating success/failure of the write operation.
        """
        request = led_matrix_pb2.WriteColorBufferRequest(**kwargs)
        return await self.stub.WriteColorBuffer(request)
