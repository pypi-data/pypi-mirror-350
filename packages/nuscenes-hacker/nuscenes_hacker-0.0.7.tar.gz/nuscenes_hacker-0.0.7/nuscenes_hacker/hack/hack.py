import os
import random
import re

from nuscenes.nuscenes import NuScenes


def get_available_scenes(nuscene_path, data_version):
    """Get available scenes from the input nuScenes dataset.

    Args:
        nuscene_path (str): Path to the root folder of the nuScenes dataset.
        data_version (str): Version of the nuScenes dataset. Should be
            "v1.0-trainval" or "v1.0-test".

    Returns:
        available_scenes (list[dict]): List of basic information for the
            available scenes.
    """
    # data_version should be "v1.0-trainval" or "v1.0-test"
    if data_version not in ["v1.0-trainval", "v1.0-test"]:
        raise Exception("data_version should be 'v1.0-trainval' or 'v1.0-test'")

    # nuscene_path should be valid path
    target_path = os.path.join(nuscene_path, data_version)
    if not os.path.exists(target_path):
        print("get_available_scenes failed: " + target_path + " is not a valid path")

    nusc = NuScenes(version=data_version, dataroot=nuscene_path, verbose=True)
    available_scenes = []
    for scene in nusc.scene:
        scene_token = scene["token"]
        scene_rec = nusc.get("scene", scene_token)
        sample_rec = nusc.get("sample", scene_rec["first_sample_token"])

        # Count the number of samples in the scene
        sample_token = scene_rec["first_sample_token"]
        num_samples = 0
        while sample_token:
            sample_rec = nusc.get("sample", sample_token)
            num_samples += 1
            sample_token = sample_rec["next"]

        scene_info = {"name": scene["name"], "num_samples": num_samples}

        available_scenes.append(scene_info)

    # sort scenes by name
    available_scenes = sorted(available_scenes, key=lambda x: x["name"])
    return available_scenes


def get_all_scene_name(nuscenes_path):
    # 1. check nuscenes_path
    if not os.path.exists(nuscenes_path):
        raise Exception("nuscenes_path should be valid path")

    # 2. echo nuscenes info
    root_path = nuscenes_path

    # echo v1.0-trainval info
    trainval_available_scenes = get_available_scenes(root_path, "v1.0-trainval")
    print("v1.0-trainval info :")
    print(" available scene num: {}".format(len(trainval_available_scenes)))
    print(" available scene:")
    for scene in trainval_available_scenes:
        # echo scene info
        print("     " + scene["name"] + " " + str(scene["num_samples"]))

    # echo v1.0-test info
    test_available_scenes = get_available_scenes(root_path, "v1.0-test")
    print("v1.0-test info :")
    print(" available scene num: {}".format(len(test_available_scenes)))
    print(" available scene:")
    for scene in test_available_scenes:
        print("     " + scene["name"] + " " + str(scene["num_samples"]))

    # get trainval and test available scene name list
    trainval_scene_name_list = []
    test_scene_name_list = []
    trainval_scene_name_list = [scene["name"] for scene in trainval_available_scenes]
    test_scene_name_list = [scene["name"] for scene in test_available_scenes]

    return trainval_scene_name_list, test_scene_name_list


