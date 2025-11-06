local L1_1
L0_0 = {}
Utility = L0_0
L0_0 = Utility
function L1_1(A0_2)
  id = System.Wait(A0_2)
  while System.FindProcedure(id) do
    coroutine.yield(0)
  end
end
L0_0.Wait = L1_1
L0_0 = Utility
function L1_1()
  coroutine.yield(0)
end
L0_0.BreakScript = L1_1
L0_0 = Utility
function L1_1(A0_3)
  while System.FindProcedure(A0_3) do
    coroutine.yield(0)
  end
end
L0_0.WaitProcedure = L1_1
L0_0 = Utility
function L1_1(A0_4)
  System.CheckTrophy(A0_4)
end
L0_0.CheckTrophy = L1_1
L0_0 = Utility
function L1_1()
  return System.IsSpecialSoundEdition()
end
L0_0.IsSpecialSoundEdition = L1_1
L0_0 = Utility
function L1_1()
  return System.GetLanguageType()
end
L0_0.GetLanguageType = L1_1
L0_0 = Utility
function L1_1()
  return System.GetScreenSize()
end
L0_0.GetScreenSize = L1_1
L0_0 = Utility
function L1_1(A0_5)
  return System.DebugPrint(A0_5)
end
L0_0.DebugPrint = L1_1
L0_0 = Utility
function L1_1()
  return System.GetElapsedTime()
end
L0_0.GetElapsedTime = L1_1
L0_0 = {}
Message = L0_0
L0_0 = Message
function L1_1(A0_6, ...)
  while not System.IsReadyTelop() do
    coroutine.yield(0)
  end
  System.ShowTelop(A0_6, ...)
  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
end
L0_0.ShowTelop = L1_1
L0_0 = Message
function L1_1(A0_7, ...)
  while not System.IsReadyTelop() do
    coroutine.yield(0)
  end
  System.ShowTelopCenter(A0_7, ...)
  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
end
L0_0.ShowTelopCenter = L1_1
L0_0 = Message
function L1_1(A0_8, A1_9, ...)
  while not System.IsReadyTelop() do
    coroutine.yield(0)
  end
  System.ShowTelopWithoutKeyWait(A0_8, A1_9, ...)
  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
end
L0_0.ShowTelopWithoutKeyWait = L1_1
L0_0 = Message
function L1_1(A0_10, ...)
  while not System.IsReadyTelopWindow() do
    coroutine.yield(0)
  end
  System.ShowTelopWindow(A0_10, ...)
  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
end
L0_0.ShowTelopWindow = L1_1
L0_0 = Message
function L1_1(A0_11, A1_12, ...)
  while not System.IsReadyMessageWindow() do
    coroutine.yield(0)
  end
  System.ShowMessageWithCharacterId(A0_11, A1_12, ...)
  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
end
L0_0.ShowMessageWithCharacterId = L1_1
L0_0 = Message
function L1_1(A0_13, A1_14, A2_15, A3_16)
  while not System.IsReadyTwoMessageWindow() do
    coroutine.yield(0)
  end
  System.ShowTwoMessage(A0_13, A1_14, A2_15, A3_16)
  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
end
L0_0.ShowTwoMessage = L1_1
L0_0 = Message
function L1_1(A0_17, A1_18, ...)
  while not System.IsReadyMessageWindow() do
    coroutine.yield(0)
  end
  System.ShowMessageOnline(A0_17, A1_18, false)
  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
end
L0_0.ShowMessageOnline = L1_1
L0_0 = Message
function L1_1(A0_19, A1_20, ...)
  while not System.IsReadyMessageWindow() do
    coroutine.yield(0)
  end
  System.ShowMessageOnline(A0_19, A1_20, true)
  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
end
L0_0.ShowMessageVoiceOnly = L1_1
L0_0 = Message
function L1_1(A0_21, A1_22, ...)
  while not System.IsReadyMessageWindow() do
    coroutine.yield(0)
  end
  System.ShowMessageWithCharacterId(A0_21, A1_22)
end
L0_0.ShowMessageWithoutKeyWait = L1_1
L0_0 = Message
function L1_1()
  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
end
L0_0.IsShowNextMessage = L1_1
L0_0 = Message
function L1_1()
  System.CloseMessageWindow()
  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
end
L0_0.CloseWindow = L1_1
L0_0 = Message
function L1_1()
  System.CloseMessageWindowRight()
  Message.CloseWindow()
