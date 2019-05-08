import bpy
from os import path

class LM_PT_main(bpy.types.Panel):          
    bl_label = "Make Lineup"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = 'Lineup Maker'

    
    def draw(self, context):
        scn = context.scene
        assetPath = bpy.path.abspath(scn.lm_asset_path)
        layout = self.layout

        row = layout.row(align=True)
        if path.exists(assetPath):
            icon = "DOWNARROW_HLT"
        else:
            icon = "BLANK1"
        row.prop(scn, 'lm_asset_path', text = 'Asset Path', icon=icon)
        layout.operator("scene.lm_importfiles", icon='IMPORT', text="Import all assets")

class LM_PT_NamingConvention(bpy.types.Panel):
    bl_label = "Naming Convention"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Lineup Maker"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        scn = context.scene
        assetPath = bpy.path.abspath(scn.lm_asset_path)
        layout = self.layout

        col = layout.column(align=True)
        # NAMING CONVENTION SETUP
        col = layout.column(align=True)
        
        col.prop(scn, 'lm_asset_naming_convention', text = 'Asset Naming Convention')
        col.prop(scn, 'lm_mesh_naming_convention', text = 'Mesh Naming Convention')
        col.prop(scn, 'lm_texture_naming_convention', text = 'Texture Naming Convention')

class LM_PT_TextureSetSettings(bpy.types.Panel):
    bl_label = "TextureSet Settings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Lineup Maker"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        scn = context.scene
        assetPath = bpy.path.abspath(scn.lm_asset_path)
        layout = self.layout

        col = layout.column(align=True)
        col.label(text='Shader Name')
        row = col.row()
        
        rows = len(scn.lm_shaders) if len(scn.lm_shaders) > 4 else 4
        row.template_list('LM_UL_shaders', '', scn, 'lm_shaders', scn, 'lm_shader_idx', rows=rows)
        c = row.column(align=True)
        c.operator("scene.lm_move_shader", text="", icon='TRIA_UP').direction = "UP"
        c.operator("scene.lm_move_shader", text="", icon='TRIA_DOWN').direction = "DOWN"

        c.separator()
        c.operator("scene.lm_clear_shaders", text="", icon='LOOP_BACK')
        c.operator("scene.lm_remove_shader", text="", icon='X')
        c.separator()
        c.operator("scene.lm_rename_shader", text="", icon='OUTLINER_DATA_FONT')

        col.prop(scn, 'lm_shader_name')

        c.separator()

        col = layout.column(align=True)
        col.label(text='Channel Name')
        row = col.row()
        
        rows = len(scn.lm_channels) if len(scn.lm_channels) > 4 else 4
        row.template_list('LM_UL_channels', '', scn, 'lm_channels', scn, 'lm_channel_idx', rows=rows)
        c = row.column(align=True)
        c.operator("scene.lm_move_channel", text="", icon='TRIA_UP').direction = "UP"
        c.operator("scene.lm_move_channel", text="", icon='TRIA_DOWN').direction = "DOWN"

        c.separator()
        c.operator("scene.lm_clear_channels", text="", icon='LOOP_BACK')
        c.operator("scene.lm_remove_channel", text="", icon='X')
        c.separator()
        c.operator("scene.lm_rename_channel", text="", icon='OUTLINER_DATA_FONT')

        col.prop(scn, 'lm_channel_name')

        c.separator()
        col.label(text='Texture Name')
        row = col.row()
        
        rows = len(scn.lm_texture_channels) if len(scn.lm_texture_channels) > 4 else 4
        row.template_list('LM_UL_texturesets', '', scn, 'lm_texture_channels', scn, 'lm_texture_channel_idx', rows=rows)
        c = row.column(align=True)
        c.operator("scene.lm_move_texture_channel", text="", icon='TRIA_UP').direction = "UP"
        c.operator("scene.lm_move_texture_channel", text="", icon='TRIA_DOWN').direction = "DOWN"

        c.separator()
        c.operator("scene.lm_clear_texture_channels", text="", icon='LOOP_BACK')
        c.operator("scene.lm_remove_texture_channel", text="", icon='X')
        c.separator()
        c.operator("scene.lm_rename_texture_channel", text="", icon='OUTLINER_DATA_FONT')

        col.prop(scn, 'lm_texture_channel_name')