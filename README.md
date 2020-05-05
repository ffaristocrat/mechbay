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
organize assets and edit JSON that gets combined with the base data.



### What to mod

In-progress catalog of the assets and data files edits required to add something to the game.

#### Characters & NPCs

Playable characters have a guid in the format of G###C#####. The first 4 characters
are the series ID the character belongs to. The next 5 identify the character in that series
and the last character identifies the variant.

Variants are generally used for playable guest units. For example, there are multiple versions of "Heero Yuy"
that are identical except for their stats and/or images. With exceptions, only the first is recruitable. The others are used for
different versions during a campaign. As such, "Heero Yuy (EW)" is *not* a variant of "Heero Yuy" since it has
an entirely different guid. As far as the game is concerned, they have as little in common as Duo and Treize.

Non-playable characters, including pilots without cutins and characters who only speak in cut-scenes,
have the same format except it's an N instead a C.

##### Data

* data/resident/CharacterSpecList.pkd/CharacterSpecList.cdb

Primary data about characters. References records in other files by index.

* data/resident/CharacterSpecList.pkd/CharacterGrowthList.cdb

Profiles for how stats increase on each level up.

* data/resident/CharacterSpecList.pkd/SkillAcquisitionPatternList.cdb

Profiles for which skills are gained as a character levels up.

* data/resident/PersonalMachineList.cdb

Which units will turn into a custom unit when piloted by a certain character. 

* data/resident/SpecProfileList.cdb

Links units to string text in SpecProfileList.tbl

* data/language/*/SpecProfileList.tbl

Profile text for each unit, including MS and characters.

* data/resident/CharacterSpecList.pkd/CharacterConversionList.cdb

Seems to change characters from one variant to another.  Not sure how/when/why it's
triggered.

##### Cut-Ins

* data/battle/cutin/general_chara/{guid}_lip.zip
* data/battle/cutin/scene_chara/f####{guid}/f####.zip
* data/battle/cutin/scene_chara/f####{guid}/f####{guid}_lip.zip
* data/battle/cutin/scene_chara/f####{guid}/f####{guid}_wiggler.zip
* data/battle/cutin/scene_chara/f####{guid}/f####{guid}.asp
* data/battle/cutin/scene_chara/f####{guid}/mask_f####.zip
* data/battle/cutin/scene_chara/f####{guid}/*

Images and animation data for battle cutins. Only used for characters. Not sure what
f#### represents. They're generally static images with smaller images of the lips to use for
speaking animation. The rest is placement, effects, etc. Not all the files
are present for every character.

* data/battle/table/cutin.tbl

Matches characters to cutin files.

##### Images

* data/images/chara_org/m/{guid}_m.txd/{guid}_m.dds

156 x 216 DDS in a TXD

* data/images/chara_org/s/{guid}_s.txd/{guid}_s.dds

156 x 88 DDS in a TXD

* data/images/chara_org/st/{guid}_st.txd

768 × 1024 DDS in a TXD of the character standing.

* data/images/chara_pick_up/{guid}_pu.txd

256 × 768 DDS in a TXD

* data/images/chara_status/{guid}_status.txd

1024 × 768 DDS in a TXD

* data/images/schips.txd/{guid}

128 × 64 DDS (extension stripped) in a TXD

* data/tmap/txds/talkChara/{guid}.txd

Images used for VN scenes. Variants are used for different poses, ids, etc. Referenced by Lua scripts.

##### Audio

* data/sound/voice/BTL/{guid}/*.hca

Voiced lines used in battle animations.

* data/sound/voice/BTL/idset.tbl
* data/sound/voice/BTL/voice_table.tbl

Matches character ids to voice data.

* data/sound/voice/BTL/text/*/text.tbl

Localized text for battle lines

* data/sound/voice/EVM/{guid}/{guid}_*.hca
* data/sound/voice/EVT/{guid}/*.hca

Voiced lines used for movies and cut-scenes.

##### Localization

* data/language/*/CharacterSpecList.tbl

Localized names for characters.

