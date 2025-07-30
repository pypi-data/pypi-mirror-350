import datetime as dt
from setuptools import setup, Extension

now = dt.datetime.now()
nowstr = now.astimezone().strftime("%Y-%m-%d %H:%M %z")
extra_arg = f'-DCOMPILE_TIME="{nowstr}"'

sources = [
    "src/hex.c",
    "src/hls.c",
    "src/hsv.c",
    "src/lab.c",
    "src/luminance.c",
    "src/luv.c",
    "src/rgb.c",
    "src/xyz.c",
    "src/rgbxyzlabmodule.c",
    ]

headers = [
    "src/hex.h",
    "src/hls.h",
    "src/hsv.h",
    "src/lab.h",
    "src/luminance.h",
    "src/luv.h",
    "src/rgb.h",
    "src/vector3.h",
    "src/version.h",
    "src/xyz.h",
]

ext_module = Extension('rgbxyzlab._rgbxyzlab',
                       sources = sources,
                       language="c",
                       extra_compile_args = [extra_arg],
                       libraries=['m'],
                       )

setup(ext_modules=[ext_module], include_package_data=False)
