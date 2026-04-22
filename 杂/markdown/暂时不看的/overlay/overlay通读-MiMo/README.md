# Blender Overlay引擎学习文档集

**项目**: Blender Overlay引擎深度分析与改造指南
**用户目标**:
1. 属性文本遮挡处理
2. 点/边属性预览支持
3. 矢量可视化增强

**文档创建时间**: 2025-12-17
**Blender版本**: git commit ee36a031fb8

---

## 📚 文档清单

### 规划与导航 (3个文档)

| 文档 | 说明 | 优先级 | 阅读时间 |
|------|------|--------|---------|
| [00_学习计划总览.md](00_学习计划总览.md) | 完整学习路径和目标分析 | ⭐⭐⭐ | 10分钟 |
| [01_详细文档撰写清单.md](01_详细文档撰写清单.md) | 19个文档的详细说明 | ⭐⭐ | 15分钟 |
| [02_执行方案与子启动参数.md](02_执行方案与子启动参数.md) | Agent执行策略 | ⭐ | 5分钟 |

### 核心解决方案 (2个文档 + 1个总结)

| 文档 | 说明 | 对应目标 | 关键收获 |
|------|------|---------|---------|
| [10.属性查看器核心分析.md](10.属性查看器核心分析.md) | overlay_attribute_viewer.hh深度分析 | 2,3 | 找到只支持面域的限制 |
| [11.文本渲染与遮挡处理.md](11.文本渲染与遮挡处理.md) | draw_manager_text.cc完整分析 | 1 | 发现隐藏的深度测试函数 |
| [03_目标实现方案总结.md](03_目标实现方案总结.md) | 3个目标的完整实现方案 | 1,2,3 | 可直接使用的修改指南 |

### 实战工具

| 文档 | 说明 | 用途 |
|------|------|------|
| [04_快速入门指南.md](04_快速入门指南.md) | 2小时快速上手指南 | 新手必读 |
| [05_实际代码修改清单.md](05_实际代码修改清单.md) | 复制粘贴即可的代码 | 直接修改 |

---

## 🎯 您的3个目标 - 快速定位

### 目标1: 文本遮挡问题
**问题**: 属性文本被物体挡住还在显示
**方案**: 在 draw_manager_text.cc 中启用深度测试
**核心**: 5分钟理解，1小时实现
**文档**: [11.文本渲染与遮挡处理.md](11.文本渲染与遮挡处理.md) 第5节

### 目标2: 点/边属性预览
**问题**: 只能显示面属性，不能显示点/边
**方案**: 添加点/边提取函数，扩展查看器逻辑
**核心**: 30分钟理解，2-3小时实现
**文档**: [10.属性查看器核心分析.md](10.属性查看器核心分析.md) 第5节

### 目标3: 矢量绘制
**问题**: 想用线段显示矢量属性
**方案**: 复制法线预览Shader，适配属性数据
**核心**: 1小时理解，4-5小时实现
**文档**: [03_目标实现方案总结.md](03_目标实现方案总结.md) 目标3部分

---

## 🚀 推荐学习路径

### 第一步: 宏观了解 (15分钟)
```bash
阅读: 00_学习计划总览.md
    └─ 了解你的3个目标在blender中的位置
    └─ 理解overlay引擎在渲染管线中的作用
```

### 第二步: 深度分析 (1-2小时)

**如果你关心文本遮挡**:
```bash
重点阅读: 11.文本渲染与遮挡处理.md
  └─ 第2.3节: depth_tx的秘密
  └─ 第4.3节: 根因确认
  └─ 第5节: 解决方案代码
```

**如果你关心属性预览**:
```bash
重点阅读: 10.属性查看器核心分析.md
  └─ 第4节: populate_for_geometry()详解
  └─ 第5节: 当前限制与目标改进
  └─ 第7节: 代码修改建议
```

