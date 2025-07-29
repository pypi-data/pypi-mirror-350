import os
from typing import List, Optional

from .hack import hack_nuscenes


def run(
    nuscenes_dataset_path: str,
    conda_env_name: Optional[str] = None,
    lidar_channel_name: Optional[str] = None,
    camera_channels: Optional[List[str]] = None,
    pcd_dims: int = 4,
):
    if not os.path.exists(nuscenes_dataset_path):
        raise FileNotFoundError(
            f"错误: NuScenes 数据集路径不存在: {nuscenes_dataset_path}"
        )

    hack_nuscenes(
        nuscenes_path=nuscenes_dataset_path,
        conda_env_name=conda_env_name,
        lidar_channel_name=lidar_channel_name,
        camera_channels=camera_channels or [],
        pcd_dims=pcd_dims,
    )
