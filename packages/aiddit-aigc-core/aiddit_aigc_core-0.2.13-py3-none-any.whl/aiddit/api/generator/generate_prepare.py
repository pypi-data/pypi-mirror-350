from aiddit.api.generator.prompts import gnereate_prepare_prompt
from aiddit.model.google_genai import GenaiConversationMessage, GenaiMessagePart, MessageType
from aiddit.api.xhs_api import _get_xhs_account_info, _get_xhs_account_note_list, _get_note_detail_by_id
import aiddit.model.google_genai as google_genai
import aiddit.utils as utils


def prepare(xhs_user_id: str):
    account_info = _get_xhs_account_info(xhs_user_id)
    account_history_note_path = _get_xhs_account_note_list(xhs_user_id)

    model = google_genai.MODEL_GEMINI_2_5_FLASH
    history_notes = utils.load_from_json_dir(account_history_note_path)

    history_messages = []

    for index, h_note in enumerate(history_notes):
        # 历史参考帖子
        h_note_images = utils.remove_duplicates(h_note.get("images"))
        h_note_images = [utils.oss_resize_image(i) for i in h_note_images]
        history_note_prompt = gnereate_prepare_prompt.NOTE_PROVIDER_PROMPT.format(
            index=index + 1,
            title=h_note.get("title"),
            body_text=h_note.get("body_text"))
        history_note_conversation_user_message = google_genai.GenaiConversationMessage.text_and_images(
            history_note_prompt, h_note_images)
        history_messages.append(history_note_conversation_user_message)

    prepare_prompt = gnereate_prepare_prompt.PROMPT.format(account_name=account_info.get("account_name"))

    prepare_conversation_user_message = GenaiConversationMessage.one("user", prepare_prompt)

    script_ans_conversation_model_message = google_genai.google_genai_output_images_and_text(
        prepare_conversation_user_message,
        model=model,
        history_messages=history_messages)
    ans_content = script_ans_conversation_model_message.content[0].value

    return ans_content

def material_comprehension(script):
    model = google_genai.MODEL_GEMINI_2_5_PRO_EXPT_0325

    # 提取材料
    material_extract_prompt = gnereate_prepare_prompt.MATERIAL_EXTRACT_PROMPT.format(script=script)
    material_extract__conversation_user_message = GenaiConversationMessage.one("user", material_extract_prompt)
    script_ans_conversation_model_message = google_genai.google_genai_output_images_and_text(
        material_extract__conversation_user_message,
        model=model,
        response_mime_type="application/json",
        history_messages=[])

    material_extract_ans_content = script_ans_conversation_model_message.content[0].value
    material_extract_data = utils.try_remove_markdown_tag_and_to_json(material_extract_ans_content)

    # 材料理解





