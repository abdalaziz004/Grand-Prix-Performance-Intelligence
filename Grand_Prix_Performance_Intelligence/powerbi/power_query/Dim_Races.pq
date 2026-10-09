let
    Source = Staging_races,
    Keep = Table.SelectColumns(Source, {"id", "year", "round", "date", "grandPrixId", "officialName", "qualifyingFormat", "circuitId", "circuitType", "direction", "courseLength", "turns", "laps", "distance", "scheduledLaps", "scheduledDistance", "sprintRaceDate", "sprintRaceLaps", "sprintRaceDistance"}),
    Types = Table.TransformColumnTypes(Keep, {{"id", Int64.Type}, {"year", Int64.Type}, {"round", Int64.Type}, {"date", type date}, {"grandPrixId", type text}, {"circuitId", type text}, {"courseLength", type number}, {"turns", Int64.Type}, {"laps", Int64.Type}, {"distance", type number}, {"scheduledLaps", Int64.Type}, {"scheduledDistance", type number}, {"sprintRaceDate", type date}, {"sprintRaceLaps", Int64.Type}, {"sprintRaceDistance", type number}}),
    MergeGP = Table.NestedJoin(Types, {"grandPrixId"}, Dim_GrandPrix, {"GrandPrixId"}, "GrandPrix", JoinKind.LeftOuter),
    ExpandGP = Table.ExpandTableColumn(MergeGP, "GrandPrix", {"GrandPrixName"}, {"GrandPrixName"}),
    Rename = Table.RenameColumns(ExpandGP, {{"id", "RaceId"}, {"year", "Year"}, {"round", "Round"}, {"date", "RaceDate"}, {"grandPrixId", "GrandPrixId"}, {"circuitId", "CircuitId"}, {"officialName", "OfficialRaceName"}, {"qualifyingFormat", "QualifyingFormat"}})
in
    Rename
