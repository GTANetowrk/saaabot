import discord
import asyncio

# ============================================================
#   SAN ANDREAS AVIATION ADMINISTRATION — Setup Script v2
#   English | Private channels | Clean aesthetic
# ============================================================

TOKEN = "PON_TU_TOKEN_AQUI"  # <-- reemplaza esto

intents = discord.Intents.default()
intents.guilds = True
client = discord.Client(intents=intents)

ROLES = [
    # (nombre, color_hex, hoist, mentionable)
    # Discord crea los roles de abajo hacia arriba,
    # así que los listamos del más bajo al más alto.

    # ── Visitantes y certificados (más bajos) ──
    ("👁️ Visitor",                              0x2C2F33, False, False),
    ("🎓 Student Pilot",                        0x747F8D, False, False),
    ("🛩️ Private Pilot — PPL",                 0x4F545C, False, False),
    ("✈️ Commercial Pilot — CPL",              0x206694, False, False),
    ("🏅 Airline Transport Pilot — ATP",        0xFFD700, False, False),

    # ── Admin & Finance ──
    ("💼 HR Management",                        0x1F8B4C, False, True),
    ("💻 Information Technology",               0x1F8B4C, False, True),
    ("📊 Finance & Management",                 0x1F8B4C, False, True),

    # ── Advanced Aviation Tech ──
    ("⚡ eVTOL / AAM Analyst",                  0x9B59B6, False, True),
    ("🛸 UAS Integration Specialist",           0x9B59B6, False, True),
    ("🚁 AAT Office Director",                  0x9B59B6, True,  True),

    # ── Policy & Legal ──
    ("📜 Regulatory Affairs Specialist",        0xE91E63, False, True),
    ("⚖️ Attorney — Aviation Law",              0xE91E63, False, True),
    ("🔏 Chief Counsel",                        0xE91E63, True,  True),

    # ── Airports Division ──
    ("🏗️ Airport Compliance Inspector",        0x607D8B, False, True),
    ("🛂 Airport Certification Specialist",     0x607D8B, False, True),
    ("🛫 Airports Division Director",           0x607D8B, True,  True),

    # ── Aviation Safety ──
    ("📋 Accident Investigation Specialist",    0xE67E22, False, True),
    ("🔍 Aviation Safety Technician",           0xF39C12, False, True),
    ("🔎 Aviation Safety Inspector — ASI",      0xF39C12, True,  True),
    ("🛡️ Flight Standards Division Manager",   0xE74C3C, False, True),
    ("🛡️ AVS Director",                        0xE74C3C, True,  True),

    # ── Air Traffic Organization ──
    ("🎙️ Developmental Controller — OJT",      0x1ABC9C, False, True),
    ("🎙️ Air Traffic Controller — CPC",        0x1ABC9C, True,  True),
    ("📡 TRACON Supervisor",                    0x2ECC71, True,  True),
    ("🗼 Area Manager | ATC",                   0x2ECC71, True,  True),
    ("🗼 ATO Deputy Director",                  0x27AE60, True,  True),
    ("🗼 ATO Director",                         0x27AE60, True,  True),

    # ── Leadership (más altos) ──
    ("🔵 Chief of Staff",                       0x3498DB, True,  True),
    ("🛩️ Deputy Administrator",                0xFF8C00, True,  True),
    ("✈️ Administrator | SAAA",                0xFFD700, True,  True),
]

# NOTA: Discord asigna posición jerárquica en el orden en que se crean.
# El script crea los roles en este orden y luego los reordena
# para que Administrator quede arriba y Visitor abajo.


# Estructura de canales
# ("category", "nombre")
# ("text", "nombre", "topic", readonly, private_staff)
# ("voice", "nombre", bitrate)
# ("announce", "nombre", "topic")  -> canal de anuncios

