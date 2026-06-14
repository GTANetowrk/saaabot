import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import os
from datetime import datetime
from discord.ext import commands
from discord import app_commands
import asyncio
from datetime import datetime

# ============================================================
#   SAAA — TICKET BOT
#   Sistema de tickets para el servidor de Discord
# ============================================================

TOKEN    = os.environ["TOKEN"]
GUILD_ID = int(os.environ["GUILD_ID"])
TICKET_CAT   = "SAAA — Support Tickets"  # Categoría donde se crean los tickets
LOG_CHANNEL  = "📋│ticket-logs"          # Canal de logs
STAFF_ROLE   = "✈️ Administrator | SAAA" # Rol que puede ver todos los tickets

# ── Colores por tipo de ticket ─────────────────────────────
TICKET_TYPES = {
    "pilot_cert": {
        "label":       "🎖️  Pilot Certificate",
        "description": "Request, renew or query a pilot certificate (SPL, PPL, CPL, ATP)",
        "color":       0x2E8FD4,
        "emoji":       "🎖️",
        "fields": [
            ("Full Name",          "Your full in-game name"),
            ("Certificate Type",   "Student / Private / Commercial / ATP"),
            ("Current Hours",      "Total flight hours logged"),
            ("Additional Info",    "Any extra details or documents"),
        ]
    },
    "aircraft_reg": {
        "label":       "✈️  Aircraft Registry",
        "description": "Register a new aircraft or update existing registration",
        "color":       0x27AE60,
        "emoji":       "✈️",
        "fields": [
            ("Full Name",          "Owner's full in-game name"),
            ("Aircraft Type",      "Make and model (e.g. Cessna 172, Boeing 737)"),
            ("Registration N#",    "Requested tail number (e.g. N-SA1042)"),
            ("Base of Operations", "Primary airport (e.g. KLSIA)"),
        ]
    },
    "flight_plan": {
        "label":       "📡  Flight Plan",
        "description": "Submit an IFR or VFR flight plan for approval",
        "color":       0x8E44AD,
        "emoji":       "📡",
        "fields": [
            ("Pilot Name",         "PIC full in-game name"),
            ("Departure / Arrival","E.g. KLSIA → KSBA"),
            ("Aircraft N#",        "Registered tail number"),
            ("Route & Altitude",   "Planned route and cruising altitude"),
            ("ETD / ETA",          "Estimated departure and arrival times"),
            ("Flight Rules",       "IFR or VFR"),
        ]
    },
    "incident_report": {
        "label":       "🚨  Incident Report",
        "description": "Report an aviation incident or safety violation (mandatory)",
        "color":       0xC0392B,
        "emoji":       "🚨",
        "fields": [
            ("Your Name",          "Full in-game name"),
            ("Date & Time",        "When the incident occurred"),
            ("Location",           "Airport / airspace where it happened"),
            ("Description",        "Full description of what happened"),
            ("Aircraft Involved",  "N# or aircraft type(s) involved"),
        ]
    },
    "atc_complaint": {
        "label":       "📢  ATC Complaint / Feedback",
        "description": "Report an ATC issue or submit feedback on air traffic services",
        "color":       0xD4A843,
        "emoji":       "📢",
        "fields": [
            ("Your Name",          "Full in-game name"),
            ("Controller / Facility","ATC unit involved (e.g. KLSIA Tower)"),
            ("Date & Time",        "When the incident occurred"),
            ("Description",        "Describe the issue or feedback in detail"),
        ]
    },
    "job_application": {
        "label":       "💼  Job Application",
        "description": "Apply for a position within the SAAA",
        "color":       0x1A6B3C,
        "emoji":       "💼",
        "fields": [
            ("Full Name",          "Your full in-game name"),
            ("Position Applying",  "E.g. Air Traffic Controller, Aviation Safety Inspector"),
            ("Division",           "ATO / AVS / ARP / Legal / AAT / HR"),
            ("Experience",         "Relevant experience and background"),
            ("Availability",       "Days / times you are available"),
        ]
    },
    "regulation_query": {
        "label":       "⚖️  Regulation Query",
        "description": "Ask a legal or regulatory question to the Policy & Legal office",
        "color":       0xAD1457,
        "emoji":       "⚖️",
        "fields": [
            ("Your Name",          "Full in-game name"),
            ("Topic",              "Subject of your query"),
            ("Question",           "Describe your regulatory question in detail"),
            ("Reference",          "Any regulation or case number you're referencing"),
        ]
    },
    "general_support": {
        "label":       "💬  General Support",
        "description": "Any other question or request not covered above",
        "color":       0x607D8B,
        "emoji":       "💬",
        "fields": [
            ("Your Name",          "Full in-game name"),
            ("Subject",            "Brief summary of your request"),
            ("Description",        "Full details of what you need"),
        ]
    },
}

