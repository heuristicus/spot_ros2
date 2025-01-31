# Copyright [2023] Boston Dynamics AI Institute, Inc.
from typing import Optional

import bdai_ros2_wrappers.tf_listener_wrapper as tfl
from bosdyn.client.math_helpers import Quat, SE3Pose
from geometry_msgs.msg import Transform


def ros_transform_to_se3_pose(transform: Transform) -> SE3Pose:
    return SE3Pose(
        transform.translation.x,
        transform.translation.y,
        transform.translation.z,
        Quat(w=transform.rotation.w, x=transform.rotation.x, y=transform.rotation.y, z=transform.rotation.z),
    )


class TFListenerWrapper(tfl.TFListenerWrapper):
    def lookup_a_tform_b(
        self,
        frame_a: str,
        frame_b: str,
        transform_time: Optional[float] = None,
        timeout: Optional[float] = None,
        wait_for_frames: bool = False,
    ) -> SE3Pose:
        """
        Parameters:
            frame_a: Base frame for transform.  The transform returned will be frame_a_t_frame_b
            frame_b: Tip frame for transform.  The transform returned will be frame_a_t_frame_b
            transform_time: The time at which to look up the transform.  If left at None, will be the most recent
                transform available
            timeout: The time to wait for the transform to become available if the transform_time is beyond the most
                recent transform in the buffer.
            wait_for_frames: If true, waits timeout amount of time for a path to exist from frame_a to frame_b in the
                the buffer.  If false, this will return immediately if a path does not exist even if timeout is not
                None.  Note that wait_for_transform can be used to wait indefinitely for a transform to become
                available.
        Returns:
            The transform frame_a_t_frame_b at the time specified.
        Raises:
            All the possible TransformExceptions.
        """
        return ros_transform_to_se3_pose(
            tfl.TFListenerWrapper.lookup_a_tform_b(
                self, frame_a, frame_b, transform_time, timeout, wait_for_frames
            ).transform
        )