STRUCTURE = [

    ("category", "SAAA — Entrance Desk"),
        ("announce", "📋│rules",              "Server rules and guidelines. Read before proceeding."),
        ("text",     "👥│about-us",           "About the San Andreas Aviation Administration.", True, False),
        ("text",     "📞│contact-saaa",       "Contact information for all SAAA divisions.", True, False),
        ("text",     "👔│our-leadership",     "Meet the leadership team of the SAAA.", True, False),
        ("text",     "🎖️│credentials",       "Request your pilot certificate role here.", False, False),

    ("category", "SAAA — Aeronautical Information"),
        ("text",     "🗺️│ls-airspace",       "San Andreas airspace map: Class B/C/D zones and restricted areas.", True, False),
        ("text",     "🛬│airport-diagrams",   "Official airport diagrams for KLSIA, KSBA and all SA airports.", True, False),
        ("text",     "🌤️│metar",             "Current METAR and weather information for San Andreas airports.", True, False),
        ("text",     "📢│notices-to-airmen",  "Active NOTAMs for the San Andreas National Airspace System.", True, False),

    ("category", "SAAA — Newsroom"),
        ("announce", "📣│saaa-news",          "Official press releases and announcements from SAAA HQ."),
        ("text",     "💼│open-positions",     "Current job openings within the SAAA.", True, False),
        ("text",     "📸│x-saaa",             "Posts and updates from the official SAAA X (Twitter) account.", True, False),
        ("text",     "📷│instagram-saaa",     "Posts and updates from the official SAAA Instagram.", True, False),

    ("category", "SAAA — Lounge"),
        ("text",     "💬│general",            "General conversation for all SAAA members.", False, False),
        ("text",     "✈️│aviation-talk",      "Discuss aviation topics, real-world news and aircraft.", False, False),
        ("text",     "📸│flight-gallery",     "Share screenshots and photos from your flights. Images only.", False, False),
        ("text",     "🎮│off-topic",          "Anything that isn't aviation. Keep it civil.", False, False),
        ("voice",    "🔊 Lounge",             64000),

    ("category", "SAAA — Air Traffic Organization"),
        ("text",     "📡│ato-general",        "General channel for the Air Traffic Organization.", False, True),
        ("text",     "📋│atc-procedures",     "Standard procedures, phraseology and SOPs for ATC operations.", True, True),
        ("text",     "📟│active-notams",      "Active NOTAMs issued by the ATO. Staff post only.", True, True),
        ("text",     "📊│traffic-reports",    "ATC session logs, traffic reports and incident records.", False, True),
        ("voice",    "🎙️ KLSIA Ground / Tower", 64000),
        ("voice",    "🎙️ KLSIA Approach / Departure", 64000),
        ("voice",    "🎙️ KLSIA ARTCC Center", 64000),

    ("category", "SAAA — Aviation Safety"),
        ("text",     "🛡️│avs-general",       "General channel for the Aviation Safety Division.", False, True),
        ("text",     "🔍│active-inspections", "Active safety inspection log. Format: [Date] [Operator] [Type] [Status]", False, True),
        ("text",     "📋│airworthiness",      "Aircraft type certification and airworthiness records.", False, True),
        ("text",     "🚨│accident-reports",   "Aviation accident and incident reports. Coordination with NTSB.", False, True),
        ("text",     "📁│sms-reports",        "Safety Management System — risk reports and corrective action tracking.", False, True),

    ("category", "SAAA — Airports Division"),
        ("text",     "🛫│arp-general",        "General channel for the Airports Division.", False, True),
        ("text",     "🏗️│airport-projects",  "Construction, expansion and improvement projects across SA airports.", False, True),
        ("text",     "📋│part-139",           "Part 139 compliance tracking for certified SA airports.", False, True),

    ("category", "SAAA — Policy & Legal"),
        ("text",     "⚖️│legal-general",      "Office of Policy and Legal Affairs.", False, True),
        ("text",     "📜│saaa-regulations",   "Active SAAA regulations. Equivalent to CFR Title 14 (FARs).", True, True),
        ("text",     "🔨│enforcement",        "Record of sanctions, suspensions and certificate revocations.", False, True),

    ("category", "SAAA — Advanced Aviation Tech"),
        ("text",     "🚁│aat-general",        "Advanced Aviation Technologies division general channel.", False, True),
        ("text",     "🛸│uas-drones",         "UAS/drone regulation and integration into SA airspace.", False, True),
        ("text",     "⚡│evtol-aam",          "Electric Vertical Takeoff & Landing and advanced air mobility.", False, True),

    ("category", "SAAA — Citizen Services"),
        ("text",     "📝│pilot-certificate",  "Request your pilot certificate here. See pinned message for format.", False, False),
        ("text",     "✈️│aircraft-registry",  "Register your aircraft. Include: registration, type, owner, base.", False, False),
        ("text",     "📡│flight-plan",        "Submit your flight plan before operating. IFR/VFR format pinned.", False, False),
        ("text",     "🚨│report-incident",    "Report aviation incidents. Mandatory under SAAA Regulation §830.", False, False),
        ("text",     "📋│application-status", "Check the status of your pending requests. Staff respond only.", True, False),

    ("category", "SAAA — Human Resources"),
        ("text",     "📢│job-openings",       "Open positions within the SAAA. Read only.", True, True),
        ("text",     "📝│applications",       "Submit your application. Format: Name | Position | Division | Experience", False, True),
        ("text",     "📊│performance-review", "Internal performance evaluations and staff tracking.", False, True),

    ("category", "SAAA — Executive Office"),
        ("text",     "🔒│administrator-desk", "Administrator's office. Executive decisions of the SAAA.", False, True),
        ("text",     "📊│budget-policy",      "Budget planning and institutional policy.", False, True),
        ("text",     "📋│executive-meetings", "Meeting minutes and executive session records.", False, True),
        ("voice",    "🔒 Executive Chamber",  96000),
]

