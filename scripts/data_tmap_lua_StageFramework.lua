local L1_1
function L0_0()
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
Startup = L0_0
function L0_0(A0_2)
  PlayStageCommonBGM()
  OnStartPhase(A0_2)
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
StartPhase = L0_0
function L0_0(A0_3)
  local L1_4, L2_5, L3_6, L4_7, L5_8, L6_9
  L1_4 = OnBeforeEnd
  L1_4(L2_5)
  L1_4 = Stage
  L1_4 = L1_4.IsGameOver
  L1_4 = L1_4()
  if L1_4 then
    L1_4 = GameOverEvent
    L1_4()
    L1_4 = System
    L1_4 = L1_4.GameOver
    L1_4()
    return
  end
  L1_4 = CheckEventCondition
  L1_4()
  L1_4 = Stage
  L1_4 = L1_4.IsStageClear
  L1_4 = L1_4()
  if L1_4 then
    L1_4 = StageClearEvent
    L1_4()
    L1_4 = System
    L1_4 = L1_4.StageClear
    L1_4()
    L1_4 = System
    L1_4 = L1_4.IsTriggeredEvent
    L1_4(L2_5)
    return
  end
  L1_4 = Utility
  L1_4 = L1_4.EndEventSkip
  L1_4()
  while true do
    L1_4 = Utility
    L1_4 = L1_4.IsShowTutorial
    L1_4 = L1_4()
    if L1_4 then
      L1_4 = Utility
      L1_4 = L1_4.BreakScript
      L1_4()
    end
  end
  L1_4 = Unit
  L1_4 = L1_4.GetAllUnits
  L1_4 = L1_4(L2_5)
  for L5_8, L6_9 in L2_5(L3_6) do
    if Unit.GetParameter(L6_9).Hp > 0 and not Unit.IsInWarShip(L6_9) and not Unit.IsDoneWarningHp(L6_9) and Unit.IsValidPosition(L6_9) and 0 < Battle.GetDamage(L6_9) and Unit.GetWarningHpPercent(L6_9) / 100 > Unit.GetParameter(L6_9).Hp / Unit.GetParameter(L6_9).MaxHp then
      if Unit.HasStageWarningHp(L6_9) then
        OnWarningHp(L6_9)
      elseif Unit.IsPlayer(L6_9) and not Unit.IsSfs(L6_9) then
        CheckHpWarning(0, L6_9, 0, true)
      end
    end
  end
end
BeforeEnd = L0_0
function L0_0()
  OnTalkBeforeBattle()
end
BeforeBattle = L0_0
function L0_0()
  local L0_10, L1_11, L2_12, L3_13, L4_14, L5_15
  L0_10 = Battle
  L0_10 = L0_10.DeadUnits
  L0_10 = L0_10()
  for L4_14, L5_15 in L1_11(L2_12) do
    if Unit.IsAlive(L5_15) then
      if Unit.HasDeadEvent(L5_15) then
        OnDiedEvent(L5_15)
      elseif Unit.IsPlayer(L5_15) and not Unit.IsSfs(L5_15) then
        OutEvent(0, L5_15, 0, OutEventType.Explosion, true)
      end
    end
  end
