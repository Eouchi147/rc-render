"""Proper 3D figures for the dioramas: an anatomical skeleton (8 heads tall) skinned with Blender's Skin modifier and
smoothed, a head with brow, nose and jaw, clothes (tunic, cloak, hood), head bandages and a staff. Poses: a walking cycle
phase, a forward bow, arms hanging / reaching to the shoulder ahead / holding a staff."""
import bpy, bmesh, math
from mathutils import Vector, Matrix

def _mat(name, col, rough=0.85, sheen=0.0):
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*col, 1); b.inputs['Roughness'].default_value = rough
    if sheen:
        b.inputs['Sheen Weight'].default_value = sheen
    return m

def _rot(v, ax, ang):
    return Matrix.Rotation(ang, 3, ax) @ v

def skeleton(phase=0.0, stride=0.5, bow=0.25, arm='hang', arm2='hang'):
    """Joint positions in body units (height 1, feet at 0, facing +X, left = +Y)."""
    s = math.sin(phase) * stride
    J = {}
    pel = Vector((0.0, 0.0, 0.53 - 0.012 * abs(s)))
    J['pelvis'] = pel
    # spine bends forward by `bow` (radians) from the pelvis
    def up(l, ang):
        return Vector((math.sin(ang) * l, 0, math.cos(ang) * l))
    J['spine'] = pel + up(0.12, bow * 0.4)
    J['chest'] = J['spine'] + up(0.12, bow * 0.8)
    J['neck'] = J['chest'] + up(0.08, bow * 1.1)
    J['head'] = J['neck'] + up(0.075, bow * 1.3)
    for side, sg in (('L', 1), ('R', -1)):
        sw = s * sg
        J['hip' + side] = pel + Vector((0, 0.055 * sg, -0.02))
        th = 0.55 * sw                                    # thigh swing
        kn = J['hip' + side] + Vector((math.sin(th) * 0.245, 0, -math.cos(th) * 0.245))
        bend = 0.15 + max(0.0, -sw) * 0.9                 # the back leg bends as it lifts
        sh = th - bend
        an = kn + Vector((math.sin(sh) * 0.24, 0, -math.cos(sh) * 0.24))
        an.z = max(an.z, 0.04)
        J['knee' + side], J['ankle' + side] = kn, an
        J['toe' + side] = an + Vector((0.09, 0, -0.03))
        J['toe' + side].z = max(J['toe' + side].z, 0.01)
        sho = J['chest'] + Vector((0.0, 0.115 * sg, 0.045))
        J['sho' + side] = sho
        a = arm if side == 'R' else arm2
        if a == 'fwd':                                    # reaching to the shoulder of the man ahead
            el = sho + Vector((0.16, -0.02 * sg, -0.07)); wr = el + Vector((0.17, -0.03 * sg, 0.05))
        elif a == 'staff':
            el = sho + Vector((0.08, 0.05 * sg, -0.15)); wr = el + Vector((0.14, 0.0, 0.03))
        else:                                             # hanging, swinging against the leg
            sa = -0.5 * sw
            el = sho + Vector((math.sin(sa) * 0.15, 0.01 * sg, -math.cos(sa) * 0.15))
            wr = el + Vector((math.sin(sa + 0.25) * 0.14, 0.0, -math.cos(sa + 0.25) * 0.14))
        J['elb' + side], J['wri' + side] = el, wr
        J['hand' + side] = wr + (wr - el).normalized() * 0.06
    return J

BONES = [('pelvis', 'spine'), ('spine', 'chest'), ('chest', 'neck'), ('neck', 'head'),
         ('pelvis', 'hipL'), ('hipL', 'kneeL'), ('kneeL', 'ankleL'), ('ankleL', 'toeL'),
         ('pelvis', 'hipR'), ('hipR', 'kneeR'), ('kneeR', 'ankleR'), ('ankleR', 'toeR'),
         ('chest', 'shoL'), ('shoL', 'elbL'), ('elbL', 'wriL'), ('wriL', 'handL'),
         ('chest', 'shoR'), ('shoR', 'elbR'), ('elbR', 'wriR'), ('wriR', 'handR')]
RAD = dict(pelvis=(0.075, 0.095), spine=(0.07, 0.085), chest=(0.08, 0.105), neck=(0.03, 0.03), head=(0.03, 0.03),
           hipL=(0.06, 0.06), hipR=(0.06, 0.06), kneeL=(0.04, 0.04), kneeR=(0.04, 0.04), ankleL=(0.026, 0.026),
           ankleR=(0.026, 0.026), toeL=(0.02, 0.026), toeR=(0.02, 0.026), shoL=(0.04, 0.04), shoR=(0.04, 0.04),
           elbL=(0.03, 0.03), elbR=(0.03, 0.03), wriL=(0.022, 0.022), wriR=(0.022, 0.022), handL=(0.024, 0.014),
           handR=(0.024, 0.014))