def get_nuscenes_api_path(conda_env_name=None):
    """获取nuscenes API路径

    Args:
        conda_env_name (str, optional): conda环境名称。默认为None，表示使用当前环境。

    Returns:
        str: nuscenes API的路径
    """

    if conda_env_name is None:
        # 使用 pip 命令查找 nuscenes 安装路径
        import importlib.util
        import os

        spec = importlib.util.find_spec("nuscenes")
        if spec and spec.origin:
            nuscenes_path = os.path.dirname(spec.origin)
            print(f"使用当前环境中的nuscenes: {nuscenes_path}")
            return nuscenes_path
        else:
            raise Exception("当前环境中未找到 nuscenes 包")

    # 如果指定了conda环境，则获取该环境的路径
    conda_command = os.popen("which conda").read()
    if conda_command == "":
        raise Exception("conda command not exist, please check if conda is installed")
    conda_env_list = os.popen("conda env list").read()
    if conda_env_name not in conda_env_list:
        raise Exception(
            "conda env {} not exist, please check if conda env name is correct".format(
                conda_env_name
            )
        )

    # 3.2.1 get user name
    user_name = os.popen("whoami").read().strip()
    # 3.2.2 get conda_env_path
    conda_env_path = ""
    miniconda_env_path = os.path.join(
        "/home", user_name, "miniconda3", "envs", conda_env_name
    )
    anaconda_env_path = os.path.join(
        "/home", user_name, "anaconda3", "envs", conda_env_name
    )
    # check which conda env path is valid
    if os.path.exists(miniconda_env_path):
        conda_env_path = miniconda_env_path
    elif os.path.exists(anaconda_env_path):
        conda_env_path = anaconda_env_path
    else:
        raise Exception(
            "conda env path not exist, please check if conda env name is correct"
        )
    # 3.2.3 get python version
    # ls conda_env_path/lib and get python version which dir name start with python3
    python_version = ""
    for root, dirs, files in os.walk(os.path.join(conda_env_path, "lib")):
        for dir in dirs:
            if dir.startswith("python3"):
                python_version = dir
    if python_version == "":
        raise Exception("python version not exist, please check if python is installed")
    # 3.2.4 get nuscenes api path
    nuscenes_api_path = os.path.join(
        conda_env_path, "lib", python_version, "site-packages", "nuscenes"
    )

    # 3.2.5 check which conda env path is valid
    if not os.path.exists(nuscenes_api_path):
        # raise error and echo nuscenes api path
        print("nuscenes_api_path: {}".format(nuscenes_api_path))
        raise Exception(
            "nuscenes api path not exist, please check if nuscenes api path is correct"
        )

    return nuscenes_api_path


