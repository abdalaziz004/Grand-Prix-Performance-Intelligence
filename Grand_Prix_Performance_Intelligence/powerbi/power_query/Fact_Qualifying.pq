let
    Source = Staging_qualifying_results,
    Types = Table.TransformColumns(Source, {
        {"driverId", each if _ = null then null else Text.From(_), type nullable text},
        {"constructorId", each if _ = null then null else Text.From(_), type nullable text},
        {"raceId", each try Int64.From(_) otherwise null, Int64.Type},
        {"year", each try Int64.From(_) otherwise null, Int64.Type},
        {"round", each try Int64.From(_) otherwise null, Int64.Type},
        {"positionNumber", each try Number.FromText(Text.From(_), "en-US") otherwise null, type nullable number},
        {"q1Millis", each try Number.From(_) otherwise null, type nullable number},
        {"q2Millis", each try Number.From(_) otherwise null, type nullable number},
        {"q3Millis", each try Number.From(_) otherwise null, type nullable number},
        {"timeMillis", each try Number.From(_) otherwise null, type nullable number},
        {"gapMillis", each try Number.From(_) otherwise null, type nullable number},
        {"intervalMillis", each try Number.From(_) otherwise null, type nullable number},
        {"laps", each try Int64.From(_) otherwise null, Int64.Type}
    }),
    AddRowId = Table.AddIndexColumn(Types, "QualifyingRowId", 1, 1, Int64.Type)
in
    AddRowId