# ─────────────────────────────────────────────────────────────
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# ── Modal de ticket ────────────────────────────────────────
class TicketModal(discord.ui.Modal):
    def __init__(self, ticket_type: str):
        self.ticket_type = ticket_type
        cfg = TICKET_TYPES[ticket_type]
        super().__init__(title=f"SAAA — {cfg['label']}")

        self.inputs = []
        for i, (label, placeholder) in enumerate(cfg["fields"][:5]):
            inp = discord.ui.TextInput(
                label=label,
                placeholder=placeholder,
                style=discord.TextStyle.paragraph if i >= 3 else discord.TextStyle.short,
                required=i < 3,
                max_length=500
            )
            self.add_item(inp)
            self.inputs.append(inp)

    async def on_submit(self, interaction: discord.Interaction):
        cfg = TICKET_TYPES[self.ticket_type]
        guild = interaction.guild

        # Buscar o crear categoría
        category = discord.utils.get(guild.categories, name=TICKET_CAT)
        if not category:
            category = await guild.create_category(TICKET_CAT)

        # Buscar rol de staff
        staff_role = discord.utils.get(guild.roles, name=STAFF_ROLE)

        # Nombre del canal: ticket-tipo-usuario
        short_type = self.ticket_type.replace("_", "-")
        ch_name = f"🎫│{short_type}-{interaction.user.name[:12].lower()}"

        # Permisos del canal
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user:   discord.PermissionOverwrite(
                view_channel=True, send_messages=True, read_message_history=True
            ),
        }
        if staff_role:
            overwrites[staff_role] = discord.PermissionOverwrite(
                view_channel=True, send_messages=True, read_message_history=True
            )

        channel = await guild.create_text_channel(
            ch_name,
            category=category,
            overwrites=overwrites,
            topic=f"Ticket de {interaction.user} — {cfg['label']} — {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC"
        )

        # ── Embed principal del ticket ──────────────────────
        embed = discord.Embed(
            title=f"{cfg['emoji']}  {cfg['label']}",
            description=(
                f"**Submitted by:** {interaction.user.mention}\n"
                f"**Date:** {discord.utils.format_dt(discord.utils.utcnow(), 'F')}\n"
                f"**Status:** 🟡 Open — Awaiting SAAA Staff"
            ),
            color=cfg["color"],
            timestamp=discord.utils.utcnow()
        )
        embed.set_author(
            name="San Andreas Aviation Administration",
            icon_url="https://r2.fivemanage.com/OunBpxGnvT9qTEdkdPMNj/gtanetpng.png"
        )

        for i, (label, _) in enumerate(cfg["fields"][:len(self.inputs)]):
            val = self.inputs[i].value.strip() or "*Not provided*"
            embed.add_field(name=label, value=val, inline=False)

        embed.set_footer(text=f"SAAA Ticket System · {guild.name}")

        # Botones de gestión
        view = TicketControlView(interaction.user.id)
        msg = await channel.send(
            content=f"||{staff_role.mention if staff_role else '@staff'}||",
            embed=embed,
            view=view
        )
        await msg.pin()

        # Mensaje de bienvenida al usuario
        welcome = discord.Embed(
            description=(
                f"✅ **Ticket created successfully.**\n\n"
                f"Your request has been received by the **SAAA**. "
                f"A staff member will respond shortly.\n\n"
                f"📌 Please do not open duplicate tickets.\n"
                f"🔒 Only you and SAAA staff can see this channel."
            ),
            color=cfg["color"]
        )
        await channel.send(embed=welcome)

        # Log
        log_ch = discord.utils.get(guild.text_channels, name=LOG_CHANNEL.replace("📋│", ""))
        if log_ch:
            log_embed = discord.Embed(
                title="📋 New Ticket Opened",
                description=(
                    f"**User:** {interaction.user.mention} (`{interaction.user}`)\n"
                    f"**Type:** {cfg['label']}\n"
                    f"**Channel:** {channel.mention}\n"
                    f"**Time:** {discord.utils.format_dt(discord.utils.utcnow(), 'f')}"
                ),
                color=cfg["color"]
            )
            await log_ch.send(embed=log_embed)

        await interaction.response.send_message(
            f"✅ Your ticket has been created: {channel.mention}",
            ephemeral=True
        )