* data/tmap/stage/scoutMessage/*/ScoutMessageTable.tbl

String text for death messages.

* data/tmap/resident/scoutMessageId.dat


#### Series

Series IDs are in the format of G####. Every campaign, character, MS, WS, etc
needs to be associated with a series.

* data/images/series_logo_l/{series}_l.txd
* data/images/series_logo_s/{series}_s.txd

Banner representing a series in campaign/stage selects.

* data/images/series_logo_l/*/{series}_l.txd
* data/images/series_logo_s/*/{series}_s.txd

Language specific versions of the series logos.
 
* data/gallery/gallery.txd/{series}_gallery.dds

Banner representing a series in the gallery.

* data/gallery/*/gallery.txd/{series}_gallery.dds

Language specific versions of the normal gallery images.

* data/language/*/SeriesProfileList.tbl

Profile text about the series.

* data/resident/MiscData.pkd/SeriesList.cdb

Primary data file about series.

* data/resident/MiscData.pkd/SeriesProfileList.cdb


#### Stages

Stage_id is a 5 digit value. The first three correspond to the campaign.
The second two correspond to the stage within that campaign. This is typically
stored as a 4-byte unsigned integer.

* data/resident/SpecProfileList.cdb

* data/resident/StageList.pkd/StageList.cdb

List of stages with rewards

* data/resident/StageList.pkd/QuestList.cdb

* data/resident/StageList.pkd/GetUnitList.cdb

Score requirements for Get Units.

* data/tmap/stage/StageClearGetList.cdb

Units rewarded for clearing a stage.

* data/language/*/MiscData.tbl
* data/language/*/StageList.tbl

* data/tmap/bg/map_###.zip
* data/tmap/bg/map_###.zip/*.dds
* data/tmap/bg/map_###.zip/map_###.pmdl

Images used for the map. Background images seem to be universally 1024x1024, even if the
playable/shown area is much less. Other images may be layered above/below the bg and units.
Ie: asteroids, clouds, etc. The pmdl file appears to control how images
are layered, animated, etc.

* data/images/stage_img/l/st_###_##_l.txd
* data/images/stage_img/s/st_###_##_s.txd

Stages are broken up into 3 or 4 sections.
* 0 - VN scenes before the stage.
* 1 - VN and battle scripting for the story section.
* 2 - VN and battle scripting for the sortie section.
* 3 - Post battle VN executed at the end of the campaign.

* data/stageComment/###_##0/*/StageCommentStringTable.tbl
* data/tmap/stage/###_##0/stringTable/*/StringCommentStringTable.tbl
* data/tmap/stage/###_##1/stringTable/*/TMapStringTable.tbl
* data/tmap/stage/###_##2/stringTable/*/TMapStringTable2.tbl
* data/tmap/stage/###_##3/stringTable/*/SeriesEndingStringTable.tbl

String text referenced by index in their respective LUA scripts. 

* data/stageComment/###_##0/StageCommentVoiceTable.tbl
* data/tmap/stage/###_##1/VoiceTable.tbl
* data/tmap/stage/###_##2/VoiceTable2.tbl
* data/tmap/stage/###_##3/SeriesEndingVoiceTable.tbl

String tables of comma separated values. The first value is the name of the
voice file for a string text in a scene, if any. The rest of the values aren't understood yet.
Probably audio length and volume?

* data/stageComment/###_##0/script.luac
* data/tmap/stage/###_##1/script.luac
* data/tmap/stage/###_##2/script.luac
* data/tmap/stage/###_##3/script.luac

Only script.luac is actually called by the engine. There are a number of functions that need to
exist that are called at each various points before, during, and after a battle. I haven't cataloged
all the required functions for each scene and the utility functions (found in data/tmap/lua) that are
called.

* data/tmap/stage/###_##1/beforeBattleTalk.luac
* data/tmap/stage/###_##2/beforeBattleTalk.luac

Every stage has this broken out as a separate file but it's just imported into script.luac.

* data/tmap/stage/###_##1/miniMap.txd
* data/tmap/stage/###_##1/miniMap.txd/*.dds

Images of thumbnails of the images in data/tmap/bg/map_###.zip.

* data/tmap/stage/###_##1/stage.dat
* data/tmap/stage/###_##1/stageConditions.dat

Data about what the map tiles are, which background images they use, structure of the map
and all the units being used in this stage.


#### Battle Environments


#### Mobile Suits, Warships and other units




#### Group Dispatches

Group dispatches have a straightforward 4 digit id.

* data/images/mission_l/gd####_l.txd/gd####_l.dds

1920 × 784 DDS in a TXD of the background for a dispatch.

