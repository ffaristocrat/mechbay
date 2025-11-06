SSA = {}

function SSA.CreateSSA(ssaId, ...)
  local arg1 = false -- 'not ready'
  if select("#", ...) >= 1 then
    arg1 = select(1, ...)
  end
  
  local arg2 = true -- 'can skip'
  if select("#", ...) >= 2 then
    arg2 = select(2, ...)
  end
  
  local ssaHandle = System.CreateSSA(ssaId, arg1, arg2)
  
  while not System.IsReadySSA(ssaHandle) do
    coroutine.yield(0)
  end
  
  if select("#", ...) >= 3 then
    SSA.SetSSAIndex(ssaHandle, select(3, ...))
  end
  
  return ssaHandle
end

function SSA.CreateSSAonUnit(ssaId, unitId, ...)
  local arg1 = false -- 'not ready'
  if select("#", ...) >= 1 then
    arg1 = select(1, ...)
  end
  
  local arg2 = true -- 'can skip'
  if select("#", ...) >= 2 then
    arg2 = select(2, ...)
  end
  
  local unit = System.GetUnit(unitId)
  local ssaHandle = System.CreateSSAonUnit(ssaId, unit, arg1, arg2)
  
  while not System.IsReadySSA(ssaHandle) do
    coroutine.yield(0)
  end
  
  if select("#", ...) >= 3 then
    SSA.SetSSAIndex(ssaHandle, select(3, ...))
  end
  
  return ssaHandle
end

function SSA.CreateSSANotReady(ssaId)
  return System.CreateSSA(ssaId, true, true)
end

function SSA.CreateSSAonUnitNotReady(ssaId, unitId)
  local unit = System.GetUnit(unitId)
  return System.CreateSSAonUnit(ssaId, unit, true, true)
end

function SSA.Loop(ssaHandle, loop)
  System.LoopSSA(ssaHandle, loop)
end

function SSA.Scale(ssaHandle, scale)
  System.ScaleSSA(ssaHandle, scale)
end

function SSA.Position(ssaHandle, x, y)
  System.PositionSSA(ssaHandle, x, y)
end

function SSA.CellPosition(ssaHandle, cellX, cellY)
  System.PositionSSA(ssaHandle, (cellX + 0.5) * Grid.Size(), (cellY + 0.5) * Grid.Size())
end

function SSA.Angle(ssaHandle, angle)
  System.AngleSSA(ssaHandle, angle)
end

function SSA.Visible(ssaHandle, visible)
  System.VisibleSSA(ssaHandle, visible)
end

function SSA.CanSkip(ssaHandle, canSkip)
  System.CanSkipSSA(ssaHandle, canSkip)
end

function SSA.IsPlaying(ssaHandle)
  return System.IsPlayingSSA(ssaHandle)
end

function SSA.CurrentTime(ssaHandle)
  return System.CurrentTimeSSA(ssaHandle)
end

function SSA.Move(ssaHandle, x, y, duration)
  System.MoveSSA(ssaHandle, x, y, duration)
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

function SSA.SetSSAIndex(ssaHandle, index)
  System.SetSSAIndex(ssaHandle, index)
end

function SSA.KomaPriority(ssaHandle, unitId)
  local unit = System.GetUnit(unitId)
  System.KomaPrioritySSA(ssaHandle, unit)
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

function SSA.MultiEffectAroundUnit(effectId, unitId, range, interval, duration)
  local unit = System.GetUnit(unitId)
  return System.MultiEffectAroundUnit(effectId, unit, range, interval, duration)
end

function SSA.CreateMapWeaponEffect(unitId, weaponId, x, y)
  local unit = System.GetUnit(unitId)
  local ssaHandle = System.CreateMapWeaponEffect(unit, weaponId, x, y)
  while not System.IsReadySSA(ssaHandle) do
    coroutine.yield(0)
  end
  return ssaHandle
end

function SSA.GetDisappearTime(ssaHandle)
  return System.GetDisappearTime(ssaHandle)
end

function SSA.GetMoveRangeWithMapWeapon()
  return System.GetMoveRangeWithMapWeapon()
end

function SSA.MoveUnitWithMapWeapon(unitId, ssaHandle)
  local unit = System.GetUnit(unitId)
  return System.MoveUnitWithMapWeapon(unit, ssaHandle)
end

