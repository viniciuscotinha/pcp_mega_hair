import html
from datetime import datetime, timedelta

from flask import render_template, Blueprint, request, redirect, jsonify, session
from flask_login import login_user, current_user, logout_user, login_required
from markupsafe import Markup
from sqlalchemy import func

from producao.models import lote, usuario, db

bp = Blueprint('routes', __name__)


@bp.route('/login', methods=['GET', "POST"])
def Login():
    if current_user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        user = usuario.pegar_usuario_por_email(email)
        if user:
            if senha == user.senha:
                login_user(user)
                return redirect(request.args.get('next', '/'))
        else:
            return redirect('/login')
    return render_template('login.html')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


@bp.route('/')
@login_required
def homepage():
    nome_pagina = "Início"
    return render_template('homepage.html', nome_pagina=nome_pagina)


@bp.route('/servicos')
@login_required
def servicos_page():
    nome_pagina = "Serviços"
    return render_template('servico.html', nome_pagina=nome_pagina)


@bp.route('/lotes', methods=['GET', "POST", "PATCH"])
@login_required
def lotes_page():
    if request.method == 'GET' and request.args.get('lote') == 'proximo_numero':
        prefixo = request.args.get('prefixo')
        return jsonify({'numero': lote.proximo_sufixo(prefixo)})

    if request.method == 'PATCH' and request.args.get('lote') == 'inativar':
        id_lote = int(request.args.get('id_lote'))
        lote_inativar = lote.query.get(id_lote)
        lote_inativar.status = 'Inativo'
        lote_inativar.modificado_em = datetime.now()
        lote_inativar.modificado_por = current_user.id
        db.session.commit()
        return jsonify({}), 202

    if request.method == 'POST' and request.args.get('lote') == 'addlote':
        prefixo = request.args.get('prefixo')
        sufixo = int(request.args.get('sufixo'))
        if lote.exite_lote(prefixo, sufixo):
            return jsonify({'aviso': "Lote já cadastrado na base de dados!"})
        else:
            lote_novo = lote(prefixo, sufixo, current_user.id, current_user.id)
            db.session.add(lote_novo)
            db.session.commit()
            return jsonify({'aviso': "Lote cadastrado com sucesso!", 'lote': lote_novo.to_dict()})

    nome_pagina = "Lote"
    consulta = lote.resgatar_itens()
    lista = Markup(render_template('lista_lotes.html', consulta=consulta))
    usuarios = usuario.listar_usuarios()
    data_mais_antiga = db.session.query(func.min(lote.criado_em)).scalar()
    return render_template('lote.html', nome_pagina=nome_pagina, lista=lista, usuarios=usuarios, hoje=datetime.today(), primeira_data=data_mais_antiga)


@bp.route('/lotes_lista', methods=['GET'])
@login_required
def lote_page():
    pagina = int(request.args.get('pagina', '1'))
    data_inicio = datetime.strptime(request.args.get('data_inicio', '2000-01-01 00:00:00'), "%Y-%m-%d %H:%M:%S")
    data_final = datetime.strptime(request.args.get('data_final', '3000-12-31 23:59:59'), "%Y-%m-%d %H:%M:%S")
    pesquisa = request.args.get('pesquisa', None)
    usuario_filtro = request.args.get('usuario', None)
    situacao = request.args.get('situacao', "Ativo")
    consulta = lote.resgatar_itens(pagina=pagina, data_inicio=data_inicio, data_final=data_final, pesquisa=pesquisa, usuario_filtro=usuario_filtro, situacao=situacao)
    return render_template('lista_lotes.html', consulta=consulta)


@bp.route('/colaboradores')
@login_required
def colaboradores_page():
    nome_pagina = "Colaboradores"
    return render_template('colaborador.html', nome_pagina=nome_pagina)


@bp.route('/produtos')
@login_required
def produtos_page():
    nome_pagina = "Produtos"
    return render_template('produto.html', nome_pagina=nome_pagina)


@bp.route('/processos')
@login_required
def processos_page():
    nome_pagina = "Processos"
    return render_template('processo.html', nome_pagina=nome_pagina)


@bp.route('/departamentos')
@login_required
def departamentos_page():
    nome_pagina = "Departamentos"
    return render_template('departamento.html', nome_pagina=nome_pagina)
