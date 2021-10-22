__name__ = "不可以色色"
__doc__ = "生成色色敲图"

import os
from PIL import Image, ImageDraw, ImageFont

from botoy import GroupMsg, S
from botoy import decorators as deco
from botoy.collection import MsgTypes

base_dir_path = os.path.dirname(__file__)
gif_file_path = os.path.join(base_dir_path, 'origin/400x221.gif')
out_file_dir_path = os.path.join(base_dir_path, 'output')

font_path = os.path.join(base_dir_path, 'font/DroidSansFallback.ttf')

scale = 1
fixed_padding_bottom = int(10 * scale)
fixed_x_padding = int(4 * 2 * scale)
init_font_size = int(24 * scale)
min_font_limit = init_font_size / 1.65

start_draw_text_index = 10
throttle_w = 360
throttle_h = 204


def check_dir():
    if not os.path.exists(out_file_dir_path):
        os.makedirs(out_file_dir_path)


def handle_frame(frame, render_text):
    width = frame.width
    height = frame.height
    r_w = int(width * scale)
    r_h = int(height * scale)
    empty_img = Image.new("RGBA", (r_w, r_h), (255, 255, 255))
    background = frame.resize((r_w, r_h), Image.ANTIALIAS)
    empty_img.paste(background, (0, 0))
    empty_draw = ImageDraw.Draw(empty_img)

    font_size = init_font_size
    ttfront = ImageFont.truetype(font_path, font_size)
    font_render_width = ttfront.getsize(render_text)[0]

    while (font_render_width + fixed_x_padding) > r_w:
        font_size -= 1
        ttfront = ImageFont.truetype(font_path, font_size)
        font_render_width = ttfront.getsize(render_text)[0]

    if font_size <= min_font_limit:
        return [False, frame]

    center_x = r_w / 2
    bottom_y = r_h - fixed_padding_bottom
    draw_x = int(center_x)
    draw_y = int(bottom_y)

    stroke_width = int(font_size / 7)
    empty_draw.text(
        (draw_x, draw_y),
        text=render_text,
        font=ttfront,
        fill='white',
        stroke_width=stroke_width,
        stroke_fill='black',
        anchor='mb',
    )

    return [True, empty_img.resize((width, height), Image.ANTIALIAS)]


def gen_gif(render_text='', qq=0):
    """
      max case: 你所热爱的，就是你的生活，柠檬什么时候熟啊？？
    """

    render_text = render_text.strip()
    if not render_text:
        return

    img_list = []

    img = Image.open(gif_file_path)
    duration = img.info['duration']
    img.seek(0)

    is_text_width_overflow = False
    while True:
        try:
            current_idx = img.tell()
            new_img = img.resize((throttle_w, throttle_h), Image.ANTIALIAS)
            if current_idx >= start_draw_text_index:
                status, new_img = handle_frame(
                    new_img, render_text=render_text)
                if not status:
                    is_text_width_overflow = True
                    break
            img_list.append(new_img)
            img.seek(current_idx + 1)
        except EOFError:
            break

    if is_text_width_overflow:
        print('text width overflow')
        return

    check_dir()
    output_file_path = os.path.join(out_file_dir_path, f'{qq}.gif')
    img_list.append(img_list[-1])
    img_list[0].save(output_file_path,
                     save_all=True,
                     append_images=img_list,
                     duration=duration + 15,
                     loop=0)

    return output_file_path


@deco.ignore_botself
@deco.these_msgtypes(MsgTypes.TextMsg)
@deco.on_regexp(r"ss (\w+)")
def receive_group_msg(ctx: GroupMsg):
    text: str = ctx._match.group(1).strip()
    img_base64 = gen_gif(render_text=text, qq=ctx.FromUserId)
    if img_base64:
        S.image(data=img_base64, type=S.TYPE_PATH)
