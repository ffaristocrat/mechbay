Message = {}

function Message.ShowMessage(text, unitId, ...)
  while not System.IsReadyMessageWindow() do
    coroutine.yield(0)
  end

  local unit = System.GetUnit(unitId)

  local moveCursor = true
  if select("#", ...) >= 1 then
    moveCursor = select(1, ...)
  end

  Cursor.MoveToUnit(unit, 0, moveCursor, false)
  Utility.Wait(0.05)
  Cursor.Visible(true)
  System.ShowMessage(text, unit, ...)

  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
end

function Message.ShowMessageWithCameraZoom(text, unitId, ...)
  while not System.IsReadyMessageWindow() do
    coroutine.yield(0)
  end

  local unit = System.GetUnit(unitId)

  local moveCursor = true
  if select("#", ...) >= 1 then
    moveCursor = select(1, ...)
  end

  Cursor.MoveToUnit(unit, 0, moveCursor, false)
  Utility.Wait(0.05)
  Cursor.Visible(true)
  Camera.ZoomIn()
  System.ShowMessage(text, unit, ...)

  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
end

function Message.ShowMessageWithoutCharacter(text, ...)
  while not System.IsReadyMessageWindow() do
    coroutine.yield(0)
  end

  local voiceId = ""
  if select("#", ...) >= 1 then
    voiceId = select(1, ...)
  end

  System.ShowMessage(text, -1, false, voiceId)

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
  System.ShowMessageOnline(text, charId, false)
  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
end

function Message.ShowMessageVoiceOnly(text, charId, ...)
  while not System.IsReadyMessageWindow() do
    coroutine.yield(0)
  end
  System.ShowMessageOnline(text, charId, true)
  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
end

function Message.ShowScoutMessage(unitId, scoutMessage)
  while not System.IsReadyMessageWindow() do
    coroutine.yield(0)
  end

  local unit = System.GetUnit(unitId)
  Cursor.MoveToUnit(unit, 0, true, false)
  Utility.Wait(0.05)
  Camera.ZoomIn()
  Cursor.Visible(true)
  System.ShowScoutMessage(unitId, scoutMessage) -- Note: A0_22 is unitId

  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
end

-- This function was duplicated in the original file.
--[[
function Message.ShowMessageWithoutCharacter(text)
  while not System.IsReadyMessageWindow() do
    coroutine.yield(0)
  end
  System.ShowMessage(text, -1, false, "")
  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
end
--]]

function Message.ShowMessageWithoutKeyWait(text, charId, ...)
  while not System.IsReadyMessageWindow() do
    coroutine.yield(0)
  end
  System.ShowMessageWithCharacterId(text, charId)
end

function Message.IsShowNextMessage()
  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
end

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

function Message.CloseWindow(...)
  local zoomOut = true
  if select("#", ...) >= 1 then
    zoomOut = select(1, ...)
  end

  System.CloseMessageWindow()
  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end

  if zoomOut then
    Camera.ZoomOut()
  end
  Cursor.Visible(false)
end

function Message.CloseWindowRight(...)
  System.CloseMessageWindowRight()
  Message.CloseWindow(...)
end

function Message.CloseWindowFront()
  System.CloseMessageWindowFront()
  while not System.IsCloseMessageWindowFront() do
    coroutine.yield(0)
  end
end

function Message.CloseTelopWindow()
  Message.CloseWindow(false)
end

---
-- Enums
---

WindowColor = {
  Player = 0,
  Friend = 1,
  NPC = 2,
  Enemy1 = 3,
  Enemy2 = 4,
  Secret = 5,
  Master = 6
}

ScoutMessageType = {
  Out = 0,
  Ws = 1,
  Master = 2,
  Warning = 3
}