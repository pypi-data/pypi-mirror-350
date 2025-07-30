import asyncio

from playwright.async_api import async_playwright
from playwright._impl._errors import TimeoutError, Error


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(storage_state="state.json", record_video_dir="videos")
        page = await context.new_page()
        await page.goto("https://www.tbank.ru/mybank/")
        await page.wait_for_timeout(1000)
        try:
            await page.wait_for_url("https://www.tbank.ru/mybank/", timeout=3000)
        except TimeoutError:
            # Новый пользователь
            if await page.locator('[automation-id="form-title"]', has_text="Вход в Т‑Банк").is_visible():
                await page.wait_for_timeout(200)
                await page.locator('[automation-id="phone-input"]').fill("9992259898")
                await page.locator('[automation-id="button-submit"] svg').click()
            # Известный пользователь
            else:
                await page.locator('[automation-id="button-submit"]').click()
                await page.wait_for_timeout(100)
            await page.locator('[automation-id="otp-input"]').fill(input("Введите код"))
            await page.wait_for_timeout(1000)
            if await page.locator('[automation-id="cancel-button"]').is_visible():
                await page.wait_for_timeout(3000)
                await page.locator('[automation-id="cancel-button"]', has_text="Не сейчас").click(delay=500)
            elif await page.locator('[automation-id="password-input"]').is_visible():
                await page.locator('[automation-id="password-input"]').fill("mixfix98")
                await page.locator('[automation-id="button-submit"] svg').click()
            await page.context.storage_state(path="state.json")
            await page.wait_for_timeout(200)

        # Переходим на сбп и вводим данные получателя
        # await page.locator(
        #     '[data-qa-type="desktop-ib-pay-buttons"] [data-qa-type="atomPanel pay-card-0"]',
        #     has_text="Перевести по телефону",
        # ).click()
        # await page.locator('[data-qa-type="recipient-input.value.placeholder"]').click()
        # await page.wait_for_timeout(300)
        # await page.locator('[data-qa-type="recipient-input.value.input"]').fill("9992259898")
        # await page.locator('[data-qa-type="amount-from.placeholder"]').click()
        # await page.locator('[data-qa-type="amount-from.input"]').fill("100")
        # await page.wait_for_timeout(300)
        # await page.locator('[data-qa-type="bank-plate-other-bank click-area"]').click()
        # await page.locator('[data-qa-type*="inputAutocomplete.value.input"]').click()
        # await page.locator('[data-qa-type*="inputAutocomplete.value.input"]').fill("Озон")
        # await page.wait_for_timeout(300)
        # await page.locator('[data-qa-type="banks-popup-list"]').click()
        # await page.locator('[data-qa-type="transfer-button"]').click()

        # Проверка последнего платежа
        try:
            await page.goto("https://www.tbank.ru/events/feed")
        except Error:
            await page.wait_for_timeout(1000)
            await page.goto("https://www.tbank.ru/events/feed")
        await page.wait_for_timeout(2000)
        await page.locator('[data-qa-type = "timeline-operations-list"]:last-child').scroll_into_view_if_needed()
        transactions = await page.locator(
            '[data-qa-type="timeline-operations-list"] [data-qa-type="operation-money"]'
        ).all_text_contents()
        result = recursion_payments(100, transactions)
        if result == 100:
            print("Платеж", result, "получен")
        else:
            print("Ничегошеньки нет")
        await page.wait_for_timeout(3000)
        await context.close()
        await page.video.path()
        # BufferedInputFile(pth, 'tbank')
        # await bot.send_video('mixartemev')
        ...
    await browser.close()


def recursion_payments(amount: int, transactions: list):
    tran = transactions.pop(0)
    normalized_tran = tran.replace("−", "-").replace(",", ".")
    if 0 > int(float(normalized_tran)) != amount:
        return recursion_payments(amount, transactions)
    return int(float(tran.replace("−", "-").replace(",", ".")))


asyncio.run(main())
