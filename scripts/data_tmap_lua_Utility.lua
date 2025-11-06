local L1_1
L0_0 = {}
Utility = L0_0
L0_0 = Utility
function L1_1(A0_2)
  local L1_3
  L1_3 = System
  L1_3 = L1_3.Wait
  L1_3 = L1_3(A0_2)
  Utility.WaitProcedure(L1_3)
end
L0_0.Wait = L1_1
L0_0 = Utility
function L1_1()
  while System.WaitAllAsyncProcedures() do
    coroutine.yield(0)
  end
end
L0_0.WaitAllAsyncProcedures = L1_1
L0_0 = Utility
function L1_1()
  coroutine.yield(0)
end
L0_0.BreakScript = L1_1
L0_0 = Utility
function L1_1(A0_4)
  while System.FindProcedure(A0_4) do
    coroutine.yield(0)
  end
end
L0_0.WaitProcedure = L1_1
L0_0 = Utility
function L1_1()
  return System.IsEventSkip()
end
L0_0.IsEventSkip = L1_1
L0_0 = Utility
function L1_1()
  System.EndEventSkip()
end
L0_0.EndEventSkip = L1_1
L0_0 = Utility
function L1_1(A0_5)
  System.EnableEventSkip(A0_5)
end
L0_0.EnableEventSkip = L1_1
L0_0 = Utility
function L1_1()
  return System.IsShowTutorial()
end
L0_0.IsShowTutorial = L1_1
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
function L1_1()
  return System.GetRandomValue()
end
L0_0.GetRandomValue = L1_1
L0_0 = Utility
function L1_1(A0_6)
  return System.DebugPrint(A0_6)
end
L0_0.DebugPrint = L1_1
L0_0 = Utility
function L1_1()
  return System.GetElapsedTime()
end
L0_0.GetElapsedTime = L1_1
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
