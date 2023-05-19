# PIL

from PIL import Image, ImageDraw, ImageFont
import string
import random
from io import BytesIO

def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


str_all = string.digits + string.ascii_letters

def random_code(size=(174, 40), length=6, point_num=200, lin_num=8):
    width, height = size
    img = Image.new('RGB', (width, height), color=(255, 255, 220))

    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(font='static/my/font/long.ttf', size=32)

    valid_code = ''
    for i in range(length):
        randoms = random.choice(str_all)
        draw.text((25 * i + 15, 0), randoms, (0, 0, 0), font=font)
        valid_code += randoms
    print(valid_code)

    # 随机生成点
    for i in range(point_num):
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.point((x, y), random_color())

    # 随机生成线
    for i in range(lin_num):
        x1, y1 = random.randint(0, width), random.randint(0, height)
        x2, y2 = random.randint(0, width), random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=random_color())

    # 创建一个内存句柄
    f = BytesIO()
    # 把图片保存到内存句柄
    img.save(f, 'PNG')

    # 读取内存句柄
    data = f.getvalue()
    return (data, valid_code)


if __name__ == '__main__':
    random_code()
