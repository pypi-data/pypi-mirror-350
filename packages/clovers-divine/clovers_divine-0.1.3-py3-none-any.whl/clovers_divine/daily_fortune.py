import json
import random
from datetime import date
from io import BytesIO
from pathlib import Path
from pydantic import BaseModel, Field
from PIL import Image, ImageDraw, ImageFont
from PIL.ImageFont import FreeTypeFont

type DailyFortuneResult = tuple[str, str]


class Data(BaseModel):
    results: dict[str, tuple[DailyFortuneResult, date]] = {}
    cache: dict[str, dict[str, Path]] = {}

    def save(self, file: Path):
        if not file.parent.exists():
            file.parent.mkdir(exist_ok=True, parents=True)
        file.write_text(self.model_dump_json(indent=4), encoding="utf-8")


class Copywriting(BaseModel):
    good_luck: str = Field(..., alias="good-luck")
    rank: int
    content: list[str]


class Manager:
    def __init__(
        self,
        data_path: Path | str,
        resource_path: Path | str,
        title_font: Path | str,
        text_font: Path | str,
    ):
        """
        path: Path 实例数据路径
        resource_path: Path 背景资源路径
        """
        resource = Path(__file__).parent / "resource" / "copywriting.json"
        with resource.open("r", encoding="utf-8") as f:
            self.copywriting = [Copywriting.model_validate(x) for x in json.load(f)["copywriting"]]
        if isinstance(data_path, str):
            data_path = Path(data_path)
        self.data_file = data_path / "fortune_data.json"
        if self.data_file.exists():
            self.data = Data.model_validate_json(self.data_file.read_text(encoding="utf-8"))
        else:
            self.data = Data()
        self.cache_path = data_path / "cache"
        if isinstance(resource_path, str):
            resource_path = Path(resource_path)
        if not self.cache_path.parent.exists():
            self.cache_path.parent.mkdir(exist_ok=True, parents=True)
        self.basemaps = [
            [file for file in theme.rglob("*") if file.suffix.lower() in {".jpg", ".jpeg", ".png"}]
            for theme in resource_path.iterdir()
            if theme.is_dir()
        ]
        self.title_font = ImageFont.truetype(title_font, 45)
        self.text_font = ImageFont.truetype(text_font, 25)

    def cache(self, group_id: str, user_id: str) -> None | BytesIO:
        file = self.data.cache.setdefault(group_id, {}).get(user_id)
        if file is not None and file.exists() and date.fromtimestamp(file.stat().st_mtime) == date.today():
            return BytesIO(file.read_bytes())

    def get_results(self, user_id: str) -> DailyFortuneResult | None:
        """获取今天的运势结果"""
        if data := self.data.results.get(user_id):
            result, stored_date = data
            if stored_date == date.today():
                return result

    def divine(self, user_id: str) -> DailyFortuneResult:
        copywriting = random.choice(self.copywriting)
        good_luck = copywriting.good_luck
        content = random.choice(copywriting.content)
        result = (good_luck, content)
        self.data.results[user_id] = result, date.today()
        return result

    def draw(self, group_id: str, user_id: str, result: DailyFortuneResult) -> BytesIO:
        image_file = self.cache_path / f"{group_id}_{user_id}.png"
        self.data.cache.setdefault(group_id, {})[user_id] = image_file
        theme = random.choice(self.basemaps)
        basemap = random.choice(theme)
        image = drawing(result, basemap, self.title_font, self.text_font)
        if not image_file.parent.exists():
            image_file.parent.mkdir(exist_ok=True, parents=True)
        image_file.write_bytes(image.getvalue())
        self.data.save(self.data_file)
        return image


def drawing(
    result: DailyFortuneResult,
    basemap: Path,
    title_font: FreeTypeFont,
    text_font: FreeTypeFont,
):
    title, text = result
    canvas = Image.open(basemap).convert("RGB")
    draw = ImageDraw.Draw(canvas)
    # 标题位置中心点是 (140, 99)，标题字号是 45
    draw.text((140 - title_font.getlength(title) / 2, 76.5), title, fill="#F5F5F5", font=title_font)
    # 文本位置中心点是 (140, 297)，文本字号是 25
    col_num, lines = decrement(text)
    text_length = col_num * 25 + (col_num - 1) * 4
    x = 111 + text_length / 2
    for line in lines:
        line_length = len(line)
        line_height = line_length * 25 + (line_length - 1) * 4
        y = 297 - line_height / 2
        for char in line:
            draw.text((x, y), char, fill="#323232", font=text_font)
            y += 29
        x -= 29
    output = BytesIO()
    canvas.save(output, format="png")
    return output


def decrement(text: str):
    if (length := len(text)) > 36:
        length = 36
        text = text[:36]
    col_num = length // 9 + int(length % 9 != 0)
    # 两行的话把字符串平分，半个字符给上半行
    if col_num == 2:
        harf = length - length // 2
        return col_num, [text[:harf] + " " * (9 - harf), " " * (9 - harf + int(length % 2 == 1)) + text[harf:]]
    else:
        return col_num, [text[i : i + 9] for i in range(0, length, 9)]