STAFF_ROLE_NAMES = [
    "✈️ Administrator | SAAA",
    "🛩️ Deputy Administrator",
    "🔵 Chief of Staff",
    "🗼 ATO Director",
    "🗼 ATO Deputy Director",
    "🗼 Area Manager | ATC",
    "📡 TRACON Supervisor",
    "🎙️ Air Traffic Controller — CPC",
    "🛡️ AVS Director",
    "🛡️ Flight Standards Division Manager",
    "🛫 Airports Division Director",
    "🔏 Chief Counsel",
    "🚁 AAT Office Director",
    "📊 Finance & Management",
    "💻 Information Technology",
    "💼 HR Management",
]

EXEC_ROLE_NAMES = [
    "✈️ Administrator | SAAA",
    "🛩️ Deputy Administrator",
    "🔵 Chief of Staff",
]

@client.event
async def on_ready():
    print(f"\n✅ Bot conectado como: {client.user}")

    if not client.guilds:
        print("❌ El bot no está en ningún servidor.")
        await client.close()
        return

    guild = client.guilds[0]
    print(f"🏛️  Servidor: {guild.name}")
    print("⚙️  Iniciando setup SAAA v2...\n")

    # ── Renombrar server ──────────────────────────────────────
    await guild.edit(name="S.A. Aviation Administration")
    print("📝 Servidor renombrado.")

    # ── Borrar roles ──────────────────────────────────────────
    print("🗑️  Limpiando roles...")
    for role in guild.roles:
        if role.name != "@everyone" and not role.managed:
            try:
                await role.delete()
                await asyncio.sleep(0.5)
            except:
                pass

    # ── Crear roles ───────────────────────────────────────────
    print(f"🎭 Creando {len(ROLES)} roles...")
    created_roles = {}
    for nombre, color, hoist, mentionable in ROLES:
        try:
            r = await guild.create_role(
                name=nombre,
                color=discord.Color(color),
                hoist=hoist,
                mentionable=mentionable
            )
            created_roles[nombre] = r
            print(f"   ✅ {nombre}")
            await asyncio.sleep(0.6)
        except Exception as e:
            print(f"   ❌ {nombre}: {e}")

    # ── Reordenar roles: Administrator arriba, Visitor abajo ──
    print("\n🔃 Reordenando jerarquía de roles...")
    try:
        positions = {}
        for i, (nombre, *_) in enumerate(ROLES):
            if nombre in created_roles:
                positions[created_roles[nombre]] = i + 1
        await guild.edit_role_positions(positions)
        print("   ✅ Jerarquía: Administrator arriba → Visitor abajo")
    except Exception as e:
        print(f"   ⚠️ Reordenamiento manual necesario: {e}")

    staff_roles  = [created_roles[n] for n in STAFF_ROLE_NAMES if n in created_roles]
    exec_roles   = [created_roles[n] for n in EXEC_ROLE_NAMES  if n in created_roles]
    everyone     = guild.default_role

    # ── Borrar canales ────────────────────────────────────────
    print("\n🗑️  Limpiando canales...")
    for ch in guild.channels:
        try:
            await ch.delete()
            await asyncio.sleep(0.4)
        except:
            pass

    # ── Crear canales ─────────────────────────────────────────
    print("\n📁 Creando estructura de canales...")
    current_cat = None

    for item in STRUCTURE:
        tipo = item[0]

        if tipo == "category":
            nombre = item[1]
            # Categorías privadas por defecto (solo staff ve)
            overwrites = {
                everyone: discord.PermissionOverwrite(view_channel=False),
            }
            for r in staff_roles:
                overwrites[r] = discord.PermissionOverwrite(view_channel=True)
            try:
                current_cat = await guild.create_category(nombre, overwrites=overwrites)
                print(f"\n   📁 {nombre}")
                await asyncio.sleep(0.5)
            except Exception as e:
                print(f"   ❌ Categoría {nombre}: {e}")

        elif tipo == "text":
            _, nombre, topic, readonly, private_staff = item

            if private_staff:
                # Solo staff puede ver y escribir
                overwrites = {
                    everyone: discord.PermissionOverwrite(view_channel=False),
                }
                for r in staff_roles:
                    overwrites[r] = discord.PermissionOverwrite(
                        view_channel=True,
                        send_messages=not readonly
                    )
            else:
                # Todos pueden ver, pero escribir depende de readonly
                overwrites = {
                    everyone: discord.PermissionOverwrite(
                        view_channel=True,
                        send_messages=not readonly
                    ),
                }
                for r in staff_roles:
                    overwrites[r] = discord.PermissionOverwrite(
                        view_channel=True,
                        send_messages=True
                    )

            try:
                await guild.create_text_channel(
                    nombre,
                    category=current_cat,
                    topic=topic,
                    overwrites=overwrites
                )
                print(f"      💬 {nombre}")
                await asyncio.sleep(0.5)
            except Exception as e:
                print(f"      ❌ {nombre}: {e}")

        elif tipo == "announce":
            _, nombre, topic = item
            overwrites = {
                everyone: discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=False
                ),
            }
            for r in staff_roles:
                overwrites[r] = discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True
                )
            try:
                await guild.create_text_channel(
                    nombre,
                    category=current_cat,
                    topic=topic,
                    overwrites=overwrites
                )
                print(f"      📣 {nombre}")
                await asyncio.sleep(0.5)
            except Exception as e:
                print(f"      ❌ {nombre}: {e}")

        elif tipo == "voice":
            _, nombre, bitrate = item
            overwrites = {
                everyone: discord.PermissionOverwrite(view_channel=False),
            }
            for r in staff_roles:
                overwrites[r] = discord.PermissionOverwrite(
                    view_channel=True,
                    connect=True
                )
            try:
                await guild.create_voice_channel(
                    nombre,
                    category=current_cat,
                    bitrate=bitrate,
                    overwrites=overwrites
                )
                print(f"      🎙️ {nombre}")
                await asyncio.sleep(0.5)
            except Exception as e:
                print(f"      ❌ {nombre}: {e}")

    print("\n" + "="*55)
    print("✅  S.A. Aviation Administration — Setup completo!")
    print(f"    Roles: {len(created_roles)} | Estructura lista")
    print("="*55)
    await client.close()

client.run(TOKEN)
