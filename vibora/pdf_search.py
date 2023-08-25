from duckduckgo_search import ddg, ddg_videos, ddg_answers, ddg_news

# search in the web for pdf files
def pdf_search(theme):
    words = theme.split()
    last_word = words[-1]

    keywords = ' '.join(words[:-1]) + f"{last_word}:pdf" # self explanatory....
    print(keywords)
    max_files = 3 # define number of pdf files result
    print(max_files)
    result = ddg(keywords, safesearch='Off', max_results=max_files)
    for i in range(max_files):
        response = f"I found this pdf for {theme}: {result[i]['title']}"
        print(response)