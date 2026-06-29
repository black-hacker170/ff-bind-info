import telebot
from telebot import types
import json
import os
import requests
import re
from urllib.parse import urlparse, parse_qs

# ================= CONFIGURATION =================
BOT_TOKEN = "8847641700:AAFwKwRxC6PEdKSlsYhOHfP1gveLc0oVhTY"
CHANNEL_URL = "https://t.me/+4NhZQXvSXlVkYjY1"
ADMIN_1_USERNAME = "sakibblack"
ADMIN_2_USERNAME = "rx_ebrahim_2_0"
GITHUB_URL = "https://github.com/black-hacker170"
DB_FILE = "database.json"

bot = telebot.TeleBot(BOT_TOKEN)

# ================= DATABASE =================
def init_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w') as f:
            json.dump({}, f)

def get_user_data(user_id):
    init_db()
    with open(DB_FILE, 'r') as f:
        try:
            data = json.load(f)
        except:
            data = {}
    return data.get(str(user_id), {})

def save_user_data(user_id, key, value):
    init_db()
    with open(DB_FILE, 'r') as f:
        try:
            data = json.load(f)
        except:
            data = {}
    if str(user_id) not in data or not isinstance(data[str(user_id)], dict):
        data[str(user_id)] = {}
    data[str(user_id)][key] = value
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def delete_user_mail_data(user_id):
    init_db()
    with open(DB_FILE, 'r') as f:
        try:
            data = json.load(f)
        except:
            data = {}
    if str(user_id) in data and isinstance(data[str(user_id)], dict):
        data[str(user_id)]["email"] = ""
        data[str(user_id)]["token"] = ""
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

init_db()

# Helper function to convert seconds to readable format
def convert_seconds(s):
    try:
        s = int(s)
        d, h = divmod(s, 86400)
        h, m = divmod(h, 3600)
        m, s = divmod(m, 60)
        return f"{d} Day {h} Hour {m} Min {s} Sec"
    except:
        return "0 Day 0 Hour 0 Min 0 Sec"

# ================= MENUS =================
def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🔧 FF Bind Tools", callback_data="ff_tools"),
        types.InlineKeyboardButton("📧 Temp Mail", callback_data="temp_mail_menu"),
        types.InlineKeyboardButton("📢 Channel Link", url=CHANNEL_URL),
        types.InlineKeyboardButton("👨‍💻 Admin Connect", callback_data="admin_menu"),
        types.InlineKeyboardButton("📂 GitHub Link", url=GITHUB_URL)
    )
    return markup

def admin_connect_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("👤 1's Admin Connect", url=f"https://t.me/{ADMIN_1_USERNAME}"),
        types.InlineKeyboardButton("👤 2's Admin Connect", url=f"https://t.me/{ADMIN_2_USERNAME}"),
        types.InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="back_main")
    )
    return markup

def tools_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("🔄 1. Bind Change", callback_data="tool_1"),
        types.InlineKeyboardButton("🗑️ 2. Unbind Email", callback_data="tool_2"),
        types.InlineKeyboardButton("📊 3. Check Bind Info", callback_data="tool_3"),
        types.InlineKeyboardButton("❌ 4. Cancel Bind", callback_data="tool_4"),
        types.InlineKeyboardButton("📧 5. Bind New Email", callback_data="tool_5"),
        types.InlineKeyboardButton("🔍 6. Check Links", callback_data="tool_6"),
        types.InlineKeyboardButton("🔐 7. Revoke Token", callback_data="tool_7"),
        types.InlineKeyboardButton("🚀 8. EAT TO ACCESS", callback_data="tool_8"),
        types.InlineKeyboardButton("⬅️ Back", callback_data="back_main")
    ]
    markup.add(*buttons)
    return markup

def result_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("⬅️ Back to Tools", callback_data="ff_tools"),
        types.InlineKeyboardButton("🏠 Main Menu", callback_data="back_main")
    )
    return markup

def result_menu_with_copy():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("📋 Copy Token", callback_data="copy_generated_token"),
        types.InlineKeyboardButton("⬅️ Back to Tools", callback_data="ff_tools"),
        types.InlineKeyboardButton("🏠 Main Menu", callback_data="back_main")
    )
    return markup

