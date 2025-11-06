local L1_1
L0_0 = {}
Unit = L0_0
L0_0 = Unit
function L1_1(A0_2)
  return System.GetUnit(A0_2)
end
L0_0.GetUnit = L1_1
L0_0 = Unit
function L1_1(A0_3)
  return System.GetAllUnits(A0_3)
end
L0_0.GetAllUnits = L1_1
L0_0 = Unit
function L1_1(A0_4, A1_5)
  return System.GetUnitsByAdmiId(A0_4, A1_5)
end
L0_0.GetUnitsByAdmiId = L1_1
L0_0 = Unit
function L1_1(A0_6, A1_7)
  return System.GetUnitsByGroupName(A0_6, A1_7)
end
L0_0.GetUnitsByGroupName = L1_1
L0_0 = Unit
function L1_1(A0_8)
  return System.GetUnitsByArea(A0_8)
end
L0_0.GetUnitsByArea = L1_1
L0_0 = Unit
function L1_1(A0_9)
  local L1_10, L2_11, L3_12, L4_13, L5_14, L6_15, L7_16
  L1_10 = {}
  L2_11 = Unit
  L2_11 = L2_11.GetAllUnits
  L2_11 = L2_11(L3_12)
  for L6_15, L7_16 in L3_12(L4_13) do
    if Unit.GetArmyType(L7_16) == A0_9 and Unit.IsValidMap(L7_16) then
      table.insert(L1_10, L7_16)
    end
  end
  return L1_10
end
L0_0.GetUnitsByArmyType = L1_1
L0_0 = Unit
function L1_1(...)
  local L1_18, L2_19, L3_20, L4_21, L5_22
  L5_22 = ...
  for L3_20 = 1, L1_18(L2_19, L3_20, L4_21, L5_22, ...) do
    L4_21 = System
    L4_21 = L4_21.GetUnit
    L5_22 = select
    L5_22 = L5_22(L3_20, ...)
    L4_21 = L4_21(L5_22, L5_22(L3_20, ...))
    L5_22 = System
    L5_22 = L5_22.Appear
    L5_22 = L5_22(L4_21, UnitAppearType.Instant)
    Utility.WaitProcedure(L5_22)
  end
end
L0_0.AppearInstant = L1_1
L0_0 = Unit
function L1_1(A0_23)
  local L1_24, L2_25, L3_26, L4_27, L5_28, L6_29, L7_30, L8_31
  L1_24 = System
  L1_24 = L1_24.GetUnitsByGroupName
  L1_24 = L1_24(L2_25, L3_26)
  for L5_28, L6_29 in L2_25(L3_26) do
    L7_30 = System
    L7_30 = L7_30.GetUnit
    L8_31 = L6_29
    L7_30 = L7_30(L8_31)
    L8_31 = System
    L8_31 = L8_31.Appear
    L8_31 = L8_31(L7_30, UnitAppearType.Instant)
    Utility.WaitProcedure(L8_31)
  end
end
L0_0.AppearInstantGroup = L1_1
L0_0 = Unit
function L1_1(...)
  local L1_33, L2_34, L3_35, L4_36, L5_37
  L5_37 = ...
  for L3_35 = 1, L1_33(L2_34, L3_35, L4_36, L5_37, ...) do
    L4_36 = System
    L4_36 = L4_36.GetUnit
    L5_37 = select
    L5_37 = L5_37(L3_35, ...)
    L4_36 = L4_36(L5_37, L5_37(L3_35, ...))
    L5_37 = System
    L5_37 = L5_37.Appear
    L5_37 = L5_37(L4_36, UnitAppearType.Normal)
    Utility.WaitProcedure(L5_37)
  end
end
L0_0.Appear = L1_1
L0_0 = Unit
function L1_1(A0_38, ...)
  local L2_40, L3_41, L4_42, L5_43, L6_44
  L1_39 = 0
  L6_44 = ...
  for L5_43 = 1, L3_41(L4_42, L5_43, L6_44, ...) do
    L6_44 = System
    L6_44 = L6_44.GetUnit
    L6_44 = L6_44(select(L5_43, ...))
    L1_39 = System.Appear(L6_44, UnitAppearType.Normal)
    Utility.Wait(A0_38)
  end
  L2_40(L3_41)
end
L0_0.AppearFast = L1_1
L0_0 = Unit
function L1_1(A0_45)
  local L1_46, L2_47, L3_48, L4_49, L5_50, L6_51, L7_52, L8_53
  L1_46 = System
  L1_46 = L1_46.GetUnitsByGroupName
  L1_46 = L1_46(L2_47, L3_48)
  for L5_50, L6_51 in L2_47(L3_48) do
    L7_52 = System
    L7_52 = L7_52.GetUnit
    L8_53 = L6_51
    L7_52 = L7_52(L8_53)
    L8_53 = System
    L8_53 = L8_53.Appear
    L8_53 = L8_53(L7_52, UnitAppearType.Normal)
    Utility.WaitProcedure(L8_53)
  end
end
L0_0.AppearGroup = L1_1
L0_0 = Unit
function L1_1(...)
  local L1_55, L2_56, L3_57, L4_58, L5_59
  L5_59 = ...
  for L3_57 = 1, L1_55(L2_56, L3_57, L4_58, L5_59, ...) do
    L4_58 = System
    L4_58 = L4_58.GetUnit
    L5_59 = select
    L5_59 = L5_59(L3_57, ...)
    L4_58 = L4_58(L5_59, L5_59(L3_57, ...))
    L5_59 = Map
    L5_59 = L5_59.SetIndex
    L5_59(Unit.GetMapIndex(L4_58))
    L5_59 = System
    L5_59 = L5_59.Appear
    L5_59 = L5_59(L4_58, UnitAppearType.MoveCamera)
    Utility.WaitProcedure(L5_59)
  end
end
L0_0.AppearSet = L1_1
L0_0 = Unit
function L1_1(A0_60)
  local L1_61, L2_62, L3_63, L4_64, L5_65, L6_66, L7_67, L8_68, L9_69
  L1_61 = System
  L1_61 = L1_61.GetUnitsByGroupName
  L1_61 = L1_61(L2_62, L3_63)
  for L5_65, L6_66 in L2_62(L3_63) do
    L7_67 = System
    L7_67 = L7_67.GetUnit
    L8_68 = L6_66
    L7_67 = L7_67(L8_68)
    L8_68 = UnitAppearType
    L8_68 = L8_68.Normal
    L9_69 = Unit
    L9_69 = L9_69.IsLeader
    L9_69 = L9_69(L7_67)
    if not L9_69 then
      L9_69 = Unit
      L9_69 = L9_69.IsWs
      L9_69 = L9_69(L7_67)
      if not L9_69 then
        L9_69 = Unit
        L9_69 = L9_69.IsRaidGroupLeader
        L9_69 = L9_69(L7_67)
      end
    elseif L9_69 then
      L9_69 = Map
      L9_69 = L9_69.SetIndex
      L9_69(Unit.GetMapIndex(L7_67))
      L9_69 = UnitAppearType
      L8_68 = L9_69.MoveCamera
    end
    L9_69 = System
    L9_69 = L9_69.Appear
    L9_69 = L9_69(L7_67, L8_68)
    Utility.WaitProcedure(L9_69)
  end
end
L0_0.AppearSetGroup = L1_1
L0_0 = Unit
function L1_1(A0_70, ...)
  local L2_72, L3_73, L4_74, L5_75, L6_76
  L6_76 = ...
  for L4_74 = 1, L2_72(L3_73, L4_74, L5_75, L6_76, ...) do
    L5_75 = System
    L5_75 = L5_75.GetUnit
    L6_76 = select
    L6_76 = L6_76(L4_74, ...)
    L5_75 = L5_75(L6_76, L6_76(L4_74, ...))
    L6_76 = System
    L6_76 = L6_76.AppearWithEffectId
    L6_76 = L6_76(L5_75, UnitAppearType.Normal, A0_70)
    Utility.WaitProcedure(L6_76)
  end
end
L0_0.AppearWithEffectId = L1_1
L0_0 = Unit
function L1_1(A0_77, ...)
  local L2_79, L3_80, L4_81, L5_82, L6_83
  L6_83 = ...
  for L4_81 = 1, L2_79(L3_80, L4_81, L5_82, L6_83, ...) do
    L5_82 = System
    L5_82 = L5_82.GetUnit
    L6_83 = select
    L6_83 = L6_83(L4_81, ...)
    L5_82 = L5_82(L6_83, L6_83(L4_81, ...))
    L6_83 = Map
    L6_83 = L6_83.SetIndex
    L6_83(Unit.GetMapIndex(L5_82))
    L6_83 = System
    L6_83 = L6_83.AppearWithEffectId
    L6_83 = L6_83(L5_82, UnitAppearType.MoveCamera, A0_77)
    Utility.WaitProcedure(L6_83)
  end
