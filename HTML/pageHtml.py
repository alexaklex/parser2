from bs4 import BeautifulSoup
import re
import csv

class Getpage:
    def get_data(self, html):
        self.html = html
        soup = BeautifulSoup(html, 'lxml')
        #Главная картинка
        try:
            image = soup.find('table', id="product-table").find(id="img_photo").get('src')
            image_thumb = []
        except:
            image = ""
            image_thumb = ""
        #артикуль и название
        try:
            article_title = soup.find('table', id="product-table").find('h2')
            article_title_h2 = article_title.text
        except:
            article_title_h2 = ""
        try:
        # Состав материала и вес и цена
            material = ""
            weight = ""
            price = ""
        except:
            material = ""
            weight   = ""
            price = ""
        # все Свойства материала из списка
        try:
            properties_item = []
        except:
            properties_item = ""
        # Блок цвета пока текстом
        try:
            color_item = []
        except:
            color_item = ""
        #Размер
        try:
            size = []
        except:
            size = ""
        try:
            stock = []
        except:
            stock = ""
    #____________________________________________________

        # Собираем массив из цветов
        color = soup.select(".cwy")
        color_len = len(color)
        for i in range(0, color_len):
            color_item.append(color[i].text)
        # Из какого материала сделано
        try:
            material_2 = soup.find(text="Material: ")
        except:
            material_2 = ""
        try:
            weight_2 = soup.find(text="Weight: ")
        except:
            weight_2 = ""
        try:
            price_2 = soup.find(text="List price from: ")
        except:
            price_2 = ""

        material_data = article_title.find_next_siblings("p")
        for material_item in material_data:
            if material_item.find(text="Material: ") == material_2:
                material = material_item.text.split(':')[1]

            elif material_item.find(text="Weight: ") == weight_2:
                 weight = material_item.text.split(':')[1]

            elif material_item.find(text="List price from: ") == price_2:
                 price = material_item.text.split(':')[1]
            else:
                print("Пустой тег")

        properties_data = article_title.find_next('ul')
        properties_len = int(len(properties_data) / 2)
        for i in range(0, properties_len):
            prop  = properties_data('li')[i].string
            properties_item.append(prop.strip())
            # regex = re.compile(spl_thumb)
            # reg = regex.sub(spl_image, img_thumb)
        #Ищем все картинки из миниатюры
        try:
            image_thumb_data = soup.find(id="cwyImagesInner").find_all('a')
            for img in image_thumb_data:
                img_src = img.find('img').get('src')
                image_thumb.append(self.img_replace_num(img_src, image))
        except:
            print("Картинок здесь нет")
        #Собираем siz(размер) и stock(Остаток)
        try:
            size_len = soup.find('table', class_="custom-prices").find("tbody")
            size_type = ["XS", "S", "M", "L", "XL", "XXL"]

            #Количество
            for i in range(len(size_type)):
                type = soup.find('table', class_="custom-prices").find(text=size_type[i])
                if type in size_type:
                    size.append(type)
            #Размер
            for st in range(0, len(size_len)-1):
                stock_data = soup.find('table', class_="custom-prices").find(id="stk_1_"+str(st))
                stock.append(stock_data.text)
        except:
            print("размеров нет")
        data = {
            'image': image,
            'thumb': '| '.join(image_thumb),
            'title': article_title_h2,
            'material': material,
            'weight': weight,
            'price': price,
            'properties': '| '.join(properties_item),
            'stock':'| '.join(stock),
            'size': '| '.join(size),
            'color_item': '| '.join(color_item)
        }

        self.write_csv(data)

    def img_replace_num(self, img_thumb, image_base):
        spl_image = image_base.split('/')[-1].split('.')[0]
        spl_thumb = img_thumb.split('/')[-1].split('.')[0]
        if spl_thumb is not spl_image:
            regex = re.compile(spl_thumb)
            reg = regex.sub(spl_image, img_thumb)
        return reg

    def write_csv(self, data):
        with open('data.csv', 'a', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow((data['image'],
                             data['thumb'],
                             data['title'],
                             data['material'],
                             data['weight'],
                             data['price'],
                             data['properties'],
                             data['stock'],
                             data['size'],
                             data['color_item'])
                            )




