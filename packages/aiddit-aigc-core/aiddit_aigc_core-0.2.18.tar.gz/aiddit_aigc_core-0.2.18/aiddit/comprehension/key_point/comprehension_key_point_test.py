from comprehension_key_point import analysis_key_point_v1, distinct_image_content
import json

note_path = "/image_article_comprehension/comprehension/note_data/account_烟熏账号_5a7497f24eacab31d58d556d/66fbd0ed000000002a030768.json"

note = json.load(open(note_path, 'r'))

distinct_images = distinct_image_content(note)
for index, i in enumerate(distinct_images):
    print(f"index = {index} , {i}")

ans = analysis_key_point_v1(note)

print(ans)

# print(f"{json.dumps(json.loads(ans), ensure_ascii=False, indent=4)}")
