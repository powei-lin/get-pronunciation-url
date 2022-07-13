import requests
from bs4 import BeautifulSoup
from argparse import ArgumentParser
import subprocess


def parse_url_as_macos(url):
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"
    }
    res = requests.get(url, headers=header)
    return BeautifulSoup(res.text, "lxml")


def get_from_cambridge(word: str):
    base_url = "https://dictionary.cambridge.org"
    dictionary_url = base_url + "/us/dictionary/english/"

    soup = parse_url_as_macos(dictionary_url + word)
    audio = soup.find("amp-audio", {"id": "ampaudio1"})
    if not audio:
        return None
    res = soup.find("amp-audio", {"id": "ampaudio1"}).find(
        "source", {"type": "audio/mpeg"}
    )
    audio_url = res.get_attribute_list("src")[0]
    data = base_url + audio_url
    print("get from cambridge")
    return data


def get_from_merriam_webster(word: str):
    base_url = "https://www.merriam-webster.com/dictionary/" + word
    soup = parse_url_as_macos(base_url)
    d = soup.find(class_="play-pron hw-play-pron")
    if d:
        data_dir = d.get("data-dir")
        data_file = d.get("data-file")
        data_url = data_dir + "/" + data_file + ".mp3"
        print("get from merriam webster")
        return "https://media.merriam-webster.com/audio/prons/en/us/mp3/" + data_url

    return None


def main():
    parser = ArgumentParser()
    parser.add_argument("-w", help="imput word", dest="w", required=True)
    args = parser.parse_args()

    word = args.w

    # try from cambridge
    data = get_from_cambridge(word)

    # try from merriam_webster
    if not data:
        data = get_from_merriam_webster(word)

    if data:
        subprocess.run("pbcopy", universal_newlines=True, input=data)
    else:
        print("not found")


if __name__ == "__main__":
    main()
