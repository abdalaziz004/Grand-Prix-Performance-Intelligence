let
    Source = Staging_race_results,
    NumericTypes = Table.TransformColumns(Source, {
        {"driverId", each if _ = null then null else Text.From(_), type nullable text},
        {"constructorId", each if _ = null then null else Text.From(_), type nullable text},
        {"raceId", each try Int64.From(_) otherwise null, Int64.Type},
        {"year", each try Int64.From(_) otherwise null, Int64.Type},
        {"round", each try Int64.From(_) otherwise null, Int64.Type},
        {"positionNumber", each try Number.FromText(Text.From(_), "en-US") otherwise null, type nullable number},
        {"gridPositionNumber", each try Number.FromText(Text.From(_), "en-US") otherwise null, type nullable number},
        {"qualificationPositionNumber", each try Number.FromText(Text.From(_), "en-US") otherwise null, type nullable number},
        {"points", each try Number.FromText(Text.From(_), "en-US") otherwise null, type nullable number},
        {"positionsGained", each try Number.FromText(Text.From(_), "en-US") otherwise null, type nullable number},
        {"laps", each try Int64.From(_) otherwise null, Int64.Type},
        {"pitStops", each try Int64.From(_) otherwise null, Int64.Type},
        {"timeMillis", each try Number.From(_) otherwise null, type nullable number},
        {"gapMillis", each try Number.From(_) otherwise null, type nullable number},
        {"intervalMillis", each try Number.From(_) otherwise null, type nullable number}
    }),
    TypedFlags = Table.TransformColumns(NumericTypes, {
        {"sharedCar", each fxNullableBoolean(_), type nullable logical},
        {"polePosition", each fxNullableBoolean(_), type nullable logical},
        {"driverOfTheDay", each fxNullableBoolean(_), type nullable logical},
        {"grandSlam", each fxNullableBoolean(_), type nullable logical},
        {"fastestLap", each fxNullableBoolean(_), type nullable logical}
    }),
    FieldSizes = Table.Group(TypedFlags, {"raceId"}, {{"ClassifiedFieldSize", (g) => List.Count(List.Distinct(Table.SelectRows(g, each [positionNumber] <> null)[driverId])), Int64.Type}}),
    MergeFieldSize = Table.NestedJoin(TypedFlags, {"raceId"}, FieldSizes, {"raceId"}, "Field", JoinKind.LeftOuter),
    ExpandFieldSize = Table.ExpandTableColumn(MergeFieldSize, "Field", {"ClassifiedFieldSize"}, {"ClassifiedFieldSize"}),
    AddCategory = Table.AddColumn(ExpandFieldSize, "RetirementCategory", each fxRetirementCategory([reasonRetired]), type text),
    AddNonClassified = Table.AddColumn(AddCategory, "IsBlankFinishPosition", each [positionNumber] = null, type logical),
    AddResultRowId = Table.AddIndexColumn(AddNonClassified, "ResultRowId", 1, 1, Int64.Type)
in
    AddResultRowId
