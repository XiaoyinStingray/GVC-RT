
import os
import glob
import sys
from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension


cxx_flags = ["-O3", "-std=c++20"]
nvcc_flags = ["-O3", "--use_fast_math", "--extra-device-vectorization", "-arch=native",
              # kernel.cu 在 lambda 里捕获了 structured binding（auto [a,b] = ...），
              # C++17 下是非法的（gcc 宽容、nvcc 11.8 直接报错），C++20 才合法。
              "-std=c++20"]
if sys.platform == 'win32':
    cxx_flags = ["/O2"]


setup(
    name='inference_extensions_cuda',
    ext_modules=[
        CUDAExtension(
            name='inference_extensions_cuda',
            sources=glob.glob('*.cpp') + glob.glob('*.cu'),
            extra_compile_args={
                "cxx": cxx_flags,
                "nvcc": nvcc_flags,
            },
        ),
    ],
    cmdclass={
        'build_ext': BuildExtension
    }
)
