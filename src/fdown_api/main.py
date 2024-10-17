import cloudscraper
import re
import random
import string
import os
import logging
import typing as t
from bs4 import BeautifulSoup
from dataclasses import dataclass
from pathlib import Path

try:
    from tqdm import tqdm
    from colorama import Fore

    cli_deps_installed = True
except ImportError:
    cli_deps_installed = False

logger = logging.getLogger(__name__)


@dataclass
class VideoLinks:
    """Urls to downloadable video
    sdlink : Normal video quality url
    hdlink : HD video quality url
    """

    title: t.Optional[str] = None
    sdlink: t.Optional[str] = None
    hdlink: t.Optional[str] = None
    cover_photo: t.Optional[str] = None
    description: t.Optional[str] = None
    duration: t.Optional[str] = None


class Fdown:
    """Download facebook videos"""

    def __init__(
        self,
        timeout: int = 20,
        proxies: dict[str, str] = {},
        cookies: dict[str, str] = {},
    ):
        """Initialize `Fdown`

        Args:
            timeout (optional) Http request timeout in seconds. Defaults to 20.
        """
        self.session = cloudscraper.create_scraper(
            browser={
                "browser": "firefox",
                "platform": "linux",
                "desktop": True,
            },
        )
        self.request_timeout = timeout

    def validate_url(self, url: str) -> str:
        """Check authenticity of video url

        Args:
            url (str)

        Returns:
            str
        """
        url_pattern = r"https://.+\.facebook\.com.+?mibextid=\w{16}"
        match = re.match(url_pattern, url)
        if match:
            return url
        else:
            raise ValueError(f"Invalid url passed - '{url}'")

    def _extract_video_quality_urls(self, contents: str) -> VideoLinks:
        """Extract links to download the video

        Args:
            contents (str): html contents of the page containing links

        Returns:
            VideoLinks: Links
        """
        soup = BeautifulSoup(contents, "html.parser")
        params: dict[str, str] = {}
        info_soup = soup.find("div", {"id": "result"})
        for target in info_soup.find_all("a", {"class": "btn btn-primary btn-sm"}):
            params[target.get("id")] = target.get("href")
        cover_photo_soup = soup.find("img", {"class": "lib-img-show"})
        if cover_photo_soup:
            params["cover_photo"] = cover_photo_soup.get("src")
        title_soup = info_soup.find("div", {"class": "lib-row lib-header"})
        if title_soup:
            params["title"] = title_soup.text.strip()
        for desc in info_soup.find_all("div", {"class": "lib-row lib-desc"}):
            splitted_text = desc.text.strip().split(" ")
            target = splitted_text[0][:-1]
            info = " ".join(splitted_text[1:])
            params[target.lower()] = info

        return VideoLinks(**params)

    def get_links(self, url: str) -> VideoLinks:
        """Get url to downloadable videos

        Args:
            (str): Link pointing to the targeted facebook video.

        Returns:
            VideoLinks: Link to normal and hd video quality.
        """
        video_post_url = self.validate_url(url)
        resp = self.session.post(
            "https://fdown.net/download.php",
            data={"URLz": video_post_url},
            timeout=self.request_timeout,
        )
        resp.raise_for_status()

        return self._extract_video_quality_urls(resp.text)

    def download_video(
        self,
        videolinks: VideoLinks,
        quality: t.Literal["normal", "hd"] = "hd",
        filename: str = None,
        dir: str = os.getcwd(),
        progress_bar=True,
        quiet: bool = False,
        chunk_size: int = 512,
        resume: bool = False,
    ):
        """Download and save the video in disk
        Args:
            videolinks (VideoLinks)
            quality (t.Literal['normal','hd']', optional): Video quality to be downloaded. Defaults to 'hd'.
            filename (str): Movie filename. Defaults to  None.
            dir (str, optional): Directory for saving the contents Defaults to current directory.
            progress_bar (bool, optional): Display download progress bar. Defaults to True.
            quiet (bool, optional): Not to stdout anything. Defaults to False.
            chunk_size (int, optional): Chunk_size for downloading files in KB. Defaults to 512.
            resume (bool, optional):  Resume the incomplete download. Defaults to False.

        Raises:
            FileExistsError:  Incase of `resume=True` but the download was complete
            Exception: _description_

        Returns:
            str: Path: Path where the downloaded video file has been saved to.
        """
        if not isinstance(videolinks, VideoLinks):
            raise ValueError(
                f"Videolink should be an instance of {VideoLinks} not {type(videolinks)}"
            )
        if filename is None:
            filename = "".join(random.sample(string.ascii_letters + string.digits, 16))
        if not filename.endswith(".mp4"):
            filename = filename + ".mp4"
        current_downloaded_size = 0
        current_downloaded_size_in_mb = 0
        save_to = Path(dir) / filename
        video_file_url = videolinks.hdlink if quality == "hd" else videolinks.sdlink

        if not video_file_url:
            raise ValueError(
                f"The video cannot be downloaded in that quality - {quality}"
            )

        def pop_range_in_session_headers():
            if self.session.headers.get("Range"):
                self.session.headers.pop("Range")

        if resume:
            assert os.path.exists(save_to), f"File not found in path - '{save_to}'"
            current_downloaded_size = os.path.getsize(save_to)
            # Set the headers to resume download from the last byte
            self.session.headers.update({"Range": f"bytes={current_downloaded_size}-"})
            current_downloaded_size_in_mb = round(
                current_downloaded_size / 1000000, 2
            )  # convert to mb

        default_content_length = 0

        resp = self.session.get(video_file_url, stream=True)

        size_in_bytes = int(resp.headers.get("content-length", default_content_length))
        if not size_in_bytes:
            if resume:
                raise FileExistsError(
                    f"Download completed for the file in path - '{save_to}'"
                )
            else:
                raise Exception(
                    f"Cannot download file of content-length {size_in_bytes} bytes"
                )

        if resume:
            assert (
                size_in_bytes != current_downloaded_size
            ), f"Download completed for the file in path - '{save_to}'"

        size_in_mb = round(size_in_bytes / 1000000, 2) + current_downloaded_size_in_mb
        chunk_size_in_bytes = chunk_size * 1024

        saving_mode = "ab" if resume else "wb"
        if progress_bar:
            if not cli_deps_installed:
                raise Exception(
                    "CLI dependencies are missing reinstall with cli extras i.e "
                    "'pip install fdown-api[cli]'"
                )
            with tqdm(
                total=size_in_bytes + current_downloaded_size,
                bar_format="%s%d MB %s{bar} %s{l_bar}%s"
                % (Fore.GREEN, size_in_mb, Fore.CYAN, Fore.YELLOW, Fore.RESET),
                initial=current_downloaded_size,
            ) as p_bar:
                # p_bar.update(current_downloaded_size)
                with open(save_to, saving_mode) as fh:
                    for chunks in resp.iter_content(chunk_size=chunk_size_in_bytes):
                        fh.write(chunks)
                        p_bar.update(chunk_size_in_bytes)
                pop_range_in_session_headers()
                return save_to
        else:
            with open(save_to, saving_mode) as fh:
                for chunks in resp.iter_content(chunk_size=chunk_size_in_bytes):
                    fh.write(chunks)

            logger.info(f"{filename} - {size_in_mb}MB ✅")
            pop_range_in_session_headers()
            return save_to