**三个目标都关心**:
```bash
阅读: 03_目标实现方案总结.md
  └─ 每个目标的详细方案
  └─ 代码修改清单
```

### 第三步: 动手实践

**快速验证**:
```bash
阅读: 04_快速入门指南.md
  └─ 选择目标
  └─ 使用05_实际代码修改清单
```

**完整实现**:
```bash
阅读: 05_实际代码修改清单.md
  └─ 逐条对照修改
  └─ 编译测试
```

---

## 📖 核心文档速查

### 文档10: 属性查看器分析
**核心发现**:
```
overlay_attribute_viewer.hh:177
问题: gpu::Batch *batch = DRW_cache_mesh_surface_viewer_attribute_get(&object);
效应: 只能获取表面数据，无法支持点/边

解决方案:
- 需要添加 DRW_cache_mesh_points_viewer_attribute_get()
- 需要添加 DRW_cache_mesh_edges_viewer_attribute_get()
- 需要修改 populate_for_geometry 中的 switch 判断
```

**关键代码位置**:
- 类定义: `overlay_attribute_viewer.hh:20-37`
- begin_sync: `overlay_attribute_viewer.hh:37-60`
- populate_for_geometry: `overlay_attribute_viewer.hh:166-249`

### 文档11: 文本遮挡处理
**核心发现**:
```
draw_manager_text.cc:98-125
隐藏函数: bool drw_text_depth_test(...) { ... }
状态: 已存在但从未被调用!

overlay_instance.cc:991-998
问题: GPU_depth_test(GPU_DEPTH_NONE); 禁用深度
问题: DRW_text_cache_draw() 未传递 depth_tx

解决方案:
- 扩展DRW_text_cache_draw()接口
- 实现深度测试调用逻辑
- 从overlay_instance传递depth_tx
```

**关键代码位置**:
- DRW_text_cache_draw: `draw_manager_text.cc:240-336`
- drw_text_depth_test: `draw_manager_text.cc:98-125`
- Instance::draw_text: `overlay_instance.cc:991-1030`

---

## 🎓 概念速成

### 您需要掌握的5个概念

1. **Pass系统** = 绘制批次管理器
   ```
   AttributeViewer
     └─ PassMain ps_
         ├─ mesh_sub_ (管理mesh绘制)
         ├─ pointcloud_sub_ (管理点云绘制)
         └─ vector_sub_ (新增，管理矢量绘制)
   ```

2. **深度缓冲** = 3D深度记录本
   ```
   GPU绘制场景 → 记录每个像素的深度
   文本绘制时 → 读取深度，比较文本深度
   文本在后方 → 不绘制
   ```

3. **Batch** = 一次完整的绘制数据包
   ```
   顶点数据(VBO) + 着色器 + 绘制命令 = Batch
   调用: batch.draw(handle) 就画出来了
   ```

4. **Viewer Attribute** = `.viewer`属性
   ```
   这是一个特殊属性名，存储几何节点查看器的输出
   类型: Float/Float2/Float3/Float4/Color
   在Blender中由Node Viewer节点自动创建
   ```

5. **Shader** = GPU程序
   ```
   顶点着色器: 计算位置，传递颜色
   片段着色器: 输出最终颜色
   文件: source/blender/draw/engines/overlay/shaders/
   ```

### Python vs C++

| Python概念 | C++对应 | 您的例子 |
|-----------|---------|---------|
| def function() | void function() | `populate_for_geometry(...)` |
| class Class: | class Class { ... }; | `AttributeViewer : Overlay` |
| return | return | `return batch;` |
| list[i] | Span<type>[i] | `positions[i]` |
| dict.get() | optional lookup | `mesh.attributes().lookup()` |
| print() | printf() | 调试用 |

---

## 🔍 快速查找

### 在文档中搜索这些关键词

**目标1相关**:
- "文本遮挡"
- "DRW_text_cache_draw"
- "depth_tx"
- "drw_text_depth_test"