* data/images/mission_s/gd####_s.txd/gd####_s.dds

136 × 60 DDS in a TXD that's a thumbnail of the above.

* data/resident/MiscData.pkd/GroupSendingMissionList.cdb

Primary data for group dispatches including rewards.

* data/language/*/MiscData.tbl

String values for dispatch missions and their requirements. Shared with
series names.


### Progress

#### Read & Write - All Fields understood

* All PKD archives
** data/\*\*/\*.pkd

* All String TBL files
** data/language/\*/MiscData.tbl
** data/language/\*/StageList.tbl
** data/language/\*/CharacterSpecList.tbl
** data/language/\*/SpecProfileList.tbl
** data/stageComment/???_??0/\*/StageCommentStringTable.tbl
** data/tmap/stage/???_??0/stringTable/\*/StringCommentStringTable.tbl
** data/tmap/stage/???_??1/stringTable/\*/TMapStringTable.tbl
** data/tmap/stage/???_??2/stringTable/\*/TMapStringTable2.tbl
** data/tmap/stage/???_??3/stringTable/\*/SeriesEndingStringTable.tbl

* data/resident/CharacterConversionList.cdb
* data/resident/CharacterSpecList.pkd/CharacterGrowthList.cdb
* data/resident/MachineSpecList.pkd/MachineConversionList.cdb
* data/resident/MachineSpecList.pkd/MachineDesignList.cdb
* data/resident/MachineSpecList.pkd/MachineDevelopmentList.cdb
* data/resident/MachineSpecList.pkd/PersonalMachineList.cdb
* data/resident/StageList.pkd/GetUnitList.cdb
* data/tmap/stage/StageClearGetList.cdb


#### Read & Write but some fields not understood
* All Voice String TBL files
** data/stageComment/???_??0/StageCommentVoiceTable.tbl
** data/tmap/stage/???_??1/VoiceTable.tbl
** data/tmap/stage/???_??2/VoiceTable2.tbl
** data/tmap/stage/???_??3/SeriesEndingVoiceTable.tbl

* data/resident/CellAttributeList.pkd/BattleBgList.cdb
* data/resident/SeriesProfileList.cdb
* data/resident/MiscData.pkd/SeriesList.cdb
* data/resident/StageList.pkd/QuestList.cdb
* data/resident/SpecProfileList.cdb

* data/tmap/resident/scoutMessageId.dat
* data/tmap/resident/ActAbilityEffectList.cdb


#### In Progress
* data/tmap/resident/MapTypes.cdb
* data/tmap/resident/editBgmScoutId.dat
* data/tmap/resident/effectList.dat
* data/tmap/resident/MapWeaponList.dat
* data/tmap/resident/movieList.dat
* data/tmap/resident/powerUpList.dat

* data/resident/AbilitySpecList.cdb
* data/resident/CellAttributeList.pkd/CellAttributeList.cdb
* data/resident/CharacterSpecList.pkd/CharacterSpecList.cdb
* data/resident/CharacterSpecList.pkd/MyCharacterConfiguration.cdb
* data/resident/CharacterSpecList.pkd/SkillAcquisitionPatternList.cdb
* data/resident/MachineSpecList.pkd/MachineGrowthList.cdb
* data/resident/MachineSpecList.pkd/MachineSpecList.cdb
* data/resident/MiscData.pkd/GroupSendingMissionList.cdb
* data/resident/MiscData.pkd/TutorialList.cdb
* data/resident/WeaponSpecList.cdb


#### Not/Barely Started

* data/tmap/stage/???_??1/stage.dat
* data/tmap/stage/???_??1/stageConditions.dat

* data/resident/CreditBgmList.cdb
* data/resident/CreditList.cdb
* data/resident/DlcList.dat
* data/resident/GalleryMovieList.cdb
* data/resident/MiscData.pkd/DatabaseCaluclation.cdb
* data/resident/RangeDataList.cdb
* data/resident/SteamDlcGroupList.dat
* data/resident/TitleBgmList.cdb

* data/battle/table/animation.tbl
* data/battle/table/bomb_table.atp
* data/battle/table/cockpit_bg_table.atp
* data/battle/table/cutin_same.tbl
* data/battle/table/cutin.tbl
* data/battle/table/filter_table.atp
* data/battle/table/idset.tbl
* data/battle/table/information.tbl
* data/battle/table/weapon.tbl
