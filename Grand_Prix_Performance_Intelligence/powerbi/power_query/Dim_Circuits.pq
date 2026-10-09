let
    Source = Staging_circuits,
    Keep = Table.SelectColumns(Source, {"id", "name", "fullName", "previousNames", "type", "direction", "placeName", "countryId", "latitude", "longitude", "length", "turns", "totalRacesHeld"}),
    Types = Table.TransformColumnTypes(Keep, {{"id", type text}, {"latitude", type number}, {"longitude", type number}, {"length", type number}, {"turns", Int64.Type}, {"totalRacesHeld", Int64.Type}}),
    MergeCountry = Table.NestedJoin(Types, {"countryId"}, Staging_countries, {"id"}, "CountryLookup", JoinKind.LeftOuter),
    ExpandCountry = Table.ExpandTableColumn(MergeCountry, "CountryLookup", {"name", "continentId"}, {"HostCountry", "Continent"}),
    Rename = Table.RenameColumns(ExpandCountry, {{"id", "CircuitId"}, {"name", "CircuitName"}, {"type", "CircuitType"}, {"latitude", "Latitude"}, {"longitude", "Longitude"}})
in
    Rename
