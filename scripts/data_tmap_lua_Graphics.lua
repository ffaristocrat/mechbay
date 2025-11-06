local L1_1
L0_0 = {}
SSA = L0_0
L0_0 = SSA
function L1_1(A0_2, ...)
  local L2_4, L3_5, L4_6
  L1_3 = false
  L2_4 = select
  L3_5 = "#"
  L4_6 = ...
  L2_4 = L2_4(L3_5, L4_6, ...)
  if L2_4 >= 1 then
    L2_4 = select
    L3_5 = 1
    L4_6 = ...
    L2_4 = L2_4(L3_5, L4_6, ...)
    L1_3 = L2_4
  end
  L2_4 = true
  L3_5 = select
  L4_6 = "#"
  L3_5 = L3_5(L4_6, ...)
  if L3_5 >= 2 then
    L3_5 = select
    L4_6 = 2
    L3_5 = L3_5(L4_6, ...)
    L2_4 = L3_5
  end
  L3_5 = System
  L3_5 = L3_5.CreateSSA
  L4_6 = A0_2
  L3_5 = L3_5(L4_6, L1_3, L2_4)
  while true do
    L4_6 = System
    L4_6 = L4_6.IsReadySSA
    L4_6 = L4_6(L3_5)
    if not L4_6 then
      L4_6 = coroutine
      L4_6 = L4_6.yield
      L4_6(0)
    end
  end
  L4_6 = select
  L4_6 = L4_6("#", ...)
  if L4_6 >= 3 then
    L4_6 = select
    L4_6 = L4_6(3, ...)
    SSA.SetSSAIndex(L3_5, L4_6)
  end
  return L3_5
end
L0_0.CreateSSA = L1_1
L0_0 = SSA
function L1_1(A0_7, A1_8, ...)
  local L3_10, L4_11, L5_12, L6_13
  L2_9 = false
  L3_10 = select
  L4_11 = "#"
  L6_13 = ...
  L3_10 = L3_10(L4_11, L5_12, L6_13, ...)
  if L3_10 >= 1 then
    L3_10 = select
    L4_11 = 1
    L6_13 = ...
    L3_10 = L3_10(L4_11, L5_12, L6_13, ...)
    L2_9 = L3_10
  end
  L3_10 = true
  L4_11 = select
  L5_12 = "#"
  L6_13 = ...
  L4_11 = L4_11(L5_12, L6_13, ...)
  if L4_11 >= 2 then
    L4_11 = select
    L5_12 = 2
    L6_13 = ...
    L4_11 = L4_11(L5_12, L6_13, ...)
    L3_10 = L4_11
  end
  L4_11 = System
  L4_11 = L4_11.GetUnit
  L5_12 = A1_8
  L4_11 = L4_11(L5_12)
  L5_12 = System
  L5_12 = L5_12.CreateSSAonUnit
  L6_13 = A0_7
  L5_12 = L5_12(L6_13, L4_11, L2_9, L3_10)
  while true do
    L6_13 = System
    L6_13 = L6_13.IsReadySSA
    L6_13 = L6_13(L5_12)
    if not L6_13 then
      L6_13 = coroutine
      L6_13 = L6_13.yield
      L6_13(0)
    end
  end
  L6_13 = select
  L6_13 = L6_13("#", ...)
  if L6_13 >= 3 then
    L6_13 = select
    L6_13 = L6_13(3, ...)
    SSA.SetSSAIndex(L5_12, L6_13)
  end
  return L5_12
end
L0_0.CreateSSAonUnit = L1_1
L0_0 = SSA
function L1_1(A0_14)
  return (System.CreateSSA(A0_14, true, true))
end
L0_0.CreateSSANotReady = L1_1
L0_0 = SSA
function L1_1(A0_15, A1_16)
  local L2_17
  L2_17 = System
  L2_17 = L2_17.GetUnit
  L2_17 = L2_17(A1_16)
  return (System.CreateSSAonUnit(A0_15, L2_17, true, true))
end
L0_0.CreateSSAonUnitNotReady = L1_1
L0_0 = SSA
function L1_1(A0_18, A1_19)
  System.LoopSSA(A0_18, A1_19)
end
L0_0.Loop = L1_1
L0_0 = SSA
function L1_1(A0_20, A1_21)
  System.ScaleSSA(A0_20, A1_21)
end
L0_0.Scale = L1_1
L0_0 = SSA
function L1_1(A0_22, A1_23, A2_24)
  System.PositionSSA(A0_22, A1_23, A2_24)
