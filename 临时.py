import bpy

ui_scale = bpy.context.preferences.system.dpi / 72
nodes = bpy.data.node_groups["Geometry Nodes"].nodes

nodes_l = list(nodes)
for node in nodes_l:
    print(node.name)
    reroute1 = nodes.new(type="NodeReroute")
    reroute2 = nodes.new(type="NodeReroute")
    reroute1.location = node.location
    reroute2.location = node.location
    height = node.dimensions.y / ui_scale
    if node.hide:
        reroute1.location.y -= (height / 2 + 9)
        reroute2.location.y += (height / 2 - 9)
    else:
        reroute1.location.y -= height


def node_top_y(node: bpy.types.Node):
    height = node.dimensions.y / ui_scale
    if node.hide:
        return node.location.y - (height / 2 + 9)
    else:
        return node.location.y

def node_bottom_y(node: bpy.types.Node):
    height = node.dimensions.y / ui_scale
    if node.hide:
        return node.location.y + (height / 2 - 9)
    else:
        return node.location.y - height


