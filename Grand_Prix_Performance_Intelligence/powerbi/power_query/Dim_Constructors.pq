let
    Source = Staging_constructors,
    KeepColumns = Table.SelectColumns(Source, {"id", "name", "fullName", "countryId", "bestChampionshipPosition", "bestStartingGridPosition", "bestRaceResult", "bestSprintRaceResult"}),
    Types = Table.TransformColumnTypes(KeepColumns, {{"id", type text}, {"bestChampionshipPosition", Int64.Type}, {"bestStartingGridPosition", Int64.Type}, {"bestRaceResult", Int64.Type}, {"bestSprintRaceResult", Int64.Type}}),
    MergeCountry = Table.NestedJoin(Types, {"countryId"}, Staging_countries, {"id"}, "CountryLookup", JoinKind.LeftOuter),
    ExpandCountry = Table.ExpandTableColumn(MergeCountry, "CountryLookup", {"name", "continentId"}, {"CountryName", "CountryContinent"}),
    Rename = Table.RenameColumns(ExpandCountry, {{"id", "ConstructorId"}, {"name", "ConstructorName"}})
in
    Rename