end
L0_0.CloseWindowRight = L1_1
L0_0 = Message
function L1_1()
  System.CloseMessageWindowFront()
  while not System.IsCloseMessageWindowFront() do
    coroutine.yield(0)
  end
end
L0_0.CloseWindowFront = L1_1
L0_0 = Message
function L1_1()
  Message.CloseWindow()
end
L0_0.CloseTelopWindow = L1_1
L0_0 = {}
SSA = L0_0
L0_0 = SSA
function L1_1(A0_23)
  local L1_24
  L1_24 = System
  L1_24 = L1_24.CreateSSA
  L1_24 = L1_24(A0_23)
  while not System.IsReadySSA(L1_24) do
    coroutine.yield(0)
  end
  return L1_24
end
L0_0.CreateSSA = L1_1
L0_0 = SSA
function L1_1(A0_25, A1_26)
  System.LoopSSA(A0_25, A1_26)
end
L0_0.Loop = L1_1
L0_0 = SSA
function L1_1(A0_27, A1_28)
  System.VisibleSSA(A0_27, A1_28)
end
L0_0.Visible = L1_1
L0_0 = SSA
function L1_1(A0_29)
  return System.IsPlayingSSA(A0_29)
end
L0_0.IsPlaying = L1_1
L0_0 = SSA
function L1_1(A0_30)
  return System.CurrentTimeSSA(A0_30)
end
L0_0.CurrentTime = L1_1
L0_0 = SSA
function L1_1(A0_31)
  System.StopSSA(A0_31)
end
L0_0.Stop = L1_1
L0_0 = SSA
function L1_1(A0_32, A1_33)
  System.PauseSSA(A0_32, A1_33)
end
L0_0.Pause = L1_1
L0_0 = SSA
function L1_1(A0_34, A1_35)
  System.PrioritySSA(A0_34, A1_35)
end
L0_0.Priority = L1_1
L0_0 = SSA
function L1_1(A0_36)
  while not System.RemoveLoopPoint(A0_36) do
    Utility.BreakScript()
  end
end
L0_0.RemoveLoopPoint = L1_1
L0_0 = SSA
function L1_1(A0_37, A1_38)
  System.FlipVerticalSSA(A0_37, A1_38)
end
L0_0.FlipVertical = L1_1
L0_0 = SSA
function L1_1(A0_39, A1_40)
  System.FlipHorizontalSSA(A0_39, A1_40)
end
L0_0.FlipHorizontal = L1_1
L0_0 = SSA
function L1_1(A0_41, A1_42, A2_43, A3_44, A4_45)
  System.SetColorSSA(A0_41, A1_42, A2_43, A3_44, A4_45)
end
L0_0.SetColor = L1_1
L0_0 = SSA
function L1_1(A0_46, A1_47, A2_48)
  local L3_49, L4_50
  L3_49 = 0
  while A1_47 > L3_49 do
    L4_50 = L3_49 / A1_47
    if not A2_48 then
      L4_50 = 1 - L4_50
    end
    SSA.SetColor(A0_46, 1, 1, 1, L4_50)
    L3_49 = L3_49 + Utility.GetElapsedTime()
    Utility.BreakScript()
  end
end
L0_0.Fade = L1_1
L0_0 = {}
EventGraphics = L0_0
L0_0 = EventGraphics
function L1_1(A0_51, A1_52)
  return System.CreateGraphic(A0_51, A1_52)
end
L0_0.Create = L1_1
L0_0 = EventGraphics
function L1_1(A0_53, ...)
  local L2_55
  L1_54 = EventGraphics
  L1_54 = L1_54.DefaultFadeTime
  L2_55 = select
  L2_55 = L2_55("#", ...)
  if L2_55 >= 1 then
    L2_55 = select
    L2_55 = L2_55(1, ...)
    L1_54 = L2_55
  end
  L2_55 = System
  L2_55 = L2_55.FadeGraphic
  L2_55(A0_53, L1_54, true)
  L2_55 = true
  if select("#", ...) >= 2 then
    L2_55 = select(2, ...)
  end
  if L2_55 then
    while not System.IsCompletedFadeGraphic(A0_53) do
      coroutine.yield(0)
    end
  end
