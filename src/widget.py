def mask_account_card(card_or_account_info: str) -> str:
    """Принимает строку с типом и номером карты/счета, возвращает замаскированный номер"""
    if not card_or_account_info:
        return ""
    parts = card_or_account_info.split()

    if len(parts) == 1:
        return card_or_account_info
    number = parts[-1]
    name = " ".join(parts[:-1])
    if "Счет" in name or "счет" in name:
        if len(number) >= 4:
            masked_number = "**" + number[-4:]
        else:
            masked_number = "**" + number
    else:
        if len(number) >= 16:
            masked_number = number[:4] + "******" + number[-4:]
        else:
            masked_number = number
    return f"{name} {masked_number}"


def get_date(date_string: str) -> str:
    """Преобразует строку с датой из формата ISO в формат ДД.ММ.ГГГГ"""
    if not date_string:
        return ""
    try:
        if "T" in date_string:
            date_part = date_string.split("T")[0]
        elif " " in date_string:
            date_part = date_string.split(" ")[0]
        else:
            date_part = date_string

        parts = date_part.split("-")
        if len(parts) != 3:
            return date_string
        year, month, day = parts
        return f"{day}.{month}.{year}"
    except ValueError, AttributeError, IndexError:
        return date_string
