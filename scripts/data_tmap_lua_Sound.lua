BGM = {}

function BGM.Play(bgmId, ...)
  local volume = 0.8
  if select("#", ...) >= 1 then
    volume = select(1, ...)
  end
  System.PlayBGM(bgmId, volume)
end

function BGM.PlayBGMIgnoreEventSkip(bgmId)
  System.PlayBGMIgnoreEventSkip(bgmId, 0.8)
end

function BGM.Stop(...)
  local fadeTime = 0.8
  if select("#", ...) >= 1 then
    fadeTime = select(1, ...)
  end
  System.StopBGM(fadeTime)
end

function BGM.EnableCrossfade(enable)
  System.EnableCrossfade(enable)
end

function BGM.GetMapBgmNo(mapIndex)
  return System.GetMapBgmNo(mapIndex)
end

function BGM.SetMapBgmNo(mapIndex, bgmId)
  System.SetMapBgmNo(mapIndex, bgmId)
end

function BGM.SetNoChange(noChange)
  System.SetNoChangeBGM(noChange)
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

function Voice.PlayFromPath(path)
  return System.PlayVoiceFromPath(path)
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
  
  local seHandle = System.PlaySE(seId, arg1, arg2, arg3)
  
  -- Wait until the SE is ready
  while not SE.IsReady(seHandle) do
    Utility.BreakScript()
  end
  return seHandle
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