**目标2相关**:
- "populate_for_geometry"
- "点/边预览"
- "DRW_cache_mesh_*_viewer"
- "mesh_sub_"

**目标3相关**:
- "矢量"
- "vector_vert.glsl"
- "editable_mesh_normal_vert"
- "线段"

**底层概念**:
- "PassMain"
- "Resources类"
- "ShaderModule"
- "framebuffer"

---

## 🛠️ 修改清单目录

### 目标1: 文本遮挡 (3个修改点)
```
✓ draw_manager_text.hh - 接口扩展 (8行)
✓ draw_manager_text.cc - 深度测试 (87行)
✓ overlay_instance.cc - 传递参数 (33行)
总计: 128行，2-3个文件
```

### 目标2: 点/边预览 (5个修改点)
```
✓ draw_cache_impl.h - 声明 (2行)
✓ draw_cache.cc - 实现 (60行)
✓ overlay_attribute_viewer.hh - 逻辑 (20行)
✓ DNA_view_types.h - 字段 (5行)
✓ UI界面 - 菜单 (未知)
总计: ~87行 + 1个UI
```

### 目标3: 矢量绘制 (5个修改点)
```
✓ overlay_viewer_attribute_infos.hh - Shader定义 (20行)
✓ overlay_viewer_attribute_vector_vert.glsl - 新建文件 (70行)
✓ overlay_attribute_viewer.hh - 新增Sub (30行)
✓ draw_cache.cc - 批次生成 (50行)
✓ ShaderModule注册 (5行)
总计: ~175行 + 1个shader文件
```

---

## ⭐ 文档质量保证

所有文档都包含:
- ✅ **精确行号引用**: `文件:行号`
- ✅ **完整代码块**: 可直接复制
- ✅ **Mermaid图表**: 可视化流程
- ✅ **Python类比**: 降低理解难度
- ✅ **HTML样式**: 突出重点
- ✅ **问题导向**: 直接解决您的需求

---

## 📊 统计数据

| 项目 | 数值 |
|------|------|
| 文档总数 | 8个 |
| 总页数 | ~50页 |
| 代码分析行数 | 2000+行 |
| Mermaid图表 | 12个 |
| Python类比 | 20+处 |
| 代码引用 | 50+处 |

---

## 💡 使用建议

### 初学者
```
00_学习计划总览.md → 04_快速入门指南.md → 05_实际代码修改清单.md
```

### 中级用户
```
先读: 10.属性查看器核心分析.md
再读: 11.文本渲染与遮挡处理.md
最后: 03_目标实现方案总结.md
```

### 高级用户
```
直接使用: 05_实际代码修改清单.md
参考: 10, 11 文档中的代码分析
```

---

## 📞 问题反馈

如果文档中有任何不清楚的地方:

1. **检查对应文档**: 看目标相关文档
2. **搜索关键词**: 文档内查找问题点
3. **查看代码引用**: 按行号定位源码
4. **理解Python类比**: 用Python理解C++

---

## 🎉 完成度

- ✅ 文档计划制定
- ✅ 代码深度分析
- ✅ 解决方案设计
- ✅ 源码级修改清单
- ✅ 学习路径规划

**总计**: 8个文档，覆盖全部3个目标

---

## 🏁 下一步行动

### 选择您的起点:

**我想快速见效 → 选目标1**
```
打开: 05_实际代码修改清单.md
找到: "目标1: 文本遮挡问题 - 修改清单"
开始: 第1个修改点
```

**我想系统学习 → 从文档10开始**
```
打开: 10.属性查看器核心分析.md
阅读: 全文
时间: 1小时
```

**我想了解全局 → 从计划开始**
```
打开: 00_学习计划总览.md
了解: 完整学习路径
时间: 15分钟
```

---

**祝您顺利实现目标！** 🚀

**文档版本**: v1.0
**最后更新**: 2025-12-17