class Hack:
    def __init__(
        self,
        nuscenes_api_path,
        pcd_dims=None,
        lidar_channel_name=None,
        camera_channels=[],
        train_scene_name_list=[],
        val_scene_name_list=[],
        test_scene_name_list=[],
    ):
        self.nuscenes_root = nuscenes_api_path
        self.pcd_dims = pcd_dims
        self.lidar_channel_name = lidar_channel_name
        self.camera_channels = camera_channels
        self.train_scene_name_list = train_scene_name_list
        self.val_scene_name_list = val_scene_name_list
        self.test_scene_name_list = test_scene_name_list

    def hack(self):
        if self.lidar_channel_name:
            print("will hack lidar_channel_name to {}".format(self.lidar_channel_name))
            self.hack_lidar_channel_name(self.lidar_channel_name)

        if self.camera_channels:
            print("tmp not replace camera_channels")

            # print("will hack camera_channels to {}".format(self.camera_channels))
            # self.hack_camera_channels_name(self.camera_channels)

        if self.pcd_dims:
            print("will hack pcd_dims to {}".format(self.pcd_dims))
            self.hack_pcd_dims(self.pcd_dims)

        # hack splits
        print("will hack splits")
        self.hack_splits()

    def hack_lidar_channel_name(self, lidar_channel_name):
        raw_lidar_channel_name = "LIDAR_TOP"

        for root, dirs, files in os.walk(self.nuscenes_root):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    # 读取文件内容
                    with open(file_path, "r", encoding="utf-8") as file:
                        content = file.read()

                    # 替换字符串
                    content = content.replace(
                        raw_lidar_channel_name, lidar_channel_name
                    )

                    # 写入新内容到文件
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(content)

    def hack_camera_channels_name(self, camera_channels):
        raw_camera_channels = [
            "CAM_FRONT_LEFT",
            "CAM_FRONT",
            "CAM_FRONT_RIGHT",
            "CAM_BACK_LEFT",
            "CAM_BACK",
            "CAM_BACK_RIGHT",
        ]

        new_camera_channels = camera_channels

        # 通过正则匹配替换的方式，将原始的相机通道名称替换为新的相机通道名称是一种更加稳妥的方式
        # 1. 如果两个列表长度一致,直接构建一一对应的替换关系
        # 2. 如果 new_camera_channels 长度小于 raw_camera_channels 长度,则只替换 new_camera_channels 中的相机通道名称
        # 3. 如果 new_camera_channels 长度大于 raw_camera_channels 长度,暂时不支持这种情况

        if len(new_camera_channels) > len(raw_camera_channels):
            raise Exception(
                "new_camera_channels length should <= raw_camera_channels length"
            )

        camera_channel_replace_dict = {}
        for i in range(len(raw_camera_channels)):
            if i < len(new_camera_channels):
                camera_channel_replace_dict[raw_camera_channels[i]] = (
                    new_camera_channels[i]
                )
            else:
                break

        for root, dirs, files in os.walk(self.nuscenes_root):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    # 读取文件内容
                    with open(file_path, "r", encoding="utf-8") as file:
                        content = file.read()

                    # 通过正则表达式匹配替换
                    for (
                        raw_camera_channel,
                        new_camera_channel,
                    ) in camera_channel_replace_dict.items():
                        pattern = re.compile(
                            r"(" + re.escape(raw_camera_channel) + r")"
                        )
                        content = pattern.sub(new_camera_channel, content)

    def hack_pcd_dims(self, pcd_dims):
        target_file_list = [
            os.path.join(self.nuscenes_root, "utils", "data_classes.py")
        ]

        for target_file in target_file_list:
            # replace pcd_dims
            self.repalce_dims(target_file, 5, pcd_dims)

    def hack_splits(self):
        target_file = os.path.join(self.nuscenes_root, "utils", "splits.py")

        # debug
        print("target_file: {}".format(target_file))

        # replace train_detect
        if self.train_scene_name_list:
            train_detect = self.train_scene_name_list
            print("will hack train_detect to {}".format(train_detect))
            if train_detect:
                self.repalce_list(target_file, "train_detect", train_detect)

        # replace train_track
        if self.train_scene_name_list:
            train_track = self.train_scene_name_list
            print("will hack train_track to {}".format(train_track))
            if train_track:
                self.repalce_list(target_file, "train_track", train_track)

        # replace val
        if self.val_scene_name_list:
            val = self.val_scene_name_list
            print("will hack val to {}".format(val))
            if val:
                self.repalce_list(target_file, "val", val)

        # replace test
        if self.test_scene_name_list:
            test = self.test_scene_name_list
            print("will hack test to {}".format(test))
            if test:
                self.repalce_list(target_file, "test", test)

        self.commit_assert(target_file)

        print("hack splits done")

    @staticmethod
    def repalce_list(file_path, target_list_name, replace):
        # 定义正则表达式，匹配形如 array_name = [...] 的模式，其中 [...] 可能跨多行
        pattern = re.compile(
            r"(" + re.escape(target_list_name) + r"\s*=\s*\\\s*\[)[^\]]*\]", re.DOTALL
        )

        # 读取原始文件
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        # judge if find target_list_name
        if not pattern.search(content):
            print("not find target_list_name: {}".format(target_list_name))
            return

        # 替换找到的内容
        replace_str = str(replace)
        replace_str = replace_str[1:-1]  # remove '[' and ']'

        new_content = pattern.sub(r"\1" + replace_str + "]", content)

        # 将修改后的内容写回文件
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(new_content)

    @staticmethod
    def commit_assert(file_path):
        # 在 nuscenes/utils/splits.py 中，有一个断言语句，检查是否有 1000 个场景
        # 如果我们修改了场景的划分，那么这个断言语句就会失效
        # 我们需要注释掉这个断言语句
        # find special pattern
        target_list = [
            "assert len(all_scenes) == 1000 and len(set(all_scenes)) == 1000, 'Error: Splits incomplete!'"
        ]

        # 读取原始文件
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        # judge if find target_list_name
        for target in target_list:
            if target in content:
                # delete target
                content = content.replace(target, "")
        # 将修改后的内容写回文件
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

    @staticmethod
    def repalce_dims(file_path, old_dims, new_dims):
        # 定义正则表达式来匹配形如 (-1,5) 的模式，并允许其中有空白
        pattern = re.compile(r"(\(-1,\s*)" + re.escape(str(old_dims)) + r"(\s*\))")

        # 读取原始文件
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        # 替换找到的数字
        new_content = pattern.sub(r"\g<1>" + str(new_dims) + r"\g<2>", content)

        # 将修改后的内容写回文件
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(new_content)


