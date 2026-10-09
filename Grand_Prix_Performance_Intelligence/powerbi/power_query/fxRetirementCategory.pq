(reason as nullable any) as text =>
let
    V = if reason = null then "" else Text.Lower(Text.Trim(Text.From(reason))),
    HasAny = (terms as list) as logical => List.AnyTrue(List.Transform(terms, each Text.Contains(V, _))),
    Category =
        if V = "" then "Not recorded / not applicable"
        else if HasAny({"accident", "collision", "crash", "spun off", "spin", "contact"}) then "Accident / contact"
        else if HasAny({"engine", "gearbox", "transmission", "clutch", "suspension", "brake", "oil leak", "water leak", "mechanical", "bearing", "axle", "differential", "steering"}) then "Mechanical / powertrain"
        else if HasAny({"electrical", "fuel", "fire", "overheating", "radiator", "cooling", "battery", "ignition"}) then "Electrical / fuel / cooling"
        else if HasAny({"injury", "illness", "driver", "disqualified", "rule", "penalty", "withdrawn"}) then "Driver / rules / withdrawal"
        else "Other / unclassified"
in
    Category
