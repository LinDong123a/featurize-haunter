import argparse
from collections import defaultdict
import json
import logging
import os
import subprocess
import time
from typing import List

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


file_dir = os.path.dirname(os.path.abspath(__file__))


def parse_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--token", "-t", type=str, required=True,
        help="Featurize提供的token",
    )
    parser.add_argument(
        "--gpus", type=str, required=True,
        help="要进行抢占的机器类型，当有多种gpu机型要进行抢占时，按优先级从左到右排列，"
             "多种gpu间以半角逗号分隔"
    )
    parser.add_argument(
        "--interval", "-i", type=float, default=1.0,
        help="进行轮询操作的间隔，单位s，默认为1s"
    )
    parser.add_argument(
        "--num_machine", "-n", type=int, default=1,
        help="要抢占的机器数量"
    )
    parser.add_argument(
        "--notification", type=str, choices=["none", "music", "email"], default="none",
        help="抢票提醒方式，none-无提醒，music-音效提醒"
    )

    return parser.parse_args()


def play_music(fpath: str):
    from playsound import playsound
    playsound(fpath)


def execute_command(command: List[str]):
    process = subprocess.run(command, capture_output=True)

    try:
        process.check_returncode()
    except subprocess.CalledProcessError as e:
        error_msg = process.stderr.decode("utf-8")
        logger.error(
            f"运行命令: {command}报错，错误信息为: {error_msg}"
        )
        raise e

    return process.stdout


class Instance(object):
    def __init__(self, instance_id: str, name: str, gpu: str, unit_price: str, status: str):
        self.id = instance_id
        self.name = name
        self.gpu = gpu
        self.unit_price = unit_price
        self.status = status

    def idle(self) -> bool:
        return self.status == "online"


class FeaturizeClient(object):
    def __init__(self, token: str) -> None:
        self.token = token

    def get_all_machine(self) -> List[Instance]:
        stdout = execute_command([
            "featurize",
            "--token", self.token,
            "instance", "ls", "-r"
        ])

        instance_list = json.loads(stdout)["records"]
        return [
            Instance(
                ins["id"],
                ins["name"],
                ins["gpu"].split(",")[0],
                ins["unit_price"],
                ins["status"]
            ) for ins in instance_list
        ]

    def get_all_availabel_machine(self) -> List[Instance]:
        return [ins for ins in self.get_all_machine() if ins.idle()]

    def request_instance(self, ins: Instance) -> bool:
        try:
            execute_command([
                "featurize",
                "--token", self.token,
                "instance", "request", ins.id,
            ])
        except subprocess.CalledProcessError:
            return False

        return True
        

def main():
    args = parse_parser()

    client = FeaturizeClient(args.token)

    gpus = [gpu.strip() for gpu in args.gpus.split(",")]

    logger.info(
        f"本次获取实例目标:\n"
        f"\tGPU类型: {gpus}\n"
        f"\t获取实例数量: {args.num_machine}\n"
        f"\t查询间隔: {args.interval}"
    )
    left_num = args.num_machine
    gpu_set = set(gpus)
    gpu_prio_dict = {gpu: idx for idx, gpu in enumerate(gpus)}

    try:
        requested_gpu_records = defaultdict(int)
        while left_num:
            available_ins_list = client.get_all_availabel_machine()
            sorted_avai_ins_list = sorted(
                available_ins_list,
                key=lambda x: gpu_prio_dict.get(x.gpu, 1e5),
            )

            valid_ins_list = [
                ins for ins in sorted_avai_ins_list if ins.gpu in gpu_set
            ]

            if valid_ins_list:
                logger.info(f"查询到有效实例数量: {len(valid_ins_list)}")
            else:
                logger.info(
                    f"无有效实例，GPU类型为"
                    f": {set(ins.gpu for ins in available_ins_list)} "
                    f"目标类型为: {gpu_set}"
                )

            for ins in valid_ins_list:
                if left_num == 0:
                    break

                success = client.request_instance(ins)
                if success:
                    if args.notification == "music":
                        play_music(os.path.join(file_dir, "source/success.mp3"))

                    requested_gpu_records[ins.gpu] += 1
                    left_num -= 1

            time.sleep(args.interval)
    except Exception as e:
        if isinstance(e, KeyboardInterrupt):
            raise e

        if args.notification == "music":
            play_music(os.path.join(file_dir, "source/error.mp3"))

        raise e
    finally:
        gpu_info = ", ".join(
            [f"{gpu}: {num}" for gpu, num in requested_gpu_records.items()]
        )

        logger.info(
            f"本次获取结果: \n"
            f"\t目标获取机型数量 {args.num_machine}, 实际获取机型数量 {args.num_machine - left_num}\n"
            f"\t获取实例gpu分布:\n"
            f"\t\t{gpu_info}"
        )


if __name__ == "__main__":
    main()