end
L0_0.Position = L1_1
L0_0 = SSA
function L1_1(A0_25, A1_26, A2_27)
  System.PositionSSA(A0_25, (A1_26 + 0.5) * Grid.Size(), (A2_27 + 0.5) * Grid.Size())
end
L0_0.CellPosition = L1_1
L0_0 = SSA
function L1_1(A0_28, A1_29)
  System.AngleSSA(A0_28, A1_29)
end
L0_0.Angle = L1_1
L0_0 = SSA
function L1_1(A0_30, A1_31)
  System.VisibleSSA(A0_30, A1_31)
end
L0_0.Visible = L1_1
L0_0 = SSA
function L1_1(A0_32, A1_33)
  System.CanSkipSSA(A0_32, A1_33)
end
L0_0.CanSkip = L1_1
L0_0 = SSA
function L1_1(A0_34)
  return System.IsPlayingSSA(A0_34)
end
L0_0.IsPlaying = L1_1
L0_0 = SSA
function L1_1(A0_35)
  return System.CurrentTimeSSA(A0_35)
end
L0_0.CurrentTime = L1_1
L0_0 = SSA
function L1_1(A0_36, A1_37, A2_38, A3_39)
  System.MoveSSA(A0_36, A1_37, A2_38, A3_39)
end
L0_0.Move = L1_1
L0_0 = SSA
function L1_1(A0_40)
  System.StopSSA(A0_40)
end
L0_0.Stop = L1_1
L0_0 = SSA
function L1_1(A0_41, A1_42)
  System.PauseSSA(A0_41, A1_42)
end
L0_0.Pause = L1_1
L0_0 = SSA
function L1_1(A0_43, A1_44)
  System.PrioritySSA(A0_43, A1_44)
end
L0_0.Priority = L1_1
L0_0 = SSA
function L1_1(A0_45, A1_46)
  System.SetSSAIndex(A0_45, A1_46)
end
L0_0.SetSSAIndex = L1_1
L0_0 = SSA
function L1_1(A0_47, A1_48)
  local L2_49
  L2_49 = System
  L2_49 = L2_49.GetUnit
  L2_49 = L2_49(A1_48)
  System.KomaPrioritySSA(A0_47, L2_49)
end
L0_0.KomaPriority = L1_1
L0_0 = SSA
function L1_1(A0_50)
  while not System.RemoveLoopPoint(A0_50) do
    Utility.BreakScript()
  end
end
L0_0.RemoveLoopPoint = L1_1
L0_0 = SSA
function L1_1(A0_51, A1_52)
  System.FlipVerticalSSA(A0_51, A1_52)
end
L0_0.FlipVertical = L1_1
L0_0 = SSA
function L1_1(A0_53, A1_54)
  System.FlipHorizontalSSA(A0_53, A1_54)
end
L0_0.FlipHorizontal = L1_1
L0_0 = SSA
function L1_1(A0_55, A1_56, A2_57, A3_58, A4_59)
  System.SetColorSSA(A0_55, A1_56, A2_57, A3_58, A4_59)
end
L0_0.SetColor = L1_1
L0_0 = SSA
function L1_1(A0_60, A1_61, A2_62, A3_63, A4_64)
  local L5_65
  L5_65 = System
  L5_65 = L5_65.GetUnit
  L5_65 = L5_65(A1_61)
  return System.MultiEffectAroundUnit(A0_60, L5_65, A2_62, A3_63, A4_64)
end
L0_0.MultiEffectAroundUnit = L1_1
L0_0 = SSA
function L1_1(A0_66, A1_67, A2_68, A3_69)
  local L4_70, L5_71
  L4_70 = System
  L4_70 = L4_70.GetUnit
  L5_71 = A0_66
  L4_70 = L4_70(L5_71)
  L5_71 = System
  L5_71 = L5_71.CreateMapWeaponEffect
  L5_71 = L5_71(L4_70, A1_67, A2_68, A3_69)
  while not System.IsReadySSA(L5_71) do
    coroutine.yield(0)
  end
  return L5_71
end
L0_0.CreateMapWeaponEffect = L1_1
L0_0 = SSA
function L1_1(A0_72)
  return System.GetDisappearTime(A0_72)
end
L0_0.GetDisappearTime = L1_1
L0_0 = SSA
function L1_1()
  return System.GetMoveRangeWithMapWeapon()
end
L0_0.GetMoveRangeWithMapWeapon = L1_1
L0_0 = SSA
function L1_1(A0_73, A1_74)
  local L2_75
  L2_75 = System
  L2_75 = L2_75.GetUnit
  L2_75 = L2_75(A0_73)
  return System.MoveUnitWithMapWeapon(L2_75, A1_74)
