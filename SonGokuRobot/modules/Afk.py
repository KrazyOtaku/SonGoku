import random
import time

from SonGokuRobot import dispatcher
from SonGokuRobot.modules.disable import DisableAbleCommandHandler
from SonGokuRobot.modules.sql import afk_sql as sql
from SonGokuRobot.modules.users import get_user_id
from telegram import MessageEntity, Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext, Filters, MessageHandler, run_async

AFK_GROUP = 7
AFK_REPLY_GROUP = 8


@run_async
def afk(update: Update, context: CallbackContext):
    args = update.effective_message.text.split(None, 1)
    afk_time = int(time.time())
    notice = ""
    if len(args) >= 2:
        reason = args[1]
        if len(reason) > 100:
            reason = reason[:100]
            notice = "\nYour afk reason was shortened to 100 characters."
    else:
        reason = ""

    sql.set_afk(update.effective_user.id, afk_time, reason)
    fname = update.effective_user.first_name
    update.effective_message.reply_text("{} 𝑖𝑠 𝑛𝑜𝑤 𝑎𝑤𝑎𝑦! 𝐺𝑖𝑏 𝑝𝑎𝑤𝑟𝑖!{}".format(fname, notice))


@run_async
def no_longer_afk(update: Update, context: CallbackContext):
    user = update.effective_user
    message = update.effective_message

    if not user:  # ignore channels
        return

    res = sql.rm_afk(user.id)
    if res:
        if message.new_chat_members:  # dont say msg
            return
        firstname = update.effective_user.first_name
        try:
            options = [
                "{} 𝑑𝑎𝑚𝑛... 𝐼 𝑠𝑎𝑤 𝑦𝑜𝑢 𝑤𝑒𝑟𝑒 𝑜𝑛𝑙𝑖𝑛𝑒.. 𝑟𝑒𝑎𝑑𝑖𝑛𝑔 𝑡ℎ𝑒 𝑚𝑒𝑠𝑠𝑎𝑔𝑒𝑠.. 𝑏𝑢𝑡 𝑢 𝑤𝑒𝑟𝑒 𝐴𝐹𝐾.",
                "{} 𝑤𝑒𝑙𝑐𝑜𝑚𝑒 𝑏𝑎𝑐𝑘 𝑏𝑟𝑜! 𝑁𝑜 𝑜𝑛𝑒 𝑚𝑖𝑠𝑠𝑒𝑑 𝑦𝑜𝑢!",
                "{} 𝑤𝑒𝑙𝑐𝑜𝑚𝑒 𝑏𝑎𝑐𝑘, 𝑛𝑜𝑤 𝑝𝑎𝑦 100$ 𝑜𝑟 𝑔𝑒𝑡 𝑏𝑎𝑛𝑛𝑒𝑑",
                "𝑌𝑎𝑚𝑒𝑡𝑒...𝑌𝑎𝑚𝑒𝑡𝑒 𝑘𝑢𝑑𝑎𝑠𝑎𝑖 {}-𝑠𝑎𝑚𝑎!",
                "𝑜ℎ 𝑚𝑦! {} 𝑔𝑜𝑡 𝑛𝑜 𝑐ℎ𝑖𝑙𝑙𝑠!",
                "𝑆𝑝𝑎𝑚𝑚𝑒𝑟 𝑗𝑢𝑠𝑡 𝑎𝑟𝑟𝑖𝑣𝑒𝑑.. 𝑏𝑒 𝑟𝑒𝑎𝑑𝑦 𝑒𝑣𝑒𝑟𝑦𝑜𝑛𝑒.. 𝑙𝑒𝑡 𝑚𝑒 𝑔𝑟𝑎𝑏 𝑚𝑦 𝑏𝑎𝑛-ℎ𝑎𝑚𝑚𝑒𝑟!",
                "{} 𝑏𝑟𝑢ℎ 𝑦𝑜𝑢 𝑠ℎ𝑜𝑢𝑙𝑑 𝑑𝑒𝑙𝑒𝑡𝑒 𝑦𝑜𝑢𝑟 𝑡𝑒𝑙𝑒𝑔𝑟𝑎𝑚 𝑎𝑐𝑐𝑜𝑢𝑛𝑡.",
                "{} 𝑦𝑒𝑠𝑠𝑠𝑠𝑠!!1 𝑙𝑒𝑡𝑠 𝑠𝑡𝑎𝑟𝑡 𝑡𝑟𝑎𝑠ℎ𝑖𝑛𝑔 𝑡ℎ𝑒 𝑐ℎ𝑎𝑡!",
                "{} 𝑤𝑒𝑙𝑐𝑜𝑚𝑒 𝑡𝑜 ℎ𝑒𝑙𝑙 𝑎𝑔𝑎𝑖𝑛!!",
                "{} 𝑔𝑜𝑡 𝑎 𝑔𝑖𝑟𝑙𝑓𝑟𝑖𝑒𝑛𝑑 𝑡ℎ𝑎𝑡𝑠 𝑤ℎ𝑦 ℎ𝑒 𝑤𝑎𝑠 𝐴𝐹𝐾!",
            ]
            chosen_option = random.choice(options)
            update.effective_message.reply_text(chosen_option.format(firstname))
        except:
            return


