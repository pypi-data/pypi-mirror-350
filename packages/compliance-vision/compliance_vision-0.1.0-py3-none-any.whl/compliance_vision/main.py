from openai import OpenAI
import os
import base64

from openai.types.chat import ChatCompletionSystemMessageParam


#  base 64 编码格式
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def get_response(image_path):
    base64_image = encode_image(image_path)
    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    system_role: ChatCompletionSystemMessageParam = {
        "role": "system",
        "content": """
你是一位营业执照稽核专家，对图片内容进行识别，并严格按照以下规则作出是否合规的判断，并说明不合规的原因。判断规则如下：
1、营业执照图片为黑白复印件加盖红色章的，判断为不合规；
2、营业执照为全彩色图片，但图片中含有“复印件”或“电子营业执照”或“仅供展示”的水印或字样，判断为不合规；
3、营业执照为全彩色图片，但图片中无“复印件”或“电子营业执照”水印或字样，或者营业执照图片边缘不完整，判断为不合规；
4、营业执照为全彩色图片，但图片中无“复印件”或“电子营业执照”水印或字样，且营业执照图片边缘完整，但营业执照图片为对屏幕翻拍照片文字或红色章模糊无法识别，判断为不合规。
回答格式：第一行输出“合规”或“不合规”，第二行输出不合规的原因。"""
    }
    completion = client.chat.completions.create(
        # model="qwen2.5-vl-72b-instruct",
        model="qwen-vl-max",
        messages=[
            system_role,
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
    )
    print(completion.model_dump_json())
