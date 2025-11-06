-- Initial setup
Unit = {}

---
-- Simple passthrough functions to System
---

function Unit.GetUnit(unitId)
  return System.GetUnit(unitId)
end

function Unit.GetAllUnits(filter)
  return System.GetAllUnits(filter)
end

function Unit.GetUnitsByAdmiId(adminId, filter)
  return System.GetUnitsByAdmiId(adminId, filter)
end

function Unit.GetUnitsByGroupName(groupName, filter)
  return System.GetUnitsByGroupName(groupName, filter)
end

function Unit.GetUnitsByArea(area)
  return System.GetUnitsByArea(area)
end

---
-- Functions with more complex logic
---

function Unit.GetUnitsByArmyType(armyType)
  -- NOTE: The original decompiled loop was corrupt.
  -- This is a logical reconstruction of the inferred intent.
  local results = {}
  local allUnits = Unit.GetAllUnits() -- Assuming GetAllUnits() returns a list
  if allUnits then
    for _, unit in ipairs(allUnits) do
      if Unit.GetArmyType(unit) == armyType and Unit.IsValidMap(unit) then
        table.insert(results, unit)
      end
    end
  end
  return results
end

function Unit.AppearInstant(...)
  for i = 1, select("#", ...) do
    local unitId = select(i, ...)
    local unit = System.GetUnit(unitId)
    local proc = System.Appear(unit, UnitAppearType.Instant)
    Utility.WaitProcedure(proc)
  end
end

function Unit.AppearInstantGroup(groupName)
  -- NOTE: The original decompiled loop was corrupt.
  -- This is a logical reconstruction.
  local unitList = System.GetUnitsByGroupName(groupName)
  if unitList then
    for _, unitHandle in ipairs(unitList) do
      local unit = System.GetUnit(unitHandle)
      local proc = System.Appear(unit, UnitAppearType.Instant)
      Utility.WaitProcedure(proc)
    end
  end
end

function Unit.Appear(...)
  for i = 1, select("#", ...) do
    local unitId = select(i, ...)
    local unit = System.GetUnit(unitId)
    local proc = System.Appear(unit, UnitAppearType.Normal)
    Utility.WaitProcedure(proc)
  end
end

function Unit.AppearFast(delay, ...)
  for i = 1, select("#", ...) do
    local unit = System.GetUnit(select(i, ...))
    local proc = System.Appear(unit, UnitAppearType.Normal)
    Utility.Wait(delay)
  end
  -- Original decompiled code had a call to nil(nil) here, which was removed.
end

function Unit.AppearGroup(groupName)
  -- NOTE: The original decompiled loop was corrupt.
  -- This is a logical reconstruction.
  local unitList = System.GetUnitsByGroupName(groupName)
  if unitList then
    for _, unitHandle in ipairs(unitList) do
      local unit = System.GetUnit(unitHandle)
      local proc = System.Appear(unit, UnitAppearType.Normal)
      Utility.WaitProcedure(proc)
    end
  end
end

function Unit.AppearSet(...)
  for i = 1, select("#", ...) do
    local unitId = select(i, ...)
    local unit = System.GetUnit(unitId)
    Map.SetIndex(Unit.GetMapIndex(unit))
    local proc = System.Appear(unit, UnitAppearType.MoveCamera)
    Utility.WaitProcedure(proc)
  end
end

function Unit.AppearSetGroup(groupName)
  -- NOTE: The original decompiled loop was corrupt.
  -- This is a logical reconstruction.
  local unitList = System.GetUnitsByGroupName(groupName)
  if unitList then
    for _, unitHandle in ipairs(unitList) do
      local unit = System.GetUnit(unitHandle)
      local appearType = UnitAppearType.Normal

      local isLeader = Unit.IsLeader(unit) or Unit.IsWs(unit) or Unit.IsRaidGroupLeader(unit)

      if isLeader then
        Map.SetIndex(Unit.GetMapIndex(unit))
        appearType = UnitAppearType.MoveCamera
      end

      local proc = System.Appear(unit, appearType)
      Utility.WaitProcedure(proc)
    end
  end
end

function Unit.AppearWithEffectId(effectId, ...)
  for i = 1, select("#", ...) do
    local unitId = select(i, ...)
    local unit = System.GetUnit(unitId)
    local proc = System.AppearWithEffectId(unit, UnitAppearType.Normal, effectId)
    Utility.WaitProcedure(proc)
  end
end

