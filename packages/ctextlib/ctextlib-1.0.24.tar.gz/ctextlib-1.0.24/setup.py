import os
import re
import sys
import platform
import subprocess
import setuptools
import io
import sysconfig
import shutil

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from distutils.version import LooseVersion

class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        super(CMakeExtension, self).__init__(name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)

class CMakeBuild(build_ext):
    def run(self):
        try:
            out = subprocess.check_output(['cmake', '--version'])
            cmake_version = LooseVersion(re.search(r'version\s*([\d.]+)', out.decode()).group(1))
            print("Detected CMake version:", cmake_version)
        except OSError:
            raise RuntimeError("CMake must be installed to build the following extensions: " +
                               ", ".join(e.name for e in self.extensions))

        if platform.system() == "Windows" and cmake_version < LooseVersion("3.5.0"):
            raise RuntimeError("CMake >= 3.5.0 is required on Windows")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        cfg = 'Debug' if self.debug else 'Release'

        cmake_args = [
            "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={0}".format(extdir),
            "-DPYTHON_EXECUTABLE={0}".format(sys.executable)
        ]

        build_args = ['--config', cfg]

        if platform.system() == "Windows":
            cmake_args += ["-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{0}={1}".format(cfg.upper(), extdir)]
            arch = 'x64' if sys.maxsize > 2**32 else 'Win32'
            cmake_args += ['-A', arch]
            build_args += ['--', '/m']
        else:
            cmake_args += ["-DCMAKE_BUILD_TYPE={0}".format(cfg)]
            build_args += ['--', '-j2']

        env = os.environ.copy()
        env['CXXFLAGS'] = '{0} -DVERSION_INFO=\\"{1}\\"'.format(env.get("CXXFLAGS", ""), self.distribution.get_version())

        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)

        cmake_path = shutil.which("cmake") or os.path.join(sysconfig.get_path('scripts'), 'cmake')
        print("Using cmake path: {0}".format(cmake_path))

        subprocess.check_call([cmake_path, ext.sourcedir] + cmake_args, cwd=self.build_temp, env=env)
        subprocess.check_call([cmake_path, '--build', '.'] + build_args, cwd=self.build_temp)

# Load long description
with io.open("README.md", 'r', encoding='utf8') as f:
    long_description = f.read()

# Optional: wheel support
try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            super(bdist_wheel, self).finalize_options()
            self.root_is_pure = False
except ImportError:
    bdist_wheel = None

setup(
    name='ctextlib',
    version='1.0.24',
    author='Anton Milev',
    author_email='amil@abv.bg',
    description='Python package with CText C++ extension',
    long_description=long_description,
    long_description_content_type="text/markdown",
    ext_modules=[CMakeExtension('cmake_ctextlib')],
    cmdclass={
        'bdist_wheel': bdist_wheel,
        'build_ext': CMakeBuild,
    },
    zip_safe=False,
    url="https://github.com/antonmilev/CText",
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: C++',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[],
    python_requires='>=3.5',
)