end
L0_0.AppearSetWithEffectId = L1_1
L0_0 = Unit
function L1_1(A0_84, A1_85, A2_86)
  local L3_87, L4_88, L5_89, L6_90, L7_91
  L3_87 = System
  L3_87 = L3_87.GetUnit
  L4_88 = A0_84
  L3_87 = L3_87(L4_88)
  L4_88 = System
  L4_88 = L4_88.GetUnit
  L5_89 = A1_85
  L4_88 = L4_88(L5_89)
  L5_89 = Unit
  L5_89 = L5_89.GetPosition
  L6_90 = L4_88
  L5_89 = L5_89(L6_90)
  L6_90 = Unit
  L6_90 = L6_90.GetDirection
  L7_91 = L4_88
  L6_90 = L6_90(L7_91)
  L7_91 = Unit
  L7_91 = L7_91.GetRegistrationScore
  L7_91 = L7_91(L4_88)
  System.Disappear(L4_88, A2_86, false)
  Unit.AppearJump(A0_84, Map.GetIndex(), L5_89.X, L5_89.Y, L6_90, A2_86)
  Unit.SetRegistrationScore(L3_87, L7_91)
end
L0_0.AppearReplace = L1_1
L0_0 = Unit
function L1_1(A0_92, A1_93, A2_94, A3_95, A4_96, A5_97)
  local L6_98, L7_99
  L6_98 = UnitAppearType
  L6_98 = L6_98.Instant
  if A5_97 ~= L6_98 then
    L6_98 = Map
    L6_98 = L6_98.SetIndex
    L7_99 = A1_93
    L6_98(L7_99)
  end
  L6_98 = System
  L6_98 = L6_98.GetUnit
  L7_99 = A0_92
  L6_98 = L6_98(L7_99)
  L7_99 = System
  L7_99 = L7_99.AppearJump
  L7_99 = L7_99(L6_98, A1_93, A2_94, A3_95, A4_96, A5_97)
  Utility.WaitProcedure(L7_99)
end
L0_0.AppearJump = L1_1
L0_0 = Unit
function L1_1(...)
  local L1_101, L2_102, L3_103, L4_104, L5_105
  L5_105 = ...
  for L3_103 = 1, L1_101(L2_102, L3_103, L4_104, L5_105, ...) do
    L4_104 = System
    L4_104 = L4_104.GetUnit
    L5_105 = select
    L5_105 = L5_105(L3_103, ...)
    L4_104 = L4_104(L5_105, L5_105(L3_103, ...))
    L5_105 = System
    L5_105 = L5_105.Disappear
    L5_105 = L5_105(L4_104, UnitAppearType.Instant, false)
    Utility.WaitProcedure(L5_105)
  end
end
L0_0.DisappearInstant = L1_1
L0_0 = Unit
function L1_1(...)
  local L1_107, L2_108, L3_109, L4_110, L5_111
  L5_111 = ...
  for L3_109 = 1, L1_107(L2_108, L3_109, L4_110, L5_111, ...) do
    L4_110 = System
    L4_110 = L4_110.GetUnit
    L5_111 = select
    L5_111 = L5_111(L3_109, ...)
    L4_110 = L4_110(L5_111, L5_111(L3_109, ...))
    L5_111 = System
    L5_111 = L5_111.Disappear
    L5_111 = L5_111(L4_110, UnitAppearType.Normal, false)
    Utility.WaitProcedure(L5_111)
  end
end
L0_0.Disappear = L1_1
L0_0 = Unit
function L1_1(A0_112, ...)
  local L2_114, L3_115, L4_116, L5_117, L6_118
  L1_113 = 0
  L6_118 = ...
  for L5_117 = 1, L3_115(L4_116, L5_117, L6_118, ...) do
    L6_118 = System
    L6_118 = L6_118.GetUnit
    L6_118 = L6_118(select(L5_117, ...))
    L1_113 = System.Disappear(L6_118, UnitAppearType.Normal, false)
    Utility.Wait(A0_112)
  end
  L2_114(L3_115)
end
L0_0.DisappearFast = L1_1
L0_0 = Unit
function L1_1(...)
  local L1_120, L2_121, L3_122, L4_123, L5_124
  L5_124 = ...
  for L3_122 = 1, L1_120(L2_121, L3_122, L4_123, L5_124, ...) do
    L4_123 = System
    L4_123 = L4_123.GetUnit
    L5_124 = select
    L5_124 = L5_124(L3_122, ...)
    L4_123 = L4_123(L5_124, L5_124(L3_122, ...))
    L5_124 = Unit
    L5_124 = L5_124.IsAlive
    L5_124 = L5_124(L4_123)
    if L5_124 then
      L5_124 = Map
      L5_124 = L5_124.SetIndex
      L5_124(Unit.GetMapIndex(L4_123))
      L5_124 = System
      L5_124 = L5_124.Disappear
      L5_124 = L5_124(L4_123, UnitAppearType.MoveCamera, false)
      Utility.WaitProcedure(L5_124)
    end
  end
end
L0_0.DisappearSet = L1_1
L0_0 = Unit
function L1_1(A0_125, ...)
  local L2_127, L3_128, L4_129, L5_130, L6_131
  L6_131 = ...
  for L4_129 = 1, L2_127(L3_128, L4_129, L5_130, L6_131, ...) do
    L5_130 = System
    L5_130 = L5_130.GetUnit
    L6_131 = select
    L6_131 = L6_131(L4_129, ...)
    L5_130 = L5_130(L6_131, L6_131(L4_129, ...))
    L6_131 = Unit
    L6_131 = L6_131.IsAlive
    L6_131 = L6_131(L5_130)
    if L6_131 then
      L6_131 = Map
      L6_131 = L6_131.SetIndex
      L6_131(Unit.GetMapIndex(L5_130))
      L6_131 = System
      L6_131 = L6_131.DisappearWithEffectId
      L6_131 = L6_131(L5_130, A0_125)
      Utility.WaitProcedure(L6_131)
    end
  end
end
L0_0.DisappearSetWithEffectId = L1_1
L0_0 = Unit
function L1_1(...)
  local L1_133, L2_134, L3_135, L4_136, L5_137
  L5_137 = ...
  for L3_135 = 1, L1_133(L2_134, L3_135, L4_136, L5_137, ...) do
    L4_136 = System
    L4_136 = L4_136.GetUnit
    L5_137 = select
    L5_137 = L5_137(L3_135, ...)
    L4_136 = L4_136(L5_137, L5_137(L3_135, ...))
    L5_137 = Unit
    L5_137 = L5_137.IsAlive
    L5_137 = L5_137(L4_136)
    if L5_137 then
      L5_137 = Map
      L5_137 = L5_137.SetIndex
      L5_137(Unit.GetMapIndex(L4_136))
      L5_137 = System
      L5_137 = L5_137.Disappear
      L5_137 = L5_137(L4_136, UnitAppearType.MoveCamera, true)
      Utility.WaitProcedure(L5_137)
    end
  end
end
L0_0.DisappearFake = L1_1
L0_0 = Unit
function L1_1(...)
  local L1_139, L2_140, L3_141, L4_142, L5_143
  L5_143 = ...
  for L3_141 = 1, L1_139(L2_140, L3_141, L4_142, L5_143, ...) do
    L4_142 = System
    L4_142 = L4_142.GetUnit
    L5_143 = select
    L5_143 = L5_143(L3_141, ...)
    L4_142 = L4_142(L5_143, L5_143(L3_141, ...))
    L5_143 = System
    L5_143 = L5_143.Disappear
    L5_143 = L5_143(L4_142, UnitAppearType.Instant, true)
    Utility.WaitProcedure(L5_143)
  end
end
L0_0.DisappearFakeInstant = L1_1
L0_0 = Unit
function L1_1(A0_144, ...)
  local L2_146, L3_147
  L1_145 = UnitAppearType
  L1_145 = L1_145.Explosion
  L2_146 = select
  L3_147 = "#"
  L2_146 = L2_146(L3_147, ...)
  if L2_146 >= 1 then
    L2_146 = select
    L3_147 = 1
    L2_146 = L2_146(L3_147, ...)
    if L2_146 then
      L2_146 = UnitAppearType
      L1_145 = L2_146.MasterExplosion
    end
  end
  L2_146 = System
  L2_146 = L2_146.GetUnit
  L3_147 = A0_144
  L2_146 = L2_146(L3_147)
  L3_147 = Unit
  L3_147 = L3_147.IsMaster
  L3_147 = L3_147(L2_146)
  if L3_147 then
    L3_147 = UnitAppearType
    L1_145 = L3_147.MasterExplosion
  end
  L3_147 = Unit
  L3_147 = L3_147.IsAlive
  L3_147 = L3_147(L2_146)
  if L3_147 then
    L3_147 = Map
    L3_147 = L3_147.SetIndex
    L3_147(Unit.GetMapIndex(L2_146))
    L3_147 = System
    L3_147 = L3_147.Disappear
    L3_147 = L3_147(L2_146, L1_145, false, false)
    Utility.WaitProcedure(L3_147)
  end
end
L0_0.Kill = L1_1
L0_0 = Unit
function L1_1(...)
  local L1_149, L2_150, L3_151, L4_152, L5_153
  L0_148 = 0
  L5_153 = ...
  for L4_152 = 1, L2_150(L3_151, L4_152, L5_153, ...) do
    L5_153 = System
    L5_153 = L5_153.GetUnit
    L5_153 = L5_153(select(L4_152, ...))
    L0_148 = System.Disappear(L5_153, UnitAppearType.Explosion, false, true)
  end
  L1_149(L2_150)
