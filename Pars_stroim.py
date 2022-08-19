import requests
import lxml
import csv
from bs4 import BeautifulSoup


def get_data(url):
    header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 ' \
             '(KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}

    url = url
    # response = requests.get(url=url, headers=header)
    # response.encoding = 'utf-8'
    # soup = BeautifulSoup(response.text, 'lxml')

    # link_cat = [url + x['href'] for x in soup.find('div', class_='all_cat_list').find_all('a')]
    #
    # with open('link_cat.txt', 'w', encoding='utf-8') as file:
    #     for l in link_cat:
    #         file.write(l)
    #         file.write('\n')

    # with open('link_cat.txt', 'r', encoding='utf-8') as file:
    #     link_cat = [x.strip() for x in file]
    #     for i in link_cat:
    #         response = requests.get(url=i, headers=header)
    #         response.encoding = 'utf-8'
    #         soup = BeautifulSoup(response.text, 'lxml')
    #
    #         s = soup.find('div', class_='section_city_a').find_all('a')
    #
    #         with open('city_section.txt', 'a', encoding='utf-8') as file:
    #             for k in s:
    #                 file.write(i + k['href'])
    #                 file.write('\n')
    #                 print(k['href'])

    # with open('city_section.txt', 'r') as file:
    #     for i in file:
    #         response = requests.get(url=i.strip(), headers=header)
    #         response.encoding = 'utf-8'
    #         soup = BeautifulSoup(response.text, 'lxml')
    #         pagen = soup.find('a', class_='navigation_activ')
    #
    #         if pagen:
    #             link_pagen = soup.find('div', class_='num_pages').find_all('a')
    #
    #             with open('company.txt', 'a', encoding='utf-8') as file:
    #
    #                 for k in link_pagen:
    #                     file.write(url + k['href'])
    #                     file.write('\n')
    #                     print(url + k['href'])

    # with open('true_city_sec.txt', 'r') as file:
    #     for i in file:
    #         response = requests.get(url=i.strip(), headers=header)
    #         response.encoding = 'utf-8'
    #         soup = BeautifulSoup(response.text, 'lxml')
    #         company = soup.find_all('h5')
    #
    #         with open('company111.txt', 'a', encoding='utf-8') as files:
    #             for k in company:
    #                 files.write(url + k.find_next()['href'])
    #                 files.write('\n')
    #                 print(url + k.find_next()['href'])

    with open('company_str.csv', 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['НАЗВАНИЕ',
                         'ВИДЫ ДЕЯТЕЛЬНОСТИ',
                         'КОНТАКТЫ',
                         'ГОРОД',
                         'АДРЕС',
                         'КАТЕГОРИЯ',
                         'ССЫЛКА'])
    sc = 0

    with open('company.txt', 'r', ) as file_r:
        for l in file_r:
            try:
                sc += 1
                print(sc, l.strip())
                response = requests.get(url=l.strip(), headers=header)
                soup = BeautifulSoup(response.content, 'lxml')

                name = soup.find('div', class_='content').find('h1').text

                a = ''
                try:
                    activities = [x.text.strip('/') for x in soup.find('ul', class_='ul_comp').find_all('li')]
                    for i in activities:
                        a += '* ' + str(i) + '\n'

                    s = ''
                    c = []
                    contact = [x.text.strip() for x in soup.find('div', class_='company_full_text')]
                    for i in contact:
                        if i == 'Виды деятельности:':
                            break
                        if i == '':
                            continue
                        c.append(i)

                    cont = c[2:]
                    for x in cont:
                        s += str(x) + '\n'

                    city = [c[1].split(',')[0]]
                    adress = [c[1]]
                except IndexError:
                    print('Index Error', l)
                except AttributeError:
                    print('Attribute Error', l)

                t = ''
                category = [x.text.split() for x in soup.find('div', class_='control_company_cont').find_next_sibling()]
                true_cat = category[0][3:-1]
                for k in true_cat:
                    t += str(k) + ' '

                with open('company_str.csv', 'a', newline='', encoding='utf-8-sig') as file:
                    writer = csv.writer(file, delimiter=';')
                    writer.writerow([name, a.strip(), s.strip(), *city, *adress, t, l])
            except AttributeError:
                print('Attribute Error', l)
                continue


def main():
    get_data('https://stroit-kompanii.ru/')


if __name__ == '__main__':
    main()
