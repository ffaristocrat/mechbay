-- Global stage variables
gameover = 0
gameclear = 0
questclear = 0

-- Sound effect constants
se_call = "sf90500.hca"
se_kiki = "sb10050.hca"
se_online = "sa00090.hca"
se_shake = "sf90220.hca"
se_kamae = "sf90290.hca"
se_gain = "sf90790.hca"
se_noise = "sf90510.hca"

-- Time and speed constants
waitTime0 = "0.4"
waitTime1 = "1"
waitTime2 = "1.5"
waitTime3 = "2.0"
fadeSpeed0 = "1"
fadeSpeed1 = "2"
fadeSpeed2 = "3"
fadeSpeed3 = "4"
cursorPSlow = 2.5
cursorSlow = 5
cursorRSlow = 7
cursorNormal = 10
cursorRFast = 15
cursorFast = 20

-- ELS unit lists
ELSUnitList = {
  "G1220U03200",
  "G1220U03300"
}
ELSGNXListS = {
  "G1220U03800",
  "G1220U03900"
}
ELSGNXListM = {
  "G1220U04000"
}

function IsELSUnit(unitId)
  local isEis = false
  for _, machineId in ipairs(ELSUnitList) do
    if machineId == Unit.GetMachineId(unitId) then
      isEis = true
      break
    end
  end
  return isEis
end