end
L0_0.KillMulti = L1_1
L0_0 = Unit
function L1_1(A0_154, ...)
  local L2_156, L3_157, L4_158, L5_159, L6_160, L7_161, L8_162, L9_163, L10_164, L11_165, L12_166, L13_167, L14_168, L15_169
  L1_155 = 0
  L2_156 = Unit
  L2_156 = L2_156.GetDisplaySize
  L3_157 = A0_154
  L2_156 = L2_156(L3_157)
  L3_157 = false
  L4_158 = select
  L5_159 = "#"
  L15_169 = ...
  L4_158 = L4_158(L5_159, L6_160, L7_161, L8_162, L9_163, L10_164, L11_165, L12_166, L13_167, L14_168, L15_169, ...)
  if L4_158 >= 1 then
    L4_158 = select
    L5_159 = 1
    L15_169 = ...
    L4_158 = L4_158(L5_159, L6_160, L7_161, L8_162, L9_163, L10_164, L11_165, L12_166, L13_167, L14_168, L15_169, ...)
    L3_157 = L4_158
  end
  L4_158 = DisplaySizeType
  L4_158 = L4_158.LL
  if L2_156 <= L4_158 then
    L4_158 = Unit
    L4_158 = L4_158.IsMaster
    L5_159 = A0_154
    L4_158 = L4_158(L5_159)
    if L4_158 or L3_157 then
      L4_158 = SSA
      L4_158 = L4_158.CreateSSAonUnit
      L5_159 = 902
      L6_160 = A0_154
      L4_158 = L4_158(L5_159, L6_160)
      L1_155 = L4_158
    else
      L4_158 = SSA
      L4_158 = L4_158.CreateSSAonUnit
      L5_159 = 901
      L6_160 = A0_154
      L4_158 = L4_158(L5_159, L6_160)
      L1_155 = L4_158
    end
    L4_158 = Utility
    L4_158 = L4_158.Wait
    L5_159 = 0.5
    L4_158(L5_159)
    L4_158 = Unit
    L4_158 = L4_158.DisappearInstant
    L5_159 = A0_154
    L4_158(L5_159)
  else
    L4_158 = 3
    L5_159 = {}
    L5_159.Left = -1
    L5_159.Top = -1
    L5_159.Right = 1
    L5_159.Bottom = 1
    L6_160 = Unit
    L6_160 = L6_160.GetPosition
    L6_160 = L6_160(L7_161)
    if L2_156 == L7_161 then
      L4_158 = 5
      L5_159 = L7_161
    end
    for L10_164 = 1, L4_158 do
      L11_165 = math
      L11_165 = L11_165.random
      L11_165 = L11_165()
      L12_166 = L5_159.Right
      L13_167 = L5_159.Left
      L12_166 = L12_166 - L13_167
      L11_165 = L11_165 * L12_166
      L12_166 = L5_159.Left
      L11_165 = L11_165 + L12_166
      L11_165 = L11_165 + 0.5
      L12_166 = math
      L12_166 = L12_166.random
      L12_166 = L12_166()
      L13_167 = L5_159.Bottom
      L14_168 = L5_159.Top
      L13_167 = L13_167 - L14_168
      L12_166 = L12_166 * L13_167
      L13_167 = L5_159.Top
      L12_166 = L12_166 + L13_167
      L12_166 = L12_166 + 0.5
      L13_167 = L6_160.X
      L13_167 = L11_165 + L13_167
      L14_168 = Grid
      L14_168 = L14_168.Size
      L14_168 = L14_168()
      L13_167 = L13_167 * L14_168
      L14_168 = L6_160.Y
      L14_168 = L12_166 + L14_168
      L15_169 = Grid
      L15_169 = L15_169.Size
      L15_169 = L15_169()
      L14_168 = L14_168 * L15_169
      L15_169 = SSA
      L15_169 = L15_169.CreateSSA
      L15_169 = L15_169(901)
      SSA.Position(L15_169, L13_167, L14_168)
      Utility.Wait(0.2)
    end
    if L7_161 or L3_157 then
      L1_155 = L7_161
      L7_161(L8_162)
    else
      L1_155 = L7_161
      L7_161(L8_162)
    end
    L7_161(L8_162)
  end
  return L1_155
end
L0_0.BombEffect = L1_1
L0_0 = Unit
function L1_1(A0_170)
  local L1_171, L2_172
  L1_171 = System
  L1_171 = L1_171.GetUnit
  L2_172 = A0_170
  L1_171 = L1_171(L2_172)
  L2_172 = Map
  L2_172 = L2_172.SetIndex
  L2_172(Unit.GetMapIndex(L1_171))
  L2_172 = System
  L2_172 = L2_172.KillUnit
  L2_172 = L2_172(L1_171, true)
  Utility.WaitProcedure(L2_172)
end
L0_0.BiriBiriKill = L1_1
L0_0 = Unit
function L1_1(A0_173)
  local L1_174
  L1_174 = System
  L1_174 = L1_174.GetUnit
  L1_174 = L1_174(A0_173)
  return System.GetParameter(L1_174)
end
L0_0.GetParameter = L1_1
L0_0 = Unit
function L1_1(A0_175, A1_176)
  local L2_177
  L2_177 = System
  L2_177 = L2_177.GetUnit
  L2_177 = L2_177(A0_175)
  System.SetParameter(L2_177, A1_176)
end
L0_0.SetParameter = L1_1
L0_0 = Unit
function L1_1(A0_178, ...)
  local L2_180
  L1_179 = System
  L1_179 = L1_179.GetUnit
  L2_180 = A0_178
  L1_179 = L1_179(L2_180)
  L2_180 = CharaterCrewType
  L2_180 = L2_180.Captain
  if select("#", ...) >= 1 then
    L2_180 = select(1, ...)
  end
  return System.GetCharacterParameter(L1_179, L2_180)
end
L0_0.GetCharacterParameter = L1_1
L0_0 = Unit
function L1_1(A0_181, A1_182, ...)
  local L3_184
  L2_183 = System
  L2_183 = L2_183.GetUnit
  L3_184 = A0_181
  L2_183 = L2_183(L3_184)
  L3_184 = CharaterCrewType
  L3_184 = L3_184.Captain
  if select("#", ...) >= 1 then
    L3_184 = select(1, ...)
  end
  System.SetCharacterParameter(L2_183, L3_184, A1_182)
end
L0_0.SetCharacterParameter = L1_1
L0_0 = Unit
function L1_1(A0_185, A1_186, A2_187)
  local L3_188
  L3_188 = System
  L3_188 = L3_188.GetUnit
  L3_188 = L3_188(A0_185)
  System.SetOptionParts(L3_188, A1_186, A2_187)
end
L0_0.SetOptionParts = L1_1
L0_0 = Unit
function L1_1(A0_189, A1_190, A2_191)
  local L3_192
  L3_192 = System
  L3_192 = L3_192.GetUnit
  L3_192 = L3_192(A0_189)
  while not Unit.IsReadyKomaAnimation(L3_192) and Unit.IsAlive(L3_192) do
    Utility.BreakScript()
  end
  System.SetKomaAnimation(L3_192, A1_190, A2_191)
  while not Unit.IsReadyKomaAnimation(L3_192) and Unit.IsAlive(L3_192) do
    Utility.BreakScript()
  end
end
L0_0.SetAnimation = L1_1
L0_0 = Unit
function L1_1(A0_193)
  local L1_194
  L1_194 = System
  L1_194 = L1_194.GetUnit
  L1_194 = L1_194(A0_193)
  while not System.RemoveLoopPointKomaAnimation(L1_194) do
    Utility.BreakScript()
  end
end
L0_0.RemoveLoopPoint = L1_1
L0_0 = Unit
function L1_1(A0_195)
  local L1_196
  L1_196 = System
  L1_196 = L1_196.GetUnit
  L1_196 = L1_196(A0_195)
  return System.ShowWarningHp(L1_196)
end
L0_0.ShowWarningHp = L1_1
L0_0 = Unit
function L1_1(A0_197)
  local L1_198
  L1_198 = System
  L1_198 = L1_198.GetUnit
  L1_198 = L1_198(A0_197)
  return System.GetUnitNumber(L1_198, 1)
end
L0_0.GetDirection = L1_1
L0_0 = Unit
function L1_1(A0_199, A1_200)
  local L2_201
  L2_201 = System
  L2_201 = L2_201.GetUnit
  L2_201 = L2_201(A0_199)
  System.SetUnitNumber(L2_201, 1, A1_200)
end
L0_0.SetDirection = L1_1
L0_0 = Unit
function L1_1(A0_202)
  local L1_203
  L1_203 = System
  L1_203 = L1_203.GetUnit
  L1_203 = L1_203(A0_202)
  return System.GetUnitNumber(L1_203, 3)
end
L0_0.GetRegistrationScore = L1_1
L0_0 = Unit
function L1_1(A0_204, A1_205)
  local L2_206
  L2_206 = System
  L2_206 = L2_206.GetUnit
  L2_206 = L2_206(A0_204)
  System.SetUnitNumber(L2_206, 3, A1_205)
