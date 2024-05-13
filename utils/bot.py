from telebot import TeleBot
from utils.config import BOT_TOKEN, CHAT_ID, LAUNCH_PRICE

bot = TeleBot(token=BOT_TOKEN)


def create_presale_message(bnb_used, tokens_bought, tx_hash, stage_number, stage_price, launch_price, unit):
    # Determine the number of circles based on BNB used
    if bnb_used < 0.005:
        circles = "🟢" * 3
    elif bnb_used < 0.01:
        circles = "🟢" * 6
    elif bnb_used < 0.1:
        circles = "🟢" * 9
    elif bnb_used < 0.2:
        circles = "🟢" * 12
    else:
        circles = "🟢" * 16

    # Format the message
    message = f"""
🚀 *Token Presale Update*

{circles}
🎟️ Tokens Bought: {round(tokens_bought,3)} HLD
🔗 TX Hash: [View Transaction](https://bscscan.com/tx/{tx_hash})
🎭 Stage: {stage_number+1}
💵 Stage Price: {stage_price} BNB
🚀 Launch Price: {launch_price} BNB

*BUY NOW*
[www.Helldiver.vip](https://www.Helldiver.vip)
"""
    return message


def send_presale_alert(data):
    create_caption = create_presale_message(bnb_used=float(data['amountIn']), tokens_bought=float(data['tokens']),
                                            tx_hash=data['tx']['hash'], stage_number=data['stage'], stage_price=data['stage_price'],launch_price=LAUNCH_PRICE, unit=data['unit'])
    
    with open('utils/picture.gif', 'rb') as gif:
        bot.send_animation(chat_id=CHAT_ID, animation=gif, caption=create_caption, parse_mode='MarkDown')
    