def hack_nuscenes(
    nuscenes_path,
    conda_env_name,
    pcd_dims,
    lidar_channel_name,
    camera_channels,
):

    print("----------------------")
    print("----hack  nuscenes----")
    print("----------------------")

    # 1. get all scene name which car brand is car_brand
    # trainval_available_scenes = get_available_scenes(nuscenes_path, "v1.0-trainval")
    # test_available_scenes = get_available_scenes(nuscenes_path, "v1.0-test")
    print("1. echo nuscenes info")
    print("---------------------------------------------------------------------------")
    trainval_scene_name_list, test_scene_name_list = get_all_scene_name(nuscenes_path)

    target_trainval_scene_name_list = trainval_scene_name_list
    target_test_scene_name_list = test_scene_name_list

    print("target_trainval_scene_name_list:")
    print("trainval_scene_name_list:", len(trainval_scene_name_list))
    for scene_name in target_trainval_scene_name_list:
        print("  " + scene_name)
    print("target_test_scene_name_list:")
    print("target_test_scene_name_list:", len(target_test_scene_name_list))
    for scene_name in target_test_scene_name_list:
        print("  " + scene_name)

    # 2. split scene name to train, val, test
    print("2. split scene name to train, val, test")
    print("---------------------------------------------------------------------------")
    # target_trainval_scene_name_list size must > =2
    if len(target_trainval_scene_name_list) < 2:
        raise Exception(
            "target_trainval_scene_name_list size must > =2, but got {}".format(
                len(target_trainval_scene_name_list)
            )
        )
    # split train, val : 80%, 20%
    # random shuffle target_trainval_scene_name_list first
    random.shuffle(target_trainval_scene_name_list)
    train_scene_name_list = target_trainval_scene_name_list[
        : int(len(target_trainval_scene_name_list) * 0.8)
    ]
    val_scene_name_list = target_trainval_scene_name_list[
        int(len(target_trainval_scene_name_list) * 0.8) :
    ]

    # debug
    print("train_scene_name_list:", len(train_scene_name_list))
    for scene_name in train_scene_name_list:
        print("  " + scene_name)
    print("val_scene_name_list:", len(val_scene_name_list))
    for scene_name in val_scene_name_list:
        print("  " + scene_name)

    # 3. hack nuScenes api
    print("3. hack nuScenes api")
    print("---------------------------------------------------------------------------")
    # 3.2. make sure target conda env if exist nuscenes api
    nuscenes_api_path = get_nuscenes_api_path(conda_env_name)

    nuscenes_hack = Hack(
        nuscenes_api_path,
        pcd_dims=pcd_dims,
        lidar_channel_name=lidar_channel_name,
        camera_channels=camera_channels,
        train_scene_name_list=train_scene_name_list,
        val_scene_name_list=val_scene_name_list,
        test_scene_name_list=target_test_scene_name_list,
    )
    nuscenes_hack.hack()

    return
