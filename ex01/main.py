"""
writer:
Yudha Styawan

email:
yudhastyawan@gmail.com

usage:
1D wave simulation generator in blender

"""

import bpy
import bmesh
import os
import numpy as np


# in fact, we can't use the absolute path of this file, so we manually input it.
dirfile = '/path/to/directory'

# read ac1d.py file and execute it in this file
with open(os.path.join(dirfile, 'ac1d.py'), 'r') as f:
    exec(f.read())

x, dx, amps, fps = getwave()

# simply normalize to get amplitude around -1 and 1 and then multiply by 10 in order to show the displacements
amps = amps / np.max(np.abs(amps))
amps = amps * 10


# a function to generate keyframes
# origin code: https://blender.stackexchange.com/questions/196554/how-to-keyframe-mesh-vertices-in-python-without-fcurve
def keyframe(vert, frame):
    for index in range(3):    
        vert.keyframe_insert("co", index=index, frame=frame, group="location")

# a main function
def execute():
    ch = []
    for i, xi in enumerate(x[:-1]):
        bpy.ops.mesh.primitive_cube_add(size=dx, location=(xi+dx/2, 0, 0), scale=(1, 1, 1))     # create cubes
        bpy.context.active_object.name = f'c{i}'
        obj = bpy.data.objects[f'c{i}']
        
        mod = obj.modifiers.new("wf1", 'WIREFRAME')                                             # add a wireframe modifier to show the edges
        mod.use_replace = False
        mod.thickness = 0.074
        mod.material_offset = 1
        
        mat = bpy.data.materials.new(name="Material")                                           # a main material
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        node = nodes.new('ShaderNodeBsdfDiffuse')
        node.inputs[0].default_value = (1, 1, 1, 1)
        material_output = nodes.get('Material Output')
        mat.node_tree.links.new(material_output.inputs[0], node.outputs[0])
        obj.data.materials.append(mat)
        
        mat = bpy.data.materials.new(name="Material")                                           # an edges material
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        node = nodes.new('ShaderNodeBsdfDiffuse')
        node.inputs[0].default_value = (0.022263, 0.00763625, 0.8, 1)
        material_output = nodes.get('Material Output')
        mat.node_tree.links.new(material_output.inputs[0], node.outputs[0])
        obj.data.materials.append(mat)
        mesh = obj.data
        
        for v in mesh.vertices:                                                                 # identifying each side of the cube edges (-1 for left and 1 for right side in x-direction)
            if np.isclose(v.co[0], -1*dx/2):
                ch.append(-1)
            elif np.isclose(v.co[0], dx/2):
                ch.append(1)
            else:
                ch.append(0)

    for it in range(len(amps[:,0])):
        ich = 0
        for i, _ in enumerate(x[:-1]):
            obj = bpy.data.objects[f'c{i}']
            bpy.context.view_layer.objects.active = obj
            mesh = obj.data
            for v in mesh.vertices:                                                             # apply the displacements to each side of the cube edges
                if ch[ich] == -1:
                    v.co[0] = (-1*dx/2) + amps[it,i]
                elif ch[ich] == 1:
                    v.co[0] = (dx/2) + amps[it,i+1]
                keyframe(v,it)
                ich += 1
        print(it)

# a function to remove all cubes
def erase():
    bpy.ops.object.select_all(action='DESELECT')
    for i, _ in enumerate(x[:-1]):
        bpy.data.objects[f'c{i}'].select_set(True)
    bpy.ops.object.delete()

# switch execute and remove cubes by assigning m to 0 and non-0 value.
m = 0 #
if m == 0: execute()
else: erase()