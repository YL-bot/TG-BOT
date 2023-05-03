from PIL import Image


# функция, возвращающая фото в фильтре ч/б
def black_white():
    try:
        picture = 'files/image.img'
        im = Image.open(picture)
        pixels = im.load()
        x, y = im.size
        index = picture.find('.')

        for i in range(x):
            for j in range(y):
                r, g, b = pixels[i, j]
                bw = (r + g + b) // 3
                pixels[i, j] = bw, bw, bw
        im.save(f"{picture[::index]}_black_white.jpg")

        # возвращаем название лучше
        return f"{picture[::index]}_black_white.jpg"

    except Exception:
        return 'error'