end
L0_0.FadeIn = L1_1
L0_0 = EventGraphics
function L1_1(A0_56, ...)
  local L2_58
  L1_57 = EventGraphics
  L1_57 = L1_57.DefaultFadeTime
  L2_58 = select
  L2_58 = L2_58("#", ...)
  if L2_58 >= 1 then
    L2_58 = select
    L2_58 = L2_58(1, ...)
    L1_57 = L2_58
  end
  L2_58 = System
  L2_58 = L2_58.FadeGraphic
  L2_58(A0_56, L1_57, false)
  L2_58 = true
  if select("#", ...) >= 2 then
    L2_58 = select(2, ...)
  end
  if L2_58 then
    while not System.IsCompletedFadeGraphic(A0_56) do
      coroutine.yield(0)
    end
  end
end
L0_0.FadeOut = L1_1
L0_0 = EventGraphics
function L1_1(A0_59)
  return System.IsReadyGraphic(A0_59)
end
L0_0.IsReady = L1_1
L0_0 = EventGraphics
function L1_1(A0_60)
  return System.IsCompletedFadeGraphic(A0_60)
end
L0_0.IsCompletedFade = L1_1
L0_0 = EventGraphics
function L1_1(A0_61, A1_62, A2_63, A3_64)
  return System.SetGraphicColor(A0_61, A1_62, A2_63, A3_64)
end
L0_0.SetColor = L1_1
L0_0 = EventGraphics
function L1_1(A0_65, A1_66, A2_67, A3_68)
  local L4_69
  L4_69 = System
  L4_69 = L4_69.FadeScreen
  L4_69 = L4_69(0, true, A0_65, A1_66, A2_67, A3_68)
  while not System.IsCompletedFadeGraphic(L4_69) do
    coroutine.yield(0)
  end
  return L4_69
end
L0_0.FadeInScreen = L1_1
L0_0 = EventGraphics
function L1_1(A0_70, A1_71)
  System.FadeScreen(A0_70, false, A1_71, 0, 0, 0)
  while not System.IsCompletedFadeGraphic(A0_70) do
    coroutine.yield(0)
  end
end
L0_0.FadeOutScreen = L1_1
L0_0 = EventGraphics
function L1_1()
  local L0_72
  L0_72 = System
  L0_72 = L0_72.FadeTelopScreen
  L0_72 = L0_72(true)
  while not System.IsCompletedFadeGraphic(L0_72) do
    coroutine.yield(0)
  end
end
L0_0.FadeInTelopScreen = L1_1
L0_0 = EventGraphics
function L1_1()
  local L0_73
  L0_73 = System
  L0_73 = L0_73.FadeTelopScreen
  L0_73 = L0_73(false)
  while not System.IsCompletedFadeGraphic(L0_73) do
    coroutine.yield(0)
  end
end
L0_0.FadeOutTelopScreen = L1_1
L0_0 = EventGraphics
function L1_1(A0_74)
  System.ShakeGraphic(A0_74, true)
end
L0_0.StartShake = L1_1
L0_0 = EventGraphics
function L1_1(A0_75)
  System.ShakeGraphic(A0_75, false)
end
L0_0.StopShake = L1_1
L0_0 = EventGraphics
function L1_1(A0_76, A1_77, A2_78, A3_79, ...)
  local L5_81, L6_82, L7_83, L8_84, L9_85
  L4_80 = 1
  L9_85 = ...
  if L5_81 >= 1 then
    L9_85 = ...
    L4_80 = L5_81
  end
  for L8_84 = 1, L4_80 do
    L9_85 = System
    L9_85 = L9_85.MoveGraphic
    L9_85 = L9_85(A0_76, A1_77, A2_78, A3_79)
    Utility.WaitProcedure(L9_85)
    Utility.Wait(0.1)
  end
end
L0_0.Move = L1_1
L0_0 = EventGraphics
function L1_1(A0_86, A1_87, A2_88, ...)
  local L5_90, L6_91, L7_92
  L4_89 = System
  L4_89 = L4_89.StartSlideShow
  L5_90 = A0_86
  L6_91 = A1_87
  L7_92 = A2_88
  L4_89(L5_90, L6_91, L7_92, ...)
end
L0_0.StartSlideShow = L1_1
L0_0 = EventGraphics
function L1_1()
  local L0_93
  L0_93 = System
  L0_93 = L0_93.EndSlideShow
  L0_93 = L0_93()
  Utility.WaitProcedure(L0_93)
end
L0_0.EndSlideShow = L1_1
L0_0 = {}
BGM = L0_0
L0_0 = BGM
function L1_1(A0_94, ...)
  L1_95 = 0.8
  if select("#", ...) >= 1 then
    L1_95 = select(1, ...)
  end
  System.PlayBGM(A0_94, L1_95)