def security_choice_menu(tool_type):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("✅ Yes (With Code)", callback_data=f"{tool_type}_sec_yes"),
        types.InlineKeyboardButton("❌ No (No Code/OTP)", callback_data=f"{tool_type}_sec_no"),
        types.InlineKeyboardButton("⬅️ Back", callback_data="ff_tools")
    )
    return markup

def temp_mail_dashboard(email, token):
    markup = types.InlineKeyboardMarkup(row_width=2)
    inbox_url = f"https://temp-mail.io/en/email/{email}/token/{token}" if email and token else "#"
    
    buttons = [
        types.InlineKeyboardButton("📥 Inbox", callback_data="tm_inbox"),
        types.InlineKeyboardButton("🔄 Refresh Inbox", callback_data="tm_refresh"),
        types.InlineKeyboardButton("🔄 Generate New", callback_data="tm_generate"),
        types.InlineKeyboardButton("🗑 Delete Email", callback_data="tm_delete")
    ]
    markup.add(*buttons)
    if email and token:
        markup.add(types.InlineKeyboardButton("🌐 Open Inbox (Web)", url=inbox_url))
    markup.add(types.InlineKeyboardButton("🏠 Main Menu", callback_data="back_main"))
    return markup

# ================= HANDLERS =================
@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = (
        "👋 *WELCOME TO BLACK TOOL*\n\n"
        "🔥 *Status:* `⚡ Active`\n"
        "⚙️ *Version:* `v1.0`\n\n"
        "👇 _Choose an option from below:_ "
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    # ---------------- TEMP MAIL LOGIC ----------------
    if call.data == "temp_mail_menu":
        bot.answer_callback_query(call.id)
        user_data = get_user_data(chat_id)
        email = user_data.get("email")
        
        if not email:
            text = "📧 *Temp Mail Bot* - Your privacy is our priority.\n\nআপনি এখনো কোনো ইমেইল জেনারেট করেননি। নিচের বাটনে চাপ দিয়ে ইমেইল তৈরি করুন।"
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("✨ Generate Email", callback_data="tm_generate"))
            markup.add(types.InlineKeyboardButton("🏠 Main Menu", callback_data="back_main"))
            bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)
        else:
            text = f"<b>📧 Your Temp Email</b>\n\n<code>{email}</code>"
            token = user_data.get("token", "")
            bot.edit_message_text(text, chat_id, message_id, parse_mode="HTML", reply_markup=temp_mail_dashboard(email, token))

    elif call.data == "tm_generate":
        bot.answer_callback_query(call.id, "Generating Email...")
        try:
            res = requests.post("https://api.internal.temp-mail.io/api/v3/email/new", json={
                "min_name_length": 10,
                "max_name_length": 10
            }, timeout=15)
            if res.status_code == 200:
                data = res.json()
                email = data.get("email")
                token = data.get("token")
                
                save_user_data(chat_id, "email", email)
                save_user_data(chat_id, "token", token)
                
                text = f"<b>📧 Your Temp Email</b>\n\n<code>{email}</code>"
                bot.edit_message_text(text, chat_id, message_id, parse_mode="HTML", reply_markup=temp_mail_dashboard(email, token))
            else:
                bot.send_message(chat_id, "❌ API Error. Try again.")
        except Exception as e:
            bot.send_message(chat_id, f"❌ Error: {str(e)}")

    elif call.data in ["tm_inbox", "tm_refresh"]:
        bot.answer_callback_query(call.id, "Checking Inbox...")
        user_data = get_user_data(chat_id)
        email = user_data.get("email")
        token = user_data.get("token", "")
        
        if not email:
            bot.send_message(chat_id, "❌ No active email found")
            return
            
        try:
            res = requests.get(f"https://api.internal.temp-mail.io/api/v3/email/{email}/messages", timeout=15)
            if res.status_code == 200:
                data = res.json()
                if not data or len(data) == 0:
                    bot.send_message(chat_id, "📭 No messages yet.")
                    return
                
                found = False
                for msg in data:
                    if not msg.get("body_text") and not msg.get("subject") and not msg.get("from"):
                        continue
                    
                    found = True
                    msg_from = msg.get("from", "Unknown")
                    subject = msg.get("subject", "No Subject")
                    body = msg.get("body_text", "Empty")
                    
                    text = (
                        "<b>📩 New Message</b>\n\n"
                        f"<b>From:</b> {msg_from}\n"
                        f"<b>Subject:</b> {subject}\n\n"
                        f"<b>Message:</b>\n<code>{body}</code>"
                    )
                    bot.send_message(chat_id, text, parse_mode="HTML")
                
                if not found:
                    bot.send_message(chat_id, "📭 No real messages yet.")
            else:
                bot.send_message(chat_id, "❌ Failed to load inbox")
        except Exception as e:
            bot.send_message(chat_id, f"❌ Error: {str(e)}")

    elif call.data == "tm_delete":
        bot.answer_callback_query(call.id)
        delete_user_mail_data(chat_id)
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✨ Generate New Email", callback_data="tm_generate"))
        markup.add(types.InlineKeyboardButton("🏠 Main Menu", callback_data="back_main"))
        
        bot.edit_message_text("🗑 Temp email deleted", chat_id, message_id, reply_markup=markup)

    # ---------------- ORIGINAL BOT LOGIC ----------------
    elif call.data == "ff_tools":
        bot.answer_callback_query(call.id)
        bot.edit_message_text("🔧 *Select a Free Fire Tool:*", chat_id, message_id, parse_mode="Markdown", reply_markup=tools_menu())
    
    elif call.data == "admin_menu":
        bot.answer_callback_query(call.id)
        bot.edit_message_text("👨‍💻 *Select an Admin to Connect:*", chat_id, message_id, parse_mode="Markdown", reply_markup=admin_connect_menu())
    
    elif call.data == "back_main":
        bot.answer_callback_query(call.id)
        welcome_text = (
            "👋 *WELCOME TO BLACK TOOL*\n\n"
            "🔥 *Status:* `⚡ Active`\n"
            "⚙️ *Version:* `v1.0`\n\n"
            "👇 _Choose an option from below:_ "
        )
        bot.edit_message_text(welcome_text, chat_id, message_id, parse_mode="Markdown", reply_markup=main_menu())

    elif call.data == "copy_generated_token":
        bot.answer_callback_query(call.id, text="🎯 Extracting Token...")
        msg_text = call.message.text
        
        token_match = re.search(r'([a-f0-9]{32,64})', msg_text)
        if token_match:
            clean_token = token_match.group(1)
            bot.send_message(chat_id, f"`{clean_token}`", parse_mode="Markdown")
        else:
            bot.send_message(chat_id, "❌ Token extraction failed. Please copy manually.")

    elif call.data in ["t1_sec_yes", "t1_sec_no", "t2_sec_yes", "t2_sec_no"]:
        bot.answer_callback_query(call.id)
        msg = bot.send_message(chat_id, "🔑 *Please Enter Your Access Token:*", parse_mode="Markdown")
        bot.register_next_step_handler(msg, route_security_flow, call.data)

    elif call.data.startswith("tool_"):
        bot.answer_callback_query(call.id)
        if call.data == "tool_1":
            bot.send_message(chat_id, "⚙️ *Do you have your current Security Code?*", parse_mode="Markdown", reply_markup=security_choice_menu("t1"))
        elif call.data == "tool_2":
            bot.send_message(chat_id, "⚙️ *Do you have your current Security Code?*", parse_mode="Markdown", reply_markup=security_choice_menu("t2"))
        elif call.data == "tool_8":
            msg = bot.send_message(chat_id, "📥 *Please Paste Your EAT Token or Full URL Here:*", parse_mode="Markdown")
            bot.register_next_step_handler(msg, run_tool_logic, call.data)
        elif call.data == "tool_5":
            msg = bot.send_message(chat_id, "📧 *Enter New Email for Binding:*", parse_mode="Markdown")
            bot.register_next_step_handler(msg, tool_5_get_email)
        else:
            msg = bot.send_message(chat_id, "🔑 *Please Enter Your Access Token:*", parse_mode="Markdown")
            bot.register_next_step_handler(msg, run_tool_logic, call.data)

