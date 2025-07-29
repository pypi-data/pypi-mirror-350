import asyncio
import json
from collections import deque
from dataclasses import dataclass
from typing import Deque, Optional

import numpy as np
from go2_webrtc_driver.constants import RTC_TOPIC, SPORT_CMD
from go2_webrtc_driver.webrtc_driver import Go2WebRTCConnection, WebRTCConnectionMethod
from loguru import logger

from phosphobot.hardware.base import BaseMobileRobot
from phosphobot.models import RobotConfigStatus


@dataclass
class MovementCommand:
    position: np.ndarray
    orientation: np.ndarray | None = None


class UnitreeGo2(BaseMobileRobot):
    name = "unitree-go2"

    UNITREE_MAC_PREFIXES = ["78:22:88"]

    def __init__(self, ip: str = "192.168.1.42", max_history_len: int = 100, **kwargs):
        """
        Initialize the UnitreeGo2 robot.

        Args:
            ip: IP address of the robot
            **kwargs: Additional keyword arguments
        """
        super().__init__(**kwargs)
        self.ip = ip
        self.conn = None
        self.current_position = np.zeros(3)  # [x, y, z]
        self.current_orientation = np.zeros(3)  # [roll, pitch, yaw]
        self._is_connected = False

        # Track movement instructions
        self.movement_queue: Deque[MovementCommand] = deque(maxlen=max_history_len)
        self.connect()

    @property
    def is_connected(self) -> bool:
        """
        Check if the robot is connected.

        Returns:
            bool: True if connected, False otherwise
        """
        return self._is_connected and self.conn is not None

    @is_connected.setter
    def is_connected(self, value: bool) -> None:
        """
        Set the connection status of the robot.

        Args:
            value: True if connected, False otherwise
        """
        if value and self.conn is None:
            raise ValueError("Cannot set is_connected to True without a connection")
        self._is_connected = value

    def connect(self) -> None:
        """
        Initialize communication with the robot.

        This method creates a WebRTC connection to the robot.

        Raises:
            Exception: If the connection fails
        """
        try:
            # Create a synchronous event loop to run the connect method
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            # Create connection and connect
            self.conn = Go2WebRTCConnection(WebRTCConnectionMethod.LocalSTA, ip=self.ip)
            if self.conn is None:
                raise Exception("Failed to create WebRTC connection")

            loop.run_until_complete(self.conn.connect())

            # Check if in normal mode and switch if needed
            response = loop.run_until_complete(
                self.conn.datachannel.pub_sub.publish_request_new(
                    RTC_TOPIC["MOTION_SWITCHER"], {"api_id": 1001}
                )
            )

            if response["data"]["header"]["status"]["code"] == 0:
                data = json.loads(response["data"]["data"])
                current_motion_switcher_mode = data["name"]

                if current_motion_switcher_mode != "normal":
                    logger.info(
                        f"Switching from {current_motion_switcher_mode} to 'normal' mode"
                    )
                    loop.run_until_complete(
                        self.conn.datachannel.pub_sub.publish_request_new(
                            RTC_TOPIC["MOTION_SWITCHER"],
                            {"api_id": 1002, "parameter": {"name": "normal"}},
                        )
                    )
                    # Wait for mode switch
                    loop.run_until_complete(asyncio.sleep(5))

            self.is_connected = True
            logger.info("Successfully connected to UnitreeGo2")

        except Exception as e:
            logger.error(f"Failed to connect to UnitreeGo2: {e}")
            raise Exception(f"Failed to connect to UnitreeGo2: {e}")
        finally:
            loop.close()

    def disconnect(self) -> None:
        """
        Close the connection to the robot.
        """
        if self.conn:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            # There's no explicit disconnect method, but we can clean up
            self.conn = None
            self.is_connected = False
            logger.info("Disconnected from UnitreeGo2")
            loop.close()

    def get_observation(self) -> tuple[np.ndarray, np.ndarray]:
        """
        Get the observation of the robot.

        Returns:
            - state: Last movement command position [x, y, z] and orientation [roll, pitch, yaw]
            - joints_position: Empty array as we're not tracking joint positions
        """
        # Return the last movement command as observation
        # Combine position and orientation into a 6D state vector
        state = np.concatenate([self.current_position, self.current_orientation])
        # Return empty array for joints since we're not tracking them
        joints_position = np.array([])

        return state, joints_position

    def set_motors_positions(
        self, positions: np.ndarray, enable_gripper: bool = False
    ) -> None:
        """
        Not implemented
        """
        pass

    def get_info_for_dataset(self):
        """
        Not implemented
        """
        raise NotImplementedError

    async def move_robot_absolute(
        self,
        target_position: np.ndarray,
        target_orientation_rad: np.ndarray | None,
        **kwargs,
    ) -> None:
        """
        Move the robot to the target position and orientation asynchronously.

        Args:
            target_position: Target position as [x, y, z]
            target_orientation_rad: Target orientation in radians [roll, pitch, yaw]
            **kwargs: Additional arguments
        """
        if not self.is_connected or self.conn is None:
            logger.error("Robot is not connected")
            return

        self.movement_queue.append(
            MovementCommand(
                position=target_position.copy(),
                orientation=target_orientation_rad.copy()
                if target_orientation_rad is not None
                else None,
            )
        )

        self.current_position = target_position

        await self.conn.datachannel.pub_sub.publish_request_new(
            RTC_TOPIC["SPORT_MOD"],
            {
                "api_id": SPORT_CMD["Move"],
                "parameter": {
                    "x": float(target_position[0]),
                    "y": float(target_position[1]),
                    "z": float(target_position[2]),
                },
            },
        )

        if target_orientation_rad is not None:
            self.current_orientation = target_orientation_rad
            target_orientation_deg = np.degrees(target_orientation_rad[2])

            await self.conn.datachannel.pub_sub.publish_request_new(
                RTC_TOPIC["SPORT_MOD"],
                {
                    "api_id": SPORT_CMD["Euler"],
                    "parameter": {
                        "x": float(target_orientation_rad[0]),
                        "y": float(target_orientation_rad[1]),
                        "z": float(target_orientation_deg),
                    },
                },
            )

        logger.info(
            f"Moved to position {target_position} with orientation {target_orientation_rad}"
        )

    @classmethod
    def from_ip(cls, ip: str, **kwargs) -> Optional["UnitreeGo2"]:
        """
        Create a UnitreeGo2 instance from an IP address.

        Args:
            ip: IP address of the robot
            **kwargs: Additional arguments

        Returns:
            UnitreeGo2 instance or None if the connection fails
        """
        try:
            robot = cls(ip=ip, **kwargs)
            return robot
        except Exception as e:
            logger.error(f"Failed to connect to UnitreeGo2 at {ip}: {e}")
            return None

    def status(self) -> RobotConfigStatus:
        """
        Get the status of the robot.

        Returns:
            RobotConfigStatus object
        """
        return RobotConfigStatus(
            name=self.name,
            usb_port=self.ip,
        )

    async def move_to_initial_position(self) -> None:
        """
        Move the robot to its initial position.

        This puts the robot in a stand position ready for operation.
        """
        if not self.is_connected or self.conn is None:
            logger.error("Robot is not connected")
            return

        # Stand up the robot
        await self.conn.datachannel.pub_sub.publish_request_new(
            RTC_TOPIC["SPORT_MOD"],
            {"api_id": SPORT_CMD["StandUp"], "parameter": {"data": True}},
        )

        # Wait for the robot to stand up
        await asyncio.sleep(5)

        # Reset position tracking
        self.current_position = np.zeros(3)
        self.current_orientation = np.zeros(3)

        # Clear movement history
        self.movement_queue.clear()

        logger.info("Robot moved to initial position")

    async def move_to_sleep(self) -> None:
        """
        Move the robot to its sleep position.

        This makes the robot sit down before potentially disconnecting.
        """
        if not self.is_connected or self.conn is None:
            logger.error("Robot is not connected")
            return

        # Make the robot sit
        await self.conn.datachannel.pub_sub.publish_request_new(
            RTC_TOPIC["SPORT_MOD"],
            {"api_id": SPORT_CMD["Sit"], "parameter": {"data": True}},
        )

        # Wait for the robot to sit
        await asyncio.sleep(3)

        logger.info("Robot moved to sleep position")
