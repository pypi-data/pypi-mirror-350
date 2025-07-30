import asyncio
from collections import defaultdict
from pathlib import Path

import nest_asyncio
from cement import Controller, ex
from telegraph import Telegraph

from grabber.core.settings import TELEGRAPH_TOKEN
from grabber.core.sources.asianviralhub import get_sources_for_asianviralhub
from grabber.core.sources.buondua import get_sources_for_buondua
from grabber.core.sources.bypass import bypass_link, bypass_ouo
from grabber.core.sources.common import get_sources_for_common
from grabber.core.sources.cosxuxi import get_sources_for_cosxuxi
from grabber.core.sources.ehentai import get_sources_for_ehentai
from grabber.core.sources.erome import get_sources_for_erome
from grabber.core.sources.everia import get_sources_for_everia
from grabber.core.sources.fapachi import get_sources_for_fapachi
from grabber.core.sources.fapello import get_sources_for_fapello
from grabber.core.sources.fapello_pics import get_sources_for_fapello_pics
from grabber.core.sources.fapello_to import get_sources_for_fapello_to
from grabber.core.sources.fapeza import get_sources_for_fapeza
from grabber.core.sources.fapomania import get_sources_for_fapomania
from grabber.core.sources.fuligirl import get_sources_for_fuligirl
from grabber.core.sources.graph import get_for_telegraph
from grabber.core.sources.hentai_club import get_sources_for_hentai_club
from grabber.core.sources.hotgirl2024 import get_sources_for_hotgirl2024
from grabber.core.sources.hotgirl_asia import get_sources_for_hotgirl_asia
from grabber.core.sources.hotgirl_china import get_sources_for_hotgirl_china
from grabber.core.sources.hotleaks import get_sources_for_hotleaks
from grabber.core.sources.jrants import get_sources_for_jrant
from grabber.core.sources.kemono import get_sources_for_kemono
from grabber.core.sources.khd import get_sources_for_4khd
from grabber.core.sources.kup import get_sources_for_4kup
from grabber.core.sources.lewdweb import get_sources_for_lewdweb
from grabber.core.sources.lovecos import get_sources_for_lovecos
from grabber.core.sources.misskon import get_sources_for_misskon
from grabber.core.sources.mitaku import get_sources_for_mitaku
from grabber.core.sources.notion import get_sources_for_notion
from grabber.core.sources.nsfw247 import get_sources_for_nsfw24
from grabber.core.sources.nudecosplay import get_sources_for_nudecosplay
from grabber.core.sources.nudogram import get_sources_for_nudogram
from grabber.core.sources.nudostar import get_sources_for_nudostar
from grabber.core.sources.ouo import ouo_bypass
from grabber.core.sources.paster import retrieve_paster_contents
from grabber.core.sources.pixibb import get_sources_for_pixibb
from grabber.core.sources.spacemiss import get_sources_for_spacemiss
from grabber.core.sources.sweetlicious import get_sources_for_sweetlicious
from grabber.core.sources.thefappening import get_sources_for_fappening
from grabber.core.sources.ugirls import get_sources_for_ugirls
from grabber.core.sources.xasiat import get_for_xasiat
from grabber.core.sources.xiuren import get_sources_for_xiuren
from grabber.core.sources.xlust import get_sources_for_xlust
from grabber.core.sources.xmissy import get_sources_for_xmissy
from grabber.core.sources.xpics import get_sources_for_xpics
from grabber.core.utils import get_entity, query_mapping, upload_folders_to_telegraph

from ..core.version import get_version

VERSION_BANNER = f"""
A beautiful CLI utility to download images from the web! {get_version()}
"""


