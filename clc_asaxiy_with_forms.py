from telegram.ext import CommandHandler, Updater, MessageHandler, Filters
from bs4 import BeautifulSoup
import requests

def start(update, context):
    update.message.reply_text('Enter the product name:  ')

def form(update, context):
    form = update.message.text
    URL = 'https://asaxiy.uz/'
    URL += f"product?key={form}"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    images = soup.find_all('img', class_='img-fluid lazyload')
    links  =[]
    for img in images[:10]:
        links.append(img['data-src'])

    first_div = soup.find('div', class_='row custom-gutter mb-40')
    titles, costs = [], []
    for i in range(10):
        titles.append(first_div.find_all('h5', class_='product__item__info-title')[i].text)
        costs.append(first_div.find_all('span', class_='product__item-price')[i].text)

    for_more = soup.find_all('a', class_='title__link')
    for_more_links = []
    for link in for_more[:10]:
        for_more_links.append(link["href"])

    # titles_text = ""
    # costs_text = ""
    # for i,j  in zip(titles, costs):
    #     titles_text += i.strip() + '\n'
    #     costs_text += j.strip() + '\n'

    for item in range(10):
        if links[item][-5:] == '.webp':
            update.message.reply_photo(links[item][:-5],
                                        f'\n {titles[item].strip()}\n<b>{costs[item].strip()}</b>\n\n<b>For more:</b>  asaxiy.uz{for_more_links[item]}', parse_mode='html')
        else:
            update.message.reply_photo(links[item],
                                       f'\n {titles[item].strip()}\n<b>{costs[item].strip()}</b>\n\n<b>For more:</b>  asaxiy.uz{for_more_links[item]}', parse_mode='html')

def main():
    updater = Updater('5462884979:AAHkCjLQupRu4SW2_so0wGj7mYiXInb1oIM', use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text, form))

    updater.start_polling()
    updater.idle()

if __name__=='__main__':
    main()