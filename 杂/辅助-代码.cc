为什么不去掉函数的drop_into_panel参数,把switch放在函数内判断 bool NodeSocketDropTarget::on_drop(bContext *C, const DragInfo &drag_info) const
{
  bNodeTree &nodetree = this->get_view<NodeTreeInterfaceView>().nodetree();
  return on_drop_common(C, drag_info, nodetree, socket_.item, false);
}

bool NodePanelDropTarget::on_drop(bContext *C, const DragInfo &drag_info) const
{
  bNodeTree &nodetree = get_view<NodeTreeInterfaceView>().nodetree();
  switch (drag_info.drop_location) {
    case DropLocation::Into: {
      /* Insert into target */
      return on_drop_common(C, drag_info, nodetree, panel_.item, true);
    }
    case DropLocation::Before:
    case DropLocation::After: {
      /* Insert into same panel as the target. */
      return on_drop_common(C, drag_info, nodetree, panel_.item, false);
    }
  }
}
bool on_drop_common(bContext *C,
                    const DragInfo &drag_info,
                    bNodeTree &ntree,
                    bNodeTreeInterfaceItem &drop_target_item,
                    bool drop_into_panel = false)
{
  bNodeTreeInterfaceItemReference *drag_data = get_drag_node_tree_declaration(drag_info.drag_data);
  BLI_assert(drag_data != nullptr);

  bNodeTreeInterface &interface = ntree.tree_interface;
  bNodeTreeInterfaceItem *original_active = interface.active_item();
  bNodeTreeInterfacePanel *parent = nullptr;
  int insert_index = -1;

  /* 2. 计算初始插入点 (Base Index) */
  if (drop_into_panel) {
    parent = reinterpret_cast<bNodeTreeInterfacePanel *>(&drop_target_item);
    const bool has_toggle = parent->header_toggle_socket() != nullptr;
    insert_index = has_toggle ? 1 : 0;
  }
  else {
    parent = interface.find_item_parent(drop_target_item, true);
    BLI_assert(parent != nullptr);

    int target_idx = parent->items().as_span().first_index_try(&drop_target_item);
    if (target_idx < 0) {
      return false;
    }
    insert_index = target_idx + (drag_info.drop_location == DropLocation::After);
  }

  if (parent == nullptr || insert_index < 0) {
    return false;
  }

  /* 3. 循环移动并修正索引 */
  for (int i = 0; i < drag_data->items_count; i++) {
    bNodeTreeInterfaceItem *drag_item = drag_data->items[i];

    /* 查找当前 Item 现在的父级和位置 */
    bNodeTreeInterfacePanel *current_parent = interface.find_item_parent(*drag_item, true);
    int current_index = -1;
    if (current_parent) {
      current_index = current_parent->items().as_span().first_index_try(drag_item);
    }

    int final_index = current_index < insert_index ? insert_index : insert_index + i;

    interface.move_item_to_parent(*drag_item, parent, final_index);
  }

  interface.active_item_set(original_active);

  /* General update */
  BKE_main_ensure_invariants(*CTX_data_main(C), ntree.id);
  ED_undo_push(C, "Insert node group item");
  return true;
}
