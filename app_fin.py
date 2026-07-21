from flask import Flask, render_template, request
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
app = Flask(__name__)

def format_date(date):
    return date.strftime("%B %d, %Y")
today=date.today()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/result", methods=["POST"])
def answers():
    cutoff = request.form["cutoff"]
    grace = int(request.form["grace"])
        
        

    cutoff_date = datetime.strptime(cutoff, "%Y-%m-%d").date()
    pre_date= cutoff_date - relativedelta(months=1)
    
    first_payment = cutoff_date + timedelta(days=grace)
    next_cutoff = cutoff_date + relativedelta(months=1)
    second_payment = first_payment + relativedelta(months=1)
    time_left=(first_payment-today).days
    box=[cutoff_date, pre_date, first_payment, next_cutoff, second_payment]
    for i in range(0, len(box)):
        box[i]=format_date(box[i])
    
    return render_template("new_index.html", cutoff_date=box[0], pre_date=box[1], first_payment=box[2], next_cutoff=box[3], second_payment=box[4], time_left=time_left)




            
if __name__ == "__main__":
    app.run(debug=True)

#2026-07-20
# timedelta(days=20)