@run_async
def reply_afk(update: Update, context: CallbackContext):
    bot = context.bot
    message = update.effective_message
    userc = update.effective_user
    userc_id = userc.id
    if message.entities and message.parse_entities(
        [MessageEntity.TEXT_MENTION, MessageEntity.MENTION]
    ):
        entities = message.parse_entities(
            [MessageEntity.TEXT_MENTION, MessageEntity.MENTION]
        )

        chk_users = []
        for ent in entities:
            if ent.type == MessageEntity.TEXT_MENTION:
                user_id = ent.user.id
                fst_name = ent.user.first_name

                if user_id in chk_users:
                    return
                chk_users.append(user_id)

            if ent.type == MessageEntity.MENTION:
                user_id = get_user_id(
                    message.text[ent.offset : ent.offset + ent.length]
                )
                if not user_id:
                    # Should never happen, since for a user to become AFK they must have spoken. Maybe changed username?
                    return

                if user_id in chk_users:
                    return
                chk_users.append(user_id)

                try:
                    chat = bot.get_chat(user_id)
                except BadRequest:
                    print(
                        "Error: Could not fetch userid {} for AFK module".format(
                            user_id
                        )
                    )
                    return
                fst_name = chat.first_name

            else:
                return

            check_afk(update, context, user_id, fst_name, userc_id)

    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        fst_name = message.reply_to_message.from_user.first_name
        check_afk(update, context, user_id, fst_name, userc_id)


def check_afk(update, context, user_id, fst_name, userc_id):
    if sql.is_afk(user_id):
        user = sql.check_afk_status(user_id)
        afk_time = sql.get_afk_time(user_id)
        afk_since = get_readable_time((time.time() - afk_time))
        if not user.reason:
            if int(userc_id) == int(user_id):
                return
            res = "{} is afk since {}".format(fst_name, afk_since)
            update.effective_message.reply_text(res)
        else:
            if int(userc_id) == int(user_id):
                return
            res = "{} is 卂下长 since {}\nReason: {}".format(
                fst_name, afk_since, user.reason
            )
            update.effective_message.reply_text(res)


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


__help__ = """
 • `/afk <reason>`*:* mark yourself as AFK(away from keyboard).
When marked as AFK, any mentions will be replied to with a message to say you're not available!
"""

AFK_HANDLER = DisableAbleCommandHandler("afk", afk)
NO_AFK_HANDLER = MessageHandler(Filters.all & Filters.group, no_longer_afk)
AFK_REPLY_HANDLER = MessageHandler(Filters.all & Filters.group, reply_afk)

dispatcher.add_handler(AFK_HANDLER, AFK_GROUP)
dispatcher.add_handler(NO_AFK_HANDLER, AFK_GROUP)
dispatcher.add_handler(AFK_REPLY_HANDLER, AFK_REPLY_GROUP)

__mod_name__ = "AFK"
__command_list__ = ["afk"]
__handlers__ = [
    (AFK_HANDLER, AFK_GROUP),
    (NO_AFK_HANDLER, AFK_GROUP),
    (AFK_REPLY_HANDLER, AFK_REPLY_GROUP),
]
