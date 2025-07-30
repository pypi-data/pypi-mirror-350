import requests
import mimetypes
import os

proxy = "http://dpaytent:11gizg4f@36.139.119.113:16816"

def proxy_download_video(url: str, local_path: str, proxy: str = None):
    proxies = {'http': proxy, 'https': proxy} if proxy else None
    response = requests.get(url, stream=True, proxies=proxies)
    response.raise_for_status()
    content_type = response.headers.get('Content-Type')
    extension = mimetypes.guess_extension(content_type)
    if extension:
        if "." not in local_path:
            local_path += extension
        if os.path.exists(local_path):
            # print(f"url  {url} exists in {local_path}")
            return local_path
    with open(local_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    return local_path


# 使用示例
if __name__ == "__main__":
    video_url = "ttp://sns-video-alos.xhscdn.com/stream/79/110/258/01e8287d146796714f03700196de2dff0c_258.mp4"
    save_path = "downloaded_video.mp4"
    proxy_download_video(video_url, save_path, proxy=proxy)