end
AfterBattle = L0_0
function L0_0(A0_16, A1_17, A2_18, A3_19, ...)
  local L5_21
  L4_20 = Cursor
  L4_20 = L4_20.Visible
  L5_21 = false
  L4_20(L5_21)
  L4_20 = Cursor
  L4_20 = L4_20.MoveToUnit
  L5_21 = A1_17
  L4_20(L5_21, 0, true)
  L4_20 = Utility
  L4_20 = L4_20.Wait
  L5_21 = 0.3
  L4_20(L5_21)
  L4_20 = SSA
  L4_20 = L4_20.CreateSSAonUnit
  L5_21 = 900
  L4_20 = L4_20(L5_21, A1_17)
  L5_21 = SSA
  L5_21 = L5_21.Loop
  L5_21(L4_20, true)
  L5_21 = Cursor
  L5_21 = L5_21.Visible
  L5_21(true)
  L5_21 = Utility
  L5_21 = L5_21.Wait
  L5_21(0.4)
  L5_21 = false
  if select("#", ...) >= 1 then
    L5_21 = select(1, ...)
  end
  if L5_21 then
    Message.ShowScoutMessage(A1_17, false)
    Message.CloseWindow()
    if Unit.IsWs(A1_17) or Unit.IsMaster(A1_17) then
      A3_19 = OutEventType.Master
    end
  else
    Message.ShowMessageWithCameraZoom(A0_16, A1_17, A2_18)
    Message.CloseWindow()
  end
  SSA.Loop(L4_20, false)
  if A3_19 == OutEventType.Disappear then
    Unit.Disappear(A1_17)
  else
    Unit.Kill(A1_17, A3_19 == OutEventType.Master)
  end
  Utility.Wait(0.2)
end
OutEvent = L0_0
function L0_0(A0_22, A1_23, A2_24, ...)
  local L4_26, L5_27, L6_28
  L3_25 = Unit
  L3_25 = L3_25.GetParameter
  L4_26 = A1_23
  L3_25 = L3_25(L4_26)
  L4_26 = Unit
  L4_26 = L4_26.GetWarningHpPercent
  L5_27 = A1_23
  L4_26 = L4_26(L5_27)
  L4_26 = L4_26 / 100
  L5_27 = L3_25.Hp
  L6_28 = L3_25.MaxHp
  L5_27 = L5_27 / L6_28
  if L4_26 > L5_27 then
    L5_27 = Cursor
    L5_27 = L5_27.MoveToUnit
    L6_28 = A1_23
    L5_27(L6_28, 0, true)
    L5_27 = Utility
    L5_27 = L5_27.Wait
    L6_28 = 0.3
    L5_27(L6_28)
    L5_27 = Unit
    L5_27 = L5_27.ShowWarningHp
    L6_28 = A1_23
    L5_27 = L5_27(L6_28)
    L6_28 = Utility
    L6_28 = L6_28.WaitProcedure
    L6_28(L5_27)
    L6_28 = false
    if select("#", ...) >= 1 then
      L6_28 = select(1, ...)
    end
    if L6_28 then
      Message.ShowScoutMessage(A1_23, true)
      Message.CloseWindow()
    else
      Message.ShowMessageWithCameraZoom(A0_22, A1_23, A2_24)
      Message.CloseWindow()
    end
  end
end
CheckHpWarning = L0_0
function L0_0()
  local L0_29, L1_30, L2_31, L3_32, L4_33, L5_34
  L0_29 = Utility
  L0_29 = L0_29.DebugPrint
  L0_29(L1_30)
  L0_29 = Stage
  L0_29 = L0_29.IsGameOver
  L0_29 = L0_29()
  if not L0_29 then
    L0_29 = Battle
    L0_29 = L0_29.IsDestroyGameOverUnitWithoutBattleControl
    L0_29 = L0_29()
  elseif L0_29 then
    L0_29 = GameOverEvent
    L0_29()
    L0_29 = System
    L0_29 = L0_29.GameOver
    L0_29()
    return
  end
  L0_29 = CheckEventCondition
  L0_29()
  L0_29 = Stage
  L0_29 = L0_29.IsStageClear
  L0_29 = L0_29()
  if L0_29 then
    L0_29 = StageClearEvent
    L0_29()
    L0_29 = System
    L0_29 = L0_29.StageClear
    L0_29()
    L0_29 = System
    L0_29 = L0_29.IsTriggeredEvent
    L0_29(L1_30)
    return
  end
  L0_29 = Utility
  L0_29 = L0_29.EndEventSkip
  L0_29()
  while true do
    L0_29 = Utility
    L0_29 = L0_29.IsShowTutorial
    L0_29 = L0_29()
    if L0_29 then
      L0_29 = Utility
      L0_29 = L0_29.BreakScript
      L0_29()
    end
  end
  L0_29 = Unit
  L0_29 = L0_29.GetAllUnits
  L0_29 = L0_29(L1_30)
  for L4_33, L5_34 in L1_30(L2_31) do
    if Unit.GetParameter(L5_34).Hp > 0 and not Unit.IsInWarShip(L5_34) and not Unit.IsDoneWarningHp(L5_34) and Unit.IsValidPosition(L5_34) and Unit.GetWarningHpPercent(L5_34) / 100 > Unit.GetParameter(L5_34).Hp / Unit.GetParameter(L5_34).MaxHp then
      if Unit.HasStageWarningHp(L5_34) then
        OnWarningHp(L5_34)
      elseif Unit.IsPlayer(L5_34) and not Unit.IsSfs(L5_34) then
        CheckHpWarning(0, L5_34, 0, true)
      end
    end
  end
