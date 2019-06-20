from flask import Flask, render_template, request
app = Flask(__name__)
from rapidconnect import RapidConnect
import urllib.request as urllib2
from bs4 import BeautifulSoup
import json
import re
import os
from load import *
ratings = []
legit_stuff = []
stripped_menu = []
def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        # If value has not been encountered yet,
        # ... add it to both list and set.
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output



@app.route("/")
def index():
    return render_template("index.html")
'''@app.route("/dostuff",methods = ["GET","POST"])
def dostuff():
    return str(final_stuff)'''
@app.route("/dawgstuff",methods = ["GET","POST"])
def dawgstuff():
    r2 = str(request.get_data())
    print(r2)
    pagina = "https://www.allmenus.com/custom-results/-/ca/san-jose/" + r2[1:]
    print(pagina)
    pg = urllib2.urlopen(pagina)
    sopa = BeautifulSoup(pg,"html.parser")
    thelinks = sopa.findAll("a", {"data-masterlist-id" : re.compile(r".*")})
    print(thelinks)
    da_str = str(thelinks[0])
    #print(re.search(r'\"\.+\"',da_str).group(0))
    start = da_str.index("/ca/")
    end = da_str.index("/menu/") + 6
    da_str = da_str[start: end]
    print(da_str)


    quote_page = "https://www.allmenus.com" + da_str
    #https://www.allmenus.com/ca/san-jose/216536-mcdonalds/menu/
    print(quote_page)
    page = urllib2.urlopen(quote_page)
    soup = BeautifulSoup(page, 'html.parser')
    titles = soup.find_all("span",attrs = {'class':'item-title'})
    print(titles)
    ingredients = soup.find_all("p",attrs = {'class':'description'})
    print(ingredients)


    counter = 0


    class total_values:
        fat =  65
        carbs =  300
        protein =  50
        sodium = 2.4

        def function(self):
            pass

    class ideal_values:
        fat = total_values.fat/3
        carbs = total_values.carbs/3
        protein = total_values.protein/3

    for i in range(0,len(titles)):
        print(i)
        print(titles[i].get_text())
        print(ingredients[i].get_text())
        stripped_menu.append(titles[i].get_text() + ": " + ingredients[i].get_text())

    #print(stripped_menu)


    parsed_titles = []
    for title in titles:
        parsed_titles.append(title)
    print(parsed_titles)
    parsed_titles = remove_duplicates(parsed_titles)
    print(parsed_titles)
    rapid = RapidConnect("d_562854dae4b049ee93f17049", "1d71d14a-e7c0-478c-9635-f76b62490adb")
    for i in range(0,len(parsed_titles)):
        food = parsed_titles[i]
        print(food)
        counter+=1
        if counter>5:
            break
        result = rapid.call('Nutritionix', 'getFoodsNutrients', {
            'applicationSecret': '8594e772f2b653ab072e04d6a5feb6e0',
    	    'foodDescription': food,
    	    'applicationId': '444f4a33'
            })

        print(result)
        if "We couldn't match any of your foods" in str(result):
            pass
        else:
            info = result[0]["foods"][0]
            print(info["food_name"])
            #print("Sodium: " + str(info["nf_sodium"]))
            print("fat: " + str(info["nf_total_fat"]))
            print("carbohydrates: " + str(info["nf_total_carbohydrate"]))
            print("protein: " + str(info["nf_protein"]))
            #sodium = info["nf_sodium"] aayush says something abuot iterations in presentaion
            fat = info["nf_total_fat"]
            carbs = info["nf_total_carbohydrate"]
            protein = info["nf_protein"]
            rating = (abs(0.33 - fat/ideal_values.fat) + abs(0.33-carbs/ideal_values.carbs) +  abs(0.33 - protein/ideal_values.protein))
            ratings.append([stripped_menu[i],rating])
    print(ratings)
    sorted_ratings = sorted(ratings, key=lambda x: x[1])
    final_stuff = sorted_ratings
    return str(final_stuff)


if __name__ == '__main__':
    port = int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port = port)
