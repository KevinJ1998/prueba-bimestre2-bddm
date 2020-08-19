import requests
from bs4 import BeautifulSoup
# Import MongoClient from pymongo so we can connect to the database
from pymongo import MongoClient




if __name__ == '__main__':
    # Instantiate a client to our MongoDB instance
    db_client = MongoClient()
    bdd3 = db_client.bdd3
    webscrapping = bdd3.webscrapping


    response = requests.get("https://cnnespanol.cnn.com/")
    soup = BeautifulSoup(response.content, "lxml")

    post_titles = soup.find_all("h2", class_="news__title")

    extracted = []
    for post_title in post_titles:
        extracted.append({
            'title' : post_title.a["title"],
            'link'  : post_title.a['href']
        })

    # Iterate over each post. If the link does not exist in the database, it's new! Add it.
    for post in extracted:
        if db_client.bdd3.webscrapping.find_one({'link': post['link']}) is None:
            # Let's print it out to verify that we added the new post
            print("Found a new listing at the following url: ", post['link'])
            db_client.bdd3.webscrapping.insert(post)

   
    

