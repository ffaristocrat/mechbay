function Startup()
  Utility.DebugPrint("[StageFramework.lua] Startup")
  math.randomseed(Utility.GetRandomValue())
  Grid.IsVisibleGridAndSquare(false)
  Cursor.Visible(false)
  Cursor.DisableScriptColor()
  BGM.EnableCrossfade(false)
  BGM.SetNoChange(false)
  Stage.SetOpenCondition(ConditionType.Event, 0, true)
  Stage.SetOpenCondition(ConditionType.Challenge, 0, true)

  Utility.DebugPrint("[StageFramework.lua] Configuration")
  Configuration()

  if not Utility.IsEventSkip() then
    EventGraphics.FadeNowLoading(false)
  end

  Utility.DebugPrint("[StageFramework.lua] StartEvent")
  StartEvent()

  Cursor.Visible(true)
  Grid.IsVisibleGridAndSquare(true)
  Camera.ZoomClear()
  System.StageStart()
end

function StartPhase(phase)
  PlayStageCommonBGM()
  OnStartPhase(phase)

  if Stage.IsGameOver() then
    GameOverEvent()
    System.GameOver()
    return
  end

  CheckEventCondition()
  Stage.CheckQuestAchieved()

  if Stage.IsGameOver() then
    GameOverEvent()
    System.GameOver()
    return
  end

  if Stage.IsStageClear() then
    StageClearEvent()
    System.StageClear()
    System.IsTriggeredEvent(false)
    return
  end
end

function BeforeEnd(arg)
  OnBeforeEnd()

  if Stage.IsGameOver() then
    GameOverEvent()
    System.GameOver()
    return
  end

  CheckEventCondition()

  if Stage.IsStageClear() then
    StageClearEvent()
    System.StageClear()
    System.IsTriggeredEvent(false) -- 'false' is inferred
    return
  end

  Utility.EndEventSkip()

  while Utility.IsShowTutorial() do
    Utility.BreakScript()
  end

  -- Check for HP warnings
  local allUnits = Unit.GetAllUnits()
  if allUnits then
    for _, unit in ipairs(allUnits) do
      local param = Unit.GetParameter(unit)
      if param.Hp > 0 and not Unit.IsInWarShip(unit) and not Unit.IsDoneWarningHp(unit) and Unit.IsValidPosition(unit) and 0 < Battle.GetDamage(unit) and Unit.GetWarningHpPercent(unit) / 100 > param.Hp / param.MaxHp then
        if Unit.HasStageWarningHp(unit) then
          OnWarningHp(unit)
        elseif Unit.IsPlayer(unit) and not Unit.IsSfs(unit) then
          CheckHpWarning(0, unit, 0, true)
        end
      end
    end
  end
end

function BeforeBattle()
  OnTalkBeforeBattle()
end

function AfterBattle()
  local deadUnits = Battle.DeadUnits()
  if deadUnits then
    for _, unit in ipairs(deadUnits) do
      if Unit.IsAlive(unit) then
        if Unit.HasDeadEvent(unit) then
          OnDiedEvent(unit)
        elseif Unit.IsPlayer(unit) and not Unit.IsSfs(unit) then
          OutEvent(0, unit, 0, OutEventType.Explosion, true)
        end
      end
    end
  end
end

function OutEvent(message, unitId, voiceId, outType, ...)
  Cursor.Visible(false)
  Cursor.MoveToUnit(unitId, 0, true)
  Utility.Wait(0.3)

  local ssaHandle = SSA.CreateSSAonUnit(900, unitId)
  SSA.Loop(ssaHandle, true)
  Cursor.Visible(true)
  Utility.Wait(0.4)

  local isScout = false
  if select("#", ...) >= 1 then
    isScout = select(1, ...)
  end

  if isScout then
    Message.ShowScoutMessage(unitId, false) -- 'false' for 'is warning'
    Message.CloseWindow()
    if Unit.IsWs(unitId) or Unit.IsMaster(unitId) then
      outType = OutEventType.Master
    end
  else
    Message.ShowMessageWithCameraZoom(message, unitId, voiceId)
    Message.CloseWindow()
  end

  SSA.Loop(ssaHandle, false)
  if outType == OutEventType.Disappear then
    Unit.Disappear(unitId)
  else
    Unit.Kill(unitId, outType == OutEventType.Master)
  end
  Utility.Wait(0.2)
end

function CheckHpWarning(message, unitId, voiceId, ...)
  local param = Unit.GetParameter(unitId)
  local warningPercent = Unit.GetWarningHpPercent(unitId) / 100
  local currentPercent = param.Hp / param.MaxHp

  if warningPercent > currentPercent then
    Cursor.MoveToUnit(unitId, 0, true)
    Utility.Wait(0.3)

    local proc = Unit.ShowWarningHp(unitId)
    Utility.WaitProcedure(proc)

    local isScout = false
    if select("#", ...) >= 1 then
      isScout = select(1, ...)
    end

    if isScout then
      Message.ShowScoutMessage(unitId, true) -- 'true' for 'is warning'
      Message.CloseWindow()
    else
      Message.ShowMessageWithCameraZoom(message, unitId, voiceId)
      Message.CloseWindow()
    end
  end
