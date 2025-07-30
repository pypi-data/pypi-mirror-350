import os
import setuptools
import sys
import platform, shutil
from setuptools import find_packages, setup, Extension
from setuptools.command.build_ext import build_ext as build_ext_orig
from setuptools.command.install_lib import install_lib as install_lib_orig
from subprocess import check_output
from shutil import copyfile
import sysconfig
import pathlib

class CMakeExtension(Extension):
    def __init__(self, name, sources=[]):
        Extension.__init__(self, name=name, sources=sources)

def get_hepmc3_version():
    line = "#define HEPMC3_VERSION_CODE 3003000"
    current = os.getcwd()
    with open(current + "/include/HepMC3/Version.h") as f:
        line = next(
            (l for l in f if "HEPMC3_VERSION_CODE" in l and "#define " in l), None
        )
    number = int(line.split(" ")[2])
    return (
        str(int(number / 1000000))
        + "."
        + str(int((number % 1000000) / 1000))
        + "."
        + str((number % 1000))
    )
def get_hepmc3_so_version(arg):
    if arg == "search":
       return str(5)
    return str(4)    

def get_install(whe,wha,glo=True):
    if glo:
      examples=[ a.as_posix() for a in  list(pathlib.Path(wha).rglob("*"))  if a.is_file() ]
    else:
      examples=[ a.as_posix() for a in  list(pathlib.Path(wha).glob("*"))  if a.is_file() ]
    return [(whe, examples)]

def get_install_rec(whe,wha):
    dirs = [ a.as_posix() for a in  list(pathlib.Path(wha).rglob("*"))  if a.is_dir() ]
    xx=[]
    for dr in dirs:
      xx+=[( os.path.join(whe,dr) , [ a.as_posix() for a in  list(pathlib.Path(dr).glob("*"))  if a.is_file() ],) ]
    return xx
    
def get_library_location():
    ps = platform.system()
    bits = platform.architecture()[0]
    if ps == "Linux" and bits == "64bit":
        return "lib64"
    if ps == "Solaris" or ps == "FreeBSD" or ps == "Darwin" or ps == "Windows" or (ps == "Linux" and bits == "32bit"):
        return "lib"
    return "lib"

def get_hepmc3_libraries():
    lib = get_library_location()
    ps = platform.system()
    if ps == "Darwin":
        return [(lib,[ os.path.normpath( "outputs/" + lib + "/" + x) for x in ['libHepMC3.dylib','libHepMC3search.dylib','libHepMC3-static.a','libHepMC3search-static.a']],)]
    if ps == "Windows" :
        if  (os.environ.get('MSYSTEM') is None):
          return [(lib,[ os.path.normpath( "outputs/" + lib + "/" + x) for x in ['HepMC3.dll','HepMC3search.dll','HepMC3search-static.lib','HepMC3-static.lib']],)]
        else:
          return [(lib,[ os.path.normpath( "outputs/" + lib + "/" + x) for x in ['libHepMC3.dll.a','libHepMC3.dll','libHepMC3search.dll.a','libHepMC3search.dll','libHepMC3search-static.a','libHepMC3-static.a']],)]
    return [(lib,[ os.path.normpath( "outputs/" + lib + "/" + x) for x in ['libHepMC3.so','libHepMC3.so.'+get_hepmc3_so_version(""),'libHepMC3search.so','libHepMC3search.so.'+get_hepmc3_so_version("search")]],)]

class hm3_install_lib(install_lib_orig):
    def run(self):
        cwd = os.path.abspath(os.getcwd())
        v = sys.version_info
        versionstring = str(v[0]) + "." + str(v[1]) + "." + str(v[2])
        shutil.copytree(
            os.path.normpath(os.path.join(cwd, "python", "A", versionstring, "pyHepMC3")),
            os.path.normpath(os.path.join(cwd, self.build_dir, "pyHepMC3")),
        )
        print(install_lib_orig.get_outputs(self))
        print(self.install_dir)
        print(self.build_dir)
        install_lib_orig.run(self)