# ================= CORE LOGIC ROUTER =================
def route_security_flow(message, flow_type):
    token = message.text.strip()
    chat_id = message.chat.id

    if flow_type == "t1_sec_yes":
        msg = bot.send_message(chat_id, "📧 *Enter New Email Address:*", parse_mode="Markdown")
        bot.register_next_step_handler(msg, t1_yes_step1, token)
    elif flow_type == "t1_sec_no":
        msg = bot.send_message(chat_id, "📧 *Enter Current Email Address:*", parse_mode="Markdown")
        bot.register_next_step_handler(msg, t1_no_step1, token)
    elif flow_type == "t2_sec_yes":
        msg = bot.send_message(chat_id, "🔐 *Enter Security Code:*", parse_mode="Markdown")
        bot.register_next_step_handler(msg, t2_yes_final, token)
    elif flow_type == "t2_sec_no":
        msg = bot.send_message(chat_id, "📧 *Enter Current Email Address:*", parse_mode="Markdown")
        bot.register_next_step_handler(msg, t2_no_step1, token)

# --- TOOL 1: Bind Change With Security ---
def t1_yes_step1(message, token):
    email = message.text.strip()
    res = requests.get("https://chngemailcode48.vercel.app/send_otp", params={'access_token': token, 'email': email})
    if res.status_code == 200:
        msg = bot.send_message(message.chat.id, "📩 *OTP Sent.* Enter OTP:")
        bot.register_next_step_handler(msg, t1_yes_step2, token, email)
    else:
        bot.send_message(message.chat.id, f"❌ Failed. Error: {res.text}", reply_markup=result_menu())

