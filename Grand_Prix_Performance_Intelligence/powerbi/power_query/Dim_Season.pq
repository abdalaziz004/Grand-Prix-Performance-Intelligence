let
    Years1 = List.Transform(List.RemoveNulls(Staging_races[year]), each Int64.From(_)),
    Years2 = List.Transform(List.RemoveNulls(Staging_season_driver_standings[year]), each Int64.From(_)),
    Years3 = List.Transform(List.RemoveNulls(Staging_season_constructor_standings[year]), each Int64.From(_)),
    Years = List.Sort(List.Distinct(List.Combine({Years1, Years2, Years3}))),
    AsTable = Table.FromList(Years, Splitter.SplitByNothing(), {"Year"}, null, ExtraValues.Error),
    Typed = Table.TransformColumnTypes(AsTable, {{"Year", Int64.Type}})
in
    Typed
