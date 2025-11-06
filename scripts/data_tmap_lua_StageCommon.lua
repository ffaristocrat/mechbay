gameover = 0
gameclear = 0
questclear = 0
se_call = "sf90500.hca"
se_kiki = "sb10050.hca"
se_online = "sa00090.hca"
se_shake = "sf90220.hca"
se_kamae = "sf90290.hca"
se_gain = "sf90790.hca"
se_noise = "sf90510.hca"
waitTime0 = "0.4"
waitTime1 = "1"
waitTime2 = "1.5"
waitTime3 = "2.0"
fadeSpeed0 = "1"
fadeSpeed1 = "2"
fadeSpeed2 = "3"
fadeSpeed3 = "4"
cursorPSlow = 2.5
cursorSlow = 5
cursorRSlow = 7
cursorNormal = 10
cursorRFast = 15
cursorFast = 20
L0_0 = {
  "G1220U03200",
  "G1220U03300"
}
ELSUnitList = L0_0
L0_0 = {
  "G1220U03800",
  "G1220U03900"
}
ELSGNXListS = L0_0
L0_0 = {
  "G1220U04000"
}
ELSGNXListM = L0_0
function L0_0(A0_1)
  local L1_2
  L1_2 = false
  for _FORV_6_, _FORV_7_ in ipairs(ELSUnitList) do
    if _FORV_7_ == Unit.GetMachineId(A0_1) then
      L1_2 = true
      break
    end
  end
  return L1_2
