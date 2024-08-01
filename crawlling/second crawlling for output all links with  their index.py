import requests
import bs4

the_links = ['https://gate.ahram.org.eg/', 'https://english.ahram.org.eg/']
the_count = 0
count = 1

try:
    while len(the_links) < 10001:
        print('####################### New page #################################', the_count)
        res = requests.get(the_links[the_count])
        the_count += 1
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        for link in soup.find_all('a', href=True):
            if str(link['href']).startswith('https://') and str(link['href']) not in the_links and count < 10001:
                print('<<<<<<<<<<<<<<<<link number>>>>>>>>>>', count)
                the_links.append(link['href'])
                print(link['href'])
                count += 1
except (requests.ConnectionError, requests.Timeout, requests.RequestException) as e:
    print("An error occurred while connecting:", str(e))

links_count = 0

with open('PR-Input10000(Ahram).txt', 'w', encoding="utf-8") as file:
    for link in the_links:
        file.write("{} {}\n".format(links_count, link))
        links_count += 1

with open('PR-Input10000(Ahram).txt', 'a', encoding="utf-8") as file:
    for i_of_l in range(len(the_links)):
        try:
            res3 = requests.get(the_links[i_of_l])
            soup3 = bs4.BeautifulSoup(res3.text, 'lxml')
            for l in soup3.find_all('a', href=True):
                if str(l['href']).startswith('https://') and str(l['href']) in the_links:
                    file.write("{} {}\n".format(i_of_l, the_links.index(l['href'])))
                    links_count += 1
        except (requests.ConnectionError, requests.Timeout, requests.RequestException) as e:
            print("An error occurred while connecting:", str(e))

def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

line_prepender('PR-Input10000(Ahram).txt', '{} {}'.format(len(the_links), links_count - len(the_links)))