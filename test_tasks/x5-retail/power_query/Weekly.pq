let
    Source = SalesModel[Weekly],
    Renamed = Table.RenameColumns(Source, {
        {"YearWeek", "ISO-неделя"},
        {"WeekStartDate", "Понедельник"},
        {"Revenue", "Выручка, ₽"},
        {"Gross Margin %", "Вал. маржа, %"},
        {"Losses %", "Потери, % ₽"},
        {"Avg Selling Price", "Ср. цена, ₽/шт."}
    })
in
    Renamed
