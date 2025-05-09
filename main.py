from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask import flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///household_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = "your_secret_key"  # Set a secret key for session management
db = SQLAlchemy(app)


class DietModel(db.Model):
    __tablename__ = 'diet'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    measure = db.Column(db.String, nullable=False)
    serving_adult = db.Column(db.Float, nullable=False)
    serving_child = db.Column(db.Float, nullable=False)
    serving_infant = db.Column(db.Float, nullable=False)
    food_type = db.Column(db.String, nullable=False)
    food_group = db.Column(db.String, nullable=False)
   
@app.route('/')
def index():
    return render_template('index.html')

    
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        adult = request.form.get('adult').strip()
        child = request.form.get('child').strip()
        infant = request.form.get('infant').strip()
        session['people'] = {
            'adult': adult,
            'child': child,
            'infant': infant
        }
        
        return redirect("/instructions")
    session.clear()
    return render_template('main.html')


@app.route('/instructions')
def instructions():
    return render_template('instructions.html')

@app.route('/meals/add')
def meals():
    data = DietModel.query.all()
    session['diet'] = {}
    for meal in data:
        if meal.food_group in session['diet']:
            session['diet'][meal.food_group.strip()].append(meal.food_type)
        else:
            session['diet'][meal.food_group.strip()] = [meal.food_type]
    return render_template('meals.html')

@app.route('/meals/add/new', methods=['GET', 'POST'])
def addMeal():
    if request.method == 'POST':
        day = request.form.get('day').strip()
        meal_time = request.form.get('meal_time').strip()
        foodlist = request.form.getlist('food')
        # day, mealtime, foodgroup, measure, totalA, totalC, totalI, totalF, food_type
        
        food = [[day, meal_time]]
        i = 0
        for food_item in foodlist:
            diet = DietModel.query.filter_by(food_type=food_item).first()
            if diet:
                child = diet.serving_child * float(session['people']['child'])
                infant = diet.serving_infant * float(session['people']['infant'])
                adult = diet.serving_adult * float(session['people']['adult'])
                family = adult + child + infant
                if i == 0:
                    for item in [diet.food_group, diet.measure, adult, child, infant, family, food_item]:
                        food[0].append(item)
                else:
                    food.append(["", "", diet.food_group, diet.measure, adult, child, infant,family, food_item])
                    
            i = i + 1
        session['food'] = food
        return redirect('/meal/plan')
    
    return redirect('/meals/add')


@app.route('/get-food')
def get_food_data():
    if 'food' in session:
        return jsonify(session['food'])
    return jsonify({'error': 'No food data found'})

@app.route('/get-food/table')
def get_food_table():
    if 'food' in session:
        printTable = []
        food_data = session['food']
        prev = ""
        for item in food_data:
           
            if item[2] not in prev:
                prev = item[2]
                printTable.append([item[2], item[8], item[7], (item[7])/1000])
            else:
                printTable.append(["", item[8], item[7], (item[7])/1000])
                
        print(printTable)
        return jsonify( printTable)
    return jsonify({'error': 'No food data found'})

@app.route('/meal/plan')
def mealPlan():
    
    return render_template('meal.plan.html')

@app.route('/meal/plan/add/basket')
def foodBasket():
    return render_template('food.basket.html')

@app.route('/capture/data/', methods=['GET', 'POST'])
def captureData():
    if request.method == 'POST':
        # Here you would typically save the data to a database or perform some action
        foodtype = request.form.get('food_type')
        foodgroup = request.form.get('food_group')
        measure = request.form.get('measure')
        serving_adult = request.form.get('serving_adult')
        serving_child = request.form.get('serving_child') 
        serving_infant = request.form.get('serving_infant')
        
        new_entry = DietModel(measure=measure, serving_adult=serving_adult, serving_child=serving_child, serving_infant=serving_infant, food_type=foodtype, food_group=foodgroup)
        db.session.add(new_entry)
        db.session.commit()
        flash('Data captured successfully!', 'success')

        
    food = DietModel.query.all()
    return render_template('capture.data.html', food=food)

@app.route('/capture/data/delete/<id>')
def delete_data(id):
    entry = DietModel.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    flash('Data deleted successfully!', 'success')
    return redirect(url_for('captureData'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