end
L0_0.SetRegistrationScore = L1_1
L0_0 = Unit
function L1_1(A0_207)
  local L1_208
  L1_208 = System
  L1_208 = L1_208.GetUnit
  L1_208 = L1_208(A0_207)
  return System.GetUnitPosition(L1_208)
end
L0_0.GetPosition = L1_1
L0_0 = Unit
function L1_1(A0_209)
  local L1_210
  L1_210 = System
  L1_210 = L1_210.GetUnit
  L1_210 = L1_210(A0_209)
  return System.GetUnitToolPosition(L1_210)
end
L0_0.GetToolPosition = L1_1
L0_0 = Unit
function L1_1(A0_211)
  local L1_212
  L1_212 = System
  L1_212 = L1_212.GetUnit
  L1_212 = L1_212(A0_211)
  return System.GetUnitPositionBeforeExplosion(L1_212)
end
L0_0.GetPositionBeforeExplosion = L1_1
L0_0 = Unit
function L1_1(A0_213)
  local L1_214
  L1_214 = System
  L1_214 = L1_214.GetUnit
  L1_214 = L1_214(A0_213)
  return System.GetUnitName(L1_214)
end
L0_0.GetName = L1_1
L0_0 = Unit
function L1_1(A0_215)
  local L1_216
  L1_216 = System
  L1_216 = L1_216.GetUnit
  L1_216 = L1_216(A0_215)
  return System.GetMachineId(L1_216)
end
L0_0.GetMachineId = L1_1
L0_0 = Unit
function L1_1(A0_217)
  local L1_218
  L1_218 = System
  L1_218 = L1_218.GetUnit
  L1_218 = L1_218(A0_217)
  return System.GetCharacterId(L1_218)
end
L0_0.GetCharacterId = L1_1
L0_0 = Unit
function L1_1(A0_219)
  local L1_220
  L1_220 = System
  L1_220 = L1_220.GetUnit
  L1_220 = L1_220(A0_219)
  return System.GetUnitNumber(L1_220, 0)
end
L0_0.GetControlId = L1_1
L0_0 = Unit
function L1_1(A0_221, A1_222, A2_223, A3_224, A4_225, A5_226, A6_227, ...)
  local L8_229, L9_230
  L7_228 = System
  L7_228 = L7_228.GetUnit
  L8_229 = A0_221
  L7_228 = L7_228(L8_229)
  L8_229 = Map
  L8_229 = L8_229.SetIndex
  L9_230 = Unit
  L9_230 = L9_230.GetMapIndex
  L9_230 = L9_230(L7_228)
  L8_229(L9_230, L9_230(L7_228))
  L8_229 = false
  L9_230 = select
  L9_230 = L9_230("#", ...)
  if L9_230 >= 1 then
    L9_230 = select
    L9_230 = L9_230(1, ...)
    L8_229 = L9_230
  end
  if A6_227 then
    L9_230 = Unit
    L9_230 = L9_230.GetPosition
    L9_230 = L9_230(A0_221)
    Cursor.SetPosition(L9_230.X, L9_230.Y, 0, false, true)
    Cursor.SetPosition(A1_222, A2_223, math.sqrt((L9_230.X - A1_222) ^ 2 + (L9_230.Y - A2_223) ^ 2) / ((math.abs(L9_230.X - A1_222) + math.abs(L9_230.Y - A2_223)) / A3_224 * 0.1), true, false)
  end
  L9_230 = System
  L9_230 = L9_230.MoveUnit
  L9_230 = L9_230(L7_228, A1_222, A2_223, A3_224, A4_225, A5_226, L8_229)
  Utility.WaitProcedure(L9_230)
end
L0_0.Move = L1_1
L0_0 = Unit
function L1_1(A0_231, A1_232)
  local L2_233, L3_234, L4_235, L5_236, L6_237, L7_238, L8_239, L9_240, L10_241, L11_242, L12_243, L13_244
  L2_233 = Map
  L2_233 = L2_233.GetUnitsByMapIndex
  L2_233 = L2_233(L3_234, L4_235)
  for L6_237, L7_238 in L3_234(L4_235) do
    L8_239 = Unit
    L8_239 = L8_239.GetPosition
    L9_240 = L7_238
    L8_239 = L8_239(L9_240)
    L9_240 = Unit
    L9_240 = L9_240.GetDirection
    L10_241 = L7_238
    L9_240 = L9_240(L10_241)
    L10_241 = Unit
    L10_241 = L10_241.GetMp
    L11_242 = L7_238
    L10_241 = L10_241(L11_242)
    L11_242 = Unit
    L11_242 = L11_242.GetTension
    L12_243 = L7_238
    L11_242 = L11_242(L12_243)
    L12_243 = System
    L12_243 = L12_243.DisappearWithoutClearSKill
    L13_244 = L7_238
    L12_243 = L12_243(L13_244, UnitAppearType.Instant)
    L13_244 = Utility
    L13_244 = L13_244.WaitProcedure
    L13_244(L12_243)
    L13_244 = Unit
    L13_244 = L13_244.AppearJump
    L13_244 = L13_244(L7_238, A1_232, L8_239.X, L8_239.Y, L9_240, UnitAppearType.Instant)
    Utility.WaitProcedure(L13_244)
    Unit.SetMp(L7_238, L10_241)
    if L11_242 == TensionType.SuperBlow then
      Unit.SetSuperBlowTension(L7_238, true)
    end
  end
end
L0_0.MoveMapToMap = L1_1
L0_0 = Unit
function L1_1(A0_245, A1_246)
  local L2_247
  L2_247 = System
  L2_247 = L2_247.GetUnit
  L2_247 = L2_247(A0_245)
  return System.FindAroundUnit(L2_247, A1_246)
end
L0_0.FindAroundUnit = L1_1
L0_0 = Unit
function L1_1(A0_248)
  local L1_249, L2_250
  L1_249 = System
  L1_249 = L1_249.GetUnit
  L2_250 = A0_248
  L1_249 = L1_249(L2_250)
  L2_250 = Cursor
  L2_250 = L2_250.MoveToUnit
  L2_250(L1_249, 0, true, true)
  L2_250 = System
  L2_250 = L2_250.ChangeExam
  L2_250 = L2_250(L1_249)
  Utility.WaitProcedure(L2_250)
end
L0_0.ChangeExam = L1_1
L0_0 = Unit
function L1_1(A0_251, A1_252)
  local L2_253, L3_254
  L2_253 = System
  L2_253 = L2_253.GetUnit
  L3_254 = A0_251
  L2_253 = L2_253(L3_254)
  L3_254 = System
  L3_254 = L3_254.TransformMachine
  L3_254 = L3_254(L2_253, A1_252)
  Utility.WaitProcedure(L3_254)
end
L0_0.TransformMachine = L1_1
L0_0 = Unit
function L1_1()
  return System.GetRandomPlayerUnit()
end
L0_0.GetRandomPlayerUnit = L1_1
L0_0 = Unit
function L1_1(A0_255, A1_256, A2_257)
  local L3_258
  L3_258 = System
  L3_258 = L3_258.GetUnit
  L3_258 = L3_258(A0_255)
  System.ForbidWeapon(L3_258, A1_256, A2_257)
end
L0_0.ForbidWeapon = L1_1
L0_0 = Unit
function L1_1(A0_259, A1_260, A2_261)
  local L3_262
  L3_262 = System
  L3_262 = L3_262.GetUnit
  L3_262 = L3_262(A0_259)
  System.ForbidAbility(L3_262, A1_260, A2_261)
end
L0_0.ForbidAbility = L1_1
L0_0 = Unit
function L1_1(...)
  local L1_264, L2_265, L3_266, L4_267, L5_268
  L0_263 = true
  L5_268 = ...
  for L4_267 = 1, L2_265(L3_266, L4_267, L5_268, ...) do
    L5_268 = System
    L5_268 = L5_268.GetUnit
    L5_268 = L5_268(select(L4_267, ...))
    L0_263 = L0_263 and System.GetUnitFlag(L5_268, 0)
  end
  return L0_263
end
L0_0.IsAlive = L1_1
L0_0 = Unit
function L1_1(A0_269)
  local L1_270
  L1_270 = System
  L1_270 = L1_270.GetUnit
  L1_270 = L1_270(A0_269)
  return System.GetUnitFlag(L1_270, 1)
end
L0_0.IsWs = L1_1
L0_0 = Unit
function L1_1(A0_271)
  local L1_272
  L1_272 = System
  L1_272 = L1_272.GetUnit
  L1_272 = L1_272(A0_271)
  return System.GetUnitFlag(L1_272, 2)
end
L0_0.IsLeader = L1_1
L0_0 = Unit
function L1_1(A0_273)
  local L1_274
  L1_274 = System
  L1_274 = L1_274.GetUnit
  L1_274 = L1_274(A0_273)
  return System.GetUnitFlag(L1_274, 3)
end
L0_0.HasDeadEvent = L1_1
L0_0 = Unit
function L1_1(A0_275)
  local L1_276
  L1_276 = System
  L1_276 = L1_276.GetUnit
  L1_276 = L1_276(A0_275)
  return System.GetUnitFlag(L1_276, 4)
