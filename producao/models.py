from flask_login import UserMixin
from sqlalchemy.dialects import sqlite
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import ForeignKey, desc, or_, func
from producao import db
from flask_login import current_user


class usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    senha = db.Column(db.String, nullable=False)

    @staticmethod
    def pegar_usuario_por_email(email):
        return usuario.query.filter_by(email=email).first()

    @staticmethod
    def listar_usuarios():
        return usuario.query.with_entities(usuario.id, usuario.nome).all()


class departamento(db.Model):
    __table_args__ = {'extend_existing': True}
    departamento_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    nome = db.Column(db.Text, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.now)

    processos = relationship("departamento_processo", back_populates="departamento")
    colaboradores = relationship("departamento_colaborador", back_populates="departamento")

    def __init__(self, nome):
        self.nome = nome
        print(f'Departamento {nome} criado com sucesso!')


class departamento_processo(db.Model):
    __table_args__ = {'extend_existing': True}
    departamento_id = db.Column(db.Integer, ForeignKey('departamento.departamento_id'), nullable=False,
                                primary_key=True)
    processo_id = db.Column(db.Integer, ForeignKey('processo.processo_id'), nullable=False, primary_key=True)
    criado_em = db.Column(db.DateTime, default=datetime.now)

    departamento = relationship("departamento", back_populates="processos")
    processo = relationship("processo", back_populates="departamentos")

    def __init__(self, departamento_id, processo_id):
        self.departamento_id = departamento_id
        self.processo_id = processo_id
        print(f'Vínculo entre processo {processo_id} e departamento {departamento_id} criado com sucesso!')


class departamento_colaborador(db.Model):
    __table_args__ = {'extend_existing': True}
    departamento_id = db.Column(db.Integer, ForeignKey('departamento.departamento_id'), nullable=False,
                                primary_key=True)
    colaborador_id = db.Column(db.Integer, ForeignKey('colaborador.colaborador_id'), nullable=False, primary_key=True)
    criado_em = db.Column(db.DateTime, default=datetime.now)

    departamento = relationship("departamento", back_populates="colaboradores")
    colaborador = relationship("colaborador", back_populates="departamentos")

    def __init__(self, departamento_id, colaborador_id):
        self.departamento_id = departamento_id
        self.colaborador_id = colaborador_id
        print(f'Vínculo entre colaborador e departamento criado!')


class processo(db.Model):
    __table_args__ = {'extend_existing': True}
    processo_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    criado_em = db.Column(db.DateTime, default=datetime.now)
    nome = db.Column(db.Text, nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    pesavel = db.Column(db.Boolean, nullable=False, default=False)
    une_cabelos = db.Column(db.Boolean, nullable=False, default=False)
    muda_cabelo = db.Column(db.Boolean, nullable=False, default=False)
    responsavel_unico = db.Column(db.Boolean, nullable=False, default=False)
    muda_tamanho = db.Column(db.Boolean, nullable=False, default=False)
    de_espera = db.Column(db.Boolean, nullable=False, default=False)

    departamentos = relationship("departamento_processo", back_populates="processo")
    servicos = relationship("servico", back_populates="processo")

    def __init__(self, nome, descricao, pesavel, une_cabelos, muda_cabelo, responsavel_unico, muda_tamanho, de_espera):
        self.nome = nome
        self.descricao = descricao
        self.pesavel = pesavel
        self.une_cabelos = une_cabelos
        self.muda_cabelo = muda_cabelo
        self.responsavel_unico = responsavel_unico
        self.muda_tamanho = muda_tamanho
        self.de_espera = de_espera
        print(f'Processo {nome} criado com sucesso!')


class colaborador(db.Model):
    __table_args__ = {'extend_existing': True}
    colaborador_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    criado_em = db.Column(db.DateTime, default=datetime.now)
    nome = db.Column(db.Text, nullable=False)
    status = db.Column(db.Text, nullable=False, default="A")

    departamentos = relationship("departamento_colaborador", back_populates="colaborador")
    servicos = relationship("servico", back_populates="colaborador")

    def __init__(self, nome, status="A"):
        self.nome = nome
        self.status = status
        print(f'Colaborador {nome} criado com sucesso!')


class servico(db.Model):
    __table_args__ = {'extend_existing': True}
    servico_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    criado_em = db.Column(db.DateTime, default=datetime.now)
    duracao = db.Column(db.Integer, nullable=False)
    inicio = db.Column(db.DateTime, nullable=True)
    fim = db.Column(db.DateTime, nullable=True)
    observacao = db.Column(db.Text, nullable=True)
    processo_id = db.Column(db.Integer, ForeignKey('processo.processo_id'), nullable=False)
    colaborador_id = db.Column(db.Integer, ForeignKey('colaborador.colaborador_id'), nullable=False)

    processo = relationship("processo", back_populates="servicos")
    colaborador = relationship("colaborador", back_populates="servicos")

    servico_cabelos = relationship("servico_cabelo", back_populates="servico")

    def __init__(self, duracao, observacao, processo_id, colaborador_id, inicio=None, fim=None):
        self.duracao = duracao
        self.observacao = observacao
        self.processo_id = processo_id
        self.colaborador_id = colaborador_id
        self.inicio = inicio
        self.fim = fim
        print(f'Serviço criado com sucesso!')


class servico_cabelo(db.Model):
    __table_args__ = {'extend_existing': True}
    servico_id = db.Column(db.Integer, ForeignKey('servico.servico_id'), nullable=False, primary_key=True)
    cabelo_id = db.Column(db.Integer, ForeignKey('cabelo.cabelo_id'), nullable=False, primary_key=True)
    criado_em = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.Text, nullable=False, default="não iniciado")

    servico = db.relationship("servico", back_populates="servico_cabelos")
    cabelo = db.relationship("cabelo", back_populates="servico_cabelos")

    def __init__(self, servico_id, cabelo_id, status="não iniciado"):
        self.servico_id = servico_id
        self.cabelo_id = cabelo_id
        self.status = status
        print(f'Serviço {servico_id} associado ao cabelo {cabelo_id} com status "{status}" criado com sucesso!')


