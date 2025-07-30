import os.path
import traceback
import json
from tqdm import tqdm
from traceback import print_exc
from concurrent.futures import ThreadPoolExecutor

from aiddit.comprehension.key_point.comprehension_key_point import analysis_key_point_v1, \
    analysis_xuanti_v7
from aiddit.comprehension.script0221 import script_compehension
from tenacity import retry, stop_after_attempt, wait_fixed

def save(r, path):
    with open(path, 'w') as f:
        json.dump(r, f, ensure_ascii=False, indent=4)


@retry(stop=stop_after_attempt(5), wait=wait_fixed(5))
def process_note_path(input_note_path, output_dir):
    if os.path.exists(input_note_path) is False:
        print(f"file {input_note_path} not exists")
        return

    input_note_info = json.load(open(input_note_path, 'r'))

    if os.path.exists(output_dir) is False:
        try:
            os.makedirs(output_dir)
        except Exception as e:
            print(f"create dir error {output_dir} , {str(e)}")

    script_result_path = os.path.join(output_dir, os.path.basename(input_note_path))

    print(f"start .... script_result_path={script_result_path}")

    if input_note_info.get('images') is None or len(input_note_info.get('images')) == 0:
        print(f"script_result_path={script_result_path} no images")
        return

    if os.path.exists(script_result_path) is False:
        script_result = {
            "note_info": input_note_info
        }
        save(script_result, script_result_path)
    else:
        script_result = json.load(open(script_result_path, 'r'))

    # 理解选题 & 文本
    if script_result.get('xuanti_result') is None:
        print("xuanti comprehension start")
        xuanti_ans = None
        try:
            xuanti_ans = analysis_xuanti_v7(input_note_info, img_num=100)
            xuanti_result = json.loads(xuanti_ans)
            script_result['xuanti_result'] = xuanti_result
            save(script_result, script_result_path)
        except Exception as e:
            print(f"analysis xuanti error {script_result_path}, \n{xuanti_ans} \n{str(e)}")
            traceback.print_exc()
    else:
        print(f"{script_result_path} xuanti  already exists")

    # 理解整体要点 & 整体材料
    print(f"{os.path.basename(input_note_path)} keypoint is list?  {isinstance(script_result.get('key_point'), list)}")
    if script_result.get("key_point") is None or isinstance(script_result.get("key_point"), list) is False:
        key_point_ans = None
        try:
            key_point_ans = analysis_key_point_v1(input_note_info)
            key_point = json.loads(key_point_ans)
            script_result["key_point"] = key_point
            save(script_result, script_result_path)
        except Exception as e:
            print(f"analysis key point error {script_result_path}, \n{key_point_ans}")
            print_exc()
    else:
        print(f"{script_result_path} key point already exists")


    if script_result.get("script") is None:
        try:
            script_result["script"] = script_compehension.note_script(input_note_info)
            save(script_result, script_result_path)
        except Exception as e:
            print(f"generate script error {script_result_path} , {str(e)}")
            print_exc()

    # if script_result.get("script") is None or script_result.get("script").get("图片", {}).get("图片描述") is None:
    #     try:
    #         script_result["script"] = script_compehension.process_note(input_note_info)
    #         save(script_result, script_result_path)
    #     except Exception as e:
    #         print(f"generate script error {script_result_path} , {str(e)}")
    #         print_exc()
    # else:
    #     print(f"{script_result_path} script exist")


def check_note_process_finished(input_note_path, output_dir):
    script_result_path = os.path.join(output_dir, os.path.basename(input_note_path))
    if os.path.exists(script_result_path) is False:
        return False

    script_result = json.load(open(script_result_path, 'r'))

    if script_result.get('xuanti_result') is None:
        return False

    if script_result.get("key_point") is None or isinstance(script_result.get("key_point"), list) is False:
        return False

    if script_result.get("script") is None:
        return False

    return True


def note_dir_process():
    dir_path = "/image_article_comprehension/aiddit/comprehension/note_data/account_20250110_摸鱼阿希_617a100c000000001f03f0b9"
    list_dir = os.listdir(dir_path)

    output_dir = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/comprehension/renshe/account_note_comprehension/" + \
                 os.path.basename(dir_path).split("_")[-3] + "_" + os.path.basename(dir_path).split("_")[-2]

    target_note_dir = [os.path.join(dir_path, i) for i in list_dir][:30]
    with ThreadPoolExecutor(max_workers=5) as executor:
        list(tqdm(executor.map(lambda note_path: process_note_path(note_path, output_dir), target_note_dir),
                  total=len(target_note_dir), desc="帖子所有理解"))
    pass


