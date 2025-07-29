# -*- coding: utf-8 -*-
"""
    Session
    ~~~~~~~~~~~~~~~~~~
    连接控制

    Log:
        2025-04-23 3.2.0 Me2sY  默认关闭 heartbeat

        2024-09-22 1.6.0 Me2sY  支持视频帧回调方法

        2024-08-29 1.4.0 Me2sY
            创建，支持连接监控，断线重连，加载配置连接等功能
"""

__author__ = 'Me2sY'
__version__ = '3.2.0'

__all__ = [
    'Session'
]

import threading
import time
from typing import Callable

import av
from adbutils import AdbDevice, AdbError
from loguru import logger

from myscrcpy.core.video import *
from myscrcpy.core.audio import *
from myscrcpy.core.control import *


class Session:
    """
        Scrcpy Connect Session
    """

    def __init__(
            self,
            adb_device: AdbDevice,
            video_args: VideoArgs = None,
            audio_args: AudioArgs = None,
            control_args: ControlArgs = None,
            heartbeat: bool = False,
            frame_update_callback: Callable = None,
            **kwargs
    ):
        self.adb_device = adb_device

        self.ca = None if control_args is None else ControlAdapter.connect(self.adb_device, control_args)
        self.aa = None if audio_args is None else AudioAdapter.connect(self.adb_device, audio_args)
        self.va = None if video_args is None else VideoAdapter.connect(
            self.adb_device, video_args, frame_update_callback
        )

        if self.ca is None and self.aa is None and self.va is None:
            raise RuntimeError(f"At Least One Adapter Required!")

        self.is_running = True
        self.is_loss = False

        if heartbeat:
            threading.Thread(target=self.heartbeat, kwargs=kwargs).start()

    def __del__(self):
        try:
            self.disconnect()
        except:
            ...

    @classmethod
    def connect_by_configs(
            cls,
            adb_device: AdbDevice,
            frame_update_callback: Callable[[av.VideoFrame, int], None] = None,
            **kwargs):
        """

        :param adb_device:
        :param frame_update_callback:
        :param kwargs:
        :return:
        """
        return cls(
            adb_device,
            video_args=VideoArgs.load(**kwargs) if kwargs.get('video', False) else None,
            audio_args=AudioArgs.load(**kwargs) if kwargs.get('audio', False) else None,
            control_args=ControlArgs.load(**kwargs) if kwargs.get('control', False) else None,
            frame_update_callback=frame_update_callback,
            **kwargs
        )

    def reconnect(self):
        """
            重连
        :return:
        """
        self.disconnect()
        for _ in [self.ca, self.aa, self.va]:
            if _ is None:
                continue
            _.start(self.adb_device)

        self.is_running = True

    def disconnect(self):
        """
            断开连接
        :return:
        """
        try:
            self.ca.stop()
        except Exception as e:
            ...

        try:
            self.aa.stop()
        except Exception as e:
            ...

        try:
            self.va.stop()
        except Exception as e:
            ...

        self.is_running = False

    def heartbeat(self, auto_reconnect: bool = True, wait_sec: int = 5, retry_n: int = 12, **kwargs):
        """
            监控及重连
        :param auto_reconnect: 自动重连
        :param wait_sec:
        :param retry_n:
        :return:
        """
        _retry_n = retry_n
        while self.is_running or self.is_loss:
            if retry_n < 0:
                self.is_running = False
                logger.error(f"Session Lost Connect!")
                break

            try:
                assert '1' == str(self.adb_device.shell('echo 1', timeout=3))

                # Auto Reconnect
                if self.is_loss and auto_reconnect:
                    self.reconnect()

                self.is_loss = False
                retry_n = _retry_n

            except (AdbError, AssertionError) as e:
                logger.warning(f"Session Heartbeat Error => {e}")
                self.is_loss = True
                if auto_reconnect:
                    retry_n -= 1
                else:
                    retry_n = -1

            time.sleep(wait_sec)

    @property
    def is_video_ready(self) -> bool:
        return self.va is not None and self.va.is_ready

    @property
    def is_audio_ready(self) -> bool:
        return self.aa is not None and self.aa.is_ready

    @property
    def is_control_ready(self) -> bool:
        return self.ca is not None and self.ca.is_ready


if __name__ == '__main__':
    """
        DEMO Here
    """
    from adbutils import adb
    d = adb.device_list()[0]

    sess = Session.connect_by_configs(
        d,
        **{'video': True, 'audio': True},
        **VideoArgs().dump(),
        **AudioArgs(audio_codec=AudioArgs.CODEC_RAW).dump()
    )

    # sess = Session(d, video_args=VideoArgs(1200), audio_args=AudioArgs(), control_args=ControlArgs())

    # sess.disconnect()
