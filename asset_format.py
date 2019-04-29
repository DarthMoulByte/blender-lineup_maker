import bpy
from . import variables as V
from . import helper as H
from . import preferences as P
from os import path
import time
import sys

class BpyAsset(object):
    def __init__(self, context, meshes, textures):
        self.separator = '_'
        self.context = context
        self.asset_name = self.get_asset_name(meshes)
        self.asset_root = self.get_asset_root(meshes)
        self.meshes = meshes
        self.textures = textures
        self.texture_set = {}

        self.naming_convention = self.get_naming_convention()
        
    # Decorators
    def check_asset_exist(func):
        def func_wrapper(self, *args, **kwargs):
            if self.asset_name in bpy.data.collections:
                return func(self, *args, **kwargs)
            else:
                print('Lineup Maker : Asset doesn\'t exist in current scene')
                return None
        return func_wrapper

    def check_length(func):
        def func_wrapper(self, *args, **kwargs):
            if not len(self.meshes):
                print('Lineup Maker : No file found in the asset folder')
                return None
            else:
                return func(self, *args, **kwargs)
        return func_wrapper
    # Methods
    def import_asset(self):
        self.import_mesh()
        self.import_texture()
    
    def update_asset(self):
        self.update_mesh()
        self.update_texture()

    def import_mesh(self, update=False):
        name,ext = path.splitext(path.basename(self.meshes[0]))

        curr_asset_collection = H.create_asset_collection(self.context, self.asset_name)

        H.set_active_collection(self.context, self.asset_name)

        for i,f in enumerate(self.meshes):
            name,ext = path.splitext(path.basename(f))

            # Import asset
            if ext.lower() in V.LM_COMPATIBLE_MESH_FORMAT.keys():
                print('Lineup Maker : Importing mesh "{}"'.format(name))
                compatible_format = V.LM_COMPATIBLE_MESH_FORMAT[ext.lower()]
                kwargs = {}
                kwargs.update({'filepath':f})
                kwargs.update(compatible_format[1])
                compatible_format[0](**kwargs)
            else:
                print('Lineup Maker : Skipping file "{}"\n     Incompatible format'.format(f))
                continue
            
            # register the mesh in scene variable
            if update:
                curr_asset = self.context.scene.lm_asset_list[self.asset_name]
            else:
                curr_asset = self.context.scene.lm_asset_list.add()
                curr_asset.name = self.asset_name
            
            curr_asset.last_update = path.getmtime(f)

            if update:
                curr_mesh_list = curr_asset.mesh_list[i]
            else:
                curr_mesh_list = curr_asset.mesh_list.add()
                curr_mesh_list.file_path = f

            for o in curr_asset_collection.objects:
                curr_mesh_list.mesh_name = o.name
                curr_mesh_list.mesh = o

                for m in o.material_slots:
                    if m.name not in curr_asset.material_list:
                        material_list = curr_asset.material_list.add()
                        material_list.material_name = m.material.name
                        material_list.material = m.material

                    curr_mesh_material_list = curr_mesh_list.material_list.add()
                    curr_mesh_material_list.material_name = m.material.name
                    curr_mesh_material_list.material = m.material
    

    @check_length
    def update_mesh(self):
        file = path.basename(self.meshes[0])
        name,ext = path.splitext(file)

        H.create_asset_collection(self.context, self.asset_name)
        H.set_active_collection(self.context, self.asset_name)

        if self.asset_name not in self.context.scene.lm_asset_list:
            self.remove_objects()
            self.import_mesh(update=True)
        else: # Update
            curr_asset = self.context.scene.lm_asset_list[self.asset_name]

            need_update = False

            for f in self.meshes:
                if curr_asset.last_update < path.getmtime(f):
                    need_update = True
                    break

            if need_update:
                print('Lineup Maker : Updating asset "{}" : {}'.format(self.asset_name, time.ctime(curr_asset.last_update)))
                print('Lineup Maker : Updating file "{}" : {}'.format(file, time.ctime(path.getmtime(f))))
                
                self.remove_objects()
                self.context.scene.update()
                self.import_mesh(update=True)
                # Dirty fix to avoid bad mesh naming when updating asset
                self.rename_objects()
            else:
                print('Lineup Maker : Asset "{}" is already up to date'.format(name))

    def import_texture(self):
        print(P.get_prefs().textureSet_albedo_keyword)
        print(P.get_prefs().textureSet_normal_keyword)
        print(P.get_prefs().textureSet_roughness_keyword)
        print(P.get_prefs().textureSet_metalic_keyword)
    
    def update_texture(self):
        pass

    # Helper

    def store_texture_set():
        pass
    
    def get_naming_convention(self):
        asset_name = H.slice(self.asset_name)
        asset_naming_convention = self.context.scene.lm_asset_naming_convention
        mesh_naming_convention = self.context.scene.lm_mesh_naming_convention
        texture_naming_convention = self.context.scene.lm_texture_naming_convention

        asset_keywords = H.slice(asset_naming_convention)
        mesh_keywords = H.slice(mesh_naming_convention)
        texture_keywords = H.slice(texture_naming_convention)
        
        naming_convention = {}
        
        i = 0
        for k in asset_keywords:
            if k in V.LM_NAMING_CONVENTION_KEYWORDS:
                naming_convention[k] = asset_name[i]
                i = i + 1

        # for i,k in enumerate(mesh_keywords):
        #     if k in V.LM_NAMING_CONVENTION_KEYWORDS:
        #         mesh_naming_convention[k] = asset_name[i]

        # for i,k in enumerate(texture_keywords):
        #     if k in V.LM_NAMING_CONVENTION_KEYWORDS:
        #         texture_naming_convention[k] = asset_name[i]

        return naming_convention

    def get_asset_name(self, meshes):
        return path.basename(path.dirname(meshes[0]))
    
    def get_asset_root(self, meshes):
        return path.dirname(meshes[0])

    @check_asset_exist
    def select_asset(self):
        bpy.data.collections[self.asset_name].select_set(True)


    @check_asset_exist    
    def select_objects(self):
        curr_asset_collection = bpy.data.collections[self.asset_name]
        bpy.ops.object.select_all(action='DESELECT')
        for o in curr_asset_collection.all_objects:
            o.select_set(True)

    
    def remove_objects(self):
        self.select_objects()

        bpy.ops.object.delete()


    @check_asset_exist
    def print_asset_objects_name(self):
        names = self.get_objects_name()
        for n in names:
            print(n)

    @check_asset_exist
    def get_objects_name(self):
        names = []
        curr_asset_collection = bpy.data.collections[self.asset_name]
        for o in curr_asset_collection.all_objects:
            names.append(o.name)
        
        return names
    @check_asset_exist
    def rename_objects(self):
        curr_asset_collection = bpy.data.collections[self.asset_name]
        separator = '.'
        for o in curr_asset_collection.all_objects:
            splited_name = o.name.split(separator)[:-1]
            name = ''
            for i,split in enumerate(splited_name):
                name = name + split
                if i < len(splited_name) - 1:
                    name = name + separator
            o.name = name

class BpyAssetFBX(BpyAsset):
    def __init__(self, context, meshes, textures):
        super(BpyAssetFBX, self).__init__(context, meshes, textures)

class TextureSet(object):
    pass