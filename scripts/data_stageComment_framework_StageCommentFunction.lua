Utility = {}

function Utility.Wait(duration)
  local id = System.Wait(duration)
  while System.FindProcedure(id) do
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

function Utility.CheckTrophy(trophyId)
  System.CheckTrophy(trophyId)
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

function Utility.DebugPrint(message)
  return System.DebugPrint(message)
end

function Utility.GetElapsedTime()
  return System.GetElapsedTime()
end

---
-- Message
---

Message = {}

function Message.ShowTelop(text, ...)
  while not System.IsReadyTelop() do
    coroutine.yield(0)
  end
  System.ShowTelop(text, ...)
  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
end

function Message.ShowTelopCenter(text, ...)
  while not System.IsReadyTelop() do
    coroutine.yield(0)
  end
  System.ShowTelopCenter(text, ...)
  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
end

function Message.ShowTelopWithoutKeyWait(text, duration, ...)
  while not System.IsReadyTelop() do
    coroutine.yield(0)
  end
  System.ShowTelopWithoutKeyWait(text, duration, ...)
  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
end

function Message.ShowTelopWindow(text, ...)
  while not System.IsReadyTelopWindow() do
    coroutine.yield(0)
  end
  System.ShowTelopWindow(text, ...)
  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
end

function Message.ShowMessageWithCharacterId(text, charId, ...)
  while not System.IsReadyMessageWindow() do
    coroutine.yield(0)
  end
  System.ShowMessageWithCharacterId(text, charId, ...)
  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
end

function Message.ShowTwoMessage(text1, charId1, text2, charId2)
  while not System.IsReadyTwoMessageWindow() do
    coroutine.yield(0)
  end
  System.ShowTwoMessage(text1, charId1, text2, charId2)
  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
end

function Message.ShowMessageOnline(text, charId, ...)
  while not System.IsReadyMessageWindow() do
    coroutine.yield(0)
  end
  System.ShowMessageOnline(text, charId, false) -- 'false' is hardcoded in original
  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
end

function Message.ShowMessageVoiceOnly(text, charId, ...)
  while not System.IsReadyMessageWindow() do
    coroutine.yield(0)
  end
  System.ShowMessageOnline(text, charId, true) -- 'true' is hardcoded in original
  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
end

function Message.ShowMessageWithoutKeyWait(text, charId, ...)
  while not System.IsReadyMessageWindow() do
    coroutine.yield(0)
  end
  System.ShowMessageWithCharacterId(text, charId) -- '...' is passed but not used in original
end

function Message.IsShowNextMessage()
  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
end

function Message.CloseWindow()
  System.CloseMessageWindow()
  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
end

function Message.CloseWindowRight()
  System.CloseMessageWindowRight()
  Message.CloseWindow()
end

function Message.CloseWindowFront()
  System.CloseMessageWindowFront()
  while not System.IsCloseMessageWindowFront() do
    coroutine.yield(0)
  end
end

function Message.CloseTelopWindow()
  Message.CloseWindow()
end

---
-- SSA (Special Screen Animation)
---

SSA = {}

function SSA.CreateSSA(ssaId)
  local ssaHandle = System.CreateSSA(ssaId)
  while not System.IsReadySSA(ssaHandle) do
    coroutine.yield(0)
  end
  return ssaHandle
end

function SSA.Loop(ssaHandle, loop)
  System.LoopSSA(ssaHandle, loop)
end

function SSA.Visible(ssaHandle, visible)
  System.VisibleSSA(ssaHandle, visible)
end

function SSA.IsPlaying(ssaHandle)
  return System.IsPlayingSSA(ssaHandle)
end

function SSA.CurrentTime(ssaHandle)
  return System.CurrentTimeSSA(ssaHandle)
end

function SSA.Stop(ssaHandle)
  System.StopSSA(ssaHandle)
end

function SSA.Pause(ssaHandle, pause)
  System.PauseSSA(ssaHandle, pause)
