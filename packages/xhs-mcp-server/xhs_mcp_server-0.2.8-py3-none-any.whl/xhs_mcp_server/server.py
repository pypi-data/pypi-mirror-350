import concurrent
import os
import tempfile
import time
import requests

from mcp.server import FastMCP
from mcp.types import TextContent

from .write_xiaohongshu import XiaohongshuPoster

mcp = FastMCP("xhs")
phone = os.getenv("phone", "")
path= os.getenv("json_path","/Users/bruce/")
slow_mode=os.getenv("slow_mode","False").lower() == "true"
def login():
    poster = XiaohongshuPoster(path)
    poster.login(phone)
    time.sleep(1)
    poster.close()

def download_image(url):
    local_filename = url.split('/')[-1]
    temp_dir = tempfile.gettempdir()

    local_path = os.path.join(temp_dir, local_filename)  # 假设缓存地址为/tmp
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_path

def download_images_parallel(urls):
    """
    并行下载图片到本地缓存地址
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(download_image, urls))
    return results

@mcp.tool()
def create_note(title: str, content: str, images: list) -> list[TextContent]:
    """Create a note (post) to xiaohongshu (rednote) with title, description, and images

    Args:
        title: the title of the note (post), which should not exceed 20 words
        content: the description of the note (post).
        images: the list of image paths or URLs to be included in the note (post)
    """
    poster = XiaohongshuPoster(path)
    #poster.login(phone)
    res = ""
    try:
        if len(images)>0 and images[0].startswith("http"):
            # 使用并行下载图片
            local_images = download_images_parallel(images)
        else:
            local_images = images
        code,info=poster.login_to_publish(title, content, local_images,slow_mode)
        poster.close()
        res = info
    except Exception as e:
        res = "error:" + str(e)

    return [TextContent(type="text", text=res)]


@mcp.tool()
def create_video_note(title: str, content: str, videos: list) -> list[TextContent]:
    """Create a note (post) to xiaohongshu (rednote) with title, description, and videos

    Args:
        title: the title of the note (post), which should not exceed 20 words
        content: the description of the note (post).
        videos: the list of video paths or URLs to be included in the note (post)
    """
    poster = XiaohongshuPoster(path)
    #poster.login(phone)
    res = ""
    try:
        # 使用并行下载视频
        if len(videos)>0 and videos[0].startswith("http"):
            # 使用并行下载图片
            local_videos = download_images_parallel(videos)
        else:
            local_videos = videos


        #local_videos = download_images_parallel(videos)
        
        code,info=poster.login_to_publish_video(title, content, local_videos,slow_mode)
        poster.close()
        res = info
    except Exception as e:
        res = "error:" + str(e)

    return [TextContent(type="text", text=res)]

def main():
    mcp.run()

if __name__ == "__main__":
    main()