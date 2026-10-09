let
    Source = Csv.Document(
        File.Contents(pDataFolder & "season_constructor_standings.csv"),
        [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    TrimmedHeaders = Table.TransformColumnNames(PromotedHeaders, each Text.Trim(_))
in
    TrimmedHeaders