def figure(name, base, height, yaw, phase=0.0, stride=0.5, bow=0.25, arm='hang', arm2='hang', cloth=(0.12, 0.09, 0.07),
           cloak=False, hood=False, bandage=False, one_eye=False, staff=False, skin=(0.42, 0.3, 0.24)):
    """Build one figure; base = feet position (world), height in world units, yaw in radians (0 = facing +X)."""
    J = skeleton(phase, stride, bow, arm, arm2)
    names = list(J)
    me = bpy.data.meshes.new(name + '_body')
    me.from_pydata([tuple(J[n]) for n in names], [(names.index(a), names.index(b)) for a, b in BONES], [])
    ob = bpy.data.objects.new(name + '_body', me); bpy.context.scene.collection.objects.link(ob)
    sk = ob.modifiers.new('skin', 'SKIN')
    for i, n in enumerate(names):
        r = RAD[n]; me.skin_vertices[0].data[i].radius = (r[0], r[1])
    me.skin_vertices[0].data[0].use_root = True
    ss = ob.modifiers.new('sub', 'SUBSURF'); ss.levels = 2; ss.render_levels = 2
    ob.data.materials.append(_mat('skin', skin, 0.6))
    parts = [ob]
    # head: skull, brow, nose, jaw
    h = J['head'] + Vector((0.0, 0, 0.035))
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.062, location=h, segments=32, ring_count=16)
    sk_ = bpy.context.object; sk_.scale = (1.12, 0.92, 1.12); parts.append(sk_)
    sk_.data.materials.append(_mat('skin', skin))
    bpy.ops.object.shade_smooth()
    fwd = (J['head'] - J['neck']).normalized()
    face = Vector((1, 0, 0))
    bpy.ops.mesh.primitive_cone_add(radius1=0.014, radius2=0.002, depth=0.035, location=h + face * 0.068 + Vector((0, 0, -0.008)))
    no = bpy.context.object; no.rotation_euler = (0, math.radians(100), 0); parts.append(no); no.data.materials.append(_mat('skin', skin))
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.045, location=h + face * 0.03 + Vector((0, 0, -0.045)), segments=20, ring_count=10)
    jw = bpy.context.object; jw.scale = (1.0, 1.05, 0.8); parts.append(jw); jw.data.materials.append(_mat('beard', (0.06, 0.05, 0.045), 0.9))
    bpy.ops.object.shade_smooth()
    # hair / hood
    if hood:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.078, location=h + Vector((-0.012, 0, 0.006)), segments=24, ring_count=12)
        hd = bpy.context.object; hd.scale = (1.15, 1.05, 1.15); parts.append(hd); hd.data.materials.append(_mat('cloth2', tuple(c * 0.8 for c in cloth)))
        bpy.ops.object.shade_smooth()
    # bandage over the eyes (the leader keeps one eye)
    if bandage:
        bpy.ops.mesh.primitive_torus_add(major_radius=0.064, minor_radius=0.011, location=h + Vector((0.004, 0, 0.004)))
        bd = bpy.context.object; bd.scale = (1.12, 0.95, 1.0); bd.rotation_euler = (0, math.radians(-8), 0); parts.append(bd)
        bd.data.materials.append(_mat('linen', (0.82, 0.78, 0.7), 0.9))
        if one_eye:
            bd.rotation_euler = (math.radians(14), math.radians(-8), 0)
    # tunic: a flared tube from the shoulders to the knees, belted
    def tube(nm, top, bot, r0, r1, depth_scale=(1.0, 1.0), mat=None, back=0.0):
        n = 24; verts = []; faces = []
        rings = 6
        for k in range(rings + 1):
            u = k / rings
            c = top.lerp(bot, u); r = r0 + (r1 - r0) * u ** 1.3
            for j in range(n):
                a = 2 * math.pi * j / n
                wob = 1 + 0.06 * math.sin(a * 7 + k) * u
                verts.append((c.x + (math.cos(a) * r * depth_scale[0] - back * u) * wob, c.y + math.sin(a) * r * depth_scale[1] * wob, c.z))
        for k in range(rings):
            for j in range(n):
                a_, b_ = k * n + j, k * n + (j + 1) % n
                faces.append((a_, b_, b_ + n, a_ + n))
        m_ = bpy.data.meshes.new(nm); m_.from_pydata(verts, [], faces)
        o_ = bpy.data.objects.new(nm, m_); bpy.context.scene.collection.objects.link(o_)
        for p in m_.polygons: p.use_smooth = True
        sd = o_.modifiers.new('s', 'SOLIDIFY'); sd.thickness = 0.008
        sb = o_.modifiers.new('sub', 'SUBSURF'); sb.levels = 1; sb.render_levels = 2
        o_.data.materials.append(mat or _mat('cloth', cloth, 0.9, 0.3))
        return o_
    knee_z = (J['kneeL'].z + J['kneeR'].z) / 2
    parts.append(tube(name + '_tunic', J['chest'] + Vector((0, 0, 0.05)), Vector((J['pelvis'].x + 0.02, 0, knee_z - 0.02)), 0.1, 0.15,
                      (0.85, 1.0)))
    if cloak:
        parts.append(tube(name + '_cloak', J['neck'] + Vector((-0.02, 0, -0.01)), Vector((J['pelvis'].x - 0.06, 0, 0.12)), 0.12, 0.22,
                          (0.9, 1.05), _mat('cloak', tuple(c * 0.7 for c in cloth), 0.95, 0.4), back=0.05))
    if staff:
        hand = J['handR']
        bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=1.15, location=(hand.x + 0.03, hand.y, 0.56))
        st = bpy.context.object; st.rotation_euler = (0, math.radians(-4), 0); parts.append(st)
        st.data.materials.append(_mat('wood', (0.2, 0.13, 0.08), 0.8))
    # join, then place in the world
    M = Matrix.Translation(base) @ Matrix.Rotation(yaw, 4, 'Z') @ Matrix.Scale(height, 4)
    for p in parts:
        p.matrix_world = M @ p.matrix_world
    return parts
