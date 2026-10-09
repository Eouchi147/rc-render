"""Build the scene as a 3D diorama in Blender and render one look.
    blender -b -P blend.py -- scene.json sky.png LOOK out.png
Each design layer becomes a thin extruded card at its own depth, scaled so the camera sees the original composition:
real parallax, light, fog, depth of field and materials from the films' own drawings. Looks:
  papercut  layered card dioramas (thick paper, soft shadows, warm practical lights, light haze)
  theatre   shadow-puppet theatre (black cut-outs against a glowing cloth screen)
  clay      handmade miniature (rounded clay forms, soft studio light, tilt-shift focus)
  noir      graphic noir (flat blacks, gold ink outlines, one hard light)
  volume    moody volumetric (coloured cards in thick atmosphere, light shafts)"""
import bpy, sys, json, math
from mathutils import Vector
a = sys.argv[sys.argv.index('--') + 1:]
J, SKY, LOOK, OUT = a[0], a[1], a[2], a[3]
D = json.load(open(J))
F = 2000.0                       # camera distance to the design plane (design px units)
SCREEN_D = 300.0                 # theatre: the cloth screen
DEPTH = 7000.0                   # depth of the far end of the diorama
W, H = 720, 1280

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'
sc.cycles.device = 'CPU'
sc.cycles.samples = 48 if LOOK in ('volume', 'papercut') else 32
sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = W, H
sc.render.film_transparent = False
sc.view_settings.view_transform = 'AgX'
sc.view_settings.look = 'AgX - Medium High Contrast'
sc.cycles.max_bounces = 4

def depth(z):
    return (1.0 - z) ** 1.35 * DEPTH

def place(x, y, d, s=None):
    s = (F + d) / F if s is None else s
    return Vector((540 + (x - 540) * s, d, -960 - (y - 960) * s))

def mat_principled(name, col, rough=0.8, emit=0.0, alpha=1.0, sss=0.0, trans=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*col, 1)
    b.inputs['Roughness'].default_value = rough
    if emit > 0:
        b.inputs['Emission Color'].default_value = (*col, 1)
        b.inputs['Emission Strength'].default_value = emit
    if alpha < 1:
        b.inputs['Alpha'].default_value = alpha
    if sss:
        b.inputs['Subsurface Weight'].default_value = sss
    if trans:
        b.inputs['Transmission Weight'].default_value = trans
    return m

def add_noise_bump(m, scale=0.02, strength=0.25):
    nt = m.node_tree
    tex = nt.nodes.new('ShaderNodeTexNoise'); tex.inputs['Scale'].default_value = scale; tex.inputs['Detail'].default_value = 8
    bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = strength
    nt.links.new(tex.outputs['Fac'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], nt.nodes['Principled BSDF'].inputs['Normal'])

def card(name, polys, d, thick, mat, bevel=0.0, smooth=False, rim=None, subsurf=0):
    verts, faces = [], []
    s = (F + d) / F
    for p in polys:
        if len(p) < 3:
            continue
        i0 = len(verts)
        for x, y in p:
            v = place(x, y, d, s); verts.append((v.x, v.y, v.z))
        faces.append(list(range(i0, i0 + len(p))))
    if not faces:
        return None
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.validate()
    ob = bpy.data.objects.new(name, me); sc.collection.objects.link(ob)
    ob.data.materials.append(mat)
    sol = ob.modifiers.new('t', 'SOLIDIFY'); sol.thickness = thick * s; sol.offset = 1.0
    if rim is not None:
        ob.data.materials.append(rim); sol.material_offset_rim = 1
    if bevel:
        bv = ob.modifiers.new('b', 'BEVEL'); bv.width = bevel * s; bv.segments = 3; bv.limit_method = 'ANGLE'
    if subsurf:
        ss = ob.modifiers.new('s', 'SUBSURF'); ss.levels = subsurf; ss.render_levels = subsurf
    if smooth:
        for poly in me.polygons:
            poly.use_smooth = True
    return ob

def tint(c, k=1.0, sat=1.0, lift=0.0):
    l = sum(c) / 3
    return tuple(max(0.0, min(1.0, (l + (ci - l) * sat) * k + lift)) for ci in c)