end
BeforeEndWithoutBattleControl = L0_0
function L0_0()
  local L0_35, L1_36, L2_37, L3_38
  L0_35 = System
  L0_35 = L0_35.IsTriggeredEvent
  L0_35 = L0_35()
  if L0_35 then
    return
  end
  L0_35 = Stage
  L0_35 = L0_35.IsEventBattle
  L0_35 = L0_35()
  L1_36 = ConditionState
  L1_36 = L1_36.Continue
  L2_37 = System
  L2_37 = L2_37.GetEventStatus
  L2_37 = L2_37()
  L3_38 = ConditionState
  L3_38 = L3_38.Continue
  if L2_37 == L3_38 then
    L2_37 = Stage
    L2_37 = L2_37.CheckCondition
    L3_38 = ConditionType
    L3_38 = L3_38.Event
    L2_37 = L2_37(L3_38)
    L1_36 = L2_37
    L2_37 = ConditionState
    L2_37 = L2_37.Success
    if L1_36 == L2_37 then
      L2_37 = System
      L2_37 = L2_37.SetEventStatus
      L3_38 = ConditionState
      L3_38 = L3_38.Success
      L2_37(L3_38)
    else
      L2_37 = ConditionState
      L2_37 = L2_37.Failed
      if L1_36 == L2_37 then
        L2_37 = System
        L2_37 = L2_37.SetEventStatus
        L3_38 = ConditionState
        L3_38 = L3_38.Failed
        L2_37(L3_38)
      end
    end
  end
  L2_37 = System
  L2_37 = L2_37.GetChallengeStatus
  L2_37 = L2_37()
  L3_38 = ConditionState
  L3_38 = L3_38.Continue
  if L2_37 == L3_38 then
    L2_37 = Stage
    L2_37 = L2_37.CheckCondition
    L3_38 = ConditionType
    L3_38 = L3_38.Challenge
    L2_37 = L2_37(L3_38)
    L3_38 = ConditionState
    L3_38 = L3_38.Success
    if L2_37 == L3_38 then
      L3_38 = System
      L3_38 = L3_38.SetChallengeStatus
      L3_38(ConditionState.Success)
    else
      L3_38 = ConditionState
      L3_38 = L3_38.Failed
      if L2_37 == L3_38 then
        L3_38 = System
        L3_38 = L3_38.SetChallengeStatus
        L3_38(ConditionState.Failed)
      end
    end
  end
  L2_37 = System
  L2_37 = L2_37.GetEventStatus
  L2_37 = L2_37()
  L3_38 = ConditionState
  L3_38 = L3_38.Success
  if L2_37 == L3_38 then
    L2_37 = BGM
    L2_37 = L2_37.Stop
    L2_37()
    L2_37 = Cursor
    L2_37 = L2_37.Visible
    L3_38 = false
    L2_37(L3_38)
    L2_37 = Grid
    L2_37 = L2_37.IsVisibleGridAndSquare
    L3_38 = false
    L2_37(L3_38)
    L2_37 = 906
    L3_38 = Stage
    L3_38 = L3_38.IsChallengeStage
    L3_38 = L3_38()
    if L3_38 then
    end
    L3_38 = SSA
    L3_38 = L3_38.CreateSSA
    L3_38 = L3_38(L2_37)
    SSA.CanSkip(L3_38, true)
    Utility.WaitProcedure(L3_38)
    if System.GetChallengeStatus() == ConditionState.Success then
      L0_35 = true
    else
      System.SetChallengeStatus(ConditionState.Failed)
    end
    BreakEvent1()
    System.IsTriggeredEvent(true)
  end
  if L0_35 then
    L2_37 = Stage
    L2_37 = L2_37.IsEventBattle
    L2_37 = L2_37()
    if not L2_37 then
      L2_37 = Utility
      L2_37 = L2_37.Wait
      L3_38 = 1
      L2_37(L3_38)
      L2_37 = BGM
      L2_37 = L2_37.Stop
      L2_37()
      L2_37 = BGM
      L2_37 = L2_37.GetMapBgmNo
      L3_38 = Stage
      L3_38 = L3_38.Phase
      L3_38 = L3_38()
      L2_37 = L2_37(L3_38, L3_38())
      L3_38 = BGM
      L3_38 = L3_38.Play
      L3_38(L2_37)
      L3_38 = SSA
      L3_38 = L3_38.CreateSSA
      L3_38 = L3_38(903)
      SSA.CanSkip(L3_38, true)
      Utility.WaitProcedure(L3_38)
      ChallengeEvent()
      Stage.ShowTutorial(180)
    else
      L2_37 = System
      L2_37 = L2_37.GetChallengeStatus
      L2_37 = L2_37()
      L3_38 = ConditionState
      L3_38 = L3_38.Success
      if L2_37 == L3_38 then
        L2_37 = ChallengeEvent
        L2_37()
        L2_37 = System
        L2_37 = L2_37.IsTriggeredEvent
        L3_38 = true
        L2_37(L3_38)
      end
    end
  end
  L2_37 = Utility
  L2_37 = L2_37.IsEventSkip
  L2_37 = L2_37()
  if L2_37 then
    L2_37 = BGM
    L2_37 = L2_37.GetMapBgmNo
    L3_38 = Stage
    L3_38 = L3_38.Phase
    L3_38 = L3_38()
    L2_37 = L2_37(L3_38, L3_38())
    L3_38 = BGM
    L3_38 = L3_38.PlayBGMIgnoreEventSkip
    L3_38(L2_37)
  end
  L2_37 = Cursor
  L2_37 = L2_37.Visible
  L3_38 = true
  L2_37(L3_38)
  L2_37 = Grid
  L2_37 = L2_37.IsVisibleGridAndSquare
  L3_38 = true
  L2_37(L3_38)
  L2_37 = System
  L2_37 = L2_37.IsTriggeredEvent
  L2_37 = L2_37()
  if L2_37 then
    L2_37 = Stage
    L2_37 = L2_37.IsEventBattle
    L2_37 = L2_37()
    if not L2_37 then
      L2_37 = Utility
      L2_37 = L2_37.EnableEventSkip
      L3_38 = false
      L2_37(L3_38)
      L2_37 = Utility
      L2_37 = L2_37.EndEventSkip
      L2_37()
      L2_37 = Stage
      L2_37 = L2_37.ShowVictoryCondition
      L2_37()
      L2_37 = Utility
      L2_37 = L2_37.EnableEventSkip
      L3_38 = true
      L2_37(L3_38)
    end
  end