end
L0_0.Play = L1_1
L0_0 = BGM
function L1_1(...)
  L1_96 = System
  L1_96 = L1_96.StopBGM
  L1_96(...)
end
L0_0.Stop = L1_1
L0_0 = BGM
function L1_1(A0_97)
  System.EnableCrossfade(A0_97)
end
L0_0.EnableCrossfade = L1_1
L0_0 = BGM
function L1_1()
  return System.GetCurrentBgmNo()
end
L0_0.GetCurrentBgmNo = L1_1
L0_0 = {}
Voice = L0_0
L0_0 = Voice
function L1_1(A0_98, ...)
  local L2_100
  L1_99 = false
  L2_100 = false
  if select("#", ...) >= 1 then
    L1_99 = select(1, ...)
  end
  if select("#", ...) >= 2 then
    L2_100 = select(2, ...)
  end
  return System.PlayVoice(A0_98, L1_99, L2_100)
end
L0_0.Play = L1_1
L0_0 = Voice
function L1_1(A0_101, ...)
  L1_102 = 0.2
  if select("#", ...) >= 1 then
    L1_102 = select(1, ...)
  end
  System.StopVoice(A0_101, L1_102)
end
L0_0.Stop = L1_1
L0_0 = Voice
function L1_1()
  System.StopAllVoice()
end
L0_0.StopAll = L1_1
L0_0 = Voice
function L1_1(A0_103, A1_104)
  System.PauseVoice(A0_103, A1_104)
end
L0_0.Pause = L1_1
L0_0 = Voice
function L1_1(A0_105)
  return System.IsPrepareVoice(A0_105)
end
L0_0.IsPrepare = L1_1
L0_0 = Voice
function L1_1(A0_106)
  return System.IsPlayingVoice(A0_106)
end
L0_0.IsPlaying = L1_1
L0_0 = {}
SE = L0_0
L0_0 = SE
function L1_1(A0_107, ...)
  local L2_109, L3_110
  L1_108 = false
  L2_109 = false
  L3_110 = false
  if select("#", ...) >= 1 then
    L1_108 = select(1, ...)
  end
  if select("#", ...) >= 2 then
    L2_109 = select(2, ...)
  end
  if select("#", ...) >= 3 then
    L3_110 = select(3, ...)
  end
  return System.PlaySE(A0_107, L1_108, L2_109, L3_110)
end
L0_0.Play = L1_1
L0_0 = SE
function L1_1(A0_111, ...)
  L1_112 = 0.2
  if select("#", ...) >= 1 then
    L1_112 = select(1, ...)
  end
  System.StopSE(A0_111, L1_112)
end
L0_0.Stop = L1_1
L0_0 = SE
function L1_1()
  System.StopAllSE()
end
L0_0.StopAll = L1_1
L0_0 = SE
function L1_1(A0_113, A1_114)
  System.PauseSE(A0_113, A1_114)
end
L0_0.Pause = L1_1
L0_0 = SE
function L1_1(A0_115)
  return System.IsPrepareSE(A0_115)
end
L0_0.IsPrepare = L1_1
L0_0 = SE
function L1_1(A0_116)
  return System.IsReadySE(A0_116)
end
L0_0.IsReady = L1_1
L0_0 = SE
function L1_1(A0_117)
  return System.IsPlayingSE(A0_117)
end
L0_0.IsPlaying = L1_1
L0_0 = SE
function L1_1(A0_118)
  System.ChangeSeVolume(A0_118)
end
L0_0.ChangeVolume = L1_1
L0_0 = {}
LanguageType = L0_0
L0_0 = LanguageType
L0_0.Japanese = 0
L0_0 = LanguageType
L0_0.Hongkong = 1
L0_0 = LanguageType
L0_0.Taiwan = 2
L0_0 = LanguageType
L0_0.English = 3
L0_0 = LanguageType
L0_0.Chinese = 4
L0_0 = LanguageType
L0_0.Korean = 5
L0_0 = {}
WindowColor = L0_0
L0_0 = WindowColor
L0_0.Player = 0
L0_0 = WindowColor
L0_0.Friend = 1
L0_0 = WindowColor
L0_0.NPC = 2
L0_0 = WindowColor
L0_0.Enemy1 = 3
L0_0 = WindowColor
L0_0.Enemy2 = 4
L0_0 = WindowColor
L0_0.Secret = 5
L0_0 = WindowColor
L0_0.Master = 6
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
