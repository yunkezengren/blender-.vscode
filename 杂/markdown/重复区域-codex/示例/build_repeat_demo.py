"""Run inside Blender: create a repeat x <- 2*x+1 and expose x as a named attribute.

Example: blender --background --factory-startup --python build_repeat_demo.py
Only resources with our exact dedicated names are reused/removed.
No blend file is saved by this script.
"""
import bpy
import json

PREFIX = 'RZ_Codex_Affine_Demo'


def item_socket(sockets, item):
    # RepeatItem.identifier is an internal DNA field, not exposed in the tested RNA.
    # This freshly created item has a unique script-controlled name. The socket
    # itself exposes identifier if callers need to retain a stable lookup key.
    return next(s for s in sockets if s.name == item.name)


def build():
    obj = bpy.data.objects.get(PREFIX)
    if obj is not None:
        bpy.data.objects.remove(obj, do_unlink=True)
    old_group = bpy.data.node_groups.get(PREFIX)
    if old_group is not None and old_group.users == 0:
        bpy.data.node_groups.remove(old_group)
    mesh = bpy.data.meshes.new(PREFIX)
    mesh.from_pydata([(0, 0, 0)], [], [])
    obj = bpy.data.objects.new(PREFIX, mesh)
    bpy.context.scene.collection.objects.link(obj)
    group = bpy.data.node_groups.new(PREFIX, 'GeometryNodeTree')
    group.interface.new_socket(name='Geometry', in_out='INPUT', socket_type='NodeSocketGeometry')
    group.interface.new_socket(name='Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')
    nodes, links = group.nodes, group.links
    source = nodes.new('NodeGroupInput')
    sink = nodes.new('NodeGroupOutput')
    begin = nodes.new('GeometryNodeRepeatInput')
    end = nodes.new('GeometryNodeRepeatOutput')
    begin.pair_with_output(end)
    # Default geometry item is retained; float is a second independent state.
    item = end.repeat_items.new('FLOAT', 'StateX')
    begin.inputs['Iterations'].default_value = 3
    item_socket(begin.inputs, item).default_value = 1.0
    multiply = nodes.new('ShaderNodeMath')
    multiply.operation = 'MULTIPLY'
    multiply.inputs[1].default_value = 2.0
    add = nodes.new('ShaderNodeMath')
    add.operation = 'ADD'
    add.inputs[1].default_value = 1.0
    store = nodes.new('GeometryNodeStoreNamedAttribute')
    store.data_type = 'FLOAT'
    store.domain = 'POINT'
    store.inputs['Name'].default_value = 'rz_state_x'
    geometry_in = next(s for s in begin.inputs if s.type == 'GEOMETRY')
    geometry_body_out = next(s for s in begin.outputs if s.type == 'GEOMETRY')
    geometry_body_in = next(s for s in end.inputs if s.type == 'GEOMETRY')
    geometry_out = next(s for s in end.outputs if s.type == 'GEOMETRY')
    links.new(source.outputs['Geometry'], geometry_in)
    links.new(geometry_body_out, geometry_body_in)
    links.new(item_socket(begin.outputs, item), multiply.inputs[0])
    links.new(multiply.outputs[0], add.inputs[0])
    links.new(add.outputs[0], item_socket(end.inputs, item))
    links.new(geometry_out, store.inputs['Geometry'])
    links.new(item_socket(end.outputs, item), store.inputs['Value'])
    links.new(store.outputs['Geometry'], sink.inputs['Geometry'])
    for node, x, y in [(source, -650, 100), (begin, -400, 100),
                       (multiply, -150, -100), (add, 50, -100),
                       (end, 300, 100), (store, 550, 100), (sink, 800, 100)]:
        node.location = (x, y)
    modifier = obj.modifiers.new(PREFIX, 'NODES')
    modifier.node_group = group
    return obj, begin


def verify(obj, begin):
    observations = []
    for count, expected in [(0, 1.0), (1, 3.0), (2, 7.0), (3, 15.0)]:
        begin.inputs['Iterations'].default_value = count
        obj.update_tag()
        bpy.context.view_layer.update()
        depsgraph = bpy.context.evaluated_depsgraph_get()
        evaluated = obj.evaluated_get(depsgraph)
        mesh = evaluated.to_mesh()
        try:
            attribute = mesh.attributes.get('rz_state_x')
            assert attribute is not None, 'Missing output attribute'
            actual = attribute.data[0].value
            assert abs(actual-expected) < 1e-6, (count, actual, expected)
            observations.append({'iterations': count, 'actual': actual, 'expected': expected})
        finally:
            evaluated.to_mesh_clear()
    begin.inputs['Iterations'].default_value = 3
    return observations


if __name__ == '__main__':
    obj, begin = build()
    print('RZ_DEMO_RESULT '+json.dumps(verify(obj, begin), ensure_ascii=False))
