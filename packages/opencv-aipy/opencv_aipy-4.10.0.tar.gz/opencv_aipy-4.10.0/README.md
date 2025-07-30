This project is a branch of [opencv-python](https://pypi.org/project/opencv-python/) on [QPython](https://www.qpython.org).

OpenCV is raising funds to keep the library free for everyone, and we need the support of the entire community to do it.

## OpenCV on Wheels

Pre-built CPU-only OpenCV packages for Python.

Check the manual build section if you wish to compile the bindings from source to enable additional modules such as CUDA.

### Installation and Usage

1. If you have previous/other manually installed (= not installed via ``pip``) version of OpenCV installed (e.g. cv2 module in the root of Python's site-packages), remove it before installation to avoid conflicts.
2. Make sure that your `pip` version is up-to-date (19.3 is the minimum supported version): `pip install --upgrade pip`. Check version with `pip -V`. For example Linux distributions ship usually with very old `pip` versions which cause a lot of unexpected problems especially with the `manylinux` format.
3. Select the correct package for your environment:

    There are four different packages (see options 1, 2, 3 and 4 below) and you should **SELECT ONLY ONE OF THEM**. Do not install multiple different packages in the same environment. There is no plugin architecture: all the packages use the same namespace (`cv2`). If you installed multiple different packages in the same environment, uninstall them all with ``pip uninstall`` and reinstall only one package.

    **a.** Packages for standard desktop environments (Windows, macOS, almost any GNU/Linux distribution)

    - Option 1 - Main modules package: ``pip install opencv-python``
    - Option 2 - Full package (contains both main modules and contrib/extra modules): ``pip install opencv-contrib-python`` (check contrib/extra modules listing from [OpenCV documentation](https://docs.opencv.org/master/))

    **b.** Packages for server (headless) environments (such as Docker, cloud environments etc.), no GUI library dependencies

    These packages are smaller than the two other packages above because they do not contain any GUI functionality (not compiled with Qt / other GUI components). This means that the packages avoid a heavy dependency chain to X11 libraries and you will have for example smaller Docker images as a result. You should always use these packages if you do not use `cv2.imshow` et al. or you are using some other package (such as PyQt) than OpenCV to create your GUI.

    - Option 3 - Headless main modules package: ``pip install opencv-python-headless``
    - Option 4 - Headless full package (contains both main modules and contrib/extra modules): ``pip install opencv-contrib-python-headless`` (check contrib/extra modules listing from [OpenCV documentation](https://docs.opencv.org/master/))

4. Import the package:

    ``import cv2``

    All packages contain Haar cascade files. ``cv2.data.haarcascades`` can be used as a shortcut to the data folder. For example:

    ``cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")``

5. Read [OpenCV documentation](https://docs.opencv.org/master/)

6. Before opening a new issue, read the FAQ below and have a look at the other issues which are already open.

Frequently Asked Questions
--------------------------

**Q: Do I need to install also OpenCV separately?**

A: No, the packages are special wheel binary packages and they already contain statically built OpenCV binaries.

**Q: Pip install fails with ``ModuleNotFoundError: No module named 'skbuild'``?**

Since ``opencv-python`` version 4.3.0.\*, ``manylinux1`` wheels were replaced by ``manylinux2014`` wheels. If your pip is too old, it will try to use the new source distribution introduced in 4.3.0.38 to manually build OpenCV because it does not know how to install ``manylinux2014`` wheels. However, source build will also fail because of too old ``pip`` because it does not understand build dependencies in ``pyproject.toml``. To use the new ``manylinux2014`` pre-built wheels (or to build from source), your ``pip`` version must be >= 19.3. Please upgrade ``pip`` with ``pip install --upgrade pip``.

**Q: Import fails on Windows: ``ImportError: DLL load failed: The specified module could not be found.``?**

A: If the import fails on Windows, make sure you have [Visual C++ redistributable 2015](https://www.microsoft.com/en-us/download/details.aspx?id=48145) installed. If you are using older Windows version than Windows 10 and latest system updates are not installed, [Universal C Runtime](https://support.microsoft.com/en-us/help/2999226/update-for-universal-c-runtime-in-windows) might be also required.

Windows N and KN editions do not include Media Feature Pack which is required by OpenCV. If you are using Windows N or KN edition, please install also [Windows Media Feature Pack](https://support.microsoft.com/en-us/help/3145500/media-feature-pack-list-for-windows-n-editions).

If you have Windows Server 2012+, media DLLs are probably missing too; please install the Feature called "Media Foundation" in the Server Manager. Beware, some posts advise to install "Windows Server Essentials Media Pack", but this one requires the "Windows Server Essentials Experience" role, and this role will deeply affect your Windows Server configuration (by enforcing active directory integration etc.); so just installing the "Media Foundation" should be a safer choice.

If the above does not help, check if you are using Anaconda. Old Anaconda versions have a bug which causes the error, see [this issue](https://github.com/opencv/opencv-python/issues/36) for a manual fix.

If you still encounter the error after you have checked all the previous solutions, download [Dependencies](https://github.com/lucasg/Dependencies) and open the ``cv2.pyd`` (located usually at ``C:\Users\username\AppData\Local\Programs\Python\PythonXX\Lib\site-packages\cv2``) file with it to debug missing DLL issues.

**Q: I have some other import errors?**

A: Make sure you have removed old manual installations of OpenCV Python bindings (cv2.so or cv2.pyd in site-packages).

**Q: Function foo() or method bar() returns wrong result, throws exception or crashes interpreter. What should I do?**

A: The repository contains only OpenCV-Python package build scripts, but not OpenCV itself. Python bindings for OpenCV are developed in official OpenCV repository and it's the best place to report issues. Also please check [OpenCV wiki](https://github.com/opencv/opencv/wiki) and [the official OpenCV forum](https://forum.opencv.org/) before file new bugs.

**Q: Why the packages do not include non-free algorithms?**

A: Non-free algorithms such as SURF are not included in these packages because they are patented / non-free and therefore cannot be distributed as built binaries. Note that SIFT is included in the builds due to patent expiration since OpenCV versions 4.3.0 and 3.4.10. See this issue for more info: https://github.com/skvark/opencv-python/issues/126

**Q: Why the package and import are different (opencv-python vs. cv2)?**

A: It's easier for users to understand ``opencv-python`` than ``cv2`` and it makes it easier to find the package with search engines. `cv2` (old interface in old OpenCV versions was named as `cv`) is the name that OpenCV developers chose when they created the binding generators. This is kept as the import name to be consistent with different kind of tutorials around the internet. Changing the import name or behaviour would be also confusing to experienced users who are accustomed to the ``import cv2``.

## Documentation for opencv-python

[![Windows Build Status](https://github.com/opencv/opencv-python/actions/workflows/build_wheels_windows.yml/badge.svg)](https://github.com/opencv/opencv-python/actions/workflows/build_wheels_windows.yml)
[![(Linux Build status)](https://github.com/opencv/opencv-python/actions/workflows/build_wheels_linux.yml/badge.svg)](https://github.com/opencv/opencv-python/actions/workflows/build_wheels_linux.yml)
[![(Mac OS Build status)](https://github.com/opencv/opencv-python/actions/workflows/build_wheels_macos.yml/badge.svg)](https://github.com/opencv/opencv-python/actions/workflows/build_wheels_macos.yml)

The aim of this repository is to provide means to package each new [OpenCV release](https://github.com/opencv/opencv/releases) for the most used Python versions and platforms.

### CI build process

The project is structured like a normal Python package with a standard ``setup.py`` file.
The build process for a single entry in the build matrices is as follows (see for example `.github/workflows/build_wheels_linux.yml` file):

0. In Linux and MacOS build: get OpenCV's optional C dependencies that we compile against

1. Checkout repository and submodules

   -  OpenCV is included as submodule and the version is updated
      manually by maintainers when a new OpenCV release has been made
   -  Contrib modules are also included as a submodule

2. Find OpenCV version from the sources

3. Build OpenCV

   -  tests are disabled, otherwise build time increases too much
   -  there are 4 build matrix entries for each build combination: with and without contrib modules, with and without GUI (headless)
   -  Linux builds run in manylinux Docker containers (CentOS 5)
   -  source distributions are separate entries in the build matrix

4. Rearrange OpenCV's build result, add our custom files and generate wheel

5. Linux and macOS wheels are transformed with auditwheel and delocate, correspondingly

6. Install the generated wheel
7. Test that Python can import the library and run some sanity checks
8. Use twine to upload the generated wheel to PyPI (only in release builds)

Steps 1--4 are handled by ``pip wheel``.

The build can be customized with environment variables. In addition to any variables that OpenCV's build accepts, we recognize:

- ``CI_BUILD``. Set to ``1`` to emulate the CI environment build behaviour. Used only in CI builds to force certain build flags on in ``setup.py``. Do not use this unless you know what you are doing.
- ``ENABLE_CONTRIB`` and ``ENABLE_HEADLESS``. Set to ``1`` to build the contrib and/or headless version
- ``ENABLE_JAVA``, Set to ``1`` to enable the Java client build.  This is disabled by default.
- ``CMAKE_ARGS``. Additional arguments for OpenCV's CMake invocation. You can use this to make a custom build.

See the next section for more info about manual builds outside the CI environment.