
name(1, 2)

def name(one, two):
    print(one, two)

name(1, 2)


import bpy
# tree = bpy.context.space_data.edit_tree
tree = bpy.data.node_groups["Instance on .002"]
items = tree.interface.items_tree
print("="*50)
for i in items:
    print(f"{i.index:2} {i.position:2} {i.item_type:6} parent:{i.parent.index:2} {i.parent.parent==None}")

# tree.interface.move_to_parent(items[6], None, 0)
items[1].is_panel_toggle = True

