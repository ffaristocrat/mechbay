local L1_1
L0_0 = {}
Message = L0_0
L0_0 = Message
function L1_1(A0_2, A1_3, ...)
  local L3_5
  while true do
    L2_4 = System
    L2_4 = L2_4.IsReadyMessageWindow
    L2_4 = L2_4()
    if not L2_4 then
      L2_4 = coroutine
      L2_4 = L2_4.yield
      L3_5 = 0
      L2_4(L3_5)
    end
  end
  L2_4 = System
  L2_4 = L2_4.GetUnit
  L3_5 = A1_3
  L2_4 = L2_4(L3_5)
  L3_5 = true
  if select("#", ...) >= 1 then
    L3_5 = select(1, ...)
  end
  Cursor.MoveToUnit(L2_4, 0, L3_5, false)
  Utility.Wait(0.05)
  Cursor.Visible(true)
  System.ShowMessage(A0_2, L2_4, ...)
  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
end
L0_0.ShowMessage = L1_1
L0_0 = Message
function L1_1(A0_6, A1_7, ...)
  local L3_9
  while true do
    L2_8 = System
    L2_8 = L2_8.IsReadyMessageWindow
    L2_8 = L2_8()
    if not L2_8 then
      L2_8 = coroutine
      L2_8 = L2_8.yield
      L3_9 = 0
      L2_8(L3_9)
    end
  end
  L2_8 = System
  L2_8 = L2_8.GetUnit
  L3_9 = A1_7
  L2_8 = L2_8(L3_9)
  L3_9 = true
  if select("#", ...) >= 1 then
    L3_9 = select(1, ...)
  end
  Cursor.MoveToUnit(L2_8, 0, L3_9, false)
  Utility.Wait(0.05)
  Cursor.Visible(true)
  Camera.ZoomIn()
  System.ShowMessage(A0_6, L2_8, ...)
  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
end
L0_0.ShowMessageWithCameraZoom = L1_1
L0_0 = Message
function L1_1(A0_10, ...)
  while true do
    L1_11 = System
    L1_11 = L1_11.IsReadyMessageWindow
    L1_11 = L1_11()
    if not L1_11 then
      L1_11 = coroutine
      L1_11 = L1_11.yield
      L1_11(0)
    end
  end
  L1_11 = ""
  if select("#", ...) >= 1 then
    L1_11 = select(1, ...)
  end
  System.ShowMessage(A0_10, -1, false, L1_11)
  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
end
L0_0.ShowMessageWithoutCharacter = L1_1
L0_0 = Message
function L1_1(A0_12, A1_13, ...)
  while not System.IsReadyMessageWindow() do
    coroutine.yield(0)
  end
  System.ShowMessageWithCharacterId(A0_12, A1_13)
  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
end
L0_0.ShowMessageWithCharacterId = L1_1
L0_0 = Message
function L1_1(A0_14, A1_15, A2_16, A3_17)
  while not System.IsReadyTwoMessageWindow() do
    coroutine.yield(0)
  end
  System.ShowTwoMessage(A0_14, A1_15, A2_16, A3_17)
  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
end
L0_0.ShowTwoMessage = L1_1
L0_0 = Message
function L1_1(A0_18, A1_19, ...)
  while not System.IsReadyMessageWindow() do
    coroutine.yield(0)
  end
  System.ShowMessageOnline(A0_18, A1_19, false)
  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
end
L0_0.ShowMessageOnline = L1_1
L0_0 = Message
function L1_1(A0_20, A1_21, ...)
  while not System.IsReadyMessageWindow() do
    coroutine.yield(0)
  end
  System.ShowMessageOnline(A0_20, A1_21, true)
  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
end
L0_0.ShowMessageVoiceOnly = L1_1
L0_0 = Message
function L1_1(A0_22, A1_23)
  local L2_24
  while true do
    L2_24 = System
    L2_24 = L2_24.IsReadyMessageWindow
    L2_24 = L2_24()
    if not L2_24 then
      L2_24 = coroutine
      L2_24 = L2_24.yield
      L2_24(0)
    end
  end
  L2_24 = System
  L2_24 = L2_24.GetUnit
  L2_24 = L2_24(A0_22)
  Cursor.MoveToUnit(L2_24, 0, true, false)
  Utility.Wait(0.05)
  Camera.ZoomIn()
  Cursor.Visible(true)
  System.ShowScoutMessage(A0_22, A1_23)
  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
end
L0_0.ShowScoutMessage = L1_1
L0_0 = Message
function L1_1(A0_25)
  while not System.IsReadyMessageWindow() do
    coroutine.yield(0)
  end
  System.ShowMessage(A0_25, -1, false, "")
  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
end
L0_0.ShowMessageWithoutCharacter = L1_1
L0_0 = Message
function L1_1(A0_26, A1_27, ...)
  while not System.IsReadyMessageWindow() do
    coroutine.yield(0)
  end
  System.ShowMessageWithCharacterId(A0_26, A1_27)
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
function L1_1(A0_28, ...)
  while not System.IsReadyTelop() do
    coroutine.yield(0)
  end
  System.ShowTelop(A0_28, ...)
  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
end
L0_0.ShowTelop = L1_1
L0_0 = Message
function L1_1(A0_29, ...)
  while not System.IsReadyTelop() do
    coroutine.yield(0)
  end
  System.ShowTelopCenter(A0_29, ...)
  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
end
L0_0.ShowTelopCenter = L1_1
L0_0 = Message
function L1_1(A0_30, A1_31, ...)
  while not System.IsReadyTelop() do
    coroutine.yield(0)
  end
  System.ShowTelopWithoutKeyWait(A0_30, A1_31, ...)
  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
end
L0_0.ShowTelopWithoutKeyWait = L1_1
L0_0 = Message
function L1_1(A0_32, ...)
  while not System.IsReadyTelopWindow() do
    coroutine.yield(0)
  end
  System.ShowTelopWindow(A0_32, ...)
  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
end
L0_0.ShowTelopWindow = L1_1
L0_0 = Message
function L1_1(...)
  L0_33 = true
  if select("#", ...) >= 1 then
    L0_33 = select(1, ...)
  end
  System.CloseMessageWindow()
  while not System.IsShowNextMessage() do
    coroutine.yield(0)
  end
  if L0_33 then
    Camera.ZoomOut()
  end
  Cursor.Visible(false)
end
L0_0.CloseWindow = L1_1
L0_0 = Message
function L1_1(...)
  System.CloseMessageWindowRight()
  Message.CloseWindow(...)
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
  Message.CloseWindow(false)
end
L0_0.CloseTelopWindow = L1_1
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
ScoutMessageType = L0_0
L0_0 = ScoutMessageType
L0_0.Out = 0
L0_0 = ScoutMessageType
L0_0.Ws = 1
L0_0 = ScoutMessageType
L0_0.Master = 2
L0_0 = ScoutMessageType
L0_0.Warning = 3