def t1_yes_step2(message, token, email):
    otp = message.text.strip()
    res = requests.get("https://chngemailcode48.vercel.app/verify_otp", params={'access_token': token, 'email': email, 'otp': otp})
    try:
        auth = res.json().get("verifier_token") or res.json().get("data", {}).get("verifier_token")
        if auth:
            msg = bot.send_message(message.chat.id, "🔐 *Enter Security Code:*")
            bot.register_next_step_handler(msg, t1_yes_step3, token, email, auth)
            return
    except:
        pass
    bot.send_message(message.chat.id, "❌ Invalid OTP or Error response.", reply_markup=result_menu())

def t1_yes_step3(message, token, email, auth):
    sec = message.text.strip()
    res = requests.get("https://chngemailcode48.vercel.app/verify_identity", params={'access_token': token, 'code': sec})
    try:
        iden = res.json().get("identity_token") or res.json().get("data", {}).get("identity_token")
        if iden:
            res_c = requests.get("https://chngemailcode48.vercel.app/create_rebind", params={'access_token': token, 'email': email, 'identity_token': iden, 'verifier_token': auth})
            bot.send_message(message.chat.id, f"📡 *Result:* {res_c.text}", reply_markup=result_menu())
            return
    except:
        pass
    bot.send_message(message.chat.id, "❌ Identity verification failed.", reply_markup=result_menu())

# --- TOOL 1: Bind Change No Security ---
def t1_no_step1(message, token):
    cur_email = message.text.strip()
    res = requests.get("https://chngeforgotcrownx72.vercel.app/otp", params={'access_token': token, 'current_email': cur_email})
    msg = bot.send_message(message.chat.id, "📩 *Current Email OTP Request Sent.* Enter OTP:")
    bot.register_next_step_handler(msg, t1_no_step2, token, cur_email)

def t1_no_step2(message, token, cur_email):
    otp = message.text.strip()
    res = requests.get("https://chngeforgotcrownx72.vercel.app/verify", params={'access_token': token, 'current_email': cur_email, 'otp': otp})
    try:
        iden = res.json().get("identity_token") or res.json().get("data", {}).get("identity_token")
        if iden:
            msg = bot.send_message(message.chat.id, "📧 *Enter New Email Address:*")
            bot.register_next_step_handler(msg, t1_no_step3, token, iden)
            return
    except:
        pass
    bot.send_message(message.chat.id, "❌ Verification failed.", reply_markup=result_menu())

def t1_no_step3(message, token, iden):
    new_email = message.text.strip()
    res = requests.get("https://chngeforgotcrownx72.vercel.app/newotp", params={'access_token': token, 'new_email': new_email})
    msg = bot.send_message(message.chat.id, f"📩 *New Email OTP Sent to {new_email}.* Enter OTP:")
    bot.register_next_step_handler(msg, t1_no_step4, token, iden, new_email)

def t1_no_step4(message, token, iden, new_email):
    otp2 = message.text.strip()
    res = requests.get("https://chngeforgotcrownx72.vercel.app/newverify", params={'access_token': token, 'new_email': new_email, 'otp': otp2})
    try:
        auth = res.json().get("verifier_token") or res.json().get("data", {}).get("verifier_token")
        if auth:
            res_f = requests.get("https://chngeforgotcrownx72.vercel.app/change", params={'access_token': token, 'new_email': new_email, 'identity_token': iden, 'verifier_token': auth})
            bot.send_message(message.chat.id, f"📡 *Result:* {res_f.text}", reply_markup=result_menu())
            return
    except:
        pass
    bot.send_message(message.chat.id, "❌ Process failed.", reply_markup=result_menu())