function Unit.AppearSetWithEffectId(effectId, ...)
  for i = 1, select("#", ...) do
    local unitId = select(i, ...)
    local unit = System.GetUnit(unitId)
    Map.SetIndex(Unit.GetMapIndex(unit))
    local proc = System.AppearWithEffectId(unit, UnitAppearType.MoveCamera, effectId)
    Utility.WaitProcedure(proc)
  end
end

function Unit.AppearReplace(unitToAppearId, unitToDisappearId, appearType)
  local unitToAppear = System.GetUnit(unitToAppearId)
  local unitToDisappear = System.GetUnit(unitToDisappearId)

  local pos = Unit.GetPosition(unitToDisappear)
  local dir = Unit.GetDirection(unitToDisappear)
  local regScore = Unit.GetRegistrationScore(unitToDisappear)

  System.Disappear(unitToDisappear, appearType, false)
  Unit.AppearJump(unitToAppearId, Map.GetIndex(), pos.X, pos.Y, dir, appearType)
  Unit.SetRegistrationScore(unitToAppear, regScore)
end

function Unit.AppearJump(unitId, mapIndex, x, y, direction, appearType)
  if appearType ~= UnitAppearType.Instant then
    Map.SetIndex(mapIndex)
  end

  local unit = System.GetUnit(unitId)
  local proc = System.AppearJump(unit, mapIndex, x, y, direction, appearType)
  Utility.WaitProcedure(proc)
end

function Unit.DisappearInstant(...)
  for i = 1, select("#", ...) do
    local unit = System.GetUnit(select(i, ...))
    local proc = System.Disappear(unit, UnitAppearType.Instant, false)
    Utility.WaitProcedure(proc)
  end
end

function Unit.Disappear(...)
  for i = 1, select("#", ...) do
    local unit = System.GetUnit(select(i, ...))
    local proc = System.Disappear(unit, UnitAppearType.Normal, false)
    Utility.WaitProcedure(proc)
  end
end

function Unit.DisappearFast(delay, ...)
  for i = 1, select("#", ...) do
    local unit = System.GetUnit(select(i, ...))
    local proc = System.Disappear(unit, UnitAppearType.Normal, false)
    Utility.Wait(delay)
  end
  -- Original decompiled code had a call to nil(nil) here, which was removed.
end

function Unit.DisappearSet(...)
  for i = 1, select("#", ...) do
    local unit = System.GetUnit(select(i, ...))
    if Unit.IsAlive(unit) then
      Map.SetIndex(Unit.GetMapIndex(unit))
      local proc = System.Disappear(unit, UnitAppearType.MoveCamera, false)
      Utility.WaitProcedure(proc)
    end
  end
end

function Unit.DisappearSetWithEffectId(effectId, ...)
  for i = 1, select("#", ...) do
    local unit = System.GetUnit(select(i, ...))
    if Unit.IsAlive(unit) then
      Map.SetIndex(Unit.GetMapIndex(unit))
      local proc = System.DisappearWithEffectId(unit, effectId)
      Utility.WaitProcedure(proc)
    end
  end
end

function Unit.DisappearFake(...)
  for i = 1, select("#", ...) do
    local unit = System.GetUnit(select(i, ...))
    if Unit.IsAlive(unit) then
      Map.SetIndex(Unit.GetMapIndex(unit))
      local proc = System.Disappear(unit, UnitAppearType.MoveCamera, true)
      Utility.WaitProcedure(proc)
    end
  end
end

function Unit.DisappearFakeInstant(...)
  for i = 1, select("#", ...) do
    local unit = System.GetUnit(select(i, ...))
    local proc = System.Disappear(unit, UnitAppearType.Instant, true)
    Utility.WaitProcedure(proc)
  end
end

function Unit.Kill(unitId, ...)
  local appearType = UnitAppearType.Explosion

  if select("#", ...) >= 1 then
    local forceMasterExplosion = select(1, ...)
    if forceMasterExplosion then
      appearType = UnitAppearType.MasterExplosion
    end
  end

  local unit = System.GetUnit(unitId)
  if Unit.IsMaster(unit) then
    appearType = UnitAppearType.MasterExplosion
  end

  if Unit.IsAlive(unit) then
    Map.SetIndex(Unit.GetMapIndex(unit))
    local proc = System.Disappear(unit, appearType, false, false)
    Utility.WaitProcedure(proc)
  end
end

function Unit.KillMulti(...)
  local proc
  for i = 1, select("#", ...) do
    local unit = System.GetUnit(select(i, ...))
    proc = System.Disappear(unit, UnitAppearType.Explosion, false, true)
  end
  -- Original decompiled code had a call to nil(nil) here, which was removed.
