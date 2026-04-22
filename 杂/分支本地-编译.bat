
cd /d E:/blender-git/blender
@REM set Branch=change-socket-shape
@REM set Branch=bevelnode
@REM set Branch=test-branch
set Branch=blender

set nj_release_Branch=E:\blender-git\%Branch%_ninja_release
make nobuild ninja builddir %nj_release_Branch%
cd %nj_release_Branch%

@REM set nj_Branch=E:\blender-git\%Branch%_ninja_lite
@REM make nobuild ninja lite builddir %nj_Branch%
@REM cd %nj_Branch%

@REM set nj_Branch=E:\blender-git\%Branch%_ninja_lite_debug
@REM make nobuild ninja lite debug builddir %nj_Branch%
@REM cd %nj_Branch%

@REM set nj_Branch=E:\blender-git\%Branch%_ninja_debug
@REM make nobuild ninja debug builddir %nj_Branch%
@REM cd %nj_Branch%

@REM set nj_Branch=E:\blender-git\%Branch%_ninja_debug_developer
@REM make nobuild ninja debug developer builddir %nj_Branch%
@REM cd %nj_Branch%


code CmakeCache.txt
@REM   可以按需要启用一些
@REM   启用 CMAKE_EXPORT_COMPILE_COMMANDS: 会在构建目录中创建 compile_commands.json
@REM   禁用: WITH_UNITY_BUILD (Clangd要禁用这个)
@REM   启用 echo: CMAKE_VERBOSE_MAKEFILE:
@REM  lite 还需要这三个
@REM   启用 WITH_TBB
@REM   启用 ime: WITH_INPUT_IME
@REM   启用 i18n: WITH_INTERNATIONAL

@REM   此外: CMAKE_BUILD_TYPE 可以改, lite时是Release
@REM   问的AI, 我是4核8线程, 所以 j8 会创建8个线程还是进程, 卡的话可以开少点
@REM rebuild -j8

pause