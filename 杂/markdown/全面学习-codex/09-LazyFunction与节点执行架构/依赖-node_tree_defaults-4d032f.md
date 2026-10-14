# 实现依赖专题：source/blender/nodes/intern/node_tree_defaults.cc

[方向导航](README.md) · [符号索引](../%E7%AC%A6%E5%8F%B7%E4%BE%9D%E8%B5%96%E4%B8%8E%E5%AE%9E%E7%8E%B0%E7%B4%A2%E5%BC%95.md)

本专题从正文实际调用进入，集中保存共享实现。函数有稳定锚点，可从调用处直接跳到对应完整函数；递归与互相调用通过回链组织。

## 本文件的实现关系

```mermaid
flowchart LR
  F0["blender::nodes::node_tree_shader_default"]:::abstraction
  classDef input fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:2px;
  classDef data fill:#CFFAFE,stroke:#0891B2,color:#164E63,stroke-width:2px;
  classDef abstraction fill:#EDE9FE,stroke:#7C3AED,color:#3B0764,stroke-width:2px;
  classDef compute fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:2px;
  classDef result fill:#DCFCE7,stroke:#16A34A,color:#14532D,stroke-width:2px;
  classDef error fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:2px;
```

```mermaid
flowchart TB
  C["调用者提供参数与有效对象"]:::input
  F["node_tree_defaults.cc实现"]:::compute
  R["结果与被修改状态"]:::result
  C -->|"进入"| F
  F -->|"返回或提交"| R
  classDef input fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:2px;
  classDef data fill:#CFFAFE,stroke:#0891B2,color:#164E63,stroke-width:2px;
  classDef abstraction fill:#EDE9FE,stroke:#7C3AED,color:#3B0764,stroke-width:2px;
  classDef compute fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:2px;
  classDef result fill:#DCFCE7,stroke:#16A34A,color:#14532D,stroke-width:2px;
  classDef error fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:2px;
```

```mermaid
flowchart TB
  T["具体类型与模板实参"]:::abstraction
  B["分支与构建条件"]:::data
  I["匹配的实现"]:::compute
  E["标准库或系统契约边界"]:::result
  T -->|"静态选择"| I
  B -->|"配置选择"| I
  I -->|"到达外部接口"| E
  classDef input fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:2px;
  classDef data fill:#CFFAFE,stroke:#0891B2,color:#164E63,stroke-width:2px;
  classDef abstraction fill:#EDE9FE,stroke:#7C3AED,color:#3B0764,stroke-width:2px;
  classDef compute fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:2px;
  classDef result fill:#DCFCE7,stroke:#16A34A,color:#14532D,stroke-width:2px;
  classDef error fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:2px;
```

```mermaid
flowchart TB
  S["完整源码单元"]:::input
  A["教学注释与推导"]:::abstraction
  D["被调用实现专题"]:::compute
  V["原文与token一致性检查"]:::result
  S -->|"就近阅读"| A
  A -->|"继续深入"| D
  A -->|"核对"| V
  classDef input fill:#DBEAFE,stroke:#2563EB,color:#172554,stroke-width:2px;
  classDef data fill:#CFFAFE,stroke:#0891B2,color:#164E63,stroke-width:2px;
  classDef abstraction fill:#EDE9FE,stroke:#7C3AED,color:#3B0764,stroke-width:2px;
  classDef compute fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:2px;
  classDef result fill:#DCFCE7,stroke:#16A34A,color:#14532D,stroke-width:2px;
  classDef error fill:#FEE2E2,stroke:#DC2626,color:#7F1D1D,stroke-width:2px;
```

## 完整成员与函数实现

<a id="f-d8712912f3ff2dec"></a>

### `blender::nodes::node_tree_shader_default`

实现位置：[source/blender/nodes/intern/node_tree_defaults.cc](../../../../../source/blender/nodes/intern/node_tree_defaults.cc) · L35—L113。

接口参数：

- `const bContext *C`
- `Main *bmain`
- `ID *id`

**教学注释版**

<!-- annotated:8aba12ed607cf6 -->

