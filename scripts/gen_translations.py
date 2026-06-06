#!/usr/bin/env python3
"""Generate ru.csv and et.csv translation files for books app."""
import csv, io, os, sys

TIMESTAMP = "2026-06-06T12:00:00.000Z"

# (source, ru, et)
# Empty string = no translation needed (keep source)
STRINGS = [
    ("${0}", "", ""),
    ("${0} ${1} already exists.", "${0} ${1} уже существует.", "${0} ${1} on juba olemas."),
    ("${0} ${1} does not exist", "${0} ${1} не существует", "${0} ${1} ei eksisteeri"),
    ("${0} ${1} has been modified after loading please reload entry.", "${0} ${1} был изменён после загрузки, пожалуйста перезагрузите запись.", "${0} ${1} on muudetud pärast laadimist, palun laadige kirje uuesti."),
    ("${0} ${1} is linked with existing records.", "${0} ${1} связан с существующими записями.", "${0} ${1} on seotud olemasolevate kirjetega."),
    ("${0} account not set in Inventory Settings.", "Счёт ${0} не задан в настройках инвентаря.", "Konto ${0} ei ole varude seadetes määratud."),
    ("${0} already saved", "${0} уже сохранён", "${0} on juba salvestatud"),
    ("${0} already submitted", "${0} уже проведён", "${0} on juba esitatud"),
    ("${0} cancelled", "${0} отменён", "${0} tühistatud"),
    ("${0} cannot be cancelled", "${0} не может быть отменён", "${0} ei saa tühistada"),
    ("${0} cannot be deleted", "${0} не может быть удалён", "${0} ei saa kustutada"),
    ("${0} deleted", "${0} удалён", "${0} kustutatud"),
    ("${0} entries failed", "${0} записей не удалось", "${0} kirjet ebaõnnestus"),
    ("${0} entries imported", "${0} записей импортировано", "${0} kirjet imporditud"),
    ("${0} entry failed", "${0} запись не удалась", "${0} kirje ebaõnnestus"),
    ("${0} entry imported", "${0} запись импортирована", "${0} kirje imporditud"),
    ("${0} fields selected", "${0} полей выбрано", "${0} välja valitud"),
    ("${0} filters applied", "${0} фильтров применено", "${0} filtrit rakendatud"),
    ("${0} has linked child accounts.", "${0} имеет связанные дочерние счета.", "${0} omab seotud alamkontosid."),
    ("${0} of type ${1} does not exist", "${0} типа ${1} не существует", "${0} tüüpi ${1} ei eksisteeri"),
    ("${0} out of ${1}", "${0} из ${1}", "${0} / ${1}"),
    ("${0} party ${1} is different from ${2}", "${0} контрагент ${1} отличается от ${2}", "${0} osapool ${1} erineb ${2}-st"),
    ("${0} quantity 1 added.", "Добавлено количество 1 для ${0}.", "${0} kogus 1 lisatud."),
    ("${0} row added.", "Строка ${0} добавлена.", "${0} rida lisatud."),
    ("${0} rows", "${0} строк", "${0} rida"),
    ("${0} rows added.", "${0} строк добавлено.", "${0} rida lisatud."),
    ("${0} saved", "${0} сохранён", "${0} salvestatud"),
    ("${0} shortcuts", "${0} горячих клавиш", "${0} otseteed"),
    ("${0} stored at ${1}", "${0} сохранён в ${1}", "${0} salvestatud asukohta ${1}"),
    ("${0} submitted", "${0} проведён", "${0} esitatud"),
    ("${0} value ${1} does not exist.", "Значение ${0} ${1} не существует.", "${0} väärtus ${1} ei eksisteeri."),
    ("0%", "", ""),
    ("03-23-2022", "", ""),
    ("03/23/2022", "", ""),
    ("1 filter applied", "1 фильтр применён", "1 filter rakendatud"),
    ("2022-03-23", "", ""),
    ("23 Mar, 2022", "", ""),
    ("23-03-2022", "", ""),
    ("23.03.2022", "", ""),
    ("23/03/2022", "", ""),
    ("9888900000", "", ""),
    ("A submittable entry is deleted only if it is in the cancelled state.", "Проводимая запись удаляется только в отменённом состоянии.", "Esitatav kirje kustutatakse ainult tühistatud olekus."),
    ("Account", "Счёт", "Konto"),
    ("Account ${0} does not exist.", "Счёт ${0} не существует.", "Konto ${0} ei eksisteeri."),
    ("Account Entries", "Записи счёта", "Konto kirjed"),
    ("Account Name", "Название счёта", "Konto nimi"),
    ("Account Type", "Тип счёта", "Konto tüüp"),
    ("Accounting", "Бухгалтерия", "Raamatupidamine"),
    ("Accounting Entries", "Бухгалтерские записи", "Raamatupidamiskirjed"),
    ("Accounting Ledger Entry", "Запись в бухгалтерской книге", "Pearaamatu kirje"),
    ("Accounting Settings", "Настройки бухгалтерии", "Raamatupidamise seaded"),
    ("Accounts", "Счета", "Kontod"),
    ("Accounts Payable", "Кредиторская задолженность", "Võlad tarnijatele"),
    ("Accounts Receivable", "Дебиторская задолженность", "Ostjate nõuded"),
    ("Accumulated Depreciation", "Накопленная амортизация", "Akumuleeritud kulum"),
    ("Action", "Действие", "Toiming"),
    ("Active", "Активный", "Aktiivne"),
    ("Add Account", "Добавить счёт", "Lisa konto"),
    ("Add Customers", "Добавить клиентов", "Lisa kliente"),
    ("Add Group", "Добавить группу", "Lisa grupp"),
    ("Add Items", "Добавить позиции", "Lisa kaupu"),
    ("Add Row", "Добавить строку", "Lisa rida"),
    ("Add Suppliers", "Добавить поставщиков", "Lisa tarnijaid"),
    ("Add Taxes", "Добавить налоги", "Lisa makse"),
    ("Add a few customers to create your first sales invoice", "Добавьте несколько клиентов для создания первого счёта-фактуры", "Lisa mõned kliendid oma esimese müügiarve loomiseks"),
    ("Add a few suppliers to create your first purchase invoice", "Добавьте несколько поставщиков для создания первого счёта на покупку", "Lisa mõned tarnijad oma esimese ostuarve loomiseks"),
    ("Add a filter", "Добавить фильтр", "Lisa filter"),
    ("Add a remark", "Добавить примечание", "Lisa märkus"),
    ("Add attachment", "Добавить вложение", "Lisa manus"),
    ("Add invoice terms", "Добавить условия счёта", "Lisa arve tingimused"),
    ("Add products or services that you buy from your suppliers", "Добавьте товары или услуги, которые вы покупаете у поставщиков", "Lisa tooted või teenused, mida ostate tarnijatelt"),
    ("Add products or services that you sell to your customers", "Добавьте товары или услуги, которые вы продаёте клиентам", "Lisa tooted või teenused, mida müüte klientidele"),
    ("Add transfer terms", "Добавить условия перевода", "Lisa ülekande tingimused"),
    ("Add'l Discounts", "Доп. скидки", "Lisasoodustused"),
    ("Additional ${0} Serial Numbers required for ${1} quantity of ${2}.", "Требуется дополнительно ${0} серийных номеров для ${1} количества ${2}.", "Nõutav on täiendavalt ${0} seerianumbrit ${1} koguse ${2} jaoks."),
    ("Additional quantity (${0}) required${1} to make outward transfer of item ${2} from ${3} on ${4}", "Требуется дополнительное количество (${0})${1} для исходящего перемещения товара ${2} из ${3} ${4}", "Nõutav on täiendav kogus (${0})${1} toote ${2} väljamineva ülekande tegemiseks kohast ${3} kuupäeval ${4}"),
    ("Address", "Адрес", "Aadress"),
    ("Address Display", "Отображение адреса", "Aadressi kuvamine"),
    ("Address Line 1", "Адрес строка 1", "Aadressirida 1"),
    ("Address Line 2", "Адрес строка 2", "Aadressirida 2"),
    ("Address Name", "Название адреса", "Aadressi nimi"),
    ("Administrative Expenses", "Административные расходы", "Halduskulud"),
    ("All", "Все", "Kõik"),
    ("Amount", "Сумма", "Summa"),
    ("Amount Paid", "Оплаченная сумма", "Makstud summa"),
    ("Amount: ${0} and writeoff: ${1} is less than the total amount allocated to references: ${2}.", "Сумма: ${0} и списание: ${1} меньше общей суммы, выделенной для ссылок: ${2}.", "Summa: ${0} ja mahakandmine: ${1} on väiksem kui viidetele eraldatud kogu summa: ${2}."),
    ("Amount: ${0} is less than the total amount allocated to references: ${1}.", "Сумма: ${0} меньше общей суммы, выделенной для ссылок: ${1}.", "Summa: ${0} on väiksem kui viidetele eraldatud kogu summa: ${1}."),
    ("Amounts", "Суммы", "Summad"),
    ("An entry is cancelled only if it is in the submitted state.", "Запись отменяется только в проведённом состоянии.", "Kirje tühistatakse ainult esitatud olekus."),
    ("An entry is submitted only if it is submittable and is in the saved state.", "Запись проводится только если она проводимая и находится в сохранённом состоянии.", "Kirje esitatakse ainult siis, kui see on esitatav ja salvestatud olekus."),
    ("An error occurred.", "Произошла ошибка.", "Ilmnes viga."),
    ("Applicable anywhere in Arveli", "", ""),
    ("Applicable when Quick Search is open", "", ""),
    ("Applicable when Template Builder is open", "", ""),
    ("Applicable when a entry is open in the Form view or Quick Edit view", "", ""),
    ("Applicable when the List View of an entry type is open", "", ""),
    ("Application of Funds (Assets)", "Размещение средств (Активы)", "Varade paigutus"),
    ("Apply Discount After Tax", "Применить скидку после налогов", "Rakenda allahindlus pärast makse"),
    ("Apply and view changes made to the print template", "Применить и просмотреть изменения шаблона печати", "Rakenda ja vaata prindimallile tehtud muudatusi"),
    ("April", "Апрель", "Aprill"),
    ("Arial", "", ""),
    ("Ascending Order", "По возрастанию", "Kasvav järjestus"),
    ("Asset", "Актив", "Vara"),
    ("Attach Image", "Прикрепить изображение", "Lisa pilt"),
    ("Attachment", "Вложение", "Manus"),
    ("August", "Август", "August"),
    ("Auto Payments", "Автоплатежи", "Automaksed"),
    ("Auto Stock Transfer", "", ""),
    ("Autocomplete", "Автодополнение", "Automaatne täitmine"),
    ("Back", "Назад", "Tagasi"),
    ("Back Reference", "Обратная ссылка", "Tagasiviide"),
    ("Bad import data, could not read file.", "Некорректные данные импорта, не удалось прочитать файл.", "Vigased impordandmed, faili ei saanud lugeda."),
    ("Balance", "Баланс", "Saldo"),
    ("Balance Amount", "Сумма баланса", "Saldo summa"),
    ("Balance Sheet", "Бухгалтерский баланс", "Bilanss"),
    ("Bank", "Банк", "Pank"),
    ("Bank Accounts", "Банковские счета", "Pangakontod"),
    ("Bank Entry", "Банковская запись", "Pangakirje"),
    ("Bank Name", "Название банка", "Panga nimi"),
    ("Bank Overdraft Account", "Счёт овердрафта", "Arvelduskrediidi konto"),
    ("Barcode", "Штрихкод", "Vöötkood"),
    ("Base Grand Total", "Базовая итоговая сумма", "Põhikogu summa"),
    ("Based On", "На основе", "Põhineb"),
    ("Batch", "", ""),
    ("Batch not set for row ${0}.", "", ""),
    ("Batch set for row ${0}.", "", ""),
    ("Bill Created", "Счёт создан", "Arve loodud"),
    ("Billing", "Выставление счетов", "Arveldamine"),
    ("Black", "Чёрный", "Must"),
    ("Blue", "Синий", "Sinine"),
    ("Both", "Оба", "Mõlemad"),
    ("Both From and To Location cannot be undefined", "Местоположения «Откуда» и «Куда» не могут быть неопределены", "Nii algus- kui sihtkoht ei tohi olla määramata"),
    ("Buildings", "Здания", "Ehitised"),
    ("Cancel", "Отмена", "Tühista"),
    ("Cancel ${0}?", "Отменить ${0}?", "Tühistada ${0}?"),
    ("Cancel or Delete an entry.", "Отменить или удалить запись.", "Tühistage või kustutage kirje."),
    ("Cancelled", "Отменён", "Tühistatud"),
    ("Cannot Commit Error", "", ""),
    ("Cannot Delete", "Невозможно удалить", "Ei saa kustutada"),
    ("Cannot Delete Account", "Невозможно удалить счёт", "Ei saa kontot kustutada"),
    ("Cannot Export", "Невозможно экспортировать", "Ei saa eksportida"),
    ("Cannot Import", "Невозможно импортировать", "Ei saa importida"),
    ("Cannot Open File", "Невозможно открыть файл", "Ei saa faili avada"),
    ("Cannot cancel ${0} ${1} because of the following ${2}: ${3}", "Невозможно отменить ${0} ${1} из-за следующего ${2}: ${3}", "Ei saa tühistada ${0} ${1} järgmise ${2} tõttu: ${3}"),
    ("Cannot cancel ${0} because of the following ${1}: ${2}", "Невозможно отменить ${0} из-за следующего ${1}: ${2}", "Ei saa tühistada ${0} järgmise ${1} tõttu: ${2}"),
    ('Cannot delete ${0} "${1}" because of linked entries.', 'Невозможно удалить ${0} "${1}" из-за связанных записей.', 'Ei saa kustutada ${0} "${1}" seotud kirjete tõttu.'),
    ("Cannot open file", "Невозможно открыть файл", "Ei saa faili avada"),
    ("Cannot perform operation.", "Невозможно выполнить операцию.", "Ei saa toimingut teha."),
    ("Cannot read file", "Невозможно прочитать файл", "Ei saa faili lugeda"),
    ("Capital Equipments", "Основное оборудование", "Põhivara seadmed"),
    ("Capital Stock", "Уставный капитал", "Põhikapital"),
    ("Cash", "Наличные", "Sularaha"),
    ("Cash Denominations", "", ""),
    ("Cash Entry", "Кассовая запись", "Kassaoperatsioon"),
    ("Cash In Hand", "Наличные в кассе", "Kassas olev sularaha"),
    ("Cashflow", "Денежный поток", "Rahavoog"),
    ("Central Tax", "Центральный налог", "Keskmaks"),
    ("Change DB", "Сменить БД", "Vaheta andmebaas"),
    ("Change File", "Сменить файл", "Vaheta fail"),
    ("Change Ref Type", "Сменить тип ссылки", "Vaheta viite tüüp"),
    ("Changes made to settings will be visible on reload.", "Изменения настроек будут видны после перезагрузки.", "Seadete muudatused on nähtavad pärast uuesti laadimist."),
    ("Chargeable", "Оплачиваемый", "Tasustatav"),
    ("Chart Of Accounts Reviewed", "План счетов проверен", "Kontoplaan üle vaadatud"),
    ("Chart of Accounts", "План счетов", "Kontoplaan"),
    ("Check", "", ""),
    ("Cheque", "Чек", "Tšekk"),
    ("City / Town", "Город / Населённый пункт", "Linn / Alev"),
    ("Clear", "Очистить", "Tühjenda"),
    ("Clearance Date", "Дата клиринга", "Kliirimise kuupäev"),
    ("Close", "Закрыть", "Sulge"),
    ("Close Arveli and try manually.", "", ""),
    ("Close POS Shift", "Закрыть смену PoS", "Sulge kassavahetus"),
    ("Close Quick Search", "Закрыть быстрый поиск", "Sulge kiirotsing"),
    ("Closing", "Закрытие", "Sulgemine"),
    ("Closing ${0} Amount can not be negative.", "", ""),
    ("Closing (Cr)", "Закрытие (Кр)", "Sulgemine (Kr)"),
    ("Closing (Dr)", "Закрытие (Дб)", "Sulgemine (Db)"),
    ("Closing Amount", "Сумма закрытия", "Sulgemissumma"),
    ("Closing Cash In Denominations", "", ""),
    ("Closing Date", "Дата закрытия", "Sulgemiskuupäev"),
    ("Collapse", "Свернуть", "Ahenda"),
    ("Color", "Цвет", "Värv"),
    ("Commission on Sales", "Комиссия с продаж", "Müügikomisjon"),
    ("Common", "Общее", "Üldine"),
    ("Company", "Компания", "Ettevõte"),
    ("Company Logo", "Логотип компании", "Ettevõtte logo"),
    ("Company Name", "Название компании", "Ettevõtte nimi"),
    ("Company Setup", "Настройка компании", "Ettevõtte seadistamine"),
    ("Completed", "Завершён", "Lõpetatud"),
    ("Condition", "Условие", "Tingimus"),
    ("Consolidate Columns", "Консолидировать столбцы", "Ühenda veerud"),
    ("Contacts", "Контакты", "Kontaktid"),
    ("Contains", "Содержит", "Sisaldab"),
    ("Continue submitting Sales Invoice?", "Продолжить проведение счёта-фактуры?", "Jätkata müügiarve esitamist?"),
    ("Contra Entry", "Контрарная запись", "Kontrarje kirje"),
    ("Conversion Error", "Ошибка конвертации", "Konverteerimise viga"),
    ("Conversion Factor", "Коэффициент конвертации", "Konverteerimisnäitaja"),
    ("Cost Of Goods Sold Acc.", "Счёт себестоимости продаж", "Müüdud kaupade maksumuse konto"),
    ("Cost of Goods Sold", "Себестоимость продаж", "Müüdud kaupade maksumus"),
    ("Could not connect to database file ${0}, please select the file manually", "Не удалось подключиться к файлу базы данных ${0}, выберите файл вручную", "Ei saanud ühenduda andmebaasifailiga ${0}, palun valige fail käsitsi"),
    ("Count", "Количество", "Arv"),
    ("Counter Cash Account", "Счёт кассы", "Kassaraha konto"),
    ("Country", "Страна", "Riik"),
    ("Country Code", "Код страны", "Riigikood"),
    ("Country code used to initialize regional settings.", "Код страны для инициализации региональных настроек.", "Riigikood regionaalsete seadete lähtestamiseks."),
    ("Courier", "", ""),
    ("Cr.", "", ""),
    ("Cr. ${0}", "", ""),
    ("Create", "Создать", "Loo"),
    ("Create Demo", "Создать демо", "Loo demo"),
    ("Create Purchase", "Создать закупку", "Loo ost"),
    ("Create Purchase Invoice", "Создать счёт на закупку", "Loo ostuarve"),
    ("Create Sale", "Создать продажу", "Loo müük"),
    ("Create Sales Invoice", "Создать счёт-фактуру", "Loo müügiarve"),
    ("Create a demo company to try out Arveli", "", ""),
    ("Create a new company and store it on your computer", "", ""),
    ("Create a new company or select an existing one from your computer", "", ""),
    ("Create a new entry of the same type as the List View", "", ""),
    ("Create new ${0} entry?", "", ""),
    ("Create your first purchase invoice from the created supplier", "Создайте первый счёт на закупку от созданного поставщика", "Looge esimene ostuarve loodud tarnijalt"),
    ("Create your first sales invoice for the created customer", "Создайте первый счёт-фактуру для созданного клиента", "Looge esimene müügiarve loodud kliendile"),
    ("Created", "Создано", "Loodud"),
    ("Created By", "Создано пользователем", "Loodud kasutaja poolt"),
    ("Creating Items and Parties", "Создание товаров и контрагентов", "Kaupade ja osapoolte loomine"),
    ("Creating Journal Entries", "Создание журнальных записей", "Raamatupidamiskirjete loomine"),
    ("Creating Purchase Invoices", "Создание счетов на закупку", "Ostuarvete loomine"),
    ("Credit", "Кредит", "Kreedit"),
    ("Credit Card Entry", "Запись по кредитной карте", "Krediitkaardi kirje"),
    ("Credit Note", "Кредит-нота", "Kreeditarve"),
    ("Creditors", "Кредиторы", "Võlausaldajad"),
    ("Currency", "Валюта", "Valuuta"),
    ("Currency Name", "Название валюты", "Valuuta nimi"),
    ("Current", "Текущий", "Praegune"),
    ("Current Assets", "Оборотные активы", "Käibevara"),
    ("Current Liabilities", "Краткосрочные обязательства", "Lühiajalised kohustused"),
    ("Custom Field", "Пользовательское поле", "Kohandatud väli"),
    ("Custom Fields", "Пользовательские поля", "Kohandatud väljad"),
    ("Custom Form", "Пользовательская форма", "Kohandatud vorm"),
    ("Custom Hex", "Произвольный шестнадцатеричный", "Kohandatud hex"),
    ("Customer", "Клиент", "Klient"),
    ("Customer Created", "Клиент создан", "Klient loodud"),
    ("Customer Currency", "Валюта клиента", "Kliendi valuuta"),
    ("Customers", "Клиенты", "Kliendid"),
    ("Customizations", "Настройки", "Kohandused"),
    ("Customize Form", "Настроить форму", "Kohanda vormi"),
    ("Customize your invoices by adding a logo and address details", "Настройте счета-фактуры, добавив логотип и адресные данные", "Kohandage arveid, lisades logo ja aadressiandmed"),
    ("Dashboard", "Панель управления", "Töölaud"),
    ("Data", "Данные", "Andmed"),
    ("Database Error", "Ошибка базы данных", "Andmebaasi viga"),
    ("Database file: ${0}", "Файл базы данных: ${0}", "Andmebaasifail: ${0}"),
    ("Date", "Дата", "Kuupäev"),
    ("Date Format", "Формат даты", "Kuupäeva formaat"),
    ("Date Time", "Дата и время", "Kuupäev ja aeg"),
    ("Day", "День", "Päev"),
    ("Debit", "Дебет", "Deebet"),
    ("Debit Note", "Дебет-нота", "Deebetarve"),
    ("Debtors", "Дебиторы", "Võlgnikud"),
    ("December", "Декабрь", "Detsember"),
    ("Decrease print template display scale", "Уменьшить масштаб шаблона печати", "Vähenda prindimalli kuvamismõõtkava"),
    ("Default", "По умолчанию", "Vaikimisi"),
    ("Default Account", "Счёт по умолчанию", "Vaikimisi konto"),
    ("Default Cash Denominations", "", ""),
    ("Default Location", "Местоположение по умолчанию", "Vaikimisi asukoht"),
    ("Defaults", "Значения по умолчанию", "Vaikeväärtused"),
    ("Delete", "Удалить", "Kustuta"),
    ("Delete ${0}?", "Удалить ${0}?", "Kustutada ${0}?"),
    ("Delete Account", "Удалить счёт", "Kustuta konto"),
    ("Delete Failed", "Удаление не удалось", "Kustutamine ebaõnnestus"),
    ("Delete Group", "Удалить группу", "Kustuta grupp"),
    ("Delivered", "", ""),
    ("Denomination", "", ""),
    ("Depreciation", "Амортизация", "Kulum"),
    ("Depreciation Entry", "Запись амортизации", "Kulumi kirje"),
    ("Description", "Описание", "Kirjeldus"),
    ("Details", "Детали", "Üksikasjad"),
    ("Difference Amount", "Разница суммы", "Vahe summa"),
    ("Direct Expenses", "Прямые расходы", "Otsesed kulud"),
    ("Direct Income", "Прямые доходы", "Otsesed tulud"),
    ("Directory for database file ${0} does not exist, please select the file manually", "", ""),
    ("Disabled", "Отключено", "Keelatud"),
    ("Discount Account", "Счёт скидок", "Allahindluste konto"),
    ("Discount Account is not set.", "Счёт скидок не задан.", "Allahindluste konto ei ole määratud."),
    ("Discount Amount", "Сумма скидки", "Allahindluse summa"),
    ("Discount Amount (${0}) cannot be greated than Amount (${1}).", "Сумма скидки (${0}) не может превышать сумму (${1}).", "Allahindluse summa (${0}) ei tohi olla suurem kui summa (${1})."),
    ("Discount Percent", "Процент скидки", "Allahindluse protsent"),
    ("Discount Percent (${0}) cannot be greater than 100.", "Процент скидки (${0}) не может превышать 100.", "Allahindluse protsent (${0}) ei saa olla suurem kui 100."),
    ("Discounted Amount", "Сумма со скидкой", "Allahinnatud summa"),
    ("Discounts", "Скидки", "Allahindlused"),
    ("Display Doc", "", ""),
    ("Display Logo in Invoice", "Отображать логотип в счёте-фактуре", "Kuva logo arvel"),
    ("Display Precision", "Точность отображения", "Kuvamise täpsus"),
    ("Display Precision should have a value between 0 and 9.", "Точность отображения должна быть от 0 до 9.", "Kuvamise täpsus peab olema vahemikus 0–9."),
    ("Display Scale", "", ""),
    ("Dividends Paid", "Выплаченные дивиденды", "Makstud dividendid"),
    ("Doc ${0} ${1} not set", "", ""),
    ("Docs", "Документы", "Dokumendid"),
    ("Documentation", "Документация", "Dokumentatsioon"),
    ("Does Not Contain", "Не содержит", "Ei sisalda"),
    ("Done", "Готово", "Valmis"),
    ("Dr.", "", ""),
    ("Dr. ${0}", "", ""),
    ("Draft", "Черновик", "Mustand"),
    ("Duplicate", "Дублировать", "Dubleeri"),
    ("Duplicate Entry", "", ""),
    ("Duplicate Template", "", ""),
    ("Duplicate columns found: ${0}", "", ""),
    ("Duties and Taxes", "Пошлины и налоги", "Tollimaksud ja maksud"),
    ("Dynamic Link", "", ""),
    ("Earnest Money", "Задаток", "Tagatisraha"),
    ("Electronic Equipments", "Электронное оборудование", "Elektroonikaseadmed"),
    ("Email", "Электронная почта", "E-post"),
    ("Email Address", "Адрес электронной почты", "E-posti aadress"),
    ("Empty", "Пусто", "Tühi"),
    ("Empty file selected", "", ""),
    ("Enable Barcodes", "", ""),
    ("Enable Batches", "", ""),
    ("Enable Discount Accounting", "Включить учёт скидок", "Luba allahindluste arvestus"),
    ("Enable Form Customization", "", ""),
    ("Enable Inventory", "Включить инвентаризацию", "Luba varude arvestus"),
    ("Enable Invoice Returns", "", ""),
    ("Enable Point of Sale", "", ""),
    ("Enable Price List", "", ""),
    ("Enable Serial Number", "", ""),
    ("Enable Stock Returns", "", ""),
    ("Enable UOM Conversion", "", ""),
    ("Enabled", "Включено", "Lubatud"),
    ("Enabled For", "", ""),
    ("Enter Country to load States", "Введите страну для загрузки регионов", "Sisestage riik, et laadida maakonnad"),
    ("Enter State", "Введите регион", "Sisestage maakond"),
    ("Enter barcode", "", ""),
    ("Entertainment Expenses", "Представительские расходы", "Vastuvõtukulud"),
    ("Entry", "Запись", "Kirje"),
    ("Entry Currency", "Валюта записи", "Kirje valuuta"),
    ("Entry Label", "Метка записи", "Kirje silt"),
    ("Entry No", "Номер записи", "Kirje nr"),
    ("Entry No.", "Номер записи", "Kirje nr."),
    ("Entry Type", "Тип записи", "Kirje tüüp"),
    ("Entry has Grand Total ${0}. Please verify amounts.", "", ""),
    ("Equity", "Капитал", "Omakapital"),
    ("Error", "Ошибка", "Viga"),
    ("Exchange Gain/Loss", "Курсовая прибыль/убыток", "Valuutakursi kasum/kahjum"),
    ("Exchange Rate", "Обменный курс", "Vahetuskurss"),
    ("Excise Entry", "Акцизная запись", "Aktsiisikirje"),
    ("Existing Company", "Существующая компания", "Olemasolev ettevõte"),
    ("Expand", "Развернуть", "Laienda"),
    ("Expected Amount", "Ожидаемая сумма", "Oodatav summa"),
    ("Expense", "Расход", "Kulu"),
    ("Expense Account", "Счёт расходов", "Kulukonto"),
    ("Expenses", "Расходы", "Kulud"),
    ("Expenses Included In Valuation", "Расходы, включённые в оценку", "Hindamisse kaasatud kulud"),
    ("Expiry Date", "Срок действия", "Aegumiskuupäev"),
    ("Export", "Экспорт", "Eksport"),
    ("Export Failed", "Экспорт не удался", "Eksport ebaõnnestus"),
    ("Export Format", "Формат экспорта", "Ekspordi formaat"),
    ("Export Successful", "Экспорт успешен", "Eksport õnnestus"),
    ("Export Wizard", "", ""),
    ("Failed", "Не удалось", "Ebaõnnestus"),
    ("Fax", "Факс", "Faks"),
    ("Features", "", ""),
    ("February", "Февраль", "Veebruar"),
    ("Field", "Поле", "Väli"),
    ("Fieldname", "Имя поля", "Välja nimi"),
    ("Fieldname ${0} already exists for ${1}", "", ""),
    ("Fieldname ${0} already used for Custom Field ${1}", "", ""),
    ("Fieldtype", "", ""),
    ("File ${0} does not exist.", "Файл ${0} не существует.", "Fail ${0} ei eksisteeri."),
    ("File selection failed", "", ""),
    ("Fill", "", ""),
    ("Filter", "Фильтр", "Filter"),
    ("Fiscal Year", "Финансовый год", "Majandusaasta"),
    ("Fiscal Year End Date", "Дата окончания финансового года", "Majandusaasta lõppkuupäev"),
    ("Fiscal Year Start Date", "Дата начала финансового года", "Majandusaasta alguskuupäev"),
    ("Fix Failed", "", ""),
    ("Fixed Asset", "Основное средство", "Põhivara"),
    ("Fixed Assets", "Основные средства", "Põhivarad"),
    ("Float", "", ""),
    ("Following cells have errors: ${0}.", "", ""),
    ("Following links do not exist: ${absentLinks .map((l) =>", "", ""),
    ("Font", "Шрифт", "Font"),
    ("For Purchase", "", ""),
    ("For Sales", "", ""),
    ("Forbidden Error", "", ""),
    ("Form Section", "", ""),
    ("Form Tab", "", ""),
    ("Form Type", "", ""),
    ("Fr", "", ""),
    ("Fraction", "Дробь", "Murd"),
    ("Fraction Units", "Дробные единицы", "Murdühikud"),
    ("Arveli does not have access to the selected file: ${0}", "", ""),
    ("Freight and Forwarding Charges", "Транспортные расходы", "Veokulud ja ekspedeerimistasud"),
    ("From", "С", "Alates"),
    ("From Account", "Со счёта", "Kontolt"),
    ("From Date", "С даты", "Alguskuupäev"),
    ("From Loc.", "", ""),
    ("From Year", "С года", "Aastast"),
    ("Full Name", "Полное имя", "Täisnimi"),
    ("Furnitures and Fixtures", "Мебель и инвентарь", "Mööbel ja sisustus"),
    ("GST", "", ""),
    ("GSTIN No.", "", ""),
    ("GSTR1", "", ""),
    ("GSTR2", "", ""),
    ("Gain/Loss on Asset Disposal", "Прибыль/убыток от выбытия актива", "Kasum/kahjum vara müügist"),
    ("General", "Общее", "Üldine"),
    ("General Ledger", "Главная книга", "Pearaamat"),
    ("Get Started", "Начать", "Alusta"),
    ("Global", "", ""),
    ("Go back to the previous page", "", ""),
    ("Gram", "", ""),
    ("Grand Total", "Итого", "Kokku"),
    ("Greater Than", "Больше чем", "Suurem kui"),
    ("Green", "Зелёный", "Roheline"),
    ("Group By", "Группировать по", "Grupeeri"),
    ("HSN/SAC", "", ""),
    ("HSN/SAC Code", "", ""),
    ("Half Yearly", "Полугодовой", "Poolaastane"),
    ("Half Years", "Полугодия", "Poolaastad"),
    ("Has Batch", "", ""),
    ("Has Serial Number", "", ""),
    ("Height (in cm)", "Высота (в см)", "Kõrgus (cm)"),
    ("Help", "Помощь", "Abi"),
    ("Hex Value", "Шестнадцатеричное значение", "Hex väärtus"),
    ("Hidden values will be visible on Print on.", "", ""),
    ("Hide Get Started", "Скрыть «Начать»", "Peida «Alusta»"),
    ("Hide Group Amounts", "Скрыть суммы групп", "Peida grupisummad"),
    ("Hide Month/Year", "", ""),
    ("Hides the Get Started section from the sidebar. Change will be visible on restart or refreshing the app.", "", ""),
    ("Hour", "Час", "Tund"),
    ("INR", "", ""),
    ("Image", "Изображение", "Pilt"),
    ("Import Complete", "Импорт завершён", "Import lõpetatud"),
    ("Import Data", "Импорт данных", "Andmete import"),
    ("Import Data.", "Импорт данных.", "Andmete import."),
    ("Import Type", "Тип импорта", "Impordi tüüp"),
    ("Import Wizard", "", ""),
    ("Importer not set, reload tool", "", ""),
    ("Inactive", "Неактивный", "Mitteaktiivne"),
    ("Include Cancelled", "Включить отменённые", "Kaasa tühistatud"),
    ("Income", "Доход", "Tulu"),
    ("Income Account", "Счёт доходов", "Tulukonto"),
    ("Increase print template display scale", "", ""),
    ("Indigo", "", ""),
    ("Indirect Expenses", "Косвенные расходы", "Kaudsed kulud"),
    ("Indirect Income", "Косвенные доходы", "Kaudsed tulud"),
    ("Inflow", "Поступления", "Laekumine"),
    ("Instance Id", "ID экземпляра", "Eksemplari ID"),
    ("Insufficient Quantity", "Недостаточное количество", "Ebapiisav kogus"),
    ("Insufficient Quantity.", "Недостаточное количество.", "Ebapiisav kogus."),
    ("Insufficient Quantity. Item ${0} has only ${1} quantities available. you selected ${2}", "", ""),
    ("Int", "", ""),
    ("Intergrated Tax", "Интегрированный налог", "Integreeritud maks"),
    ("Internal Precision", "Внутренняя точность", "Sisemine täpsus"),
    ("Invalid Key Error", "", ""),
    ("Invalid Quantity for Item ${0}", "", ""),
    ("Invalid barcode value ${0}.", "", ""),
    ("Invalid value ${0} for ${1}", "Недопустимое значение ${0} для ${1}", "Vigane väärtus ${0} väljale ${1}"),
    ("Invalid value found for ${0}", "", ""),
    ("Inventory", "", ""),
    ("Inventory Settings", "", ""),
    ("Investments", "Инвестиции", "Investeeringud"),
    ("Invoice", "Счёт-фактура", "Arve"),
    ("Invoice Created", "Счёт-фактура создан", "Arve loodud"),
    ("Invoice Date", "Дата счёта-фактуры", "Arve kuupäev"),
    ("Invoice Item", "", ""),
    ("Invoice No", "Номер счёта-фактуры", "Arve nr"),
    ("Invoice No.", "Номер счёта-фактуры", "Arve nr."),
    ("Invoice Value", "Стоимость счёта-фактуры", "Arve väärtus"),
    ("Invoices", "Счета-фактуры", "Arved"),
    ("Is", "Является", "On"),
    ("Is Custom", "", ""),
    ("Is Empty", "Пусто", "On tühi"),
    ("Is Group", "Является группой", "On grupp"),
    ("Is Landscape", "", ""),
    ("Is Not", "Не является", "Ei ole"),
    ("Is Not Empty", "Не пусто", "Ei ole tühi"),
    ("Is POS Shift Open", "", ""),
    ("Is Price List Enabled", "", ""),
    ("Is Required", "", ""),
    ("Is Whole", "Является целым", "On täisarv"),
    ("Item", "Товар", "Kaup"),
    ("Item ${0} has Zero Quantity", "", ""),
    ("Item ${0} is a batched item", "", ""),
    ("Item ${0} is not a batched item", "", ""),
    ("Item ${0} not in Stock", "", ""),
    ("Item Description", "Описание товара", "Kauba kirjeldus"),
    ("Item Discounts", "", ""),
    ("Item Name", "Название товара", "Kauba nimi"),
    ("Item Prices", "", ""),
    ("Item with From location not found", "", ""),
    ("Item with To location not found", "", ""),
    ("Item with barcode ${0} not found.", "", ""),
    ("Items", "Товары", "Kaubad"),
    ("January", "Январь", "Jaanuar"),
    ("John Doe", "", ""),
    ("Journal Entries", "Журнальные записи", "Raamatupidamiskirjed"),
    ("Journal Entry", "Журнальная запись", "Raamatupidamiskirje"),
    ("Journal Entry Account", "Счёт журнальной записи", "Raamatupidamiskirje konto"),
    ("Journal Entry Number Series", "", ""),
    ("Journal Entry Print Template", "", ""),
    ("July", "Июль", "Juuli"),
    ("June", "Июнь", "Juuni"),
    ("Key Hints", "", ""),
    ("Kg", "", ""),
    ("Label", "Метка", "Silt"),
    ("Language", "Язык", "Keel"),
    ("Left Index", "Левый индекс", "Vasak indeks"),
    ("Legal Expenses", "Юридические расходы", "Õigusabikulud"),
    ("Less Filters", "Меньше фильтров", "Vähem filtreid"),
    ("Less Than", "Меньше чем", "Väiksem kui"),
    ("Liability", "Обязательство", "Kohustus"),
    ("Limit", "", ""),
    ("Link", "", ""),
    ("Link Validation Error", "", ""),
    ("Linked Entries", "", ""),
    ("List", "Список", "Loend"),
    ("List View", "", ""),
    ("Load an existing company from your computer", "", ""),
    ("Loading Report...", "Загрузка отчёта...", "Aruande laadimine..."),
    ("Loading instance...", "", ""),
    ("Loading...", "Загрузка...", "Laadimine..."),
    ("Loans (Liabilities)", "Займы (Обязательства)", "Laenud (kohustused)"),
    ("Loans and Advances (Assets)", "Займы и авансы (Активы)", "Laenud ja ettemaksed (varad)"),
    ("Locale", "", ""),
    ("Location", "", ""),
    ("Location Name", "", ""),
    ("Logo", "", ""),
    ("Make Entry", "Создать запись", "Loo kirje"),
    ("Make Payment On Submit", "", ""),
    ("Make Purchase Receipt On Submit", "", ""),
    ("Make Shipment On Submit", "", ""),
    ("Mandatory Error", "", ""),
    ("Manufacture", "", ""),
    ("Manufacture Date", "", ""),
    ("Mar 23, 2022", "", ""),
    ("March", "Март", "Märts"),
    ("Mark ${0} as submitted?", "Отметить ${0} как проведённый?", "Märkida ${0} esitatuks?"),
    ("Marketing Expenses", "Расходы на маркетинг", "Turunduskulud"),
    ("Material Issue", "", ""),
    ("Material Receipt", "", ""),
    ("Material Transfer", "", ""),
    ("May", "Май", "Mai"),
    ("Meter", "", ""),
    ("Misc", "Разное", "Muud"),
    ("Miscellaneous", "Разное", "Mitmesugune"),
    ("Miscellaneous Expenses", "Разные расходы", "Mitmesugused kulud"),
    ("Mo", "", ""),
    ("Modified", "Изменено", "Muudetud"),
    ("Modified By", "Изменено пользователем", "Muudetud kasutaja poolt"),
    ("Monthly", "Ежемесячный", "Igakuine"),
    ("Months", "Месяцы", "Kuud"),
    ("More", "Ещё", "Rohkem"),
    ("More Filters", "Больше фильтров", "Rohkem filtreid"),
    ("More shortcuts will be added soon.", "", ""),
    ("Movement Type", "", ""),
    ("Name", "Название", "Nimi"),
    ("Navigate", "Навигация", "Navigeeri"),
    ("Need ${0} Serial Numbers for Item ${1}. You have provided ${2}", "", ""),
    ("Net Total", "Итого без налогов", "Netosumma"),
    ("New ${0}", "Новый ${0}", "Uus ${0}"),
    ("New ${0} ${1}", "", ""),
    ("New Account", "Новый счёт", "Uus konto"),
    ("New Company", "", ""),
    ("New Entry", "Новая запись", "Uus kirje"),
    ("New Template", "", ""),
    ("No", "Нет", "Ei"),
    ("No Display Entries Found", "", ""),
    ("No Print Templates not found for entry type ${0}", "", ""),
    ("No Value", "", ""),
    ("No Values to be Displayed", "Нет значений для отображения", "Kuvamiseks väärtused puuduvad"),
    ("No entries found", "Записи не найдены", "Kirjeid ei leitud"),
    ("No entries were imported.", "", ""),
    ("No expenses in this period", "Расходов в этом периоде нет", "Sellel perioodil kulud puuduvad"),
    ("No filters selected", "Фильтры не выбраны", "Filtreid ei ole valitud"),
    ("No linked entries found", "", ""),
    ("No results found", "Результаты не найдены", "Tulemusi ei leitud"),
    ("No results found, disable filters", "Результаты не найдены, отключите фильтры", "Tulemusi ei leitud, keelake filtrid"),
    ("No rows added. Select a file or add rows.", "", ""),
    ("No transactions yet", "Транзакций ещё нет", "Tehinguid pole veel"),
    ("Non Active Serial Number ${0} cannot be used as Manufacture raw material", "", ""),
    ("Non Active Serial Number ${0} cannot be used for Material Issue", "", ""),
    ("Non Active Serial Number ${0} cannot be used for Material Transfer", "", ""),
    ("Non Inactive Serial Number ${0} cannot be used for Material Receipt", "", ""),
    ("None", "Нет", "Puudub"),
    ("Not Found", "", ""),
    ("Not Saved", "Не сохранено", "Salvestamata"),
    ("Not Submitted", "", ""),
    ("Not Transferred", "", ""),
    ("Notes", "Заметки", "Märkused"),
    ("November", "Ноябрь", "November"),
    ("Number Display", "", ""),
    ("Number Series", "Серия номеров", "Numbriseeriate"),
    ("Number of ${0}", "Количество ${0}", "${0} arv"),
    ("Number of Rows", "", ""),
    ("October", "Октябрь", "Oktoober"),
    ("Office Equipments", "Офисное оборудование", "Kontoriseadmed"),
    ("Office Maintenance Expenses", "Расходы на обслуживание офиса", "Kontori hoolduskulud"),
    ("Office Rent", "Аренда офиса", "Kontori üür"),
    ("Okay", "Хорошо", "Olgu"),
    ("Onboarding Complete", "Регистрация завершена", "Sisseelamine lõpetatud"),
    ("Only From or To can be set for Manufacture", "", ""),
    ("Open Count", "Открытое количество", "Avatud arv"),
    ("Open Documentation", "", ""),
    ("Open Folder", "Открыть папку", "Ava kaust"),
    ("Open Print View", "", ""),
    ("Open Print View if Print is available.", "", ""),
    ("Open Quick Search", "", ""),
    ("Open Report Print View", "", ""),
    ("Open the Export Wizard modal", "", ""),
    ("Opening (Cr)", "Открытие (Кр)", "Avamine (Kr)"),
    ("Opening (Dr)", "Открытие (Дб)", "Avamine (Db)"),
    ("Opening Amount", "Сумма открытия", "Avamissumma"),
    ("Opening Balance Equity", "Капитал начального баланса", "Avabilansi omakapital"),
    ("Opening Balances", "Начальные остатки", "Avabilansi saldod"),
    ("Opening Cash Amount can not be negative.", "", ""),
    ("Opening Cash In Denominations", "", ""),
    ("Opening Date", "Дата открытия", "Avamiskuupäev"),
    ("Opening Entry", "Запись открытия", "Avakirje"),
    ("Options", "Параметры", "Valikud"),
    ("Orange", "Оранжевый", "Oranž"),
    ("Organisation", "Организация", "Organisatsioon"),
    ("Outflow", "Выплаты", "Väljaminek"),
    ("Outstanding", "Непогашенный", "Tasumata"),
    ("Outstanding Amount", "Непогашенная сумма", "Tasumata summa"),
    ("POS", "", ""),
    ("POS Counter Cash Account is not set. Please set it on POS Settings", "", ""),
    ("POS Customer", "", ""),
    ("POS Inventory is not set. Please set it on POS Settings", "", ""),
    ("POS Settings", "", ""),
    ("POS Shift Amount", "", ""),
    ("POS Write Off Account is not set. Please set it on POS Settings", "", ""),
    ("Pad Zeros", "Дополнить нулями", "Täida nullidega"),
    ("Page", "Страница", "Lehekülg"),
    ("Paid", "Оплачено", "Makstud"),
    ("Paid ${0}", "Оплачено ${0}", "Makstud ${0}"),
    ("Paid Change", "", ""),
    ("Parent", "Родитель", "Vanem"),
    ("Parent Account", "Родительский счёт", "Ülakonto"),
    ("Party", "Контрагент", "Osapool"),
    ("Patch Run", "Запуск патча", "Paigu käivitamine"),
    ("Pay", "Оплатить", "Maksa"),
    ("Payable", "К оплате", "Tasumisele kuuluv"),
    ("Payment", "Платёж", "Makse"),
    ("Payment ${0} is Saved", "", ""),
    ("Payment For", "Платёж за", "Makse eest"),
    ("Payment Method", "Способ оплаты", "Makseviis"),
    ("Payment No", "Номер платежа", "Makse nr"),
    ("Payment Number Series", "", ""),
    ("Payment Print Template", "", ""),
    ("Payment Reference", "Платёжный референс", "Makse viide"),
    ("Payment Type", "Тип платежа", "Makse tüüp"),
    ("Payment amount cannot be ${0}.", "Сумма платежа не может быть ${0}.", "Makse summa ei tohi olla ${0}."),
    ("Payment amount cannot be less than zero.", "Сумма платежа не может быть менее нуля.", "Makse summa ei tohi olla negatiivne."),
    ("Payment amount cannot exceed ${0}.", "Сумма платежа не может превышать ${0}.", "Makse summa ei tohi ületada ${0}."),
    ("Payment amount: ${0} should be greater than 0.", "Сумма платежа: ${0} должна быть больше 0.", "Makse summa: ${0} peab olema suurem kui 0."),
    ("Payment amount: ${0} should be less than Outstanding amount: ${1}.", "Сумма платежа: ${0} должна быть меньше непогашенной суммы: ${1}.", "Makse summa: ${0} peab olema väiksem kui tasumata summa: ${1}."),
    ('Payment of ${0} will be made from account "${1}" to account "${2}" on Submit.', "", ""),
    ("Payments", "Платежи", "Maksed"),
    ("Payroll Payable", "Задолженность по зарплате", "Palgavõlg"),
    ("Pending Qty. ${0}", "Ожидаемое кол-во ${0}", "Ootel kogus ${0}"),
    ("Pending qty. ${0}", "Ожидаемое кол-во ${0}", "Ootel kogus ${0}"),
    ("Periodicity", "Периодичность", "Perioodilisus"),
    ("Phone", "Телефон", "Telefon"),
    ("Pick Columns", "", ""),
    ("Pick Import Columns", "", ""),
    ("Pink", "Розовый", "Roosa"),
    ("Place", "Место", "Koht"),
    ("Place of supply", "Место поставки", "Tarnimise koht"),
    ("Plants and Machineries", "Оборудование и механизмы", "Tehased ja masinad"),
    ("Please Wait", "Пожалуйста, подождите", "Palun oodake"),
    ("Please check Key Hints for valid key names", "", ""),
    ("Please create a ${0} entry to view Template Preview.", "", ""),
    ("Please fill all values.", "", ""),
    ("Please restart and try again.", "", ""),
    ("Please select a Print Template", "", ""),
    ("Please select a valid reference type.", "Пожалуйста, выберите корректный тип ссылки.", "Palun valige kehtiv viite tüüp."),
    ("Please set GSTIN in General Settings.", "", ""),
    ("Please set Round Off Account in the Settings.", "Пожалуйста, задайте счёт округления в настройках.", "Palun määrake ümardamiskonto seadetes."),
    ("Please set a Display Doc", "", ""),
    ("Point of Sale", "", ""),
    ("Postal Code", "Почтовый индекс", "Postiindeks"),
    ("Postal Expenses", "Почтовые расходы", "Postikulud"),
    ("Posting Date", "Дата проводки", "Kandmise kuupäev"),
    ("Prefix", "Префикс", "Eesliide"),
    ("Price List", "", ""),
    ("Price List Item", "", ""),
    ("Prime Bank", "Первоклассный банк", "Esmaklassiline pank"),
    ("Print", "Печать", "Prindi"),
    ("Print ${0}", "", ""),
    ("Print Settings", "Настройки печати", "Prindiseaded"),
    ("Print Setup", "", ""),
    ("Print Template", "", ""),
    ("Print Template Name not set", "", ""),
    ("Print Template is empty", "", ""),
    ("Print Templates", "", ""),
    ("Print View", "", ""),
    ("Print and Stationery", "Печать и канцтовары", "Trükikulud ja kirjatarbed"),
    ("Product", "Продукт", "Toode"),
    ("Profit And Loss", "Прибыли и убытки", "Kasumi- ja kahjumiaruanne"),
    ("Profit and Loss", "Прибыли и убытки", "Kasumi- ja kahjumiaruanne"),
    ("Purchase", "Закупка", "Ost"),
    ("Purchase Acc.", "", ""),
    ("Purchase Invoice", "Счёт на закупку", "Ostuarve"),
    ("Purchase Invoice Item", "Позиция счёта на закупку", "Ostuarve kaup"),
    ("Purchase Invoice Number Series", "", ""),
    ("Purchase Invoice Print Template", "", ""),
    ("Purchase Invoice Terms", "", ""),
    ("Purchase Invoices", "Счета на закупку", "Ostuarved"),
    ("Purchase Item", "", ""),
    ("Purchase Item Created", "Позиция закупки создана", "Ostukaup loodud"),
    ("Purchase Items", "Позиции закупки", "Ostukaubad"),
    ("Purchase Payment", "", ""),
    ("Purchase Payment Account", "", ""),
    ("Purchase Payments", "Платежи за закупки", "Ostumaksed"),
    ("Purchase Receipt", "", ""),
    ("Purchase Receipt Item", "", ""),
    ("Purchase Receipt Location", "", ""),
    ("Purchase Receipt Number Series", "", ""),
    ("Purchase Receipt Print Template", "", ""),
    ("Purchase Receipt Terms", "", ""),
    ("Purchases", "Закупки", "Ostud"),
    ("Purple", "Фиолетовый", "Lilla"),
    ("Purpose", "", ""),
    ("Qty in Batch", "", ""),
    ("Qty. ${0}", "Кол-во ${0}", "Kogus ${0}"),
    ("Qty. in Transfer Unit", "", ""),
    ("Quantity", "Количество", "Kogus"),
    ("Quantity (${0}) has to be greater than zero", "", ""),
    ("Quantity needs to be set", "", ""),
    ("Quarterly", "Квартальный", "Kvartaalne"),
    ("Quarters", "Кварталы", "Kvartalid"),
    ("Quick Search", "", ""),
    ("Quick edit error: ${0} entry has no name.", "", ""),
    ("Quote", "Цитата", "Hinnapakkumine"),
    ("Quote Reference", "Ссылка на цитату", "Hinnapakkumise viide"),
    ("Rate", "Ставка", "Määr"),
    ("Rate (${0}) cannot be less zero.", "Ставка (${0}) не может быть отрицательной.", "Määr (${0}) ei tohi olla negatiivne."),
    ("Rate (${0}) has to be greater than zero", "", ""),
    ("Rate can't be negative.", "Ставка не может быть отрицательной.", "Määr ei tohi olla negatiivne."),
    ("Rate needs to be set", "", ""),
    ("Raw Value: ${0}", "", ""),
    ("Receivable", "К получению", "Laekuv"),
    ("Receive", "Получить", "Saa"),
    ("Red", "Красный", "Punane"),
    ("Ref Name", "Имя ссылки", "Viite nimi"),
    ("Ref Type", "Тип ссылки", "Viite tüüp"),
    ("Ref. / Cheque No.", "Реф. / Номер чека", "Viide / Tšeki nr"),
    ("Ref. Date", "Дата ссылки", "Viite kuupäev"),
    ("Ref. Name", "Имя ссылки", "Viite nimi"),
    ("Ref. Type", "Тип ссылки", "Viite tüüp"),
    ("Reference", "Ссылка", "Viide"),
    ("Reference Date", "Дата ссылки", "Viite kuupäev"),
    ("Reference Number", "Номер ссылки", "Viite number"),
    ("Reference Type", "Тип ссылки", "Viite tüüp"),
    ("References", "", ""),
    ("Reload Arveli?", "", ""),
    ("Report", "Отчёт", "Aruanne"),
    ("Report Error", "Ошибка отчёта", "Aruande viga"),
    ("Report Issue", "Сообщить о проблеме", "Teata probleemist"),
    ("Report will use more than one page if required.", "", ""),
    ("Reports", "Отчёты", "Aruanded"),
    ("Required fields not selected: ${0}", "", ""),
    ("Retained Earnings", "Нераспределённая прибыль", "Jaotamata kasum"),
    ("Return", "", ""),
    ("Return Against", "", ""),
    ("Return Issued", "", ""),
    ("Reverse Chrg.", "Обратное начисление", "Pöördkäibemaks"),
    ("Reverted", "Отменено", "Tagasi pööratud"),
    ("Reverts", "Отменяет", "Pöörab tagasi"),
    ("Review Accounts", "Проверить счета", "Vaata kontod üle"),
    ("Review your chart of accounts, add any account or tax heads as needed", "Проверьте план счетов, добавьте счета или налоговые статьи по необходимости", "Vaadake kontoplaani üle, lisage vajadusel kontosid või maksurühmi"),
    ("Right Index", "Правый индекс", "Parem indeks"),
    ("Role", "Роль", "Roll"),
    ("Root Type", "Корневой тип", "Juuretüüp"),
    ("Round Off", "Округлить", "Ümarda"),
    ("Round Off Account", "Счёт округления", "Ümardamiskonto"),
    ("Round Off Account Not Found", "Счёт округления не найден", "Ümardamiskontot ei leitud"),
    ("Rounded Off", "Округлено", "Ümardatud"),
    ("Row ${0}", "Строка ${0}", "Rida ${0}"),
    ("Sa", "", ""),
    ("Salary", "Зарплата", "Palk"),
    ("Sales", "Продажи", "Müük"),
    ("Sales Acc.", "", ""),
    ("Sales Expenses", "Расходы на продажи", "Müügikulud"),
    ("Sales Invoice", "Счёт-фактура", "Müügiarve"),
    ("Sales Invoice ${0} is Submitted", "", ""),
    ("Sales Invoice Item", "Позиция счёта-фактуры", "Müügiarve kaup"),
    ("Sales Invoice Number Series", "", ""),
    ("Sales Invoice Print Template", "", ""),
    ("Sales Invoice Terms", "", ""),
    ("Sales Invoices", "Счета-фактуры", "Müügiarved"),
    ("Sales Item", "", ""),
    ("Sales Item Created", "Позиция продажи создана", "Müügikaup loodud"),
    ("Sales Items", "Позиции продажи", "Müügikaubad"),
    ("Sales Payment", "", ""),
    ("Sales Payment Account", "", ""),
    ("Sales Payments", "Платежи за продажи", "Müügimaksed"),
    ("Sales Quote", "Коммерческое предложение", "Hinnapakkumine"),
    ("Sales Quote Item", "", ""),
    ("Sales Quote Number Series", "", ""),
    ("Sales Quote Print Template", "", ""),
    ("Sales Quotes", "Коммерческие предложения", "Hinnapakkumised"),
    ("Sales and Purchase", "", ""),
    ("Save", "Сохранить", "Salvesta"),
    ("Save ${0}?", "", ""),
    ("Save Customizations", "", ""),
    ("Save Template", "Сохранить шаблон", "Salvesta mall"),
    ("Save Template File", "", ""),
    ("Save as PDF", "Сохранить как PDF", "Salvesta PDF-ina"),
    ("Save as PDF Successful", "Сохранено как PDF успешно", "PDF-ina salvestamine õnnestus"),
    ("Save changes made to ${0}?", "", ""),
    ("Save or Submit an entry.", "", ""),
    ("Saved", "Сохранено", "Salvestatud"),
    ("Search an Item", "", ""),
    ("Secured Loans", "Обеспеченные займы", "Tagatud laenud"),
    ("Securities and Deposits", "Ценные бумаги и депозиты", "Väärtpaberid ja deposiidid"),
    ("Select", "Выбрать", "Vali"),
    ("Select CoA", "Выбрать план счетов", "Vali kontoplaan"),
    ("Select Color", "Выбрать цвет", "Vali värv"),
    ("Select Country", "Выбрать страну", "Vali riik"),
    ("Select File", "Выбрать файл", "Vali fail"),
    ("Select Image", "Выбрать изображение", "Vali pilt"),
    ("Select Template File", "", ""),
    ("Select a Display Doc to view the Template", "", ""),
    ("Select a Template type", "", ""),
    ("Select a form type to customize", "", ""),
    ("Select a pre-defined page size, or set a custom page size for your Print Template.", "", ""),
    ("Select column", "", ""),
    ("Select file", "Выбрать файл", "Vali fail"),
    ("Select folder", "Выбрать папку", "Vali kaust"),
    ("Select the template type.", "", ""),
    ("Selected", "Выбрано", "Valitud"),
    ("September", "Сентябрь", "September"),
    ("Serial Number", "", ""),
    ("Serial Number ${0} does not belong to the item ${1}.", "", ""),
    ("Serial Number ${0} does not exist.", "", ""),
    ("Serial Number ${0} is not Active.", "", ""),
    ("Serial Number ${0} is not Inactive", "", ""),
    ("Serial Number ${0} status is not Active.", "", ""),
    ("Serial Number Description", "", ""),
    ("Serial Number is enabled for Item ${0}", "", ""),
    ("Serial Number is not enabled for Item ${0}", "", ""),
    ("Serial Number not set for row ${0}.", "", ""),
    ("Serial Number set for row ${0}.", "", ""),
    ("Service", "Услуга", "Teenus"),
    ("Set Discount Amount", "Установить сумму скидки", "Määra allahindluse summa"),
    ("Set Period", "", ""),
    ("Set Print Size", "Установить размер печати", "Määra prindi suurus"),
    ("Set Template Type", "Установить тип шаблона", "Määra malli tüüp"),
    ("Set Up", "Настройка", "Seadistamine"),
    ("Set Up Your Workspace", "Настройте рабочее пространство", "Seadistage oma tööruum"),
    ("Set a Template value to see the Print Template", "", ""),
    ("Set an Import Type", "Установить тип импорта", "Määra impordi tüüp"),
    ("Set the display language.", "Установить язык отображения.", "Määrake kuvakeel."),
    ("Set the local code. This is used for number formatting.", "Установите локальный код, используемый для форматирования чисел.", "Määrake kohalik kood, mida kasutatakse numbrite vormindamiseks."),
    ("Set up your company information, email, country and fiscal year", "Укажите информацию о компании, email, стране и финансовом году", "Seadistage ettevõtte andmed, e-post, riik ja majandusaasta"),
    ("Set up your opening balances before performing any accounting entries", "Укажите начальные остатки перед выполнением бухгалтерских записей", "Seadistage avabilansi saldod enne raamatupidamiskirjete tegemist"),
    ("Set up your organization", "Настройте вашу организацию", "Seadistage oma organisatsioon"),
    ("Set up your tax templates for your sales or purchase transactions", "Настройте налоговые шаблоны для продаж или закупок", "Seadistage oma müügi- ja ostu-tehingute maksumallid"),
    ("Sets how many digits are shown after the decimal point.", "Устанавливает количество знаков после запятой.", "Määrab kümnendkoha järel kuvatavate numbrite arvu."),
    ("Sets the app-wide date display format.", "Устанавливает формат отображения даты.", "Määrab rakenduse kuupäeva kuvamise vormingu."),
    ("Sets the internal precision used for monetary calculations. Above 6 should be sufficient for most currencies.", "Устанавливает внутреннюю точность для денежных расчётов. Значения выше 6 достаточно для большинства валют.", "Määrab rahaliste arvutuste sisemise täpsuse. Enamiku valuutade jaoks piisab väärtusest üle 6."),
    ("Setting Up Instance", "Настройка экземпляра", "Eksemplari seadistamine"),
    ("Settings", "Настройки", "Seaded"),
    ("Setup", "Настройка", "Seadistus"),
    ("Setup Complete", "Настройка завершена", "Seadistus lõpetatud"),
    ("Setup Wizard", "Мастер настройки", "Seadistusviisard"),
    ("Setup system defaults like date format and display precision", "Настройте системные параметры по умолчанию: формат даты, точность отображения", "Seadistage süsteemi vaikeväärtused nagu kuupäeva formaat ja kuvamise täpsus"),
    ("Shipment", "", ""),
    ("Shipment ${0} is Submitted", "", ""),
    ("Shipment Item", "", ""),
    ("Shipment Location", "", ""),
    ("Shipment Number Series", "", ""),
    ("Shipment Print Template", "", ""),
    ("Shipment Terms", "", ""),
    ("Shortcuts", "Горячие клавиши", "Otseteed"),
    ("Should entries be submitted after syncing?", "Следует ли проводить записи после синхронизации?", "Kas kirjed tuleks esitada pärast sünkroonimist?"),
    ("Show HSN", "", ""),
    ("Show Me", "Показать", "Näita mulle"),
    ("Show Month/Year", "", ""),
    ("Single Value", "Одно значение", "Üksik väärtus"),
    ("Skip Child Tables", "Пропустить дочерние таблицы", "Jäta alustabelid vahele"),
    ("Skip Transactions", "Пропустить транзакции", "Jäta tehingud vahele"),
    ("Smallest Currency Fraction Value", "Минимальная дробная единица валюты", "Valuuta väikseim ühik"),
    ("Softwares", "Программное обеспечение", "Tarkvara"),
    ("Something has gone terribly wrong. Please check the console and raise an issue.", "Что-то пошло очень не так. Проверьте консоль и сообщите о проблеме.", "Midagi läks väga valesti. Kontrollige konsooli ja esitage probleem."),
    ("Source of Funds (Liabilities)", "Источники финансирования (Пассивы)", "Rahastamisallikad (kohustused)"),
    ("Standard Chart of Accounts", "Стандартный план счетов", "Standardkontoplaan"),
    ("Start", "Начало", "Alusta"),
    ("Start From Row Index", "", ""),
    ("State", "Регион", "Maakond"),
    ("State Tax", "Региональный налог", "Maakonna maks"),
    ("Status", "Статус", "Staatus"),
    ("Stock", "", ""),
    ("Stock Adjustment", "Корректировка запасов", "Varude korrigeerimine"),
    ("Stock Assets", "Запасы (активы)", "Varude varad"),
    ("Stock Balance", "", ""),
    ("Stock Entries", "", ""),
    ("Stock Expenses", "Расходы на запасы", "Varude kulud"),
    ("Stock In Hand", "Запасы в наличии", "Laoseis"),
    ("Stock In Hand Acc.", "", ""),
    ("Stock Ledger", "", ""),
    ("Stock Ledger Entry", "", ""),
    ("Stock Liabilities", "Обязательства по запасам", "Varude kohustused"),
    ("Stock Movement", "", ""),
    ("Stock Movement Item", "", ""),
    ("Stock Movement No.", "", ""),
    ("Stock Movement Number Series", "", ""),
    ("Stock Movement Print Template", "", ""),
    ("Stock Movements", "", ""),
    ("Stock Not Received", "", ""),
    ("Stock Not Shipped", "", ""),
    ("Stock Not Transferred", "", ""),
    ("Stock Received But Not Billed", "Запасы получены, но не выставлен счёт", "Kaubad saadud, kuid arveldamata"),
    ("Stock Received But Not Billed Acc.", "", ""),
    ("Stock Transfer Item", "", ""),
    ("Stock Unit", "", ""),
    ("StockTransfer", "", ""),
    ("Stores", "", ""),
    ("Su", "", ""),
    ("Submit", "Провести", "Esita"),
    ("Submit ${0}?", "Провести ${0}?", "Esitada ${0}?"),
    ("Submit & Print", "", ""),
    ("Submit entries?", "", ""),
    ("Submitted", "Проведён", "Esitatud"),
    ("Success", "Успех", "Õnnestus"),
    ("Supplier", "Поставщик", "Tarnija"),
    ("Supplier Created", "Поставщик создан", "Tarnija loodud"),
    ("Suppliers", "Поставщики", "Tarnijad"),
    ("Symbol", "Символ", "Sümbol"),
    ("System", "Система", "Süsteem"),
    ("System Settings", "Системные настройки", "Süsteemi seaded"),
    ("System Setup", "Системная настройка", "Süsteemi seadistus"),
    ("Table", "", ""),
    ("Target", "", ""),
    ("Tax", "Налог", "Maks"),
    ("Tax Account", "Налоговый счёт", "Maksukonto"),
    ("Tax Amount", "Сумма налога", "Maksusumma"),
    ("Tax Assets", "Налоговые активы", "Maksuvarad"),
    ("Tax Detail", "Детали налога", "Maksu üksikasiad"),
    ("Tax ID", "Налоговый ID", "Maksu ID"),
    ("Tax Invoice Account", "", ""),
    ("Tax Payment Account", "", ""),
    ("Tax Rate", "Налоговая ставка", "Maksumäär"),
    ("Tax Summary", "Сводка по налогам", "Maksukokkuvõte"),
    ("Tax Template", "", ""),
    ("Tax Templates", "", ""),
    ("Tax and Totals", "", ""),
    ("Taxable Value", "Налогооблагаемая сумма", "Maksustatav väärtus"),
    ("Taxed Amount", "Сумма с налогом", "Maksustatud summa"),
    ("Taxes", "Налоги", "Maksud"),
    ("Taxes and Charges", "", ""),
    ("Teal", "", ""),
    ("Telephone Expenses", "Расходы на телефон", "Telefonikulud"),
    ("Template", "Шаблон", "Mall"),
    ("Template Builder", "", ""),
    ("Template Compilation Error", "", ""),
    ("Template Name", "", ""),
    ("Template Type", "", ""),
    ("Template file saved", "", ""),
    ("Temporary", "Временный", "Ajutine"),
    ("Temporary Accounts", "Временные счета", "Ajutised kontod"),
    ("Temporary Opening", "Временное открытие", "Ajutine avamine"),
    ("Terms", "Условия", "Tingimused"),
    ("Text", "Текст", "Tekst"),
    ("Th", "", ""),
    ("The following characters cannot be used ${0} in a Number Series name.", "", ""),
    ("The following items have insufficient quantity for Shipment: ${0}", "", ""),
    ("This Month", "Этот месяц", "Käesolev kuu"),
    ("This Quarter", "Этот квартал", "Käesolev kvartal"),
    ("This Year", "Этот год", "Käesolev aasta"),
    ("This action is permanent", "Это действие необратимо", "See toiming on püsiv"),
    ("This action is permanent and will cancel the following payment: ${0}", "Это действие необратимо и отменит следующий платёж: ${0}", "See toiming on püsiv ja tühistab järgmise makse: ${0}"),
    ("This action is permanent and will cancel the following payments: ${0}", "Это действие необратимо и отменит следующие платежи: ${0}", "See toiming on püsiv ja tühistab järgmised maksed: ${0}"),
    ("This action is permanent and will delete associated ledger entries.", "Это действие необратимо и удалит связанные записи главной книги.", "See toiming on püsiv ja kustutab seotud pearaamatu kirjed."),
    ("This action is permanent.", "Это действие необратимо.", "See toiming on püsiv."),
    ("Times New Roman", "", ""),
    ("To", "До", "Kuni"),
    ("To Account", "На счёт", "Kontole"),
    ("To Account and From Account can't be the same: ${0}", "Счёт назначения и исходный счёт не могут совпадать: ${0}", "Sihtkoha konto ja lähtekonto ei tohi olla samad: ${0}"),
    ("To Date", "По дату", "Lõppkuupäev"),
    ("To Loc.", "", ""),
    ("To Year", "По год", "Aastani"),
    ("Toggle Edit Mode", "", ""),
    ("Toggle Key Hints", "", ""),
    ("Toggle Linked Entries widget, not available in Quick Edit view.", "", ""),
    ("Toggle between form and full width", "", ""),
    ("Toggle sidebar", "", ""),
    ("Toggle the Create filter", "", ""),
    ("Toggle the Docs filter", "", ""),
    ("Toggle the List filter", "", ""),
    ("Toggle the Page filter", "", ""),
    ("Toggle the Report filter", "", ""),
    ("Top Expenses", "Основные расходы", "Peamised kulud"),
    ("Total", "Итого", "Kokku"),
    ("Total Amount", "Общая сумма", "Kogu summa"),
    ("Total Asset (Debit)", "Всего активов (Дебет)", "Varad kokku (deebet)"),
    ("Total Debit: ${0} must be equal to Total Credit: ${1}", "Дебет итого: ${0} должен равняться кредиту итого: ${1}", "Deebet kokku: ${0} peab võrduma kreedit kokku: ${1}"),
    ("Total Discount", "Общая скидка", "Kogu allahindlus"),
    ("Total Equity (Credit)", "Всего капитала (Кредит)", "Omakapital kokku (kreedit)"),
    ("Total Expense (Debit)", "Всего расходов (Дебет)", "Kulud kokku (deebet)"),
    ("Total Income (Credit)", "Всего доходов (Кредит)", "Tulud kokku (kreedit)"),
    ("Total Liability (Credit)", "Всего обязательств (Кредит)", "Kohustused kokku (kreedit)"),
    ("Total Profit", "Общая прибыль", "Kasum kokku"),
    ("Total Quantity", "Общее количество", "Kogus kokku"),
    ("Total Spending", "Общие расходы", "Kogukulud"),
    ("Track Inventory", "Вести учёт запасов", "Jälgi varusid"),
    ("Transfer", "Перевод", "Ülekanne"),
    ("Transfer No", "", ""),
    ("Transfer Type", "Тип перевода", "Ülekande tüüp"),
    ("Transfer Unit", "", ""),
    ("Transfer Unit ${0} is not applicable for Item ${1}", "", ""),
    ("Transfer will cause future entries to have negative stock.", "", ""),
    ("Travel Expenses", "Командировочные расходы", "Lähetuskulud"),
    ("Trial Balance", "Оборотно-сальдовая ведомость", "Käibeandmik"),
    ("Tu", "", ""),
    ("Type", "Тип", "Tüüp"),
    ("Type to search...", "Введите для поиска...", "Sisestage otsimiseks..."),
    ("UOM", "", ""),
    ("UOM Conversion Item", "", ""),
    ("UOM Conversions", "", ""),
    ("Unit", "Единица", "Ühik"),
    ("Unit Type", "Тип единицы", "Ühiku tüüp"),
    ("Unpaid", "Не оплачено", "Maksmata"),
    ("Unpaid ${0}", "Не оплачено ${0}", "Maksmata ${0}"),
    ("Unsecured Loans", "Необеспеченные займы", "Tagamata laenud"),
    ("Until Date", "По дату", "Kuni kuupäevani"),
    ("Use Full Width", "", ""),
    ("Use List Filters", "", ""),
    ("User Remark", "Примечание пользователя", "Kasutaja märkus"),
    ("Utility Expenses", "Коммунальные расходы", "Kommunaalkulud"),
    ("Validation Error", "", ""),
    ("Value", "Значение", "Väärtus"),
    ("Value missing for ${0}", "Значение не указано для ${0}", "Väärtus puudub väljal ${0}"),
    ("Value: ${0}", "Значение: ${0}", "Väärtus: ${0}"),
    ("Version", "Версия", "Versioon"),
    ("View", "Просмотр", "Vaata"),
    ("View Accounting Entries", "", ""),
    ("View Paid Invoices", "", ""),
    ("View Purchases", "Просмотр закупок", "Vaata oste"),
    ("View Sales", "Просмотр продаж", "Vaata müüki"),
    ("View Stock Entries", "", ""),
    ("View Unpaid Invoices", "", ""),
    ("View linked entries", "", ""),
    ("We", "", ""),
    ("Welcome to Arveli", "Tere tulemast Arvelisse", "Tere tulemast Arvelisse"),
    ("Width (in cm)", "Ширина (в см)", "Laius (cm)"),
    ("Write Off", "Списание", "Mahakandmine"),
    ("Write Off Account", "Счёт списания", "Mahakandmise konto"),
    ("Write Off Account ${0} does not exist. Please set Write Off Account in General Settings", "", ""),
    ("Write Off Account not set. Please set Write Off Account in General Settings", "Счёт списания не задан. Задайте счёт списания в общих настройках.", "Mahakandmise konto ei ole määratud. Palun määrake see üldseadetes."),
    ("Write Off Entry", "Запись списания", "Mahakandmise kirje"),
    ("Year to Date", "", ""),
    ("Yearly", "Ежегодный", "Iga-aastane"),
    ("Years", "Годы", "Aastad"),
    ("Yellow", "Жёлтый", "Kollane"),
    ("Yes", "Да", "Jah"),
    ("check values and click on", "проверьте значения и нажмите", "kontrollige väärtusi ja klõpsake"),
    ("in Batch ${0}", "", ""),
    ("john@doe.com", "", ""),
    ("to apply changes", "чтобы применить изменения", "muudatuste rakendamiseks"),
    ("Allow to bypass filters", "Разрешить обход фильтров", "Luba filtrite eiramist"),
    ("When linking documents, if no match is found and filtering is in effect, allow to disable filters.", "При связывании документов, если совпадений не найдено и фильтры активны, разрешить их отключить.", "Dokumentide linkimisel, kui vasteid ei leita ja filtreerimine on aktiivne, lubage filtrid keelata."),
    # ── EE module strings ────────────────────────────────────────────────────
    ("Estonia", "Эстония", "Eesti"),
    ("Bank Import", "Импорт банковских выписок", "Pankade import"),
    ("KMD", "KMD", "KMD"),
    ("Annual Report", "Годовой отчёт", "Aastaaruanne"),
    ("Annual Report (XBRL)", "Годовой отчёт (XBRL)", "Aastaaruanne (XBRL)"),
    ("No draft journal entries.", "Черновых журнальных записей нет.", "Mustandkirjeid ei ole."),
    ("Submit ${0} draft journal entries?", "Провести ${0} черновых журнальных записей?", "Esitada ${0} mustandkirjet?"),
    ("This posts them to the ledger. Each can still be cancelled individually afterwards.", "Это проведёт их в главную книгу. Каждую можно будет отменить по отдельности позже.", "See kannab need pearaamatusse. Kõiki saab hiljem eraldi tühistada."),
    ("Submitted ${0}, ${1} failed.", "Проведено ${0}, ${1} не удалось.", "Esitatud ${0}, ${1} ebaõnnestus."),
    ("Submitted ${0} journal entries.", "Проведено ${0} журнальных записей.", "Esitatud ${0} raamatupidamiskirjet."),
    ("Submit Drafts", "Провести черновики", "Esita mustandid"),
    # EE schema labels
    ("Bank Archival ID", "Архивный ID банка", "Panga arhiivi ID"),
    ("Import Bank", "Банк-импортёр", "Importpank"),
    ("VAT Code", "Код НДС", "Käibemaksukood"),
    ("EU Partner VAT", "НДС партнёра ЕС", "EL partneri KMKR number"),
    ("VAT Number", "Номер НДС", "KMKR number"),
    ("Registry Code", "Регистрационный код", "Registrikood"),
    ("Arelle CLI Path", "Путь к Arelle CLI", "Arelle käsurea tee"),
    ("VAT Status", "Статус НДС", "Käibemaksu staatus"),
    ("Estonian VAT Registered", "Зарегистрирован плательщиком НДС в Эстонии", "Eesti KM kohustuslane"),
    ("Estonian Non-Registered", "Незарегистрированный плательщик НДС в Эстонии", "Eesti KM mittekohustuslane"),
    ("EU Business", "Компания ЕС", "EL ettevõte"),
    ("EU Consumer", "Потребитель ЕС", "EL eraisik"),
    ("Non-EU", "Не-ЕС", "Väljaspool EL"),
    ("VAT Exempt", "Освобождён от НДС", "KM-vaba"),
    # Bank import UI
    ("${0} bank entries created", "Создано ${0} банковских записей", "${0} pangakirjet loodud"),
    ("${0} duplicates skipped", "Пропущено ${0} дублей", "${0} duplikaati vahele jäetud"),
    ("${0} errors — see console", "${0} ошибок — см. консоль", "${0} viga — vaata konsooli"),
    ("${0} reverse-charge entries created", "Создано ${0} записей обратного начисления НДС", "${0} pöördkäibemaksu kirjet loodud"),
    ("${0} errors, ${1} warnings. See first issues below.", "${0} ошибок, ${1} предупреждений. Первые проблемы ниже.", "${0} viga, ${1} hoiatust. Vaata esimesi probleeme allpool."),
    ("Amount (EUR)", "Сумма (EUR)", "Summa (EUR)"),
    ("Arelle CLI path not configured — XBRL validation unavailable. Set path in Accounting Settings.", "Путь к Arelle CLI не настроен — проверка XBRL недоступна. Укажите путь в настройках бухгалтерии.", "Arelle käsurea tee ei ole seadistatud — XBRL valideerimine pole saadaval. Seadista tee raamatupidamise seadetes."),
    ("Arelle binary not found", "Исполняемый файл Arelle не найден", "Arelle käivitatavat faili ei leitud"),
    ("Balance sheet does not balance — Assets ≠ Liabilities + Equity. Fix ledger before exporting.", "Баланс не сходится — Активы ≠ Обязательства + Капитал. Исправьте главную книгу перед экспортом.", "Bilanss ei tasa — Varad ≠ Kohustused + Omakapital. Paranda pearaamat enne eksportimist."),
    ("CSV import is not yet supported for ${0}", "Импорт CSV пока не поддерживается для ${0}", "CSV import ei ole veel toetatud: ${0}"),
    ("Counterparty", "Контрагент", "Vastaspool"),
    ("Create ${0} Entries", "Создать ${0} записей", "Loo ${0} kirjet"),
    ("Create Journal Entries", "Создать журнальные записи", "Loo raamatupidamiskirjeid"),
    ("Created as drafts — review and attach invoices, then submit.", "Созданы как черновики — проверьте и прикрепите счета, затем проведите.", "Loodud mustanditena — vaata üle, lisa arved ja seejärel esita."),
    ("Download the taxonomy zip from xbrl.eesti.ee, unzip it, and place the et-gaap_<version> folder in reports/EstonianAnnualReport/taxonomy/. See the README for details.", "Загрузите zip таксономии с xbrl.eesti.ee, распакуйте его и поместите папку et-gaap_<версия> в reports/EstonianAnnualReport/taxonomy/. Подробности в README.", "Laadi taksonoomia zip alla xbrl.eesti.ee-st, paki lahti ja pane et-gaap_<versioon> kaust reports/EstonianAnnualReport/taxonomy/ kausta. Vaata README."),
    ("Duplicate detection uses the archival ID, so re-importing the same statement is safe.", "Обнаружение дублей использует архивный ID, поэтому повторный импорт одной выписки безопасен.", "Duplikaatide tuvastamine kasutab arhiivi ID-d, seega sama väljavõtte uuesti importimine on ohutu."),
    ("Estonian GAAP taxonomy not found", "Таксономия эстонских GAAP не найдена", "Eesti GAAP taksonoomiat ei leitud"),
    ("Export an XBRL file first. The Validate action checks the most recent export.", "Сначала экспортируйте XBRL файл. Действие проверки проверяет последний экспорт.", "Ekspordi esmalt XBRL fail. Valideerimine kontrollib viimast eksporti."),
    ("Import a ${0} CSV or CAMT.053.001.02 XML statement.", "Импортируйте выписку ${0} CSV или CAMT.053.001.02 XML.", "Impordi ${0} CSV või CAMT.053.001.02 XML väljavõte."),
    ("Import a CAMT.053.001.02 XML statement exported from ${0}. CSV is not yet supported for this bank.", "Импортируйте выписку CAMT.053.001.02 XML, экспортированную из ${0}. CSV для этого банка пока не поддерживается.", "Impordi CAMT.053.001.02 XML väljavõte, mis on eksporditud ${0}-st. CSV ei ole selle panga jaoks veel toetatud."),
    ("Import complete", "Импорт завершён", "Import lõpetatud"),
    ("No errors or warnings — file accepted by arelle.", "Ошибок и предупреждений нет — файл принят Arelle.", "Vigu ega hoiatusi ei ole — Arelle aktsepteeris faili."),
    ("No exported XBRL in this session", "В этом сеансе XBRL не экспортировался", "Selles seansis pole XBRL-i eksporditud"),
    ("No rows found in file.", "В файле строк не найдено.", "Failis ridu ei leitud."),
    ("Open Accounting Settings and set the Arelle CLI Path field.", "Откройте настройки бухгалтерии и укажите поле «Путь к Arelle CLI».", "Ava raamatupidamise seaded ja seadista Arelle käsurea tee väli."),
    ('Path "${0}" is not an executable file. Verify the path in Accounting Settings.', 'Путь "${0}" не является исполняемым файлом. Проверьте путь в настройках бухгалтерии.', 'Tee "${0}" ei ole käivitatav fail. Kontrolli teed raamatupidamise seadetes.'),
    ("Remittance", "Назначение платежа", "Saatekiri"),
    ("Rows are matched against built-in rules (AWS, GitHub, Stripe, Apple/Google payouts, LHV fees). You can override the proposed account and VAT code before committing.", "Строки сопоставляются со встроенными правилами (AWS, GitHub, Stripe, выплаты Apple/Google, комиссии LHV). Вы можете изменить предложенный счёт и код НДС перед подтверждением.", "Read vastavad sisseehitatud reeglitele (AWS, GitHub, Stripe, Apple/Google väljamaksed, LHV tasud). Sa saad enne kinnitamist pakutud kontot ja käibemaksukoodi muuta."),
    ("Select Statement File", "Выбрать файл выписки", "Vali väljavõtte fail"),
    ("Select a bank and import a CAMT.053 XML statement.", "Выберите банк и импортируйте выписку CAMT.053 XML.", "Vali pank ja impordi CAMT.053 XML väljavõte."),
]


