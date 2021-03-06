from selenium import webdriver as wd
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup as bs

options = Options()
options.headless = True  # set the option "headless" for the web driver
driver = wd.Firefox(options=options)  # configure webdriver to use Firefox browser

def more_articles(p):
    driver.get(p)
    content = driver.page_source
    soup = bs(content, "html.parser")
    tmpArticles = []

    print(p)
    for a in soup.find_all(class_="btn", href=True):
        if a.text and "/Science_Exploration/Human_and_Robotic_Exploration/" in a['href']:
            tmpArticles.append("https://www.esa.int" + a['href'])

    return tmpArticles


def esa_scraper(p):
    """Function used to scrape and find the articles indexed in the ESA web pages
        @:param p the page to scrape
        @:return tmpArticles temporary list of ESA articles"""

    driver.get(p)  # to obtain a specified web page
    content = driver.page_source  # get the page content
    soup = bs(content, "html.parser")
    tmpArticles = []  # list of articles links for this site

    for a in soup.find_all(class_="story", href=True):  # obtain <a> class for the articles
        if a.text:
            tmpArticles.append(a['href'])  # to get the "href" value

    tmpArticles = [p[:19] + i for i in tmpArticles]  # list of links retrieved from esa web page

    return tmpArticles


def bo_scraper(p):
    """Function used to scrape and find the articles indexed in the Blue Origin web page
        @:param p the page to scrape
        @:return tmpArticles temporary list of Blue Origin articles"""

    driver.get(p)  # to obtain a specified web page
    content = driver.page_source  # get the page content
    soup = bs(content, "html.parser")
    tmpArticles = []  # list of articles links for this site

    for a in soup.find_all(class_="NewsArchive__postTitleLink", href=True):  # obtain <a> class for the articles
        if a.text:
            tmpArticles.append(a['href'])  # to get the "href" value

    tmpArticles = [p + i[8:] for i in tmpArticles]  # list of links retrieved from Blue Origin web page

    return tmpArticles


def space_com_scraper(p):
    """Function used to scrape and find the articles indexed in the Space.com web pages
        @:param p the page to scrape
        @:return tmpArticles temporary list of Space.com articles"""

    driver.get(p)  # to obtain a specified web page
    content = driver.page_source  # get the page content
    soup = bs(content, "html.parser")
    tmpArticles = []  # list of articles links for this site

    for a in soup.find_all(class_="article-link", href=True):  # obtain <a> class for the articles
        if a.text:
            tmpArticles.append(a['href'])  # to get the "href" value

    return tmpArticles


def write_to_file(links_articles, file_name):
    """Function used to write down to one file all the links got from the scrapers
        @:param links_articles list of the articles to index
        @:param file_name name of links file"""

    try:
        with open(file_name, "r") as file:
            lines = file.readlines()
            n_links = len(lines)  # number of links
            lines[0] = str(n_links)+"\n"  # add the number of previous links at the beginning of the file

        with open(file_name, "w") as file:
            file.writelines(lines)  # write all the previous links

        with open(file_name, "r+") as file:     # try to open the file to update it
            for link in links_articles:     # search in the file if the link is present
                for line in file:
                    if link in line:
                        break

                else:   # not found, we are at the eof
                    file.write(link)    # append missing link
                    file.write("\n")

                file.seek(0)    # return the pointer at the beginning of the file

    except FileNotFoundError:   # if the file doesn't exists it will be created
        with open(file_name, "w") as file:
            file.write("0\n")

        write_to_file(links_articles, file_name)    # recall the function to write for the first time the file


def esa_iteration(dic_cat, root, links_articles):
    for cat in dic_cat:
        for k in range(dic_cat[cat]):
            links_articles.extend(esa_scraper(root.replace("(archive)/", cat) + "(archive)/" + str(k * 50)))


def main():
    """Main function to start the whole scraping action"""

    root_esa = "https://www.esa.int/Science_Exploration/Human_and_Robotic_Exploration/(archive)/"  # root of ESA website
    root_bo = "https://www.blueorigin.com/news/"  # root page of Blue Origin website
    root_space_com = "https://www.space.com/spaceflight/"  # root page of Space.com website

    links_articles = []  # list of all articles links

    links_file = "links.txt"   # name of the links file

    esa_counter = 36  # index used to set the max page of ESA articles
    space_com_counter = 9  # index used to set the max page of Space.com articles
    """
    for k in range(esa_counter):
        links_articles.extend(
            esa_scraper(root_esa + str(k * 50)))  # adding the links retrieved from the first "i" ESA pages
    """
    sub_cat = {"Exploration/": 5, "Exploration/ExoMars/": 2, "Mars500/": 3, "PromISSe/": 1, "MagISStra/": 2,
               "Futura/": 1, "Education/": 5, "Research/": 9, "Astronauts/": 9, "Blue_Dot/": 1, "AstroLab/": 2,
               "OasISS_Mission/": 2, "Exploration/Orion/": 1, "concordia/": 1}

    # esa_iteration(sub_cat, root_esa, links_articles)

    #for cat in sub_cat:
    links_articles.extend(
        esa_scraper(root_esa.replace("(archive)/", "Concordia/") + "(archive)/"))
        
    links_articles.extend(more_articles(root_esa.replace("(archive)/", "Concordia/")))
    # links_articles.extend(bo_scraper(root_bo))  # adding the links retrieved from the Blue Origin page
    """
    for k in range(1, space_com_counter+1):
        links_articles.extend(
            space_com_scraper(root_space_com + str(k)))  # adding the links retrieved from the first "i" Space.com pages
    """
    write_to_file(links_articles, links_file)   # create or update links file


if __name__ == "__main__":
    main()