end
CheckEventCondition = L0_0
function L0_0()
  local L0_39
  L0_39 = BGM
  L0_39 = L0_39.GetMapBgmNo
  L0_39 = L0_39(Stage.Phase())
  BGM.Play(L0_39)
end
PlayStageCommonBGM = L0_0
function L0_0()
  System.SaveScriptTable(SaveTable)
  if AfterDataSave ~= nil then
    AfterDataSave()
  end
end
SaveScriptTable = L0_0
function L0_0()
  SaveTable = System.LoadScriptTable(SaveTable)
  if AfterDataLoad ~= nil then
    AfterDataLoad()
  end
end
LoadScriptTable = L0_0
function L0_0()
  local L0_40, L1_41
  L0_40 = 0
  L1_41 = UniqueCharacterBgmNo
  if L1_41 ~= nil then
    L1_41 = UniqueCharacterBgmNo
    L1_41 = L1_41(Stage.Phase())
    L0_40 = L1_41
  end
  return L0_40
end
GetUniqueCharacterBgmNo = L0_0
function L0_0(A0_42, A1_43, A2_44, A3_45)
  local L4_46, L5_47, L6_48, L7_49, L8_50, L9_51, L10_52, L11_53, L12_54
  L4_46 = Battle
  L4_46 = L4_46.MainAttacker
  L4_46 = L4_46()
  L5_47 = Unit
  L5_47 = L5_47.GetPosition
  L6_48 = L4_46
  L5_47 = L5_47(L6_48)
  L6_48 = MapWeaponEffectType
  L6_48 = L6_48.Snipe
  if A2_44 ~= L6_48 then
    L6_48 = MapWeaponEffectType
    L6_48 = L6_48.SubRange
  elseif A2_44 == L6_48 then
    L6_48 = SSA
    L6_48 = L6_48.IsUnitCenterEffect
    L7_49 = L4_46
    L6_48 = L6_48(L7_49)
    if not L6_48 then
      L5_47.X = A0_42
      L5_47.Y = A1_43
    end
  end
  L6_48 = Cursor
  L6_48 = L6_48.SetPosition
  L7_49 = L5_47.X
  L6_48(L7_49, L8_50, L9_51, L10_52, L11_53)
  L6_48 = PlayDragonVoice
  L7_49 = L4_46
  L6_48(L7_49, L8_50)
  L6_48 = MapWeaponEffectType
  L6_48 = L6_48.Move
  if A2_44 == L6_48 then
    L6_48 = SSA
    L6_48 = L6_48.GetKomaAnimeMapEffect
    L7_49 = L4_46
    L6_48 = L6_48(L7_49)
    if L6_48 then
      L6_48 = Unit
      L6_48 = L6_48.SetAnimation
      L7_49 = L4_46
      L6_48(L7_49, L8_50, L9_51)
      L6_48 = Unit
      L6_48 = L6_48.SetHighPriority
      L7_49 = L4_46
      L6_48(L7_49, L8_50)
      L6_48 = SSA
      L6_48 = L6_48.MoveUnitWithMapWeapon
      L7_49 = L4_46
      L6_48 = L6_48(L7_49, L8_50)
      L7_49 = Utility
      L7_49 = L7_49.WaitProcedure
      L7_49(L8_50)
      L7_49 = Unit
      L7_49 = L7_49.SetAnimation
      L7_49(L8_50, L9_51, L10_52)
      L7_49 = Unit
      L7_49 = L7_49.SetHighPriority
      L7_49(L8_50, L9_51)
    else
      L6_48 = SSA
      L6_48 = L6_48.GetMoveRangeWithMapWeapon
      L6_48 = L6_48()
      L7_49 = {}
      for L11_53 = 1, L9_51 - 1 do
        L12_54 = SSA
        L12_54 = L12_54.CreateMapWeaponEffect
        L12_54 = L12_54(L4_46, L6_48[2 * L11_53 - 1], L6_48[2 * L11_53], A3_45)
        L7_49[L11_53] = L12_54
      end
      L9_51(L10_52)
      for L12_54 = 1, #L7_49 do
        SSA.Pause(L7_49[L12_54], false)
        Utility.Wait(0.1)
      end
      L9_51(L10_52)
      while true do
        if L9_51 then
          L9_51()
          else
            L6_48 = SSA
            L6_48 = L6_48.IsHaroMapWeapon
            L7_49 = L4_46
            L6_48 = L6_48(L7_49)
            if L6_48 then
              L6_48 = Battle
              L6_48 = L6_48.TargetUnits
              L6_48 = L6_48()
              L7_49 = {}
              for L11_53, L12_54 in L8_50(L9_51) do
                L7_49[L11_53] = SSA.CreateMapWeaponEffect(L4_46, Unit.GetPosition(L12_54).X, Unit.GetPosition(L12_54).Y, A3_45)
              end
              for L11_53 = 1, #L7_49 do
                L12_54 = SSA
                L12_54 = L12_54.SetTerrainOffset
                L12_54(L7_49[L11_53], L6_48[L11_53])
                L12_54 = SSA
                L12_54 = L12_54.Pause
                L12_54(L7_49[L11_53], false)
              end
              while true do
                if L8_50 then
                  L8_50()
                  else
                    L6_48 = SSA
                    L6_48 = L6_48.CreateMapWeaponEffect
                    L7_49 = L4_46
                    L6_48 = L6_48(L7_49, L8_50, L9_51, L10_52)
                    L7_49 = SSA
                    L7_49 = L7_49.Pause
                    L7_49(L8_50, L9_51)
                    while true do
                      L7_49 = SSA
                      L7_49 = L7_49.IsPlaying
                      L7_49 = L7_49(L8_50)
                      if L7_49 then
                        L7_49 = SSA
                        L7_49 = L7_49.CurrentTime
                        L7_49 = L7_49(L8_50)
                      end
                      if L7_49 < 0.2 then
                        L7_49 = Utility
                        L7_49 = L7_49.BreakScript
                        L7_49()
                      end
                    end
                    L7_49 = MapWeaponEffectType
                    L7_49 = L7_49.SelfExplosion
                    if A2_44 == L7_49 then
                      L7_49 = SSA
                      L7_49 = L7_49.GetDisappearTime
                      L7_49 = L7_49(L8_50)
                      while true do
                        if L7_49 > L8_50 then
                          L8_50()
                        end
                      end
                      L8_50(L9_51, L10_52)
                    end
                    while true do
                      L7_49 = SSA
                      L7_49 = L7_49.IsPlaying
                      L7_49 = L7_49(L8_50)
                      if L7_49 then
                        L7_49 = Utility
                        L7_49 = L7_49.BreakScript
                        L7_49()
                      end
                    end
                  end
                end
              end
          end
        end
      end
    end
