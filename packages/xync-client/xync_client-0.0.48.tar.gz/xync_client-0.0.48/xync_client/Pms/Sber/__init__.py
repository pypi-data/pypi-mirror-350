import asyncio
import os
from playwright.async_api import async_playwright
from playwright._impl._errors import TimeoutError


async def main():
    from x_model import init_db
    from xync_schema import models
    from xync_client.loader import PG_DSN

    _ = await init_db(PG_DSN, models, True)
    agent = await models.PmAgent.filter(pm__norm="sber", auth__isnull=False).first()

    async with async_playwright() as p:
        storage_state = "state.json" if os.path.exists("state.json") else None
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(storage_state=storage_state, record_video_dir="videos")
        page = await context.new_page()

        await page.goto("https://online.sberbank.ru/CSAFront/index.do")
        try:
            await page.wait_for_url("https://online.sberbank.ru/CSAFront/index.do", timeout=3000)
        except TimeoutError:
            if card := agent.auth.get("card"):
                await page.locator('button[aria-controls="tabpanel-card"]').is_visible()
                await page.locator('button[aria-controls="tabpanel-card"]').click()
                await page.wait_for_selector('input[placeholder="Введите номер карты"]', timeout=10000)
                await page.locator('input[placeholder="Введите номер карты"]').fill(card)
                await page.locator('button[type="submit"]').click()

                sms_code = input("Введите код из SMS: ")
                for i in range(5):
                    await page.locator(f'input[name="confirmPassword-{i}"]').fill(sms_code[i])

                password = input("Введите 5-значный код: ")
                await page.wait_for_selector(".FWAhBZHPePsATLTVFeTT", timeout=10000)
                otp_fields = page.locator('[class="BjsSl7Uv2es5tUtwB03r"]')
                for i in range(await otp_fields.count() + 1):
                    await page.keyboard.press(password[i])

                await page.wait_for_timeout(1000)

                await page.wait_for_selector(".Re_Wg4Drqw9QjVM43vJ_", timeout=10000)
                fields = page.locator('[class="BjsSl7Uv2es5tUtwB03r"]')
                for i in range(await fields.count() + 1):
                    await page.keyboard.press(password[i])
                await page.wait_for_timeout(100000)
            elif login := agent.auth.get("login"):
                await page.locator('input[autocomplete="login"]').fill(login)
                password = input("Введите пароль: ")
                await page.locator('input[autocomplete="password"]').fill(password)
                await page.locator('button[data-testid="button-continue"]').click()
                sms_code = input("Введите код из SMS: ")
                for i in range(5):
                    await page.locator(f'input[name="confirmPassword-{i}"]').fill(sms_code[i])

                password = input("Введите 5-значный код: ")
                await page.wait_for_selector(".FWAhBZHPePsATLTVFeTT", timeout=10000)
                otp_fields = page.locator('[class="BjsSl7Uv2es5tUtwB03r"]')
                for i in range(await otp_fields.count() + 1):
                    await page.keyboard.press(password[i])

                await page.wait_for_timeout(1000)

                await page.wait_for_selector(".Re_Wg4Drqw9QjVM43vJ_", timeout=10000)
                fields = page.locator('[class="BjsSl7Uv2es5tUtwB03r"]')
                for i in range(await fields.count() + 1):
                    await page.keyboard.press(password[i])

                await page.wait_for_timeout(100000)
            await context.storage_state(path="state.json")

        await context.close()
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
