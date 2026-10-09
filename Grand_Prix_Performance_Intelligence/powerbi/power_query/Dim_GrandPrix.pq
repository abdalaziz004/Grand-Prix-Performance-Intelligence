let
    Source = Staging_grands_prix,
    Keep = Table.SelectColumns(Source, {"id", "name", "fullName", "shortName", "abbreviation", "countryId", "totalRacesHeld"}),
    Types = Table.TransformColumnTypes(Keep, {{"id", type text}, {"totalRacesHeld", Int64.Type}}),
    MergeCountry = Table.NestedJoin(Types, {"countryId"}, Staging_countries, {"id"}, "CountryLookup", JoinKind.LeftOuter),
    ExpandCountry = Table.ExpandTableColumn(MergeCountry, "CountryLookup", {"name"}, {"GrandPrixCountry"}),
    Rename = Table.RenameColumns(ExpandCountry, {{"id", "GrandPrixId"}, {"name", "GrandPrixName"}})
in
    Rename
