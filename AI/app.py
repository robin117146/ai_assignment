
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from models.user_model import User
import re
import openai
import random
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# OpenAI API Key (Replace with your key)
openai.api_key = "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"

@app.route('/')
def home():
    return render_template('index.html', user=session.get('user'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.authenticate(email, password)
        if user:
            session['user'] = user['name']
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        if User.register(name, email, password):
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error="Registration failed")
    return render_template('register.html')

ELEMENTS = [
    {"name": "Hydrogen", "symbol": "H"},
    {"name": "Oxygen", "symbol": "O"},
    {"name": "Carbon", "symbol": "C"},
    {"name": "Sodium", "symbol": "Na"},
    {"name": "Chlorine", "symbol": "Cl"},
    {"name": "Nitrogen", "symbol": "N"},
    {"name": "Phosphorus", "symbol": "P"},
    {"name": "Potassium", "symbol": "K"},
    {"name": "Sulphar", "symbol": "S"},
    {"name": "Magnesium", "symbol": "Mg"}
]
@app.route('/game')
def game():
    # Randomly shuffle the elements for the game
    random_elements = random.sample(ELEMENTS, 5)
    return render_template('game.html', elements=random_elements)


@app.route('/check_answer', methods=['POST'])
def check_answer():
    # Check if the answer is correct
    data = request.json
    element_name = data.get('element_name')
    user_answer = data.get('user_answer')

    # Find the correct symbol for the element
    for element in ELEMENTS:
        if element["name"] == element_name:
            correct_symbol = element["symbol"]
            return jsonify({
                "correct": user_answer == correct_symbol,
                "correct_symbol": correct_symbol
            })
    return jsonify({"error": "Element not found"}), 400
    
@app.route('/periodic_table')
def periodic_table():
    return render_template('periodic_table.html', elements=elements)
elements = [
    {"symbol": "H", "name": "Hydrogen", "atomic_number": 1, "details": "Lightest element, colorless gas."},
    {"symbol": "He", "name": "Helium", "atomic_number": 2, "details": "Noble gas, used in balloons."},
    {"symbol": "Li", "name": "Lithium", "atomic_number": 3, "details": "Soft metal, used in batteries."},
    {"symbol": "Be", "name": "Beryllium", "atomic_number": 4, "details": "Used in aerospace components."},
    {"symbol": "B", "name": "Boron", "atomic_number": 5, "details": "Used in glass and ceramics."},
    {"symbol": "C", "name": "Carbon", "atomic_number": 6, "details": "Basis of all known life."},
    {"symbol": "N", "name": "Nitrogen", "atomic_number": 7, "details": "Major part of Earth's atmosphere."},
    {"symbol": "O", "name": "Oxygen", "atomic_number": 8, "details": "Essential for respiration."},
    {"symbol": "F", "name": "Fluorine", "atomic_number": 9, "details": "Highly reactive gas, used in toothpaste."},
    {"symbol": "Ne", "name": "Neon", "atomic_number": 10, "details": "Used in bright neon signs."},
    {"symbol": "Na", "name": "Sodium", "atomic_number": 11, "details": "Reactive metal, found in salt."},
    {"symbol": "Mg", "name": "Magnesium", "atomic_number": 12, "details": "Lightweight metal, used in aircraft."},
    {"symbol": "Al", "name": "Aluminum", "atomic_number": 13, "details": "Used in cans and foil."},
    {"symbol": "Si", "name": "Silicon", "atomic_number": 14, "details": "Key component in electronics."},
    {"symbol": "P", "name": "Phosphorus", "atomic_number": 15, "details": "Used in fertilizers."},
    {"symbol": "S", "name": "Sulfur", "atomic_number": 16, "details": "Used in gunpowder and medicine."},
    {"symbol": "Cl", "name": "Chlorine", "atomic_number": 17, "details": "Used in disinfectants and pools."},
    {"symbol": "Ar", "name": "Argon", "atomic_number": 18, "details": "Inert gas used in light bulbs."},
    {"symbol": "K", "name": "Potassium", "atomic_number": 19, "details": "Essential nutrient in plants."},
    {"symbol": "Ca", "name": "Calcium", "atomic_number": 20, "details": "Strengthens bones and teeth."},
    {"symbol": "Sc", "name": "Scandium", "atomic_number": 21, "details": "Transition metal, lightweight."},
    {"symbol": "Ti", "name": "Titanium", "atomic_number": 22, "details": "Strong metal, resistant to corrosion."},
    {"symbol": "V", "name": "Vanadium", "atomic_number": 23, "details": "Used in steel alloys."},
    {"symbol": "Cr", "name": "Chromium", "atomic_number": 24, "details": "Used in stainless steel."},
    {"symbol": "Mn", "name": "Manganese", "atomic_number": 25, "details": "Used in steel manufacturing."},
    {"symbol": "Fe", "name": "Iron", "atomic_number": 26, "details": "Essential for blood production."},
    {"symbol": "Co", "name": "Cobalt", "atomic_number": 27, "details": "Used in magnets and batteries."},
    {"symbol": "Ni", "name": "Nickel", "atomic_number": 28, "details": "Resistant to corrosion, used in coins."},
    {"symbol": "Cu", "name": "Copper", "atomic_number": 29, "details": "Conductive metal used in wires."},
    {"symbol": "Zn", "name": "Zinc", "atomic_number": 30, "details": "Used to galvanize steel."},
    {"symbol": "Ga", "name": "Gallium", "atomic_number": 31, "details": "Melts at low temperatures."},
    {"symbol": "Ge", "name": "Germanium", "atomic_number": 32, "details": "Used in semiconductors."},
    {"symbol": "As", "name": "Arsenic", "atomic_number": 33, "details": "Toxic element, used in pesticides."},
    {"symbol": "Se", "name": "Selenium", "atomic_number": 34, "details": "Used in photocells."},
    {"symbol": "Br", "name": "Bromine", "atomic_number": 35, "details": "Liquid at room temperature."},
    {"symbol": "Kr", "name": "Krypton", "atomic_number": 36, "details": "Used in lighting."},
    {"symbol": "Rb", "name": "Rubidium", "atomic_number": 37, "details": "Soft, silvery-white metallic element."},
    {"symbol": "Sr", "name": "Strontium", "atomic_number": 38, "details": "Used in fireworks and flares."},
    {"symbol": "Y", "name": "Yttrium", "atomic_number": 39, "details": "Used in LEDs and superconductors."},
    {"symbol": "Zr", "name": "Zirconium", "atomic_number": 40, "details": "Used in nuclear reactors."},
    {"symbol": "Nb", "name": "Niobium", "atomic_number": 41, "details": "Used in steel alloys."},
    {"symbol": "Mo", "name": "Molybdenum", "atomic_number": 42, "details": "Used in lubricants and alloys."},
    {"symbol": "Tc", "name": "Technetium", "atomic_number": 43, "details": "Radioactive element, synthetic."},
    {"symbol": "Ru", "name": "Ruthenium", "atomic_number": 44, "details": "Used in electrical contacts."},
    {"symbol": "Rh", "name": "Rhodium", "atomic_number": 45, "details": "Used in catalytic converters."},
    {"symbol": "Pd", "name": "Palladium", "atomic_number": 46, "details": "Used in jewelry and industry."},
    {"symbol": "Ag", "name": "Silver", "atomic_number": 47, "details": "Used in jewelry and electronics."},
    {"symbol": "Cd", "name": "Cadmium", "atomic_number": 48, "details": "Used in batteries, toxic."},
    {"symbol": "In", "name": "Indium", "atomic_number": 49, "details": "Soft metal, used in touch screens."},
    {"symbol": "Sn", "name": "Tin", "atomic_number": 50, "details": "Used in solder and tin cans."},
    {"symbol": "Sb", "name": "Antimony", "atomic_number": 51, "details": "Used in flame retardants."},
    {"symbol": "Te", "name": "Tellurium", "atomic_number": 52, "details": "Used in alloys and solar panels."},
    {"symbol": "I", "name": "Iodine", "atomic_number": 53, "details": "Essential for thyroid health."},
    {"symbol": "Xe", "name": "Xenon", "atomic_number": 54, "details": "Used in flash lamps and anesthesia."},
    {"symbol": "Cs", "name": "Cesium", "atomic_number": 55, "details": "Soft, gold-colored metal."},
    {"symbol": "Ba", "name": "Barium", "atomic_number": 56, "details": "Used in medical imaging."},
    {"symbol": "La", "name": "Lanthanum", "atomic_number": 57, "details": "Used in hybrid car batteries."},
    {"symbol": "Ce", "name": "Cerium", "atomic_number": 58, "details": "Used in polishing powders."},
    {"symbol": "Pr", "name": "Praseodymium", "atomic_number": 59, "details": "Used in aircraft engines."},
    {"symbol": "Nd", "name": "Neodymium", "atomic_number": 60, "details": "Used in powerful magnets."},
    {"symbol": "Pm", "name": "Promethium", "atomic_number": 61, "details": "Radioactive, synthetic element."},
    {"symbol": "Sm", "name": "Samarium", "atomic_number": 62, "details": "Used in lasers and magnets."},
    {"symbol": "Eu", "name": "Europium", "atomic_number": 63, "details": "Used in TV screens and LEDs."},
    {"symbol": "Gd", "name": "Gadolinium", "atomic_number": 64, "details": "Used in MRI contrast agents."},
    {"symbol": "Tb", "name": "Terbium", "atomic_number": 65, "details": "Used in fluorescent lamps."},
    {"symbol": "Dy", "name": "Dysprosium", "atomic_number": 66, "details": "Used in magnets and lasers."},
    {"symbol": "Ho", "name": "Holmium", "atomic_number": 67, "details": "Used in nuclear reactors."},
    {"symbol": "Er", "name": "Erbium", "atomic_number": 68, "details": "Used in fiber optics."},
    {"symbol": "Tm", "name": "Thulium", "atomic_number": 69, "details": "Used in portable X-ray devices."},
    {"symbol": "Yb", "name": "Ytterbium", "atomic_number": 70, "details": "Used in stainless steel."},
    {"symbol": "Lu", "name": "Lutetium", "atomic_number": 71, "details": "Used in cancer treatments."},
    {"symbol": "Hf", "name": "Hafnium", "atomic_number": 72, "details": "Used in nuclear reactors."},
    {"symbol": "Ta", "name": "Tantalum", "atomic_number": 73, "details": "Used in electronic components."},
    {"symbol": "W", "name": "Tungsten", "atomic_number": 74, "details": "Used in lightbulb filaments."},
    {"symbol": "Re", "name": "Rhenium", "atomic_number": 75, "details": "Used in jet engines."},
    {"symbol": "Os", "name": "Osmium", "atomic_number": 76, "details": "Densest naturally occurring element."},
    {"symbol": "Ir", "name": "Iridium", "atomic_number": 77, "details": "Used in spark plugs."},
    {"symbol": "Pt", "name": "Platinum", "atomic_number": 78, "details": "Used in jewelry and catalysts."},
    {"symbol": "Au", "name": "Gold", "atomic_number": 79, "details": "Valuable precious metal."},
    {"symbol": "Hg", "name": "Mercury", "atomic_number": 80, "details": "Liquid metal at room temperature."},
    {"symbol": "Tl", "name": "Thallium", "atomic_number": 81, "details": "Toxic metal, used in electronics."},
    {"symbol": "Pb", "name": "Lead", "atomic_number": 82, "details": "Used in batteries and shielding."},
    {"symbol": "Bi", "name": "Bismuth", "atomic_number": 83, "details": "Used in cosmetics and alloys."},
    {"symbol": "Po", "name": "Polonium", "atomic_number": 84, "details": "Radioactive, used in industry."},
    {"symbol": "At", "name": "Astatine", "atomic_number": 85, "details": "Rare and radioactive."},
    {"symbol": "Rn", "name": "Radon", "atomic_number": 86, "details": "Radioactive noble gas."},
    {"symbol": "Fr", "name": "Francium", "atomic_number": 87, "details": "Highly radioactive, unstable."},
    {"symbol": "Ra", "name": "Radium", "atomic_number": 88, "details": "Radioactive, used in luminescence."},
    {"symbol": "Ac", "name": "Actinium", "atomic_number": 89, "details": "Used in radiation therapy."},
    {"symbol": "Th", "name": "Thorium", "atomic_number": 90, "details": "Potential nuclear fuel."},
    {"symbol": "U", "name": "Uranium", "atomic_number": 92, "details": "Used in nuclear reactors."},
    {"symbol": "Pu", "name": "Plutonium", "atomic_number": 94, "details": "Radioactive metal used in nuclear reactors and weapons."},
    {"symbol": "Am", "name": "Americium", "atomic_number": 95, "details": "Used in smoke detectors and research."},
    {"symbol": "Cm", "name": "Curium", "atomic_number": 96, "details": "Radioactive metal used in space applications."},
    {"symbol": "Bk", "name": "Berkelium", "atomic_number": 97, "details": "Radioactive element used in scientific research."},
    {"symbol": "Cf", "name": "Californium", "atomic_number": 98, "details": "Used in neutron sources and cancer treatment."},
    {"symbol": "Es", "name": "Einsteinium", "atomic_number": 99, "details": "Named after Einstein, used in scientific research."},
    {"symbol": "Fm", "name": "Fermium", "atomic_number": 100, "details": "Highly radioactive element used for research."},
    {"symbol": "Md", "name": "Mendelevium", "atomic_number": 101, "details": "Named after Dmitri Mendeleev, discovered in California."},
    {"symbol": "No", "name": "Nobelium", "atomic_number": 102, "details": "Radioactive element named after Alfred Nobel."},
    {"symbol": "Lr", "name": "Lawrencium", "atomic_number": 103, "details": "Named after Ernest Lawrence, used in research."},
    {"symbol": "Rf", "name": "Rutherfordium", "atomic_number": 104, "details": "Named after Ernest Rutherford, first synthesized in 1964."},
    {"symbol": "Db", "name": "Dubnium", "atomic_number": 105, "details": "Named after Dubna, Russia, used in research."},
    {"symbol": "Sg", "name": "Seaborgium", "atomic_number": 106, "details": "Named after Glenn T. Seaborg, discovered in 1974."},
    {"symbol": "Bh", "name": "Bohrium", "atomic_number": 107, "details": "Named after Niels Bohr, a Danish physicist."},
    {"symbol": "Hs", "name": "Hassium", "atomic_number": 108, "details": "Named after the German state of Hesse."},
    {"symbol": "Mt", "name": "Meitnerium", "atomic_number": 109, "details": "Named after Lise Meitner, discovered in 1982."},
    {"symbol": "Ds", "name": "Darmstadtium", "atomic_number": 110, "details": "Named after Darmstadt, Germany, where it was discovered."},
    {"symbol": "Rg", "name": "Roentgenium", "atomic_number": 111, "details": "Named after Wilhelm Röntgen, discoverer of X-rays."},
    {"symbol": "Cn", "name": "Copernicium", "atomic_number": 112, "details": "Named after Nicolaus Copernicus, synthesized in 1996."},
    {"symbol": "Nh", "name": "Nihonium", "atomic_number": 113, "details": "Named after Japan (Nihon), discovered in 2004."},
    {"symbol": "Fl", "name": "Flerovium", "atomic_number": 114, "details": "Named after Flerov Laboratory, discovered in Russia."},
    {"symbol": "Mc", "name": "Moscovium", "atomic_number": 115, "details": "Named after Moscow, Russia, where it was discovered."},
    {"symbol": "Lv", "name": "Livermorium", "atomic_number": 116, "details": "Named after Lawrence Livermore National Laboratory."},
    {"symbol": "Ts", "name": "Tennessine", "atomic_number": 117, "details": "Named after Tennessee, USA, discovered in 2010."},
    {"symbol": "Uuo", "name": "Oganesson", "atomic_number": 118, "details": "Synthetic element, very unstable."}

]

@app.route('/bonding_simulator', methods=['GET', 'POST'])
def bonding_simulator():
    bonding_result = None
    if request.method == 'POST':
        element1 = request.form['element1']
        element2 = request.form['element2']
        bonding_result = simulate_bonding(element1, element2)
    return render_template('bonding_simulator.html', bonding_result=bonding_result)

def simulate_bonding(element1, element2):
    # Simplified bonding logic
    ionic_bond_elements = ['Na', 'Cl', 'K', 'Br']
    covalent_bond_elements = ['H', 'O', 'N', 'C']

    if element1 in ionic_bond_elements and element2 in ionic_bond_elements:
        return f"{element1} and {element2} are likely to form an ionic bond."
    elif element1 in covalent_bond_elements and element2 in covalent_bond_elements:
        return f"{element1} and {element2} are likely to form a covalent bond."
    else:
        return f"Bonding simulation for {element1} and {element2} is unclear. Please provide valid elements."

def balance_reaction(reaction):
    # For demonstration purposes, let's use a placeholder logic
    if "H2 + O2" in reaction:
        return "2 H2 + O2 → 2 H2O"  # Example hardcoded reaction
    elif "CH4 + O2" in reaction:
        return "CH4 + 2 O2 → CO2 + 2 H2O"  # Another example
    else:
        return "Balancing logic not implemented for this reaction."

# Route for the chemical reactions page
@app.route('/chemical_reactions', methods=['GET', 'POST'])
def chemical_reactions():
    if request.method == 'POST':
        input_reaction = request.form['reaction']
        reaction_result = balance_reaction(input_reaction)
        return render_template('chemical_reactions.html',
                               input_reaction=input_reaction,
                               reaction_result=reaction_result)
    return render_template('chemical_reactions.html')

@app.route('/feedback', methods=['GET'])
def feedback():
    return render_template('feedback.html')

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    # Process or save the feedback (e.g., save to database or send via email)
    print(f"Feedback received from {name} ({email}): {message}")
    return redirect(url_for('feedback'))

@app.route('/tutoring', methods=['GET', 'POST'])
def tutoring():
    
    elements = [
        {"name": "Hydrogen", "symbol": "H"},
        {"name": "Oxygen", "symbol": "O"},
        {"name": "Carbon", "symbol": "C"},
        {"name": "Sodium", "symbol": "Na"},
        {"name": "Chlorine", "symbol": "Cl"}
    ]
    if request.method == 'POST':
        # Receive user's answers
        user_answers = request.form.to_dict()
        results = []
        for element in elements:
            correct = user_answers.get(element["name"]) == element["symbol"]
            results.append({
                "element": element["name"],
                "correct": correct,
                "user_answer": user_answers.get(element["name"], ""),
                "correct_answer": element["symbol"]
            })
        return render_template('tutoring.html', elements=elements, results=results)

    return render_template('tutoring.html', elements=elements, results=None)



@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))





# Initialize SQLite Database
def init_db():
    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            feedback TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/feedback', methods=['GET', 'POST'])
def handle_feedback():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        feedback_text = request.form['feedback']

        # Save feedback to the database
        conn = sqlite3.connect('feedback.db')
        c = conn.cursor()
        c.execute("INSERT INTO feedback (name, email, feedback) VALUES (?, ?, ?)", (name, email, feedback_text))
        conn.commit()
        conn.close()

        success_message = "Thank you for your feedback!"
        return render_template('feedback.html', success_message=success_message)

    return render_template('feedback.html')

if __name__ == '__main__':
    init_db()  # Ensure the database is initialized
    app.run(debug=True)