class hm3_build_ext(build_ext_orig):
    def get_ctest_exe(self):
        return "ctest"

    def get_cmake_exe(self):
      for ex in ['cmake','cmake3']:
        vg = "0"
        cmakeg_exe = ""
        outg = check_output([ex, "--version"])
        outgsplit = outg.split()
        if len(outgsplit) > 2:
            vg = outgsplit[2]
            if int(vg[0]) >= 3:
                cmakeg_exe = ex
        if cmakeg_exe != "":
            return cmakeg_exe
      return "foo "

    def get_cmake_python_flags(self):
        pv = sys.version_info
        return "-DHEPMC3_PYTHON_VERSIONS=" + str(pv[0]) + "." + str(pv[1])

    def run(self):
        for ext in self.extensions:
            self.build_cmake(ext)

    def build_cmake(self, ext):
        build_temp = os.getcwd()
        cwd = os.path.abspath(os.getcwd())
        cmake_exe = self.get_cmake_exe()
        ctest_exe = self.get_ctest_exe()
        cmake_args = [
            "CMakeLists.txt",
            "-DHEPMC3_BUILD_EXAMPLES:BOOL=ON",
            "-DHEPMC3_INSTALL_INTERFACES:BOOL=ON",
            "-DHEPMC3_ENABLE_SEARCH:BOOL=ON",
            "-DHEPMC3_BUILD_DOCS:BOOL=OFF",
            "-DHEPMC3_ENABLE_PYTHON:BOOL=ON",
            "-DHEPMC3_ENABLE_ROOTIO:BOOL=OFF",
            "-DCMAKE_BUILD_TYPE=Release",
            "-DHEPMC3_ENABLE_TEST:BOOL=ON",
            self.get_cmake_python_flags(),
        ]
        ps = platform.system()
        bits = platform.architecture()[0]
        # Workaround for the manulinux
        if ps == "Linux":
            cmake_args.append("-DCMAKE_POSITION_INDEPENDENT_CODE=ON")
            cmake_args.append("-DHEPMC3_USE_STATIC_LIBS_FOR_PYTHON=ON")
            cmake_args.append(
                "-DPython"
                + str(sys.version_info[0])
                + "_INCLUDE_DIR="
                + sysconfig.get_path("include")
            )
            cmake_args.append(
                "-DPython"
                + str(sys.version_info[0])
                + "_ARTIFACTS_INTERACTIVE:BOOL=TRUE"
            )
            cmake_args.append("-DPython_INCLUDE_DIR=" + sysconfig.get_path("include"))
            cmake_args.append("-DPython_ARTIFACTS_INTERACTIVE:BOOL=TRUE")

        if ps == "Linux" and bits == "64bit":
                cmake_args.append("-DLIB_SUFFIX=64")
                cmake_args.append("-DCMAKE_INSTALL_LIBDIR=lib64")
        if ps == "Windows" and (os.environ.get('MSYSTEM') is None):
            # FIXME: detect arch
            cmake_args.append("-Thost=x64")
            cmake_args.append("-A")
            cmake_args.append("x64")
        cmake_args.append("-DPython"+str(sys.version_info[0])+"_ROOT_DIR="+ os.path.dirname(sysconfig.get_path("scripts")))
        self.spawn([cmake_exe, str(cwd)] + cmake_args)

        if not self.dry_run:
            build_args = []
            self.spawn([cmake_exe, "--build", "."] + build_args)
            for a in list(pathlib.Path(".").rglob("*Targets*.cmake")): 
               copyfile(a, os.path.join(os.getcwd(),"outputs","share","HepMC3","cmake",os.path.basename(a)))
            ctest_args = []
            v = sys.version_info
            if ps == "Windows":
                ctest_args.append("-C")
                ctest_args.append("Debug")
                ctest_args.append("-j1")
            if ps != "Darwin" and (os.environ.get('MSYSTEM') is  None):
                self.spawn([ctest_exe, ".", "--output-on-failure"] + ctest_args)
        os.chdir(str(cwd))

def local_find_packages():
    os.mkdir("pyHepMC3")
    return ["pyHepMC3"]


setuptools.setup(
    name="HepMC3",
    version=get_hepmc3_version(),
    author="HepMC3 Developers",
    author_email="hepmc-dev@cern.ch",
    description="HepMC3 library and Python bindings for HepMC3",
    long_description="Official python bindings for the HepMC3 library. Please visit https://hepmc.web.cern.ch/hepmc/ and  https://gitlab.cern.ch/hepmc/HepMC3 for more documentation",
    long_description_content_type="text/markdown",
    url="https://gitlab.cern.ch/hepmc/HepMC3",
    license="GPLv3",
    platforms=["any"],
    include_package_data=True,
    packages=local_find_packages(),
    data_files=get_hepmc3_libraries()
    + get_install_rec("share/doc/HepMC3-" + get_hepmc3_version(),"examples")
    + get_install_rec("","include/HepMC3")
    + get_install("include/HepMC3", "include/HepMC3",False)
    + get_install("include/HepMC3", "search/include/HepMC3")
    + [("bin", ["outputs/bin/HepMC3-config"])]
    + [("share/HepMC3/cmake", ["outputs/share/HepMC3/cmake/HepMC3Config-version.cmake","outputs/share/HepMC3/cmake/HepMC3Config.cmake","outputs/share/HepMC3/cmake/HepMC3searchTargets.cmake", "outputs/share/HepMC3/cmake/HepMC3searchTargets-release.cmake", "outputs/share/HepMC3/cmake/HepMC3Targets.cmake", "outputs/share/HepMC3/cmake/HepMC3Targets-release.cmake",],)],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    ext_modules=[CMakeExtension("pyHepMC3")],
    cmdclass={"build_ext": hm3_build_ext, "install_lib": hm3_install_lib},
)
