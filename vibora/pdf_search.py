from duckduckgo_search import ddg, ddg_videos, ddg_answers, ddg_news

# search in the web for pdf files
def pdf_search(theme):
    words = theme.split()
    last_word = words[-1]

    keywords = ' '.join(words[:-1]) + f"{last_word}:pdf" # self explanatory....
    print(keywords)

    result = ddg(keywords, safesearch='Off', max_results=1)
    response = f"I found this pdf for {theme}: {result}"
    print(response)