# ── CSV build ─────────────────────────────────────────────────────────────────

def csv_row(src: str, tr: str) -> str:
    def q(s: str) -> str:
        if not s:
            return ""
        if "," in s or '"' in s or "\n" in s:
            return '"' + s.replace('"', '""') + '"'
        return s
    return f"{q(src)},{q(tr)},,"


def write_lang(col_idx: int, out_path: str):
    lines = [TIMESTAMP]
    for row in STRINGS:
        lines.append(csv_row(row[0], row[col_idx]))
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Wrote {out_path} ({len(lines) - 1} rows)")


def cmd_build():
    base = _REPO / "translations"
    base.mkdir(exist_ok=True)
    write_lang(1, str(base / "ru.csv"))
    write_lang(2, str(base / "et.csv"))


# ── discovery helpers ─────────────────────────────────────────────────────────

import re as _re
import json as _json
import csv as _csv
from pathlib import Path as _Path

_REPO = _Path(__file__).parent.parent

# dirs/names to never descend into
_SKIP = {"node_modules", "dist", "out", ".git", "__pycache__", "taxonomy", ".cache"}

# skip test/spec files to avoid false positives
_SKIP_SUFFIXES = {".spec.ts", ".test.ts", ".spec.js", ".test.js"}

# regex: t`...` — DOTALL so multiline strings are captured
_T_RE = _re.compile(r"\bt`((?:[^`\\]|\\.)*)`", _re.DOTALL)

