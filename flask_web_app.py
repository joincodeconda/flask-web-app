from flask import Flask, render_template, request

app = Flask(__name__)

def is_prime(number):
    if number == 1:
        return False
    elif number == 2:
        return True
    else:
        for i in range(2, number):
            if number % i == 0:
                return False
        return True

@app.route("/", methods=("GET", "POST"))
def home_page():
    result = ""
    if request.method == "POST":
        number = int(request.form["number"])
        if number < 1:
            result = "Please enter a number greater than 0."
        elif is_prime(number):
            result = "{} is a prime number!".format(number)
        else:
            result = "{} is NOT a prime number.".format(number)
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run()