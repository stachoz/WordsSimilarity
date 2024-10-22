import WordsListScrapper

def main():
    url = "http://pl.talkenglish.com/vocabulary/top-500-adjectives.aspx"
    scrapper = WordsListScrapper.WebPageFetcher(url)
    words = scrapper.getScrappedWords()
    print(len(words))

if __name__ == '__main__':
    main()

