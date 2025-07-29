import requests
import os
import tqdm
import logging

logger = logging.getLogger("crypticorn")


async def download_file(
    url: str, dest_path: str, show_progress_bars: bool = True
) -> str:
    """downloads a file and shows a progress bar. allow resuming a download"""
    file_size = 0
    req = requests.get(url, stream=True, timeout=600)
    req.raise_for_status()

    total_size = int(req.headers.get("content-length", 0))
    temp_path = dest_path + ".temp"

    if os.path.exists(dest_path):
        logger.info(f" file already exists: {dest_path}")
        file_size = os.stat(dest_path).st_size
        if file_size == total_size:
            return dest_path

    if os.path.exists(temp_path):
        file_size = os.stat(temp_path).st_size

        if file_size < total_size:
            # Download incomplete
            logger.info(f" resuming download")
            resume_header = {"Range": f"bytes={file_size}-"}
            req = requests.get(
                url,
                headers=resume_header,
                stream=True,
                verify=False,
                allow_redirects=True,
                timeout=600,
            )
        else:
            # Error, delete file and restart download
            logger.error(f" deleting file {dest_path} and restarting")
            os.remove(temp_path)
            file_size = 0
    else:
        # File does not exist, starting download
        logger.info(f" starting download")

    # write dataset to file and show progress bar
    pbar = tqdm.tqdm(
        total=total_size,
        unit="B",
        unit_scale=True,
        desc=dest_path,
        disable=not show_progress_bars,
    )
    # Update progress bar to reflect how much of the file is already downloaded
    pbar.update(file_size)
    with open(temp_path, "ab") as dest_file:
        for chunk in req.iter_content(1024):
            dest_file.write(chunk)
            pbar.update(1024)
    # move temp file to target destination
    os.replace(temp_path, dest_path)
    return dest_path
