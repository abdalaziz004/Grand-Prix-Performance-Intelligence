let
    Source = Staging_season_driver_standings,
    Types = Table.TransformColumns(Source, {
        {"driverId", each if _ = null then null else Text.From(_), type nullable text},
        {"year", each try Int64.From(_) otherwise null, Int64.Type},
        {"positionNumber", each try Number.FromText(Text.From(_), "en-US") otherwise null, type nullable number},
        {"points", each try Number.FromText(Text.From(_), "en-US") otherwise null, type nullable number},
        {"championshipWon", each fxNullableBoolean(_), type nullable logical}
    }),
    AddRowId = Table.AddIndexColumn(Types, "SeasonDriverRowId", 1, 1, Int64.Type)
in
    AddRowId
