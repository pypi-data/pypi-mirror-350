def save_photo(pic_path, data):
    # Сохранить данные фото (data) в pic_path
    with open(pic_path, 'wb') as fobj:
        fobj.write(data)