end
MapWeaponEffect = L0_0
function L0_0()
  local L0_55, L1_56, L2_57, L3_58, L4_59, L5_60, L6_61, L7_62, L8_63
  L0_55 = Battle
  L0_55 = L0_55.MainAttacker
  L0_55 = L0_55()
  L1_56 = SSA
  L1_56 = L1_56.CreateSSAonUnit
  L2_57 = 921
  L3_58 = L0_55
  L1_56 = L1_56(L2_57, L3_58, L4_59)
  L2_57 = {}
  L3_58 = Battle
  L3_58 = L3_58.TargetUnits
  L3_58 = L3_58()
  for L7_62, L8_63 in L4_59(L5_60) do
    L2_57[L7_62] = SSA.CreateSSAonUnit(922, L8_63, true)
  end
  L4_59(L5_60, L6_61)
  L4_59(L5_60, L6_61)
  while true do
    if L4_59 then
      L4_59()
    end
  end
  for L7_62 = 1, #L2_57 do
    L8_63 = SSA
    L8_63 = L8_63.Pause
    L8_63(L2_57[L7_62], false)
    L8_63 = Utility
    L8_63 = L8_63.Wait
    L8_63(0.1)
  end
  while true do
    if L4_59 then
      L4_59()
    end
  end
end
DragonMapWeapon = L0_0
function L0_0(A0_64, A1_65)
  local L2_66, L3_67, L4_68, L5_69
  L2_66 = Unit
  L2_66 = L2_66.GetMachineId
  L3_67 = A0_64
  L2_66 = L2_66(L3_67)
  L3_67 = Unit
  L3_67 = L3_67.GetCharacterId
  L4_68 = A0_64
  L3_67 = L3_67(L4_68)
  if L2_66 == "G5190U00103" and L3_67 == "G5190C00100" then
    L4_68 = ""
    if A1_65 == 12 then
      L4_68 = "data/sound/voice/BTL/G5190C00100/W0301"
    else
      L4_68 = "data/sound/voice/BTL/G5190C00100/Z0101"
    end
    L5_69 = Voice
    L5_69 = L5_69.PlayFromPath
    L5_69 = L5_69(L4_68)
    if Voice.IsPrepare then
      Voice.Pause(L5_69, false)
    end
    while Voice.IsPlaying(L5_69) do
      Utility.BreakScript()
    end
  end