end
L0_0.IsPlayer = L1_1
L0_0 = Unit
function L1_1(A0_277)
  local L1_278
  L1_278 = System
  L1_278 = L1_278.GetUnit
  L1_278 = L1_278(A0_277)
  return System.GetUnitFlag(L1_278, 5)
end
L0_0.IsDoneWarningHp = L1_1
L0_0 = Unit
function L1_1(A0_279)
  local L1_280
  L1_280 = System
  L1_280 = L1_280.GetUnit
  L1_280 = L1_280(A0_279)
  return System.GetUnitFlag(L1_280, 6)
end
L0_0.HasStageWarningHp = L1_1
L0_0 = Unit
function L1_1(A0_281)
  local L1_282
  L1_282 = System
  L1_282 = L1_282.GetUnit
  L1_282 = L1_282(A0_281)
  return System.GetUnitFlag(L1_282, 7)
end
L0_0.IsInWarShip = L1_1
L0_0 = Unit
function L1_1(A0_283)
  local L1_284
  L1_284 = System
  L1_284 = L1_284.GetUnit
  L1_284 = L1_284(A0_283)
  return System.GetUnitFlag(L1_284, 8)
end
L0_0.GetFinishedAction = L1_1
L0_0 = Unit
function L1_1(A0_285, A1_286)
  local L2_287
  L2_287 = System
  L2_287 = L2_287.GetUnit
  L2_287 = L2_287(A0_285)
  System.SetUnitFlag(L2_287, 8, A1_286)
end
L0_0.SetFinishedAction = L1_1
L0_0 = Unit
function L1_1(A0_288)
  local L1_289
  L1_289 = System
  L1_289 = L1_289.GetUnit
  L1_289 = L1_289(A0_288)
  return System.GetUnitFlag(L1_289, 9)
end
L0_0.IsRaisedWhiteFlag = L1_1
L0_0 = Unit
function L1_1(A0_290)
  local L1_291
  L1_291 = System
  L1_291 = L1_291.GetUnit
  L1_291 = L1_291(A0_290)
  return System.GetUnitNumber(L1_291, 2)
end
L0_0.GetMapIndex = L1_1
L0_0 = Unit
function L1_1(A0_292)
  local L1_293
  L1_293 = System
  L1_293 = L1_293.GetUnit
  L1_293 = L1_293(A0_292)
  return System.GetUnitNumber(L1_293, 4)
end
L0_0.GetBgmNo = L1_1
L0_0 = Unit
function L1_1(A0_294, A1_295)
  local L2_296
  L2_296 = System
  L2_296 = L2_296.GetUnit
  L2_296 = L2_296(A0_294)
  System.SetUnitNumber(L2_296, 5, A1_295)
end
L0_0.SetCriticalRate = L1_1
L0_0 = Unit
function L1_1(A0_297, A1_298)
  local L2_299
  L2_299 = System
  L2_299 = L2_299.GetUnit
  L2_299 = L2_299(A0_297)
  System.SetUnitNumber(L2_299, 6, A1_298)
end
L0_0.SetDetectRange = L1_1
L0_0 = Unit
function L1_1(A0_300)
  local L1_301
  L1_301 = System
  L1_301 = L1_301.GetUnit
  L1_301 = L1_301(A0_300)
  return System.GetUnitNumber(L1_301, 7)
end
L0_0.GetTension = L1_1
L0_0 = Unit
function L1_1(A0_302, A1_303)
  local L2_304
  L2_304 = System
  L2_304 = L2_304.GetUnit
  L2_304 = L2_304(A0_302)
  System.SetUnitNumber(L2_304, 7, A1_303)
end
L0_0.SetTension = L1_1
L0_0 = Unit
function L1_1(A0_305, A1_306)
  local L2_307
  L2_307 = System
  L2_307 = L2_307.GetUnit
  L2_307 = L2_307(A0_305)
  System.SetUnitFlag(L2_307, 10, A1_306)
end
L0_0.SetForbidAct = L1_1
L0_0 = Unit
function L1_1(A0_308)
  local L1_309
  L1_309 = System
  L1_309 = L1_309.GetUnit
  L1_309 = L1_309(A0_308)
  return System.GetUnitNumber(L1_309, 9)
end
L0_0.GetHp = L1_1
L0_0 = Unit
function L1_1(A0_310, A1_311)
  local L2_312
  L2_312 = System
  L2_312 = L2_312.GetUnit
  L2_312 = L2_312(A0_310)
  System.SetUnitNumber(L2_312, 9, A1_311)
end
L0_0.SetHp = L1_1
L0_0 = Unit
function L1_1(A0_313)
  local L1_314
  L1_314 = System
  L1_314 = L1_314.GetUnit
  L1_314 = L1_314(A0_313)
  return System.GetUnitNumber(L1_314, 10)
end
L0_0.GetEn = L1_1
L0_0 = Unit
function L1_1(A0_315, A1_316)
  local L2_317
  L2_317 = System
  L2_317 = L2_317.GetUnit
  L2_317 = L2_317(A0_315)
  System.SetUnitNumber(L2_317, 10, A1_316)
end
L0_0.SetEn = L1_1
L0_0 = Unit
function L1_1(A0_318)
  local L1_319
  L1_319 = System
  L1_319 = L1_319.GetUnit
  L1_319 = L1_319(A0_318)
  return System.GetUnitNumber(L1_319, 12)
end
L0_0.GetMp = L1_1
L0_0 = Unit
function L1_1(A0_320, A1_321)
  local L2_322
  L2_322 = System
  L2_322 = L2_322.GetUnit
  L2_322 = L2_322(A0_320)
  System.SetUnitNumber(L2_322, 12, A1_321)
end
L0_0.SetMp = L1_1
L0_0 = Unit
function L1_1(A0_323)
  local L1_324
  L1_324 = System
  L1_324 = L1_324.GetUnit
  L1_324 = L1_324(A0_323)
  if System.GetUnitNumber(L1_324, 8) < 3 then
  else
  end
  return 0 - 3
end
L0_0.GetDisplaySize = L1_1
L0_0 = Unit
function L1_1(A0_325)
  local L1_326
  L1_326 = System
  L1_326 = L1_326.GetUnit
  L1_326 = L1_326(A0_325)
  return System.GetOccupiedRange(L1_326)
end
L0_0.GetOccupiedRange = L1_1
L0_0 = Unit
function L1_1(A0_327, A1_328, A2_329, A3_330)
  local L4_331
  L4_331 = System
  L4_331 = L4_331.GetUnit
  L4_331 = L4_331(A0_327)
  System.SetAttackTarget(L4_331, A1_328, A2_329, A3_330)
end
L0_0.SetAttackTarget = L1_1
L0_0 = Unit
function L1_1(A0_332, A1_333, A2_334, A3_335)
  local L4_336
  L4_336 = System
  L4_336 = L4_336.GetUnit
  L4_336 = L4_336(A0_332)
  System.SetNonAttackTarget(L4_336, A1_333, A2_334, A3_335)
end
L0_0.SetNonAttackTarget = L1_1
L0_0 = Unit
function L1_1(A0_337, A1_338, A2_339, A3_340, A4_341)
  local L5_342
  L5_342 = System
  L5_342 = L5_342.GetUnit
  L5_342 = L5_342(A0_337)
  System.SetNoMoveSetting(L5_342, A1_338, A2_339, A3_340, A4_341)
end
L0_0.SetNoMoveSetting = L1_1
L0_0 = Unit
function L1_1(A0_343, A1_344)
  local L2_345
  L2_345 = System
  L2_345 = L2_345.GetUnit
  L2_345 = L2_345(A0_343)
  System.SetLoopSetting(L2_345, A1_344)
end
L0_0.SetLoopSetting = L1_1
L0_0 = Unit
function L1_1(A0_346, A1_347)
  local L2_348
  L2_348 = System
  L2_348 = L2_348.GetUnit
  L2_348 = L2_348(A0_346)
  System.SetLoopCountSetting(L2_348, A1_347)
end
L0_0.SetLoopCountSetting = L1_1
L0_0 = Unit
function L1_1(A0_349, A1_350, A2_351, A3_352, A4_353)
  local L5_354
  L5_354 = System
  L5_354 = L5_354.GetUnit
  L5_354 = L5_354(A0_349)
  System.SetMovePositionSetting(L5_354, A1_350, A2_351, A3_352, A4_353)
end
L0_0.SetMovePositionSetting = L1_1
L0_0 = Unit
function L1_1(A0_355, A1_356, A2_357)
  local L3_358
  L3_358 = System
  L3_358 = L3_358.GetUnit
  L3_358 = L3_358(A0_355)
  System.SetFollowSetting(L3_358, A1_356, A2_357)
end
L0_0.SetFollowSetting = L1_1
L0_0 = Unit
function L1_1(A0_359, A1_360, A2_361)
  local L3_362
  L3_362 = System
  L3_362 = L3_362.GetUnit
  L3_362 = L3_362(A0_359)
  System.SetLandAptitude(L3_362, A1_360, A2_361)
