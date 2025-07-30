import logging
import re
from asyncio import run
from enum import StrEnum
from playwright.async_api import async_playwright, Page, Locator, Position  # , FloatRect
from pyotp import TOTP
from playwright._impl._errors import TimeoutError
from pyro_client.client.user import UserClient
from pyro_client.loader import API_ID, API_HASH
from xync_schema.enums import UserStatus
from xync_schema.models import User, PmAgent

from xync_client.loader import TOKEN


class CaptchaException(Exception): ...


class OtpNotSetException(Exception): ...


class NoCodeException(Exception): ...


class NoMailException(Exception): ...


class Pages(StrEnum):
    base_url = "https://account.volet.com/"
    LOGIN = base_url + "login"
    OTP = base_url + "login/otp"
    HOME = base_url + "pages/transaction"
    SEND = base_url + "pages/transfer/wallet"
    GMH = "https://mail.google.com/mail/u/0/"


def parse_transaction_info(text: str) -> dict[str, str] | None:
    # Поиск ID транзакции
    transaction_id_match = re.search(r"Transaction ID:\s*([\w-]+)", text)
    # Поиск суммы и валюты
    amount_match = re.search(r"Amount:\s*([+-]?[0-9]*\.?[0-9]+)\s*([A-Z]+)", text)
    # Поиск email отправителя
    sender_email_match = re.search(r"Sender:\s*([\w.-]+@[\w.-]+)", text)

    if transaction_id_match and amount_match and sender_email_match:
        return {
            "transaction_id": transaction_id_match.group(1),
            "amount": amount_match.group(1),
            "currency": amount_match.group(2),
            "sender_email": sender_email_match.group(1),
        }
    return None


