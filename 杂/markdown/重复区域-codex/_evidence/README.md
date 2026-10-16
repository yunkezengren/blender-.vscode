# 证据与维护工具

[返回课程入口](../README.md)

- [source-excerpts.json](source-excerpts.json)：源文件、SHA-256、区间和对应正文。
- [document-stats.json](document-stats.json)：14篇正文的行数和字符数。
- [validation.json](validation.json)：源码摘录、链接、围栏和篇幅检查。
- [reference-models.json](reference-models.json)：独立参考模型的断言结果。
- [blender-demo.json](blender-demo.json)：独立安装Blender的版本、命令和真实输出。
- [build_docs.py](build_docs.py)：课程正文的作者说明、案例与源码区间配置。
- [finish_course.py](finish_course.py)：导航和课程指南的生成工具。
- [validate_docs.py](validate_docs.py)：只读文档校验并写出本目录验证记录。
- [run_examples.py](run_examples.py)：运行两类示例并保存输出。

从仓库根目录重建：

```powershell
python .markdown\重复区域-codex\_evidence\build_docs.py
python .markdown\重复区域-codex\_evidence\finish_course.py
python .markdown\重复区域-codex\_evidence\run_examples.py
python .markdown\重复区域-codex\_evidence\validate_docs.py
```

重建会覆写本课程生成的正文与导航。修改正文时应同步更新作者配置，避免下一次重建丢失修改。

源码漂移应先检查差异，再更新摘录区间与机制解释；不能只刷新哈希后声称语义仍然正确。

`.markdown` 在当前机器是目录联接，工具从实际父目录寻找Blender源码根，源码相对链接也按真实目录计算。

Mermaid已检查围栏与基本结构，没有安装渲染器时不声称所有图都做过像素级渲染验证。