# --- TOOL 2: Unbind With Security ---
def t2_yes_final(message, token):
    sec = message.text.strip()
    res = requests.get("https://crownxnewkey10010.vercel.app/securityunbind", params={'access_token': token, 'security_code': sec})
    bot.send_message(message.chat.id, f"📡 *Unbind Result:* {res.text}", reply_markup=result_menu())

# --- TOOL 2: Unbind No Security ---
def t2_no_step1(message, token):
    cur_email = message.text.strip()
    res = requests.get("https://chngeforgotcrownx72.vercel.app/otp", params={'access_token': token, 'current_email': cur_email})
    msg = bot.send_message(message.chat.id, "📩 *OTP Request Sent.* Enter OTP:")
    bot.register_next_step_handler(msg, t2_no_step2, token, cur_email)

def t2_no_step2(message, token, cur_email):
    otp = message.text.strip()
    res = requests.get("https://chngeforgotcrownx72.vercel.app/verify", params={'access_token': token, 'current_email': cur_email, 'otp': otp})
    try:
        iden = res.json().get("identity_token") or res.json().get("data", {}).get("identity_token")
        if iden:
            res3 = requests.get("https://crownxforgotremove23.vercel.app/forgotunbind", params={'access_token': token, 'identity_token': iden})
            bot.send_message(message.chat.id, f"📡 *Result:* {res3.text}", reply_markup=result_menu())
            return
    except:
        pass
    bot.send_message(message.chat.id, "❌ Unbind Process Failed.", reply_markup=result_menu())

# --- TOOL 5: Bind New Email ---
def tool_5_get_email(message):
    email = message.text.strip()
    msg = bot.send_message(message.chat.id, "🔑 *Now Enter Your Access Token:*", parse_mode="Markdown")
    bot.register_next_step_handler(msg, tool_5_send_otp, email)

def tool_5_send_otp(message, email):
    token = message.text.strip()
    res = requests.get("https://bindcnclcrownx34.vercel.app/bind", params={'access_token': token, 'email': email})
    msg = bot.send_message(message.chat.id, "📩 *OTP Sent.* Enter OTP:")
    bot.register_next_step_handler(msg, tool_5_get_sec, token, email)

def tool_5_get_sec(message, token, email):
    otp = message.text.strip()
    msg = bot.send_message(message.chat.id, "🔐 *Enter Security Code:*")
    bot.register_next_step_handler(msg, tool_5_final, token, email, otp)

def tool_5_final(message, token, email, otp):
    sec = message.text.strip()
    res_c = requests.get("https://bindcnclcrownx34.vercel.app/confirmbind", params={'access_token': token, 'email': email, 'otp': otp, 'security_code': sec})
    bot.send_message(message.chat.id, f"📡 *Result:* {res_c.text}", reply_markup=result_menu())

