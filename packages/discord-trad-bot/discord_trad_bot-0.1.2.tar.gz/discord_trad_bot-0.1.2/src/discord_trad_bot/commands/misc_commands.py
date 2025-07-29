import discord
from discord.ext import commands

class CustomHelpCommand(commands.HelpCommand):
    def is_admin_command(self, command):
        # Check if the command requires administrator permissions
        for check in command.checks:
            if hasattr(check, '__qualname__') and 'has_permissions' in check.__qualname__:
                closure = getattr(check, '__closure__', None)
                if closure:
                    for cell in closure:
                        if isinstance(cell.cell_contents, dict) and cell.cell_contents.get('administrator', False):
                            return True
        return False

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Translation Bot Help", color=discord.Color.blue())
        user_commands = []
        admin_commands = []
        for cmd in self.get_bot_mapping()[None]:
            if not cmd.hidden:
                if self.is_admin_command(cmd):
                    admin_commands.append(f"`!{cmd.name}` - {cmd.short_doc}")
                else:
                    user_commands.append(f"`!{cmd.name}` - {cmd.short_doc}")
        embed.add_field(name="User Commands", value="\n".join(user_commands) or "No user commands available", inline=False)
        if admin_commands:
            embed.add_field(name="Admin Commands", value="\n".join(admin_commands), inline=False)
        embed.add_field(
            name="Additional Information",
            value="• Use `!languages` to see all supported language codes\n"
                  "• Translation is automatic in designated channels\n"
                  "• Admin commands require administrator permissions",
            inline=False
        )
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(
            title=f"Command: !{command.name}",
            description=command.help or "No description available",
            color=discord.Color.blue()
        )
        if command.usage:
            embed.add_field(name="Usage", value=f"`!{command.name} {command.usage}`", inline=False)
        await self.get_destination().send(embed=embed)

def setup(bot):
    bot.help_command = CustomHelpCommand() 