end

function SSA.Priority(ssaHandle, priority)
  System.PrioritySSA(ssaHandle, priority)
end

function SSA.RemoveLoopPoint(ssaHandle)
  while not System.RemoveLoopPoint(ssaHandle) do
    Utility.BreakScript()
  end
end

function SSA.FlipVertical(ssaHandle, flip)
  System.FlipVerticalSSA(ssaHandle, flip)
end

function SSA.FlipHorizontal(ssaHandle, flip)
  System.FlipHorizontalSSA(ssaHandle, flip)
end

function SSA.SetColor(ssaHandle, r, g, b, a)
  System.SetColorSSA(ssaHandle, r, g, b, a)
end

function SSA.Fade(ssaHandle, duration, fadeIn)
  local elapsed = 0
  while duration > elapsed do
    local alpha = elapsed / duration
    if not fadeIn then
      alpha = 1 - alpha
    end
    SSA.SetColor(ssaHandle, 1, 1, 1, alpha)
    elapsed = elapsed + Utility.GetElapsedTime()
    Utility.BreakScript()
  end
  -- Ensure final state
  SSA.SetColor(ssaHandle, 1, 1, 1, fadeIn and 1 or 0)
end

---
-- EventGraphics
---

EventGraphics = {}

function EventGraphics.Create(graphicId, priority)
  return System.CreateGraphic(graphicId, priority)
end

function EventGraphics.FadeIn(graphicHandle, ...)
  local fadeTime = EventGraphics.DefaultFadeTime
  if select("#", ...) >= 1 then
    fadeTime = select(1, ...)
  end
  
  System.FadeGraphic(graphicHandle, fadeTime, true)
  
  local wait = true
  if select("#", ...) >= 2 then
    wait = select(2, ...)
  end
  
  if wait then
    while not System.IsCompletedFadeGraphic(graphicHandle) do
      coroutine.yield(0)
    end
  end
end

function EventGraphics.FadeOut(graphicHandle, ...)
  local fadeTime = EventGraphics.DefaultFadeTime
  if select("#", ...) >= 1 then
    fadeTime = select(1, ...)
  end
  
  System.FadeGraphic(graphicHandle, fadeTime, false)
  
  local wait = true
  if select("#", ...) >= 2 then
    wait = select(2, ...)
  end
  
  if wait then
    while not System.IsCompletedFadeGraphic(graphicHandle) do
      coroutine.yield(0)
    end
  end
end

function EventGraphics.IsReady(graphicHandle)
  return System.IsReadyGraphic(graphicHandle)
end

function EventGraphics.IsCompletedFade(graphicHandle)
  return System.IsCompletedFadeGraphic(graphicHandle)
end

function EventGraphics.SetColor(graphicHandle, r, g, b)
  return System.SetGraphicColor(graphicHandle, r, g, b)
end

function EventGraphics.FadeInScreen(duration, r, g, b)
  local fadeHandle = System.FadeScreen(0, true, duration, r, g, b)
  while not System.IsCompletedFadeGraphic(fadeHandle) do
    coroutine.yield(0)
  end
  return fadeHandle
end

function EventGraphics.FadeOutScreen(fadeHandle, duration)
  System.FadeScreen(fadeHandle, false, duration, 0, 0, 0)
  while not System.IsCompletedFadeGraphic(fadeHandle) do
    coroutine.yield(0)
  end
end

function EventGraphics.FadeInTelopScreen()
  local fadeHandle = System.FadeTelopScreen(true)
  while not System.IsCompletedFadeGraphic(fadeHandle) do
    coroutine.yield(0)
  end
end

function EventGraphics.FadeOutTelopScreen()
  local fadeHandle = System.FadeTelopScreen(false)
  while not System.IsCompletedFadeGraphic(fadeHandle) do
    coroutine.yield(0)
  end
end

