import requests
from bs4 import BeautifulSoup
from argparse import ArgumentParser


def main():
    parser = ArgumentParser()
    parser.add_argument("-w", help="imput word", dest="w", required=True)
    args = parser.parse_args()

    base_url = 'https://dictionary.cambridge.org'
    dictionary_url = base_url + '/us/dictionary/english/'
    word = args.w
    header = {
        'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
    }
    res = requests.get(dictionary_url + word, headers=header)
    soup = BeautifulSoup(res.text, "lxml")
    res = soup.find("amp-audio", {
        "id": "ampaudio1"
    }).find("source", {"type": "audio/mpeg"})
    audio_url = res.get_attribute_list('src')[0]
    
    print(base_url + audio_url)
    r = requests.get(base_url + audio_url, headers=header)
    with open(word + '.mp3', 'wb') as f:
        f.write(r.content)


if __name__ == '__main__':
    main()