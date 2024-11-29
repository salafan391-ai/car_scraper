class Translate:
    def __init__(self, list_data, translated):
        self.list_data = list_data
        self.list_titles=[i['title'] for i in self.list_data]
        self.words = self.get_unique_words()
        self.check_available_words(translated)
        self.car_raw_data = self.trnslate_all_words(translated, self.list_titles)
    

    def get_unique_words(self):
        words = []
        # Clean and collect unique words
        for i in set(self.list_titles):
            words.extend(i.lower().split())
        return set(words)  # Return the unique words
    
    def is_float(self, string):
        try:
            float(string)
            return True
        except ValueError:
            return False
    
    def check_available_words(self, translated):
        new_words = []
        # Use a set for case-insensitive lookup
        translated_words = {n[0].lower() for n in translated}
        for word in self.words:
            if word.lower() not in translated_words and not self.is_float(word):
                new_words.append(word)
        print(f"New words that need translation: {new_words}")
    
    def get_final_translation(self, translated, idx, car_raw_data):
        car_name_words = car_raw_data[idx].lower().split()
        translated_words = {i[0].lower(): i[1] for i in translated}  # Build a dictionary for fast lookup
        w = []
        
        # Match each word in the car title with the translation
        for word in car_name_words:
            if word in translated_words:
                w.append((word, translated_words[word]))
        
        # Create an order map to maintain original word order
        order_map = {word: index for index, word in enumerate(car_name_words)}
        sorted_list = ' '.join([n[1] for n in sorted(w, key=lambda x: order_map.get(x[0], float('inf')))])
        
        return sorted_list
    
    def trnslate_all_words(self, translated, car_raw_data):
        all_finals = []
        for i in range(len(car_raw_data)):
            all_finals.append(self.get_final_translation(translated, i, car_raw_data))
        
        if len(all_finals) == 0:
            print('All words have been translated successfully.')
        else:
            print(f"{len(all_finals)} car titles have been translated.")
        
        return all_finals
    
    def update_titles(self):
        for k,v in zip(self.list_data,self.car_raw_data):
            k['title'] = v
    
    def __str__(self):
        return f"Translated car data: {self.car_raw_data}"