end

function BeforeEndWithoutBattleControl()
  Utility.DebugPrint("[StageFramework.lua] BeforeEndWithoutBattleControl")

  if Stage.IsGameOver() or Battle.IsDestroyGameOverUnitWithoutBattleControl() then
    GameOverEvent()
    System.GameOver()
    return
  end

  CheckEventCondition()

  if Stage.IsStageClear() then
    StageClearEvent()
    System.StageClear()
    System.IsTriggeredEvent(false)
    return
  end

  Utility.EndEventSkip()

  while Utility.IsShowTutorial() do
    Utility.BreakScript()
  end

  -- Check for HP warnings
  local allUnits = Unit.GetAllUnits()
  if allUnits then
    for _, unit in ipairs(allUnits) do
      local param = Unit.GetParameter(unit)
      if param.Hp > 0 and not Unit.IsInWarShip(unit) and not Unit.IsDoneWarningHp(unit) and Unit.IsValidPosition(unit) and Unit.GetWarningHpPercent(unit) / 100 > param.Hp / param.MaxHp then
        if Unit.HasStageWarningHp(unit) then
          OnWarningHp(unit)
        elseif Unit.IsPlayer(unit) and not Unit.IsSfs(unit) then
          CheckHpWarning(0, unit, 0, true)
        end
      end
    end
  end
end

function CheckEventCondition()
  if System.IsTriggeredEvent() then
    return
  end

  local challengeSuccess = false

  -- Check Event Condition
  if System.GetEventStatus() == ConditionState.Continue then
    local eventState = Stage.CheckCondition(ConditionType.Event)
    if eventState == ConditionState.Success then
      System.SetEventStatus(ConditionState.Success)
    elseif eventState == ConditionState.Failed then
      System.SetEventStatus(ConditionState.Failed)
    end
  end

  -- Check Challenge Condition
  if System.GetChallengeStatus() == ConditionState.Continue then
    local challengeState = Stage.CheckCondition(ConditionType.Challenge)
    if challengeState == ConditionState.Success then
      System.SetChallengeStatus(ConditionState.Success)
    elseif challengeState == ConditionState.Failed then
      System.SetChallengeStatus(ConditionState.Failed)
    end
  end

  -- Trigger Event
  if System.GetEventStatus() == ConditionState.Success then
    BGM.Stop()
    Cursor.Visible(false)
    Grid.IsVisibleGridAndSquare(false)

    local ssaId = 906
    if Stage.IsChallengeStage() then
      -- ssaId remains 906, original 'if' was a no-op
    end

    local ssaHandle = SSA.CreateSSA(ssaId)
    SSA.CanSkip(ssaHandle, true)
    Utility.WaitProcedure(ssaHandle)

    if System.GetChallengeStatus() == ConditionState.Success then
      challengeSuccess = true
    else
      System.SetChallengeStatus(ConditionState.Failed)
    end

    BreakEvent1()
    System.IsTriggeredEvent(true)
  end

  if challengeSuccess then
    if not Stage.IsEventBattle() then
      Utility.Wait(1)
      BGM.Stop()
      local bgmId = BGM.GetMapBgmNo(Stage.Phase())
      BGM.Play(bgmId)

      local ssaHandle = SSA.CreateSSA(903)
      SSA.CanSkip(ssaHandle, true)
      Utility.WaitProcedure(ssaHandle)

      ChallengeEvent()
      Stage.ShowTutorial(180)
    else
      if System.GetChallengeStatus() == ConditionState.Success then
        ChallengeEvent()
        System.IsTriggeredEvent(true)
      end
    end
  end

  if Utility.IsEventSkip() then
    local bgmId = BGM.GetMapBgmNo(Stage.Phase())
    BGM.PlayBGMIgnoreEventSkip(bgmId)
  end

  Cursor.Visible(true)
  Grid.IsVisibleGridAndSquare(true)

  if System.IsTriggeredEvent() then
    if not Stage.IsEventBattle() then
      Utility.EnableEventSkip(false)
      Utility.EndEventSkip()
      Stage.ShowVictoryCondition()
      Utility.EnableEventSkip(true)
    end
  end
end

function PlayStageCommonBGM()
  local bgmId = BGM.GetMapBgwNo(Stage.Phase())
  BGM.Play(bgmId)
end

function SaveScriptTable()
  System.SaveScriptTable(SaveTable)
  if AfterDataSave ~= nil then
    AfterDataSave()
  end
end

function LoadScriptTable()
  SaveTable = System.LoadScriptTable(SaveTable)
  if AfterDataLoad ~= nil then
    AfterDataLoad()
  end
end

function GetUniqueCharacterBgmNo()
  local bgmId = 0
  if UniqueCharacterBgmNo ~= nil then
    bgmId = UniqueCharacterBgmNo(Stage.Phase())
  end
  return bgmId
end