```cpp
void node_tree_shader_default(const bContext *C, Main *bmain, ID *id)
{
  if (GS(id->name) == ID_MA) {
    /* Materials */
    Object *ob = (C) ? CTX_data_active_object(C) : nullptr;
    Material *ma = reinterpret_cast<Material *>(id);
    Material *ma_default;

    if (ob && ob->type == OB_VOLUME) {
      ma_default = BKE_material_default_volume();
    }
    else if (ob && ob->type == OB_POINTCLOUD && ob->data &&
             id_cast<const PointCloud *>(ob->data)->type == PointCloudType::GSplat)
    {
      ma_default = BKE_material_default_gsplat();
    }
    else {
      ma_default = BKE_material_default_surface();
    }

    if (ma->nodetree) {
      bke::node_tree_free_embedded_tree(ma->nodetree);
      MEM_delete(ma->nodetree);
      ma->nodetree = nullptr;
    }
    ma->nodetree = bke::node_tree_copy_tree(bmain, *ma_default->nodetree);
    ma->nodetree->owner_id = &ma->id;
    for (bNode *node_iter : ma->nodetree->all_nodes()) {
      STRNCPY_UTF8(node_iter->name, DATA_(node_iter->name));
      bke::node_unique_name(*ma->nodetree, *node_iter);
    }

    BKE_ntree_update_after_single_tree_change(*bmain, *ma->nodetree);
  }
  else if (ELEM(GS(id->name), ID_WO, ID_LA)) {
    /* Emission */
    bNode *shader, *output;
    bNodeTree *ntree = nullptr;

    if (GS(id->name) == ID_WO) {
      World *world = reinterpret_cast<World *>(id);
      ntree = world->nodetree;

      shader = bke::node_add_static_node(nullptr, *ntree, SH_NODE_BACKGROUND);
      output = bke::node_add_static_node(nullptr, *ntree, SH_NODE_OUTPUT_WORLD);
      bke::node_add_link(*ntree,
                         *shader,
                         *bke::node_find_socket(*shader, SOCK_OUT, "Background"_ustr),
                         *output,
                         *bke::node_find_socket(*output, SOCK_IN, "Surface"_ustr));

      bNodeSocket *color_sock = bke::node_find_socket(*shader, SOCK_IN, "Color"_ustr);
      copy_v3_v3((reinterpret_cast<bNodeSocketValueRGBA *>(color_sock->default_value))->value,
                 &world->horr);
    }
    else {
      ntree = bke::node_tree_add_tree_embedded(
          nullptr, id, "Shader Nodetree", ntreeType_Shader->idname.ref());
      shader = bke::node_add_static_node(nullptr, *ntree, SH_NODE_EMISSION);
      output = bke::node_add_static_node(nullptr, *ntree, SH_NODE_OUTPUT_LIGHT);
      bke::node_add_link(*ntree,
                         *shader,
                         *bke::node_find_socket(*shader, SOCK_OUT, "Emission"_ustr),
                         *output,
                         *bke::node_find_socket(*output, SOCK_IN, "Surface"_ustr));
    }

    shader->location[0] = -200.0f;
    shader->location[1] = 100.0f;
    output->location[0] = 200.0f;
    output->location[1] = 100.0f;
    bke::node_set_active(*ntree, *output);
    BKE_ntree_update_after_single_tree_change(*bmain, *ntree);
  }
  else {
    printf("node_tree_shader_default() called on wrong ID type.\n");
    return;
  }
}
```

<details>
<summary>核对原始源码：source/blender/nodes/intern/node_tree_defaults.cc · L35—L113</summary>

<!-- original:8aba12ed607cf6:source/blender/nodes/intern/node_tree_defaults.cc:35:113 -->

