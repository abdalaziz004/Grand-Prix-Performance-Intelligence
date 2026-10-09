let
    Source = Staging_drivers,
    Keep = Table.SelectColumns(Source, {"id", "totalChampionshipWins", "totalRaceEntries", "totalRaceStarts", "totalRaceWins", "totalRaceLaps", "totalPodiums", "totalPoints", "totalChampionshipPoints", "totalPolePositions", "totalFastestLaps", "totalSprintRaceStarts", "totalSprintRaceWins", "totalDriverOfTheDay", "totalGrandSlams"})
in
    Keep
