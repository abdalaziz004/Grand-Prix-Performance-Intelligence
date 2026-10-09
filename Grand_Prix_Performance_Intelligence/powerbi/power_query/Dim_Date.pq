let
    RaceDates = List.Transform(List.RemoveNulls(Staging_races[date]), each Date.From(_)),
    StartDate = List.Min(RaceDates),
    EndDate = List.Max(RaceDates),
    CountDays = Duration.Days(EndDate - StartDate) + 1,
    Dates = List.Dates(StartDate, CountDays, #duration(1, 0, 0, 0)),
    AsTable = Table.FromList(Dates, Splitter.SplitByNothing(), {"Date"}, null, ExtraValues.Error),
    DateType = Table.TransformColumnTypes(AsTable, {{"Date", type date}}),
    AddYear = Table.AddColumn(DateType, "Year", each Date.Year([Date]), Int64.Type),
    AddQuarter = Table.AddColumn(AddYear, "Quarter", each "Q" & Text.From(Date.QuarterOfYear([Date])), type text),
    AddMonthNumber = Table.AddColumn(AddQuarter, "MonthNumber", each Date.Month([Date]), Int64.Type),
    AddMonthName = Table.AddColumn(AddMonthNumber, "MonthName", each Date.ToText([Date], "MMMM", "en-US"), type text),
    AddDay = Table.AddColumn(AddMonthName, "DayOfMonth", each Date.Day([Date]), Int64.Type),
    AddWeekday = Table.AddColumn(AddDay, "DayOfWeek", each Date.ToText([Date], "dddd", "en-US"), type text),
    RaceDateList = List.Distinct(List.Transform(List.RemoveNulls(Staging_races[date]), each Date.From(_))),
    AddRaceFlag = Table.AddColumn(AddWeekday, "IsRaceDay", each List.Contains(RaceDateList, [Date]), type logical)
in
    AddRaceFlag
