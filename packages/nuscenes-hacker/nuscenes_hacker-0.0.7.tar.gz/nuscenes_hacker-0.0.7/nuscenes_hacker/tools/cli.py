from pathlib import Path
from typing import Optional

import typer

from nuscenes_hacker.hack.main import run as run_hack
from nuscenes_hacker.restore.main import run as run_restore

app = typer.Typer(
    name="nuscenes-hacker",
    add_completion=True,
    help="Nuscenes Hacker Toolkit",
)


@app.command(name="hack")
def hack_command(
    dataset: Path = typer.Argument(
        ...,
        show_default=False,
        help="(required) nuscenes数据集路径",
        exists=True,
    ),
    conda_env_name: str = typer.Option(
        None,
        show_default=False,
        help="[Optional] 指定需要替换的conda环境名称, 如果不指定，则使用当前环境",
    ),
    lidar_channel: str = typer.Option(
        None,
        show_default=False,
        help="[Optional] 指定使用的激光雷达通道名称，如果不指定，则不替换",
    ),
    camera_channels: str = typer.Option(
        None,
        show_default=False,
        help="[Optional] 指定相机通道，多个通道用逗号分隔，如果不指定，则不替换",
    ),
    pcd_dims: int = typer.Option(
        None,
        show_default=False,
        help="[Optional] 指定点云的维度，如果不指定，则不替换",
    ),
):
    """
    🚧 替换 nuscenes 数据集中的雷达/相机数据通道，输出为指定格式。
    """
    camera_channels_list = camera_channels.split(",") if camera_channels else []

    run_hack(
        nuscenes_dataset_path=dataset,
        conda_env_name=conda_env_name,
        lidar_channel_name=lidar_channel,
        camera_channels=camera_channels_list,
        pcd_dims=pcd_dims,
    )


@app.command(name="restore")
def restore_command():
    """
    🛠️ 强制重装 nuscenes-devkit 以还原系统状态。
    """
    run_restore()


def run():
    app()


if __name__ == "__main__":
    run()