end
L0_0.MoveUnitWithMapWeapon = L1_1
L0_0 = SSA
function L1_1(A0_76)
  local L1_77
  L1_77 = System
  L1_77 = L1_77.GetUnit
  L1_77 = L1_77(A0_76)
  return System.GetKomaAnimeMapEffect(L1_77)
end
L0_0.GetKomaAnimeMapEffect = L1_1
L0_0 = SSA
function L1_1(A0_78)
  local L1_79
  L1_79 = System
  L1_79 = L1_79.GetUnit
  L1_79 = L1_79(A0_78)
  return System.IsHaroMapWeapon(L1_79)
end
L0_0.IsHaroMapWeapon = L1_1
L0_0 = SSA
function L1_1(A0_80, A1_81)
  local L2_82
  L2_82 = System
  L2_82 = L2_82.GetUnit
  L2_82 = L2_82(A1_81)
  System.SetTerrainOffsetSSA(A0_80, L2_82)
end
L0_0.SetTerrainOffset = L1_1
L0_0 = SSA
function L1_1(A0_83)
  local L1_84
  L1_84 = System
  L1_84 = L1_84.GetUnit
  L1_84 = L1_84(A0_83)
  return System.IsUnitCenterEffect(L1_84)
end
L0_0.IsUnitCenterEffect = L1_1
L0_0 = SSA
function L1_1(A0_85, A1_86)
  local L2_87
  L2_87 = System
  L2_87 = L2_87.GetUnit
  L2_87 = L2_87(A0_85)
  return System.PlaySpecialMapWeaponVoice(L2_87, A1_86)
end
L0_0.PlaySpecialMapWeaponVoice = L1_1
L0_0 = SSA
function L1_1(A0_88, A1_89, A2_90)
  local L3_91, L4_92
  L3_91 = 0
  while A1_89 > L3_91 do
    L4_92 = L3_91 / A1_89
    if not A2_90 then
      L4_92 = 1 - L4_92
    end
    SSA.SetColor(A0_88, 1, 1, 1, L4_92)
    L3_91 = L3_91 + Utility.GetElapsedTime()
    Utility.BreakScript()
  end
end
L0_0.Fade = L1_1
L0_0 = {}
MapSSA = L0_0
L0_0 = MapSSA
function L1_1(A0_93, A1_94, A2_95)
  System.PositionMapSSA(A0_93, A1_94, A2_95)
end
L0_0.Position = L1_1
L0_0 = MapSSA
function L1_1(A0_96, A1_97)
  System.VisibleMapSSA(A0_96, A1_97)
end
L0_0.Visible = L1_1
L0_0 = {}
EventGraphics = L0_0
L0_0 = EventGraphics
function L1_1(A0_98, A1_99)
  local L2_100
  L2_100 = System
  L2_100 = L2_100.CreateGraphic
  L2_100 = L2_100(A0_98, A1_99)
  while not EventGraphics.IsReady(L2_100) do
    Utility.BreakScript()
  end
  return L2_100
end
L0_0.Create = L1_1
L0_0 = EventGraphics
function L1_1(A0_101, ...)
  local L2_103
  L1_102 = EventGraphics
  L1_102 = L1_102.DefaultFadeTime
  L2_103 = select
  L2_103 = L2_103("#", ...)
  if L2_103 >= 1 then
    L2_103 = select
    L2_103 = L2_103(1, ...)
    L1_102 = L2_103
  end
  L2_103 = System
  L2_103 = L2_103.FadeGraphic
  L2_103(A0_101, L1_102, true)
  L2_103 = true
  if select("#", ...) >= 2 then
    L2_103 = select(2, ...)
  end
  if L2_103 then
    while not System.IsCompletedFadeGraphic(A0_101) do
      coroutine.yield(0)
    end
  end
end
L0_0.FadeIn = L1_1
L0_0 = EventGraphics
function L1_1(A0_104, ...)
  local L2_106
  L1_105 = EventGraphics
  L1_105 = L1_105.DefaultFadeTime
  L2_106 = select
  L2_106 = L2_106("#", ...)
  if L2_106 >= 1 then
    L2_106 = select
    L2_106 = L2_106(1, ...)
    L1_105 = L2_106
  end
  L2_106 = System
  L2_106 = L2_106.FadeGraphic
  L2_106(A0_104, L1_105, false)
  L2_106 = true
  if select("#", ...) >= 2 then
    L2_106 = select(2, ...)
  end
  if L2_106 then
    while not System.IsCompletedFadeGraphic(A0_104) do
      coroutine.yield(0)
    end
  end
