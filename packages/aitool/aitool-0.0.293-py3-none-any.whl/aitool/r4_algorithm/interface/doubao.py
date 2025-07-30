# -*- coding: UTF-8 -*-
"""

"""
from aitool import singleton, pip_install, USER_CONFIG
import base64
from typing import List


@singleton
class Client:
    def __init__(self, base_url, api_key):
        try:
            from volcenginesdkarkruntime import Ark
        except ModuleNotFoundError:
            pip_install('volcengine-python-sdk[ark]==1.0.109')
            from volcenginesdkarkruntime import Ark

        self.client = Ark(
            base_url=base_url,
            api_key=api_key,
        )


def infer_doubao(
        texts,
        base_url=USER_CONFIG['doubao_base_url'],
        api_key=USER_CONFIG['doubao_api_key'],
        model=USER_CONFIG['doubao_model'],
):
    """

    :param texts:
    :return:

    >>> infer_doubao(['你说一个数字', '2', '加1后是几'])    # 单次对话
    >>> infer_doubao(['今天是星期二'])    # 单次对话
    >>> infer_doubao(['今天是星期二', '那么明天是星期几？'])   # 多轮对话
    """
    client = Client(base_url, api_key)
    messages = []
    for idx, text in enumerate(texts):
        if idx % 2 == 0:
            messages.append({"role": "user", "content": "{}".format(text)})
        else:
            messages.append({"role": "assistant", "content": "{}".format(text)})
    completion = client.client.chat.completions.create(
        model=model,
        messages=messages,
    )
    return completion.choices[0].message.content


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def get_doubao_img_base64(local_path):
    # 参考 TODO更新
    base64_image = encode_image(local_path)
    if '.png' in local_path:
        base64_image = f"data:image/png;base64,{base64_image}"
    elif '.jpg' in local_path or '.jpeg' in local_path:
        base64_image = f"data:image/jpeg;base64,{base64_image}"
    elif '.webp' in local_path:
        base64_image = f"data:image/webp;base64,{base64_image}"
    elif '.gif' in local_path:
        base64_image = f"data:image/gif;base64,{base64_image}"
    elif '.bmp' in local_path:
        base64_image = f"data:image/bmp;base64,{base64_image}"
    elif '.tif' in local_path:
        base64_image = f"data:image/tiff;base64,{base64_image}"
    elif '.ico' in local_path:
        base64_image = f"data:image/x-icon;base64,{base64_image}"
    elif '.dib' in local_path:
        base64_image = f"data:image/bmp;base64,{base64_image}"
    else:
        raise ValueError('Invalid image format')
    return base64_image


def infer_doubao_vision(
        text,
        images: List,
        image_type,
        base_url=USER_CONFIG['doubao_base_url'],
        api_key=USER_CONFIG['doubao_api_key'],
        model=USER_CONFIG['doubao_model_vision'],
        max_pic=40,
        skip_error=True,
):
    """
    参考文档：TODO待更新
    :param text:
    :param image:
    :return:
    #

    # >>> infer_doubao_vision('第二张图片的内容是啥', ['https://img2.baidu.com/it/u=2809020982,898180050&fm=253&fmt=auto&app=138&f=JPEG?w=800&h=1428', 'https://img1.baa.bitautotech.com/dzusergroupfiles/2024/11/06/e2a4e9bb9e854429bed46ba1e343b47a.jpg', 'https://pics7.baidu.com/feed/cf1b9d16fdfaaf518b5d6daa01e826e3f11f7ab7.jpeg@f_auto?token=849a69f79836f8d80f8f4a8c5d3aa84d'], 'url')    # 单次对话
    # >>> infer_doubao_vision('这张图片内容是啥？', ['https://raw.githubusercontent.com/deepgameai/food101sample/refs/heads/main/sample_1010/2436856.jpg'], 'url')    # 单次对话
    # >>> infer_doubao_vision('这张图片内容是啥？', ['./358A88E1D73F9D111DE528EA5349870F.jpg'], 'local')    # 单次对话
    # >>> img_base64 = get_doubao_img_base64('./1112/008.webp')
    # >>> print(infer_doubao_vision('这张图片内容是啥？', [img_base64], 'base64'))
    """
    client = Client(base_url, api_key)
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": text},
            ],
        }
    ]
    for image in images[:max_pic]:
        if image_type == 'url':
            messages[0]["content"].append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image,
                        "detail": "high"
                    }
                }
            )
        elif image_type == 'local':
            base64_image = get_doubao_img_base64(image)
            messages[0]["content"].append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": base64_image

                    }
                }
            )
        elif image_type == 'base64':
            messages[0]["content"].append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image
                    }
                }
            )
        else:
            raise ValueError('image type out scope')

    try:
        # Image input:
        response = client.client.chat.completions.create(
            model=model,
            messages=messages,
        )
        ans = response.choices[0].message.content
    except Exception as e:
        if skip_error:
            print(e)
            ans = ''
        else:
            raise e

    return ans


if __name__ == "__main__":
    import doctest

    doctest.testmod()
