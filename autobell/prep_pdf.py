import json
import asyncio
import aiohttp


image="https://img-auction.autobell.co.kr/OBmZCjL58I?src=https%3A%2F%2Fauction.autobell.co.kr%2FFileUpDown%2F2100%2Fcarimg%2F2411%2FB241103560%2FB241103560_02_02.jpg%3F1732520229000&type=m&w=400&h=250&quality=90&ttype=jpg"

# def get_onload_images(id):
#         m=[]
#         for i in range(1):
#             if i < 10:
#                 i= f"0{i}"
#             else:
#                 i=i
#             count=0

#             while count < 32:
#                 count+=1
#                 try:
#                     m.append(f"https://img-auction.autobell.co.kr/OBmZCjL58I?src=https%3A%2F%2Fauction.autobell.co.kr%2FFileUpDown%2F{id[0]}2Fcarimg%2F{id[1]}%2F{id[2]}%2F{id[2]}_02_{count}.jpg%3F{id[3]}{i}&type=m&w=1280&h=800&quality=90&ttype=jpg")
#                 except:
#                     continue
#         return m

def get_onload_images(id):
    images = []
    id_part1, id_part2, id_part3, id_part4 = id  # Unpack for readability
    
    # Generate URLs for the first set of images (_02_)
    for count in range(1, 33):  # From 1 to 32 inclusive
        try:
            padded_count = f"{count:02}"  # Zero-pad the count
            images.append(
                f"https://img-auction.autobell.co.kr/OBmZCjL58I?"
                f"src=https%3A%2F%2Fauction.autobell.co.kr%2FFileUpDown%2F{id_part1}2Fcarimg%2F{id_part2}%2F{id_part3}%2F{id_part3}_02_{padded_count}.jpg%3F{id_part4}01"
                f"&type=m&w=1280&h=800&quality=90&ttype=jpg"
            )
        except Exception as e:
            # Optionally log the exception for debugging
            print(f"Error generating image URL for count {count}: {e}")
    
    # Generate URLs for the second set of images (_02_99_)
    for count in range(1, 14):  # From 1 to 14 inclusive
        try:
            padded_count = f"{count:02}"  # Zero-pad the count
            images.append(
                f"https://img-auction.autobell.co.kr/OBmZCjL58I?"
                f"src=https%3A%2F%2Fauction.autobell.co.kr%2FFileUpDown%2F{id_part1}2Fcarimg%2F{id_part2}%2F{id_part3}%2F{id_part3}_02_99_{padded_count}.jpg%3F{id_part4}01"
                f"&type=m&w=1280&h=800&quality=90&ttype=jpg"
            )
        except Exception as e:
            # Optionally log the exception for debugging
            print(f"Error generating image URL for count {count}: {e}")
    
    return images



def parse_ids(image):
    try:
        id = image.split('2F')[4]
        id1 = image.split('2F')[-1].split('.')[0][:-6]
        id2 = image.split('3F')[-1].split('&')[0]
        id0 = id1[1:5]
        return (id,id0,id1,id2)
    except IndexError:
        return None


async def check_url(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                print(f"URL {url} is valid")
                return url
    except Exception as e:
        print(f"Error checking {url}: {e}")
        return None

async def main(images):
    async with aiohttp.ClientSession() as session:
        tasks = [check_url(session, i) for i in images]
        results = await asyncio.gather(*tasks)
        return results
def run_checker(images):
    results = asyncio.run(main(images))
    return results

id = parse_ids(image)

images = get_onload_images(id)
imgs = run_checker(images)

