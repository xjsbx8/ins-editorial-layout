"""
COLX Ins风排版 SKU 渲染引擎 v2.0
默认画幅: 1080 x 1440 (3:4)
核心范式:
  1. single_stacked_star: 错落三行大字 + 复古星芒贴纸
  2. diary_inline_parens: 括号画中画照片日记
  3. gallery_clean_grid: 纯净暖白画廊多焦段拼图
"""
import math
from PIL import Image, ImageDraw, ImageFont, ImageOps


class ColxInsSkillEngine:
    def __init__(self, font_bold_path: str, font_reg_path: str):
        self.W = 1080
        self.H = 1440
        self.HEADER_H = 132
        self.FOOTER_H = 228
        self.CONTENT_H = self.H - self.HEADER_H - self.FOOTER_H
        self.font_bold_path = font_bold_path
        self.font_reg_path = font_reg_path

    def _font(self, size: int, bold: bool = False):
        path = self.font_bold_path if bold else self.font_reg_path
        return ImageFont.truetype(path, size)

    def draw_ins_outer_chrome(
        self,
        canvas: Image.Image,
        avatar_img: Image.Image,
        username: str = "soft.days",
        subtitle: str = "单页 · SINGLE PAGE",
        likes_text: str = "9,099 次赞",
        caption: str = "今天的照片这样排 #ootd #ins排版",
        liked: bool = False,
    ):
        """绘制最外圈 Ins 顶底栏原生界面框架"""
        draw = ImageDraw.Draw(canvas, "RGBA")

        # 顶部栏
        draw.rectangle((0, 0, self.W, self.HEADER_H), fill=(255, 255, 255, 255))
        draw.line([(0, self.HEADER_H - 1), (self.W, self.HEADER_H - 1)],
                  fill=(238, 238, 238, 255), width=1)

        # 头像 + 彩虹环
        av_size = 68
        av_x, av_y = 36, (self.HEADER_H - av_size) // 2
        draw.ellipse((av_x - 4, av_y - 4, av_x + av_size + 4, av_y + av_size + 4),
                     outline=(225, 48, 108, 255), width=3)
        av_crop = ImageOps.fit(avatar_img, (av_size, av_size), method=Image.LANCZOS)
        mask = Image.new("L", (av_size, av_size), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, av_size, av_size), fill=255)
        canvas.paste(av_crop, (av_x, av_y), mask)

        # 用户名与副标题
        draw.text((av_x + av_size + 20, av_y + 6), username,
                  font=self._font(28, bold=True), fill=(20, 20, 20))
        draw.text((av_x + av_size + 20, av_y + 42), subtitle,
                  font=self._font(20, bold=False), fill=(150, 150, 150))

        # 三点菜单
        for i in range(3):
            cx = self.W - 64 + i * 12
            cy = self.HEADER_H // 2
            draw.ellipse((cx - 3, cy - 3, cx + 3, cy + 3), fill=(40, 40, 40))

        # 底部栏
        fy = self.H - self.FOOTER_H
        draw.rectangle((0, fy, self.W, self.H), fill=(255, 255, 255, 255))
        draw.line([(0, fy), (self.W, fy)], fill=(238, 238, 238, 255), width=1)

        icon_y = fy + 34
        heart_color = (237, 73, 86) if liked else (30, 30, 30)
        if liked:
            draw.polygon([(42, icon_y + 12), (58, icon_y + 28), (74, icon_y + 12),
                          (66, icon_y), (58, icon_y + 8), (50, icon_y)],
                         fill=heart_color)
        else:
            draw.polygon([(42, icon_y + 12), (58, icon_y + 28), (74, icon_y + 12),
                          (66, icon_y), (58, icon_y + 8), (50, icon_y)],
                         outline=heart_color, width=3)

        # 评论气泡
        draw.ellipse((106, icon_y, 138, icon_y + 30), outline=(30, 30, 30), width=3)
        # 纸飞机
        draw.polygon([(168, icon_y + 2), (200, icon_y + 14), (182, icon_y + 18),
                      (176, icon_y + 30)], outline=(30, 30, 30), width=3)
        # 书签
        bx = self.W - 68
        draw.polygon([(bx, icon_y), (bx + 28, icon_y), (bx + 28, icon_y + 32),
                      (bx + 14, icon_y + 22), (bx, icon_y + 32)],
                     outline=(30, 30, 30), width=3)

        # 点赞数与文案
        likes_color = (237, 73, 86) if liked else (20, 20, 20)
        draw.text((38, fy + 88), likes_text,
                  font=self._font(26, bold=True), fill=likes_color)
        draw.text((38, fy + 132), f"{username}  {caption}",
                  font=self._font(24, bold=False), fill=(35, 35, 35))

    @staticmethod
    def _draw_star_polygon(draw, cx, cy, outer_r, inner_r, fill_color, rotation_deg=0):
        """绘制复古扁平五角星贴纸"""
        pts = []
        for i in range(10):
            angle = math.radians(rotation_deg + i * 36 - 90)
            r = outer_r if i % 2 == 0 else inner_r
            pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
        draw.polygon(pts, fill=fill_color)

    def render_single_stacked_star(
        self,
        photo: Image.Image,
        lines=("nov", "em", "ber"),
        text_color=(255, 245, 196, 255),
        username="soft.days",
    ) -> Image.Image:
        """TYP 范式：大字错落断行 + 星芒贴纸 + Ins 外框"""
        canvas = Image.new("RGBA", (self.W, self.H), (255, 255, 255, 255))
        body_img = ImageOps.fit(photo, (self.W, self.CONTENT_H), method=Image.LANCZOS)
        canvas.paste(body_img, (0, self.HEADER_H))

        overlay = Image.new("RGBA", (self.W, self.CONTENT_H), (0, 0, 0, 0))
        odraw = ImageDraw.Draw(overlay, "RGBA")

        # 底层星芒
        self._draw_star_polygon(odraw, 260, 480, 44, 19,
                                (248, 228, 138, 250), -15)
        self._draw_star_polygon(odraw, 640, 460, 108, 46,
                                (238, 108, 138, 248), 12)

        # 三行大字
        txt_layer = Image.new("RGBA", (700, 560), (0, 0, 0, 0))
        tdraw = ImageDraw.Draw(txt_layer, "RGBA")
        big_font = self._font(148, bold=True)
        y_offsets = [10, 145, 280]
        x_offsets = [90, 95, 105]
        for line_str, lx, ly in zip(lines, x_offsets, y_offsets):
            tdraw.text((lx + 4, ly + 6), line_str, font=big_font, fill=(20, 20, 20, 75))
            tdraw.text((lx, ly), line_str, font=big_font, fill=text_color)

        rot_txt = txt_layer.rotate(8, resample=Image.BICUBIC, expand=True)
        overlay.alpha_composite(rot_txt, (165, 340))

        # 顶层星芒
        self._draw_star_polygon(odraw, 235, 735, 98, 42,
                                (238, 108, 138, 252), -8)
        self._draw_star_polygon(odraw, 585, 665, 52, 22,
                                (248, 228, 138, 252), 18)

        canvas.alpha_composite(overlay, (0, self.HEADER_H))
        self.draw_ins_outer_chrome(
            canvas, avatar_img=photo, username=username,
            subtitle="单页 · SINGLE PAGE", likes_text="9,099 次赞",
            caption="今天的照片这样排 #ootd #ins排版", liked=False,
        )
        return canvas.convert("RGB")

    def render_diary_inline_parens(
        self,
        main_photo: Image.Image,
        inset_photos: list,
        words=("what I", "did", "in nov"),
        username="cafe.moments",
    ) -> Image.Image:
        """JNL 范式：括号画中画照片日记 + Ins 外框"""
        canvas = Image.new("RGBA", (self.W, self.H), (255, 255, 255, 255))
        body_img = ImageOps.fit(main_photo, (self.W, self.CONTENT_H), method=Image.LANCZOS)
        canvas.paste(body_img, (0, self.HEADER_H))

        draw = ImageDraw.Draw(canvas, "RGBA")
        diary_font = self._font(86, bold=False)
        paren_font = self._font(102, bold=False)

        row_y_list = [self.HEADER_H + 310, self.HEADER_H + 525, self.HEADER_H + 740]
        row_x_list = [210, 265, 190]
        thumb_w, thumb_h = 186, 114

        for idx in range(3):
            word = words[idx]
            rx, ry = row_x_list[idx], row_y_list[idx]

            draw.text((rx + 2, ry + 3), word, font=diary_font, fill=(0, 0, 0, 95))
            draw.text((rx, ry), word, font=diary_font, fill=(255, 255, 255, 255))

            bbox = draw.textbbox((rx, ry), word, font=diary_font)
            word_w = bbox[2] - bbox[0]

            # 左括号
            px = rx + word_w + 28
            draw.text((px, ry - 10), "(", font=paren_font, fill=(255, 255, 255, 255))

            # 内嵌缩略图
            tx, ty = px + 46, ry - 4
            thumb_src = inset_photos[idx % len(inset_photos)]
            thumb = ImageOps.fit(thumb_src, (thumb_w, thumb_h), method=Image.LANCZOS)
            canvas.paste(thumb, (tx, ty))
            draw.rectangle((tx, ty, tx + thumb_w, ty + thumb_h),
                           outline=(255, 255, 255, 210), width=2)

            # 右括号
            rx_close = tx + thumb_w + 14
            draw.text((rx_close, ry - 10), ")", font=paren_font, fill=(255, 255, 255, 255))

        self.draw_ins_outer_chrome(
            canvas, avatar_img=main_photo, username=username,
            subtitle="照片日记 · PHOTO DIARY", likes_text="3,744 次赞",
            caption="今天的照片这样排 #ootd #ins排版", liked=True,
        )
        return canvas.convert("RGB")

    def render_gallery_clean_grid(
        self,
        photo: Image.Image,
        username: str = "soft.days",
        mode: str = "single",
    ) -> Image.Image:
        """
        GAL 范式：高克重暖白画廊无字排版
        暖白艺术纸底 (#F4F2EC)，零文字零贴纸

        Args:
            mode: "single" 单张居中留白（默认）；"grid" 四宫格非对称切片
        """
        canvas = Image.new("RGBA", (self.W, self.H), (255, 255, 255, 255))
        gallery = Image.new("RGBA", (self.W, self.CONTENT_H), (244, 242, 236, 255))

        if mode == "single":
            # 单张居中留白：照片四周留 60px 暖白边
            margin = 60
            pw = self.W - margin * 2
            ph = self.CONTENT_H - margin * 2
            img = ImageOps.fit(photo, (pw, ph), method=Image.LANCZOS)
            gallery.paste(img, (margin, margin))
        else:
            # 四宫格非对称切片
            gap = 24
            inner_w = self.W - gap * 2
            inner_h = self.CONTENT_H - gap * 2

            big_w = int(inner_w * 0.58)
            big_h = int(inner_h * 0.58)
            img1 = ImageOps.fit(photo, (big_w, big_h), method=Image.LANCZOS)
            gallery.paste(img1, (gap, gap))

            right_w = inner_w - big_w - gap
            right_h = int(inner_h * 0.4)
            top_crop = photo.crop((0, 0, photo.width, int(photo.height * 0.4)))
            img2 = ImageOps.fit(top_crop, (right_w, right_h), method=Image.LANCZOS)
            gallery.paste(img2, (gap + big_w + gap, gap))

            bottom_h = inner_h - big_h - gap
            bot_crop = photo.crop((int(photo.width * 0.5), int(photo.height * 0.5),
                                   photo.width, photo.height))
            img3 = ImageOps.fit(bot_crop, (right_w, bottom_h), method=Image.LANCZOS)
            gallery.paste(img3, (gap + big_w + gap, gap + right_h + gap))

            left_bot_h = inner_h - big_h - gap
            left_crop = photo.crop((0, int(photo.height * 0.55),
                                    int(photo.width * 0.6), photo.height))
            img4 = ImageOps.fit(left_crop, (big_w, left_bot_h), method=Image.LANCZOS)
            gallery.paste(img4, (gap, gap + big_h + gap))

        canvas.paste(gallery, (0, self.HEADER_H))

        self.draw_ins_outer_chrome(
            canvas, avatar_img=photo, username=username,
            subtitle="画廊 · GALLERY", likes_text="6,218 次赞",
            caption="今天的照片这样排 #ootd #ins排版", liked=False,
        )
        return canvas.convert("RGB")
