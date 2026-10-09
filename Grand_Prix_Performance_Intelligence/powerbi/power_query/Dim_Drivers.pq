let
    Source = Staging_drivers,
    KeepColumns = Table.SelectColumns(Source, {"id", "name", "firstName", "lastName", "fullName", "abbreviation", "permanentNumber", "gender", "dateOfBirth", "dateOfDeath", "placeOfBirth", "countryOfBirthCountryId", "nationalityCountryId", "secondNationalityCountryId", "bestChampionshipPosition", "bestStartingGridPosition", "bestRaceResult", "bestSprintRaceResult"}),
    Types = Table.TransformColumnTypes(KeepColumns, {{"id", type text}, {"dateOfBirth", type date}, {"dateOfDeath", type date}, {"permanentNumber", Int64.Type}, {"bestChampionshipPosition", Int64.Type}, {"bestStartingGridPosition", Int64.Type}, {"bestRaceResult", Int64.Type}, {"bestSprintRaceResult", Int64.Type}}),
    MergeNationality = Table.NestedJoin(Types, {"nationalityCountryId"}, Staging_countries, {"id"}, "NationalityLookup", JoinKind.LeftOuter),
    ExpandNationality = Table.ExpandTableColumn(MergeNationality, "NationalityLookup", {"name", "continentId"}, {"NationalityCountry", "NationalityContinent"}),
    RenameId = Table.RenameColumns(ExpandNationality, {{"id", "DriverId"}, {"name", "DriverName"}})
in
    RenameId