# regex: ${anything} → positional ${0}, ${1}, …
_INTERP_RE = _re.compile(r"\$\{[^}]+\}")

# ISO timestamp line in upstream CSVs
_ISO_RE = _re.compile(r"^\d{4}-\d{2}-\d{2}T")


def _normalize(raw: str) -> str:
    """
    Mimic runtime TranslationString normalization:
    replace each ${expr} with ${0}, ${1}, … in order.
    """
    idx = [0]

    def _r(_m):
        n = idx[0]
        idx[0] += 1
        return f"${{{n}}}"

    return _INTERP_RE.sub(_r, raw.replace("\\\n", "").strip())


def _scan_ts_vue(dirs: list) -> set:
    """
    Walk dirs, find all t`` template literals in .ts / .vue files,
    normalize interpolations, return set of source strings.
    """
    found = set()
    for d in dirs:
        p = _REPO / d
        if not p.exists():
            continue
        for f in p.rglob("*"):
            if any(part in _SKIP for part in f.parts):
                continue
            if f.suffix not in (".ts", ".vue"):
                continue
            if any(str(f).endswith(s) for s in _SKIP_SUFFIXES):
                continue
            try:
                text = f.read_text(encoding="utf-8")
            except Exception:
                continue
            for m in _T_RE.finditer(text):
                s = _normalize(m.group(1))
                if s:
                    found.add(s)
    return found


