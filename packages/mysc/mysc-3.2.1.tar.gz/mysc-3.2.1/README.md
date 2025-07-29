# MYScrcpy V3.2.1

### [README in English](https://github.com/me2sy/MYScrcpy/blob/main/README_EN.md)

### python语言实现的一个 [**Scrcpy 3.2**](https://github.com/Genymobile/scrcpy/) 客户端

包含完整的视频、音频、控制解析，**开发友好，引入即用！**

**V3.2.1** GUI采用 [**Kivy**](https://kivy.org/) / [**KivyMD**](https://kivymd.readthedocs.io/en/latest/) 

现代化界面风格，支持Windows/Ubuntu(X11)/MacOSX，支持多设备连接，鼠标及键盘映射。


**V1.7.0** 采用 [**DearPyGui**](https://github.com/hoffstadt/DearPyGui) 作为主要GUI。 支持编写插件，窗口位置记忆、右键手势控制、断线重连、文件管理器、虚拟摄像头投屏、中文输入，锁屏密码解锁等功能。

高速模式使用[**pygame**](https://www.pygame.org/)作为鼠标及键盘控制映射GUI。提供鼠标隐藏、按键事件监听等功能， 适用于第一人称相关应用的按键映射。

[**点击查看V1.7.0版本介绍**](/files/doc/README_V17.md)


V3.2.1 主界面
![dpg Screenshot](/files/images/v3/main.png)


## V3.2.1 功能特性
- 支持多设备连接，切换
- 全中文界面
- 按键映射编辑器
- 窗口大小/位置记忆功能
- 相较V1.7.0，大幅降低CPU/GPU占用，接近scrcpy原生水平

### 开发
- 3.2.0 适配Scrcpy 3.2
- 1.7.0 适配Scrcpy 2.7，支持Gamepad
- 1.6.5 [插件开发教程](https://blog.csdn.net/weixin_43463913/article/details/142685828)
- 1.6.4 统一鼠标、键盘回调方法及传参，增加过滤器
- 1.6.4 自定义插件加载路径，方便插件开发
- 1.6.3 新增鼠标抢夺模式，允许插件获取鼠标控制权，实现更多功能
- 功能说明 [Window.setup_session()](/files/doc/introduce/window__setup_session.md)
- 全新插件架构！支持配置文件注入等功能 [**帮助文档**](https://github.com/me2sy/MYScrcpy/blob/main/files/doc/help/extensions/Help_extensions_v1_6.md)
- 升级KVManager ValueManager，自动注册，自动管理 
- 整合[uiautomator2](https://github.com/openatx/uiautomator2)
- 支持获取视频、音频原格式流，方便二次开发
- 开箱即用 `pip install mysc[full]`
- 使用Session/Connection/Adapter/Args架构，一行代码获取图像
  - `Session(adb_device, video_args=VideoArgs(1200)).va.get_image()`
- 按需最小化引用。支持**Termux**上安装部署服务，支持局域网WEB浏览，[**安装部署教程**](files/doc/MYScrcpy_with_Termux.md)

### GUI
- 根据设备及当前连接参数，自动记忆窗口大小，同时记忆窗口旋转前位置。在横竖屏切换时，无需频繁调整窗口位置
- 支持Windows/Linux/MacOS X
- 支持有线、无线连接设备
- 支持设置无线端口，设置后自动重连功能
- 支持加载历史连接记录功能，自动记忆历史连接记录，快速连接
- 可根据设备配置相应连接模式，保存连接参数
  - 例如若使用手机摄像头模式，则video/audio配置，control关闭，并保存为Camera配置组合
  - 使用投屏，则全部配置，并保存为投屏配置组合

### 视频
- 支持h264/h265视频流解析
- 支持按比例调整窗口大小
  - 拉动窗口，进行自由伸缩
  - 根据高度/宽度，自动调整窗口至视频比例

### 音频
- 支持opus/flac/raw

### 控制
- 优化鼠标控制器
  - 使用 F9 切换 UHID/触摸模式
  - 支持手势切换功能空间 手势：DR
- 新增键盘切换器
  - 使用 F8 切换 UHID/ADB/Ctrl模式， F7 切换 控制空间
  - 支持插件配置注入
- 按键映射创建工具，支持键盘，鼠标等多种控制映射方式，Windows/Linux/MacOS X 适用
- 支持UHID鼠标，可以实现Android界面中鼠标与PC混用
- 支持UHID-Keyboard，模拟外接键盘，直接输入中文（百度、搜狗输入法测试通过）
- 支持鼠标滚轮滑动，缩放等功能
- 支持右键手势判断，快速回退、截屏、控制音乐播放
  - 支持创建第二个虚拟点，配合左键模拟两指操作
- 侧边栏多种功能键

## 帮助与支持

在使用中有任何问题、想法及建议，欢迎通过以下方式与我联系：

#### QQ群：579618095
![579618095](files/images/qq_group.jpg)

#### 邮箱：Me2sY@outlook.com

#### Blog: [CSDN](https://blog.csdn.net/weixin_43463913)


## 基本使用

### 1.1 pypi直接安装使用（推荐）

**注意 V3.2.X以上 采用KivyMD 2.X版本 需手动安装**

[KivyMD getting-started](https://kivymd.readthedocs.io/en/latest/getting-started/)

```bash
# 完整安装
pip install mysc[full]
# NOT myscrcpy... my-scrcpy already exists in pypi...

# V3.2.0 采用 KivyMD 2.X 版本，需手动安装
pip install https://github.com/kivymd/KivyMD/archive/master.zip

# 仅核心
pip install mysc

# 支持flac
pip install mysc[flac]

# 支持opus
pip install mysc[opus]

# 若使用界面 则：
pip install mysc[gui]

# 若使用web demo 则：
pip install mysc[web]

# 可按需组合，例如
pip install mysc[gui, opus, web]

#安装完成后
# Gui 及 日志 console
# V3.2.0 Kivy
mysc-k-cli

# 无Console
# V3.2.0 Kivy
mysc-k
```

### 1.2  克隆本项目至本地或下载release package， 使用pip安装所需包
```bash
pip install mysc-X.X.X.tar.gz
pip install loguru adbutils==2.7.2 numpy av pyaudio

# GUI
pip install kivy>=2.3.1
pip install https://github.com/kivymd/KivyMD/archive/master.zip
pip install pyperclip moosegesture pynput

# Web GUI
pip install nicegui

# 使用flac
pip install pyflac

# 使用opus
pip install pyogg opuslib
```

### 2. 项目结构：
   1. **utils/**
   定义基本工具类及各类参数
   2. **gui/dpg**
   DearPyGui 界面实现，包括视频绘制，鼠标事件，UHID鼠标、键盘输入，映射编辑等。
   3. **gui/pg**
   pygame 界面实现，包括视频绘制、鼠标事件、键盘事件控制等。
   4. **gui/ng**
   Nicegui Web UI (DEMO)
   5. **core/***
   Session、Connection、视频流、音频流、控制流、设备控制器等核心包
   6. **extensions/**
   官方插件
   7. **~/.myscrcpy/***
   本地化配置文件，包括运行类文件*.db 按键映射文件 tps/*.json
   8. **tools/***
   工具类，多用于生成CLI
   9. **gui/k**
   V3.2 Kivy/KivyMD 界面实现，包括视频绘制，鼠标事件，UHID鼠标、键盘输入，映射编辑等。

### 3. 程序引用使用，便于自行开发

```python
# 1.4.X 新 Core/Session 架构，推荐使用

from adbutils import adb

from myscrcpy.core import *
from myscrcpy.utils import *

# Connect to Scrcpy
# Create a Session

adb_device = adb.device_list()[0]
# 或者使用 myscrcpy提供的高级设备管理工厂创建
# DeviceFactory.load_devices()
# adv_device = DeviceFactory.device_list()[0]
# adb_device = adb_device.adb_dev

session = Session(
   adb_device,
   video_args=VideoArgs(max_size=1200),
   audio_args=AudioArgs(),
   control_args=ControlArgs()
)


# Get RGB Frame np.ndarray
frame = session.va.get_frame()

# Get PIL.Image
image = session.va.get_image()

session.ca.f_set_screen(True)

session.ca.f_touch_spr(
   Action.DOWN,
   ScalePointR(.5, .5, 0),
   touch_id=0x0413
)


# 1.5.8 NEW
# 获取原始视频流/音频流
video_conn = VideoAdapter.raw_stream(adb_device, VideoArgs(max_size=1366, video_codec=VideoArgs.CODEC_H264))
while True:
    video_raw_bytes = video_conn.recv(1024)
    # Your Code Here
    break
video_conn.disconnect()

audio_conn = AudioAdapter.raw_stream(adb_device, AudioArgs(audio_codec=AudioArgs.CODEC_OPUS))
while True:
    audio_raw_bytes = audio_conn.recv(1024)
    # Your Code Here
    break
audio_conn.disconnect()

...
```

### 4.使用GUI

:exclamation: _Ubuntu等Linux下 使用pyaudio 需要先安装portaudio_
```bash
sudo apt install build-essential python3-dev ffmpeg libav-tools portaudio19-dev
```

#### 运行GUI
```bash
mysc-k-cli # With Log Console
mysc-k # Only GUI
```

#### 运行Nicegui DEMO
```bash
python -m myscrcpy.gui.ng.main
```


## 程序截图

### 主界面
![dpg Screenshot](/files/images/v3/main.png)

### 右键手势功能
![right](/files/images/v3/ges.png)

### Nicegui Web 界面（DEMO）
![Nicegui Demo](/files/images/Nicegui_DEMO.jpg)

### 按键映射编辑器
![Touch Proxy Editor](/files/images/v3/proxy.png)

### 连接配置界面
![Connect](/files/images/v3/config.png)


## 所思所想

2025-05-10 V3.2.0 近期喜得小宝，更新的进度慢了许多。感谢大家的理解与支持。转眼50+星了，你们的支持和鼓励是我继续下去的动力！再次谢谢大家！

作为从 Scrcpy 1.X时代就开始使用的老玩家，感叹于Scrcpy的发展及神奇的功能的同时，也一直想做点什么。不过碍于有其他项目（~~懒~~）一直迟迟没有动手。 
直到遇到了[Scrcpy Mask](https://github.com/AkiChase/scrcpy-mask) 这一优秀项目，感觉我也要做点什么了。

遂于24年6月1日开始，阅读Scrcpy源码，使用python语言，借由pyav、adbutils、numpy、pyflac等优秀工具包，形成了MYScrcpy这一项目。

开发初期，是想解决在某些场景下，鼠标操作映射相关问题。随着不断开发，也产生许多涉及图形分析、AI接入（YOLO）、自动控制等方向的新想法。

MYScrcpy是MY（Mxx & ysY）系列的开始，接下来，将继续开发完善这一项目及相关应用。

目前项目为个人开发，时间、精力、水平有限，功能说明等文档方面会逐步完善。欢迎大家使用及指正。也可通过邮箱联系。如果后续有需要，也可以建群联系。

欢迎访问我的 [Bilibili](https://space.bilibili.com/400525682)，之后会录制一些操作及讲解视频，希望大家喜欢。

最后十分感谢我的挚爱YSY在开发中给予的支持。 :heart_eyes:


## 鸣谢

感谢 [**Scrcpy**](https://github.com/Genymobile/scrcpy/) 项目及作者 [**rom1v**](https://github.com/rom1v)，在这一优秀项目基础上，才有了本项目。

感谢 Kivy/KivyMD Dearpygui Pygame等优秀GUI框架

感谢使用到的各个包项目及作者们。有你们的付出，才有了如此好的软件开发环境。

同时感谢各位使用者们，谢谢你们的支持与帮助，也希望MYScrcpy成为你们得心应手的好工具，好帮手。


## 声明

本项目供日常学习（图形、声音、AI训练等）、Android测试、开发等使用。

**请一定注意：**

1.开启手机调试模式存在一定风险，可能会造成数据泄露等风险，使用前确保您了解并可以规避相关风险

**2.本项目不可用于违法犯罪等使用**

**本人及本项目不对以上产生的相关后果负相关责任，请斟酌使用。**


## 更新日志
- 3.2.1
  - 屏蔽 Kivy BUG导致的问题
  - adbutils 更新至 2.8.10
  - 更改 配置文件保存地址，避免因权限问题导致无法存储
  - 增加连接友好提示
- 3.2.0
  - 支持Scrcpy 3.2.0
  - 全新现代风格界面，使用Kivy/KivyMD，大幅降低CPU/GPU占用
  - 全新映射编辑器
  - 修复部分缺陷
- 1.7.0
  - 支持Scrcpy 2.7
  - 支持UHID Gamepad
  - 升级支持 dearpygui 2.X
  - 新增Unlocker工具
  - 修复部分缺陷
- 1.6.6
  - VirtualCam 新增范围选择及运行状态提示
  - 修复部分缺陷
- 1.6.5
  - 支持连接虚拟机
- 1.6.4
  - 统一鼠标、键盘回调函数及传参
  - 新增指定加载插件路径
  - Capture 新增微调功能
- 1.6.3 
  - 插件功能升级
  - 鼠标支持独占模式
  - 修复部分缺陷
- 1.6.2 VirtualCam 插件化
- 1.6.1 修复缺陷
- 1.6.0
  - 接入[uiautomator2](https://github.com/openatx/uiautomator2)
  - 键盘控制器、鼠标控制器
  - 日志管理器
  - 修复窗口调整时跳动缺陷，DPG崩溃缺陷
  - 全新插件体系，插件注入，插件管理器等
- 1.5.10 支持插件
- 1.5.9 新增文件管理器，支持设备文件管理，下载、上传及预览
- 1.5.8 支持文件/文件夹/截屏一键拷贝至设备
- 1.5.8 支持输出原始视频/音频流
- 1.5.7 CLI启动虚拟摄像头
- 1.5.5 优化Nicegui界面，方便termux使用
- 1.5.4 降低CPU占用
- 1.5.3 更新 Readme 文件
- 1.5.3 支持Opus音频解析
- 1.5.0 现已上线 [**pypi**](https://pypi.org/project/mysc/)
- 1.4.2 使用[moosegesture](https://github.com/asweigart/moosegesture)实现右键手势控制功能，支持模拟第二个点、画线后退、调整音量、播放媒体等功能
- 1.4.1 改用SQLite进行配置管理
- 1.4.0 
  - 久等了！全新Core/Session/Connection/Utils架构
  - 新增窗口位置记忆功能，记录旋转前位置
  - 支持心跳检测，自动断线重连
  - 现已支持设备->PC 剪贴板
  - 优化按键映射方式，Linux适用
  - 更多控制按钮
- 1.3.6 新增网页端设备浏览页面DEMO(Nicegui),支持鼠标输入，UHID键盘输入、ADB输入及摇杆模拟鼠标输入
- 1.3.3 新增选择音频输出设备功能，可配合VB-Cables模拟麦克风输入
- 1.3.2 新增[pyvirtualcam](https://github.com/letmaik/pyvirtualcam?tab=readme-ov-file),支持OBS虚拟摄像头
- 支持连接配置保存，窗口大小保存
- 支持无线连接，历史连接记录及快速连接功能，告别繁琐命令行
- 支持按比例调整窗口大小、任意拉伸等功能
- 支持有线、无线连接安卓设备
- 支持断线重连，连接历史记录并自动尝试连接功能
- 支持 H265连接
- 实现了视频流解析（H264），生成numpy.ndarray，可自行使用opencv、image等进行图形处理
- 实现了音频流解析（FLAC）, 使用 [pyflac](https://github.com/sonos/pyFLAC) 解码，[pyaudio](https://people.csail.mit.edu/hubert/pyaudio/) 播放
- 实现了控制按键映射，鼠标映射
- 实现了UHID-Mouse与鼠标点击混用，可以实现Android界面中鼠标与PC混用模式
- 实现了UHID-Keyboard，支持模拟外接键盘，直接输入中文（搜狗输入法测试通过）
- 实现了DPG GUI下，鼠标滚轮缩放、滑动等功能
- 实现了设备锁屏下，通过InputPad输入密码解锁功能
- DPG GUI下设备翻转图像自动调整，无限制拉伸缩放等功能
- 实现了Ctrl调节鼠标移动速度功能
- 采用TwinWindow思路，解决DPG控件无法重叠问题，实现DPG控制映射编辑器（TPEditor）
- 纯Pygame控制模式下，最低延迟在6ms


## 开发计划

- APK管理器
- 使用范例及教程
- twisted / fastapi 接口
- YOLO 及 快速拉框导出等训练工具
- 视频、音频录制
- WebRTC