(value as nullable any) as nullable logical =>
let
    TextValue = if value = null then null else Text.Lower(Text.Trim(Text.From(value))),
    Result =
        if TextValue = null or TextValue = "" then null
        else if List.Contains({"true", "1", "yes", "y"}, TextValue) then true
        else if List.Contains({"false", "0", "no", "n"}, TextValue) then false
        else null
in
    Result
