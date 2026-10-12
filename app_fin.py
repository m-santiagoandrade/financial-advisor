from flask import Flask, render_template, request
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
app = Flask(__name__)

def format_date(date):

    months = {
        "January": "enero",
        "February": "febrero",
        "March": "marzo",
        "April": "abril",
        "May": "mayo",
        "June": "junio",
        "July": "julio",
        "August": "agosto",
        "September": "septiembre",
        "October": "octubre",
        "November": "noviembre",
        "December": "diciembre"}
    month=date.strftime("%B")
    return f"{date.day} de {months[month]} de {date.year}"

def mistakes(route):
        return f'No es posible calcular tu meta con los datos ingresados. Algunos valores son negativos o no son compatibles con tu situación financiera. Por favor, revisa tus ingresos, gastos y el monto de tu meta e inténtalo de nuevo.. <a href="{route}"> Presiona para volver </a>'
@app.route("/cutoff")
def start():
    return render_template("index.html")

@app.route("/result", methods=["POST"])
def answers():
    today=date.today()

    cutoff = request.form["cutoff"]
    try:
        grace = int(request.form["grace"])
        cutoff_date = datetime.strptime(cutoff, "%Y-%m-%d").date()

    except ValueError:
        response=mistakes("/cutoff") #calls function to return an error message
        return response

    pre_date= cutoff_date - relativedelta(months=1)
    
    first_payment = cutoff_date + timedelta(days=grace)
    next_cutoff = cutoff_date + relativedelta(months=1)
    second_payment = first_payment + relativedelta(months=1)
    #The statement closing date has passed
    if today<cutoff_date:
        time_left=(first_payment-today).days
    else:
         time_left=(second_payment-today).days
    box=[cutoff_date, pre_date, first_payment, next_cutoff, second_payment]
    for i in range(0, len(box)):
        box[i]=format_date(box[i])
    
    return render_template("new_index.html", cutoff_date=box[0], pre_date=box[1], first_payment=box[2], next_cutoff=box[3], second_payment=box[4], time_left=time_left)

@app.route("/")
def home():
     return render_template("home_screen.html")

def remaining_or_exceedent(amount, months, years): 
     return amount*(months+years*12)
@app.route("/principal", methods=["GET", "POST"])
def compute():
    remaining_amount=0
    excedent=0
    p=True
    if request.method=="GET":
          return render_template("computing_index.html")
    try:
        anual_income=int(request.form["anual_income"])
        current_savings=int(request.form["current_savings"])
        fixed_expenses=int(request.form["fixed_expenses"])
        goal_cost=int(request.form["goal_cost"])
        percentage=(100-(int(request.form["percentage"])))/100
        monthly_income=round(anual_income/12) # monthly_income is fixed_expenses and money to hangout
        real_monthly_income=monthly_income-fixed_expenses
        amount_to_save=round((real_monthly_income)*percentage) 
        real_goal=goal_cost-current_savings
        time_to_afford=round(real_goal/amount_to_save)
        years_to_afford=int(time_to_afford//12)
        months_to_afford=int(time_to_afford%12)
        spendable_money=round(real_monthly_income-amount_to_save)
        if time_to_afford<0 or amount_to_save<0 or spendable_money<0 or years_to_afford<0 or months_to_afford<0:
                     return (mistakes("/principal"))
        elif (remaining_or_exceedent(amount_to_save, months_to_afford, years_to_afford))<real_goal:
            remaining_amount=real_goal-(remaining_or_exceedent(amount_to_save, months_to_afford, years_to_afford))
            return description(time_to_afford, amount_to_save, spendable_money, years_to_afford, months_to_afford, remaining_amount, p)
        else:
            excedent= remaining_or_exceedent(amount_to_save, months_to_afford, years_to_afford)-real_goal
            p=False    
            return description(time_to_afford, amount_to_save, spendable_money, years_to_afford, months_to_afford, excedent, p )

    except ValueError:
        return (mistakes("/principal"))

def description(time_to_afford, amount_to_save, spendable_money, years_to_afford, months_to_afford, x,p): # x as remaining or excedent
         return render_template("description_index.html", time_to_afford=time_to_afford, amount_to_save=amount_to_save, spendable_money=spendable_money, years_to_afford=years_to_afford, months_to_afford=months_to_afford, x=x, p=p)
            
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)


     

            
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