class Base(Controller):
    class Meta:
        label = "base"

        # text displayed at the top of --help output
        description = "A beautiful CLI utility to download images from the web"

        # text displayed at the bottom of --help output
        epilog = "Usage: grabber --entity 4khd --folder 4khd --publish --sources <list of links>"

        # controller level arguments. ex: 'test --version'
        arguments = [
            ### add a version banner
            (
                ["-s", "--sources"],
                {
                    "dest": "sources",
                    "type": str,
                    "help": "List of links",
                    "nargs": "+",
                },
            ),
            (
                ["-f", "--folder"],
                {
                    "dest": "folder",
                    "default": "",
                    "type": str,
                    "help": "Folder where to save",
                },
            ),
            (
                ["-l", "--limit"],
                {
                    "dest": "limit",
                    "type": int,
                    "help": "Limit the amount of posts retrieved (used altogether with --tag)",
                    "default": 0,
                },
            ),
            (
                ["-p", "--publish"],
                {
                    "dest": "publish",
                    "action": "store_true",
                    "help": "Publish page to telegraph",
                },
            ),
            (
                ["-u", "--upload"],
                {
                    "dest": "upload",
                    "action": "store_true",
                    "help": "Upload and publish folders to telegraph",
                },
            ),
            (
                ["-t", "--tag"],
                {
                    "dest": "is_tag",
                    "action": "store_true",
                    "help": "Indicates that the link(s) passed is a tag in which the posts are paginated",
                },
            ),
            (
                ["-b", "--bot"],
                {
                    "dest": "bot",
                    "action": "store_true",
                    "help": "Should the newly post be sent to telegram?",
                },
            ),
            (
                ["-v", "--version"],
                {
                    "action": "store_true",
                    "dest": "version",
                    "help": "Version of the lib",
                },
            ),
            (
                ["-a", "--show-all-entities"],
                {
                    "action": "store_true",
                    "dest": "show_all_entities",
                    "help": "Show all the websites supported",
                },
            ),
            (
                ["-bl", "--bypass-link"],
                {
                    "dest": "bypass_link",
                    "type": str,
                    "help": "Bypass a link and returns the final URL",
                    "default": "",
                    "nargs": "+",
                },
            ),
            (
                ["-vd", "--video-enabled"],
                {
                    "dest": "is_video_enabled",
                    "action": "store_true",
                    "help": "Indicates that should also try to grab videos",
                },
            ),
        ]

    @ex(hide=True)
    def _default(self):
        """Default action if no sub-command is passed."""
        nest_asyncio.apply()

        sources: list[str] = self.app.pargs.sources
        folder = self.app.pargs.folder

        if folder:
            final_dest = Path(folder)
        else:
            final_dest = folder
        publish = self.app.pargs.publish
        # publish = True
        upload = self.app.pargs.upload
        is_tag = self.app.pargs.is_tag
        limit = self.app.pargs.limit
        version = self.app.pargs.version
        send_to_telegram = self.app.pargs.bot
        send_to_telegram = True
        telegraph_client = Telegraph(access_token=TELEGRAPH_TOKEN)
        show_all_entities = self.app.pargs.show_all_entities
        links_to_bypass: list[str] = self.app.pargs.bypass_link
        is_video_enabled = self.app.pargs.is_video_enabled

        if links_to_bypass:
            entity = asyncio.run(get_entity(links_to_bypass))
            if entity == "ouo":
                asyncio.run(ouo_bypass(links_to_bypass))
            elif entity == "paster.so":
                paster_ids: list[str] = []
                for paster_link in links_to_bypass:
                    paster_id = paster_link.split("/")[-1]
                    paster_ids.append(paster_id)
                paster_contents = retrieve_paster_contents(paster_ids)

                for content in paster_contents:
                    print(f"{content}\n\n\n")
                return
            else:
                for link in links_to_bypass:
                    try:
                        final_url = bypass_link(link)
                    except Exception:
                        final_url = None

                    if final_url is None:
                        final_url = bypass_ouo(link)

                    print(f"{final_url}")
                return

        if show_all_entities:
            websites = "All websites supported:\n"
            entities = sorted(list(query_mapping.keys()))
            for entity in entities:
                websites += f"\t- {entity}\n"

            print(websites)
            return

        if version:
            print(VERSION_BANNER)
            return

        getter_mapping = {
            "www.4khd.com": get_sources_for_4khd,
            "telegra.ph": get_for_telegraph,
            "xiuren.biz": get_sources_for_xiuren,
            "nudecosplay.biz": get_sources_for_nudecosplay,
            "nudebird.biz": get_sources_for_nudecosplay,
            "hotgirl.biz": get_sources_for_nudecosplay,
            "everia.club": get_sources_for_everia,
            "www.everiaclub.com": get_sources_for_everia,
            "bestgirlsexy.com": get_sources_for_common,
            "asigirl.com": get_sources_for_common,
            "cosplaytele.com": get_sources_for_common,
            "hotgirl.asia": get_sources_for_hotgirl_asia,
            "www.xasiat.com": get_for_xasiat,
            "4kup.net": get_sources_for_4kup,
            "buondua.com": get_sources_for_buondua,
            "erome.com": get_sources_for_erome,
            "www.erome.com": get_sources_for_erome,
            "es.erome.com": get_sources_for_erome,
            "notion": get_sources_for_notion,
            "new.pixibb.com": get_sources_for_pixibb,
            "sexy.pixibb.com": get_sources_for_pixibb,
            "ouo": ouo_bypass,
            "spacemiss.com": get_sources_for_spacemiss,
            "hentaiclub.net": get_sources_for_hentai_club,
            "www.hentaiclub.net": get_sources_for_hentai_club,
            "ugirls.pics": get_sources_for_ugirls,
            "xlust.org": get_sources_for_xlust,
            "mitaku.net": get_sources_for_mitaku,
            "hotgirlchina.com": get_sources_for_hotgirl_china,
            "pt.jrants.com": get_sources_for_jrant,
            "jrants.com": get_sources_for_jrant,
            "en.jrants.com": get_sources_for_jrant,
            "misskon.com": get_sources_for_misskon,
            "www.lovecos.net": get_sources_for_lovecos,
            "e-hentai.org": get_sources_for_ehentai,
            "fuligirl.top": get_sources_for_fuligirl,
            "youwu.lol": get_sources_for_fuligirl,
            "cosxuxi.club": get_sources_for_cosxuxi,
            "www.hotgirl2024.com": get_sources_for_hotgirl2024,
            "forum.lewdweb.net": get_sources_for_lewdweb,
            "nsfw247.to": get_sources_for_nsfw24,
            "asianviralhub.com": get_sources_for_asianviralhub,
            "www.sweetlicious.net": get_sources_for_sweetlicious,
            "xmissy.nl": get_sources_for_xmissy,
            "nudogram.com": get_sources_for_nudogram,
            "dvir.ru": get_sources_for_nudogram,
            "fapello.com": get_sources_for_fapello,
            "fapeza.com": get_sources_for_fapeza,
            "kemono.su": get_sources_for_kemono,
            "fapachi.com": get_sources_for_fapachi,
            "nudostar.tv": get_sources_for_nudostar,
            "thefappening.plus": get_sources_for_fappening,
            "www.xpics.me": get_sources_for_xpics,
            "xpics.me": get_sources_for_xpics,
            "fapomania.com": get_sources_for_fapomania,
            "fapello.pics": get_sources_for_fapello_pics,
            "fapello.to": get_sources_for_fapello_to,
            "hotleaks.tv": get_sources_for_hotleaks,
        }
        mapped_sources: defaultdict[str, list[str]] = defaultdict(list)

        for url in sources:
            entity: str = asyncio.run(get_entity([url]))
            mapped_sources[entity].append(url)

        if upload:
            asyncio.run(
                upload_folders_to_telegraph(
                    folder_name=final_dest,
                    limit=limit,
                    send_to_channel=send_to_telegram,
                    telegraph_client=telegraph_client,
                )
            )
        else:
            for source_entity in mapped_sources.keys():
                getter_images = getter_mapping.get(source_entity, get_sources_for_common)
                urls = mapped_sources[source_entity]
                asyncio.run(
                    getter_images(
                        sources=urls,
                        entity=source_entity,
                        telegraph_client=telegraph_client,
                        final_dest=final_dest,
                        save_to_telegraph=publish,
                        is_tag=is_tag,
                        limit=limit,
                        is_video_enabled=is_video_enabled,
                    )
                )
