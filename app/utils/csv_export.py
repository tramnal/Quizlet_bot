import csv
import io
from app.database.db_requests import get_all_user_words


async def export_to_csv(tg_id: int) -> io.BytesIO:
    '''Exports user dict to csv-file'''
    words = await get_all_user_words(tg_id)

    if not words:
        return None

    file = io.StringIO()
    writer = csv.writer(file)
    writer.writerow(['Слово', 'Перевод'])

    for w in words:
        writer.writerow([w.word, w.translation])

    byte_file = io.BytesIO()
    byte_file.write(file.getvalue().encode('UTF-8'))
    byte_file.seek(0)
    return byte_file
