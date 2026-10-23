# 01 · GeometrySet 组件模型

[前置知识总入口](../README.md) · [本章导航](README.md) · [下一篇](02-ImplicitSharing引用计数.md)

> 基准：Blender `5.4.0-alpha`，本地工作树。本篇讲 `GeometrySet`——几何节点的核心数据容器。理解它才能理解正篇反复强调的"传几何很便宜、改几何才贵"。主要源码：[`BKE_geometry_set.hh`](../../../source/blender/blenkernel/BKE_geometry_set.hh)（实测总行数 852）。

## 先回答一个具体问题

一个几何节点 socket 里的"几何"到底是什么？是 Mesh 吗？

**不是**。是 `GeometrySet`——一个**组件的容器**，里面可能同时装 mesh、点云、曲线、实例。

## 为什么不是"一种几何"

`[讲解]` 如果 socket 类型直接是 `Mesh*`，会遇到什么问题？

| 场景 | 用 Mesh* 的问题 |
| --- | --- |
| 同时有点和面 | 点云与网格是两个类型，装不下 |
| 实例化 | 实例不是 mesh |
| 空几何 | 没有合适的表示 |
| 类型无关传递 | 每个节点都要判断"我收到的是什么" |

`[讲解]` `GeometrySet` 的设计：**装一个"组件数组"，每个组件是一种几何类型**。

## 组件类型

`[讲解]` 源码里 `GeometryComponent::Type` 枚举（可能定义在 `BKE_geometry_component_type.hh` 或类似）：

| 类型 | 对应数据 |
| --- | --- |
| `MESH` | 网格 |
| `POINTCLOUD` | 点云 |
| `CURVE` | 曲线 |
| `INSTANCES` | 实例集合 |
| `VOLUME` | 体素（OpenVDB） |
| `GREASEPENCIL` | Grease Pencil |
| `EDIT_MESH` | 编辑态网格 |

`[讲解]` 一个 `GeometrySet` 可以同时含多个。比如：

- Distribute Points on Faces 的输出：mesh（原表面）+ pointcloud（生成的点）？
- 实际上：它输出 mesh + pointcloud 两个组件，实例化后变 instances。

## 核心接口

`[讲解]` 从源码（`BKE_geometry_set.hh`）提炼：

| 接口 | 行号 | 用途 |
| --- | --- | --- |
| `get_component_for_write(type)` | L179 | 取得**可写**组件（可能复制） |
| `get_component(type)` | L194 | 取得**只读**组件 |
| `get_component_ptr(type)` | L186 | 取得组件的共享指针 |
| `has_component<C>()` | L208 | 是否有某类型 |
| `add(component)` | L226 | 添加组件 |
| `remove(type)` | L214 | 移除组件 |
| `get_components()` | L231 | 遍历所有组件 |

`[讲解]` 模板版本（L180-L183、L195-L198）是类型安全的包装：

```cpp
template<typename Component> Component &get_component_for_write()
{
  return static_cast<Component &>(this->get_component_for_write(Component::static_type));
}
```

`[讲解]` 所以可以写：

```cpp
Mesh &mesh = geometry.get_component_for_write<MeshComponent>();
```

比 `static_cast<Mesh&>(*geometry.get_component_for_write(Type::MESH))` 简洁。

## 只读 vs 可写的关键区别

`[讲解]` 这是本篇最重要的区分，也是 09-03 篇的主题：

| | `get_component` | `get_component_for_write` |
| --- | --- | --- |
| 返回 | `const GeometryComponent*` | `GeometryComponent&` |
| 是否可能复制 | ❌ 绝不 | ✅ 可能触发写时复制 |
| 使用场景 | 读取数据 | 修改数据 |
| 代价 | 零 | 取决于引用计数 |

`[讲解]` 源码注释（L481 附近）明确提到这个对比：

> "unlike #get_component_for_write."

`[讲解]` **这就是"传几何便宜、改几何贵"的接口层体现**：

- 传 = 复制 `GeometrySet`（组件指针数组，引用计数 +1）；
- 读 = `get_component`（零成本）；
- 写 = `get_component_for_write`（可能深拷贝）。

## 存储结构

`[讲解]` `GeometrySet` 内部存什么？从 `get_components()` 返回 `Vector<const GeometryComponent*>` 可推出：**一个组件指针数组**。

`[讲解]` 关键事实：

- 直接存 `GeometryComponent` 还是 `GeometryComponentPtr`？答案是后者（共享指针）；
- 所以复制 `GeometrySet` = 复制数组 + 每个计数 +1。

`[讲解]` 这与 09-02 的 `ImplicitSharing` 直接相关。

## 空几何

