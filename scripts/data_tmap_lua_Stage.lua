Stage = {}

function Stage.EnemiesExist()
  return System.EnemiesExist()
end

function Stage.PlayersExist()
  return System.PlayersExist()
end

function Stage.Turn()
  return System.GetTurn()
end

function Stage.Phase()
  return System.GetPhase()
end

function Stage.IsPlayerControl()
  return System.GetPhase() == Phase.Player
end

function Stage.IsAssigned(phase)
  return System.GetPhase() == phase
end

function Stage.SetVictoryCondition(...)
  System.SetVictoryCondition(...)
end

function Stage.SetDefeatCondition(...)
  System.SetDefeatCondition(...)
end

function Stage.SetEventCondition(condition)
  System.SetEventCondition(condition)
end

function Stage.SetChallengeCondition(condition)
  System.SetChallengeCondition(condition)
end

function Stage.SetTurnLimit(limitType, turn)
  System.SetTurnLimit(limitType, turn)
end

function Stage.GetTurnLimit(limitType)
  return System.GetTurnLimit(limitType)
end

function Stage.SetMachineLimit(limitType, count)
  System.SetMachineLimit(limitType, count)
end

function Stage.GetMachineLimit(limitType)
  return System.GetMachineLimit(limitType)
end

function Stage.SetTurnMachineLimit(limitType, turn, count)
  System.SetTurnMachineLimit(limitType, turn, count)
end

function Stage.GetEventStatus()
  return System.GetEventStatus()
end

function Stage.PlayTitleCall()
  local proc = System.PlayTitleCall()
  Utility.WaitProcedure(proc)
end

function Stage.ShowAnnounceWindow(message, type)
  System.ShowAnnounceWindow(message, type)
end

function Stage.IsEventBattle()
  return System.IsEventBattle()
end

function Stage.SetEnableEnemyBattle(enable)
  System.SetOpponentArmyFlag(ArmyType.Enemy1, ArmyType.Enemy2, enable)
end

function Stage.SetOpponentArmyFlag(army1, army2, enable)
  System.SetOpponentArmyFlag(army1, army2, enable)
end

function Stage.ShowEventCondition()
  local proc = System.ShowEventCondition()
  Utility.WaitProcedure(proc)
end

function Stage.ShowVictoryCondition()
  local proc = System.ShowVictoryCondition()
  Utility.WaitProcedure(proc)
end

function Stage.SetVisibleDonpachi(visible)
  System.SetVisibleDonpachi(visible)
end

function Stage.CheckQuestAchieved()
  while System.CheckQuestAchieved() do
    coroutine.yield(0)
  end
end

function Stage.ShowTutorial(tutorialId)
  System.ShowTutorial(tutorialId)
end

function Stage.GetStageLevel()
  return System.GetStageLevel()
end

function Stage.GetInfernoLevel()
  return System.GetInfernoLevel()
end

function Stage.IsChallengeStage()
  return System.IsChallengeStage()
end

function Stage.GetClearCount()
  return System.GetClearCount()
end

function Stage.SetOpenCondition(conditionType, conditionId, param)
  System.SetOpenCondition(conditionType, conditionId, param)
end

function Stage.CheckCondition(conditionType)
  return System.CheckCondition(conditionType)
end

function Stage.IsGameOver()
  return Battle.IsDestroyGameOverUnit() 
    or not Stage.PlayersExist() 
    or Stage.CheckCondition(ConditionType.Defeat) == ConditionState.Success 
    or Stage.CheckCondition(ConditionType.Victory) == ConditionState.Failed
end

function Stage.IsStageClear()
  return Stage.CheckCondition(ConditionType.Victory) == ConditionState.Success
end

function Stage.GetScore()
  return System.GetScore()
end

---
-- Map
---

Map = {}

function Map.GetIndex()
  return System.GetMapIndex()
end

function Map.SetIndex(mapIndex)
  System.SetMapIndex(mapIndex)
  while not Map.IsReady() do
    coroutine.yield(0)
  end
end

function Map.SetEnable(mapIndex, enable)
  System.SetEnableMap(mapIndex, enable)
end

function Map.IsReady()
  return System.IsReadyMap()
end

function Map.PauseAnimation(pause)
  System.PauseMapAnimation(pause)
end

function Map.PauseNodeAnimation(nodeName, pause)
  System.PauseNodeAnimation(nodeName, pause)
end

function Map.SetVisibleNode(nodeName, visible)
  System.SetVisibleNode(nodeName, visible)
