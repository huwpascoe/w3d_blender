w3d_blender
===========

Blender Westwood3D Suite

Revision A
==========

Not ready for use in projects.
You can import meshes for exploring/messing with.

Materials don't update when you edit them.
Some material data is not yet imported.
Object properties and pivots/positions are not available.
No exporting functionality.

----------------------------------------------------------------------------

"THE BEER-WARE LICENSE" (Revision 42a):
<huwpascoe@github> wrote this software. As long as you retain this notice you
can do whatever you want with this stuff. If we meet some day and you think
this stuff is worth it, you can buy me a cider in return - Huw Pascoe

----------------------------------------------------------------------------

Tiberian technologies' mod tools are recommended.
http://www.tiberiantechnologies.org/

XCC is the standard toolset for working with Westwood's archive format.
http://xhp.xwis.net/

The work of Jonathan Wilson was used as a reference of the W3D format.
http://sourceforge.net/projects/rentools/

Basic Usage
===========
Place the westwood3D folder in Blender's scripts/addons/ directory
It can be enabled under Import-Export in the addons menu.

Once enabled, the material tab gains a new panel called Westwood3D.
W3D Materials should be modified with this panel only.

Use File > Import > Westwood3D to import your w3d files.
The texture paths must be relative to the w3d file.

Meshes are placed on layer 2 if they're hidden.
VIS objects which are used by the game engine for culling polygons are placed on layer 11.

The importer will first attempt to load the original filenames, e.g. 'tex.tga',
otherwise it will try to load 'text.dds'. Blender has built in DDS support.

Shared Textures
===============
To use textures such as those in always.dat,
place them in a directory above the file called 'textures'.

example directory layout:
/my_renegade_maps
    
    /textures
        /mytex
            gdi_base.dds
    
    /mymap
        /mytex
            grn_rck2.dds
        
        mymap.w3d
    
If mymap.w3d requested gdi_base.dds, the importer would first try to load
in "./mytex/gdi_base.dds" then "../textures/mytex/gdi_base.dds".