# ------------------------------------------------------------------ the cards
items = D['items']
RIM = mat_principled('rim', (0.92, 0.88, 0.8), 0.95)
for i, it in enumerate(items):
    d = depth(it['z'])
    col = tuple(it['col'])
    emis = it['emit'] > 0.05 or it['mat'] in ('window', 'glint')
    thin = it['line'] or it['mat'] in ('rope', 'foam', 'rain', 'grass', 'shrub')
    if it['mat'] == 'rain' or it['name'] in ('sheen', 'curtain'):
        continue
    if LOOK == 'papercut':
        m = mat_principled(f'm{i}', tint(col, 1.5, 0.9, 0.03), 0.95, emit=4.0 if emis else 0)
        if not emis: add_noise_bump(m, 0.08, 0.35)
        card(f'c{i}', it['polys'], d, 4.0 if thin else 18.0, m, rim=None if thin else RIM)
    elif LOOK == 'theatre':
        # cut-outs BEHIND a lit cloth screen: the camera sees their shadows, sharp when close to the screen
        if emis:
            continue
        m = mat_principled(f'm{i}', (0.0, 0.0, 0.0), 1.0)
        gap = 30 + (1 - it['z']) * 900
        card(f'c{i}', it['polys'], SCREEN_D + gap, 2.0, m)
    elif LOOK == 'clay':
        m = mat_principled(f'm{i}', tint(col, 2.0, 1.25, 0.06), 0.45, emit=3.0 if emis else 0, sss=0.25)
        card(f'c{i}', it['polys'], d, 6.0 if thin else 60.0, m, bevel=0 if thin else 22.0, smooth=True, subsurf=0 if thin else 1)
    elif LOOK == 'noir':
        l = sum(col) / 3
        g = 0.85 if l > 0.45 else (0.1 if l > 0.18 else 0.015)
        m = mat_principled(f'm{i}', (1.0, 0.7, 0.3) if emis else (g, g * 0.97, g * 0.92), 0.9, emit=5.0 if emis else 0)
        card(f'c{i}', it['polys'], d, 3.0, m)
    else:  # volume
        m = mat_principled(f'm{i}', tint(col, 1.25, 1.1), 0.7, emit=5.0 if emis else 0, alpha=it['alpha'])
        card(f'c{i}', it['polys'], d, 6.0, m)

# ------------------------------------------------------------------ the sky / screen at the back
if LOOK == 'theatre':
    bpy.ops.mesh.primitive_plane_add(size=1); scr = bpy.context.object
    ss_ = (F + SCREEN_D) / F
    scr.scale = (1500 * ss_, 2400 * ss_, 1); scr.rotation_euler = (math.radians(90), 0, 0); scr.location = place(540, 960, SCREEN_D, ss_)
    ms = bpy.data.materials.new('screen'); ms.use_nodes = True; nt = ms.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    o = nt.nodes.new('ShaderNodeOutputMaterial'); tr = nt.nodes.new('ShaderNodeBsdfTranslucent')
    tr.inputs['Color'].default_value = (1.0, 0.78, 0.52, 1)
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 0.4; nz.inputs['Detail'].default_value = 10
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.08
    nt.links.new(nz.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], tr.inputs['Normal'])
    nt.links.new(tr.outputs['BSDF'], o.inputs['Surface']); scr.data.materials.append(ms)
    for (lx, ly, e, c) in ((540, 900, 3.0e8, (1.0, 0.72, 0.45)), (200, 500, 0.8e8, (1.0, 0.45, 0.3))):
        al = bpy.data.lights.new('back', 'AREA'); al.energy = e; al.size = 500; al.color = c
        ao = bpy.data.objects.new('back', al); sc.collection.objects.link(ao)
        ao.location = place(lx, ly, SCREEN_D + 2600); ao.rotation_euler = (math.radians(90), 0, 0)
img = bpy.data.images.load(SKY)
dback = DEPTH * 1.05
sback = (F + dback) / F
bpy.ops.mesh.primitive_plane_add(size=1)
pl = bpy.context.object
pl.scale = (1080 * sback * 1.15, 1920 * sback * 1.15, 1); pl.rotation_euler = (math.radians(90), 0, 0)
pl.location = place(540, 960, dback, sback)
m = bpy.data.materials.new('sky'); m.use_nodes = True; nt = m.node_tree
for n in list(nt.nodes):
    nt.nodes.remove(n)
o = nt.nodes.new('ShaderNodeOutputMaterial'); em = nt.nodes.new('ShaderNodeEmission'); tx = nt.nodes.new('ShaderNodeTexImage')
tx.image = img; tx.extension = 'EXTEND'
nt.links.new(tx.outputs['Color'], em.inputs['Color']); nt.links.new(em.outputs['Emission'], o.inputs['Surface'])
if LOOK == 'theatre':
    rgb = nt.nodes.new('ShaderNodeRGB'); rgb.outputs[0].default_value = (1.0, 0.62, 0.3, 1)
    mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'; mix.inputs['Factor'].default_value = 0.75
    nt.links.new(tx.outputs['Color'], mix.inputs['A']); nt.links.new(rgb.outputs[0], mix.inputs['B'])
    nt.links.new(mix.outputs['Result'], em.inputs['Color'])
    em.inputs['Strength'].default_value = 2.2
elif LOOK == 'noir':
    em.inputs['Strength'].default_value = 0.35
else:
    em.inputs['Strength'].default_value = 1.0
pl.data.materials.append(m)
if LOOK == 'theatre':
    pl.hide_render = True