end
L0_0.SetLandAptitude = L1_1
L0_0 = Unit
function L1_1(A0_363, A1_364, A2_365, A3_366)
  local L4_367
  L4_367 = System
  L4_367 = L4_367.GetUnit
  L4_367 = L4_367(A0_363)
  System.SetWeaponParameter(L4_367, A1_364, A2_365, A3_366)
end
L0_0.SetWeaponParameter = L1_1
L0_0 = Unit
function L1_1(A0_368, A1_369, A2_370)
  local L3_371
  L3_371 = System
  L3_371 = L3_371.GetUnit
  L3_371 = L3_371(A0_368)
  System.SetAllWeaponPower(L3_371, A1_369, A2_370)
end
L0_0.SetAllWeaponPower = L1_1
L0_0 = Unit
function L1_1(A0_372)
  local L1_373
  L1_373 = System
  L1_373 = L1_373.GetUnit
  L1_373 = L1_373(A0_372)
  return System.GetUnitFlag(L1_373, 11)
end
L0_0.IsSfs = L1_1
L0_0 = Unit
function L1_1(A0_374, A1_375)
  local L2_376
  L2_376 = System
  L2_376 = L2_376.GetUnit
  L2_376 = L2_376(A0_374)
  System.SetUnitFlag(L2_376, 12, A1_375)
end
L0_0.SetVisible = L1_1
L0_0 = Unit
function L1_1(A0_377, A1_378)
  local L2_379
  L2_379 = System
  L2_379 = L2_379.GetUnit
  L2_379 = L2_379(A0_377)
  System.SetUnitFlag(L2_379, 13, A1_378)
end
L0_0.SetPiriPiri = L1_1
L0_0 = Unit
function L1_1(A0_380)
  local L1_381
  L1_381 = System
  L1_381 = L1_381.GetUnit
  L1_381 = L1_381(A0_380)
  return System.GetUnitFlag(L1_381, 14)
end
L0_0.DoneAnimation = L1_1
L0_0 = Unit
function L1_1(A0_382, A1_383)
  local L2_384
  L2_384 = System
  L2_384 = L2_384.GetUnit
  L2_384 = L2_384(A0_382)
  System.SetUnitFlag(L2_384, 15, A1_383)
end
L0_0.SetUnitShake = L1_1
L0_0 = Unit
function L1_1(A0_385)
  local L1_386
  L1_386 = System
  L1_386 = L1_386.GetUnit
  L1_386 = L1_386(A0_385)
  return System.GetUnitNumber(L1_386, 11)
end
L0_0.GetArmyType = L1_1
L0_0 = Unit
function L1_1(A0_387)
  local L1_388
  L1_388 = System
  L1_388 = L1_388.GetUnit
  L1_388 = L1_388(A0_387)
  return System.GetUnitFlag(L1_388, 16)
end
L0_0.IsMaster = L1_1
L0_0 = Unit
function L1_1(A0_389, A1_390, ...)
  local L3_392
  L2_391 = System
  L2_391 = L2_391.GetUnit
  L3_392 = A0_389
  L2_391 = L2_391(L3_392)
  L3_392 = false
  if select("#", ...) >= 1 then
    L3_392 = select(1, ...)
  end
  if L3_392 and not Utility.IsEventSkip() then
    proc = System.FloatingEffect(L2_391, A1_390)
    Utility.WaitProcedure(proc)
  else
    System.SetUnitFlag(L2_391, 17, A1_390)
  end
end
L0_0.SetFloating = L1_1
L0_0 = Unit
function L1_1(A0_393, A1_394)
  local L2_395
  L2_395 = System
  L2_395 = L2_395.GetUnit
  L2_395 = L2_395(A0_393)
  System.TurnAroundUnit(L2_395, A1_394)
  while Unit.IsTurnAround(L2_395) do
    Utility.BreakScript()
  end
end
L0_0.TurnAroundUnit = L1_1
L0_0 = Unit
function L1_1(A0_396, A1_397)
  local L2_398
  L2_398 = System
  L2_398 = L2_398.GetUnit
  L2_398 = L2_398(A0_396)
  System.SetUnitFlag(L2_398, 18, A1_397)
end
L0_0.SetForbidMove = L1_1
L0_0 = Unit
function L1_1(A0_399)
  local L1_400
  L1_400 = System
  L1_400 = L1_400.GetUnit
  L1_400 = L1_400(A0_399)
  return System.GetUnitFlag(L1_400, 19)
end
L0_0.IsAppeared = L1_1
L0_0 = Unit
function L1_1(A0_401)
  local L1_402
  L1_402 = System
  L1_402 = L1_402.GetUnit
  L1_402 = L1_402(A0_401)
  return System.GetUnitFlag(L1_402, 20)
end
L0_0.IsChanceStep = L1_1
L0_0 = Unit
function L1_1(A0_403)
  local L1_404
  L1_404 = System
  L1_404 = L1_404.GetUnit
  L1_404 = L1_404(A0_403)
  return System.GetUnitNumber(L1_404, 13)
end
L0_0.GetChanceStep = L1_1
L0_0 = Unit
function L1_1(A0_405, A1_406)
  local L2_407
  L2_407 = System
  L2_407 = L2_407.GetUnit
  L2_407 = L2_407(A0_405)
  return System.SetUnitNumber(L2_407, 13, A1_406)
end
L0_0.SetChanceStep = L1_1
L0_0 = Unit
function L1_1(A0_408)
  local L1_409
  L1_409 = System
  L1_409 = L1_409.GetUnit
  L1_409 = L1_409(A0_408)
  return System.GetUnitNumber(L1_409, 14)
end
L0_0.GetWarningHpPercent = L1_1
L0_0 = Unit
function L1_1(A0_410, A1_411)
  local L2_412
  L2_412 = System
  L2_412 = L2_412.GetUnit
  L2_412 = L2_412(A0_410)
  return System.SetUnitNumber(L2_412, 14, A1_411)
end
L0_0.SetWarningHpPercent = L1_1
L0_0 = Unit
function L1_1(A0_413, A1_414)
  local L2_415
  L2_415 = System
  L2_415 = L2_415.GetUnit
  L2_415 = L2_415(A0_413)
  System.SetUnitFlag(L2_415, 21, A1_414)
end
L0_0.SetHighPriority = L1_1
L0_0 = Unit
function L1_1(A0_416)
  local L1_417
  L1_417 = System
  L1_417 = L1_417.GetUnit
  L1_417 = L1_417(A0_416)
  return System.GetUnitFlag(L1_417, 22)
end
L0_0.IsReadyKomaAnimation = L1_1
L0_0 = Unit
function L1_1(A0_418)
  local L1_419
  L1_419 = System
  L1_419 = L1_419.GetUnit
  L1_419 = L1_419(A0_418)
  return System.GetUnitFlag(L1_419, 23)
end
L0_0.IsImportant = L1_1
L0_0 = Unit
function L1_1(A0_420)
  local L1_421
  L1_421 = System
  L1_421 = L1_421.GetUnit
  L1_421 = L1_421(A0_420)
  return System.GetUnitFlag(L1_421, 24)
end
L0_0.IsValidMap = L1_1
L0_0 = Unit
function L1_1(A0_422)
  local L1_423
  L1_423 = System
  L1_423 = L1_423.GetUnit
  L1_423 = L1_423(A0_422)
  return System.GetUnitFlag(L1_423, 25)
end
L0_0.IsRaidGroup = L1_1
L0_0 = Unit
function L1_1(A0_424, A1_425)
  local L2_426
  L2_426 = System
  L2_426 = L2_426.GetUnit
  L2_426 = L2_426(A0_424)
  return System.SetUnitFlag(L2_426, 25, A1_425)
end
L0_0.SetRaidGroup = L1_1
L0_0 = Unit
function L1_1(A0_427)
  local L1_428
  L1_428 = System
  L1_428 = L1_428.GetUnit
  L1_428 = L1_428(A0_427)
  return System.GetUnitFlag(L1_428, 26)
end
L0_0.IsRaidGroupLeader = L1_1
L0_0 = Unit
function L1_1(A0_429)
  local L1_430
  L1_430 = System
  L1_430 = L1_430.GetUnit
  L1_430 = L1_430(A0_429)
  return System.GetUnitFlag(L1_430, 27)
end
L0_0.IsTurnAround = L1_1
L0_0 = Unit
function L1_1(A0_431, A1_432)
  local L2_433
  L2_433 = System
  L2_433 = L2_433.GetUnit
  L2_433 = L2_433(A0_431)
  System.SetUnitFlag(L2_433, 29, A1_432)
end
L0_0.SetForbidAttack = L1_1
L0_0 = Unit
function L1_1(A0_434, A1_435)
  local L2_436
  L2_436 = System
  L2_436 = L2_436.GetUnit
  L2_436 = L2_436(A0_434)
  System.SetUnitFlag(L2_436, 30, A1_435)
end
L0_0.SetForbidTurn = L1_1
L0_0 = Unit
function L1_1(A0_437, A1_438)
  local L2_439
  L2_439 = System
  L2_439 = L2_439.GetUnit
  L2_439 = L2_439(A0_437)
  System.SetUnitFlag(L2_439, 31, A1_438)
