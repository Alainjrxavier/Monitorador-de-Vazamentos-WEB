# DENTRO DE app/routes.py

from app import app
from flask import render_template, request # <--- A CORREÇÃO ESTÁ AQUI
from app.services import check_pwned_email

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    results = None
    email_checked = ''
    
    if request.method == 'POST':
        email_checked = request.form['email']
        if email_checked:
            results = check_pwned_email(email_checked)
            
    return render_template(
        'index.html', 
        title='Verificador de Vazamentos', 
        results=results, 
        email_checked=email_checked
    )