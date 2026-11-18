let
    Columns = {
        "product_id", "product_name", "category", "purchase_price", "selling_price",
        "quantity_sold", "quantity_purchased", "losses", "date", "store_id"
    },
    ReadNumber = (value as nullable text) as nullable number =>
        let
            TextValue = if value = null then "" else Text.Trim(value),
            Parsed = if TextValue = "" then null else Number.FromText(TextValue, "en-US")
        in
            if Parsed = null then null
            else if Number.IsNaN(Parsed) or Parsed = #infinity or Parsed = -#infinity then
                error Error.Record("Invalid number", "Expected a finite number.", [Input = value])
            else Parsed,
    ReadQuantity = (value as nullable text, column as text) as number =>
        let
            Parsed = ReadNumber(value)
        in
            if Parsed = null or Parsed <> Number.RoundDown(Parsed) then
                error Error.Record("Invalid quantity", "Expected an integer quantity.", [Column = column, Input = value])
            else if Parsed < 0 then 0
            else Int64.From(Parsed),
    ReadDate = (value as nullable text) as date =>
        let
            TextValue = if value = null then "" else Text.Trim(value),
            Parsed = try Date.FromText(TextValue, "en-US") otherwise null
        in
            if Parsed <> null and Date.ToText(Parsed, "yyyy-MM-dd", "en-US") = TextValue then Parsed
            else error Error.Record("Invalid date", "Expected a date in yyyy-MM-dd format.", [Input = value]),
    CalendarMonth = (day as date) as text => Date.ToText(day, "yyyy-MM", "en-US"),
    ISOWeek = (monday as date) as text =>
        let
            ISOYear = Date.Year(Date.AddDays(monday, 3)),
            FirstMonday = Date.StartOfWeek(#date(ISOYear, 1, 4), Day.Monday),
            WeekNo = 1 + Number.IntegerDivide(Duration.Days(monday - FirstMonday), 7)
        in
            Number.ToText(ISOYear, "0000", "en-US") & "-" & Number.ToText(WeekNo, "00", "en-US"),
    Ratio = (numerator as nullable number, denominator as nullable number) as nullable number =>
        if denominator = null or denominator = 0 then null
        else Value.Divide(numerator, denominator, Precision.Decimal),

    Imported = Csv.Document(File.Contents(pCsvPath), List.Count(Columns), ",", ExtraValues.Error, 65001),
    Headers = Table.PromoteHeaders(Imported),
    Raw = Table.SelectColumns(Headers, Columns),
    Distinct = Table.Distinct(Raw),
    Prices = Table.TransformColumns(Distinct, {
        {"purchase_price", each Currency.From(ReadNumber(_)), Currency.Type},
        {"selling_price", each Currency.From(ReadNumber(_)), Currency.Type}
    }),
    AvailablePrices = Table.SelectRows(Prices, each [purchase_price] <> null and [selling_price] <> null),
    Typed = Table.TransformColumns(AvailablePrices, {
        {"product_id", each _, type text},
        {"product_name", each _, type text},
        {"category", each _, type text},
        {"store_id", each _, type text},
        {"quantity_sold", each ReadQuantity(_, "quantity_sold"), Int64.Type},
        {"quantity_purchased", each ReadQuantity(_, "quantity_purchased"), Int64.Type},
        {"losses", each ReadQuantity(_, "losses"), Int64.Type},
        {"date", ReadDate, type date}
    }),
    WithMonth = Table.AddColumn(Typed, "YearMonth", each CalendarMonth([date]), type text),
    WithMonday = Table.AddColumn(WithMonth, "WeekStartDate", each Date.StartOfWeek([date], Day.Monday), type date),
    WithWeek = Table.AddColumn(WithMonday, "YearWeek", each ISOWeek([WeekStartDate]), type text),
    WithRevenue = Table.AddColumn(WithWeek, "Revenue", each Value.Multiply([quantity_sold], [selling_price], Precision.Decimal), Currency.Type),
    WithProfit = Table.AddColumn(WithRevenue, "GrossProfit", each Value.Multiply(
        [quantity_sold], Value.Subtract([selling_price], [purchase_price], Precision.Decimal), Precision.Decimal
    ), Currency.Type),
    WithLossCost = Table.AddColumn(WithProfit, "LossCost", each Value.Multiply([losses], [purchase_price], Precision.Decimal), Currency.Type),
    Sales = Table.AddColumn(WithLossCost, "PurchaseCost", each Value.Multiply([quantity_purchased], [purchase_price], Precision.Decimal), Currency.Type),

    Summarize = (keys as list) as table =>
        let
            Totals = Table.Group(Sales, keys, {
                {"Revenue", each List.Sum([Revenue], Precision.Decimal), Currency.Type},
                {"GrossProfit", each List.Sum([GrossProfit], Precision.Decimal), Currency.Type},
                {"LossCost", each List.Sum([LossCost], Precision.Decimal), Currency.Type},
                {"PurchaseCost", each List.Sum([PurchaseCost], Precision.Decimal), Currency.Type},
                {"Sold", each List.Sum([quantity_sold]), Int64.Type},
                {"Purchased", each List.Sum([quantity_purchased]), Int64.Type},
                {"Losses", each List.Sum([losses]), Int64.Type}
            }),
            WithMargin = Table.AddColumn(Totals, "Gross Margin %", each Ratio([GrossProfit], [Revenue]), type nullable number),
            WithRate = Table.AddColumn(WithMargin, "Losses %", each Ratio([LossCost], [PurchaseCost]), type nullable number),
            WithAvgPrice = Table.AddColumn(WithRate, "Avg Selling Price", each Ratio([Revenue], [Sold]), type nullable number),
            WithTurnover = Table.AddColumn(WithAvgPrice, "Turnover", each Ratio(7 * [Sold], [Purchased] + [Losses]), type nullable number)
        in
            Table.SelectColumns(WithTurnover, keys & {"Revenue", "Gross Margin %", "Losses %", "Avg Selling Price", "Turnover"}),

    Weekly = Table.Sort(Summarize({"YearWeek", "WeekStartDate"}), {{"WeekStartDate", Order.Ascending}}),
    // Each weekly rate belongs to the calendar month of its Monday.
    WeeklyWithMonth = Table.AddColumn(Weekly, "YearMonth", each CalendarMonth([WeekStartDate]), type text),
    WeeklyAverages = Table.Group(WeeklyWithMonth, {"YearMonth"}, {
        {"Avg Weekly Turnover", each List.Average(List.RemoveNulls([Turnover]), Precision.Decimal), type nullable number}
    }),
    MonthlyTotals = Summarize({"YearMonth"}),
    Joined = Table.NestedJoin(MonthlyTotals, {"YearMonth"}, WeeklyAverages, {"YearMonth"}, "WeeklyAverages", JoinKind.LeftOuter),
    Monthly = Table.Sort(Table.ExpandTableColumn(Joined, "WeeklyAverages", {"Avg Weekly Turnover"}), {{"YearMonth", Order.Ascending}})
in
    [Sales = Sales, Weekly = Weekly, Monthly = Monthly]
