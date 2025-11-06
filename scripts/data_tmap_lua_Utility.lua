Utility = {}

function Utility.Wait(duration)
  local procId = System.Wait(duration)
  Utility.WaitProcedure(procId)
end

function Utility.WaitAllAsyncProcedures()
  while System.WaitAllAsyncProcedures() do
    coroutine.yield(0)
  end
end

function Utility.BreakScript()
  coroutine.yield(0)
end

function Utility.WaitProcedure(procId)
  while System.FindProcedure(procId) do
    coroutine.yield(0)
  end
end

function Utility.IsEventSkip()
  return System.IsEventSkip()
end

function Utility.EndEventSkip()
  System.EndEventSkip()
end

function Utility.EnableEventSkip(enable)
  System.EnableEventSkip(enable)
end

function Utility.IsShowTutorial()
  return System.IsShowTutorial()
end

function Utility.IsSpecialSoundEdition()
  return System.IsSpecialSoundEdition()
end

function Utility.GetLanguageType()
  return System.GetLanguageType()
end

function Utility.GetScreenSize()
  return System.GetScreenSize()
end

function Utility.GetRandomValue()
  return System.GetRandomValue()
end

function Utility.DebugPrint(message)
  return System.DebugPrint(message)
end

function Utility.GetElapsedTime()
  return System.GetElapsedTime()
end

---
-- Enums
---

LanguageType = {
  Japanese = 0,
  Hongkong = 1,
  Taiwan = 2,
  English = 3,
  Chinese = 4,
  Korean = 5
}