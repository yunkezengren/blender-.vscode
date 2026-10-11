
cd /d E:/blender-git/blender
@REM set Branch=change-socket-shape
set Branch=blender

@REM set nj_Branch=E:\blender-git\%Branch%_ninja_release
@REM make nobuild ninja builddir %nj_Branch%

set nj_Branch=E:\blender-git\%Branch%_ninja_lite_debug
make nobuild ninja lite debug builddir %nj_Branch%

@REM set nj_Branch=E:\blender-git\%Branch%_ninja_debug
@REM make nobuild ninja debug builddir %nj_Branch%

@REM set nj_Branch=E:\blender-git\%Branch%_ninja_debug_developer
@REM make nobuild ninja debug developer builddir %nj_Branch%

cd %nj_Branch%
code CmakeCache.txt

@REM . 表示 当前目录
cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DWITH_UNITY_BUILD=OFF -DCMAKE_VERBOSE_MAKEFILE=OFF -DWITH_WINDOWS_SCCACHE=ON -DWITH_INPUT_IME=ON -DWITH_INTERNATIONAL=ON .

@REM   可以按需要启用一些
@REM   启用 CMAKE_EXPORT_COMPILE_COMMANDS: 在构建目录创建 compile_commands.json, MS C++ 扩展和Clangd需要
@REM   禁用 WITH_UNITY_BUILD: (Clangd要禁用这个)
@REM   启用 echo: CMAKE_VERBOSE_MAKEFILE: 会在终端里每行都输出
@REM   启用 WITH_WINDOWS_SCCACHE
@REM  lite 还需要这三个
@REM   启用 ime: WITH_INPUT_IME
@REM   启用 i18n: WITH_INTERNATIONAL
@REM   启用 WITH_TBB  已经默认启用了

@REM   此外: CMAKE_BUILD_TYPE 可以改, lite时是Release
@REM   问的AI, 我是4核8线程, 所以 j8 会创建8个线程还是进程, 卡的话可以开少点

REM -S：指定 Blender 源码目录，其中包含顶层 CMakeLists.txt
REM -B：指定构建目录，其中存放 CMakeCache.txt 和编译中间文件
@REM cmake -S "E:\blender-git\blender" -B "E:\blender-git\blender_ninja_lite_debug" ^
@REM   -DCMAKE_EXPORT_COMPILE_COMMANDS:BOOL=ON ^
@REM   -DWITH_UNITY_BUILD:BOOL=OFF ^
@REM   -DCMAKE_VERBOSE_MAKEFILE:BOOL=OFF ^
@REM   -DWITH_WINDOWS_SCCACHE:BOOL=ON ^
@REM   -DWITH_INPUT_IME:BOOL=ON ^
@REM   -DWITH_INTERNATIONAL:BOOL=ON ^


rebuild -j8

@REM make clean or ninja -t clean depending on your build system will do it
make clean
ninja -t clean

pause

cd /d E:/blender-git/blender
make nobuild ninja lite debug builddir E:\blender-git\blender_ninja_lite_debug
cd E:\blender-git\blender_ninja_lite_debug
rebuild -j8