```cpp
void node_tree_shader_default(const bContext *C, Main *bmain, ID *id)
{
  if (GS(id->name) == ID_MA) {
    /* Materials */
    Object *ob = (C) ? CTX_data_active_object(C) : nullptr;
    Material *ma = reinterpret_cast<Material *>(id);
    Material *ma_default;

    if (ob && ob->type == OB_VOLUME) {
      ma_default = BKE_material_default_volume();
    }
    else if (ob && ob->type == OB_POINTCLOUD && ob->data &&
             id_cast<const PointCloud *>(ob->data)->type == PointCloudType::GSplat)
    {
      ma_default = BKE_material_default_gsplat();
    }
    else {
      ma_default = BKE_material_default_surface();
    }

    if (ma->nodetree) {
      bke::node_tree_free_embedded_tree(ma->nodetree);
      MEM_delete(ma->nodetree);
      ma->nodetree = nullptr;
    }
    ma->nodetree = bke::node_tree_copy_tree(bmain, *ma_default->nodetree);
    ma->nodetree->owner_id = &ma->id;
    for (bNode *node_iter : ma->nodetree->all_nodes()) {
      STRNCPY_UTF8(node_iter->name, DATA_(node_iter->name));
      bke::node_unique_name(*ma->nodetree, *node_iter);
    }

    BKE_ntree_update_after_single_tree_change(*bmain, *ma->nodetree);
  }
  else if (ELEM(GS(id->name), ID_WO, ID_LA)) {
    /* Emission */
    bNode *shader, *output;
    bNodeTree *ntree = nullptr;

    if (GS(id->name) == ID_WO) {
      World *world = reinterpret_cast<World *>(id);
      ntree = world->nodetree;

      shader = bke::node_add_static_node(nullptr, *ntree, SH_NODE_BACKGROUND);
      output = bke::node_add_static_node(nullptr, *ntree, SH_NODE_OUTPUT_WORLD);
      bke::node_add_link(*ntree,
                         *shader,
                         *bke::node_find_socket(*shader, SOCK_OUT, "Background"_ustr),
                         *output,
                         *bke::node_find_socket(*output, SOCK_IN, "Surface"_ustr));

      bNodeSocket *color_sock = bke::node_find_socket(*shader, SOCK_IN, "Color"_ustr);
      copy_v3_v3((reinterpret_cast<bNodeSocketValueRGBA *>(color_sock->default_value))->value,
                 &world->horr);
    }
    else {
      ntree = bke::node_tree_add_tree_embedded(
          nullptr, id, "Shader Nodetree", ntreeType_Shader->idname.ref());
      shader = bke::node_add_static_node(nullptr, *ntree, SH_NODE_EMISSION);
      output = bke::node_add_static_node(nullptr, *ntree, SH_NODE_OUTPUT_LIGHT);
      bke::node_add_link(*ntree,
                         *shader,
                         *bke::node_find_socket(*shader, SOCK_OUT, "Emission"_ustr),
                         *output,
                         *bke::node_find_socket(*output, SOCK_IN, "Surface"_ustr));
    }

    shader->location[0] = -200.0f;
    shader->location[1] = 100.0f;
    output->location[0] = 200.0f;
    output->location[1] = 100.0f;
    bke::node_set_active(*ntree, *output);
    BKE_ntree_update_after_single_tree_change(*bmain, *ntree);
  }
  else {
    printf("node_tree_shader_default() called on wrong ID type.\n");
    return;
  }
}
```

</details>

**沿实际写入检查状态**

- `ma_default = BKE_material_default_volume();`
- `ma_default = BKE_material_default_gsplat();`
- `ma_default = BKE_material_default_surface();`
- `ma->nodetree = nullptr;`
- `ma->nodetree = bke::node_tree_copy_tree(bmain, *ma_default->nodetree);`
- `ma->nodetree->owner_id = &ma->id;`
- `ntree = world->nodetree;`
- `shader = bke::node_add_static_node(nullptr, *ntree, SH_NODE_BACKGROUND);`
- `output = bke::node_add_static_node(nullptr, *ntree, SH_NODE_OUTPUT_WORLD);`
- `ntree = bke::node_tree_add_tree_embedded(`
- `shader = bke::node_add_static_node(nullptr, *ntree, SH_NODE_EMISSION);`
- `output = bke::node_add_static_node(nullptr, *ntree, SH_NODE_OUTPUT_LIGHT);`
- `shader->location[0] = -200.0f;`
- `shader->location[1] = 100.0f;`
- `output->location[0] = 200.0f;`
- `output->location[1] = 100.0f;`

**继续追踪实现**