end
L0_0.SetPhaseShiftEnable = L1_1
L0_0 = Unit
function L1_1(A0_440)
  local L1_441
  L1_441 = System
  L1_441 = L1_441.GetUnit
  L1_441 = L1_441(A0_440)
  return System.GetUnitFlag(L1_441, 31)
end
L0_0.GetPhaseShiftEnable = L1_1
L0_0 = Unit
function L1_1(A0_442, A1_443)
  local L2_444
  L2_444 = System
  L2_444 = L2_444.GetUnit
  L2_444 = L2_444(A0_442)
  System.SetUnitFlag(L2_444, 32, A1_443)
end
L0_0.SetEnableShadow = L1_1
L0_0 = Unit
function L1_1(A0_445, A1_446)
  local L2_447
  L2_447 = System
  L2_447 = L2_447.GetUnit
  L2_447 = L2_447(A0_445)
  System.SetUnitFlag(L2_447, 33, A1_446)
end
L0_0.SetSuperBlowTension = L1_1
L0_0 = Unit
function L1_1(A0_448, A1_449, ...)
  local L3_451
  L2_450 = System
  L2_450 = L2_450.GetUnit
  L3_451 = A0_448
  L2_450 = L2_450(L3_451)
  L3_451 = false
  if select("#", ...) >= 1 then
    L3_451 = select(1, ...)
  end
  if L3_451 and not Utility.IsEventSkip() then
    proc = System.WaterEffect(L2_450, A1_449)
    Utility.WaitProcedure(proc)
  else
    System.SetUnitFlag(L2_450, 28, A1_449)
  end
end
L0_0.SetFloatingWater = L1_1
L0_0 = Unit
function L1_1(A0_452)
  local L1_453
  L1_453 = System
  L1_453 = L1_453.GetUnit
  L1_453 = L1_453(A0_452)
  return Unit.GetPosition(L1_453).X >= 0 and 0 <= Unit.GetPosition(L1_453).Y
end
L0_0.IsValidPosition = L1_1
L0_0 = Unit
function L1_1(A0_454, A1_455)
  local L2_456, L3_457, L4_458, L5_459
  L2_456 = System
  L2_456 = L2_456.GetUnit
  L3_457 = A0_454
  L2_456 = L2_456(L3_457)
  L3_457 = System
  L3_457 = L3_457.PlayDamageValueEffect
  L4_458 = L2_456
  L5_459 = A1_455
  L3_457 = L3_457(L4_458, L5_459)
  L4_458 = Utility
  L4_458 = L4_458.WaitProcedure
  L5_459 = L3_457
  L4_458(L5_459)
  L4_458 = System
  L4_458 = L4_458.AnimateHpBar
  L5_459 = L2_456
  L4_458 = L4_458(L5_459, A1_455)
  L3_457 = L4_458
  L4_458 = Utility
  L4_458 = L4_458.WaitProcedure
  L5_459 = L3_457
  L4_458(L5_459)
  L4_458 = Unit
  L4_458 = L4_458.GetHp
  L5_459 = L2_456
  L4_458 = L4_458(L5_459)
  L4_458 = L4_458 - A1_455
  L5_459 = Unit
  L5_459 = L5_459.SetHp
  L5_459(L2_456, L4_458)
  L5_459 = false
  if L4_458 <= 0 then
    if Unit.HasDeadEvent(L2_456) then
      OnDiedEvent(L2_456)
    elseif Unit.IsPlayer(L2_456) and not Unit.IsSfs(L2_456) then
      OutEvent(0, L2_456, 0, OutEventType.Explosion, true)
    else
      Unit.BiriBiriKill(L2_456)
    end
    L5_459 = Unit.IsImportant(L2_456)
  end
  if Stage.IsGameOver() or L5_459 then
    GameOverEvent()
    System.GameOver()
  else
    BeforeEndWithoutBattleControl()
  end
end
L0_0.DamageHp = L1_1
L0_0 = Unit
function L1_1(A0_460, A1_461)
  local L2_462, L3_463
  L2_462 = System
  L2_462 = L2_462.GetUnit
  L3_463 = A0_460
  L2_462 = L2_462(L3_463)
  L3_463 = System
  L3_463 = L3_463.UseMapWeapon
  L3_463 = L3_463(L2_462, A1_461)
  Utility.WaitProcedure(L3_463)
end
L0_0.UseMapWeapon = L1_1
L0_0 = Unit
function L1_1(A0_464)
  local L1_465
  L1_465 = System
  L1_465 = L1_465.GetUnit
  L1_465 = L1_465(A0_464)
  System.ShowWeaponRange(L1_465, false)
end
L0_0.ShowWeaponRange = L1_1
L0_0 = Unit
function L1_1()
  System.HideWeaponRange()
end
L0_0.HideWeaponRange = L1_1
L0_0 = Unit
function L1_1(A0_466, A1_467, A2_468)
  local L3_469, L4_470
  L3_469 = System
  L3_469 = L3_469.GetUnit
  L4_470 = A0_466
  L3_469 = L3_469(L4_470)
  L4_470 = System
  L4_470 = L4_470.BlinkUnit
  L4_470 = L4_470(L3_469, A1_467, A2_468)
  Utility.WaitProcedure(L4_470)
end
L0_0.Blink = L1_1
L0_0 = Unit
function L1_1(A0_471, A1_472)
  local L2_473, L3_474, L4_475, L5_476
  L2_473 = System
  L2_473 = L2_473.GetUnit
  L3_474 = A0_471
  L2_473 = L2_473(L3_474)
  L3_474 = Unit
  L3_474 = L3_474.GetMapIndex
  L4_475 = L2_473
  L3_474 = L3_474(L4_475)
  L4_475 = Unit
  L4_475 = L4_475.GetPosition
  L5_476 = L2_473
  L4_475 = L4_475(L5_476)
  L5_476 = Unit
  L5_476 = L5_476.GetDirection
  L5_476 = L5_476(L2_473)
  Unit.DisappearFakeInstant(L2_473)
  System.ChangeMachineSpec(L2_473, A1_472)
  Unit.AppearJump(L2_473, L3_474, L4_475.X, L4_475.Y, L5_476, UnitAppearType.Instant)
end
L0_0.ChangeMachineSpec = L1_1
L0_0 = Unit
function L1_1(A0_477, A1_478)
  local L2_479, L3_480, L4_481, L5_482
  L2_479 = System
  L2_479 = L2_479.GetUnit
  L3_480 = A0_477
  L2_479 = L2_479(L3_480)
  L3_480 = Unit
  L3_480 = L3_480.GetMapIndex
  L4_481 = L2_479
  L3_480 = L3_480(L4_481)
  L4_481 = Unit
  L4_481 = L4_481.GetPosition
  L5_482 = L2_479
  L4_481 = L4_481(L5_482)
  L5_482 = Unit
  L5_482 = L5_482.GetDirection
  L5_482 = L5_482(L2_479)
  Unit.DisappearFakeInstant(L2_479)
  System.ChangeCharacterSpec(L2_479, A1_478)
  Unit.AppearJump(L2_479, L3_480, L4_481.X, L4_481.Y, L5_482, UnitAppearType.Instant)
end
L0_0.ChangeCharacterSpec = L1_1
L0_0 = {}
Battle = L0_0
L0_0 = Battle
function L1_1()
  return System.AllBattleUnits()
end
L0_0.AllUnits = L1_1
L0_0 = Battle
function L1_1()
  return System.MainAttacker()
end
L0_0.MainAttacker = L1_1
L0_0 = Battle
function L1_1()
  return System.MainTarget()
end
L0_0.MainTarget = L1_1
L0_0 = Battle
function L1_1()
  return System.TargetUnits()
end
L0_0.TargetUnits = L1_1
L0_0 = Battle
function L1_1()
  return System.DeadUnits()
end
L0_0.DeadUnits = L1_1
L0_0 = Battle
function L1_1(A0_483)
  local L1_484
  L1_484 = System
  L1_484 = L1_484.GetUnit
  L1_484 = L1_484(A0_483)
  return System.ContainBattleUnit(L1_484)
end
L0_0.ContainBattleUnit = L1_1
L0_0 = Battle
function L1_1(A0_485)
  local L1_486
  L1_486 = System
  L1_486 = L1_486.GetUnit
  L1_486 = L1_486(A0_485)
  return System.ContainDeadUnit(L1_486)
end
L0_0.ContainDeadUnit = L1_1
L0_0 = Battle
function L1_1(A0_487)
  local L1_488
  L1_488 = System
  L1_488 = L1_488.GetUnit
  L1_488 = L1_488(A0_487)
  return System.MainAttackerWeapon(L1_488)
end
L0_0.MainAttackerWeapon = L1_1
L0_0 = Battle
function L1_1(A0_489)
  return System.VSSingle(A0_489)
end
L0_0.VSSingle = L1_1
L0_0 = Battle
function L1_1(A0_490, A1_491)
  local L2_492
  L2_492 = false
  if not System.GetBattleFlag(A0_490) and System.VSSingle(A1_491) then
    L2_492 = true
    System.SetBattleFlag(A0_490, true)
  end
  return L2_492
