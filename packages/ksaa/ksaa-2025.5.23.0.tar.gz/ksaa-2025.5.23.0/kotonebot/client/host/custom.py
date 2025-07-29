import os
import subprocess
from psutil import process_iter
from .protocol import HostProtocol, Instance
from typing import Optional, ParamSpec, TypeVar, TypeGuard
from typing_extensions import override

from kotonebot import logging
from kotonebot.client.device import Device

logger = logging.getLogger(__name__)

P = ParamSpec('P')
T = TypeVar('T')

class CustomInstance(Instance):
    def __init__(self, exe_path: str, emulator_args: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exe_path: str = exe_path
        self.exe_args: str = emulator_args
        self.process: subprocess.Popen | None = None

    @override
    def start(self):
        if self.process:
            logger.warning('Process is already running.')
            return

        if self.exe_args:
            logger.info('Starting process "%s" with args "%s"...', self.exe_path, self.exe_args)
            cmd = f'"{self.exe_path}" {self.exe_args}'
            self.process = subprocess.Popen(cmd, shell=True)
        else:
            logger.info('Starting process "%s"...', self.exe_path)
            self.process = subprocess.Popen(self.exe_path)

    @override
    def stop(self):
        if not self.process:
            logger.warning('Process is not running.')
            return
        logger.info('Stopping process "%s"...', self.process.pid)
        self.process.terminate()
        self.process.wait()
        self.process = None

    @override
    def running(self) -> bool:
        if self.process is not None:
            return True
        else:
            process_name = os.path.basename(self.exe_path)
            p = next((proc for proc in process_iter() if proc.name() == process_name), None)
            if p:
                return True
            else:
                return False

    @override
    def refresh(self):
        pass

    def __repr__(self) -> str:
        return f'CustomInstance(#{self.id}# at "{self.exe_path}" with {self.adb_ip}:{self.adb_port})'

def _type_check(ins: Instance) -> CustomInstance:
    if not isinstance(ins, CustomInstance):
        raise ValueError(f'Instance {ins} is not a CustomInstance')
    return ins

def create(exe_path: str, adb_ip: str, adb_port: int, adb_name: str, emulator_args: str = "") -> CustomInstance:
    return CustomInstance(exe_path, emulator_args=emulator_args, id='custom', name='Custom', adb_ip=adb_ip, adb_port=adb_port, adb_name=adb_name)


if __name__ == '__main__':
    ins = create(r'C:\Program Files\BlueStacks_nxt\HD-Player.exe', '127.0.0.1', 5555, '**emulator-name**')
    ins.start()
    ins.wait_available()
    input('Press Enter to stop...')
    ins.stop()