class Client:
    agent: PmAgent
    bot: UserClient
    page: Page
    gpage: Page

    def __init__(self, uid: int):
        self.bot = UserClient(str(uid), API_ID, API_HASH, TOKEN)

    async def start(self, headed: bool = False):
        await self.bot.start()
        self.agent = await PmAgent.get(
            user__username_id=self.bot.me.id, user__status__gt=0, pm__norm="volet"
        ).prefetch_related("user")

        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(
            channel="chrome",
            headless=not headed,
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
        context = await browser.new_context(storage_state=self.agent.auth.get("state", {}), locale="en")
        context.set_default_navigation_timeout(15000)
        context.set_default_timeout(12000)
        self.page = await context.new_page()

        await self.gmail_page()
        await self.go(Pages.HOME)
        if self.page.url == Pages.LOGIN:
            await self.login()
        if self.page.url != Pages.HOME:
            await self.bot.receive("Not logged in!", photo=await self.page.screenshot())
            raise Exception(f"User {self.agent.user_id} has not logged in")

    async def login(self):
        await self.page.locator("input#j_username").fill("mixartemev@gmail.com")
        await self.page.locator("input#j_password").fill("mixfixX98")
        await self.page.locator("input#loginToAdvcashButton", has_text="log in").hover()
        await self.page.locator("input#loginToAdvcashButton:not([disabled])", has_text="log in").click()
        if not (code := await self.bot.wait_from(243630567, "otp_login")):
            await self.bot.receive("no login code", photo=await self.page.screenshot())
            raise NoCodeException(self.agent.user_id)
        await self.page.locator("input#otpId").fill(code)
        await self.page.click("input#checkOtpButton")
        await self.page.wait_for_url(Pages.HOME)

    async def send(self, dest: str, amount: float):
        await self.go(Pages.SEND)
        await self.page.click("[class=combobox-account]")
        await self.page.click('[class=rf-ulst-itm] b:has-text("Ruble ")')
        await self.page.wait_for_timeout(200)
        await self.page.fill("#srcAmount", str(amount))
        await self.page.fill("#destWalletId", dest)
        await self.page.wait_for_timeout(300)
        await self.page.locator("form#mainForm input[type=submit]", has_text="continue").click()
        if otp := self.agent.auth.get("otp"):
            totp = TOTP(otp)
            code = totp.now()
        elif self.agent.auth.get("sess"):
            if not (code := await self.bot.wait_from(243630567, "otp_send")):
                if 1:  # todo: need main confirm
                    await self.mail_confirm()
                await self.bot.receive("no send trans code", photo=await self.page.screenshot())
                raise NoCodeException(self.agent.user_id)
        else:
            raise OtpNotSetException(self.agent.user_id)
        await self.page.fill("#securityValue", code)
        await self.page.locator("input[type=submit]", has_text="confirm").click()
        await self.page.wait_for_url(Pages.SEND)
        await self.page.get_by_role("heading").click()
        slip = await self.page.screenshot(clip={"x": 440, "y": 205, "width": 420, "height": 360})
        await self.bot.receive(f"{amount} to {dest} sent", photo=slip)

    async def gmail_page(self):
        gp = await self.page.context.new_page()
        await gp.goto(Pages.GMH, timeout=30000)
        if not gp.url.startswith(Pages.GMH):
            if await (  # ваще с 0 заходим
                sgn_btn := gp.locator(
                    'header a[href^="https://accounts.google.com/AccountChooser/signinchooser"]:visible',
                    has_text="sign",
                )
            ).count():
                await sgn_btn.click()
            if gp.url.startswith("https://accounts.google.com/v3/signin/accountchooser"):  # если надо выбрать акк
                await gp.locator("li").first.click()
            # если предлагает залогиниться
            elif await gp.locator("h1#headingText", has_text="Sign In").count():
                await gp.fill("input[type=email]", self.agent.user.gmail_auth["login"])
                await gp.locator("button", has_text="Next").click()
            # осталось ввести пороль:
            await gp.fill("input[type=password]", self.agent.user.gmail_auth["password"])
            await gp.locator("#passwordNext").click()
            await self.bot.receive("Аппрувни гмейл, у тебя 1.5 минуты", photo=await gp.screenshot())  # todo: refact: mv
        await gp.wait_for_url(lambda u: u.startswith(Pages.GMH), timeout=90 * 1000)  # убеждаемся что мы в почте
        self.gpage = gp

    async def mail_confirm(self):
        lang = await self.gpage.get_attribute("html", "lang")
        labs = {
            "ru": "Оповещения",
            "en-US": "Updates",
        }
        tab = self.gpage.get_by_role("heading").get_by_label(labs[lang]).last
        await tab.click()
        rows = self.gpage.locator("tbody>>nth=4 >> tr")
        row = rows.get_by_text("Volet.com").and_(rows.get_by_text("Please Confirm Withdrawal"))
        if not await row.count():
            await self.bot.receive("А нет запросов от волета", photo=await self.gpage.screenshot())

        await row.click()
        await self.gpage.wait_for_load_state()
        btn = self.gpage.locator('a[href^="https://account.volet.com/verify/"]', has_text="confirm").first
        await btn.click()

    async def go(self, url: Pages):
        try:
            await self.page.goto(url)
            if len(await self.page.content()) < 1000:  # todo: fix captcha symptom
                await self.captcha_click()
        except Exception as e:
            await self.bot.receive(repr(e), photo=await self.page.screenshot())
            raise e

    async def send_cap_help(self, xcap: Locator):
        bb = await xcap.bounding_box(timeout=2000)
        byts = await self.page.screenshot(clip=bb)
        await self.bot.receive("put x, y", photo=byts)
        return await self.bot.bot.wait_from(self.bot.me.id, "xy", timeout=59)

    async def captcha_click(self):
        captcha_url = self.page.url
        cbx = self.page.frame_locator("#main-iframe").frame_locator("iframe").first.locator("div#checkbox")
        await cbx.wait_for(state="visible"), await self.page.wait_for_timeout(500)
        await cbx.click(delay=94)
        xcap = self.page.frame_locator("#main-iframe").frame_locator("iframe").last.locator("div.challenge-view")
        if await xcap.count():
            xy = await self.send_cap_help(xcap)
            x, y = xy.split(",")
            await xcap.click(position=Position(x=int(x), y=int(y)))
        try:
            await self.page.wait_for_url(lambda url: url != captcha_url)
        except TimeoutError:  # if page no changed -> captcha is undone
            await self.page.screenshot()
            raise CaptchaException(self.page.url)

    async def wait_for_payments(self, interval: int = 29):
        while (await User[self.agent.user_id]).status > UserStatus.SLEEP:
            await self.page.reload()
            await self.page.wait_for_timeout(interval * 1000)

    async def stop(self):
        # save state
        if state := await self.page.context.storage_state():
            self.agent.auth["state"] = state
            await self.agent.save()
        # closing
        await self.bot.stop()
        await self.page.context.close()
        await self.page.context.browser.close()


async def _test():
    from x_model import init_db
    from xync_client.loader import PG_DSN
    from xync_schema import models

    _ = await init_db(PG_DSN, models, True)
    logging.basicConfig(level=logging.DEBUG)
    uid = 193017646
    va = Client(uid)
    try:
        await va.start(True)
        await va.send("alena.artemeva25@gmail.com", 8.3456)
        await va.wait_for_payments()
    except TimeoutError as te:
        await va.bot.receive(repr(te), photo=await va.page.screenshot())
        raise te
    finally:
        await va.stop()


if __name__ == "__main__":
    run(_test())
