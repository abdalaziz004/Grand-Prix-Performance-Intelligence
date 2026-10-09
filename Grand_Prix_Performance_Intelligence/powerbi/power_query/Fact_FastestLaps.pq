let
    Source = Staging_fastest_laps,
    Types = Table.TransformColumns(Source, {
        {"driverId", each if _ = null then null else Text.From(_), type nullable text},
        {"constructorId", each if _ = null then null else Text.From(_), type nullable text},
        {"raceId", each try Int64.From(_) otherwise null, Int64.Type},
        {"year", each try Int64.From(_) otherwise null, Int64.Type},
        {"round", each try Int64.From(_) otherwise null, Int64.Type},
        {"positionNumber", each try Number.FromText(Text.From(_), "en-US") otherwise null, type nullable number},
        {"lap", each try Int64.From(_) otherwise null, Int64.Type},
        {"timeMillis", each try Number.From(_) otherwise null, type nullable number},
        {"gapMillis", each try Number.From(_) otherwise null, type nullable number},
        {"intervalMillis", each try Number.From(_) otherwise null, type nullable number}
    }),
    AddRowId = Table.AddIndexColumn(Types, "FastestLapRowId", 1, 1, Int64.Type)
in
    AddRowId