if __name__ == "__main__":
    # note_dir_process()

    # note_path = "/Users/nieqi/Documents/workspace/python/image_article_comprehension/comprehension/note_data/account_20250110_摸鱼阿希_617a100c000000001f03f0b9/66d1a832000000001d01a69d.json"
    #
    # note_info = json.load(open(note_path, 'r'))
    #
    # ans = analysis_xuanti_v7(note_info, img_num=100)
    #
    # print(ans)

    # ans = prompt_note_script_0125(note_info)
    # print(ans)

    # input_note_info = {
    #     "channel_content_id": "675c24eb0000000004029a5a",
    #     "link": "https://www.xiaohongshu.com/explore/675c24eb0000000004029a5a?xsec_token=ABhHN5SYB6pOpMagaTrFhe7g6DjIi_8QxqTw2ZyNGa2Dc=",
    #     "xsec_token": "ABhHN5SYB6pOpMagaTrFhe7g6DjIi_8QxqTw2ZyNGa2Dc=",
    #     "comment_count": 10,
    #     "images": [
    #         "http://res.cybertogether.net/crawler/image/00f53801c118b8c6bcd316522fee4aec.webp",
    #         "http://res.cybertogether.net/crawler/image/00f53801c118b8c6bcd316522fee4aec.webp",
    #         "http://res.cybertogether.net/crawler/image/3a066ea268aa73d5b2c0cac0f8af5ccc.webp",
    #         "http://res.cybertogether.net/crawler/image/1b11f762e167312edf024dcf6a2d1acf.webp",
    #         "http://res.cybertogether.net/crawler/image/b4b305839474f3d807c0f3f59c562d6c.webp",
    #         "http://res.cybertogether.net/crawler/image/e721b3b583ab04a8e64fbcf38a2108a3.webp",
    #         "http://res.cybertogether.net/crawler/image/c9b46aa78e5ca40dd36aa746fdbc0c3e.webp",
    #         "http://res.cybertogether.net/crawler/image/d1bc873242ce627c61f1a07298884215.webp",
    #         "http://res.cybertogether.net/crawler/image/7af9ea4025642a5c53ec8a5c7b673f31.webp",
    #         "http://res.cybertogether.net/crawler/image/b71cc3986303a96af25fc250c34f4baa.webp",
    #         "http://res.cybertogether.net/crawler/image/47355b0c66e127ff440c0db43852deb7.webp",
    #         "http://res.cybertogether.net/crawler/image/5cda39b73d85d96205532adf8dd2f825.webp",
    #         "http://res.cybertogether.net/crawler/image/048582833b3c7bf58e0dc1f925fd2c5e.webp",
    #         "http://res.cybertogether.net/crawler/image/49c0ac58c7028d9f5aa9dceca256087c.webp"
    #     ],
    #     "like_count": 10,
    #     "body_text": "-\n每当我尝试给海加上一些情绪化的词\n这片海就仿佛不再被大众和尘世所有了\n有情绪的不是海\n是人类\n\t\n被添加了这些词的海也就不再是它本身\n而是我希望看见的\n是我想象出来的海\n\t\n1. 早八起来骑车，我天呢\n2. 辛苦我的腿了\n3. 人做饭怎么能这么难吃\n4. 晚安，真的想睡72小时，但是人不吃饭会被饿死\n5. 🍫\n6. 草莓酸奶碗🍓\n7. 🌄\n8. 有情绪的不是海，是人类\n9. 咖啡补给+1☕️\n10. 橘色时刻🟠\n\t\n#生活美学#咖啡 #生活 #美食 #健身#运动#日常生活里的快乐瞬间 #plog #我的咖啡日记#拍照",
    #     "title": "Intp‘s｜或许海也只是人类的情绪载体🌊",
    #     "collect_count": 10
    # }

    # input_note_info = {
    #     "channel_content_id": "64d4222b000000000800c5cd",
    #     "link": "https://www.xiaohongshu.com/explore/64d4222b000000000800c5cd?xsec_token=ABtQ933H_5tFGK07Yi_V4K6kZw6xaSov-aswKc3c_ReHA=",
    #     "xsec_token": "ABtQ933H_5tFGK07Yi_V4K6kZw6xaSov-aswKc3c_ReHA=",
    #     "comment_count": 10,
    #     "images": [
    #         "http://res.cybertogether.net/crawler/image/17283d628c66dc76de84b1ec9ee823e9.webp",
    #         "http://res.cybertogether.net/crawler/image/17283d628c66dc76de84b1ec9ee823e9.webp",
    #         "http://res.cybertogether.net/crawler/image/c00a0e3f47ced1415da2a5ce4c414713.webp",
    #         "http://res.cybertogether.net/crawler/image/bd36d3fa797bbc86a72c773241470c3c.webp",
    #         "http://res.cybertogether.net/crawler/image/84614d1fe77522e96227f8ae057d26b4.webp",
    #         "http://res.cybertogether.net/crawler/image/5aba798829d83f59400e095eca3172a8.webp",
    #         "http://res.cybertogether.net/crawler/image/47d92e812dcad36cb4a467aeadec3b9d.webp",
    #         "http://res.cybertogether.net/crawler/image/9c43c5835bdabe6e21f0fdfd23da3663.webp",
    #         "http://res.cybertogether.net/crawler/image/23afc8d2da7b639559c48478fb5c641c.webp"
    #     ],
    #     "like_count": 10000,
    #     "body_text": "➡️空船效应\n一个人在乘船渡河的时候，前面有一只船正要撞过来。这个人喊了好几声，但是前面的船没有回应。见状这个人十分生气，开始破口大骂前方船上的人。后来他发现撞上来的竟然是一架空船，于是刚刚怒气冲冲的人怒火一下就消失得无影无踪了。\n\t\n这个故事来自于庄子的《山木》，是空船效应的典例。从这个故事中可以反映出其实日常生活中发生在你身上的事情，你的情绪10％取决于这件事情，而90％取决于你的心态。\n\t\n➡️空船效应成因\n\"空船效应”本质上是心态问题。当你在专注地做一件事情时，如果有人从背后打扰你，你不免会感到十分气愤。但当你回头发现他是个孩子，你可能会想“算了，他还是个孩子”，就没那么生气了。\n\t\n许多人在面对令人不悦的事情时，往往会抱怨：“怎么我又这么倒霉？这种事情怎么总是发生在我的身上？”其实越陷入这种想法心情越容易变的糟糕。\n\t\n能帮助你的只有自己，而不是他人。一遇到不顺心的事情就火冒三丈的人往往太以自我为中心，不妨换个角度思考，保持豁达乐观的心态，你会发现很多问题都是小问题。\n\t\n➡️空船效应摆脱\n1.转变心态\n当事情已经发生，那么我们无法改变，但是我们的心态是可以改变的。有些人在感染新冠后情绪低落、厌恶他人，这样反而不利于痊愈。不如换个角度想，如今感染的几率很高，既然这样不如既来之则安之，熬过了这几天又是一个全新的自己。\n\t\n2.不以自我为中心\n可以尝试用更加谦虚、平和的心态看待事情，不要过度关注外界对自己的不良影响，当没有什么事情能够轻易影响你的心态时，那可以很好的避免许多不必要的争吵，修炼更大的格局。\n\t\n3.学会接受\n我们都是在迷雾中前行，谁也不知道下一秒会发生什么事情。既然无法预测的话，不如去接受已经发生的事实，气愤并不能改变事实，还可能会让自己陷入不好的处境。接受已经发生的一切，并想办法解决它，我们才能走的更快更远。\n\t\n➡️用不同的心态看待事物，也许会看到不一样的风景\n\t\n#学点儿心理学 #知识点总结 #心理学效应 #心理学小知识 #知识科普 #干货分享 #空船效应 #空船心态 #思维 #成长\n@小红书成长助手 @小红书创作学院",
    #     "title": "每天分享一个心理学知识｜空船效应",
    #     "collect_count": 10000
    # }
    # #
    # ans = note_script_prompt.prompt_note_script_0220(input_note_info)
    # print(ans)
    # pass

    # ans = note_script_prompt.image_description(
    #     "http://res.cybertogether.net/crawler/image/00f53801c118b8c6bcd316522fee4aec.webp")
    # print(ans)


    note_path = "/image_article_comprehension/xhs/result/67a73167000000001701e758.json"

    result = analysis_key_point_v1(json.load(open(note_path, 'r')))

    print(result)