end

function Map.VisibleFloatingObject(mapIndex, visible)
  System.SetVisibleFloatingObject(mapIndex, visible)
end

function Map.GetNoUnitCell(mapIndex, armyType)
  return System.GetNoUnitCell(mapIndex, armyType)
end

function Map.GetUnitsByMapIndex(mapIndex, ...)
  local includeInShip = false
  if select("#", ...) >= 1 then
    includeInShip = select(1, ...)
  end
  return System.GetUnitsByMapIndex(mapIndex, includeInShip)
end

function Map.SetNegativeColorCorrection(enable)
  System.SetNegativeColorCorrection(enable)
end

function Map.SetTorchLight(unitId, enable)
  local unit = System.GetUnit(unitId)
  System.SetTorchLight(unit, enable)
end

function Map.SetTorchLightPosition(x, y, z)
  System.SetTorchLight(x, y, z)
end

function Map.SetCellAttribute(x, y, attribute, value)
  System.SetCellAttribute(x, y, attribute, value)
end

---
-- Cursor
---

Cursor = {}

function Cursor.Visible(visible)
  System.SetCursorVisible(visible)
end

function Cursor.SetScriptColor(r, g, b)
  System.SetScriptCursorColor(true, r, g, b)
end

function Cursor.DisableScriptColor()
  System.SetScriptCursorColor(false, 0, 0, 0)
end

function Cursor.SetCursorOffset(x, y)
  System.SetCursorOffset(x, y)
end

function Cursor.GetPosition()
  return System.GetCursorPosition()
end

function Cursor.SetPosition(x, y, ...)
  local proc = System.SetCursorPosition(x, y, ...)
  
  -- Check if 'wait' is true (arg 3, which is 1-indexed in '...')
  if select("#", ...) >= 3 and select(3, ...) then
    while System.FindProcedure(proc) do
      coroutine.yield(0)
    end
  end
end

function Cursor.MoveToUnit(unitId, ...)
  local unit = System.GetUnit(unitId)
  Map.SetIndex(Unit.GetMapIndex(unit))
  
  local proc = System.MoveCursorToUnit(unit, ...)
  
  -- Check if 'wait' is true (arg 3, which is 1-indexed in '...')
  if select("#", ...) >= 3 and select(3, ...) then
    while System.FindProcedure(proc) do
      coroutine.yield(0)
    end
  end
end

function Cursor.MoveToBetweenUnit(unitId1, unitId2, ...)
  local unit1 = System.GetUnit(unitId1)
  local unit2 = System.GetUnit(unitId2)
  Map.SetIndex(Unit.GetMapIndex(unit1))
  
  local proc = System.MoveCursorToBetweenUnit(unit1, unit2, ...)
  
  -- Check if 'wait' is true (arg 3, which is 1-indexed in '...')
  if select("#", ...) >= 3 and select(3, ...) then
    while System.FindProcedure(proc) do
      coroutine.yield(0)
    end
  end
end

---
-- Grid
---

Grid = {}

function Grid.Size()
  return System.GridSize()
end

function Grid.IsVisibleGridAndSquare(visible)
  System.IsVisibleGridAndSquare(visible)
end

function Grid.IsEnableArea(areaType, areaId, ...)
  System.IsEnableArea(areaType, areaId, ...)
end

function Grid.IsVisibleArea(areaType, visible)
  System.IsVisibleArea(areaType, visible)
end

function Grid.BlinkAroundUnit(unitId, range, ...)
  local unit = System.GetUnit(unitId)
  System.BlinkAroundUnit(unit, range, ...)
end

function Grid.GetIrregularPosition(unitId)
  return System.GetIrregularPosition(unitId)
end

---
-- Enums
---

Phase = {
  Player = 0,
  Friend = 1,
  Enemy1 = 2,
  Enemy2 = 3,
  Secret = 4
}

ArmyType = {
  Player = 0,
  Guest = 1,
  Friend = 2,
  Enemy1 = 3,
  Enemy2 = 4,
  Secret = 5
}

TurnLimitType = {
  Victory = 0,
  Defeat = 1,
  Event = 2,
  Challenge = 3
}

StageLevel = {
  Normal = 0,
  Hard = 1,
  Extra = 2,
  Hell = 3,
  Inferno = 4
}

ConditionType = {
  Victory = 0,
  Defeat = 1,
  Event = 2,
  Challenge = 3
}

ConditionState = {
  Continue = 0,
  Success = 1,
  Failed = 2
}