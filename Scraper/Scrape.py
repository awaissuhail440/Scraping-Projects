import requests
from bs4 import BeautifulSoup as bS
from csv import writer
import boto3

class Device:
    def __int__(self,name,image,code,rating,category,description,availability,price,processor,ram,disk,GraphicCard,Display):
        self.name = name
        self.image = image
        self.code = code
        self.rating = rating
        self.category = category
        self.description = description
        self.availability = availability
        self.price = price
        self.ram = ram
        self.disk = disk
        self.GraphicCard = GraphicCard
        self.Display = Display

response = requests.get('https://www.czone.com.pk/laptops-pakistan-ppt.74.aspx')
soup = bS(response.content, 'html.parser')
body = soup.find('body')
soup.find_all("a")

type(body)
products = soup.findAll("div", {"class": "product"})
print(len(products))

count = 0
devices = []
for div in products:
    d = Device()

    client = boto3.client(
        'dynamodb',
        aws_access_key_id="ASIAZNJQENCJATQE2F73",
        aws_secret_access_key="3DbqK3NSOlVFQ1FK78K5ACd1GwqGCqfPfVMf79Jv",
        aws_session_token="FwoGZXIvYXdzECAaDCwoY5OHqgV+DeFGEyLGASPvNAlPWYtATHz1oiz7i/BqTzz/eWTnZLrNpAEYbu/OK9keBBfj1BFOsByGuDTy7z8kcgm/Sanx9R4bYknNtergYRwUE3Dd1ERyRoupHUKV5+0kVAOOjzYzRF/dXovOMBVFA5SOfpC4A8NDzan/aQhaWBYKrEPGp7ZoKZflJq1OY7leWCoqMjQo0gxTwM6vJnCdnfEax3XzTU0Po5E8taVOiB6wQLEzlL/VaFmlJChPHZoWnx9azS3eWJNr070EV6SxW6vbAiiInY30BTItw8tkz5qO0AuTvC5iemGR3EJPAQV7IfYR7PSjTDkKKIxayTCdefgk+eSBPgmS",
        region_name='us-east-1'
    )

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('Laptops')
    count = count + 1
    print(count)
    image = div.find("div", {"class": "image"})
    src = image.find("img").get('src')
    src = "https://www.czone.com.pk" + src
    print(src)

    name = div.find('h4').find('a').text
    d.name = name

    print(name)  # including calatgory processor, ram, HDD, size, colour

    # ratings for some products dont exists

    rating = div.find("div", {"class": "star_rating"}).text
    d.rating = rating

    print(rating)

    # code

    code_div = div.find("div", {"class": "product-code no-padding"})

    code = code_div.find("span", {"class": "product-data"}).text

    d.code = code
    print(code)

    # catagory
    category = div.find("div", {"class": "product-category"}).text
    d.category = category

    print(category)

    # description
    description = div.find("div", {"class": "description"}).text
    d.description = description
    print(description)

    # specs list
    specs_list = div.findAll("li")

    specs = []
    for li in specs_list:
        specs.append(li.text)
    # availability in stock
    print(specs)

    d.processor = specs[0]
    d.ram, d.disk = specs[1].split('|')
    d.GraphicCard = specs[2]
    d.display = specs[3]
    availability = div.find("div", {"class": "product-stock"}).text
    d.availability = availability
    print(availability)
    # price

    price = div.find("div", {"class": "price"}).text
    print(price)  # done
    devices.append(d)
    print("")
    print("----------------------------------------------------------------------")
    print("")
    with table.batch_writer() as batch:
        batch.put_item(Item={"Code": d.code, "Name": d.name, "Description": d.description,
                             "Ram": d.ram, "HardDisk": d.disk, "Processor": d.processor, "GraphicCard": d.GraphicCard,
                             "Display": d.display, "Price": price,
                             "Image": src, "Availability": d.availability})