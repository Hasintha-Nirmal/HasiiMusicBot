# ==============================================================================
# cookie.py - Telegram YouTube Cookie Management (Sudo Only)
# ==============================================================================
# This plugin provides an easy way to add Netscape-formatted YouTube
# cookie files directly via Telegram for bypassing age-restrictions.
#
# Commands:
# - /addcookie - Reply to a .txt file to upload cookies.
# ==============================================================================

import os
import random
from pyrogram import filters, types
from HasiiMusic import app, yt, lang, logger

@app.on_message(filters.command(["addcookie", "upcookie"]) & app.sudo_filter)
@lang.language()
async def _addcookie(_, m: types.Message):
    # Auto-delete command message
    try:
        await m.delete()
    except Exception:
        pass

    # Basic instruction helper
    if not m.reply_to_message or not m.reply_to_message.document:
        return await m.reply_text(
            "<blockquote><b>❌ Missing Document</b></blockquote>\n\n"
            "<blockquote>Please reply to a valid <code>.txt</code> Netscape cookie file to upload it.</blockquote>"
        )
    
    doc = m.reply_to_message.document

    # Validate file extension
    if not doc.file_name or not doc.file_name.endswith(".txt"):
         return await m.reply_text(
             "<blockquote><b>❌ File Error</b></blockquote>\n\n"
             "<blockquote>Invalid file format! The cookie must be a <b>.txt</b> file in Netscape format.</blockquote>"
         )

    sent = await m.reply_text(
        "<blockquote><b>🔄 Downloading Cookie...</b></blockquote>\n\n"
        "<blockquote>Processing your uploaded file.</blockquote>"
    )

    try:
        # Define saving path
        cookie_path = f"HasiiMusic/cookies/cookie{random.randint(10000, 99999)}.txt"
        
        # Download document locally
        await m.reply_to_message.download(file_name=cookie_path)
        
        # Add to the active YouTube instance's cookie list to utilize instantly
        cookie_filename = os.path.basename(cookie_path)
        if cookie_filename not in yt.cookies:
            yt.cookies.append(cookie_filename)
            yt.checked = True

        logger.info(f"✅ User {m.from_user.id} manually uploaded new YouTube cookies: {cookie_filename}")

        return await sent.edit_text(
            "<blockquote><b>✅ Cookie Uploaded Successfully!</b></blockquote>\n\n"
            f"<blockquote>Cookie file <code>{cookie_filename}</code> has been saved correctly! It will be used for future YouTube interactions. You may need to run <code>/restart</code> to fully apply it to active streams.</blockquote>"
        )

    except Exception as e:
        logger.error(f"❌ Failed to process cookie upload from Telegram: {e}")
        return await sent.edit_text(
             "<blockquote><b>❌ Upload Failed</b></blockquote>\n\n"
             f"<blockquote>An error occurred: {str(e)}</blockquote>"
        )
