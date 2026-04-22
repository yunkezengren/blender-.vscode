######################################################################

set Branch=nodes-data-type-menu-icon
set Branch=make-group-inherit-color-tag

set Branch=change-socket-shape
set Branch=main

set bl_Branch=E:\blender-git\blender-%Branch%
# set nj_Branch=E:\blender-git\ninja_lite_debug_%Branch%
set nj_debug_Branch=E:\blender-git\ninja_debug_%Branch%
# set nj_release_Branch=E:\blender-git\ninja_release_%Branch%
cd /d E:/blender-git/blender
cd %bl_Branch%
# cd %nj_Branch%
cd %nj_release_Branch%
# cd ..\ninja_lite_debug_blender\

rebuild -j8 && bin\blender

######################################################################
# 初始建立工作树
cd /d E:\blender-git\blender
# [-b <新分支名>] <路径> [<起始点>]
git worktree add -b %Branch% %bl_Branch% main
# 已经存在的分支
git worktree add %bl_Branch% %Branch%

# 不追踪对这个 lib 文件夹的更改
git update-index --skip-worktree lib\windows_x64
# git update-index --no-skip-worktree lib\windows_x64

cd %bl_Branch%
# 强制删除 lib 文件夹
rmdir /s /q lib
mklink /J "%bl_Branch%\lib" "E:\blender-git\blender\lib"
mklink /J "%bl_Branch%\.vscode" "E:\blender-git\blender\.vscode"

make nobuild ninja builddir %nj_Branch%
make nobuild ninja lite debug builddir %nj_Branch%
cd %nj_Branch%
code CmakeCache.txt
# 原来我是4核8线程啊
#   启用 WITH_TBB
#   启用 CMAKE_EXPORT_COMPILE_COMMANDS: 会在构建目录中创建compile_commands.json
#   启用 echo: CMAKE_VERBOSE_MAKEFILE:
#   启用 i18n: WITH_INTERNATIONAL
#   启用 ime: WITH_INPUT_IME
#   禁用 WITH_UNITY_BUILD:BOOL 如果使用Clangd的话

#   CMAKE_BUILD_TYPE:STRING=

######################################################################

cd %nj_Branch%
rebuild -j8
rebuild -j8 && bin\blender


cd /d E:/blender-git/blender
@REM set Branch=change-socket-shape
@REM set Branch=bevelnode
@REM set Branch=test-branch
set Branch=blender

@REM set nj_Branch=E:\blender-git\%Branch%_ninja_lite
@REM make nobuild ninja lite builddir %nj_Branch%
@REM cd %nj_Branch%

set nj_Branch=E:\blender-git\%Branch%_ninja_lite_debug
make nobuild ninja lite debug builddir %nj_Branch%
cd %nj_Branch%

@REM set nj_Branch=E:\blender-git\%Branch%_ninja_debug
@REM make nobuild ninja debug builddir %nj_Branch%
@REM cd %nj_Branch%

@REM set nj_Branch=E:\blender-git\%Branch%_ninja_debug_developer
@REM make nobuild ninja debug developer builddir %nj_Branch%
@REM cd %nj_Branch%

@REM set nj_release_Branch=E:\blender-git\%Branch%_ninja_release
@REM make nobuild ninja builddir %nj_release_Branch%
@REM cd %nj_release_Branch%

code CmakeCache.txt
@REM   可以按需要启用一些
@REM   启用 CMAKE_EXPORT_COMPILE_COMMANDS: 会在构建目录中创建compile_commands.json
@REM   启用 echo: CMAKE_VERBOSE_MAKEFILE:
@REM  lite 还需要这三个
@REM   启用 WITH_TBB
@REM   启用 ime: WITH_INPUT_IME
@REM   启用 i18n: WITH_INTERNATIONAL

@REM   此外: CMAKE_BUILD_TYPE 可以改, lite时是Release
rebuild -j8
@REM   问的AI, 我是4核8线程, 所以 j8 会创建8个线程还是进程, 卡的话可以开少点

bin\blender