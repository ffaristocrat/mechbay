local L1_1
L0_0 = {}
BGM = L0_0
L0_0 = BGM
function L1_1(A0_2, ...)
  L1_3 = 0.8
  if select("#", ...) >= 1 then
    L1_3 = select(1, ...)
  end
  System.PlayBGM(A0_2, L1_3)
end
L0_0.Play = L1_1
L0_0 = BGM
function L1_1(A0_4)
  System.PlayBGMIgnoreEventSkip(A0_4, 0.8)
end
L0_0.PlayBGMIgnoreEventSkip = L1_1
L0_0 = BGM
function L1_1(...)
  L0_5 = 0.8
  if select("#", ...) >= 1 then
    L0_5 = select(1, ...)
  end
  System.StopBGM(L0_5)
end
L0_0.Stop = L1_1
L0_0 = BGM
function L1_1(A0_6)
  System.EnableCrossfade(A0_6)
end
L0_0.EnableCrossfade = L1_1
L0_0 = BGM
function L1_1(A0_7)
  return System.GetMapBgmNo(A0_7)
end
L0_0.GetMapBgmNo = L1_1
L0_0 = BGM
function L1_1(A0_8, A1_9)
  System.SetMapBgmNo(A0_8, A1_9)
end
L0_0.SetMapBgmNo = L1_1
L0_0 = BGM
function L1_1(A0_10)
  System.SetNoChangeBGM(A0_10)
end
L0_0.SetNoChange = L1_1
L0_0 = BGM
function L1_1()
  return System.GetCurrentBgmNo()
end
L0_0.GetCurrentBgmNo = L1_1
L0_0 = {}
Voice = L0_0
L0_0 = Voice
function L1_1(A0_11, ...)
  local L2_13
  L1_12 = false
  L2_13 = false
  if select("#", ...) >= 1 then
    L1_12 = select(1, ...)
  end
  if select("#", ...) >= 2 then
    L2_13 = select(2, ...)
  end
  return System.PlayVoice(A0_11, L1_12, L2_13)
end
L0_0.Play = L1_1
L0_0 = Voice
function L1_1(A0_14)
  return System.PlayVoiceFromPath(A0_14)
end
L0_0.PlayFromPath = L1_1
L0_0 = Voice
function L1_1(A0_15, ...)
  L1_16 = 0.2
  if select("#", ...) >= 1 then
    L1_16 = select(1, ...)
  end
  System.StopVoice(A0_15, L1_16)
end
L0_0.Stop = L1_1
L0_0 = Voice
function L1_1()
  System.StopAllVoice()
end
L0_0.StopAll = L1_1
L0_0 = Voice
function L1_1(A0_17, A1_18)
  System.PauseVoice(A0_17, A1_18)
end
L0_0.Pause = L1_1
L0_0 = Voice
function L1_1(A0_19)
  return System.IsPrepareVoice(A0_19)
end
L0_0.IsPrepare = L1_1
L0_0 = Voice
function L1_1(A0_20)
  return System.IsPlayingVoice(A0_20)
end
L0_0.IsPlaying = L1_1
L0_0 = {}
SE = L0_0
L0_0 = SE
function L1_1(A0_21, ...)
  local L2_23, L3_24, L4_25
  L1_22 = false
  L2_23 = false
  L3_24 = false
  L4_25 = select
  L4_25 = L4_25("#", ...)
  if L4_25 >= 1 then
    L4_25 = select
    L4_25 = L4_25(1, ...)
    L1_22 = L4_25
  end
  L4_25 = select
  L4_25 = L4_25("#", ...)
  if L4_25 >= 2 then
    L4_25 = select
    L4_25 = L4_25(2, ...)
    L2_23 = L4_25
  end
  L4_25 = select
  L4_25 = L4_25("#", ...)
  if L4_25 >= 3 then
    L4_25 = select
    L4_25 = L4_25(3, ...)
    L3_24 = L4_25
  end
  L4_25 = System
  L4_25 = L4_25.PlaySE
  L4_25 = L4_25(A0_21, L1_22, L2_23, L3_24)
  while not SE.IsReady(L4_25) do
    Utility.BreakScript()
  end
  return L4_25
end
L0_0.Play = L1_1
L0_0 = SE
function L1_1(A0_26, ...)
  L1_27 = 0.2
  if select("#", ...) >= 1 then
    L1_27 = select(1, ...)
  end
  System.StopSE(A0_26, L1_27)
end
L0_0.Stop = L1_1
L0_0 = SE
function L1_1()
  System.StopAllSE()
end
L0_0.StopAll = L1_1
L0_0 = SE
function L1_1(A0_28, A1_29)
  System.PauseSE(A0_28, A1_29)
end
L0_0.Pause = L1_1
L0_0 = SE
function L1_1(A0_30)
  return System.IsPrepareSE(A0_30)
end
L0_0.IsPrepare = L1_1
L0_0 = SE
function L1_1(A0_31)
  return System.IsReadySE(A0_31)
end
L0_0.IsReady = L1_1
L0_0 = SE
function L1_1(A0_32)
  return System.IsPlayingSE(A0_32)
end
L0_0.IsPlaying = L1_1
L0_0 = SE
function L1_1(A0_33)
  System.ChangeSeVolume(A0_33)
end
L0_0.ChangeVolume = L1_1
