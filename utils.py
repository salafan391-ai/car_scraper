from transelations import translated_models,colors,missions,feul,make_model_translated
from junks import junks
import re
import logging

def filter_cars_by_year(data):
    return [car for car in data if car.get('year', 0) > 2019]


def translate_words(word, filtered_cars, translated_dict):
    translation_map = {original: translated for original, translated in translated_dict}
    for car in filtered_cars:
        if car[word] in translation_map:
            car[word] = translation_map[car[word]]


def get_set_words(filtered_cars, word, translated_dict):
    translations = {i[0] for i in translated_dict}
    return {car[word] for car in filtered_cars if car[word] not in translations}


def get_make(filtered_cars, translated):
    make = []
    for i in filtered_cars:
        cleaned_title = i.get('title', '').split()[0]  # Safely get the first word of 'title'
        if cleaned_title not in [i[0] for i in translated]:
            make.append(cleaned_title)
        else:
            make.append('Unknown')  # Assign a default value if the make is already in translated
    return make


# def proccess_model(filtered_cars, make, translated):
#     untranslated_models = []  # List to collect untranslated models
    
#     for car, m in zip(filtered_cars, make):
#         car['make'] = m  # Assign make

#         # Ensure 'title' exists and is a string
#         car_title = car.get('title', [])
        
#         # If 'title' is a string, split it, otherwise assume it's already a list
#         if isinstance(car_title, str):
#             car['title'] = car_title.split()[1:] if car_title else []
#         elif isinstance(car_title, list):
#             car['title'] = car_title  # Keep it as a list if it is already a list
        
#         # Check if any word in 'title' is not translated
#         for word in car['title']:
#             if word not in junks:  # If word is not in translated list
#                 untranslated_models.append(word)

#         # Assign 'model' based on the title or use make if no translation is found
#         model = next((word for word in car['title'] if word in {i[0] for i in translated}), car['make'])
#         car['model'] = model
    
#     return set(untranslated_models)  # Return unique untranslated models


def proccess_data(filtered_cars):
    # Translating non-English fields to standardized terms
    print("Fuel Types:", get_set_words(filtered_cars, 'feul', feul))
    print("Missions:", get_set_words(filtered_cars, 'mission', missions))
    print("Colors:", get_set_words(filtered_cars, 'color', colors))
    # Process models, then apply translations
    translate_words('feul', filtered_cars, feul)
    translate_words('mission', filtered_cars, missions)
    translate_words('color', filtered_cars, colors)
   

def extract_wheel_drive_patterns(text):
    """
    Extracts wheel drive patterns (e.g., 2WD, AWD, 4WD) from a given text.

    Args:
        text (str): The input text.

    Returns:
        list: A list of extracted wheel drive patterns as strings.
    """
    pattern = r'\b(?:\dWD|AWD)\b'  # Matches patterns like 2WD, 4WD, AWD
    return re.findall(pattern, text)



def extract_seat_patterns(text):
    """
    Extracts patterns like '15인승', '9인승', '9인승프레스티지', or '11-seater', etc.,
    from a given text where the pattern might be followed by other characters.

    Args:
        text (str): The input text.

    Returns:
        list: A list of extracted patterns as strings.
    """
    pattern = r'\b(?:\d+인승\w*|\d+-seater)\b'  # Matches patterns like 15인승, 9인승, 9인승프레스티지, or 11-seater
    return re.findall(pattern, text)


