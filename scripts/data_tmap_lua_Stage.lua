local L1_1
L0_0 = {}
Stage = L0_0
L0_0 = Stage
function L1_1()
  return System.EnemiesExist()
end
L0_0.EnemiesExist = L1_1
L0_0 = Stage
function L1_1()
  return System.PlayersExist()
end
L0_0.PlayersExist = L1_1
L0_0 = Stage
function L1_1()
  return System.GetTurn()
end
L0_0.Turn = L1_1
L0_0 = Stage
function L1_1()
  return System.GetPhase()
end
L0_0.Phase = L1_1
L0_0 = Stage
function L1_1()
  return System.GetPhase() == Phase.Player
end
L0_0.IsPlayerControl = L1_1
L0_0 = Stage
function L1_1(A0_2)
  return System.GetPhase() == A0_2
end
L0_0.IsAssigned = L1_1
L0_0 = Stage
function L1_1(...)
  L1_3 = System
  L1_3 = L1_3.SetVictoryCondition
  L1_3(...)
end
L0_0.SetVictoryCondition = L1_1
L0_0 = Stage
function L1_1(...)
  L1_4 = System
  L1_4 = L1_4.SetDefeatCondition
  L1_4(...)
end
L0_0.SetDefeatCondition = L1_1
L0_0 = Stage
function L1_1(A0_5)
  System.SetEventCondition(A0_5)
end
L0_0.SetEventCondition = L1_1
L0_0 = Stage
function L1_1(A0_6)
  System.SetChallengeCondition(A0_6)
end
L0_0.SetChallengeCondition = L1_1
L0_0 = Stage
function L1_1(A0_7, A1_8)
  System.SetTurnLimit(A0_7, A1_8)
end
L0_0.SetTurnLimit = L1_1
L0_0 = Stage
function L1_1(A0_9)
  return System.GetTurnLimit(A0_9)
end
L0_0.GetTurnLimit = L1_1
L0_0 = Stage
function L1_1(A0_10, A1_11)
  System.SetMachineLimit(A0_10, A1_11)
end
L0_0.SetMachineLimit = L1_1
L0_0 = Stage
function L1_1(A0_12)
  return System.GetMachineLimit(A0_12)
end
L0_0.GetMachineLimit = L1_1
L0_0 = Stage
function L1_1(A0_13, A1_14, A2_15)
  System.SetTurnMachineLimit(A0_13, A1_14, A2_15)
end
L0_0.SetTurnMachineLimit = L1_1
L0_0 = Stage
function L1_1()
  return System.GetEventStatus()
end
L0_0.GetEventStatus = L1_1
L0_0 = Stage
function L1_1()
  local L0_16
  L0_16 = System
  L0_16 = L0_16.PlayTitleCall
  L0_16 = L0_16()
  Utility.WaitProcedure(L0_16)
end
L0_0.PlayTitleCall = L1_1
L0_0 = Stage
function L1_1(A0_17, A1_18)
  System.ShowAnnounceWindow(A0_17, A1_18)
end
L0_0.ShowAnnounceWindow = L1_1
L0_0 = Stage
function L1_1()
  return System.IsEventBattle()
end
L0_0.IsEventBattle = L1_1
L0_0 = Stage
function L1_1(A0_19)
  System.SetOpponentArmyFlag(ArmyType.Enemy1, ArmyType.Enemy2, A0_19)
end
L0_0.SetEnableEnemyBattle = L1_1
L0_0 = Stage
function L1_1(A0_20, A1_21, A2_22)
  System.SetOpponentArmyFlag(A0_20, A1_21, A2_22)
end
L0_0.SetOpponentArmyFlag = L1_1
L0_0 = Stage
function L1_1()
  local L0_23
  L0_23 = System
  L0_23 = L0_23.ShowEventCondition
  L0_23 = L0_23()
  Utility.WaitProcedure(L0_23)
end
L0_0.ShowEventCondition = L1_1
L0_0 = Stage
function L1_1()
  local L0_24
  L0_24 = System
  L0_24 = L0_24.ShowVictoryCondition
  L0_24 = L0_24()
  Utility.WaitProcedure(L0_24)
end
L0_0.ShowVictoryCondition = L1_1
L0_0 = Stage
function L1_1(A0_25)
  System.SetVisibleDonpachi(A0_25)
end
L0_0.SetVisibleDonpachi = L1_1
L0_0 = Stage
function L1_1()
  while System.CheckQuestAchieved() do
    coroutine.yield(0)
  end
end
L0_0.CheckQuestAchieved = L1_1
L0_0 = Stage
function L1_1(A0_26)
  System.ShowTutorial(A0_26)
end
L0_0.ShowTutorial = L1_1
L0_0 = Stage
function L1_1()
  return System.GetStageLevel()
end
L0_0.GetStageLevel = L1_1
L0_0 = Stage
function L1_1()
  return System.GetInfernoLevel()
end
L0_0.GetInfernoLevel = L1_1
L0_0 = Stage
function L1_1()
  return System.IsChallengeStage()
