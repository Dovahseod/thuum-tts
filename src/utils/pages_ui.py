import typing

import discord


def pages_factory(
        rows: list,
        nrows_per_page: int,
        color: int | discord.Colour | None = None,
        title: typing.Optional[str] = None,
        title_row: typing.Optional[str] = None
        ) -> tuple[discord.Embed, discord.ui.View]:
    pages = []
    for i in range((len(rows)/nrows_per_page).__ceil__()):
        range_start = i*nrows_per_page
        range_stop = min(len(rows), i*nrows_per_page+nrows_per_page)
        pages.append(rows[range_start:range_stop])
    page_control_ui = PagesUI(pages, color, title, title_row)
    return page_control_ui.display_page(), page_control_ui


class PagesUI(discord.ui.View):
    def __init__(
            self,
            pages: list[list[str]],
            color: int | discord.Colour | None = None,
            title: typing.Optional[str] = None,
            title_row: typing.Optional[str] = None):
        super().__init__(timeout=None)
        self.pages = pages
        self.color = color
        self.title = title
        self.title_row = title_row
        self.current_page = 1
        self.npages = len(pages)

    def display_page(self, page: typing.Optional[int] = None) -> discord.Embed:
        if page is None:
            page = self.current_page
        page_rows = self.pages[page-1]
        embed = discord.Embed(color=self.color, title=self.title)
        if self.title_row is not None:
            embed.add_field(name="", value=self.title_row, inline=False)
        for row in page_rows:
            embed.add_field(name="", value=row, inline=False)
        embed.set_footer(text=f"Page {page}/{self.npages}")
        return embed
        
    async def first_page(self, interaction: discord.Interaction) -> None:
        self.current_page = 1
        self.clear_items()
        self.add_item(PagesUIButton_First(disabled=True))
        self.add_item(PagesUIButton_Previous(disabled=True))
        self.add_item(PagesUIButton_Next())
        self.add_item(PagesUIButton_Final())
        await interaction.response.edit_message(embed=self.display_page(), view=self)
        
    async def previous_page(self, interaction: discord.Interaction) -> None:
        self.current_page -= 1
        self.clear_items()
        if self.current_page == 1:
            self.add_item(PagesUIButton_First(disabled=True))
            self.add_item(PagesUIButton_Previous(disabled=True))
        else:
            self.add_item(PagesUIButton_First())
            self.add_item(PagesUIButton_Previous())
        self.add_item(PagesUIButton_Next())
        self.add_item(PagesUIButton_Final())
        await interaction.response.edit_message(embed=self.display_page(), view=self)

    async def next_page(self, interaction: discord.Interaction) -> None:
        self.current_page += 1
        self.clear_items()
        self.add_item(PagesUIButton_First())
        self.add_item(PagesUIButton_Previous())
        if self.current_page == self.npages:
            self.add_item(PagesUIButton_Next(disabled=True))
            self.add_item(PagesUIButton_Final(disabled=True))
        else:
            self.add_item(PagesUIButton_Next())
            self.add_item(PagesUIButton_Final())
        await interaction.response.edit_message(embed=self.display_page(), view=self)
        
    async def final_page(self, interaction: discord.Interaction) -> None:
        self.current_page = self.npages
        self.clear_items()
        self.add_item(PagesUIButton_First())
        self.add_item(PagesUIButton_Previous())
        self.add_item(PagesUIButton_Next(disabled=True))
        self.add_item(PagesUIButton_Final(disabled=True))
        await interaction.response.edit_message(embed=self.display_page(), view=self)


class PagesUIButton_First(discord.ui.Button):
    def __init__(self, *, disabled: bool = False):
        super().__init__(label='<<', disabled=disabled, custom_id='pagesui:first')

    async def callback(self, interaction: discord.Interaction):
        view = typing.cast(PagesUI, self.view)
        await view.first_page(interaction)


class PagesUIButton_Previous(discord.ui.Button):
    def __init__(self, *, disabled: bool = False):
        super().__init__(label='<', disabled=disabled, custom_id='pagesui:previous')

    async def callback(self, interaction: discord.Interaction):
        view = typing.cast(PagesUI, self.view)
        await view.previous_page(interaction)


class PagesUIButton_Next(discord.ui.Button):
    def __init__(self, *, disabled: bool = False):
        super().__init__(label='>', disabled=disabled, custom_id='pagesui:next')

    async def callback(self, interaction: discord.Interaction):
        view = typing.cast(PagesUI, self.view)
        await view.next_page(interaction)


class PagesUIButton_Final(discord.ui.Button):
    def __init__(self, *, disabled: bool = False):
        super().__init__(label='>>', disabled=disabled, custom_id='pagesui:final')

    async def callback(self, interaction: discord.Interaction):
        view = typing.cast(PagesUI, self.view)
        await view.final_page(interaction)
