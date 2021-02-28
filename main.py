import os
import json
import pytesseract
from pdf2image import convert_from_path
from tqdm import tqdm
from PIL import Image
import hashlib
import random
import requests

os.chdir(os.getcwd())


def load_config():
    with open("./config/config.json", 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config


def pdf2image(head, file, config):
    output_dir = config['output_image'] + os.sep + head
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
        print("#### create image output dir: {}".format(output_dir))
    else:
        print("#### image output dir: {} exist".format(output_dir))

    images = convert_from_path(file, output_folder=output_dir)
    return images


def translate(source_text, config):
    url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
    app_id, secret_key, from_lang, to_lang = \
        config['app_id'], config['secret_key'], config['source_lang'], config['target_lang']
    salt = random.randint(32768, 65536)
    sign = app_id + source_text + str(salt) + secret_key
    md5_sign = hashlib.md5(sign.encode('utf-8')).hexdigest()
    params = {"q": source_text,
              "from": from_lang,
              "to": to_lang,
              "appid": app_id,
              "salt": salt,
              "sign": md5_sign}

    try:
        response = requests.get(url=url, params=params)
    except:
        response = None
        print("request fail, please check")

    target_text = ""
    if response:
        res_json = json.loads(response.text)

        t_list = [it['dst'] for it in res_json['trans_result']]
        target_text = "\n".join(t_list)

    return target_text


def ocr():
    config = load_config()
    root, _, files = next(os.walk(config['input_dir']))

    for file in sorted(files):
        if file[-4:] != '.pdf':
            print("ignore file: {}".format(file))
            continue
        print("#### deal with {}".format(file))
        p = root + os.sep + file
        images = pdf2image(file.replace(".pdf", ""), p, config)
        print("#### done")
        print("#### start translate\n****")
        print("total pages {}".format(len(images)))

        with open(config['output_text']+os.sep+file.replace(".pdf", ".txt"), 'w') as f:

            for idx, it in tqdm(enumerate(images)):
                image = Image.open(it.filename)
                source_text = pytesseract.image_to_string(image)
                target_text = translate(source_text, config)
                # print(target_text)
                f.write("[page {}]\n [source]:\n{}\n [target]:\n{}\n".format(idx, source_text, target_text))


if __name__ == "__main__":
    ocr()