class cabelo(db.Model):
    __table_args__ = {'extend_existing': True}
    cabelo_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    criado_em = db.Column(db.DateTime, default=datetime.now)
    peso = db.Column(db.Integer, nullable=False)
    tamanho = db.Column(db.Integer, nullable=False)
    foi_mesclado = db.Column(db.Boolean, nullable=False, default=False)
    status = db.Column(db.Text, nullable=False, default="livre para uso")
    observacao = db.Column(db.Text, nullable=True)
    produto_id = db.Column(db.Integer, ForeignKey('produto.produto_id'), nullable=False)
    demanda_id = db.Column(db.Integer, ForeignKey('demanda.demanda_id'), nullable=False)
    lote_id = db.Column(db.Integer, ForeignKey('lote.lote_id'), nullable=False)

    mesclagens_filho = db.relationship("mesclado", foreign_keys="[mesclado.id_cabelo_filho]", back_populates="filho")

    mesclagens_pai = db.relationship("mesclado", foreign_keys="[mesclado.id_cabelo_pai]", back_populates="pai")

    servico_cabelos = db.relationship("servico_cabelo", back_populates="cabelo")
    lote = db.relationship("lote", back_populates="cabelos")
    demanda = db.relationship("demanda", back_populates="cabelos")
    produto = db.relationship("produto", back_populates="cabelos")

    def __init__(self, peso, tamanho, produto_id, demanda_id, lote_id, foi_mesclado=False, status="livre para uso",
                 observacao=None):
        self.peso = peso
        self.tamanho = tamanho
        self.produto_id = produto_id
        self.demanda_id = demanda_id
        self.lote_id = lote_id
        self.foi_mesclado = foi_mesclado
        self.status = status
        self.observacao = observacao


class demanda(db.Model):
    __table_args__ = {'extend_existing': True}
    demanda_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    criado_em = db.Column(db.DateTime, default=datetime.now)
    tipo = db.Column(db.Text, nullable=False)
    numero = db.Column(db.Integer, nullable=False)

    cabelos = relationship("cabelo", back_populates="demanda")

    def __init__(self, tipo, numero):
        self.tipo = tipo
        self.numero = numero
        print(f'Demanda {numero} do tipo "{tipo}" criada com sucesso!')


class produto(db.Model):
    __table_args__ = {'extend_existing': True}
    produto_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    categoria_id = db.Column(db.Integer, ForeignKey('categoria_produto.categoria_id'), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    codigo = db.Column(db.Text, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.now)

    cabelos = relationship("cabelo", back_populates="produto")
    categoria = relationship("categoria_produto", back_populates="produtos")

    def __init__(self, categoria_id, descricao, codigo):
        self.categoria_id = categoria_id
        self.descricao = descricao
        self.codigo = codigo
        print(f'Produto {codigo} com descrição "{descricao}" criado com sucesso!')


class categoria_produto(db.Model):
    __table_args__ = {'extend_existing': True}
    categoria_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.Text, nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.now)

    produtos = relationship("produto", back_populates="categoria")

    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao
        print(f'Categoria "{nome}" criada com sucesso!')