end

function Unit.BombEffect(unit, ...)
  -- NOTE: The 'else' block of this function was severely mangled
  -- by the decompiler and its logic is likely incorrect/corrupt.
  -- The first half has been cleaned up.

  local ssaHandle = 0
  local displaySize = Unit.GetDisplaySize(unit)

  local forceMasterEffect = false
  if select("#", ...) >= 1 then
    forceMasterEffect = select(1, ...)
  end

  if displaySize <= DisplaySizeType.LL then
    local ssaId
    if Unit.IsMaster(unit) or forceMasterEffect then
      ssaId = 902 -- Master/Forced effect
    else
      ssaId = 901 -- Standard effect
    end
    ssaHandle = SSA.CreateSSAonUnit(ssaId, unit)
    Utility.Wait(0.5)
    Unit.DisappearInstant(unit)
  else
    -- This 'else' block is likely corrupt from decompilation.
    -- Variables L7_161, L8_162, etc. are used without being initialized.
    local L4_158 = 3
    local L5_159 = {}
    L5_159.Left = -1
    L5_159.Top = -1
    L5_159.Right = 1
    L5_159.Bottom = 1
    local L6_160 = Unit
    L6_160 = L6_160.GetPosition
    L6_160 = L6_160(L7_161) -- L7_161 is nil
    if displaySize == L7_161 then -- L7_161 is nil
      L4_158 = 5
      L5_159 = L7_161
    end
    for L10_164 = 1, L4_158 do
      local L11_165 = math
      L11_165 = L11_165.random
      L11_165 = L11_165()
      local L12_166 = L5_159.Right
      local L13_167 = L5_159.Left
      L12_166 = L12_166 - L13_167
      L11_165 = L11_165 * L12_166
      L12_166 = L5_159.Left
      L11_165 = L11_165 + L12_166
      L11_165 = L11_165 + 0.5
      L12_166 = math
      L12_166 = L12_166.random
      L12_166 = L12_166()
      L13_167 = L5_159.Bottom
      local L14_168 = L5_159.Top
      L13_167 = L13_167 - L14_168
      L12_166 = L12_166 * L13_167
      L13_167 = L5_159.Top
      L12_166 = L12_166 + L13_167
      L12_166 = L12_166 + 0.5
      L13_167 = L6_160.X
      L13_167 = L11_165 + L13_167
      L14_168 = Grid
      L14_168 = L14_168.Size
      L14_168 = L14_168()
      L13_167 = L13_167 * L14_168
      L14_168 = L6_160.Y
      L14_168 = L12_166 + L14_168
      local L15_169 = Grid
      L15_169 = L15_169.Size
      L15_169 = L15_169()
      L14_168 = L14_168 * L15_169
      L15_169 = SSA
      L15_169 = L15_169.CreateSSA
      L15_169 = L15_169(901)
      SSA.Position(L15_169, L13_167, L14_168)
      Utility.Wait(0.2)
    end
    if L7_161 or forceMasterEffect then -- L7_161 is nil
      ssaHandle = L7_161
      L7_161(L8_162) -- nil(nil)
    else
      ssaHandle = L7_161
      L7_161(L8_162) -- nil(nil)
    end
    L7_161(L8_162) -- nil(nil)
  end
  return ssaHandle
end

function Unit.BiriBiriKill(unitId)
  local unit = System.GetUnit(unitId)
  Map.SetIndex(Unit.GetMapIndex(unit))
  local proc = System.KillUnit(unit, true)
  Utility.WaitProcedure(proc)
end

