import bpy
# tree = bpy.context.space_data.edit_tree
tree = bpy.data.node_groups["Instance on .001"]
interface = tree.interface
items = interface.items_tree
print("=" * 50)

# interface.active = items[5]
# interface.active_index = 100
# print(interface.active)
# print(interface.active_index)

for i in items:
    #    print(f"{i.index:2} {i.position:2} {i.item_type:6} {i.select:2} {i.name:6}")
    # print(f"{i.index:2} {i.position:2} {i.item_type:6} parent.index:{i.parent.index:2} {i.parent.parent is None}")
    select = "选中项" if i.select else "无    "
    active = "活动项" if i == interface.active else "无    "
    print(f"{i.index:2} {i.position:2} 父索引:{i.parent.index:2} {i.item_type:6} {select} {active} {i.name}")
