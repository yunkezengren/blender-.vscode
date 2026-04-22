
cd E:\blender-git\blender-test-branch

git status

git switch fix-compositor-render-region-dimming
git merge origin/main

git switch 用来切换分支
git merge origin/main

git status

cd E:\blender-git\blender
git switch fix-compositor-render-region-dimming

cd E:\blender-git\blender_ninja_lite_debug
.\rebuild -j8
bin\blender


@REM 如果合并错了,可以强制撤回
git reset --hard f82e80290f612f4d

git for-each-ref --sort=-committerdate --format='%(committerdate:relative) %(refname:short)' refs/heads/
2  hours  ago invalid-structure-type
10 hours  ago alt-affect-selected-tree-items
22 hours  ago fix-compositor-render-region-dimming
25 hours  ago cage-gizmo-center-scale
7  days   ago bevelnode
7  days   ago 倒角节点-用来切换分支
9  days   ago fix-cage2d-circle-corner-scale
10 days   ago node-tree-navigate-history
10 days   ago fix-vertex-neighbors-domain
10 days   ago 用来切换分支
2  weeks  ago fix-extend-socket-translation
3  weeks  ago improve-auto-view-instance
7  weeks  ago main
2  months ago confirm-overwrite-existing-file