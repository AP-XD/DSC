import asyncio
import os
import logging
import qrcode
from telethon import events
from bs4 import BeautifulSoup
from dsc import dsc
from dsc.dB.database import Var as Config
logger = logging.getLogger()

def p_call(current, total):
    logger.info(
        "Downloaded {} of {}\nCompleted {}".format(
            current, total, (current / total) * 100
        )
    )


@dsc.on(events.NewMessage(pattern="^.qr", outgoing=True))
async def _(ap):
    if ap.fwd_from:
        return
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    f_name = await dsc.download_media(
        await ap.get_reply_message(),
        Config.TMP_DOWNLOAD_DIRECTORY,
        progress_callback=p_call,
    )
    # parse the Official ZXing webpage to decode the QR
    command_to_exec = [
        "curl",
        "-X",
        "POST",
        "-F",
        "f=@" + f_name + "",
        "https://zxing.org/w/decode",
    ]
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    good = stdout.decode().strip()
    os.remove(f_name)
    if not good:
        logger.info(e_response)
        logger.info(good)
        await ap.edit("Failed to decode QRCode")
        return
    soup = BeautifulSoup(good, "html.parser")
    qr_contents = soup.find_all("pre")[0].text
    await ap.edit("Obtained QRCode")
    await asyncio.sleep(2)
    await ap.edit(qr_contents)


@dsc.on(events.NewMessage(pattern="^.mkqr ?(.*)", outgoing=True))
async def _(ap):
    if ap.fwd_from:
        return
    input_str = ap.pattern_match.group(1)
    message = ""
    reply_msg_id = ap.message.id
    if input_str:
        message = input_str
    elif ap.reply_to_msg_id:
        previous_message = await ap.get_reply_message()
        reply_msg_id = previous_message.id
        if previous_message.media:
            f_name = await dsc.download_media(
                previous_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=p_call,
            )
            m_list = None
            with open(f_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            for m in m_list:
                message += m.decode("UTF-8") + "\r\n"
            os.remove(f_name)
        else:
            message = previous_message.message
    else:
        message = ""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(message)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("img_file.webp", "PNG")
    await dsc.send_file(
        ap.chat_id,
        "img_file.webp",
        caption=message,
        reply_to=reply_msg_id,
        progress_callback=p_call,
    )
    os.remove("img_file.webp")
    await ap.edit("Created QRCode")
    await asyncio.sleep(2)
    await ap.delete()