end
PlayDragonVoice = L0_0
function L0_0(A0_70, A1_71, A2_72, A3_73)
  local L4_74, L5_75, L6_76, L7_77, L8_78, L9_79, L10_80, L11_81, L12_82, L13_83, L14_84, L15_85, L16_86, L17_87, L18_88, L19_89
  L4_74 = Unit
  L4_74 = L4_74.GetUnit
  L5_75 = A0_70
  L4_74 = L4_74(L5_75)
  L5_75 = Unit
  L5_75 = L5_75.GetDisplaySize
  L6_76 = L4_74
  L5_75 = L5_75(L6_76)
  L6_76 = Unit
  L6_76 = L6_76.GetPosition
  L7_77 = L4_74
  L6_76 = L6_76(L7_77)
  L7_77 = Unit
  L7_77 = L7_77.GetOccupiedRange
  L8_78 = L4_74
  L7_77 = L7_77(L8_78)
  L8_78 = {}
  L9_79 = {}
  L10_80 = 1
  if L5_75 == L11_81 then
    L10_80 = 3
  elseif L5_75 > L11_81 then
    L10_80 = 5
  end
  for L14_84 = 1, L10_80 do
    L15_85 = SSA
    L15_85 = L15_85.CreateSSANotReady
    L16_86 = 900
    L17_87 = true
    L15_85 = L15_85(L16_86, L17_87)
    L8_78[L14_84] = L15_85
    if L10_80 > 1 then
      L15_85 = SSA
      L15_85 = L15_85.CreateSSANotReady
      L16_86 = 901
      L17_87 = true
      L15_85 = L15_85(L16_86, L17_87)
      L9_79[L14_84] = L15_85
    end
  end
  if L5_75 >= L11_81 then
    if A2_72 then
    end
    L15_85 = L4_74
    L16_86 = true
    L9_79[L12_82] = L13_83
  else
    if A2_72 then
    end
    L15_85 = true
    L9_79[1] = L12_82
  end
  while not L11_81 do
    for L15_85, L16_86 in L12_82(L13_83) do
      if L11_81 then
        L17_87 = System
        L17_87 = L17_87.IsReadySSA
        L18_88 = L16_86
        L17_87 = L17_87(L18_88)
      end
    end
    L12_82(L13_83)
  end
  while not L11_81 do
    for L15_85, L16_86 in L12_82(L13_83) do
      if L11_81 then
        L17_87 = System
        L17_87 = L17_87.IsReadySSA
        L18_88 = L16_86
        L17_87 = L17_87(L18_88)
      end
    end
    L12_82(L13_83)
  end
  for L15_85 = 1, L10_80 do
    L16_86 = math
    L16_86 = L16_86.random
    L16_86 = L16_86()
    L17_87 = L7_77.Right
    L18_88 = L7_77.Left
    L17_87 = L17_87 - L18_88
    L16_86 = L16_86 * L17_87
    L17_87 = math
    L17_87 = L17_87.random
    L17_87 = L17_87()
    L18_88 = L7_77.Bottom
    L19_89 = L7_77.Top
    L18_88 = L18_88 - L19_89
    L17_87 = L17_87 * L18_88
    L18_88 = math
    L18_88 = L18_88.ceil
    L19_89 = L6_76.X
    L19_89 = L16_86 + L19_89
    L19_89 = L19_89 + L7_77.Left
    L18_88 = L18_88(L19_89)
    L19_89 = math
    L19_89 = L19_89.ceil
    L19_89 = L19_89(L17_87 + L6_76.Y + L7_77.Top)
    SSA.CellPosition(L8_78[L15_85], L18_88, L19_89)
    if L15_85 ~= #L9_79 then
      L16_86 = math.random() * (L7_77.Right - L7_77.Left)
      L17_87 = math.random() * (L7_77.Bottom - L7_77.Top)
      L18_88 = math.ceil(L16_86 + L6_76.X + L7_77.Left)
      L19_89 = math.ceil(L17_87 + L6_76.Y + L7_77.Top)
      SSA.CellPosition(L9_79[L15_85], L18_88, L19_89)
    end
  end
  if A1_71 then
    L15_85 = true
    L16_86 = true
    L17_87 = true
    L12_82(L13_83, L14_84, L15_85, L16_86, L17_87)
  end
  L12_82(L13_83, L14_84)
  while true do
    while true do
      if L12_82 < L13_83 then
        if L13_83 > 0.4 then
          L15_85 = false
          L13_83(L14_84, L15_85)
        end
        L13_83()
      end
    end
  end
  while true do
    if L13_83 then
      L13_83()
    end
  end
  if L13_83 > 1 then
    L15_85 = false
    L13_83(L14_84, L15_85)
    while true do
      if L13_83 < L14_84 then
        L15_85 = L9_79[L13_83]
        if L14_84 > 0.4 then
          L15_85 = L9_79[L13_83]
          L16_86 = false
          L14_84(L15_85, L16_86)
        end
        L14_84()
      end
    end
  end
  if A2_72 then
  end
  L15_85 = #L9_79
  L15_85 = L9_79[L15_85]
  L16_86 = false
  L14_84(L15_85, L16_86)
  L15_85 = #L9_79
  L15_85 = L9_79[L15_85]
  L16_86 = Priority3D
  L16_86 = L16_86.Explode
  L14_84(L15_85, L16_86)
  while true do
    L15_85 = #L9_79
    L15_85 = L9_79[L15_85]
    if L13_83 > L14_84 then
      L14_84()
    end
  end