# ------------------------------------------------------------------ lights
kx, ky = D['key_dir']; kc = tuple(D['key_col'])
key = bpy.data.lights.new('key', 'SUN'); key.energy = {'noir': 6.0, 'theatre': 0.0, 'clay': 3.5, 'papercut': 3.5}.get(LOOK, 2.5)
key.color = (1.0, 0.95, 0.9) if LOOK == 'clay' else tuple(min(1, c * 1.6) for c in kc)
key.angle = math.radians(0.5 if LOOK == 'noir' else 8)
ko = bpy.data.objects.new('key', key); sc.collection.objects.link(ko)
ko.rotation_euler = (math.radians(-60 + 25 * ky), math.radians(35 * kx + (40 if LOOK in ('papercut', 'clay') else 0)), 0)
for j, L in enumerate(D['lights']):
    pl_ = bpy.data.lights.new(f'p{j}', 'POINT'); pl_.color = tuple(L['col']); pl_.shadow_soft_size = 6
    d = depth(L['z']); s = (F + d) / F
    pl_.energy = L['I'] * (L['r'] * s) ** 2 * 60
    po = bpy.data.objects.new(f'p{j}', pl_); sc.collection.objects.link(po)
    po.location = place(L['x'], L['y'], d - 40 * s, s)
if LOOK == 'clay':
    fill = bpy.data.lights.new('fill', 'AREA'); fill.energy = 4e7; fill.size = 3000; fill.color = (0.8, 0.85, 1.0)
    fo = bpy.data.objects.new('fill', fill); sc.collection.objects.link(fo)
    fo.location = (540, -2500, 1200); fo.rotation_euler = (math.radians(60), 0, 0)

# world ambient
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
bg = w.node_tree.nodes['Background']
amb = tuple(D['amb'])
bg.inputs['Color'].default_value = (*amb, 1)
bg.inputs['Strength'].default_value = {'theatre': 0.05, 'noir': 0.08, 'clay': 0.9}.get(LOOK, 0.5)

# atmosphere
if LOOK in ('volume', 'papercut'):
    bpy.ops.mesh.primitive_cube_add(size=1)
    cu = bpy.context.object
    cu.scale = (40000, DEPTH * 1.1, 40000); cu.location = (540, DEPTH * 0.5, -960)
    vm = bpy.data.materials.new('fog'); vm.use_nodes = True
    vt = vm.node_tree
    vt.nodes.remove(vt.nodes['Principled BSDF'])
    pv = vt.nodes.new('ShaderNodeVolumePrincipled')
    pv.inputs['Density'].default_value = 0.0004 if LOOK == 'volume' else 0.00008
    pv.inputs['Anisotropy'].default_value = 0.6
    pv.inputs['Color'].default_value = (0.9, 0.85, 0.8, 1)
    vt.links.new(pv.outputs['Volume'], vt.nodes['Material Output'].inputs['Volume'])
    cu.data.materials.append(vm)
    sc.cycles.volume_step_rate = 4.0
    if D.get('sun') and LOOK == 'volume':      # a hard light behind the scene through the haze: light shafts
        sp = bpy.data.lights.new('shaft', 'SPOT'); sp.energy = 4e9; sp.spot_size = math.radians(70); sp.shadow_soft_size = 20
        sp.color = (1.0, 0.8, 0.55)
        so = bpy.data.objects.new('shaft', sp); sc.collection.objects.link(so)
        so.location = place(D['sun'][0], D['sun'][1], DEPTH * 0.98)
        so.rotation_euler = (math.radians(-90), 0, 0)

# ------------------------------------------------------------------ camera
cam = bpy.data.cameras.new('cam'); cam.sensor_fit = 'HORIZONTAL'
cam.angle = 2 * math.atan(540 / F)
cam.clip_end = DEPTH * 3
co = bpy.data.objects.new('cam', cam); sc.collection.objects.link(co); sc.camera = co
if LOOK in ('papercut', 'clay', 'volume'):
    co.location = (540 + 420, -F, -960 + 160); co.rotation_euler = (math.radians(90 - 4), 0, math.radians(11))
    cam.angle = 2 * math.atan(600 / F)
else:
    co.location = (540, -F, -960); co.rotation_euler = (math.radians(90), 0, 0)
if LOOK in ('clay', 'papercut', 'volume'):
    cam.dof.use_dof = True
    cam.dof.focus_distance = F + depth(0.62)
    cam.dof.aperture_fstop = {'clay': 1.4, 'papercut': 4.0, 'volume': 5.6}[LOOK]
    cam.lens_unit = 'MILLIMETERS'
if LOOK == 'noir':
    sc.render.use_freestyle = True
    sc.render.line_thickness_mode = 'ABSOLUTE'; sc.render.line_thickness = 1.6
    fs = sc.view_layers[0].freestyle_settings
    ls = fs.linesets[0] if len(fs.linesets) else fs.linesets.new('lines')
    if ls.linestyle is None:
        ls.linestyle = bpy.data.linestyles.new('gold')
    ls.linestyle.color = (0.95, 0.72, 0.35)
sc.render.filepath = OUT
bpy.ops.render.render(write_still=True)
print('done', LOOK, OUT)