if __name__ == "__main__":
    # prepare("5bb61a0a59b9bf0001e9a986")
    input_script = """
{
  "脚本": {
    "图集描述": [
      "第一张图为封面：一个经过精心改造的卫生间全景，整体色调温馨。墙壁是浅米白色，地面铺着浅色防滑地砖。洗手台区域，<<白色斗柜1>>般的台面上摆放着一个淡紫色的陶瓷牙刷杯和紫色的洗手液瓶，上方镜子边缘有柔和的LED灯带，类似<<斗柜与台灯1>>的照明氛围。浴缸/淋浴区旁边，挂着一条薰衣草紫色的浴巾，旁边的置物架上放着几瓶包装精美的沐浴用品，其中有紫色瓶身的。<<阿橘代表图>>（猫咪）正好奇地蹲在紫色的地垫（颜色后期调整或新购）上，仰头看着镜头，可参考<<猫咪在地毯上1>>的姿态，地垫材质可参考<<米色地毯1>>。窗户（如果有）透进柔和的自然光或室内灯光营造出温暖氛围，如同<<卧室夜间氛围1>>中的柔光。",
      "改造前的卫生间全景：一个普通、略显陈旧的卫生间，墙面可能是简单的白瓷砖，灯光偏白且亮度一般。可参考<<改造前房间状态1>>的整体感觉，但场景替换为卫生间，表现出未改造前的基础和略显杂乱的状态。",
      "改造前洗手台区域特写：近距离拍摄改造前的洗手台，台面上可能摆放着颜色不统一的洗漱用品，水龙头略显老旧，镜子普通无特色，整体感觉平淡无奇。可参考<<改造前房间状态1>>中家具的原始状态，聚焦于卫生间的洗手台区域。",
      "改造细节：装修师傅正在给一面小墙壁（或某个区域）涂刷淡紫色的防水乳胶漆，或者正在安装一个带有紫色元素的置物架。",
      "改造细节：特写一张新购入的紫色元素的浴室用品，如一套紫色的毛巾、紫色的香薰瓶、或者紫色的收纳盒，旁边散落着一些安装工具或包装。",
      "改造后的洗手台区域：明亮柔和的灯光下，类似<<白色床头柜1>>的白色陶瓷洗手台上整齐摆放着淡紫色的牙刷杯、同色系洗手液瓶，旁边点缀一小盆绿植。镜子带有柔光灯圈，映出整洁的台面，光线氛围参考<<床头柜与台灯1>>。墙上可能挂着一个精致的紫色小挂件或装饰画。",
      "改造后的淋浴/浴缸区：淋浴区或浴缸旁，叠放着柔软的薰衣草紫色和白色毛巾，一个精致的置物架上摆放着几瓶设计感十足的沐浴露、洗发水（部分为紫色包装）。墙壁上贴着几块带有淡雅紫色花纹的防水贴纸或挂着紫色的浴帘一角。整体氛围可借鉴<<窗边卧榻1>>的舒适感，但场景为浴室。",
      "紫色细节特写：一个充满设计感的角落，比如一个紫色的香薰蜡烛正在燃烧，散发着柔和光芒，旁边放着一本摊开的<<阅读的书1>>和一杯水，营造放松惬意的氛围。背景是新改造的卫生间墙面或浴缸边缘，灯光可参考<<床头氛围灯1>>的柔和感。",
      "收纳巧思展示：打开浴室柜或展示墙面置物架，内部物品通过紫色的收纳筐或隔板分类整理得井井有条，如化妆品、护肤品或清洁用品，展示了小空间的高效利用。收纳的整洁感可参考<<书桌收纳细节1>>的桌面或<<斗柜收纳细节1>>的开放架。",
      "猫咪与新空间互动：<<阿橘代表图>>（猫咪）正舒适地趴在新铺的淡紫色防滑地垫上（参考<<猫咪在地毯上1>>的姿态，地垫为紫色），或者用爪子轻轻拨弄着浴缸边垂下的紫色毛巾一角，眼神慵懒可爱，可参考<<猫咪在床上1>>的放松状态。",
      "氛围感夜间模式：调暗主灯，只开启镜前灯或香薰灯等辅助光源，整个卫生间沉浸在暖黄色与淡紫色的柔和光影中，水汽氤氲，浴缸里放满了热水，水面漂浮着花瓣或浴球，营造出极致治愈的泡澡氛围。灯光氛围可参考<<卧室夜间氛围1>>或<<床头氛围灯1>>的温馨感。",
      "博主视角体验：从博主进入卫生间的视角拍摄，开门瞬间看到焕然一新的紫色治愈系空间，前方是温馨的灯光和整洁的布置，如<<房间入口视角1>>所呈现的进入房间的视野。左下角或右下角露出博主穿着舒适家居服的脚或手的一部分（参考<<博主视角脚部1>>的脚部出镜），传达出满足和喜悦的心情。"
    ],
    "图集材料": [
      {
        "材料名": "阿橘代表图",
        "材料类型": "主体",
        "材料描述": "一只棕色虎斑猫，毛发蓬松，面部清晰，眼神略显犀利地看着镜头，趴在床上，背景是深蓝色和格纹床单。",
        "材料图片": "http://res.cybertogether.net/crawler/image/5be7d74a7abdaeec8c2b70d638b470fc.webp"
      },
      {
        "材料名": "改造前房间状态1",
        "材料类型": "场景",
        "材料描述": "一个空旷的卧室，尚未布置。房间中央放置着一个只有床垫和蓝色床单的浅色木质床架，床头板简约。左侧有一个床头柜。大窗户前是灰色窗帘，地板是木纹地板。房间整体显得空荡和原始。",
        "材料图片": "http://res.cybertogether.net/crawler/image/74d9ef9d1090d98cae2384c643148b6f.webp"
      },
      {
        "材料名": "斗柜与台灯1",
        "材料类型": "物品组合",
        "材料描述": "一个白色六斗柜，柜面上摆放着一个亮着暖黄色光的蘑菇造型台灯、一个相框、一些小摆件和收纳盒。斗柜旁的墙上贴有黑白艺术画和照片，右侧有一个白色沙发和落地灯。",
        "材料图片": "http://res.cybertogether.net/crawler/image/1454f74f96be7b3ab09d4382aca9182f.webp"
      },
      {
        "材料名": "床头柜与台灯1",
        "材料类型": "物品组合",
        "材料描述": "一个白色的三层抽屉床头柜，柜面上放置着一个亮着暖黄色光的球形小台灯和一个相框。床头柜旁是带有格纹床品的床和一面大镜子的一角。",
        "材料图片": "http://res.cybertogether.net/crawler/image/61d13e883def33f838fa6d4cc34f474f.webp"
      },
      {
        "材料名": "床头柜与台灯2",
        "材料类型": "物品组合",
        "材料描述": "一个白色的三层抽屉床头柜，柜面上放置着一个亮着暖黄色光的球形小台灯、一本闭合的书。一只棕色虎斑猫的一部分身体（尾巴和后腿）出现在床头柜旁的米色地毯上。床品是浅蓝色和白色。",
        "材料图片": "http://res.cybertogether.net/crawler/image/71706a2247d93977b64fb3df435fe831.jpeg"
      },
      {
        "材料名": "阅读的书1",
        "材料类型": "物品",
        "材料描述": "一只手拿着一本摊开的书，书页上有文字和少量插画。背景是浅色的床单和一个灰色毛绒象玩偶的头部。",
        "材料图片": "http://res.cybertogether.net/crawler/image/d6b49380e93329ee796853025ad14cd3.jpeg"
      },
      {
        "材料名": "书桌收纳细节1",
        "材料类型": "场景",
        "材料描述": "一张白色书桌，桌面上放着一台笔记本电脑和一个外接显示器，显示器后方有一个白色的洞洞板，上面挂着耳机和一些小物件。书桌右侧有盆栽和投影仪。整体布局整洁有序。",
        "材料图片": "http://res.cybertogether.net/crawler/image/ac46a4f18dcb08450702989ae3a5cf7c.webp"
      },
      {
        "材料名": "斗柜收纳细节1",
        "材料类型": "场景",
        "材料描述": "从床的视角看去，房间一角有一个白色斗柜，上方是一个棕色开放式置物架，架子上放着各种物品。旁边是一个简易衣架，挂着几件衣服。整体展示了房间的收纳情况。",
        "材料图片": "http://res.cybertogether.net/crawler/image/45caf3928292d22fba8eff4de6d2af9f.webp"
      },
      {
        "材料名": "猫咪在地毯上1",
        "材料类型": "主体",
        "材料描述": "一只棕色虎斑猫舒适地躺在床边的米色编织地毯上，一半身体在床底下。前景是一只穿着米白色家居裤和袜子的脚。灯光柔和。",
        "材料图片": "http://res.cybertogether.net/crawler/image/604108d737df07b57d5243652e29560f.jpeg"
      },
      {
        "材料名": "猫咪在床上1",
        "材料类型": "主体",
        "材料描述": "一只棕色虎斑猫趴在床上，床品是多色块拼接图案。床头木板上摆放着多个毛绒玩偶，墙上挂着日历海报。",
        "材料图片": "http://res.cybertogether.net/crawler/image/ddffafe888b4c2d158def72f8d7567f7.webp"
      },
      {
        "材料名": "床头氛围灯1",
        "材料类型": "氛围",
        "材料描述": "床头特写，一个白色三层抽屉床头柜上放着一个亮着暖光的球形小台灯，旁边有一个泰迪熊玩偶。床品为格纹和纯色拼接。墙上挂着日历海报，床头板上有其他毛绒玩偶。",
        "材料图片": "http://res.cybertogether.net/crawler/image/9bb515887af5fad0996210e3dbe15226.webp"
      },
      {
        "材料名": "卧室夜间氛围1",
        "材料类型": "氛围",
        "材料描述": "夜晚的卧室，整体光线偏暗但温馨。床铺整洁，床头柜上的小台灯亮着。一只猫躺在床边的地毯上。窗户有百叶窗，窗外是城市夜景。房间内有立式镜子和衣物。",
        "材料图片": "http://res.cybertogether.net/crawler/image/d54b3fa3116f81ebedc5cc156fce66ad.jpeg"
      },
      {
        "材料名": "博主视角脚部1",
        "材料类型": "视角",
        "材料描述": "从床上俯拍的视角，前景是盖着米白色毯子的腿和穿着蓝色条纹睡裤露出的双脚，脚踩在窗边沙发前的棕色编织地毯上。沙发上放着熊猫图案的毯子，窗外是城市景色。",
        "材料图片": "http://res.cybertogether.net/crawler/image/edee970aa23176da1fe5a8f319aa8d77.webp"
      },
      {
        "材料名": "房间入口视角1",
        "材料类型": "场景",
        "材料描述": "从房间门口或玄关处看向卧室内部。可以看到床铺，床尾的猫咪，床边的地毯和床头柜。右侧有大窗户和窗台卧榻。左侧是立式全身镜。",
        "材料图片": "http://res.cybertogether.net/crawler/image/2215407375de995797096735594cd6c3.webp"
      },
      {
        "材料名": "床头玩偶区1",
        "材料类型": "物品组合",
        "材料描述": "床头木质床板上沿摆放着一排毛绒玩偶，包括两个泰迪熊、一个企鹅、一个牛油果和一个猩猩玩偶。墙上贴着一张插画风格的日历。",
        "材料图片": "http://res.cybertogether.net/crawler/image/ddffafe888b4c2d158def72f8d7567f7.webp"
      },
      {
        "材料名": "白色床头柜1",
        "材料类型": "物品",
        "材料描述": "一个宜家马尔姆款式的白色三层抽屉床头柜，设计简约现代。",
        "材料图片": "http://res.cybertogether.net/crawler/image/61d13e883def33f838fa6d4cc34f474f.webp"
      },
      {
        "材料名": "白色斗柜1",
        "材料类型": "物品",
        "材料描述": "一个宜家马尔姆款式的白色六斗柜，柜面宽敞，设计简约现代。位于床的一侧，上面摆放了灯具和装饰品。",
        "材料图片": "http://res.cybertogether.net/crawler/image/e35bb036eefea88cb97936f7263f75a9.webp"
      },
      {
        "材料名": "窗边卧榻1",
        "材料类型": "场景元素",
        "材料描述": "靠窗设置的长条形卧榻，铺有米白色垫子，光线明亮，可供休憩观景。",
        "材料图片": "http://res.cybertogether.net/crawler/image/2215407375de995797096735594cd6c3.webp"
      },
      {
        "材料名": "米色地毯1",
        "材料类型": "物品",
        "材料描述": "铺在床边木地板上的长方形米色编织地毯，质感自然，增加了空间的温馨感。",
        "材料图片": "http://res.cybertogether.net/crawler/image/2215407375de995797096735594cd6c3.webp"
      },
      {
        "材料名": "木质床架1",
        "材料类型": "物品",
        "材料描述": "浅木色的简约床架，床头板也为同色木质，风格自然清新。",
        "材料图片": "http://res.cybertogether.net/crawler/image/2215407375de995797096735594cd6c3.webp"
      }
    ]
  },
  "正文": "终于对卫生间下手啦！一直想拥有一个超级治愈的洗浴空间，这次加入了超爱的紫色元素，整个氛围都温柔起来了～每天最期待的就是结束忙碌后，在属于自己的小天地里泡个舒服的热水澡，点上香薰，被暖暖的灯光和淡淡的紫色包围，感觉一天的疲惫都被洗掉啦！独居的快乐就是可以把每个角落都打造成自己喜欢的样子，姐妹们也快动手试试吧！#卫生间改造[话题]# #独居女孩的日常[话题]# #紫色系[话题]# #治愈系空间[话题]# #浴室好物[话题]# #我的私密空间[话题]# #提升幸福感好物[话题]# #沉浸式洗澡[话题]# #一人居[话题]# #我的小家[话题]#",
  "标题": "浴室大变身💜独居女孩的紫色治愈角落，谁能不爱！",
  "选题": "独居女孩的卫生间改造，紫色细节让洗澡更治愈选题的详细说明：这个选题结合了博主\"阿橘的小窝\"一贯的独居女孩人设和居住空间改造主题，同时融入了刺激源中紫色卫生间的设计元素。选题聚焦于如何通过独特的紫色元素打造出一个既实用又充满情调的洗浴空间，与博主经常分享的\"洗澡时刻\"（如\"洗完澡才8点，谁懂！\"）紧密关联。通过这个选题，博主可以展示卫生间这个私密空间的改造过程和成果，分享如何让独居生活的每个空间都变得温馨舒适，同时保持博主一贯的温柔、治愈的内容风格。选题创作中的关键点：1. 保持独居女孩的人设核心：延续博主一直以来的独居女生人设，强调\"自己的空间按自己喜好装饰\"的独立生活态度2. 融入改造元素：与博主历史发布的居家改造类笔记相呼应，展示空间改造前后的对比和细节处理3. 突出紫色主题：从刺激源中汲取紫色卫生间的设计灵感，但以博主自己的风格重新演绎4. 结合\"洗澡时刻\"：巧妙连接博主经常分享的洗澡后的舒适时刻，强化情感共鸣5. 强调治愈感：通过色彩、灯光等元素营造治愈氛围，体现博主一贯的温馨、舒适内容风格"
}   
"""

    material_comprehension(input_script)
    pass
