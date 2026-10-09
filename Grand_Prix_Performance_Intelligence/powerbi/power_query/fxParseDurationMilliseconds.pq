(value as nullable any) as nullable number =>
let
    Raw = if value = null then null else Text.Trim(Text.From(value)),
    LowerRaw = if Raw = null then "" else Text.Lower(Raw),
    IsNotDuration = Raw = null or Raw = "" or Text.Contains(LowerRaw, "lap") or Text.StartsWith(Raw, "+"),
    Parts = if IsNotDuration then {} else Text.Split(Raw, ":"),
    ParseNumber = (s as text) as number => Number.FromText(Text.Trim(s), "en-US"),
    Milliseconds =
        if IsNotDuration then null
        else
            let
                LastPart = List.Last(Parts),
                SecParts = Text.Split(LastPart, "."),
                Seconds = ParseNumber(SecParts{0}),
                Fraction = if List.Count(SecParts) > 1 then ParseNumber("0." & SecParts{1}) else 0,
                LastMillis = Seconds * 1000 + Fraction * 1000,
                Prefix = List.FirstN(Parts, List.Count(Parts) - 1),
                Total =
                    if List.Count(Parts) = 3 then ParseNumber(Prefix{0}) * 3600000 + ParseNumber(Prefix{1}) * 60000 + LastMillis
                    else if List.Count(Parts) = 2 then ParseNumber(Prefix{0}) * 60000 + LastMillis
                    else if List.Count(Parts) = 1 then LastMillis
                    else null
            in Total,
    Result = try Milliseconds otherwise null
in
    Result