`[讲解]` `GeometrySet` 可以是**完全空的**（0 个组件）。

`[讲解]` 这不是错误状态——它是"没有几何"的合法表示。比如：

- 选择节点选了空集；
- 删除几何节点删光了；
- 初始输入没连。

`[讲解]` 正篇 06-01 讲过 Foreach 的"迭代域无元素"警告——那是在"主几何非空但迭代域为空"时提示的，区别于"完全没有几何"。

## 属性与组件的关系

`[讲解]` 一个容易混淆的点：属性（attribute）是**组件的一部分**，不是 GeometrySet 的一部分。

```text
GeometrySet
├── MeshComponent
│   └── attributes: position, normal, custom_attrs...
├── PointCloudComponent
│   └── attributes: position, radius...
```

`[讲解]` 所以：

- `geometry.get_component_for_write<MeshComponent>().attributes()` 才能访问属性；
- `GeometrySet` 层面没有"属性"概念。

## 在 Repeat 中的意义

`[讲解]` 正篇 06-02 的核心结论：

> "纯读轮近乎免费、写轮深拷贝"

`[讲解]` 机制拆解：

| 轮次操作 | 发生什么 | 成本 |
| --- | --- | --- |
| 把几何传给下一轮 | 复制 `GeometrySet`（指针数组） | 引用计数 +1 |
| 只读（如 Viewer） | `get_component` | 零 |
| 写（如 Set Position） | `get_component_for_write` → COW | 深拷贝 |

`[讲解]` 所以"纯读轮"的成本是 **N × （数组复制 + 计数操作）**——与几何规模无关。

"写轮"的成本是 **深拷贝整个组件**——与几何规模成正比。

**这就是为什么规划循环体时要避免每轮修改几何。**

## 用小数据走一遍

`[讲解]` 一个含 mesh 的 GeometrySet 在三轮循环中传递。

**第 0 轮**：

```text
G0 = GeometrySet{ components: [MeshComponent*] }
     引用计数: 1
```

**传给第 1 轮（只读）**：

```text
G1 = G0   /* 复制 GeometrySet */
     引用计数: 2（MeshComponent 被 G0、G1 共享）
成本：复制一个指针 + 原子加
```

**传给第 2 轮（要写）**：

```text
G2.get_component_for_write<MeshComponent>()
  → 检查计数 == 2 > 1
  → 深拷贝 MeshComponent
  → G2 现在有自己的 mesh，计数各自 1
成本：拷贝整个 mesh（顶点、面、属性）
```

`[讲解]` 三行对比：

| 操作 | 数据量 | 相对成本 |
| --- | --- | --- |
| 传递（只读） | 8 字节指针 | 1 |
| 深拷贝 mesh | 数万字节 | 数千 |

**量级差三到四个数量级**。

## 反例与边界

### 反例 1：以为 GeometrySet 就是一个 Mesh

它是容器，可以含多种组件，也可以是空的。

### 反例 2：用 `get_component` 拿到只读引用后强行修改

```cpp
/* 危险 */
const Mesh *mesh = geometry.get_component<MeshComponent>();
const_cast<Mesh *>(mesh)->do_something();   /* 污染其他持有者 */
```

应该用 `get_component_for_write`。

### 反例 3：以为复制 GeometrySet 会深拷贝

只复制组件指针数组，计数 +1。

### 反例 4：以为 `remove` 会销毁组件

只是从集合里移除引用，计数 -1。归零才销毁。

### 反例 5：忽略空 GeometrySet

它是合法的。代码要能处理 0 个组件。

### 反例 6：以为属性在 GeometrySet 层面

属性属于组件。

## 对理解 Repeat 的帮助

`[讲解]` 正篇 06-02 有一段完整的性能分析（L638-L672），本篇是其数据模型基础：

| 正篇结论 | 本篇机制 |
| --- | --- |
| 传几何很便宜 | `GeometrySet` 只存指针数组 |
| 复制只是计数 +1 | `ImplicitSharing`（09-02） |
| 改几何才贵 | `get_component_for_write` 触发 COW（09-03） |

`[讲解]` **最关键的一条**：Repeat 循环体里"每轮把 Geometry 传给下一轮"这个操作，在数据层面只是**复制一个指针数组**。所以哪怕 100 轮，传递成本也可忽略。

真正贵的是"每轮修改几何"——那会每轮深拷贝。

## 继续阅读

- [02-ImplicitSharing引用计数](02-ImplicitSharing引用计数.md) —— 为什么复制便宜
- [03-写时复制与组件分离](03-写时复制与组件分离.md) —— 为什么写贵
- [04-匿名属性与ReferenceSet](04-匿名属性与ReferenceSet.md) —— 属性的生命周期