# ── Botones de control del ticket ─────────────────────────
class TicketControlView(discord.ui.View):
    def __init__(self, opener_id: int):
        super().__init__(timeout=None)
        self.opener_id = opener_id

    @discord.ui.button(label="✅  Claim Ticket", style=discord.ButtonStyle.secondary, custom_id="claim")
    async def claim(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.label = f"✅  Claimed by {interaction.user.display_name}"
        button.disabled = True
        await interaction.message.edit(view=self)
        await interaction.response.send_message(
            f"📌 Ticket claimed by {interaction.user.mention}.", ephemeral=False
        )

    @discord.ui.button(label="🔒  Close Ticket", style=discord.ButtonStyle.danger, custom_id="close")
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            embed=discord.Embed(
                description="🔒 This ticket will be **closed in 5 seconds**.",
                color=0xC0392B
            )
        )
        await asyncio.sleep(5)
        await interaction.channel.delete()


# ── Selector de tipo de ticket ─────────────────────────────
class TicketTypeSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label=cfg["label"],
                description=cfg["description"][:100],
                value=key,
                emoji=cfg["emoji"]
            )
            for key, cfg in TICKET_TYPES.items()
        ]
        super().__init__(
            placeholder="Select the type of request...",
            options=options,
            min_values=1,
            max_values=1,
        )

    async def callback(self, interaction: discord.Interaction):
        ticket_type = self.values[0]
        modal = TicketModal(ticket_type)
        await interaction.response.send_modal(modal)


class TicketSelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketTypeSelect())


# ── Comando /ticket-panel ──────────────────────────────────
@tree.command(name="ticket-panel", description="[STAFF] Post the SAAA ticket panel in this channel")
@app_commands.checks.has_permissions(administrator=True)
async def ticket_panel(interaction: discord.Interaction):
    embed = discord.Embed(
        title="✈️  SAAA — Contact & Support",
        description=(
            "**Welcome to the San Andreas Aviation Administration support system.**\n\n"
            "Use the menu below to open a ticket. Our staff will respond as soon as possible.\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "🎖️ **Pilot Certificate** — Request or renew a pilot license\n"
            "✈️ **Aircraft Registry** — Register or update your aircraft\n"
            "📡 **Flight Plan** — Submit an IFR or VFR flight plan\n"
            "🚨 **Incident Report** — Report an aviation incident (mandatory)\n"
            "📢 **ATC Complaint** — Report an ATC issue or send feedback\n"
            "💼 **Job Application** — Apply to work for the SAAA\n"
            "⚖️ **Regulation Query** — Legal and regulatory questions\n"
            "💬 **General Support** — Any other request\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "⏱️ *Response times may vary. Do not open duplicate tickets.*"
        ),
        color=0x1B6CA8,
        timestamp=discord.utils.utcnow()
    )
    embed.set_author(
        name="San Andreas Aviation Administration",
        icon_url="https://r2.fivemanage.com/OunBpxGnvT9qTEdkdPMNj/gtanetpng.png"
    )
    embed.set_thumbnail(url="https://r2.fivemanage.com/OunBpxGnvT9qTEdkdPMNj/gtanetpng.png")
    embed.set_footer(text="SAAA Official Support System · gtanetwork.online")

    await interaction.channel.send(embed=embed, view=TicketSelectView())
    await interaction.response.send_message("✅ Panel posted.", ephemeral=True)


# ── Comando /close ─────────────────────────────────────────
@tree.command(name="close", description="Close the current ticket")
async def close_ticket(interaction: discord.Interaction):
    if "│" not in interaction.channel.name and "ticket" not in interaction.channel.name.lower():
        await interaction.response.send_message("❌ This is not a ticket channel.", ephemeral=True)
        return
    await interaction.response.send_message(
        embed=discord.Embed(description="🔒 Closing ticket in 5 seconds...", color=0xC0392B)
    )
    await asyncio.sleep(5)
    await interaction.channel.delete()


# ── Comando /add-user ──────────────────────────────────────
@tree.command(name="add-user", description="Add a user to this ticket")
@app_commands.describe(user="User to add")
async def add_user(interaction: discord.Interaction, user: discord.Member):
    await interaction.channel.set_permissions(user, view_channel=True, send_messages=True)
    await interaction.response.send_message(f"✅ {user.mention} added to the ticket.")


# ── Comando /remove-user ───────────────────────────────────
@tree.command(name="remove-user", description="Remove a user from this ticket")
@app_commands.describe(user="User to remove")
async def remove_user(interaction: discord.Interaction, user: discord.Member):
    await interaction.channel.set_permissions(user, view_channel=False)
    await interaction.response.send_message(f"✅ {user.mention} removed from the ticket.")


# ── On ready ───────────────────────────────────────────────
@bot.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)
    tree.copy_global_to(guild=guild)
    await tree.sync(guild=guild)
    print(f"\n✅ SAAA Ticket Bot online: {bot.user}")
    print(f"   Slash commands synced to guild {GUILD_ID}")
    print(f"\n   Usa /ticket-panel en el canal de soporte para publicar el panel.")
    print(f"   Asegúrate de que el bot tiene permisos de Administrador.\n")


bot.run(TOKEN)