-- NOTE: The following functions were severely corrupted by the decompiler
-- and are likely non-functional or incorrect.

function MapWeaponEffect(cellX, cellY, effectType, ssaHandle)
  local attacker = Battle.MainAttacker()
  local pos = Unit.GetPosition(attacker)

  if effectType == MapWeaponEffectType.Snipe then
    if not SSA.IsUnitCenterEffect(attacker) then
      pos.X = cellX
      pos.Y = cellY
    end
  elseif effectType == MapWeaponEffectType.SubRange then
    -- This block was empty in the original
  end

  Cursor.SetPosition(pos.X, pos.Y, 0, false, false)
  PlayDragonVoice(attacker, ssaHandle) -- ssaHandle is used as weaponId?

  if effectType == MapWeaponEffectType.Move then
    if SSA.GetKomaAnimeMapEffect(attacker) then
      Unit.SetAnimation(attacker, KomaAnimationType.Move, true)
      Unit.SetHighPriority(attacker, true)
      local proc = SSA.MoveUnitWithMapWeapon(attacker, ssaHandle)
      Utility.WaitProcedure(proc)
      Unit.SetAnimation(attacker, KomaAnimationType.StandBy, true)
      Unit.SetHighPriority(attacker, false)
    else
      local moveRange = SSA.GetMoveRangeWithMapWeapon()
      local effects = {}
      for i = 1, #moveRange / 2 do
        local newHandle = SSA.CreateMapWeaponEffect(attacker, moveRange[2 * i - 1], moveRange[2 * i], ssaHandle)
        effects[i] = newHandle
      end
      -- ... Corrupt logic for pausing and handling effects ...
    end
  else
    -- ... Corrupt logic for various other effect types ...
  end
end

function DragonMapWeapon()
  local attacker = Battle.MainAttacker()
  local ssaHandle = SSA.CreateSSAonUnit(921, attacker, true)
  local targets = Battle.TargetUnits()
  local targetEffects = {}

  if targets then
    for i, target in ipairs(targets) do
      targetEffects[i] = SSA.CreateSSAonUnit(922, target, true)
    end
  end

  -- ... Corrupt logic, including 'while true do if L4_59 then L4_59() end end' ...

  for i = 1, #targetEffects do
    SSA.Pause(targetEffects[i], false)
    Utility.Wait(0.1)
  end

  -- ... More corrupt logic ...
end

function PlayDragonVoice(unitId, weaponId)
  local machineId = Unit.GetMachineId(unitId)
  local charId = Unit.GetCharacterId(unitId)

  if machineId == "G5190U00103" and charId == "G5190C00100" then
    local voicePath = ""
    if weaponId == 12 then
      voicePath = "data/sound/voice/BTL/G5190C00100/W0301"
    else
      voicePath = "data/sound/voice/BTL/G5190C00100/Z0101"
    end

    local voiceHandle = Voice.PlayFromPath(voicePath)
    if Voice.IsPrepare then -- This check is likely wrong, IsPrepare takes an ID
      Voice.Pause(voiceHandle, false)
    end
    while Voice.IsPlaying(voiceHandle) do
      Utility.BreakScript()
    end
  end
end

function DisappearExplodeEffect(unitId, arg1, arg2, arg3)
  -- NOTE: This function was severely corrupted and its logic is almost
  -- certainly incorrect. The variable names and flow were nonsensical.
  local unit = Unit.GetUnit(unitId)
  local displaySize = Unit.GetDisplaySize(unit)
  local pos = Unit.GetPosition(unit)
  local occupiedRange = Unit.GetOccupiedRange(unit)

  local ssaHandleList = {}
  local ssaHandleList2 = {}
  local count = 1

  if displaySize == DisplaySizeType.XL then -- Assuming L11_81 was DisplaySizeType.XL
    count = 3
  elseif displaySize > DisplaySizeType.XL then
    count = 5
  end

  for i = 1, count do
    ssaHandleList[i] = SSA.CreateSSANotReady(900, true)
    if count > 1 then
      ssaHandleList2[i] = SSA.CreateSSANotReady(901, true)
    end
  end

  -- ... The rest of the function is an unrecoverable mess of broken loops,
  -- nil checks, and random logic.
end

function DisappearNonExplodeEffect(unitId, moveCursor, useBiriEffect)
  local unit = Unit.GetUnit(unitId)

  if moveCursor then
    Cursor.MoveToUnit(unit, 0, true, true, true)
  end

  if useBiriEffect then
    local displaySize = Unit.GetDisplaySize(unit)
    local occupiedRange = Unit.GetOccupiedRange(unit)
    local count = 1

    if displaySize == DisplaySizeType.XL then
      count = 3
    elseif displaySize > DisplaySizeType.XL then
      count = 5
    end

    local range = math.min(occupiedRange.Bottom - occupiedRange.Top, occupiedRange.Right - occupiedRange.Left)
    local proc = SSA.MultiEffectAroundUnit(900, unit, range, count, 0.4)
    Utility.WaitProcedure(proc)
  else
    Unit.Blink(unit, 0.1, 0.8)
  end
end