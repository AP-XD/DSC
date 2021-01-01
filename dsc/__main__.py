import glob
from pathlib import Path
from . import *
import logging
from telethon import TelegramClient
import telethon.utils
logging.basicConfig(format="%(asctime)s - ⫸ %(name)s ⫷ - %(levelname)s - ║ %(message)s ║", level=INFO)
logger = logging.getLogger()
def load_plugins(plugin_name):
    if plugin_name.startswith("__"):
        pass
    elif plugin_name.endswith("_"):
        import importlib
        from pathlib import Path
        path = Path(f"dsc/plugins/{plugin_name}.py")
        name = "dsc.plugins.{}".format(plugin_name)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        logger.info("dsc has (re)Imported " + plugin_name)
    else:
        import importlib, sys
        from pathlib import Path                        
        path = Path(f"dsc/plugins/{plugin_name}.py")
        name = "dsc.plugins.{}".format(plugin_name)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.dsc = dsc
        spec.loader.exec_module(mod)
        sys.modules["dsc.plugins." + plugin_name] = mod
        logger.info("☣️dsc☣️ has Imported " + plugin_name)
        
async def start(hehe):
    await dsc.start(hehe)
    dsc.me = await dsc.get_me() 
    dsc.uid = telethon.utils.get_peer_id(dsc.me)

async def bot_info(BOT_TOKEN):
    asstinfo = await asst.get_me()
    bot_name = asstinfo.username
                  
                    
dsc.asst = None
logger.info("Initialising...")
if BOT_TOKEN is not None:
    logger.info("Setting up dsc...")
    dsc.asst = TelegramClient("BOT_TOKEN",api_id=Var.API_ID,api_hash=Var.API_HASH).start(bot_token=Var.BOT_TOKEN)
    logger.info("dsc loaded.")
    logger.info("Starting dsc UserBot!")
    dsc.loop.run_until_complete(start(Var.BOT_TOKEN))
    logger.info("Done, startup completed")
else:
    logger.info("Starting User Mode...")
    dsc.start()

path = "dsc/plugins/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as a:
        patt = Path(a.name)
        plugin_name = patt.stem
        load_plugins(plugin_name.replace(".py", ""))
        logger.info(f"dsc installed {plugin_name}")
logger.info("dsc has been deployed!!")

if __name__ == "__main__":
    dsc.run_until_disconnected()