- `GS` → [blender::GS · L410](../05-%E5%87%A0%E4%BD%95%E5%AD%98%E5%82%A8%E4%B8%8E%E6%8B%93%E6%89%91%E6%98%A0%E5%B0%84/%E4%BE%9D%E8%B5%96-DNA_ID-3eb091.md#f-c3ff509f79f21b05)。
- `CTX_data_active_object` → [blender::CTX_data_active_object · L1636](../05-%E5%87%A0%E4%BD%95%E5%AD%98%E5%82%A8%E4%B8%8E%E6%8B%93%E6%89%91%E6%98%A0%E5%B0%84/%E4%BE%9D%E8%B5%96-context-a929d9.md#f-a20e763460765d4b)。
- `BKE_material_default_volume` → [blender::BKE_material_default_volume · L2314](../05-%E5%87%A0%E4%BD%95%E5%AD%98%E5%82%A8%E4%B8%8E%E6%8B%93%E6%89%91%E6%98%A0%E5%B0%84/%E4%BE%9D%E8%B5%96-material-aea8ec.md#f-fe2f74d347314fd9)。
- `id_cast<const PointCloud *>` → [blender::id_cast · L1417](../05-%E5%87%A0%E4%BD%95%E5%AD%98%E5%82%A8%E4%B8%8E%E6%8B%93%E6%89%91%E6%98%A0%E5%B0%84/%E4%BE%9D%E8%B5%96-DNA_ID-3eb091.md#f-6c8ac6412850ac5a)。
- `BKE_material_default_gsplat` → [blender::BKE_material_default_gsplat · L2324](../05-%E5%87%A0%E4%BD%95%E5%AD%98%E5%82%A8%E4%B8%8E%E6%8B%93%E6%89%91%E6%98%A0%E5%B0%84/%E4%BE%9D%E8%B5%96-material-aea8ec.md#f-bb5aaa4e8e1e88bb)。
- `BKE_material_default_surface` → [blender::BKE_material_default_surface · L2309](../05-%E5%87%A0%E4%BD%95%E5%AD%98%E5%82%A8%E4%B8%8E%E6%8B%93%E6%89%91%E6%98%A0%E5%B0%84/%E4%BE%9D%E8%B5%96-material-aea8ec.md#f-122e52a857e870c2)。
- `bke::node_tree_free_embedded_tree` → [blender::bke::node_tree_free_embedded_tree · L5231](../05-%E5%87%A0%E4%BD%95%E5%AD%98%E5%82%A8%E4%B8%8E%E6%8B%93%E6%89%91%E6%98%A0%E5%B0%84/%E4%BE%9D%E8%B5%96-node-89d753.md#f-e6364f4755cadf8b)。
- `MEM_delete` → [MEM_delete · L400](../03-%E5%86%85%E5%AD%98%E5%88%86%E9%85%8D%E4%B8%8E%E8%BF%90%E8%A1%8C%E6%97%B6%E7%B1%BB%E5%9E%8B/%E4%BE%9D%E8%B5%96-MEM_guardedalloc-b54eca.md#f-9049ffdd1682887c)。
- `bke::node_tree_copy_tree` → [blender::bke::node_tree_copy_tree · L5021](../05-%E5%87%A0%E4%BD%95%E5%AD%98%E5%82%A8%E4%B8%8E%E6%8B%93%E6%89%91%E6%98%A0%E5%B0%84/%E4%BE%9D%E8%B5%96-node-89d753.md#f-aee0c08c96ccd443)。
- `ma->nodetree->all_nodes` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L62。
- `STRNCPY_UTF8` → [STRNCPY_UTF8 · L335](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_string_utf8-bcc961.md#m-222967f0ab6a)。宏定义由构建条件选择。
- `DATA_` → [DATA_ · L52](../05-%E5%87%A0%E4%BD%95%E5%AD%98%E5%82%A8%E4%B8%8E%E6%8B%93%E6%89%91%E6%98%A0%E5%B0%84/%E4%BE%9D%E8%B5%96-BLT_translation-c89e58.md#m-178736083f83)。宏定义由构建条件选择。
- `bke::node_unique_name` → [blender::bke::node_unique_name · L4238](../05-%E5%87%A0%E4%BD%95%E5%AD%98%E5%82%A8%E4%B8%8E%E6%8B%93%E6%89%91%E6%98%A0%E5%B0%84/%E4%BE%9D%E8%B5%96-node-89d753.md#f-fb3ea2e8319c3590)。
- `BKE_ntree_update_after_single_tree_change` → [blender::BKE_ntree_update_after_single_tree_change · L2421](../05-%E5%87%A0%E4%BD%95%E5%AD%98%E5%82%A8%E4%B8%8E%E6%8B%93%E6%89%91%E6%98%A0%E5%B0%84/%E4%BE%9D%E8%B5%96-node_tree_update-60230f.md#f-60cd3f41995f06e2)。
- `ELEM` → [ELEM · L88](../05-%E5%87%A0%E4%BD%95%E5%AD%98%E5%82%A8%E4%B8%8E%E6%8B%93%E6%89%91%E6%98%A0%E5%B0%84/%E4%BE%9D%E8%B5%96-GHOST_utildefines-34b996.md#m-d28724a15928)；[ELEM · L135](../01-%E5%9F%BA%E7%A1%80%E5%AE%B9%E5%99%A8%E4%B8%8E%E7%8E%B0%E4%BB%A3CPP/%E4%BE%9D%E8%B5%96-BLI_utildefines-293a0a.md#m-d6572de7cae0)。宏定义由构建条件选择。
- `bke::node_add_static_node` → [blender::bke::node_add_static_node · L4283](../05-%E5%87%A0%E4%BD%95%E5%AD%98%E5%82%A8%E4%B8%8E%E6%8B%93%E6%89%91%E6%98%A0%E5%B0%84/%E4%BE%9D%E8%B5%96-node-89d753.md#f-aaa71011c0fa550b)。
- `bke::node_add_link` → [blender::bke::node_add_link · L4638](../05-%E5%87%A0%E4%BD%95%E5%AD%98%E5%82%A8%E4%B8%8E%E6%8B%93%E6%89%91%E6%98%A0%E5%B0%84/%E4%BE%9D%E8%B5%96-node-89d753.md#f-e4b0f883348f0d24)。
- `bke::node_find_socket` → [blender::bke::node_find_socket · L3036](../05-%E5%87%A0%E4%BD%95%E5%AD%98%E5%82%A8%E4%B8%8E%E6%8B%93%E6%89%91%E6%98%A0%E5%B0%84/%E4%BE%9D%E8%B5%96-node-89d753.md#f-cbf9dec71aff5b59)；[blender::bke::node_find_socket · L3047](../05-%E5%87%A0%E4%BD%95%E5%AD%98%E5%82%A8%E4%B8%8E%E6%8B%93%E6%89%91%E6%98%A0%E5%B0%84/%E4%BE%9D%E8%B5%96-node-89d753.md#f-4a7a677634b7fbd1)。同名重载需按实参类型选择。
- `copy_v3_v3` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：函数指针、局部可调用对象或未展开的宏；必须结合调用者环境。调用位置L87。
- `bke::node_tree_add_tree_embedded` → [blender::bke::node_tree_add_tree_embedded · L5005](../05-%E5%87%A0%E4%BD%95%E5%AD%98%E5%82%A8%E4%B8%8E%E6%8B%93%E6%89%91%E6%98%A0%E5%B0%84/%E4%BE%9D%E8%B5%96-node-89d753.md#f-8357c25dd4ab30ef)。
- `ntreeType_Shader->idname.ref` → [调用协议](../%E6%A8%A1%E6%9D%BF%E5%AE%8F%E4%B8%8E%E5%8A%A8%E6%80%81%E5%88%86%E6%B4%BE%E5%8D%8F%E8%AE%AE.md)：接收对象类型依赖auto、返回值或模板实例；不按同名猜测目标。调用位置L92。
- `bke::node_set_active` → [blender::bke::node_set_active · L5484](../05-%E5%87%A0%E4%BD%95%E5%AD%98%E5%82%A8%E4%B8%8E%E6%8B%93%E6%89%91%E6%98%A0%E5%B0%84/%E4%BE%9D%E8%B5%96-node-89d753.md#f-7b2e1b01e127aa57)。
- `printf` → [外部契约](https://eel.is/c++draft/)：这个边界按实际表达式及所属类型核对参数、返回值、寿命与失败行为。这里提供接口入口，不声称已解释该第三方版本的内部实现。
