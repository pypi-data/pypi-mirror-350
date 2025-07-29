# Nuscenes Hacker

nuscenes数据集搭配nuscenes-devkit使用非常便捷，但是因为nuscenes是已经固定的数据，所以nuscenes-devkit在设计时候没有考虑过拓展性问题，将很多数据集的信息硬编码在其中了，例如

- 场景名称
- 地图名称
- 数据集划分
- 传感器 channel 名称
- 点云的数据格式(通道数)

所以当我们使用自己制作的nuscenes格式数据时候，就会遇到很多问题

如果直接对 nuscenes-devkit 进行修改，这样会破坏兼容性问题，很不优雅

所以我想，有没有一种方式可以"悄无声息"的对 nuscenes-devkit 进行修改呢？

答案是肯定的，这就是本项目的目的

本项目的目的是在悄咪咪的情况下对 nuscenes-devkit 进行修改，当使用完毕后，nuscenes-devkit 还是原来的样子，只是在运行时候，会使用我们自己的数据集，是不是像一个 Hacker 一样呢？

## Install
>
> Warning: 该项目只支持 python3.7 及以下版本(受限于numpy与nuscenes-devkit冲突)

```bash
pip3 install nuscenes-hacker
```

or

```bash
git clone https://github.com/windzu/nuscenes_hacker.git
cd nuscenes_hacker
pip3 install -e .
python -m pip install -e .
```

## Usage

### hack

**基本用法**

```bash
nuscenes-hacker hack [参数]
```

**参数说明**
必需参数

|参数|类型|描述|
|-|-|-|
|`dataset`|string|NuScenes 数据集的根目录路径|

例如

```bash
nuscenes-hacker hack /path/to/nuscenes
```

可选参数

|参数|类型|描述|
|-|-|-|
|`--conda-env-name`|string|指定需要替换的 conda 环境名称。如果不指定，则使用当前环境。|
|`--lidar-channel`|string|指定使用的激光雷达通道名称，如果不指定，则不替换。例如：`LIDAR_TOP`|
|`--camera-channels`|string|指定相机通道，多个通道用逗号分隔，如果不指定，则不替换。例如：`CAM_FRONT,CAM_BACK`|
|`--pcd-dims`|int|指定点云的维度，如果不指定，则不替换。例如：`4`或`5`|

使用 `nuscenes-hacker hack --help` 可以查看所有参数的详细说明

### restore
>
> 恢复 nuscenes-devkit 到原始状态

```bash
nuscenes-hacker restore
```

注意事项
路径检查：程序会检查 dataset 是否存在，如果不存在将报错并终止运行

conda 环境：

如果指定了 conda-env-name，工具将尝试在该 conda 环境中找到 nuscenes 包并修改。
如果未指定，工具将使用当前环境中的 nuscenes 包。
兼容性问题：

此工具仅支持 Python 3.6 和 3.7，不支持 Python 3.8 及以上版本。
如果使用 NumPy 2.0+，可能会遇到兼容性问题，建议使用 NumPy 1.x 版本。
参数处理：

相机通道参数 (--camera-channels) 接受以逗号分隔的字符串，会被自动拆分为列表。
如果未指定某个可选参数，对应的功能将不会被替换或修改。
排错指南
如果遇到 "未找到 nuscenes 包" 的错误，请尝试以下解决方案：

确保已安装 nuscenes-devkit：pip install nuscenes-devkit
使用 --conda-env-name 参数指定正确的 conda 环境
检查 Python 版本是否为 3.6 或 3.7
如果使用 NumPy 2.0+，尝试降级到 NumPy 1.x：pip install numpy==1.24.4
支持和反馈
如有问题或建议，请访问 GitHub 仓库 或联系作者：<windzu1@gmail.com>