end
L0_0.VSSingleOnce = L1_1
L0_0 = Battle
function L1_1(A0_493, A1_494)
  return System.VSDouble(A0_493, A1_494)
end
L0_0.VSDouble = L1_1
L0_0 = Battle
function L1_1(A0_495, A1_496, A2_497)
  local L3_498
  L3_498 = false
  if not System.GetBattleFlag(A0_495) and System.VSDouble(A1_496, A2_497) then
    L3_498 = true
    System.SetBattleFlag(A0_495, true)
  end
  return L3_498
end
L0_0.VSDoubleOnce = L1_1
L0_0 = Battle
function L1_1(A0_499, A1_500)
  local L2_501, L3_502
  L2_501 = Battle
  L2_501 = L2_501.VSSingle
  L3_502 = A0_499
  L2_501 = L2_501(L3_502)
  L3_502 = false
  if L2_501 then
    L3_502 = Battle.ContainDeadUnit(A1_500)
  end
  return L3_502
end
L0_0.VSKill = L1_1
L0_0 = Battle
function L1_1(A0_503)
  return System.VSDestroy(A0_503)
end
L0_0.VSDestroy = L1_1
L0_0 = Battle
function L1_1()
  return System.IsDestroyGameOverUnit()
end
L0_0.IsDestroyGameOverUnit = L1_1
L0_0 = Battle
function L1_1()
  return System.IsDestroyGameOverUnitWithoutBattleControl()
end
L0_0.IsDestroyGameOverUnitWithoutBattleControl = L1_1
L0_0 = Battle
function L1_1(A0_504)
  local L1_505
  L1_505 = System
  L1_505 = L1_505.GetUnit
  L1_505 = L1_505(A0_504)
  return System.GetDamage(L1_505)
end
L0_0.GetDamage = L1_1
L0_0 = Battle
function L1_1(A0_506)
  local L1_507
  L1_507 = System
  L1_507 = L1_507.GetUnit
  L1_507 = L1_507(A0_506)
  return System.IsHitTarget(L1_507)
end
L0_0.IsHitTarget = L1_1
L0_0 = Battle
function L1_1()
  System.CancelBattle()
end
L0_0.CancelBattle = L1_1
L0_0 = Battle
function L1_1(A0_508, A1_509, A2_510, ...)
  local L4_512
  L3_511 = false
  L4_512 = select
  L4_512 = L4_512("#", ...)
  if L4_512 >= 1 then
    L4_512 = select
    L4_512 = L4_512(1, ...)
    L3_511 = L4_512
  end
  L4_512 = System
  L4_512 = L4_512.PlayBattleAnimation
  L4_512 = L4_512(A0_508, A1_509, A2_510, L3_511)
  Utility.WaitProcedure(L4_512)
end
L0_0.PlayBattleAnimation = L1_1
L0_0 = Battle
function L1_1()
  return System.IsPlayBattleAnimation()
end
L0_0.IsPlayBattleAnimation = L1_1
L0_0 = {}
UnitSearchType = L0_0
L0_0 = UnitSearchType
L0_0.All = 0
L0_0 = UnitSearchType
L0_0.StandBy = 1
L0_0 = UnitSearchType
L0_0.Appeared = 2
L0_0 = UnitSearchType
L0_0.Died = 3
L0_0 = UnitSearchType
L0_0.InShip = 4
L0_0 = {}
UnitAppearType = L0_0
L0_0 = UnitAppearType
L0_0.Instant = 0
L0_0 = UnitAppearType
L0_0.Normal = 1
L0_0 = UnitAppearType
L0_0.MoveCamera = 2
L0_0 = UnitAppearType
L0_0.Explosion = 3
L0_0 = UnitAppearType
L0_0.MasterExplosion = 4
L0_0 = {}
UnitArmyType = L0_0
L0_0 = UnitArmyType
L0_0.Player = 0
L0_0 = UnitArmyType
L0_0.Guest = 1
L0_0 = UnitArmyType
L0_0.NPC = 2
L0_0 = UnitArmyType
L0_0.Enemy1 = 3
L0_0 = UnitArmyType
L0_0.Enemy2 = 4
L0_0 = UnitArmyType
L0_0.Secret = 5
L0_0 = {}
UnitDirectionType = L0_0
L0_0 = UnitDirectionType
L0_0.North = 0
L0_0 = UnitDirectionType
L0_0.East = 1
L0_0 = UnitDirectionType
L0_0.South = 2
L0_0 = UnitDirectionType
L0_0.West = 3
L0_0 = {}
TensionType = L0_0
L0_0 = TensionType
L0_0.Confuse = 0
L0_0 = TensionType
L0_0.Timid = 1
L0_0 = TensionType
L0_0.Normal = 2
L0_0 = TensionType
L0_0.Aggressive = 3
L0_0 = TensionType
L0_0.SuperAggressive = 4
L0_0 = TensionType
L0_0.SuperBlow = 5
L0_0 = {}
AttackTargetType = L0_0
L0_0 = AttackTargetType
L0_0.None = 0
L0_0 = AttackTargetType
L0_0.PlayerAndGuest = 1
L0_0 = AttackTargetType
L0_0.Player = 2
L0_0 = AttackTargetType
L0_0.Guest = 3
L0_0 = AttackTargetType
L0_0.Enemy1 = 4
L0_0 = AttackTargetType
L0_0.Enemy2 = 5
L0_0 = AttackTargetType
L0_0.ControlId = 6
L0_0 = AttackTargetType
L0_0.ManyHP = 7
L0_0 = AttackTargetType
L0_0.LessHP = 8
L0_0 = AttackTargetType
L0_0.NearestEnemy = 9
L0_0 = AttackTargetType
L0_0.MasterUnit = 10
L0_0 = {}
NoMoveType = L0_0
L0_0 = NoMoveType
L0_0.None = 0
L0_0 = NoMoveType
L0_0.DetectEnemy = 1
L0_0 = NoMoveType
L0_0.Turn = 2
L0_0 = NoMoveType
L0_0.TurnOrDetectEnemy = 3
L0_0 = NoMoveType
L0_0.DefeatControlId = 4
L0_0 = NoMoveType
L0_0.BattleControlId = 5
L0_0 = {}
FollowType = L0_0
L0_0 = FollowType
L0_0.None = 0
L0_0 = FollowType
L0_0.ControlId = 1
L0_0 = FollowType
L0_0.PlayerAndGuest = 2
L0_0 = FollowType
L0_0.Player = 3
L0_0 = {}
AptitudeLandType = L0_0
L0_0 = AptitudeLandType
L0_0.Space = 0
L0_0 = AptitudeLandType
L0_0.Sky = 1
L0_0 = AptitudeLandType
L0_0.Ground = 2
L0_0 = AptitudeLandType
L0_0.Surface = 3
L0_0 = AptitudeLandType
L0_0.Water = 4
L0_0 = {}
AptitudeLevelType = L0_0
L0_0 = AptitudeLevelType
L0_0.E = 0
L0_0 = AptitudeLevelType
L0_0.D = 1
L0_0 = AptitudeLevelType
L0_0.C = 2
L0_0 = AptitudeLevelType
L0_0.B = 3
L0_0 = AptitudeLevelType
L0_0.A = 4
L0_0 = AptitudeLevelType
L0_0.S = 5
L0_0 = AptitudeLevelType
L0_0.Database = 6
L0_0 = {}
KomaAnimationType = L0_0
L0_0 = KomaAnimationType
L0_0.StandBy = 0
L0_0 = KomaAnimationType
L0_0.Move = 1
L0_0 = KomaAnimationType
L0_0.Event1 = 10
L0_0 = KomaAnimationType
L0_0.Event2 = 11
L0_0 = KomaAnimationType
L0_0.Event3 = 12
L0_0 = KomaAnimationType
L0_0.Event4 = 13
L0_0 = KomaAnimationType
L0_0.Event5 = 14
L0_0 = KomaAnimationType
L0_0.Event6 = 15
L0_0 = KomaAnimationType
L0_0.Event7 = 16
L0_0 = KomaAnimationType
L0_0.Event8 = 17
L0_0 = {}
OutEventType = L0_0
L0_0 = OutEventType
L0_0.Disappear = 0
L0_0 = OutEventType
L0_0.Explosion = 1
L0_0 = OutEventType
L0_0.Master = 2
L0_0 = {}
DisplaySizeType = L0_0
L0_0 = DisplaySizeType
L0_0.L = 0
L0_0 = DisplaySizeType
L0_0.LL = 1
L0_0 = DisplaySizeType
L0_0.XL = 2
L0_0 = DisplaySizeType
L0_0.XXL = 3
L0_0 = {}
CharaterCrewType = L0_0
L0_0 = CharaterCrewType
L0_0.Pilot = 0
L0_0 = CharaterCrewType
L0_0.Captain = 0
L0_0 = CharaterCrewType
L0_0.ViceCaptain = 1
L0_0 = CharaterCrewType
L0_0.Operator = 2
L0_0 = CharaterCrewType
L0_0.Steerer = 3
L0_0 = CharaterCrewType
L0_0.Mechanic = 4
L0_0 = CharaterCrewType
L0_0.Guest = 5
