import json
import random
from pathlib import Path
from io import BytesIO
from typing import TypedDict
from pydantic import BaseModel
from PIL import Image

type TarotResult = tuple[str, str, str, bool]
"""info:塔罗牌信息 explain:塔罗牌解读 pic:塔罗牌图片 flag:是否正位"""


class TarotFormations(BaseModel):
    key: str
    cards_num: int
    is_cut: bool
    representations: list[list[str]]


class CardMeaning(TypedDict):
    up: str
    down: str


class CardInfo(BaseModel):
    name_cn: str
    name_en: str
    type: str
    meaning: CardMeaning
    pic: str


class ResourceDict(TypedDict):
    formations: dict
    cards: dict


class Manager:
    def __init__(
        self,
        resource_path: Path | str,
    ):
        resource = Path(__file__).parent / "resource" / "tarot.json"
        with resource.open("r", encoding="utf-8") as f:
            tarot: ResourceDict = json.load(f)
            self.formations = [TarotFormations.model_validate(v | {"key": k}) for k, v in tarot["formations"].items()]
            self.cards = [CardInfo.model_validate(v) for v in tarot["cards"].values()]
        if isinstance(resource_path, str):
            resource_path = Path(resource_path)
        pics = {card.pic for card in self.cards}
        self.theme = {
            theme_path.stem: {
                card: tarot_image_file
                for tarot_image_file in theme_path.rglob("*")
                if tarot_image_file.is_file()
                and (card := tarot_image_file.stem) in pics
                and tarot_image_file.suffix.lower() in {".jpg", ".jpeg", ".png"}
            }
            for theme_path in resource_path.iterdir()
            if theme_path.is_dir()
        }
        self.theme_keys = list(self.theme.keys())

    def tarot(self) -> TarotResult:
        """
        抽一张塔罗牌

        Return:

            TarotResult
        """

        card = random.choice(self.cards)
        if random.random() < 0.5:
            return f"「{card.name_cn}逆位」", f"「{card.meaning["down"]}」", card.pic, False
        else:
            return f"「{card.name_cn}正位」", f"「{card.meaning["up"]}」", card.pic, True

    def divine(self) -> tuple[str, list[TarotResult]]:
        formation = random.choice(self.formations)
        representations = random.choice(formation.representations)
        result_list = []
        for i, tips in enumerate(representations, 1):
            card, explain, pic, flag = self.tarot()
            title = "切牌" if formation.cards_num == i and formation.is_cut else f"第{i}张牌"
            result_list.append((f"{title} {tips}{card}", explain, pic, flag))
        return formation.key, result_list

    def draw(self, theme: str, pic: str, flag: bool):
        image_file = self.theme[theme].get(pic)
        if image_file is None:
            for fallback_theme in self.theme.values():
                if pic in fallback_theme:
                    image_file = fallback_theme[pic]
                    break
            else:
                return
        if flag:
            image = BytesIO(image_file.open(mode="rb").read())
        else:
            image = BytesIO()
            Image.open(image_file).convert("RGB").rotate(180, expand=True).save(image, format="png")
        return image

    def random_theme(self) -> str:
        return random.choice(self.theme_keys)