def extract_vehicle_keywords(text):
    """
    Extracts specific vehicle-related keywords in both English and Korean from a given text.

    Args:
        text (str): The input text.

    Returns:
        list: A list of extracted keywords.
    """
    # List of keywords in both languages
    keywords = [
        'signature', 'trendy','TURBO','Ⅱ', 'Ⅲ', '고급형', '고소작업차', '그란스포츠', '그래비티', '그랜드플래티넘','컨버터블',
        '기본', '기본형', '노블레스', '노블레스_22MY', '다목적', '더블캡', '디럭스', '디럭스팩', '라이트','올뉴',
        '럭셔리', '럭셔리_렌터카', '레드라인', '레인지', '렌터카', '르블랑', '리미티드', '리빅', '마스터',
        '마스터즈', '마제스티', '모던', '모던베이직', '밴', '법인전용', '베스트셀렉션Ⅰ', '베스트셀렉션Ⅱ',
        '블랙에디션', '샤인', '셀렉션', '셀렉션Ⅰ', '슈퍼캡', '스마트', '스마트(렌터카용)', '스타일',
        '스탠다드', '스페셜', '스폐셜', '스포츠', '스포트백', '시그니처', '시그니처_보조사양미적용',
        '시그니쳐', '싱글모터', '아방가르드', '어드밴스', '어드벤처', '어스', '없음', '에디션', '에센셜',
        '에어', '에코', '엘리트', '영업용', '와일드', '윙바디', '익스클루시브', '인스크립션', '인스퍼레이션',
        '자가용', '전동식', '전동유압식', '조이', '초이스', '초장축', '캘리그래피', '코어', '콰트로',
        '쿠페', '클래식', '킹캡', '택시형', '터보', '투어링', '트렌디', '트렌디', '렌터카','특판스페셜',
        '파노라믹', '파리', '패밀리', '패키지', '퍼포먼스', '표준캡', '프레스트지', '프레스티지',
        '프레지던트', '프리미어', '프리미엄', '프리미엄초이스', '프리미에르', '플래티넘', '플래티넘Ⅰ',
        '플래티넘Ⅱ', '플래티넘Ⅲ', '플러스', '플럭스', '필', '하이브리드', '(150마력)', '(E)', '(렌터카)',
        '리프', '프레지던트', '1.4TSI', '모던',
         '2.5T', '2.5VGT', '3.5T', '스마트',
        '40', '4DOOR', '4M', '4MATIC', '4Matic', '4매틱',
        '인스퍼레이션', '프레스티지', 'AB', 'ACC', 'ACTIV', 'AT',
        'AWD', 'Blanc', 'CHOICE', 'CRDI', 'Choice', 'DLX', 'E220d', 'E3', 'EV', 'Exclusive', 'F/L', 'FLUX',
        'GL', 'GLS', 'GT', 'HI', 'INSPIRATION', 'L', 'LE', 'LONG', 'LS', 'LT', 'LT코어', 'LUXURY', 'Line',
        'L라이트', 'MODERN', 'Modern', 'M스포츠', 'N', 'Noblesse', 'PREMIER', 'PREMIERE', 'PREMIUM',
        'PRESTIGE', 'Plus', 'Premium', 'Prestige', 'R-플러스', 'RE', 'RS', 'SE', 'SE(렌터카용)', 'SIGNATURE',
        'SMART', 'SPECIAL', 'SPORT', 'STYLE', 'Smart', 'T', 'T7', 'Trendy', 'Type',
        'VAN', 'VIP','1톤','즈','e-','베스트','All', 'New','Special Features','뉴','스마트','THE','Basic','뉴','(19년~현재)','롱 레인지',
        'TM','(DN8)','(CN7)','AD','(J120)','(KA4)','(NX4)','(MQ4)','신형','더 볼드','더 마스터','더','IG','(DL3)'
        
    ]

    # Create a regex pattern to match any of the keywords
    pattern = r'\b(?:' + '|'.join(re.escape(keyword) for keyword in keywords) + r')\b'
    
    # Find all matches
    return re.findall(pattern, text, flags=re.IGNORECASE)

def extract_fuel_types(text):
    """
    Extracts fuel types (e.g., Gasoline, Diesel, Hybrid, 가솔린, 디젤, 하이브리드) from a given text.

    Args:
        text (str): The input text.

    Returns:
        list: A list of extracted fuel types as strings.
    """
    # Define fuel keywords in English and Korean
    fuel_keywords = [
        "Gasoline", "Diesel", "Hybrid", "Electric", "LPG", 
        "가솔린", "디젤", "하이브리드", "전기", "LPG"
    ]
    
    # Create a regex pattern to match any of the keywords
    pattern = r'\b(?:' + '|'.join(re.escape(keyword) for keyword in fuel_keywords) + r')\b'
    
    # Find all matches
    return re.findall(pattern, text, flags=re.IGNORECASE)





def extract_number_of_people(text):
    """
    Extracts patterns like '3인', '5인', '9인' (numbers followed by '인') from a given text.

    Args:
        text (str): The input text.

    Returns:
        list: A list of extracted patterns as strings.
    """
    pattern = r'\b\d+인\b'  # Matches numbers followed by '인'
    return re.findall(pattern, text)


def extract_door_patterns(text):
    """
    Extracts patterns like '5도어', '3도어' (numbers followed by '도어') from a given text.

    Args:
        text (str): The input text.

    Returns:
        list: A list of extracted patterns as strings.
    """
    pattern = r'\b\d+도어\b'  # Matches numbers followed by '도어'
    return re.findall(pattern, text)