function Unit.GetParameter(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetParameter(unit)
end

function Unit.SetParameter(unitId, parameter)
  local unit = System.GetUnit(unitId)
  System.SetParameter(unit, parameter)
end

function Unit.GetCharacterParameter(unitId, ...)
  local unit = System.GetUnit(unitId)
  local crewType = CharaterCrewType.Captain
  if select("#", ...) >= 1 then
    crewType = select(1, ...)
  end
  return System.GetCharacterParameter(unit, crewType)
end

function Unit.SetCharacterParameter(unitId, parameter, ...)
  local unit = System.GetUnit(unitId)
  local crewType = CharaterCrewType.Captain
  if select("#", ...) >= 1 then
    crewType = select(1, ...)
  end
  System.SetCharacterParameter(unit, crewType, parameter)
end

function Unit.SetOptionParts(unitId, partsId, value)
  local unit = System.GetUnit(unitId)
  System.SetOptionParts(unit, partsId, value)
end

function Unit.SetAnimation(unitId, animationName, loop)
  local unit = System.GetUnit(unitId)
  while not Unit.IsReadyKomaAnimation(unit) and Unit.IsAlive(unit) do
    Utility.BreakScript()
  end
  System.SetKomaAnimation(unit, animationName, loop)
  while not Unit.IsReadyKomaAnimation(unit) and Unit.IsAlive(unit) do
    Utility.BreakScript()
  end
end

function Unit.RemoveLoopPoint(unitId)
  local unit = System.GetUnit(unitId)
  while not System.RemoveLoopPointKomaAnimation(unit) do
    Utility.BreakScript()
  end
end

function Unit.ShowWarningHp(unitId)
  local unit = System.GetUnit(unitId)
  return System.ShowWarningHp(unit)
end

function Unit.GetDirection(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetUnitNumber(unit, 1)
end

function Unit.SetDirection(unitId, direction)
  local unit = System.GetUnit(unitId)
  System.SetUnitNumber(unit, 1, direction)
end

function Unit.GetRegistrationScore(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetUnitNumber(unit, 3)
end

function Unit.SetRegistrationScore(unitId, score)
  local unit = System.GetUnit(unitId)
  System.SetUnitNumber(unit, 3, score)
end

function Unit.GetPosition(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetUnitPosition(unit)
end

function Unit.GetToolPosition(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetUnitToolPosition(unit)
end

function Unit.GetPositionBeforeExplosion(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetUnitPositionBeforeExplosion(unit)
end

function Unit.GetName(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetUnitName(unit)
end

function Unit.GetMachineId(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetMachineId(unit)
end

function Unit.GetCharacterId(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetCharacterId(unit)
end

function Unit.GetControlId(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetUnitNumber(unit, 0)
end

function Unit.Move(unitId, x, y, speed, param4, param5, moveCursor, ...)
  local unit = System.GetUnit(unitId)
  Map.SetIndex(Unit.GetMapIndex(unit))

  local param7 = false
  if select("#", ...) >= 1 then
    param7 = select(1, ...)
  end

  if moveCursor then
    local pos = Unit.GetPosition(unitId)
    Cursor.SetPosition(pos.X, pos.Y, 0, false, true)
    local cursorSpeed = math.sqrt((pos.X - x) ^ 2 + (pos.Y - y) ^ 2) / ((math.abs(pos.X - x) + math.abs(pos.Y - y)) / speed * 0.1)
    Cursor.SetPosition(x, y, cursorSpeed, true, false)
  end

  local proc = System.MoveUnit(unit, x, y, speed, param4, param5, param7)
  Utility.WaitProcedure(proc)
end

function Unit.MoveMapToMap(fromMapIndex, toMapIndex)
  -- NOTE: The original decompiled loop was corrupt.
  -- This is a logical reconstruction.
  local unitList = Map.GetUnitsByMapIndex(fromMapIndex)
  if unitList then
    for _, unit in ipairs(unitList) do
      local pos = Unit.GetPosition(unit)
      local dir = Unit.GetDirection(unit)
      local mp = Unit.GetMp(unit)
      local tension = Unit.GetTension(unit)

      local procDisappear = System.DisappearWithoutClearSKill(unit, UnitAppearType.Instant)
      Utility.WaitProcedure(procDisappear)

      local procAppear = Unit.AppearJump(unit, toMapIndex, pos.X, pos.Y, dir, UnitAppearType.Instant)
      Utility.WaitProcedure(procAppear)

      Unit.SetMp(unit, mp)
      if tension == TensionType.SuperBlow then
        Unit.SetSuperBlowTension(unit, true)
      end
    end
  end
end

function Unit.FindAroundUnit(unitId, range)
  local unit = System.GetUnit(unitId)
  return System.FindAroundUnit(unit, range)
end

function Unit.ChangeExam(unitId)
  local unit = System.GetUnit(unitId)
  Cursor.MoveToUnit(unit, 0, true, true)
  local proc = System.ChangeExam(unit)
  Utility.WaitProcedure(proc)
end

function Unit.TransformMachine(unitId, machineId)
  local unit = System.GetUnit(unitId)
  local proc = System.TransformMachine(unit, machineId)
  Utility.WaitProcedure(proc)
end

function Unit.GetRandomPlayerUnit()
  return System.GetRandomPlayerUnit()
end

function Unit.ForbidWeapon(unitId, weaponId, forbidden)
  local unit = System.GetUnit(unitId)
  System.ForbidWeapon(unit, weaponId, forbidden)
end

function Unit.ForbidAbility(unitId, abilityId, forbidden)
  local unit = System.GetUnit(unitId)
  System.ForbidAbility(unit, abilityId, forbidden)
end

function Unit.IsAlive(...)
  local allAlive = true
  for i = 1, select("#", ...) do
    local unit = System.GetUnit(select(i, ...))
    allAlive = allAlive and System.GetUnitFlag(unit, 0)
  end
  return allAlive
end

function Unit.IsWs(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetUnitFlag(unit, 1)
end

function Unit.IsLeader(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetUnitFlag(unit, 2)
end

function Unit.HasDeadEvent(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetUnitFlag(unit, 3)
end

function Unit.IsPlayer(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetUnitFlag(unit, 4)
end

function Unit.IsDoneWarningHp(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetUnitFlag(unit, 5)
end

function Unit.HasStageWarningHp(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetUnitFlag(unit, 6)
end

function Unit.IsInWarShip(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetUnitFlag(unit, 7)
end

function Unit.GetFinishedAction(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetUnitFlag(unit, 8)
end

function Unit.SetFinishedAction(unitId, finished)
  local unit = System.GetUnit(unitId)
  System.SetUnitFlag(unit, 8, finished)
end

function Unit.IsRaisedWhiteFlag(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetUnitFlag(unit, 9)
end

function Unit.GetMapIndex(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetUnitNumber(unit, 2)
end

function Unit.GetBgmNo(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetUnitNumber(unit, 4)
end

function Unit.SetCriticalRate(unitId, rate)
  local unit = System.GetUnit(unitId)
  System.SetUnitNumber(unit, 5, rate)
end

function Unit.SetDetectRange(unitId, range)
  local unit = System.GetUnit(unitId)
  System.SetUnitNumber(unit, 6, range)
end

function Unit.GetTension(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetUnitNumber(unit, 7)
end

function Unit.SetTension(unitId, tension)
  local unit = System.GetUnit(unitId)
  System.SetUnitNumber(unit, 7, tension)
end

function Unit.SetForbidAct(unitId, forbid)
  local unit = System.GetUnit(unitId)
  System.SetUnitFlag(unit, 10, forbid)
end

function Unit.GetHp(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetUnitNumber(unit, 9)
end

function Unit.SetHp(unitId, hp)
  local unit = System.GetUnit(unitId)
  System.SetUnitNumber(unit, 9, hp)
end

function Unit.GetEn(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetUnitNumber(unit, 10)
end

function Unit.SetEn(unitId, en)
  local unit = System.GetUnit(unitId)
  System.SetUnitNumber(unit, 10, en)
end

function Unit.GetMp(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetUnitNumber(unit, 12)
end

function Unit.SetMp(unitId, mp)
  local unit = System.GetUnit(unitId)
  System.SetUnitNumber(unit, 12, mp)
end

function Unit.GetDisplaySize(unitId)
  local unit = System.GetUnit(unitId)
  -- NOTE: The original decompiled logic here was bizarre:
  -- if System.GetUnitNumber(unit, 8) < 3 then
  -- else
  -- end
  -- return 0 - 3
  -- This appears to be a no-op 'if' block followed by 'return -3'.
  -- Replicating the (likely broken) logic:
  if System.GetUnitNumber(unit, 8) < 3 then
    -- Do nothing
  else
    -- Do nothing
  end
  return 0 - 3 -- Always returns -3?
end

function Unit.GetOccupiedRange(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetOccupiedRange(unit)
end

function Unit.SetAttackTarget(unitId, aiType, target, priority)
  local unit = System.GetUnit(unitId)
  System.SetAttackTarget(unit, aiType, target, priority)
end

function Unit.SetNonAttackTarget(unitId, aiType, target, priority)
  local unit = System.GetUnit(unitId)
  System.SetNonAttackTarget(unit, aiType, target, priority)
end

function Unit.SetNoMoveSetting(unitId, aiType, target, priority, range)
  local unit = System.GetUnit(unitId)
  System.SetNoMoveSetting(unit, aiType, target, priority, range)
end

function Unit.SetLoopSetting(unitId, setting)
  local unit = System.GetUnit(unitId)
  System.SetLoopSetting(unit, setting)
end

function Unit.SetLoopCountSetting(unitId, count)
  local unit = System.GetUnit(unitId)
  System.SetLoopCountSetting(unit, count)
end

function Unit.SetMovePositionSetting(unitId, aiType, x, y, range)
  local unit = System.GetUnit(unitId)
  System.SetMovePositionSetting(unit, aiType, x, y, range)
end

function Unit.SetFollowSetting(unitId, followType, target)
  local unit = System.GetUnit(unitId)
  System.SetFollowSetting(unit, followType, target)
end

function Unit.SetLandAptitude(unitId, landType, aptitude)
  local unit = System.GetUnit(unitId)
  System.SetLandAptitude(unit, landType, aptitude)
end

function Unit.SetWeaponParameter(unitId, weaponId, paramType, value)
  local unit = System.GetUnit(unitId)
  System.SetWeaponParameter(unit, weaponId, paramType, value)
end

function Unit.SetAllWeaponPower(unitId, power, turn)
  local unit = System.GetUnit(unitId)
  System.SetAllWeaponPower(unit, power, turn)
end

function Unit.IsSfs(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetUnitFlag(unit, 11)
end

function Unit.SetVisible(unitId, visible)
  local unit = System.GetUnit(unitId)
  System.SetUnitFlag(unit, 12, visible)
end

function Unit.SetPiriPiri(unitId, piri)
  local unit = System.GetUnit(unitId)
  System.SetUnitFlag(unit, 13, piri)
end

function Unit.DoneAnimation(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetUnitFlag(unit, 14)
end

function Unit.SetUnitShake(unitId, shake)
  local unit = System.GetUnit(unitId)
  System.SetUnitFlag(unit, 15, shake)
end

function Unit.GetArmyType(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetUnitNumber(unit, 11)
end

function Unit.IsMaster(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetUnitFlag(unit, 16)
end

function Unit.SetFloating(unitId, isFloating, ...)
  local unit = System.GetUnit(unitId)

  -- Check for optional 'wait' argument
  local wait = false
  if select("#", ...) >= 1 then
    wait = select(1, ...)
  end

  if wait and not Utility.IsEventSkip() then
    local proc = System.FloatingEffect(unit, isFloating)
    Utility.WaitProcedure(proc)
  else
    System.SetUnitFlag(unit, 17, isFloating)
  end
end

function Unit.TurnAroundUnit(unitId, direction)
  local unit = System.GetUnit(unitId)
  System.TurnAroundUnit(unit, direction)

  -- Wait for the turn to complete
  while Unit.IsTurnAround(unit) do
    Utility.BreakScript()
  end
end

function Unit.SetForbidMove(unitId, forbid)
  local unit = System.GetUnit(unitId)
  System.SetUnitFlag(unit, 18, forbid)
end

function Unit.IsAppeared(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetUnitFlag(unit, 19)
end

function Unit.IsChanceStep(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetUnitFlag(unit, 20)
end

function Unit.GetChanceStep(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetUnitNumber(unit, 13)
end

function Unit.SetChanceStep(unitId, step)
  local unit = System.GetUnit(unitId)
  return System.SetUnitNumber(unit, 13, step)
end

function Unit.GetWarningHpPercent(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetUnitNumber(unit, 14)
end

function Unit.SetWarningHpPercent(unitId, percent)
  local unit = System.GetUnit(unitId)
  return System.SetUnitNumber(unit, 14, percent)
end

function Unit.SetHighPriority(unitId, highPriority)
  local unit = System.GetUnit(unitId)
  System.SetUnitFlag(unit, 21, highPriority)
end

function Unit.IsReadyKomaAnimation(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetUnitFlag(unit, 22)
end

function Unit.IsImportant(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetUnitFlag(unit, 23)
end

function Unit.IsValidMap(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetUnitFlag(unit, 24)
end

function Unit.IsRaidGroup(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetUnitFlag(unit, 25)
end

function Unit.SetRaidGroup(unitId, isRaidGroup)
  local unit = System.GetUnit(unitId)
  return System.SetUnitFlag(unit, 25, isRaidGroup)
end

function Unit.IsRaidGroupLeader(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetUnitFlag(unit, 26)
end

function Unit.IsTurnAround(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetUnitFlag(unit, 27)
end

function Unit.SetForbidAttack(unitId, forbid)
  local unit = System.GetUnit(unitId)
  System.SetUnitFlag(unit, 29, forbid)
end

function Unit.SetForbidTurn(unitId, forbid)
  local unit = System.GetUnit(unitId)
  System.SetUnitFlag(unit, 30, forbid)
end

function Unit.SetPhaseShiftEnable(unitId, enable)
  local unit = System.GetUnit(unitId)
  System.SetUnitFlag(unit, 31, enable)
end

function Unit.GetPhaseShiftEnable(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetUnitFlag(unit, 31)
end

function Unit.SetEnableShadow(unitId, enable)
  local unit = System.GetUnit(unitId)
  System.SetUnitFlag(unit, 32, enable)
end

function Unit.SetSuperBlowTension(unitId, enable)
  local unit = System.GetUnit(unitId)
  System.SetUnitFlag(unit, 33, enable)
end

function Unit.SetFloatingWater(unitId, isFloating, ...)
  local unit = System.GetUnit(unitId)

  -- Check for optional 'wait' argument
  local wait = false
  if select("#", ...) >= 1 then
    wait = select(1, ...)
  end

  if wait and not Utility.IsEventSkip() then
    local proc = System.WaterEffect(unit, isFloating)
    Utility.WaitProcedure(proc)
  else
    System.SetUnitFlag(unit, 28, isFloating)
  end
end

function Unit.IsValidPosition(unitId)
  local unit = System.GetUnit(unitId)
  local pos = Unit.GetPosition(unit)
  return pos.X >= 0 and pos.Y >= 0
end

function Unit.DamageHp(unitId, damageAmount)
  local unit = System.GetUnit(unitId)

  -- Play damage value effect
  local proc1 = System.PlayDamageValueEffect(unit, damageAmount)
  Utility.WaitProcedure(proc1)

  -- Animate HP bar
  local proc2 = System.AnimateHpBar(unit, damageAmount)
  Utility.WaitProcedure(proc2)

  -- Apply damage
  local newHp = Unit.GetHp(unit) - damageAmount
  Unit.SetHp(unit, newHp)

  local isGameOver = false
  if newHp <= 0 then
    if Unit.HasDeadEvent(unit) then
      OnDiedEvent(unit)
    elseif Unit.IsPlayer(unit) and not Unit.IsSfs(unit) then
      OutEvent(0, unit, 0, OutEventType.Explosion, true)
    else
      Unit.BiriBiriKill(unit)
    end
    isGameOver = Unit.IsImportant(unit)
  end

  if Stage.IsGameOver() or isGameOver then
    GameOverEvent()
    System.GameOver()
  else
    BeforeEndWithoutBattleControl()
  end
end

function Unit.UseMapWeapon(unitId, weaponId)
  local unit = System.GetUnit(unitId)
  local proc = System.UseMapWeapon(unit, weaponId)
  Utility.WaitProcedure(proc)
end

function Unit.ShowWeaponRange(unitId)
  local unit = System.GetUnit(unitId)
  System.ShowWeaponRange(unit, false)
end

function Unit.HideWeaponRange()
  System.HideWeaponRange()
end

function Unit.Blink(unitId, interval, duration)
  local unit = System.GetUnit(unitId)
  local proc = System.BlinkUnit(unit, interval, duration)
  Utility.WaitProcedure(proc)
end

function Unit.ChangeMachineSpec(unitId, newMachineId)
  local unit = System.GetUnit(unitId)
  local mapIndex = Unit.GetMapIndex(unit)
  local pos = Unit.GetPosition(unit)
  local dir = Unit.GetDirection(unit)

  Unit.DisappearFakeInstant(unit)
  System.ChangeMachineSpec(unit, newMachineId)
  Unit.AppearJump(unit, mapIndex, pos.X, pos.Y, dir, UnitAppearType.Instant)
end

function Unit.ChangeCharacterSpec(unitId, newCharacterId)
  local unit = System.GetUnit(unitId)
  local mapIndex = Unit.GetMapIndex(unit)
  local pos = Unit.GetPosition(unit)
  local dir = Unit.GetDirection(unit)

  Unit.DisappearFakeInstant(unit)
  System.ChangeCharacterSpec(unit, newCharacterId)
  Unit.AppearJump(unit, mapIndex, pos.X, pos.Y, dir, UnitAppearType.Instant)
end

---
-- Battle Table
---

Battle = {}

function Battle.AllUnits()
  return System.AllBattleUnits()
end

function Battle.MainAttacker()
  return System.MainAttacker()
end

function Battle.MainTarget()
  return System.MainTarget()
end

function Battle.TargetUnits()
  return System.TargetUnits()
end

function Battle.DeadUnits()
  return System.DeadUnits()
end

function Battle.ContainBattleUnit(unitId)
  local unit = System.GetUnit(unitId)
  return System.ContainBattleUnit(unit)
end

function Battle.ContainDeadUnit(unitId)
  local unit = System.GetUnit(unitId)
  return System.ContainDeadUnit(unit)
end

function Battle.MainAttackerWeapon(unitId)
  local unit = System.GetUnit(unitId)
  return System.MainAttackerWeapon(unit)
end

function Battle.VSSingle(vsId)
  return System.VSSingle(vsId)
end

function Battle.VSSingleOnce(flagId, vsId)
  local triggered = false
  if not System.GetBattleFlag(flagId) and System.VSSingle(vsId) then
    triggered = true
    System.SetBattleFlag(flagId, true)
  end
  return triggered
end

function Battle.VSDouble(vsId1, vsId2)
  return System.VSDouble(vsId1, vsId2)
end

function Battle.VSDoubleOnce(flagId, vsId1, vsId2)
  local triggered = false
  if not System.GetBattleFlag(flagId) and System.VSDouble(vsId1, vsId2) then
    triggered = true
    System.SetBattleFlag(flagId, true)
  end
  return triggered
end

function Battle.VSKill(vsId, deadUnitId)
  local triggered = Battle.VSSingle(vsId)
  local killed = false
  if triggered then
    killed = Battle.ContainDeadUnit(deadUnitId)
  end
  return killed
end

function Battle.VSDestroy(unitId)
  return System.VSDestroy(unitId)
end

function Battle.IsDestroyGameOverUnit()
  return System.IsDestroyGameOverUnit()
end

function Battle.IsDestroyGameOverUnitWithoutBattleControl()
  return System.IsDestroyGameOverUnitWithoutBattleControl()
end

function Battle.GetDamage(unitId)
  local unit = System.GetUnit(unitId)
  return System.GetDamage(unit)
end

function Battle.IsHitTarget(unitId)
  local unit = System.GetUnit(unitId)
  return System.IsHitTarget(unit)
end

function Battle.CancelBattle()
  System.CancelBattle()
end

function Battle.PlayBattleAnimation(param1, param2, param3, ...)
  local param4 = false
  if select("#", ...) >= 1 then
    param4 = select(1, ...)
  end

  local proc = System.PlayBattleAnimation(param1, param2, param3, param4)
  Utility.WaitProcedure(proc)
end

function Battle.IsPlayBattleAnimation()
  return System.IsPlayBattleAnimation()
end

---
-- Enums / Constants
---

UnitSearchType = {
  All = 0,
  StandBy = 1,
  Appeared = 2,
  Died = 3,
  InShip = 4
}

UnitAppearType = {
  Instant = 0,
  Normal = 1,
  MoveCamera = 2,
  Explosion = 3,
  MasterExplosion = 4
}

UnitArmyType = {
  Player = 0,
  Guest = 1,
  NPC = 2,
  Enemy1 = 3,
  Enemy2 = 4,
  Secret = 5
}

UnitDirectionType = {
  North = 0,
  East = 1,
  South = 2,
  West = 3
}

TensionType = {
  Confuse = 0,
  Timid = 1,
  Normal = 2,
  Aggressive = 3,
  SuperAggressive = 4,
  SuperBlow = 5
}

AttackTargetType = {
  None = 0,
  PlayerAndGuest = 1,
  Player = 2,
  Guest = 3,
  Enemy1 = 4,
  Enemy2 = 5,
  ControlId = 6,
  ManyHP = 7,
  LessHP = 8,
  NearestEnemy = 9,
  MasterUnit = 10
}

NoMoveType = {
  None = 0,
  DetectEnemy = 1,
  Turn = 2,
  TurnOrDetectEnemy = 3,
  DefeatControlId = 4,
  BattleControlId = 5
}

FollowType = {
  None = 0,
  ControlId = 1,
  PlayerAndGuest = 2,
  Player = 3
}

AptitudeLandType = {
  Space = 0,
  Sky = 1,
  Ground = 2,
  Surface = 3,
  Water = 4
}

AptitudeLevelType = {
  E = 0,
  D = 1,
  C = 2,
  B = 3,
  A = 4,
  S = 5,
  Database = 6
}

KomaAnimationType = {
  StandBy = 0,
  Move = 1,
  Event1 = 10,
  Event2 = 11,
  Event3 = 12,
  Event4 = 13,
  Event5 = 14,
  Event6 = 15,
  Event7 = 16,
  Event8 = 17
}

OutEventType = {
  Disappear = 0,
  Explosion = 1,
  Master = 2
}

DisplaySizeType = {
  L = 0,
  LL = 1,
  XL = 2,
  XXL = 3
}

CharaterCrewType = {
  Pilot = 0,
  Captain = 0,
  ViceCaptain = 1,
  Operator = 2,
  Steerer = 3,
  Mechanic = 4,
  Guest = 5
}