end
L0_0.FadeOut = L1_1
L0_0 = EventGraphics
function L1_1(A0_107)
  return System.IsReadyGraphic(A0_107)
end
L0_0.IsReady = L1_1
L0_0 = EventGraphics
function L1_1(A0_108)
  return System.IsCompletedFadeGraphic(A0_108)
end
L0_0.IsCompletedFade = L1_1
L0_0 = EventGraphics
function L1_1(A0_109, A1_110, A2_111, A3_112)
  return System.SetGraphicColor(A0_109, A1_110, A2_111, A3_112)
end
L0_0.SetColor = L1_1
L0_0 = EventGraphics
function L1_1(A0_113, A1_114)
  return System.SetGraphicMaxAlpha(A0_113, A1_114)
end
L0_0.SetMaxAlpha = L1_1
L0_0 = EventGraphics
function L1_1(A0_115, A1_116, A2_117, A3_118)
  local L4_119
  L4_119 = System
  L4_119 = L4_119.FadeScreen
  L4_119 = L4_119(0, true, A0_115, A1_116, A2_117, A3_118)
  while not System.IsCompletedFadeGraphic(L4_119) do
    coroutine.yield(0)
  end
  return L4_119
end
L0_0.FadeInScreen = L1_1
L0_0 = EventGraphics
function L1_1(A0_120, A1_121)
  System.FadeScreen(A0_120, false, A1_121, 0, 0, 0)
  while not System.IsCompletedFadeGraphic(A0_120) do
    coroutine.yield(0)
  end
end
L0_0.FadeOutScreen = L1_1
L0_0 = EventGraphics
function L1_1(A0_122)
  local L1_123
  L1_123 = System
  L1_123 = L1_123.FadeStartEventScreen
  L1_123 = L1_123(true, A0_122)
  while not System.IsCompletedFadeGraphic(L1_123) do
    coroutine.yield(0)
  end
end
L0_0.FadeInStartEventScreen = L1_1
L0_0 = EventGraphics
function L1_1(A0_124)
  local L1_125
  L1_125 = System
  L1_125 = L1_125.FadeStartEventScreen
  L1_125 = L1_125(false, A0_124)
  Utility.WaitProcedure(L1_125)
end
L0_0.FadeOutStartEventScreen = L1_1
L0_0 = EventGraphics
function L1_1()
  local L0_126
  L0_126 = System
  L0_126 = L0_126.FadeTelopScreen
  L0_126 = L0_126(true)
  while not System.IsCompletedFadeGraphic(L0_126) do
    coroutine.yield(0)
  end
end
L0_0.FadeInTelopScreen = L1_1
L0_0 = EventGraphics
function L1_1()
  local L0_127
  L0_127 = System
  L0_127 = L0_127.FadeTelopScreen
  L0_127 = L0_127(false)
  while not System.IsCompletedFadeGraphic(L0_127) do
    coroutine.yield(0)
  end
end
L0_0.FadeOutTelopScreen = L1_1
L0_0 = EventGraphics
function L1_1(A0_128)
  System.ShakeGraphic(A0_128, true)
end
L0_0.StartShake = L1_1
L0_0 = EventGraphics
function L1_1(A0_129)
  System.ShakeGraphic(A0_129, false)
end
L0_0.StopShake = L1_1
L0_0 = EventGraphics
function L1_1(A0_130, A1_131, A2_132, A3_133, ...)
  local L5_135, L6_136, L7_137, L8_138, L9_139
  L4_134 = 1
  L9_139 = ...
  if L5_135 >= 1 then
    L9_139 = ...
    L4_134 = L5_135
  end
  for L8_138 = 1, L4_134 do
    L9_139 = System
    L9_139 = L9_139.MoveGraphic
    L9_139 = L9_139(A0_130, A1_131, A2_132, A3_133)
    Utility.WaitProcedure(L9_139)
    Utility.Wait(0.1)
  end
end
L0_0.Move = L1_1
L0_0 = EventGraphics
function L1_1(A0_140, A1_141)
  System.SetGraphicRender3d(A0_140, A1_141)
end
L0_0.SetRender3d = L1_1
L0_0 = EventGraphics
function L1_1(A0_142, A1_143, A2_144, ...)
  local L5_146, L6_147, L7_148
  L4_145 = System
  L4_145 = L4_145.StartSlideShow
  L5_146 = A0_142
  L6_147 = A1_143
  L7_148 = A2_144
  L4_145(L5_146, L6_147, L7_148, ...)
