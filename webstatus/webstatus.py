from redbot.core import commands
import aiohttp
from bs4 import BeautifulSoup

BaseCog = getattr(commands, "Cog", object)

class Webstatus(BaseCog):
    """Cog for seeing if something is down"""

    def __init__(self, bot):
        self.bot = bot

    async def fetch(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    @commands.command()
    async def webstatus(self, ctx, *, company):
        async with aiohttp.ClientSession() as session:
            try:
                url = "https://outage.report/" + company.replace(' ', '').lower()
                webpage = self.fetch(session, url)
            except:
                await ctx.send(f"An error occured while fetching the status.  Server responded with status code {webpage.status_code}")
                return
            else:
                tree = BeautifulSoup(webpage)
                webpage = tree.prettify()
                soup = BeautifulSoup(webpage, 'html.parser')
                results = soup.find_all('div', attrs={'class': 'Alert__Div-s1eb33n4-0 cvbpXY'})
                if len(results) == 0:
                    await ctx.send("https://outage.report has not reported any problems.")
                else:
                    await ctx.send(results[1].string)
                    return