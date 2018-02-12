
def add_punctuation():
    with open("001.no_punctuation_urls.txt", "r") as f:
        urls_list = f.readlines()
        for line in urls_list:
            if line:
                line1 = line.replace("https", "\"https")
                line2 = line1.replace("\n", "\",\n")
                with open("001.add_punctuation_urls.txt", "a+", encoding="utf-8") as f:
                    f.write(line2)
            else:
                break

if __name__ == '__main__':
    add_punctuation()