function SSA.GetKomaAnimeMapEffect(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetKomaAnimeMapEffect(unit)
end

function SSA.IsHaroMapWeapon(unitId)
  local unit = System.GetUnit(unitId)
  return System.IsHaroMapWeapon(unit)
end

function SSA.SetTerrainOffset(ssaHandle, unitId)
  local unit = System.GetUnit(unitId)
  System.SetTerrainOffsetSSA(ssaHandle, unit)
end

function SSA.IsUnitCenterEffect(unitId)
  local unit = System.GetUnit(unitId)
  return System.IsUnitCenterEffect(unit)
end

function SSA.PlaySpecialMapWeaponVoice(unitId, ssaHandle)
  local unit = System.GetUnit(unitId)
  return System.PlaySpecialMapWeaponVoice(unit, ssaHandle)
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
-- MapSSA
---

MapSSA = {}

function MapSSA.Position(ssaId, x, y)
  System.PositionMapSSA(ssaId, x, y)
end

function MapSSA.Visible(ssaId, visible)
  System.VisibleMapSSA(ssaId, visible)
end

---
-- EventGraphics
---

EventGraphics = {}

function EventGraphics.Create(graphicId, priority)
  local graphicHandle = System.CreateGraphic(graphicId, priority)
  while not EventGraphics.IsReady(graphicHandle) do
    Utility.BreakScript()
  end
  return graphicHandle
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

function EventGraphics.SetMaxAlpha(graphicHandle, alpha)
  return System.SetGraphicMaxAlpha(graphicHandle, alpha)
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

function EventGraphics.FadeInStartEventScreen(duration)
  local fadeHandle = System.FadeStartEventScreen(true, duration)
  while not System.IsCompletedFadeGraphic(fadeHandle) do
    coroutine.yield(0)
  end
end

function EventGraphics.FadeOutStartEventScreen(duration)
  local proc = System.FadeStartEventScreen(false, duration)
  Utility.WaitProcedure(proc)
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

function EventGraphics.SetRender3d(graphicHandle, render3d)
  System.SetGraphicRender3d(graphicHandle, render3d)
end

function EventGraphics.StartSlideShow(arg1, arg2, arg3, ...)
  System.StartSlideShow(arg1, arg2, arg3, ...)
end

function EventGraphics.EndSlideShow()
  local proc = System.EndSlideShow()
  Utility.WaitProcedure(proc)
end

function EventGraphics.FadeNowLoading(fadeIn)
  System.FadeNowLoading(fadeIn)
  if not fadeIn then
    while not System.IsIdleNowLoading() do
      coroutine.yield(0)
    end
  end
end

---
-- Movie
---

Movie = {}

function Movie.Create(movieId, movieType)
  return System.CreateMovie(movieId, movieType)
end

function Movie.IsReady()
  return System.IsReadyMovie()
end

function Movie.IsPlaying()
  return System.IsPlayingMovie()
end

function Movie.SetFadeColor(r, g, b)
  System.SetMovieFadeColor(r, g, b)
end

function Movie.AddProfile(movieId, galleryId)
  return System.AddProfileMovie(movieId, galleryId)
end

---
-- Camera
---

Camera = {}

function Camera.CameraLv(level, ...)
  local zoom = 1 + (3 - level) * 0.25
  local proc = System.CameraZoom(zoom, ...)
  Utility.WaitProcedure(proc)
end

function Camera.ZoomIn()
  local currentZoom = System.GetCameraZoom()
  local newZoom = currentZoom + 0.25
  local proc = System.CameraZoom(newZoom)
  Utility.WaitProcedure(proc)
end

function Camera.ZoomOut()
  local currentZoom = System.GetCameraZoom()
  local newZoom = currentZoom - 0.25
  local proc = System.CameraZoom(newZoom)
  Utility.WaitProcedure(proc)
end

function Camera.ZoomClear()
  local proc = System.CameraZoom(1)
  Utility.WaitProcedure(proc)
end

function Camera.StartShake()
  System.StartShakeCamera()
end

function Camera.EndShake()
  System.EndShakeCamera()
end

---
-- Constants
---

EventGraphics.DefaultFadeTime = 0.5

Priority2D = {
  MapFade = 5000,
  EventGraphic = 7000,
  MessageWindow = 10000,
  SSA = 50000
}

Priority3D = {
  Cursor = 50800,
  Marker = 150100,
  SSA = 150200,
  Explode = 202000
}

MovieType = {
  Battle = 0,
  Event = 1
}

MapWeaponEffectType = {
  Normal = 0,
  SelfExplosion = 1,
  Snipe = 2,
  SubRange = 3,
  Move = 4
}