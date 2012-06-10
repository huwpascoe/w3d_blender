import os
from . import w3d_struct

def aggregate(root, paths):
    ag_hlod(root, paths)
    
    ags = []
    for a in ag_aggregate(root, paths):
        ag_hlod(a, paths)
        ags.append(a)
    
    return ags

def ag_aggregate(root, paths):
    files = {}
    
    ag = root.get('aggregate')
    if ag is not None:
        ainfo = ag.get('aggregate_info')
        files[ainfo.BaseModelName] = True
        for s in ainfo.Subobjects:
            files[s['SubobjectName']] = True
    
    return ag_load(files.keys(), paths)
    
def ag_hlod(root, paths):
    files = {}
    
    # hlod
    hlod = root.get('hlod')
    if hlod is not None:
        
        # hierarchy
        hinfo = hlod.get('hlod_header')
        hierarchy = root.get('hierarchy')
        if (hierarchy is None or
            hinfo.HierarchyName != hierarchy.get('hierarchy_header').Name):
            files[hinfo.HierarchyName] = True
            
        # object containers
        m = root.getRec('mesh_header3')
        ctr = m.ContainerName if m is not None else None
        
        for lod in hlod.find('hlod_lod_array'):
            for h in lod.find('hlod_sub_object'):
                s = h.Name.split('.')
                if len(s) > 1 and ctr != s[0]:
                    files[s[0]] = True
        
        for lod in hlod.find('hlod_aggregate_array'):
            for h in lod.find('hlod_sub_object'):
                files[h.Name] = True
    
    # concat w3ds
    concats = ag_load(files.keys(), paths)
    for c in concats:
        root.children += c.children

def ag_load(files, paths):
    roots = []
    for file in files:
        load = False
        for path in paths:
            filename = os.path.join(path, file.lower() + '.w3d')
            try:
                root = w3d_struct.load(filename)
                roots.append(root)
                load = True
                break
            except:
                pass
        if load == False:
            print('MISSING: ' + file.lower() + '.w3d')
    
    return roots