function EventGraphics.StartShake(graphicHandle)
  System.ShakeGraphic(graphicHandle, true)
end

function EventGraphics.StopShake(graphicHandle)
  System.ShakeGraphic(graphicHandle, false)
end

function EventGraphics.Move(graphicHandle, x, y, duration, ...)
  local loopCount = 1
  if select("#", ...) >= 1 then
    loopCount = select(1, ...) -- Decompiler likely confused this
  end
  
  for i = 1, loopCount do
    local proc = System.MoveGraphic(graphicHandle, x, y, duration)
    Utility.WaitProcedure(proc)
    Utility.Wait(0.1)
  end
end

function EventGraphics.StartSlideShow(arg1, arg2, arg3, ...)
  System.StartSlideShow(arg1, arg2, arg3, ...)
end

function EventGraphics.EndSlideShow()
  local proc = System.EndSlideShow()
  Utility.WaitProcedure(proc)
end

---
-- BGM
---

BGM = {}

function BGM.Play(bgmId, ...)
  local volume = 0.8
  if select("#", ...) >= 1 then
    volume = select(1, ...)
  end
  System.PlayBGM(bgmId, volume)
end

function BGM.Stop(...)
  System.StopBGM(...)
end

function BGM.EnableCrossfade(enable)
  System.EnableCrossfade(enable)
end

function BGM.GetCurrentBgmNo()
  return System.GetCurrentBgmNo()
end

---
-- Voice
---

Voice = {}

function Voice.Play(voiceId, ...)
  local arg1 = false
  local arg2 = false
  if select("#", ...) >= 1 then
    arg1 = select(1, ...)
  end
  if select("#", ...) >= 2 then
    arg2 = select(2, ...)
  end
  return System.PlayVoice(voiceId, arg1, arg2)
end

function Voice.Stop(voiceHandle, ...)
  local fadeTime = 0.2
  if select("#", ...) >= 1 then
    fadeTime = select(1, ...)
  end
  System.StopVoice(voiceHandle, fadeTime)
end

function Voice.StopAll()
  System.StopAllVoice()
end

function Voice.Pause(voiceHandle, pause)
  System.PauseVoice(voiceHandle, pause)
end

function Voice.IsPrepare(voiceId)
  return System.IsPrepareVoice(voiceId)
end

function Voice.IsPlaying(voiceHandle)
  return System.IsPlayingVoice(voiceHandle)
end

---
-- SE (Sound Effect)
---

SE = {}

function SE.Play(seId, ...)
  local arg1 = false
  local arg2 = false
  local arg3 = false
  if select("#", ...) >= 1 then
    arg1 = select(1, ...)
  end
  if select("#", ...) >= 2 then
    arg2 = select(2, ...)
  end
  if select("#", ...) >= 3 then
    arg3 = select(3, ...)
  end
  return System.PlaySE(seId, arg1, arg2, arg3)
end

function SE.Stop(seHandle, ...)
  local fadeTime = 0.2
  if select("#", ...) >= 1 then
    fadeTime = select(1, ...)
  end
  System.StopSE(seHandle, fadeTime)
end

function SE.StopAll()
  System.StopAllSE()
end

function SE.Pause(seHandle, pause)
  System.PauseSE(seHandle, pause)
end

function SE.IsPrepare(seId)
  return System.IsPrepareSE(seId)
end

function SE.IsReady(seHandle)
  return System.IsReadySE(seHandle)
end

function SE.IsPlaying(seHandle)
  return System.IsPlayingSE(seHandle)
end

function SE.ChangeVolume(volume)
  System.ChangeSeVolume(volume)
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

WindowColor = {
  Player = 0,
  Friend = 1,
  NPC = 2,
  Enemy1 = 3,
  Enemy2 = 4,
  Secret = 5,
  Master = 6
}

Priority2D = {
  MapFade = 5000,
  EventGraphic = 7000,
  MessageWindow = 10000,
  SSA = 50000
}