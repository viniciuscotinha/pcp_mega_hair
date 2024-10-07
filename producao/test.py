import random
from datetime import datetime
from producao import criar_app
from producao.models import departamento, processo, colaborador, servico, servico_cabelo, cabelo, demanda, produto, \
    categoria_produto, lote, mesclado, departamento_colaborador, departamento_processo, usuario

from producao import db

app = criar_app()


def create_test_data():
    # Criando categorias de produtos
    categorias = []
    for i in range(5):  # Criando 5 categorias
        categoria = categoria_produto(nome=f"Categoria {i+1}", descricao=f"Descrição da categoria {i+1}")
        db.session.add(categoria)
        db.session.flush()  # Garante que categoria_id seja atribuído
        categorias.append(categoria)

    # Criando produtos
    produtos = []
    for i in range(10):  # Criando 10 produtos
        produto_ = produto(categoria_id=random.choice(categorias).categoria_id, descricao=f"Produto {i+1}", codigo=f"Código {i+1}")
        db.session.add(produto_)
        db.session.flush()  # Garante que produto_id seja atribuído
        produtos.append(produto_)

    # Criando departamentos
    departamentos = []
    for i in range(3):  # Criando 3 departamentos
        depto = departamento(nome=f"Departamento {i+1}")
        db.session.add(depto)
        db.session.flush()  # Garante que departamento_id seja atribuído
        departamentos.append(depto)

    # Criando processos
    processos = []
    for i in range(10):  # Criando 10 processos
        processo_ = processo(
            nome=f"Processo {i+1}",
            descricao=f"Descrição do processo {i+1}",
            pesavel=bool(random.getrandbits(1)),
            une_cabelos=bool(random.getrandbits(1)),
            muda_cabelo=bool(random.getrandbits(1)),
            responsavel_unico=bool(random.getrandbits(1)),
            muda_tamanho=bool(random.getrandbits(1)),
            de_espera=bool(random.getrandbits(1))
        )
        db.session.add(processo_)
        db.session.flush()  # Garante que processo_id seja atribuído
        processos.append(processo_)

    # Associando departamentos e processos
    for depto in departamentos:
        for processo_ in random.sample(processos, k=5):  # Associando cada departamento a 5 processos aleatórios
            depto_processo = departamento_processo(departamento_id=depto.departamento_id, processo_id=processo_.processo_id)
            db.session.add(depto_processo)

    # Criando colaboradores
    colaboradores = []
    for i in range(10):  # Criando 10 colaboradores
        colab = colaborador(nome=f"Colaborador {i+1}", status=random.choice(['A', 'I']))
        db.session.add(colab)
        db.session.flush()  # Garante que colaborador_id seja atribuído
        colaboradores.append(colab)

    # Associando colaboradores e departamentos
    for depto in departamentos:
        for colaborador_ in random.sample(colaboradores, k=3):  # Associando 3 colaboradores a cada departamento
            depto_colab = departamento_colaborador(departamento_id=depto.departamento_id, colaborador_id=colaborador_.colaborador_id)
            db.session.add(depto_colab)

    # Criando demandas
    demandas = []
    for i in range(10):  # Criando 10 demandas
        demanda_ = demanda(tipo=f"Tipo {i+1}", numero=i+1)
        db.session.add(demanda_)
        db.session.flush()  # Garante que demanda_id seja atribuído
        demandas.append(demanda_)

    # Criando lotes
    lotes = []
    for i in range(5):  # Criando 5 lotes
        lote_ = lote(prefixo=f"LotePrefixo{i+1}", sufixo=i+1)
        db.session.add(lote_)
        db.session.flush()  # Garante que lote_id seja atribuído
        lotes.append(lote_)

    # Criando cabelos
    cabelos = []
    for i in range(20):  # Criando 20 cabelos
        cabelo_ = cabelo(
            peso=random.randint(50, 100),
            tamanho=random.randint(10, 30),
            produto_id=random.choice(produtos).produto_id,
            demanda_id=random.choice(demandas).demanda_id,
            lote_id=random.choice(lotes).lote_id,
            foi_mesclado=bool(random.getrandbits(1)),
            status="livre para uso"
        )
        db.session.add(cabelo_)
        db.session.flush()  # Garante que cabelo_id seja atribuído
        cabelos.append(cabelo_)

    # Criando serviços
    servicos = []
    for i in range(15):  # Criando 15 serviços
        servico_ = servico(
            duracao=random.randint(30, 120),
            observacao=f"Serviço {i+1}",
            processo_id=random.choice(processos).processo_id,
            colaborador_id=random.choice(colaboradores).colaborador_id,
            inicio=datetime.now(),
            fim=datetime.now()
        )
        db.session.add(servico_)
        db.session.flush()  # Garante que servico_id seja atribuído
        servicos.append(servico_)

    # Criando associações de serviços com cabelos
    for servico_ in servicos:
        for cabelo_ in random.sample(cabelos, k=3):  # Associando 3 cabelos aleatórios a cada serviço
            servico_cabelo_ = servico_cabelo(servico_id=servico_.servico_id, cabelo_id=cabelo_.cabelo_id)
            db.session.add(servico_cabelo_)

    # Criando mesclagem de cabelos
    for i in range(5):  # Criando 5 mesclagens de cabelos
        cabelo_filho = random.choice(cabelos)
        cabelo_pai = random.choice(cabelos)
        while cabelo_filho == cabelo_pai:  # Garantindo que o pai e o filho não sejam o mesmo cabelo
            cabelo_pai = random.choice(cabelos)

        mesclagem = mesclado(id_cabelo_filho=cabelo_filho.cabelo_id, id_cabelo_pai=cabelo_pai.cabelo_id)
        db.session.add(mesclagem)

    # Commitando todas as mudanças no banco de dados
    db.session.commit()
    print("Dados de teste criados com sucesso!")


def criar_usuario_padrao():
    usuario1 = usuario(nome="Magnus Cabelos", senha="magnus", email="magnuscabelos@gmail.com")
    db.session.add(usuario1)
    db.session.commit()


with app.app_context():
    pesquisa = lote.resgatar_itens(pesquisa="1")
    print(pesquisa)
    # create_test_data()
    # criar_usuario_padrao()
    # usuario1 = usuario(nome="Vinícius Cota", senha="viniciuscota", email="viniciuscotinha@gmail.com")
    # db.session.add(usuario1)
    # db.session.commit()