def _scan_json_labels(dirs: list) -> set:
    """
    Walk dirs, extract all 'label' and 'description' string values
    from JSON files (schema field labels go through translateSchemaMap).
    """
    found = set()

    def _walk(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in ("label", "description") and isinstance(v, str) and v.strip():
                    found.add(v.strip())
                else:
                    _walk(v)
        elif isinstance(obj, list):
            for item in obj:
                _walk(item)

    for d in dirs:
        p = _REPO / d
        if not p.exists():
            continue
        for f in p.rglob("*.json"):
            if any(part in _SKIP for part in f.parts):
                continue
            try:
                _walk(_json.loads(f.read_text(encoding="utf-8")))
            except Exception:
                continue
    return found


def _from_upstream_csv(filepath: str) -> set:
    """
    Read source strings (column 0) from any upstream translation CSV.
    Column 0 is always English regardless of which language the CSV targets.
    Skip the leading ISO timestamp line that upstream prepends.
    """
    found = set()
    with open(filepath, encoding="utf-8", newline="") as fh:
        for row in _csv.reader(fh):
            if not row or not row[0]:
                continue
            if _ISO_RE.match(row[0]):
                continue
            found.add(row[0])
    return found


def _known() -> set:
    return {r[0] for r in STRINGS}


def _find_missing(candidates: set) -> list:
    k = _known()
    return sorted(s for s in candidates if s and s not in k)


# ── output formatters ─────────────────────────────────────────────────────────

def _print_check(missing: list):
    if not missing:
        print("No missing strings.")
        return
    print(f"{len(missing)} string(s) not yet in STRINGS:\n")
    for s in missing:
        print(f"  {s!r}")


def _print_stubs(missing: list):
    if not missing:
        print("# No missing strings.")
        return
    print(f"# {len(missing)} stub(s) — paste into STRINGS list in gen_translations.py\n")
    for s in missing:
        q = '"' if "'" in s else "'"
        print(f"    ({q}{s}{q}, \"TODO_RU\", \"TODO_ET\"),")


# ── subcommands ───────────────────────────────────────────────────────────────

# Dirs scanned for all t`` and JSON label strings (full codebase, excl. node_modules)
_ALL_TS_DIRS  = ["src", "fyo", "models", "reports", "regional", "main", "utils"]
_ALL_JSON_DIRS = ["schemas", "models"]


def cmd_check():
    """Scan full codebase; show strings missing from STRINGS."""
    found = _scan_ts_vue(_ALL_TS_DIRS) | _scan_json_labels(_ALL_JSON_DIRS)
    _print_check(_find_missing(found))


def cmd_stub():
    """Scan full codebase; print stub tuples for strings missing from STRINGS."""
    found = _scan_ts_vue(_ALL_TS_DIRS) | _scan_json_labels(_ALL_JSON_DIRS)
    _print_stubs(_find_missing(found))


def cmd_stub_upstream(filepath: str):
    """
    Like cmd_check_upstream but prints ready-to-paste stub tuples.
    """
    _print_stubs(_find_missing(_from_upstream_csv(filepath)))


_WATCH_PATTERNS = ["Frappe Books", "frappe-books", "frappe books"]


def _source_watch_hits() -> list:
    hits = []
    for d in _ALL_TS_DIRS:
        p = _REPO / d
        if not p.exists():
            continue
        for f in p.rglob("*"):
            if any(part in _SKIP for part in f.parts):
                continue
            if f.suffix not in (".ts", ".vue"):
                continue
            if any(str(f).endswith(s) for s in _SKIP_SUFFIXES):
                continue
            try:
                text = f.read_text(encoding="utf-8")
            except Exception:
                continue
            for pattern in _WATCH_PATTERNS:
                if pattern in text:
                    for i, line in enumerate(text.splitlines(), 1):
                        if pattern in line:
                            hits.append(f"{f.relative_to(_REPO)}:{i}: {line.strip()}")
    return hits


def cmd_check_upstream(filepath: str):
    """
    Diff upstream CSV source column against our STRINGS.
    Works with ANY upstream language CSV — only col 0 (English source) is read.
    Also scans source files for strings that need attention after a merge.
    """
    _print_check(_find_missing(_from_upstream_csv(filepath)))
    hits = _source_watch_hits()
    if hits:
        print(f"\n{len(hits)} string(s) in source files need attention:\n")
        for h in hits:
            print(f"  {h}")


# ── entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys as _sys

    argv = _sys.argv[1:]

    if not argv:
        cmd_build()
    elif argv[0] == "--check":
        cmd_check()
    elif argv[0] == "--stub":
        cmd_stub()
    elif argv[0] == "--check-upstream":
        if len(argv) < 2:
            print("Error: --check-upstream requires a CSV file path.")
            _sys.exit(1)
        cmd_check_upstream(argv[1])
    elif argv[0] == "--stub-upstream":
        if len(argv) < 2:
            print("Error: --stub-upstream requires a CSV file path.")
            _sys.exit(1)
        cmd_stub_upstream(argv[1])
    else:
        print("See README.md — Translations section.")
        _sys.exit(1)