class lote(db.Model):
    __table_args__ = {'extend_existing': True}
    lote_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    prefixo = db.Column(db.Text, nullable=False)
    sufixo = db.Column(db.Integer, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.now)
    modificado_em = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.Text, nullable=False, default="Ativo")

    cabelos = relationship("cabelo", back_populates="lote")

    criado_por = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    modificado_por = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    usuario_criador = db.relationship("usuario", foreign_keys=[criado_por], backref="lotes_criados")
    usuario_modificador = db.relationship("usuario", foreign_keys=[modificado_por], backref="lotes_modificados")

    def __init__(self, prefixo, sufixo, criado_por_usuario_id, modifcado_por_usuario_id):
        self.prefixo = prefixo
        self.sufixo = sufixo
        self.modificado_por = modifcado_por_usuario_id
        self.criado_por = criado_por_usuario_id
        self.modificado_em = datetime.now()
        print(f'Lote {prefixo}{sufixo} criado com sucesso!')

    @staticmethod
    def proximo_sufixo(prefixo):
        lote_com_maior_sufixo = lote.query.filter_by(prefixo=prefixo).order_by(desc('sufixo')).first()
        return lote_com_maior_sufixo.sufixo + 1 if lote_com_maior_sufixo else 1

    @staticmethod
    def exite_lote(prefixo, sufixo):
        lote_existe = lote.query.filter_by(prefixo=prefixo, sufixo=sufixo).first()
        return True if lote_existe else False

    @staticmethod
    def resgatar_itens(pagina=1, data_inicio=None, data_final=None, pesquisa=None, usuario_filtro=None,
                       situacao="Ativo"):
        query = lote.query

        if situacao:
            query = query.filter_by(status=situacao)

        if usuario_filtro:
            query = query.filter(
                or_(lote.criado_por == usuario_filtro, lote.modificado_por == usuario_filtro)
            )

        if data_inicio:
            query = query.filter(lote.criado_em >= data_inicio)
        else:
            query = query.order_by(lote.criado_em.desc())

        if data_final:
            query = query.filter(lote.criado_em <= data_final)
        else:
            query = query.order_by(lote.criado_em.desc())

        if pesquisa:
            pesquisa_formatada = f"%{pesquisa}%"
            nome_lote_formatado = lote.prefixo + '0' + func.cast(lote.sufixo, db.String)
            query = query.filter(nome_lote_formatado.like(pesquisa_formatada))
        else:
            query = query.order_by(lote.criado_em.desc())

        resultados_por_pagina = 100
        paginacao = query.paginate(page=pagina, per_page=resultados_por_pagina, error_out=False)

        print(query.statement.compile(dialect=sqlite.dialect(), compile_kwargs={"literal_binds": True}))

        return {
            'itens': paginacao.items,
            'total_itens': paginacao.total,
            'pagina_atual': paginacao.page,
            'total_paginas': paginacao.pages
        }

    def to_dict(self):
        return {
            'lote_id': self.lote_id,
            'prefixo': self.prefixo,
            'sufixo': self.sufixo,
            'criado_em': '{:%d/%m/%Y %H:%M}'.format(self.criado_em),
            'modificado_em': '{:%d/%m/%Y %H:%M}'.format(self.modificado_em),
            'status': self.status,
            'criador': {
                'id': self.usuario_criador.id,
                'nome': self.usuario_criador.nome,
                'email': self.usuario_criador.email
            },
            'modificador': {
                'id': self.usuario_modificador.id,
                'nome': self.usuario_modificador.nome,
                'email': self.usuario_modificador.email
            }
        }


class mesclado(db.Model):
    __table_args__ = {'extend_existing': True}
    id_cabelo_filho = db.Column(db.Integer, ForeignKey('cabelo.cabelo_id'), nullable=False, primary_key=True)
    id_cabelo_pai = db.Column(db.Integer, ForeignKey('cabelo.cabelo_id'), nullable=False, primary_key=True)
    criado_em = db.Column(db.DateTime, default=datetime.now)

    filho = db.relationship("cabelo", foreign_keys=[id_cabelo_filho], back_populates="mesclagens_filho")

    pai = db.relationship("cabelo", foreign_keys=[id_cabelo_pai], back_populates="mesclagens_pai")

    def __init__(self, id_cabelo_filho, id_cabelo_pai):
        self.id_cabelo_filho = id_cabelo_filho
        self.id_cabelo_pai = id_cabelo_pai
        print(f'Cabelo pai {id_cabelo_pai} mesclado no filho {id_cabelo_filho}.')
