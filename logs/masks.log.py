import logging

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("logs/masks.log", mode='w', encoding="utf-8")
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_mask_card_number(card_number: str) -> str:
    logger.info(f"Вызвана get_mask_card_number с номером {card_number}")
    try:
        if not card_number:
            logger.error("Передан пустой номер карты")
            return ""
        if len(card_number) < 16:
            logger.error(f"Номер карты слишком короткий: {len(card_number)} цифр (нужно 16)")
            return card_number
        masked = card_number[:4] + "******" + card_number[-4:]
        logger.info(f"Успешно замаскирован номер карты: {masked}")
        return masked
    except Exception as e:
        logger.error(f"Непредвиденная ошибка в get_mask_card_number: {e}", exc_info=True)
        return ""


def get_mask_account(account_number: str) -> str:
    """Маскирует номер счёта: две звёздочки и последние 4 цифры"""
    logger.info(f"Вызвана get_mask_account с номером {account_number}")
    try:
        if not account_number:
            logger.error("Передан пустой номер счёта")
            return ""
        if len(account_number) < 4:
            logger.error(f"Номер счёта слишком короткий: {len(account_number)} цифр (нужно минимум 4)")
            return account_number
        masked = "**" + account_number[-4:]
        logger.info(f"Успешно замаскирован номер счёта: {masked}")
        return masked
    except Exception as e:
        logger.error(f"Непредвиденная ошибка в get_mask_account: {e}", exc_info=True)
        return ""
