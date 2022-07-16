import discord
from discord.ext import commands
from core.roles import ROLES
from main import guilds


class ColorRoles(commands.Cog):
    """
    Setup Color Embeds

    9 Embeds and 9 Cover Images
    9 Colors Each
    """

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def colorroles(self, ctx):

        cover_images = ROLES.cover_images
        colors = ROLES.colors

        await self.init(ctx)

        for i, color in enumerate(colors):
            embed = discord.Embed(
                color=int(list(colors[color][0].keys())[0], 16))
            embed.set_image(url=cover_images[i][color])
            await ctx.send(embed=embed)

            embed = discord.Embed(
                color=int(list(colors[color][0].keys())[0], 16))
            desc = ""

            for i in range(len(colors[color])):
                role = discord.utils.get(
                    ctx.guild.roles, name=ROLES.names[color], color=discord.Color(int(list(colors[color][i].keys())[0], 16)))
                desc += f"{role.mention} ・ƸӜƷ・{i + 1}\n"
            embed.description = desc
            embed.set_footer(text=f"{color}")
            msg = await ctx.send(embed=embed)
            for i in range(len(colors[color])):
                emote = discord.utils.get(
                    ctx.guild.emojis, name=ROLES.numbers_names[i])
                await msg.add_reaction(emote)
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.client.user.id:
            return
        if payload.message_id and payload.emoji.name in ROLES.numbers_names:
            msg = await self.client.get_channel(payload.channel_id).fetch_message(payload.message_id)
            guild = msg.guild
            if msg.embeds[0].footer.text:
                color = msg.embeds[0].footer.text
                if color in ROLES.colors and payload.event_type == "REACTION_ADD":
                    # remove old color of user
                    member = guild.get_member(payload.user_id)
                    for role in member.roles:
                        if role.name in ROLES.names.values():
                            await member.remove_roles(role)
                    role = discord.utils.get(
                        guild.roles, name=ROLES.names[color], color=discord.Color(int(list(ROLES.colors[color][ROLES.numbers_names.index(payload.emoji.name)].keys())[0], 16)))
                    await member.add_roles(role)
                    await msg.remove_reaction(
                        payload.emoji, member)


    async def init(self, ctx):

        for i, number in enumerate(ROLES.numbers):
                emote = discord.utils.get(
                    ctx.guild.emojis, name=ROLES.numbers_names[i])
                if not emote:
                    with open(number, "rb") as f:
                        await ctx.guild.create_custom_emoji(
                            name=ROLES.numbers_names[i], image=f.read())
                else:
                    pass
        for color in ROLES.colors:
            for i in range(len(ROLES.colors[color])):
                print(int(list(ROLES.colors[color][i].keys())[0], 16))
                role = discord.utils.get(
                    ctx.guild.roles, name=ROLES.names[color], color=discord.Color(int(list(ROLES.colors[color][i].keys())[0], 16)))
                if not role:
                    role = await ctx.guild.create_role(name=ROLES.names[color], color=int(list(ROLES.colors[color][i].keys())[0], 16))
                else:
                    pass
        for color in ROLES.colors:
            for i in range(len(ROLES.colors[color])):
                bot_role_pos = discord.utils.get(ctx.guild.roles, name=self.client.user.name).position
                print(bot_role_pos + 1)
                await role.edit(position=bot_role_pos - 1)

    @commands.command()
    @commands.is_owner()
    async def deinit(self, ctx):
        colors = ROLES.colors
        for color in colors:
            for i in range(len(colors[color])):
                try:
                    role = discord.utils.get(
                        ctx.guild.roles, name=ROLES.names[color])
                    if role:
                        print(role)
                        await role.delete()
                except discord.errors.NotFound:
                    pass
        for i, _ in enumerate(ROLES.numbers):
                emote = discord.utils.get(
                    ctx.guild.emojis, name=ROLES.numbers_names[i])
                if emote:
                    await emote.delete()
    
    @commands.slash_command(guild_ids=guilds, name="removecolor")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def remove_color_roles(self, ctx):
        member = ctx.author
        for role in member.roles:
            if role.name in ROLES.names.values():
                await member.remove_roles(role)
        await ctx.respond(f"Removed all color roles from {member.mention}")

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.respond(f"You are on cooldown for {round(error.retry_after)} seconds")
        else:
            raise error

def setup(client):
    client.add_cog(ColorRoles(client))
