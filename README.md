# New Open Source Report: Mech Bay
Utilities for reading and writing data files for SD GUNDAM G GENERATION CROSS RAYS.

## General Thoughts

GGCR uses CriWare for managing its assets and data pipeline. It appears the game is
almost entirely data driven. There's obviously no modding support and writing tools to
edit the data will be difficult, but there are otherwise very few elements hard-coded
in the executable.

### File Formats

The LUAC Scripts are compiled Lua v5.2, 32-bit. [Unluac](https://sourceforge.net/projects/unluac/)
isn't perfect but will decompile the code well enough to understand what's going on
and clean it up. Only the simplest scripts can be recompiled without edits.
(There's also [Luadec](https://github.com/viruscamp/luadec) but I haven't had any luck
compiling it to handle this specific version of Lua.) Lua scripts are used for scripting
stages, general battle/UI behavior and to establish game constants.

Most audio is HCA. Use [VGMStream](https://github.com/losnoco/vgmstream) to process.

Images are primarily DDS (DirectDraw Surface) format. They're often stored in TXD
(Texture Dictionaries) which are just easily unpacked archives of DDS images.
[GIMP](https://www.gimp.org/) with the [DDS Plug-in](https://code.google.com/archive/p/gimp-dds/downloads)
should be helpful here.

Video files are USM format. This includes cut scenes, menu backgrounds, and crucially,
battle animations for units are actually pre-rendered video, overlaid on top of 3d
environment and enhanced with other effects.

Game data is largely contained in CDBs, DATs, ATPs, and some TBLs. There's
no schema embedded in the headers so it's largely been a case of studying the raw bytes to
work out what they match up to. MechBay is primarily concerned with parsing these.

Nearly all localization strings are stored in easily parsed string TBL files.
References to the strings appear to be index based so any additions/deletions to data
elsewhere will require edits being made to their string tables (in all languages) as well.
Some TBLs contain strings for multiple data sets. MechBay can parse these.

Some files are combined into a PKD archive. Fortunately, it's a dead simple
zero-compression format and MechBay handles the iteration used by GGCR.

UI layout uses LAB files, which I'm assuming is a Criware format of some kind. No idea.

### Editing Files

There are unexpected dependencies between files so a mod manager will have
to take that into account.

For example, to add new MS design combinations, you have to unpack MachineSpecList.pkd
and parse MachineDesignList.cdb into JSON. After making edits, you rebuild
MachineDesignList.cdb and then repack it with the other files into MachineSpecList.pkd.

To edit the stats progression of a character, it's not as simple as editing
CharacterSpecList.cdb. That only has an index to one of 70+ growth profile in
CharacterGrowthList.cdb. The profile record in that file has a list of 98 indexes (one per
level up) to a sub-table in that file that has actual values to increase each character stat.
And finally, of course, these need to be repacked back into CharacterSpecList.pkd.
This means that editing the stat increase for a single stat on a single level up for a
single characters requires non-trivial changes across three files.

The indexes are spread all over the place but don't seem to be necessarily mean anything
to the game. In other words, no hard coded magic numbers. It's a pain to recalculate these
values over multiple files but the game doesn't seem to otherwise care as long as the data
is correctly formatted.

Ideally, a mod manager will handle this behind the scenes so modders only have to
edit JSON that gets combined and recompiled with the existing data.