end
L0_0.StartSlideShow = L1_1
L0_0 = EventGraphics
function L1_1()
  local L0_149
  L0_149 = System
  L0_149 = L0_149.EndSlideShow
  L0_149 = L0_149()
  Utility.WaitProcedure(L0_149)
end
L0_0.EndSlideShow = L1_1
L0_0 = EventGraphics
function L1_1(A0_150)
  System.FadeNowLoading(A0_150)
  if not A0_150 then
    while not System.IsIdleNowLoading() do
      coroutine.yield(0)
    end
  end
end
L0_0.FadeNowLoading = L1_1
L0_0 = {}
Movie = L0_0
L0_0 = Movie
function L1_1(A0_151, A1_152)
  return System.CreateMovie(A0_151, A1_152)
end
L0_0.Create = L1_1
L0_0 = Movie
function L1_1()
  return System.IsReadyMovie()
end
L0_0.IsReady = L1_1
L0_0 = Movie
function L1_1()
  return System.IsPlayingMovie()
end
L0_0.IsPlaying = L1_1
L0_0 = Movie
function L1_1(A0_153, A1_154, A2_155)
  System.SetMovieFadeColor(A0_153, A1_154, A2_155)
end
L0_0.SetFadeColor = L1_1
L0_0 = Movie
function L1_1(A0_156, A1_157)
  return System.AddProfileMovie(A0_156, A1_157)
end
L0_0.AddProfile = L1_1
L0_0 = {}
Camera = L0_0
L0_0 = Camera
function L1_1(A0_158, ...)
  local L2_160
  L1_159 = 3 - A0_158
  L1_159 = L1_159 * 0.25
  L1_159 = 1 + L1_159
  L2_160 = System
  L2_160 = L2_160.CameraZoom
  L2_160 = L2_160(L1_159, ...)
  Utility.WaitProcedure(L2_160)
end
L0_0.CameraLv = L1_1
L0_0 = Camera
function L1_1()
  local L0_161, L1_162
  L0_161 = System
  L0_161 = L0_161.GetCameraZoom
  L0_161 = L0_161()
  L0_161 = L0_161 + 0.25
  L1_162 = System
  L1_162 = L1_162.CameraZoom
  L1_162 = L1_162(L0_161)
  Utility.WaitProcedure(L1_162)
end
L0_0.ZoomIn = L1_1
L0_0 = Camera
function L1_1()
  local L0_163, L1_164
  L0_163 = System
  L0_163 = L0_163.GetCameraZoom
  L0_163 = L0_163()
  L0_163 = L0_163 - 0.25
  L1_164 = System
  L1_164 = L1_164.CameraZoom
  L1_164 = L1_164(L0_163)
  Utility.WaitProcedure(L1_164)
end
L0_0.ZoomOut = L1_1
L0_0 = Camera
function L1_1()
  local L0_165
  L0_165 = System
  L0_165 = L0_165.CameraZoom
  L0_165 = L0_165(1)
  Utility.WaitProcedure(L0_165)
end
L0_0.ZoomClear = L1_1
L0_0 = Camera
function L1_1()
  System.StartShakeCamera()
end
L0_0.StartShake = L1_1
L0_0 = Camera
function L1_1()
  System.EndShakeCamera()
end
L0_0.EndShake = L1_1
L0_0 = EventGraphics
L0_0.DefaultFadeTime = 0.5
L0_0 = {}
Priority2D = L0_0
L0_0 = Priority2D
L0_0.MapFade = 5000
L0_0 = Priority2D
L0_0.EventGraphic = 7000
L0_0 = Priority2D
L0_0.MessageWindow = 10000
L0_0 = Priority2D
L0_0.SSA = 50000
L0_0 = {}
Priority3D = L0_0
L0_0 = Priority3D
L0_0.Cursor = 50800
L0_0 = Priority3D
L0_0.Marker = 150100
L0_0 = Priority3D
L0_0.SSA = 150200
L0_0 = Priority3D
L0_0.Explode = 202000
L0_0 = {}
MovieType = L0_0
L0_0 = MovieType
L0_0.Battle = 0
L0_0 = MovieType
L0_0.Event = 1
L0_0 = {}
MapWeaponEffectType = L0_0
L0_0 = MapWeaponEffectType
L0_0.Normal = 0
L0_0 = MapWeaponEffectType
L0_0.SelfExplosion = 1
L0_0 = MapWeaponEffectType
L0_0.Snipe = 2
L0_0 = MapWeaponEffectType
L0_0.SubRange = 3
L0_0 = MapWeaponEffectType
L0_0.Move = 4
