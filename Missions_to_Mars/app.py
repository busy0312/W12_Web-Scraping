from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
# Create an instance of Flask
app = Flask(__name__,static_url_path="/css/static/style.css")


# Use PyMongo to establish Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def home():
    # Find one record of data from the mongo database
    # @TODO: YOUR CODE HERE!
    destination_data = mongo.db.destinations.find_one()
    # Return template and data
    return render_template("index.html", vacation=destination_data)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    # Run the scrape function and save the results to a variable 
    mars_data = scrape_mars.scrape_all()

    # Update the Mongo database using update and upsert=True
    mongo.db.destinations.update({}, mars_data, upsert=True)
    # Redirect back to home page
    return redirect("/")
if __name__ == "__main__":
    app.run(debug=True)

