import os

import aiohttp
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from assistants.config import environment
from assistants.telegram_ui.auth import (
    restricted_access,
    requires_superuser,
    chat_data,
)
from assistants.telegram_ui.lib import (
    requires_reply_to_message,
    assistant,
    audio_completion,
)
from assistants.user_data.interfaces.telegram_chat_data import ChatHistory
from assistants.user_data.sqlite_backend import conversations_table


@requires_superuser
@requires_reply_to_message
async def promote_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await chat_data.promote_superuser(update.message.reply_to_message.from_user.id)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="User promoted"
    )


@requires_superuser
@requires_reply_to_message
async def demote_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await chat_data.demote_superuser(update.message.reply_to_message.from_user.id)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="User demoted"
    )


@requires_superuser
async def authorise_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await chat_data.authorise_chat(update.effective_chat.id)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Chat authorised"
    )


@requires_superuser
@requires_reply_to_message
async def authorise_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await chat_data.authorise_chat(update.message.reply_to_message.from_user.id)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="User authorised"
    )


@requires_superuser
async def deauthorise_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await chat_data.deauthorise_chat(update.effective_chat.id)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Chat de-authorised"
    )


@requires_superuser
@requires_reply_to_message
async def deauthorise_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await chat_data.deauthorise_user(update.message.reply_to_message.from_user.id)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="User de-authorised"
    )


@restricted_access
async def new_thread(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await chat_data.clear_last_thread_id(update.effective_chat.id)
    await conversations_table.delete_conversation(update.effective_chat.id)
    assistant.last_message = None
    await context.bot.send_message(
        update.effective_chat.id, "Conversation history cleared."
    )


@restricted_access
async def toggle_auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_history = await chat_data.get_chat_history(update.effective_chat.id)
    result = "OFF" if chat_history.auto_reply else "ON"
    await chat_data.set_auto_reply(
        update.effective_chat.id, not chat_history.auto_reply
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=f"Auto reply is {result}"
    )


@restricted_access
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    existing_chat = await chat_data.get_chat_history(update.effective_chat.id)
    message_text = update.message.text
    if not existing_chat.auto_reply:
        bot_id = context.bot.id
        bot_username = f"@{context.bot.username}"
        if bot_username not in message_text and (
            not update.message.reply_to_message
            or update.message.reply_to_message.from_user.id != bot_id
        ):
            return
        message_text = message_text.replace(
            bot_username, os.getenv("ASSISTANT_NAME", "[ASSISTANT NAME]")
        )

    await assistant.load_conversation(
        existing_chat.thread_id or update.effective_chat.id,
        initial_system_message=f"You are a Telegram bot called {context.bot.first_name or context.bot.username}.\n{environment.ASSISTANT_INSTRUCTIONS}",
    )

    response_message = await assistant.converse(message_text, existing_chat.thread_id)

    if not existing_chat.thread_id:
        await chat_data.save_chat_history(
            ChatHistory(
                chat_id=update.effective_chat.id,
                thread_id=str(assistant.conversation_id),
                auto_reply=existing_chat.auto_reply,
            )
        )

    await assistant.save_conversation_state()

    response = response_message.text_content

    response_parts = response.split("```")

    if len(response_parts) % 2 == 0:
        # Should be an odd number of parts if codeblocks
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=response,
        )
        return

    for i, part in enumerate(response_parts):
        if i % 2:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"```{part}```",
                parse_mode=ParseMode.MARKDOWN_V2,
            )
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=part,
            )


@restricted_access
async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text.replace("/image ", "")
    image_url = await assistant.image_prompt(prompt)

    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as response:
            image_content = await response.read()

    await update.message.reply_photo(image_content)


@restricted_access
async def respond_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    existing_chat = await chat_data.get_chat_history(update.effective_chat.id)

    await audio_completion.load_conversation(
        existing_chat.thread_id or update.effective_chat.id,
        initial_system_message=f"You are a Telegram bot called {context.bot.first_name or context.bot.username}.\n{environment.ASSISTANT_INSTRUCTIONS}",
    )

    response = await audio_completion.complete_audio(
        update.message.text.replace("/voice ", "")
    )

    if not existing_chat.thread_id:
        await chat_data.save_chat_history(
            ChatHistory(
                chat_id=update.effective_chat.id,
                thread_id=str(audio_completion.conversation_id),
                auto_reply=existing_chat.auto_reply,
            )
        )

    await audio_completion.save_conversation_state()
    if isinstance(response, bytes):
        await context.bot.send_voice(
            chat_id=update.effective_chat.id,
            voice=response,
            caption="Response",
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=response,
        )