def extract_generation_patterns(text):
    """
    Extracts patterns like '3세대', '4세대', '5세대' (numbers followed by '세대') from a given text.

    Args:
        text (str): The input text.

    Returns:
        list: A list of extracted patterns as strings.
    """
    pattern = r'\b\d+세대\b'  # Matches numbers followed by '세대'
    return re.findall(pattern, text)



def extract_year_patterns(text):
    """
    Extracts patterns like 'AD18년~현재', '2세대18년~현재', '카니발18년~현재', 
    '볼드18년~21년', '15년~20년', '20년', '3세대19년~', etc., from a given text.
    
    Args:
        text (str): The input text.
    
    Returns:
        list: A list of extracted patterns as strings.
    """
    # Regex now includes models like '3세대19년~', and other year-related patterns
    pattern = r'\b\w+?\d{2}년~\d{2}년\b|\b\w+?\d{2}년~현재\b|\b\d{2}년~\d{2}년\b|\b\d{2}년\b|\b\w+?\d{2}년~\b'  # Matches ranges and model years
    return re.findall(pattern, text)
def extract_decimal_numbers(text):
    """
    Extracts decimal numbers (e.g., 1.6, 2.3, 2.0T) from a given text.

    Args:
        text (str): The input text.

    Returns:
        list: A list of extracted decimal numbers as strings.
    """
    pattern = r'\b\d+\.\d+[A-Za-z]?\b'  # Matches numbers like 1.6, 2.3, 2.0T
    return re.findall(pattern, text)





def extract_cc_patterns(text):
    """
    Extracts patterns like '2000cc', '2500cc', 'LPG3000cc', '가솔린2500cc', etc., from a given text.

    Args:
        text (str): The input text.

    Returns:
        list: A list of extracted patterns as strings.
    """
    pattern = r'\b\w*?\d+cc\b'  # Matches optional text followed by numbers and 'cc'
    return re.findall(pattern, text.lower())




def process_title(data):   
    for i in data:
        # Clean title by removing unwanted characters
        i['title'] = i['title'].replace('+', '')
        
        # Extract different patterns
        seats = extract_seat_patterns(i['title'])
        people = extract_number_of_people(i['title'])
        wheel = extract_wheel_drive_patterns(i['title'])
        points = extract_decimal_numbers(i['title'])
        shape = extract_year_patterns(i['title'])
        doors = extract_door_patterns(i['title'])
        features = extract_vehicle_keywords(i['title'])
        fuel = extract_fuel_types(i['title'])
        cc = extract_cc_patterns(i['title'])
        generation = extract_generation_patterns(i['title'])

        # Assign extracted values to dictionary
        i['seats'] = seats[0] if seats else ''
        i['people'] = people[0] if people else ''
        i['wheel'] = wheel[0] if wheel else ''
        i['points'] = points[0] if points else ''
        i['shape'] = shape[0] if shape else ''
        i['doors'] = doors[0] if doors else ''
        i['fuel_type'] = fuel[0] if fuel else ''
        i['generation'] = generation[0] if generation else ''
        i['cc'] = cc[0] if cc else ''
        i['features'] = ' '.join(features) if features else ''
        
        
        # Remove extracted patterns from the title
        to_remove = seats + people + wheel + points + shape + features + doors + generation + fuel+ cc
        for pattern in sorted(to_remove, key=len, reverse=True):  # Remove longer patterns first
            if pattern:
                i['title'] = i['title'].replace(pattern, '').strip()
        # Final cleanup of extra spaces
        i['title'] = ' '.join(i['title'].split())





def extract_vehicle_model(text):
    """
    Extracts specific vehicle-related keywords in both English and Korean from a given text.

    Args:
        text (str): The input text.

    Returns:
        list: A list of extracted keywords.
    """
    # List of keywords in both languages
    keywords = [i[0] for i in translated_models]
    # Create a regex pattern to match any of the keywords
    pattern = r'\b(?:' + '|'.join(re.escape(keyword) for keyword in keywords) + r')\b'
    
    # Find all matches
    return re.findall(pattern, text, flags=re.IGNORECASE)


def process_model(data):
    for i in data:
        i['models'] = extract_vehicle_model(i['title'])
    unextracted_models = []
    for i in data:
        if not i['models']:
            unextracted_models.append(i['title'])
        else:
            i['models'] = i['models'][0].strip()
    print('Unextracted Models:', set(unextracted_models))
         
     
    # for i in data:
    #     for n in translated_models:
    #         if i['models'] == n[0]:
    #             i['models'] = n[1]
    #             break