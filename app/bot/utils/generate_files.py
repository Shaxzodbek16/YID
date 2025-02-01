import pandas as pd
import os
from typing import Type
from sqlalchemy.future import select

from app.bot.models import Downloads
from app.bot.utils.enums import FileType
from app.core.databases.postgres import get_session


async def export_model_to_file(model: Type, file_type: FileType) -> str:
    output_dir = "media/docs"
    os.makedirs(output_dir, exist_ok=True)
    async with get_session() as session:

        data = (await session.execute(select(model))).scalars().all()

    data_dicts = [row.__dict__ for row in data]

    for item in data_dicts:
        item.pop("_sa_instance_state", None)

        for key, value in item.items():
            if isinstance(value, pd.Timestamp) or hasattr(value, "tzinfo"):
                item[key] = value.replace(tzinfo=None) if value.tzinfo else value

    df = pd.DataFrame(data_dicts)

    file_name = f"{model.__name__}.{file_type.value}"
    file_path = os.path.join(output_dir, file_name)
    if file_type == FileType.XLSX:
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

    elif file_type == FileType.CSV:
        df.to_csv(file_path, index=False)
    else:
        pass
    return file_path
