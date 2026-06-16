from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome FastAPI!"}

@app.get("/about")
def about():
    return {"message": "This is a simple E-Commerce website."}

@app.get("/contact")
def contact():
    return {"message": "Contact us at Linkedn"}

@app.get("/products")
def products():
    return {"message": "Here are our products."}

@app.get("/cart")
def cart(): 
    return {"message": "Your shopping cart is empty."}

@app.get("/checkout")
def checkout():
    return {"message": "Proceed to checkout."} 