end
L0_0.IsChallengeStage = L1_1
L0_0 = Stage
function L1_1()
  return System.GetClearCount()
end
L0_0.GetClearCount = L1_1
L0_0 = Stage
function L1_1(A0_27, A1_28, A2_29)
  System.SetOpenCondition(A0_27, A1_28, A2_29)
end
L0_0.SetOpenCondition = L1_1
L0_0 = Stage
function L1_1(A0_30)
  return System.CheckCondition(A0_30)
end
L0_0.CheckCondition = L1_1
L0_0 = Stage
function L1_1()
  return Battle.IsDestroyGameOverUnit() or not Stage.PlayersExist() or Stage.CheckCondition(ConditionType.Defeat) == ConditionState.Success or Stage.CheckCondition(ConditionType.Victory) == ConditionState.Failed
end
L0_0.IsGameOver = L1_1
L0_0 = Stage
function L1_1()
  return Stage.CheckCondition(ConditionType.Victory) == ConditionState.Success
end
L0_0.IsStageClear = L1_1
L0_0 = Stage
function L1_1()
  return System.GetScore()
end
L0_0.GetScore = L1_1
L0_0 = {}
Map = L0_0
L0_0 = Map
function L1_1()
  return System.GetMapIndex()
end
L0_0.GetIndex = L1_1
L0_0 = Map
function L1_1(A0_31)
  System.SetMapIndex(A0_31)
  while not Map.IsReady() do
    coroutine.yield(0)
  end
end
L0_0.SetIndex = L1_1
L0_0 = Map
function L1_1(A0_32, A1_33)
  System.SetEnableMap(A0_32, A1_33)
end
L0_0.SetEnable = L1_1
L0_0 = Map
function L1_1()
  return System.IsReadyMap()
end
L0_0.IsReady = L1_1
L0_0 = Map
function L1_1(A0_34)
  System.PauseMapAnimation(A0_34)
end
L0_0.PauseAnimation = L1_1
L0_0 = Map
function L1_1(A0_35, A1_36)
  System.PauseNodeAnimation(A0_35, A1_36)
end
L0_0.PauseNodeAnimation = L1_1
L0_0 = Map
function L1_1(A0_37, A1_38)
  System.SetVisibleNode(A0_37, A1_38)
end
L0_0.SetVisibleNode = L1_1
L0_0 = Map
function L1_1(A0_39, A1_40)
  System.SetVisibleFloatingObject(A0_39, A1_40)
end
L0_0.VisibleFloatingObject = L1_1
L0_0 = Map
function L1_1(A0_41, A1_42)
  return System.GetNoUnitCell(A0_41, A1_42)
end
L0_0.GetNoUnitCell = L1_1
L0_0 = Map
function L1_1(A0_43, ...)
  L1_44 = false
  if select("#", ...) >= 1 then
    L1_44 = select(1, ...)
  end
  return System.GetUnitsByMapIndex(A0_43, L1_44)
end
L0_0.GetUnitsByMapIndex = L1_1
L0_0 = Map
function L1_1(A0_45)
  System.SetNegativeColorCorrection(A0_45)
end
L0_0.SetNegativeColorCorrection = L1_1
L0_0 = Map
function L1_1(A0_46, A1_47)
  local L2_48
  L2_48 = System
  L2_48 = L2_48.GetUnit
  L2_48 = L2_48(A0_46)
  System.SetTorchLight(L2_48, A1_47)
end
L0_0.SetTorchLight = L1_1
L0_0 = Map
function L1_1(A0_49, A1_50, A2_51)
  System.SetTorchLight(A0_49, A1_50, A2_51)
end
L0_0.SetTorchLightPosition = L1_1
L0_0 = Map
function L1_1(A0_52, A1_53, A2_54, A3_55)
  System.SetCellAttribute(A0_52, A1_53, A2_54, A3_55)
end
L0_0.SetCellAttribute = L1_1
L0_0 = {}
Cursor = L0_0
L0_0 = Cursor
function L1_1(A0_56)
  System.SetCursorVisible(A0_56)
end
L0_0.Visible = L1_1
L0_0 = Cursor
function L1_1(A0_57, A1_58, A2_59)
  System.SetScriptCursorColor(true, A0_57, A1_58, A2_59)
end
L0_0.SetScriptColor = L1_1
L0_0 = Cursor
function L1_1()
  System.SetScriptCursorColor(false, 0, 0, 0)
end
L0_0.DisableScriptColor = L1_1
L0_0 = Cursor
function L1_1(A0_60, A1_61)
  System.SetCursorOffset(A0_60, A1_61)
end
L0_0.SetCursorOffset = L1_1
L0_0 = Cursor
function L1_1()
  return System.GetCursorPosition()
end
L0_0.GetPosition = L1_1
L0_0 = Cursor
function L1_1(A0_62, A1_63, ...)
  L2_64 = System
  L2_64 = L2_64.SetCursorPosition
  L2_64 = L2_64(A0_62, A1_63, ...)
  if select("#", ...) >= 3 and select(3, ...) then
    while System.FindProcedure(L2_64) do
      coroutine.yield(0)
    end
  end