end
DisappearExplodeEffect = L0_0
function L0_0(A0_90, A1_91, A2_92)
  local L3_93, L4_94, L5_95, L6_96, L7_97, L8_98
  L3_93 = Unit
  L3_93 = L3_93.GetUnit
  L4_94 = A0_90
  L3_93 = L3_93(L4_94)
  if A1_91 then
    L4_94 = Cursor
    L4_94 = L4_94.MoveToUnit
    L5_95 = L3_93
    L6_96 = 0
    L7_97 = true
    L8_98 = true
    L4_94(L5_95, L6_96, L7_97, L8_98, true)
  end
  if A2_92 then
    L4_94 = Unit
    L4_94 = L4_94.GetDisplaySize
    L5_95 = L3_93
    L4_94 = L4_94(L5_95)
    L5_95 = Unit
    L5_95 = L5_95.GetOccupiedRange
    L6_96 = L3_93
    L5_95 = L5_95(L6_96)
    L6_96 = 1
    L7_97 = DisplaySizeType
    L7_97 = L7_97.XL
    if L4_94 == L7_97 then
      L6_96 = 3
    else
      L7_97 = DisplaySizeType
      L7_97 = L7_97.XL
      if L4_94 > L7_97 then
        L6_96 = 5
      end
    end
    L7_97 = math
    L7_97 = L7_97.Min
    L8_98 = L5_95.Bottom
    L8_98 = L8_98 - L5_95.Top
    L7_97 = L7_97(L8_98, L5_95.Right - L5_95.Left)
    L8_98 = SSA
    L8_98 = L8_98.MultiEffectAroundUnit
    L8_98 = L8_98(900, L3_93, L7_97, L6_96, 0.4)
    Utility.WaitProcedure(L8_98)
  else
    L4_94 = Unit
    L4_94 = L4_94.Blink
    L5_95 = L3_93
    L6_96 = 0.1
    L7_97 = 0.8
    L4_94(L5_95, L6_96, L7_97)
  end
end
DisappearNonExplodeEffect = L0_0
