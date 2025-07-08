# app/routes.py

from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.services import check_pwned_email
from app.forms import EmailSearchForm, RegistrationForm, LoginForm, AddEmailForm, DeleteAccountForm
from app.models import User, MonitoredEmail, Log # Adicione a importação do modelo Log

# ... (todas as suas rotas existentes, de index a terms_of_service, continuam aqui) ...
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = EmailSearchForm()
    results = None
    email_checked = ''
    
    if form.validate_on_submit():
        email_checked = form.email.data
        app.logger.info(f"Consulta iniciada para o e-mail: '{email_checked}'")
        results = check_pwned_email(email_checked)
        
        log_message = f"Resultado para '{email_checked}':"
        if results.get('breaches'):
            app.logger.warning(f"{log_message} VAZAMENTO ENCONTRADO.")
        elif results.get('error'):
            app.logger.error(f"{log_message} Erro na consulta. Erro: {results.get('error')}")
        else:
            app.logger.info(f"{log_message} Nenhum vazamento conhecido encontrado.")
            
    return render_template(
        'index.html', 
        title='Verificador de Vazamentos', 
        form=form, 
        results=results, 
        email_checked=email_checked
    )

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Parabéns, seu cadastro foi realizado com sucesso!')
        app.logger.info(f"Novo usuário cadastrado: '{user.email}'")
        return redirect(url_for('login'))
    return render_template('register.html', title='Cadastro', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user is None or not user.check_password(form.password.data):
            flash('E-mail ou senha inválidos.')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        app.logger.info(f"Usuário '{user.email}' logado com sucesso.")
        return redirect(url_for('dashboard'))
        
    return render_template('login.html', title='Entrar', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = AddEmailForm()
    if form.validate_on_submit():
        existing_email = MonitoredEmail.query.filter_by(
            email=form.email.data,
            user_id=current_user.id
        ).first()
        if existing_email:
            flash('Este e-mail já está na sua lista de monitoramento.')
        else:
            email_to_monitor = MonitoredEmail(email=form.email.data, user_id=current_user.id)
            db.session.add(email_to_monitor)
            db.session.commit()
            flash('E-mail adicionado à sua lista de monitoramento!')
        return redirect(url_for('dashboard'))

    monitored_emails_objects = MonitoredEmail.query.filter_by(user_id=current_user.id).all()
    
    dashboard_data = []
    for email_obj in monitored_emails_objects:
        status_info = check_pwned_email(email_obj.email)
        dashboard_data.append({
            'db_entry': email_obj,
            'status_info': status_info
        })

    return render_template(
        'dashboard.html', 
        title='Dashboard', 
        form=form, 
        dashboard_data=dashboard_data
    )

@app.route('/delete-email/<int:email_id>', methods=['POST'])
@login_required
def delete_email(email_id):
    email_to_delete = MonitoredEmail.query.get_or_404(email_id)
    
    if email_to_delete.owner != current_user:
        flash('Operação não permitida.')
        app.logger.warning(f"Tentativa de acesso não autorizado: Usuário '{current_user.email}' tentou apagar e-mail ID {email_id} de outro usuário.")
        return redirect(url_for('dashboard'))
    
    db.session.delete(email_to_delete)
    db.session.commit()
    
    flash('E-mail removido da sua lista de monitoramento.')
    app.logger.info(f"Usuário '{current_user.email}' removeu o e-mail '{email_to_delete.email}' (ID: {email_id}) do monitoramento.")
    
    return redirect(url_for('dashboard'))

@app.route('/delete-account', methods=['GET', 'POST'])
@login_required
def delete_account():
    form = DeleteAccountForm()
    if form.validate_on_submit():
        if current_user.check_password(form.password.data):
            user_email_log = current_user.email
            db.session.delete(current_user)
            db.session.commit()
            logout_user()
            flash('Sua conta e todos os seus dados foram apagados permanentemente.')
            app.logger.info(f"Usuário '{user_email_log}' deletou sua própria conta.")
            return redirect(url_for('index'))
        else:
            flash('Senha incorreta. A exclusão da conta foi cancelada.')
            return redirect(url_for('delete_account'))
    return render_template('delete_account.html', title='Apagar Conta', form=form)

@app.route('/politica-de-privacidade')
def privacy_policy():
    return render_template('privacy_policy.html', title='Política de Privacidade')

@app.route('/termos-de-servico')
def terms_of_service():
    return render_template('terms_of_service.html', title='Termos de Serviço')

# No final de app/routes.py
from app.models import Log

@app.route('/logs')
@login_required # Futuramente, podemos criar um @admin_required aqui
def view_logs():
    # Busca os logs do mais recente para o mais antigo, com um limite de 100
    logs = Log.query.order_by(Log.timestamp.desc()).limit(100).all()
    return render_template('view_logs.html', title='Logs de Auditoria', logs=logs)