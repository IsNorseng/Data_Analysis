let
    Source = SalesModel[Monthly],
    Renamed = Table.RenameColumns(Source, {
        {"YearMonth", "Месяц"},
        {"Revenue", "Выручка, ₽"},
        {"Gross Margin %", "Вал. маржа, %"},
        {"Losses %", "Потери, % ₽"},
        {"Avg Selling Price", "Ср. цена, ₽/шт."},
        {"Avg Weekly Turnover", "Ср. недельный Turnover"}
    })
in
    Renamed