end
L0_0.SetPosition = L1_1
L0_0 = Cursor
function L1_1(A0_65, ...)
  local L2_67
  L1_66 = System
  L1_66 = L1_66.GetUnit
  L2_67 = A0_65
  L1_66 = L1_66(L2_67)
  L2_67 = Map
  L2_67 = L2_67.SetIndex
  L2_67(Unit.GetMapIndex(L1_66))
  L2_67 = System
  L2_67 = L2_67.MoveCursorToUnit
  L2_67 = L2_67(L1_66, ...)
  if select("#", ...) >= 3 and select(3, ...) then
    while System.FindProcedure(L2_67) do
      coroutine.yield(0)
    end
  end
end
L0_0.MoveToUnit = L1_1
L0_0 = Cursor
function L1_1(A0_68, A1_69, ...)
  local L3_71, L4_72
  L2_70 = System
  L2_70 = L2_70.GetUnit
  L3_71 = A0_68
  L2_70 = L2_70(L3_71)
  L3_71 = System
  L3_71 = L3_71.GetUnit
  L4_72 = A1_69
  L3_71 = L3_71(L4_72)
  L4_72 = Map
  L4_72 = L4_72.SetIndex
  L4_72(Unit.GetMapIndex(L2_70))
  L4_72 = System
  L4_72 = L4_72.MoveCursorToBetweenUnit
  L4_72 = L4_72(L2_70, L3_71, ...)
  if select("#", ...) >= 3 and select(3, ...) then
    while System.FindProcedure(L4_72) do
      coroutine.yield(0)
    end
  end
end
L0_0.MoveToBetweenUnit = L1_1
L0_0 = {}
Grid = L0_0
L0_0 = Grid
function L1_1()
  return System.GridSize()
end
L0_0.Size = L1_1
L0_0 = Grid
function L1_1(A0_73)
  System.IsVisibleGridAndSquare(A0_73)
end
L0_0.IsVisibleGridAndSquare = L1_1
L0_0 = Grid
function L1_1(A0_74, A1_75, ...)
  local L4_77, L5_78
  L3_76 = System
  L3_76 = L3_76.IsEnableArea
  L4_77 = A0_74
  L5_78 = A1_75
  L3_76(L4_77, L5_78, ...)
end
L0_0.IsEnableArea = L1_1
L0_0 = Grid
function L1_1(A0_79, A1_80)
  System.IsVisibleArea(A0_79, A1_80)
end
L0_0.IsVisibleArea = L1_1
L0_0 = Grid
function L1_1(A0_81, A1_82, ...)
  L2_83 = System
  L2_83 = L2_83.GetUnit
  L2_83 = L2_83(A0_81)
  System.BlinkAroundUnit(L2_83, A1_82, ...)
end
L0_0.BlinkAroundUnit = L1_1
L0_0 = Grid
function L1_1(A0_84)
  return System.GetIrregularPosition(A0_84)
end
L0_0.GetIrregularPosition = L1_1
L0_0 = {}
Phase = L0_0
L0_0 = Phase
L0_0.Player = 0
L0_0 = Phase
L0_0.Friend = 1
L0_0 = Phase
L0_0.Enemy1 = 2
L0_0 = Phase
L0_0.Enemy2 = 3
L0_0 = Phase
L0_0.Secret = 4
L0_0 = {}
ArmyType = L0_0
L0_0 = ArmyType
L0_0.Player = 0
L0_0 = ArmyType
L0_0.Guest = 1
L0_0 = ArmyType
L0_0.Friend = 2
L0_0 = ArmyType
L0_0.Enemy1 = 3
L0_0 = ArmyType
L0_0.Enemy2 = 4
L0_0 = ArmyType
L0_0.Secret = 5
L0_0 = {}
TurnLimitType = L0_0
L0_0 = TurnLimitType
L0_0.Victory = 0
L0_0 = TurnLimitType
L0_0.Defeat = 1
L0_0 = TurnLimitType
L0_0.Event = 2
L0_0 = TurnLimitType
L0_0.Challenge = 3
L0_0 = {}
StageLevel = L0_0
L0_0 = StageLevel
L0_0.Normal = 0
L0_0 = StageLevel
L0_0.Hard = 1
L0_0 = StageLevel
L0_0.Extra = 2
L0_0 = StageLevel
L0_0.Hell = 3
L0_0 = StageLevel
L0_0.Inferno = 4
L0_0 = {}
ConditionType = L0_0
L0_0 = ConditionType
L0_0.Victory = 0
L0_0 = ConditionType
L0_0.Defeat = 1
L0_0 = ConditionType
L0_0.Event = 2
L0_0 = ConditionType
L0_0.Challenge = 3
L0_0 = {}
ConditionState = L0_0
L0_0 = ConditionState
L0_0.Continue = 0
L0_0 = ConditionState
L0_0.Success = 1
L0_0 = ConditionState
L0_0.Failed = 2