function GetELSGNXId(unitId)
  local elsgGnxId = ""
  local displaySize = Unit.GetDisplaySize(unitId)
  
  if displaySize == DisplaySizeType.L then
    elsgGnxId = ELSGNXListS[math.random(#ELSGNXListS)]
  elseif displaySize > DisplaySizeType.L then
    elsgGnxId = ELSGNXListM[math.random(#ELSGNXListM)]
  end
  return elsgGnxId
end

function BombEffectAroundUnit(unitId, range)
  local unit = Unit.GetUnit(unitId)
  local pos = Unit.GetPosition(unit)
  local ssaHandle = 0
  
  for i = 1, 4 do
    ssaHandle = SSA.CreateSSA(901)
    local randX = (math.random() - 0.5) * range + pos.X
    local randY = (math.random() - 0.5) * range + pos.Y
    SSA.CellPosition(ssaHandle, randX, randY)
    Utility.Wait(0.1)
  end
  
  Utility.WaitProcedure(ssaHandle)
end

function BombEffectAroundPoint(cellX, cellY, range)
  -- NOTE: This function was corrupt and ended with a call to nil.
  -- The broken call has been removed.
  local ssaHandle = 0
  for i = 1, 4 do
    local randX = (math.random() - 0.5) * range
    local randY = (math.random() - 0.5) * range
    
    local posX = (randX + cellX + 0.5) * Grid.Size()
    local posY = (randY + cellY + 0.5) * Grid.Size()
    
    ssaHandle = SSA.CreateSSA(901)
    SSA.Position(ssaHandle, posX, posY)
    Utility.Wait(0.1)
  end
end

function BiriEffectAroundUnit(unitId, range)
  -- NOTE: This function was corrupt and ended with a call to nil.
  -- The broken call has been removed.
  local unit = Unit.GetUnit(unitId)
  local pos = Unit.GetPosition(unit)
  local ssaHandle = 0
  
  for i = 1, 4 do
    local randX = (math.random() - 0.5) * range
    local randY = (math.random() - 0.5) * range
    
    local posX = (pos.X + randX + 0.5) * Grid.Size()
    local posY = (pos.Y + randY + 0.5) * Grid.Size()
    
    ssaHandle = SSA.CreateSSAonUnit(900, unit)
    SSA.Position(ssaHandle, posX, posY)
    Utility.Wait(0.1)
  end
end

function BombEffectAroundPointCount(cellX, cellY, range, count)
  -- NOTE: This function was corrupt and ended with a call to nil.
  -- The broken call has been removed.
  local ssaHandle = 0
  for i = 1, count do
    local randX = (math.random() - 0.5) * range
    local randY = (math.random() - 0.5) * range
    
    local posX = (randX + cellX + 0.5) * Grid.Size()
    local posY = (randY + cellY + 0.5) * Grid.Size()
    
    ssaHandle = SSA.CreateSSA(901)
    SSA.Position(ssaHandle, posX, posY)
    Utility.Wait(0.1)
  end
end

function SetUnitHp(unitId, hp)
  local param = Unit.GetParameter(unitId)
  param.Hp = hp
  Unit.SetParameter(unitId, param)
end

function BombEffectAroundUnit_Nowait(unitId, range)
  local unit = Unit.GetUnit(unitId)
  local pos = Unit.GetPosition(unit)
  local ssaHandle = 0
  
  for i = 1, 4 do
    ssaHandle = SSA.CreateSSAonUnit(901, unit)
    local randX = (math.random() - 0.5) * range + pos.X
    local randY = (math.random() - 0.5) * range + pos.Y
    SSA.CellPosition(ssaHandle, randX, randY)
    Utility.Wait(0.1)
  end
end

function BiriEffectAroundUnit_Nowait(unitId, range)
  local unit = Unit.GetUnit(unitId)
  local pos = Unit.GetPosition(unit)
  local ssaHandle = 0
  
  for i = 1, 4 do
    local randX = (math.random() - 0.5) * range
    local randY = (math.random() - 0.5) * range
    
    local posX = (pos.X + randX + 0.5) * Grid.Size()
    local posY = (pos.Y + randY + 0.5) * Grid.Size()
    
    ssaHandle = SSA.CreateSSAonUnit(900, unit)
    SSA.Position(ssaHandle, posX, posY)
    Utility.Wait(0.1)
  end
end

function BombEffectAroundPointCount_Nowait(cellX, cellY, range, count)
  local ssaHandle = 0
  for i = 1, count do
    local randX = (math.random() - 0.5) * range
    local randY = (math.random() - 0.5) * range
    
    local posX = (randX + cellX + 0.5) * Grid.Size()
    local posY = (randY + cellY + 0.5) * Grid.Size()
    
    ssaHandle = SSA.CreateSSA(901)
    SSA.Position(ssaHandle, posX, posY)
    Utility.Wait(0.1)
  end
end

function BiriKill_Nowait(unitId)
  local unit = Unit.GetUnit(unitId)
  local ssaHandle = 0
  ssaHandle = SSA.CreateSSAonUnit(900, unit)
  Utility.Wait(0.4)
  ssaHandle = SSA.CreateSSAonUnit(901, unit)
  Utility.Wait(0.2)
  Unit.DisappearInstant(unit)
end

function Kill_Nowait(unitId)
  local unit = Unit.GetUnit(unitId)
  if Unit.IsAlive(unit) == true then
    Cursor.MoveToUnit(unit, 0, true, true)
    local ssaHandle = SSA.CreateSSAonUnit(901, unit)
    Utility.Wait(0.2)
    Unit.DisappearInstant(unit)
  end
end

function WS_Charge(unitId, percent)
  local unit = Unit.GetUnit(unitId)
  if Unit.IsInWarShip(unit) == true then
    local param = Unit.GetParameter(unit)
    param.Hp = param.Hp + param.MaxHp / 100 * percent
    param.En = param.En + param.MaxEn / 100 * percent
    Unit.SetParameter(unit, param)
  end
end

function ReinforceUnit(unitList, cellX, cellY)
  local unitId = ""
  local attempts = 0
  local randIndex = 1
  
  repeat
    randIndex = math.random(#unitList)
    unitId = unitList[randIndex]
    attempts = attempts + 1
  until not Unit.IsAppeared(unitId) or attempts >= 1000
  
  if attempts < 1000 then
    Unit.AppearJump(unitId, Map.GetIndex(), cellX, cellY, UnitDirectionType.South, UnitAppearType.Normal)
  else
    -- No available unit found
  end
end

function AppearGroupFast(groupName)
  local unitList = Unit.GetUnitsByGroupName(groupName, UnitSearchType.StandBy)
  Unit.AppearFast(0.2, table.unpack(unitList))
end

function AppearGroupInstant(groupName)
  local unitList = Unit.GetUnitsByGroupName(groupName, UnitSearchType.StandBy)
  Unit.AppearInstant(table.unpack(unitList))
end