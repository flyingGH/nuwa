import numpy as np


def convert_camera_pose(pose, in_type, out_type):
    accepted_types = ["cv", "gl", "blender"]

    assert in_type in accepted_types, f"Input type {in_type} not in {accepted_types}"
    assert out_type in accepted_types, f"Output type {out_type} not in {accepted_types}"

    if in_type == "blender":
        in_type = "gl"
    if out_type == "blender":
        out_type = "gl"

    if in_type == out_type:
        return pose

    return pose @ np.array(
        [
            [1, 0, 0, 0],
            [0, -1, 0, 0],
            [0, 0, -1, 0],
            [0, 0, 0, 1],
        ]
    )


def qvec2rotmat(qvec):
    return np.array([
        [
            1 - 2 * qvec[2] ** 2 - 2 * qvec[3] ** 2,
            2 * qvec[1] * qvec[2] - 2 * qvec[0] * qvec[3],
            2 * qvec[3] * qvec[1] + 2 * qvec[0] * qvec[2]
        ], [
            2 * qvec[1] * qvec[2] + 2 * qvec[0] * qvec[3],
            1 - 2 * qvec[1] ** 2 - 2 * qvec[3] ** 2,
            2 * qvec[2] * qvec[3] - 2 * qvec[0] * qvec[1]
        ], [
            2 * qvec[3] * qvec[1] - 2 * qvec[0] * qvec[2],
            2 * qvec[2] * qvec[3] + 2 * qvec[0] * qvec[1],
            1 - 2 * qvec[1] ** 2 - 2 * qvec[2] ** 2
        ]
    ])


def get_rot90_camera_matrices(pose, fx, fy, cx, cy, h):
    """
    Get camera matrices for rotating image 90 degrees clockwise

    :param pose: camera pose matrix
    :param fx
    :param fy
    :param cx
    :param cy
    :param h: original image height
    :return:
    """
    new_pose_matrix = pose @ np.array([[0, 1, 0, 0],
                                       [-1, 0, 0, 0],
                                       [0, 0, 1, 0],
                                       [0, 0, 0, 1]])
    nfx = fy
    nfy = fx
    ncx = h - cy
    ncy = cx

    return new_pose_matrix, nfx, nfy, ncx, ncy
