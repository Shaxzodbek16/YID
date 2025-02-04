import os
from enum import Enum

import pandas as pd
from typing import Union, List
from sqlalchemy.future import select

from app.bot.models import Downloads
from app.bot.utils.enums import VideoType
from app.core.databases.postgres import get_session


async def get_downloads_info(
    youtube: bool = False,
    instagram: bool = False,
    csv: bool = False,
    xlsx: bool = False,
) -> Union[str, List[str], List[dict]]:
    file_path = ""
    output_dir = "media/docs"
    os.makedirs(output_dir, exist_ok=True)

    async with get_session() as session:
        if youtube:
            result = await session.execute(
                select(Downloads).where(Downloads.type == VideoType.YOUTUBE.value)
            )
        elif instagram:
            result = await session.execute(
                select(Downloads).where(Downloads.type == VideoType.INSTAGRAM.value)
            )
        data = result.scalars().all()

    data_dicts = [row.__dict__ for row in data]
    for item in data_dicts:
        item.pop("_sa_instance_state", None)
        for key, value in item.items():
            if isinstance(value, pd.Timestamp) or hasattr(value, "tzinfo"):
                item[key] = (
                    value.replace(tzinfo=None)
                    if getattr(value, "tzinfo", None)
                    else value
                )
            elif isinstance(value, Enum):
                item[key] = value.value
    df = pd.DataFrame(data_dicts)
    if xlsx:
        file_name = f"youtube_downloaders.xlsx"
        file_path = os.path.join(output_dir, file_name)
        with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Sheet1")
            workbook = writer.book
            worksheet = writer.sheets["Sheet1"]

            header_format = workbook.add_format(
                {
                    "bold": True,
                    "text_wrap": True,
                    "valign": "top",
                    "fg_color": "#DDEBF7",
                    "border": 1,
                }
            )
            cell_format = workbook.add_format({"fg_color": "#B7DEE8", "border": 1})

            for col_num, col_name in enumerate(df.columns.values):
                worksheet.write(0, col_num, col_name, header_format)
            for row_num in range(1, len(df) + 1):
                worksheet.set_row(row_num, None, cell_format)

    elif csv:
        file_name = f"youtube_downloaders.csv"
        file_path = os.path.join(output_dir, file_name)
        df.to_csv(file_path, index=False)

    return file_path
