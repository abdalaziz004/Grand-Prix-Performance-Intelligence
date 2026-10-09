let
    Source = Staging_constructors,
    Keep = Table.SelectColumns(Source, {"id", "totalChampionshipWins", "totalRaceEntries", "totalRaceStarts", "totalRaceWins", "totalRaceLaps", "totalPodiums", "totalPodiumRaces", "totalPoints", "totalChampionshipPoints", "totalPolePositions", "totalFastestLaps", "totalSprintRaceStarts", "totalSprintRaceWins"})
in
    Keep
