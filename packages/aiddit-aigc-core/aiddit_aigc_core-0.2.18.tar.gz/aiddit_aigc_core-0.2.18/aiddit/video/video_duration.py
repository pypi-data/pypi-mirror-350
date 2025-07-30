import os
import json
import ffmpeg
import aiddit.utils as utils
from tqdm import tqdm


def get_video_duration(video_url):
    try:
        probe = ffmpeg.probe(video_url)
        duration = float(probe['format']['duration'])
        return duration
    except Exception as e:
        print(f"Error processing video {video_url}: {e}")
        return None


def process_json_files(folder_path):
    for filename in tqdm(os.listdir(folder_path)):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                video_url = data.get('video_url')
                if video_url:
                    if data.get("duration_seconds") is not None:
                        duration = data["duration_seconds"]
                    else:
                        duration = get_video_duration(video_url)
                        data["duration_seconds"] = duration
                        utils.save(data, file_path)
                    print(f"Video {data['channel_content_id']} URL: {video_url}, Duration: {duration} seconds")


folder_path = '/image_article_comprehension/aiddit/video/data/reference_note/抖音热榜0212'
process_json_files(folder_path)
