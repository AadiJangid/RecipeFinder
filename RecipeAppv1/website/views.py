from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_required, logout_user
import requests
import json
import pprint

views = Blueprint('views', __name__)

@views.route('/', methods = ['GET', 'POST'])
@login_required
def home():

    url = "https://api.edamam.com/search?q=&app_id=51deaba7&app_key=7c0785c328e50c3af99f7548b792d3ab"
    #response = requests.get(url)
    #print(response.content)

    if request.method == 'POST':
        generalSearch = request.form.get('generalSearch')
        ingredients = request.form.get('ingredientsList')
        diet = request.form.get('diet')
        cuisine = request.form.get('cuisine')
        meal = request.form.get('meal')

        ingredientsList = ingredients.split(',')
        for word in ingredientsList:
            word = word.lower()

        url= "https://api.edamam.com/search?q=" + generalSearch.strip() + "&app_id=51deaba7&app_key=7c0785c328e50c3af99f7548b792d3ab&from=0&to=6&diet=" + diet.lower() + "&cuisineType=" + cuisine.lower() + "&mealType=" + meal.lower()
        response = requests.get(url)
        result = response.json()
        #pprint.pprint(json.dumps(result))
        #result[hits][recipe][label] <- Title
        #result[hits][recipe][image] <- Image
        #result[hits][recipe][url] or shareAs
        #result[hits][recipe][ingredients] <- List [text]
        #in more than one hit, repeats on {recipe, }

        resultList = []

        for recipe in result['hits']:
            match = False
            for ingredient in recipe['recipe']['ingredients']:
                for elem in ingredientsList:
                    if elem in ingredient['text']:
                        match = True
                
            if match:
                resultList.append([recipe['recipe']['label'], recipe['recipe']['image'], recipe['recipe']['shareAs']])

        

        return render_template('result.html', user = current_user, resultList = resultList)

    return render_template('home.html', user=current_user)


@views.route('/wishlist', methods=['GET', 'POST'])
@login_required
def wishlist():

    return render_template('wishlist.html', user = current_user)

@views.route('/logout', methods = ['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('auth.login'))