# ================= CORE HANDLER FOR GENERAL TOOLS =================
def run_tool_logic(message, tool_id):
    user_input = message.text.strip()
    user_id = message.chat.id
    
    bot.send_message(user_id, "⏳ *Processing your request... Please wait*", parse_mode="Markdown")

    if tool_id == "tool_8":
        clean_token = user_input
        if "eat=" in user_input:
            try:
                if "http" in user_input:
                    parsed_url = urlparse(user_input)
                    clean_token = parse_qs(parsed_url.query).get('eat', [user_input])[0]
                else:
                    clean_token = parse_qs(user_input).get('eat', [user_input])[0]
            except Exception:
                clean_token = user_input

        try:
            api_url = "https://project-m0dtj.vercel.app/token"
            res = requests.get(api_url, params={'eat_token': clean_token}, timeout=20)
            if res.status_code == 200:
                bot.send_message(user_id, f"🎉 Success!\n\n📡 API Result:\n\n{res.text}", reply_markup=result_menu_with_copy())
            else:
                bot.send_message(user_id, f"❌ *API Error:* `Code {res.status_code}`", parse_mode="Markdown", reply_markup=result_menu())
        except Exception as e:
            bot.send_message(user_id, f"⚠️ *Error Occurred:* `{e}`", parse_mode="Markdown", reply_markup=result_menu())

    elif tool_id == "tool_3":
        try:
            res = requests.get("https://bindinfocrownx612.vercel.app/check", params={'access_token': user_input}, timeout=10)
            if res.status_code == 200:
                d = res.json().get("data", res.json())
                
                email = d.get("email", "")
                email_to_be = d.get("email_to_be", "")
                countdown = d.get("request_exec_countdown", 0)
                
                istikhada_status = "No Isti3ada !"
                if email == "" and email_to_be != "":
                    istikhada_status = f"Confirmed in : {convert_seconds(countdown)}"
                elif email != "" and email_to_be == "":
                    istikhada_status = "Confirmed : Yes Good !"

                output = (
                    f"📊 *FF BIND INFO RESULT*\n\n"
                    f"🔹 *Status:* `{d.get('status', 'N/A')}`\n"
                    f"🔹 *Summary:* `{d.get('summary', 'N/A')}`\n"
                    f"🔹 *Current Email:* `{d.get('current_email', 'N/A')}`\n"
                    f"🔹 *Pending Email:* `{d.get('pending_email', 'N/A')}`\n"
                    f"🔹 *Human Countdown:* `{d.get('countdown_human', 'N/A')}`\n"
                    f"🔹 *Mobile:* `{d.get('mobile', 'N/A')}`\n\n"
                    f"ℹ️ *Istikhada:* `{istikhada_status}`"
                )
                bot.send_message(user_id, output, parse_mode="Markdown", reply_markup=result_menu())
            else:
                bot.send_message(user_id, f"❌ *Failed!* HTTP Code: {res.status_code}", parse_mode="Markdown", reply_markup=result_menu())
        except Exception as e:
            bot.send_message(user_id, f"⚠️ *Error:* `{e}`", parse_mode="Markdown", reply_markup=result_menu())

    elif tool_id == "tool_4":
        try:
            res = requests.get("https://bindcnclcrownx34.vercel.app/cancelbind", params={'access_token': user_input})
            bot.send_message(user_id, f"📡 *Result:* {res.text}", reply_markup=result_menu())
        except Exception as e:
            bot.send_message(user_id, f"⚠️ *Error:* `{e}`", parse_mode="Markdown", reply_markup=result_menu())

    elif tool_id == "tool_6":
        try:
            r = requests.get("https://100067.connect.garena.com/bind/app/platform/info/get",
                             params={'access_token': user_input},
                             headers={'User-Agent': "GarenaMSDK/4.0.19P9(Redmi Note 5 ;Android 9;en;US;)"}, timeout=15)
            if r.status_code in [200, 201]:
                j = r.json()
                m = {3: "Facebook", 8: "Gmail", 10: "iCloud", 5: "VK", 11: "Twitter", 7: "Huawei"}
                b, a = j.get("bounded_accounts", []), j.get("available_platforms", [])
                
                output = "🔍 *SECONDARY LINKS INFO*\n\n"
                found_links = False
                for x in b:
                    p = x.get('platform')
                    uinfo = x.get('user_info', {})
                    if p in m:
                        output += f"🌐 *Platform:* `{m[p]}`\n📧 *Email:* `{uinfo.get('email', 'N/A')}`\n👤 *Name:* `{uinfo.get('nickname', 'N/A')}`\n\n"
                        found_links = True
                if not found_links:
                    output += "⚠️ *Secondary Links Not Found !*"
                
                bot.send_message(user_id, output, parse_mode="Markdown", reply_markup=result_menu())
            else:
                bot.send_message(user_id, f"❌ *Failed!* HTTP Code: {r.status_code}", parse_mode="Markdown", reply_markup=result_menu())
        except Exception as e:
            bot.send_message(user_id, f"⚠️ *Error:* `{e}`", parse_mode="Markdown", reply_markup=result_menu())

    elif tool_id == "tool_7":
        try:
            bot.send_message(user_id, "🔧 *Tool 7 Logic is under development.*", parse_mode="Markdown", reply_markup=result_menu())
        except Exception as e:
            bot.send_message(user_id, f"⚠️ *Error:* `{e}`", parse_mode="Markdown", reply_markup=result_menu())

# ================= START BOT POLLING =================
if __name__ == '__main__':
    print("Bot is starting...")
    bot.infinity_polling()
