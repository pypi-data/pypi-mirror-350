import hashlib
import json
import math
import os
from PIL import Image, ExifTags
from jinja2 import Environment, FileSystemLoader, select_autoescape


def is_photo(name):
    return os.path.splitext(name)[1].lower() in ('.jpg', '.png', '.jpeg')


def first(path):
    photos = [
        name
        for name in os.listdir(path)
        if is_photo(name)
    ]
    if not photos:
        return {
            'name': '',
            'code': '',
        }
    photos.sort()
    return {
        'name': photos[0],
        'code': hashlib.md5(photos[0].encode('utf-8')).hexdigest()
    }


def convert_exif(k, v):
    if k == 'ShutterSpeedValue':
        try:
            return int(math.pow(2, float(v)))
        except OverflowError:
            return str(v)
    if k == 'ApertureValue':
        try:
            v = round(math.sqrt(math.pow(2, float(v))), 1)
            return f'f/{v}'
        except OverflowError:
            return str(v)
    if isinstance(v, str):
        return v[0:100]
    if isinstance(v, int):
        return str(v)
    if isinstance(v, bytes):
        return v.decode('utf-8')[0:100]
    print(k, type(v))
    return v


def generate_words(output_name, words):
    chunks = [int(output_name[x:x+7],16) for x in range(0, len(output_name), 7)]
    result = [words[chunk % len(words)] for chunk in chunks]
    return '-'.join(result).lower()


def generate_output_name(gallery_name, words):
    output_name = hashlib.md5(gallery_name.encode('utf-8')).hexdigest()
    return generate_words(output_name, words)


def build_dir(env, args, root, dirs, files, words):
    gallery_name = os.path.basename(root)
    output_name = generate_output_name(gallery_name, words)

    album = {
        'name': gallery_name,
        'code': output_name,
    }

    print(f'Build {gallery_name} -> {output_name}')
    build_dir = os.path.join(args.output, output_name)
    if not os.path.exists(build_dir):
        os.mkdir(build_dir)

    albums = [
        {
            'name': name,
            'code': generate_output_name(name, words),
            'path': os.path.join(root, name),
            'first': first(os.path.join(root, name)),
        }
        for name in dirs
    ]

    photos = [
        {
            'name': os.path.splitext(name)[0],
            'code': hashlib.md5(name.encode('utf-8')).hexdigest(),
            'path': os.path.join(root, name),
        }
        for name in files
        if is_photo(name)
    ]
    for index, photo in enumerate(photos):
        if index > 0:
            photo['before'] = photos[index-1]
        if index+1 < len(photos):
            photo['after'] = photos[index+1]

    index_path = os.path.join(build_dir, 'index.html')
    template = env.get_template('album.html')
    with open(index_path, 'w') as f:
        template.stream(
            args=args,
            title=gallery_name,
            albums=albums,
            photos=photos,
        ).dump(f)

    for entry in photos:

        image = Image.open(entry['path'])
        exif = image._getexif()
        if exif:
            exif = {
                ExifTags.TAGS[k]: v
                for k, v in exif.items()
                if k in ExifTags.TAGS
            }
            entry['exif'] = {
                k: convert_exif(k, v)
                for k, v in exif.items()
                if k in ('DateTime', 'Make', 'Model',
                         'FocalLengthIn35mmFilm',
                         'ShutterSpeedValue',
                         'ApertureValue',
                         'ISOSpeedRatings', 'ImageDescription',
                         'Copyright', 'UserComment',
                         'LensMake', 'LensModel')
            }

        template = env.get_template('photo.html')
        photo_path = os.path.join(build_dir, f'{entry["code"]}.html')
        with open(photo_path, 'w') as f:
            template.stream(album=album, **entry).dump(f)

        thumb_path = os.path.join(build_dir, f'{entry["code"]}.thumb.jpg')
        if not os.path.exists(thumb_path):
            print(f'Generate thumbnail {thumb_path}')
            image = Image.open(entry['path'])
            image = image.convert('RGB')
            image.thumbnail((200, 200))
            data = list(image.getdata())
            image = Image.new(image.mode, image.size)
            image.putdata(data)
            image.save(thumb_path)

        image_path = os.path.join(build_dir, f'{entry["code"]}.jpg')
        if not os.path.exists(image_path):
            print(f'Generate image {image_path}')
            image = Image.open(entry['path'])
            image = image.convert('RGB')
            image.thumbnail((700, 700))
            data = list(image.getdata())
            image = Image.new(image.mode, image.size)
            image.putdata(data)
            image.save(image_path)

        large_path = os.path.join(build_dir, f'{entry["code"]}.large.jpg')
        if not os.path.exists(large_path):
            print(f'Generate image {large_path}')
            image = Image.open(entry['path'])
            image = image.convert('RGB')
            image.thumbnail((1400, 1400))
            data = list(image.getdata())
            image = Image.new(image.mode, image.size)
            image.putdata(data)
            image.save(large_path)

def build(args):
    if not os.path.isdir(args.path):
        return
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    base_dir = os.path.dirname(__file__)
    template_dir = os.path.join(base_dir, 'templates')
    print('Templates at', template_dir)

    with open(os.path.join(os.path.dirname(__file__), 'stars.json'), 'r') as f:
        words = json.load(f)
        print(len(words), 'stars')

    env = Environment(loader=FileSystemLoader(template_dir), autoescape=select_autoescape())

    template = env.get_template('theme.css')
    theme_path = os.path.join(args.output, 'theme.css')
    with open(theme_path, 'w') as f:
        template.stream().dump(f)

    template = env.get_template('robots.txt')
    robots_path = os.path.join(args.output, 'robots.txt')
    with open(robots_path, 'w') as f:
        template.stream().dump(f)

    for root, dirs, files in os.walk(args.path):
        build_dir(env, args, root, dirs, files, words)
