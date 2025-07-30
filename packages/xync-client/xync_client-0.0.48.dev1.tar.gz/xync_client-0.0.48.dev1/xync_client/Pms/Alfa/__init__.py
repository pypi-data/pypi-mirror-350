import asyncio

from playwright.async_api import async_playwright
from playwright._impl._errors import TimeoutError


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            channel="chrome",
            headless=False,
            timeout=5000,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-web-security",
                "--disable-infobars",
                "--disable-extensions",
                "--start-maximized",
            ],
        )
        context = await browser.new_context(storage_state="state.json")
        page = await context.new_page()
        await page.goto("https://web.alfabank.ru/dashboard")
        await page.wait_for_timeout(1000)
        try:
            await page.wait_for_url("https://web.alfabank.ru/dashboard")
            await page.wait_for_timeout(1000)
        # Новый пользователь
        except TimeoutError:
            await page.locator('[data-test-id="phoneInput-form-control-inner"] [data-test-id="phoneInput"]').fill(
                "79680252000"
            )
            await page.wait_for_timeout(1000)
            await page.locator("span", has_text="Вперёд").click(delay=500)
            await page.locator('[data-test-id="card-account-input"]').fill("2200150913416522")
            await page.locator('[data-test-id="card-account-continue-button"]').click()
            await page.locator(
                '[class*=confirmation__component] [class*=code-input] [autocomplete="one-time-code"]'
            ).fill(input("Введите код"))
            await page.wait_for_timeout(500)
            if await page.locator('[data-test-id="trust-device-page-submit-btn"]').is_visible():
                await page.locator('[data-test-id="trust-device-page-submit-btn"]').click()
                await page.locator('[data-test-id="new-password"]').click()
                await page.locator('[data-test-id="new-password"]').fill("0909")
                await page.locator('[data-test-id="new-password-again"]').click()
                await page.locator('[data-test-id="new-password-again"]').fill("0909")
                await page.locator('[data-test-id="submit-button"]').click()
            await page.context.storage_state(path="state.json")

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
        # try:
        #     await page.goto("https://www.tbank.ru/events/feed")
        # except Error:
        #     await page.wait_for_timeout(1000)
        #     await page.goto("https://www.tbank.ru/events/feed")
        # await page.wait_for_timeout(2000)
        # await page.locator('[data-qa-type = "timeline-operations-list"]:last-child').scroll_into_view_if_needed()
        # transactions = await page.locator(
        #     '[data-qa-type="timeline-operations-list"] [data-qa-type="operation-money"]'
        # ).all_text_contents()
        # result = recursion_payments(100, transactions)
        # if result == 100:
        #     print("Платеж", result, "получен")
        # else:
        #     print("Ничегошеньки нет")
        # await page.wait_for_timeout(3000)
        await context.close()
        # await page.video.path()
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