end
IsELSUnit = L0_0
function L0_0(A0_3)
  local L1_4
  L1_4 = ""
  if Unit.GetDisplaySize(A0_3) == DisplaySizeType.L then
    L1_4 = ELSGNXListS[math.random(#ELSGNXListS)]
  elseif Unit.GetDisplaySize(A0_3) > DisplaySizeType.L then
    L1_4 = ELSGNXListM[math.random(#ELSGNXListM)]
  end
  return L1_4
end
GetELSGNXId = L0_0
function L0_0(A0_5, A1_6)
  local L2_7, L3_8, L4_9
  L2_7 = Unit
  L2_7 = L2_7.GetUnit
  L3_8 = A0_5
  L2_7 = L2_7(L3_8)
  L3_8 = Unit
  L3_8 = L3_8.GetPosition
  L4_9 = L2_7
  L3_8 = L3_8(L4_9)
  L4_9 = 0
  for _FORV_8_ = 1, 4 do
    L4_9 = SSA.CreateSSA(901)
    SSA.CellPosition(L4_9, (math.random() - 0.5) * A1_6 + L3_8.X, (math.random() - 0.5) * A1_6 + L3_8.Y)
    Utility.Wait(0.1)
  end
  _FOR_.WaitProcedure(L4_9)
end
BombEffectAroundUnit = L0_0
function L0_0(A0_10, A1_11, A2_12)
  local L3_13, L4_14, L5_15, L6_16, L7_17, L8_18, L9_19, L10_20, L11_21, L12_22, L13_23
  L3_13 = A0_10
  L4_14 = A1_11
  L5_15 = 0
  for L9_19 = 1, 4 do
    L10_20 = math
    L10_20 = L10_20.random
    L10_20 = L10_20()
    L10_20 = L10_20 - 0.5
    L10_20 = L10_20 * A2_12
    L11_21 = math
    L11_21 = L11_21.random
    L11_21 = L11_21()
    L11_21 = L11_21 - 0.5
    L11_21 = L11_21 * A2_12
    L12_22 = L10_20 + L3_13
    L12_22 = L12_22 + 0.5
    L13_23 = Grid
    L13_23 = L13_23.Size
    L13_23 = L13_23()
    L12_22 = L12_22 * L13_23
    L13_23 = L11_21 + L4_14
    L13_23 = L13_23 + 0.5
    L13_23 = L13_23 * Grid.Size()
    L5_15 = SSA.CreateSSA(901)
    SSA.Position(L5_15, L12_22, L13_23)
    Utility.Wait(0.1)
  end
  L6_16(L7_17)
end
BombEffectAroundPoint = L0_0
function L0_0(A0_24, A1_25)
  local L2_26, L3_27, L4_28, L5_29, L6_30, L7_31, L8_32, L9_33, L10_34, L11_35, L12_36
  L2_26 = Unit
  L2_26 = L2_26.GetUnit
  L3_27 = A0_24
  L2_26 = L2_26(L3_27)
  L3_27 = Unit
  L3_27 = L3_27.GetPosition
  L4_28 = L2_26
  L3_27 = L3_27(L4_28)
  L4_28 = 0
  for L8_32 = 1, 4 do
    L9_33 = math
    L9_33 = L9_33.random
    L9_33 = L9_33()
    L9_33 = L9_33 - 0.5
    L9_33 = L9_33 * A1_25
    L10_34 = math
    L10_34 = L10_34.random
    L10_34 = L10_34()
    L10_34 = L10_34 - 0.5
    L10_34 = L10_34 * A1_25
    L11_35 = L3_27.X
    L11_35 = L9_33 + L11_35
    L11_35 = L11_35 + 0.5
    L12_36 = Grid
    L12_36 = L12_36.Size
    L12_36 = L12_36()
    L11_35 = L11_35 * L12_36
    L12_36 = L3_27.Y
    L12_36 = L10_34 + L12_36
    L12_36 = L12_36 + 0.5
    L12_36 = L12_36 * Grid.Size()
    L4_28 = SSA.CreateSSAonUnit(900, L2_26)
    SSA.Position(L4_28, L11_35, L12_36)
    Utility.Wait(0.1)
  end
  L5_29(L6_30)
end
BiriEffectAroundUnit = L0_0
function L0_0(A0_37, A1_38, A2_39, A3_40)
  local L4_41, L5_42, L6_43, L7_44, L8_45, L9_46, L10_47, L11_48, L12_49, L13_50, L14_51
  L4_41 = A0_37
  L5_42 = A1_38
  L6_43 = 0
  for L10_47 = 1, A3_40 do
    L11_48 = math
    L11_48 = L11_48.random
    L11_48 = L11_48()
    L11_48 = L11_48 - 0.5
    L11_48 = L11_48 * A2_39
    L12_49 = math
    L12_49 = L12_49.random
    L12_49 = L12_49()
    L12_49 = L12_49 - 0.5
    L12_49 = L12_49 * A2_39
    L13_50 = L11_48 + L4_41
    L13_50 = L13_50 + 0.5
    L14_51 = Grid
    L14_51 = L14_51.Size
    L14_51 = L14_51()
    L13_50 = L13_50 * L14_51
    L14_51 = L12_49 + L5_42
    L14_51 = L14_51 + 0.5
    L14_51 = L14_51 * Grid.Size()
    L6_43 = SSA.CreateSSA(901)
    SSA.Position(L6_43, L13_50, L14_51)
    Utility.Wait(0.1)
  end
  L7_44(L8_45)
end
BombEffectAroundPointCount = L0_0
function L0_0(A0_52, A1_53)
  local L2_54
  L2_54 = Unit
  L2_54 = L2_54.GetParameter
  L2_54 = L2_54(A0_52)
  L2_54.Hp = A1_53
  Unit.SetParameter(A0_52, L2_54)
end
SetUnitHp = L0_0
function L0_0(A0_55, A1_56)
  local L2_57, L3_58, L4_59
  L2_57 = Unit
  L2_57 = L2_57.GetUnit
  L3_58 = A0_55
  L2_57 = L2_57(L3_58)
  L3_58 = Unit
  L3_58 = L3_58.GetPosition
  L4_59 = L2_57
  L3_58 = L3_58(L4_59)
  L4_59 = 0
  for _FORV_8_ = 1, 4 do
    L4_59 = SSA.CreateSSAonUnit(901, L2_57)
    SSA.CellPosition(L4_59, (math.random() - 0.5) * A1_56 + L3_58.X, (math.random() - 0.5) * A1_56 + L3_58.Y)
    Utility.Wait(0.1)
  end
end
BombEffectAroundUnit_Nowait = L0_0
function L0_0(A0_60, A1_61)
  local L2_62, L3_63, L4_64, L5_65, L6_66, L7_67, L8_68, L9_69, L10_70, L11_71, L12_72
  L2_62 = Unit
  L2_62 = L2_62.GetUnit
  L3_63 = A0_60
  L2_62 = L2_62(L3_63)
  L3_63 = Unit
  L3_63 = L3_63.GetPosition
  L4_64 = L2_62
  L3_63 = L3_63(L4_64)
  L4_64 = 0
  for L8_68 = 1, 4 do
    L9_69 = math
    L9_69 = L9_69.random
    L9_69 = L9_69()
    L9_69 = L9_69 - 0.5
    L9_69 = L9_69 * A1_61
    L10_70 = math
    L10_70 = L10_70.random
    L10_70 = L10_70()
    L10_70 = L10_70 - 0.5
    L10_70 = L10_70 * A1_61
    L11_71 = L3_63.X
    L11_71 = L9_69 + L11_71
    L11_71 = L11_71 + 0.5
    L12_72 = Grid
    L12_72 = L12_72.Size
    L12_72 = L12_72()
    L11_71 = L11_71 * L12_72
    L12_72 = L3_63.Y
    L12_72 = L10_70 + L12_72
    L12_72 = L12_72 + 0.5
    L12_72 = L12_72 * Grid.Size()
    L4_64 = SSA.CreateSSAonUnit(900, L2_62)
    SSA.Position(L4_64, L11_71, L12_72)
    Utility.Wait(0.1)
  end
end
BiriEffectAroundUnit_Nowait = L0_0
function L0_0(A0_73, A1_74, A2_75, A3_76)
  local L4_77, L5_78, L6_79, L7_80, L8_81, L9_82, L10_83, L11_84, L12_85, L13_86, L14_87
  L4_77 = A0_73
  L5_78 = A1_74
  L6_79 = 0
  for L10_83 = 1, A3_76 do
    L11_84 = math
    L11_84 = L11_84.random
    L11_84 = L11_84()
    L11_84 = L11_84 - 0.5
    L11_84 = L11_84 * A2_75
    L12_85 = math
    L12_85 = L12_85.random
    L12_85 = L12_85()
    L12_85 = L12_85 - 0.5
    L12_85 = L12_85 * A2_75
    L13_86 = L11_84 + L4_77
    L13_86 = L13_86 + 0.5
    L14_87 = Grid
    L14_87 = L14_87.Size
    L14_87 = L14_87()
    L13_86 = L13_86 * L14_87
    L14_87 = L12_85 + L5_78
    L14_87 = L14_87 + 0.5
    L14_87 = L14_87 * Grid.Size()
    L6_79 = SSA.CreateSSA(901)
    SSA.Position(L6_79, L13_86, L14_87)
    Utility.Wait(0.1)
  end
end
BombEffectAroundPointCount_Nowait = L0_0
function L0_0(A0_88)
  local L1_89, L2_90
  L1_89 = Unit
  L1_89 = L1_89.GetUnit
  L2_90 = A0_88
  L1_89 = L1_89(L2_90)
  L2_90 = 0
  L2_90 = SSA.CreateSSAonUnit(900, L1_89)
  Utility.Wait(0.4)
  L2_90 = SSA.CreateSSAonUnit(901, L1_89)
  Utility.Wait(0.2)
  Unit.DisappearInstant(L1_89)
end
BiriKill_Nowait = L0_0
function L0_0(A0_91)
  local L1_92, L2_93
  L1_92 = Unit
  L1_92 = L1_92.GetUnit
  L2_93 = A0_91
  L1_92 = L1_92(L2_93)
  L2_93 = 0
  if Unit.IsAlive(L1_92) == true then
    Cursor.MoveToUnit(L1_92, 0, true, true)
    L2_93 = SSA.CreateSSAonUnit(901, L1_92)
    Utility.Wait(0.2)
    Unit.DisappearInstant(L1_92)
  end
end
Kill_Nowait = L0_0
function L0_0(A0_94, A1_95)
  local L2_96, L3_97
  L2_96 = Unit
  L2_96 = L2_96.GetUnit
  L3_97 = A0_94
  L2_96 = L2_96(L3_97)
  L3_97 = Unit
  L3_97 = L3_97.IsInWarShip
  L3_97 = L3_97(L2_96)
  if L3_97 == true then
    L3_97 = Unit
    L3_97 = L3_97.GetParameter
    L3_97 = L3_97(L2_96)
    L3_97.Hp = L3_97.Hp + L3_97.MaxHp / 100 * A1_95
    L3_97.En = L3_97.En + L3_97.MaxEn / 100 * A1_95
    Unit.SetParameter(L2_96, L3_97)
  end
end
WS_Charge = L0_0
function L0_0(A0_98, A1_99, A2_100)
  local L3_101, L4_102, L5_103
  L3_101 = 1
  L4_102 = ""
  L5_103 = 0
  repeat
    L3_101 = math.random(#A0_98)
    L4_102 = A0_98[L3_101]
    L5_103 = L5_103 + 1
  until not Unit.IsAppeared(L4_102) or L5_103 >= 1000
  if L5_103 < 1000 then
    Unit.AppearJump(L4_102, Map.GetIndex(), A1_99, A2_100, UnitDirectionType.South, UnitAppearType.Normal)
  else
  end
end
ReinforceUnit = L0_0
function L0_0(A0_104)
  local L1_105
  L1_105 = Unit
  L1_105 = L1_105.GetUnitsByGroupName
  L1_105 = L1_105(A0_104, UnitSearchType.StandBy)
  Unit.AppearFast(0.2, table.unpack(L1_105))
end
AppearGroupFast = L0_0
function L0_0(A0_106)
  local L1_107
  L1_107 = Unit
  L1_107 = L1_107.GetUnitsByGroupName
  L1_107 = L1_107(A0_106, UnitSearchType.StandBy)
  Unit.AppearInstant(table.unpack(L1_107))
end
AppearGroupInstant = L0_0
