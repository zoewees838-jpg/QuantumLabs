import sqlite3
import os
import hashlib
from telebot import TeleBot, types
from dotenv import load_dotenv

load_dotenv()

# Bot Token & Admin User ID configuration
TOKEN = os.getenv("BOT_TOKEN", "8706915052:AAHhz7uwkU8lSKqLG-FzvUAek27_LzTurck")
ADMIN_ID = int(os.getenv("ADMIN_ID", "8719436378"))

bot = TeleBot(TOKEN, parse_mode="HTML")

# ------------------- DATABASE SETUP -------------------
def get_db():
    conn = sqlite3.connect("apex_bet.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_a TEXT, team_b TEXT,
            odds_a REAL, odds_draw REAL, odds_b REAL,
            status TEXT DEFAULT 'UPCOMING'
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_code TEXT PRIMARY KEY,
            user_id INTEGER, username TEXT,
            match_id INTEGER, selection TEXT,
            stake REAL, payout REAL,
            status TEXT DEFAULT 'PENDING'
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ------------------- UI LAYOUT TEMPLATES -------------------
GOLD_HEADER = "✨ <b>=======================</b> ✨\n🏆 <b>APEX BET VIP SPORTSBOOK</b> 🏆\n✨ <b>=======================</b> ✨\n\n"

# ------------------- USER COMMANDS -------------------
@bot.message_handler(commands=['start', 'menu'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_matches = types.InlineKeyboardButton("⚽ Live Fixtures & Odds", callback_data="view_matches")
    btn_my_tickets = types.InlineKeyboardButton("🎟️ My Cash Tickets", callback_data="my_tickets")
    btn_help = types.InlineKeyboardButton("👑 VIP Support", callback_data="support")
    markup.add(btn_matches)
    markup.add(btn_my_tickets, btn_help)

    text = (
        f"{GOLD_HEADER}"
        f"<i>Welcome, <b>{message.from_user.first_name}</b></i> 👑\n\n"
        f"⚡ <b>Status:</b> Premium VIP Access\n"
        f"🪙 <b>Payment System:</b> Admin Cash Verification\n\n"
        f"Select an option below to browse active fixtures or inspect your ticket slips:"
    )
    bot.send_message(message.chat.id, text, reply_markup=markup)

# ------------------- CALLBACK HANDLERS -------------------
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    conn = get_db()
    c = conn.cursor()

    if call.data == "view_matches":
        c.execute("SELECT * FROM matches WHERE status = 'UPCOMING'")
        matches = c.fetchall()
        
        if not matches:
            bot.answer_callback_query(call.id, "No active fixtures right now!")
            return

        markup = types.InlineKeyboardMarkup()
        for m in matches:
            btn_text = f"⚔️ {m['team_a']} vs {m['team_b']}"
            markup.add(types.InlineKeyboardButton(btn_text, callback_data=f"match_{m['id']}"))
        
        markup.add(types.InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu"))
        
        text = f"{GOLD_HEADER}🔥 <b>AVAILABLE MATCH FIXTURES</b> 🔥\n\nChoose a fixture to view odds and register a bet slip:"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data.startswith("match_"):
        match_id = int(call.data.split("_")[1])
        c.execute("SELECT * FROM matches WHERE id = ?", (match_id,))
        m = c.fetchone()

        markup = types.InlineKeyboardMarkup(row_width=3)
        b1 = types.InlineKeyboardButton(f"1: {m['team_a']} ({m['odds_a']})", callback_data=f"bet_{match_id}_TEAM_A")
        bx = types.InlineKeyboardButton(f"X: Draw ({m['odds_draw']})", callback_data=f"bet_{match_id}_DRAW")
        b2 = types.InlineKeyboardButton(f"2: {m['team_b']} ({m['odds_b']})", callback_data=f"bet_{match_id}_TEAM_B")
        back = types.InlineKeyboardButton("🔙 Fixtures", callback_data="view_matches")
        
        markup.add(b1, bx, b2)
        markup.add(back)

        text = (
            f"{GOLD_HEADER}"
            f"⚔️ <b>{m['team_a'].upper()}</b> vs <b>{m['team_b'].upper()}</b>\n\n"
            f"🥇 <b>{m['team_a']} Win:</b> <code>{m['odds_a']}</code>\n"
            f"⚖️ <b>Draw:</b> <code>{m['odds_draw']}</code>\n"
            f"🥈 <b>{m['team_b']} Win:</b> <code>{m['odds_b']}</code>\n\n"
            f"<i>Tap your pick below to select outcome:</i>"
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data.startswith("bet_"):
        _, match_id, selection = call.data.split("_")
        
        # Prompt user to type stake in chat
        msg = bot.send_message(
            call.message.chat.id,
            f"💰 <b>ENTER YOUR STAKE AMOUNT (₦):</b>\n"
            f"<i>Reply to this message with the numerical amount (e.g. 2000).</i>"
        )
        bot.register_next_step_handler(msg, process_stake, int(match_id), selection)

    elif call.data == "main_menu":
        send_welcome(call.message)

    conn.close()

# ------------------- STAKE & TICKET GENERATOR -------------------
def process_stake(message, match_id, selection):
    try:
        stake = float(message.text.strip())
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM matches WHERE id = ?", (match_id,))
        m = c.fetchone()

        odds = m['odds_a'] if selection == 'TEAM_A' else (m['odds_draw'] if selection == 'DRAW' else m['odds_b'])
        payout = round(stake * odds, 2)

        # Unique Ticket Hash
        ticket_code = "APX-" + hashlib.md5(f"{message.from_user.id}_{match_id}_{stake}".encode()).hexdigest()[:6].upper()
        username = message.from_user.username or message.from_user.first_name

        c.execute(
            "INSERT INTO tickets (ticket_code, user_id, username, match_id, selection, stake, payout) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (ticket_code, message.from_user.id, username, match_id, selection, stake, payout)
        )
        conn.commit()
        conn.close()

        # Render Gold Ticket
        ticket_card = (
            f"{GOLD_HEADER}"
            f"🎟️ <b>OFFICIAL BET SLIP GENERATED</b>\n"
            f"<b>=======================</b>\n"
            f"🔑 <b>Ticket Code:</b> <code>{ticket_code}</code>\n"
            f"👤 <b>Player:</b> @{username}\n"
            f"⚔️ <b>Match:</b> {m['team_a']} vs {m['team_b']}\n"
            f"🎯 <b>Selection:</b> <code>{selection}</code> (@ {odds})\n"
            f"💵 <b>Stake:</b> ₦{stake:,.2f}\n"
            f"🏆 <b>Potential Return:</b> <b>₦{payout:,.2f}</b>\n"
            f"<b>=======================</b>\n"
            f"📌 <b>Status:</b> 🟡 <code>PENDING CASH VERIFICATION</code>\n\n"
            f"<i>Show this ticket code to the administrator to submit cash and validate your ticket.</i>"
        )
        bot.send_message(message.chat.id, ticket_card)

        # Alert Admin
        admin_alert = (
            f"⚡ <b>NEW CASH TICKET REGISTERED</b>\n\n"
            f"Code: <code>{ticket_code}</code>\n"
            f"User: @{username} ({message.from_user.id})\n"
            f"Stake: ₦{stake:,.2f}\n\n"
            f"To validate cash receipt, execute:\n"
            f"<code>/verify {ticket_code}</code>"
        )
        bot.send_message(ADMIN_ID, admin_alert)

    except ValueError:
        bot.reply_to(message, "❌ Invalid input. Please enter numbers only.")

# ------------------- ADMIN CONTROLS -------------------
# Format: /addmatch TeamA vs TeamB | OddsA | OddsDraw | OddsB
@bot.message_handler(commands=['addmatch'])
def admin_add_match(message):
    if message.from_user.id != ADMIN_ID: return
    try:
        raw = message.text.replace("/addmatch ", "")
        teams, oa, od, ob = [x.strip() for x in raw.split("|")]
        ta, tb = [t.strip() for t in teams.split("vs")]

        conn = get_db()
        c = conn.cursor()
        c.execute("INSERT INTO matches (team_a, team_b, odds_a, odds_draw, odds_b) VALUES (?, ?, ?, ?, ?)",
                  (ta, tb, float(oa), float(od), float(ob)))
        conn.commit()
        conn.close()

        bot.reply_to(message, f"✅ <b>Match Created!</b>\n{ta} vs {tb} added to sportsbook.")
    except Exception as e:
        bot.reply_to(message, "⚠️ <b>Usage:</b>\n<code>/addmatch Chelsea vs Arsenal | 2.10 | 3.20 | 2.50</code>")

@bot.message_handler(commands=['verify'])
def admin_verify_ticket(message):
    if message.from_user.id != ADMIN_ID: return
    try:
        ticket_code = message.text.split()[1].upper()
        conn = get_db()
        c = conn.cursor()
        c.execute("UPDATE tickets SET status = 'VALIDATED' WHERE ticket_code = ?", (ticket_code,))
        c.execute("SELECT * FROM tickets WHERE ticket_code = ?", (ticket_code,))
        t = c.fetchone()
        conn.commit()
        conn.close()

        if t:
            bot.reply_to(message, f"✅ Ticket <code>{ticket_code}</code> Status updated to <b>VALIDATED</b>!")
            bot.send_message(t['user_id'], f"🎉 <b>CASH RECEIVED!</b>\nYour ticket <code>{ticket_code}</code> is now <b>VALIDATED</b>!")
        else:
            bot.reply_to(message, "❌ Ticket code not found.")
    except Exception:
        bot.reply_to(message, "⚠️ <b>Usage:</b> <code>/verify APX-XXXXXX</code>")

print("⚡ Apex Bet VIP Bot Running...")
bot.infinity_polling()
