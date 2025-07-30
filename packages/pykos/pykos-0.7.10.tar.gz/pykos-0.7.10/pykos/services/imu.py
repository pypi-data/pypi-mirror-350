"""IMU service client."""

from typing import NotRequired, TypedDict, Unpack

import grpc
import grpc.aio
from google.longrunning import operations_pb2_grpc
from google.protobuf.any_pb2 import Any as AnyPb2
from google.protobuf.duration_pb2 import Duration
from google.protobuf.empty_pb2 import Empty

from kos_protos import common_pb2, imu_pb2, imu_pb2_grpc
from kos_protos.imu_pb2 import CalibrateIMUMetadata
from pykos.services import AsyncClientBase


class ZeroIMURequest(TypedDict):
    max_retries: NotRequired[int]
    max_angular_error: NotRequired[float]
    max_velocity: NotRequired[float]
    max_acceleration: NotRequired[float]


class CalibrationStatus:
    IN_PROGRESS = "IN_PROGRESS"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"


class CalibrationMetadata:
    def __init__(self, metadata_any: AnyPb2) -> None:
        self.status: str | None = None
        self.decode_metadata(metadata_any)

    def decode_metadata(self, metadata_any: AnyPb2) -> None:
        metadata = CalibrateIMUMetadata()
        if metadata_any.Is(CalibrateIMUMetadata.DESCRIPTOR):
            metadata_any.Unpack(metadata)
            self.status = metadata.status if metadata.HasField("status") else None

    def __str__(self) -> str:
        return f"CalibrationMetadata(status={self.status})"

    def __repr__(self) -> str:
        return self.__str__()


def _duration_from_seconds(seconds: float) -> Duration:
    """Convert seconds to Duration proto."""
    duration = Duration()
    duration.seconds = int(seconds)
    duration.nanos = int((seconds - int(seconds)) * 1e9)
    return duration


class IMUServiceClient(AsyncClientBase):
    """Client for the IMUService."""

    def __init__(self, channel: grpc.aio.Channel) -> None:
        super().__init__()
        self.stub = imu_pb2_grpc.IMUServiceStub(channel)
        self.operations_stub = operations_pb2_grpc.OperationsStub(channel)

    async def get_imu_values(self) -> imu_pb2.IMUValuesResponse:
        """Get the latest IMU sensor values.

        Returns:
            ImuValuesResponse: The latest IMU sensor values.
        """
        return await self.stub.GetValues(Empty())

    async def get_imu_advanced_values(self) -> imu_pb2.IMUAdvancedValuesResponse:
        """Get the latest IMU advanced values.

        Returns:
            ImuAdvancedValuesResponse: The latest IMU advanced values.
        """
        return await self.stub.GetAdvancedValues(Empty())

    async def get_euler_angles(self) -> imu_pb2.EulerAnglesResponse:
        """Get the latest Euler angles.

        Returns:
            EulerAnglesResponse: The latest Euler angles.
        """
        return await self.stub.GetEuler(Empty())

    async def get_quaternion(self) -> imu_pb2.QuaternionResponse:
        """Get the latest quaternion.

        Returns:
            QuaternionResponse: The latest quaternion.
        """
        return await self.stub.GetQuaternion(Empty())

    async def zero(self, duration: float = 1.0, **kwargs: Unpack[ZeroIMURequest]) -> common_pb2.ActionResponse:
        """Zero the IMU.

        Example:
            >>> await zero(duration=1.0,
            ...     max_retries=3,
            ...     max_angular_error=1.0,
            ...     max_velocity=1.0,
            ...     max_acceleration=1.0
            ... )

        Args:
            duration: Duration in seconds for zeroing operation
            **kwargs: Additional zeroing parameters that may include:
                     max_retries: Maximum number of retries
                     max_angular_error: Maximum angular error during zeroing
                     max_velocity: Maximum velocity during zeroing
                     max_acceleration: Maximum acceleration during zeroing

        Returns:
            ActionResponse: The response from the zero operation.
        """
        request = imu_pb2.ZeroIMURequest(duration=_duration_from_seconds(duration), **kwargs)
        return await self.stub.Zero(request)

    async def calibrate(self) -> imu_pb2.CalibrateIMUResponse:
        """Calibrate the IMU.

        This starts a long-running calibration operation. The operation can be monitored
        using get_calibration_status().

        Returns:
            CalibrationMetadata: Metadata about the calibration operation.
        """
        return await self.stub.Calibrate(Empty())

    async def get_calibration_state(self) -> imu_pb2.GetCalibrationStateResponse:
        """Get the calibration state of the IMU."""
        return await self.stub.GetCalibrationState(imu_pb2.GetCalibrationStateRequest())
