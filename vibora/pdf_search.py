from duckduckgo_search import ddg, ddg_videos, ddg_answers, ddg_news

# search in the web for pdf files
def pdf_search(theme):
    words = theme.split()
    last_word = words[-1]

    keywords = ' '.join(words[:-1]) + f"{last_word}:pdf" # self explanatory....
    print(keywords)
    max_files = 10 # define number of pdf files result
    print(max_files)
    result = ddg(keywords, safesearch='Off', max_results=max_files)
    print(f"\nI found these results for '{theme}' I think are most relevant based on what you want:\n")
    for i in range(max_files):
        response = f"{result[i]['title']}\n{result[i]['href']}\n"

        print(response)
    print("") # empty line at the bottom to give results some space :) it needs some air