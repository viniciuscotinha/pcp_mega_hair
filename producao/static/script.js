function close_filter() {
  let filtroDiv = document.querySelector('.filtro_div');

  if (filtroDiv) {
    filtroDiv.style.display = 'none';
  } else {
    console.log("Elemento com a classe 'filtro_div' não encontrado.");
  }
  let botao_filtro = document.getElementById('botao_filtro');
  botao_filtro.style.display = 'block';
}
function open_filter() {
  let filtroDiv = document.querySelector('.filtro_div');

  if (filtroDiv) {
    filtroDiv.style.display = 'block';
  } else {
    console.log("Elemento com a classe 'filtro_div' não encontrado.");
  }
  let botao_filtro = document.getElementById('botao_filtro');
  botao_filtro.style.display = 'none';
}

function selecionarTodos() {
  var checkboxPrincipal = document.getElementById("selecionarTodos");

  var checkboxes = document.getElementsByName("selecionavel");

  for (var i = 0; i < checkboxes.length; i++) {
    checkboxes[i].checked = checkboxPrincipal.checked;
  }
}

function limparTodos() {
    var checkboxPrincipal = document.getElementById("selecionarTodos");
    if (verificarTodosSelecionados()){
        checkboxPrincipal.checked = true;
    } else {
        checkboxPrincipal.checked = false;
    }

}

function verificarTodosSelecionados() {
    var checkboxes = document.getElementsByName("selecionavel");
    for (var i = 0; i < checkboxes.length; i++) {
        if (!checkboxes[i].checked) {
            return false;
        }
    }
    return true;
}

function presquisarProximoNumeroLote() {
    iniciarCarregamento();
    var sigla = document.getElementById("input_prefixo").value;
    var sufixo = document.getElementById("input_sufixo").value;
    const url = '/lotes?lote=proximo_numero&prefixo=' + sigla;

            if (sigla) {fetch(url)
                .then(response => response.json())
                .then(data => {
                    if (data.numero) {
                        document.getElementById('input_sufixo').value = data.numero;
                    } else {
                        console.error('Campo "numero" não encontrado na resposta.');
                    }
                })
                .catch(error => {
                    console.error('Erro ao buscar o próximo número:', error);
                });} else {
                    adicionarNotificacao('Preencha o campo da sigla do lote!')
                }
    pararCarregamento()
}

function limparInfomacoesCampos() {
    document.getElementById("input_prefixo").value = "";
    document.getElementById("input_sufixo").value = null;
}

function salvar_lote() {
    iniciarCarregamento();
    var url = '/lotes?lote=addlote';
    var prefixo = document.getElementById("input_prefixo").value;
    var sufixo = document.getElementById("input_sufixo").value;

    if (prefixo && sufixo) {
        fetch(url + '&prefixo=' + prefixo + '&sufixo=' + sufixo, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            adicionarNotificacao(data.aviso);
            pegarPaginaLote(1);
            limparInfomacoesCampos();
            esconderModal();
        })
        .catch(error => {
            adicionarNotificacao("Erro ao salvar o lote:", error);
        });
    } else {
       adicionarNotificacao("Prefixo e/ou sufixo não fornecidos.");
    }
    pararCarregamento();
}

const toastElList = document.querySelectorAll(".toast");
const toastList = [...toastElList].map((toastEl) => {
    const toast = new bootstrap.Toast(toastEl, {});
});


function adicionarNotificacao(mensagem) {
    const toast = document.getElementById("toast");
    const container = document.getElementById("toastContainer");
    const novoToast = toast.cloneNode(true);
    novoToast.lastElementChild.innerHTML = mensagem;
    container.appendChild(novoToast);
    const bsToast = new bootstrap.Toast(novoToast, {});
    bsToast.show();
}

const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
const tooltipList = [...tooltipTriggerList].map((tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl));

const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
const popoverList = [...popoverTriggerList].map((popoverTriggerEl) => new bootstrap.Popover(popoverTriggerEl));

function esconderModal() {
  var modalElement = document.getElementById('incluir');
  var modal = bootstrap.Modal.getInstance(modalElement);
  modal.hide();
}


function getLoteById(id){
    url= '/lotes?lote=query&id='+id;
    fetch(url)
    .then(response => response.json())
    .then(data => {

    })
}

function pegarPaginaLote(pagina) {
    iniciarCarregamento();
    seletorData_inicio = document.getElementById('calendario_inicio');
    seletorData_final = document.getElementById('calendario_final');
    seletorUsuario = document.getElementById('filtro_usuario');
    seletorSituacao = document.getElementById('filtro_status');

    dataInicio = "&data_inicio="+seletorData_inicio.value + ' 00:00:00';
    dataFinal = "&data_final="+seletorData_final.value  + ' 23:59:59';
    pesquisa = "&pesquisa="+document.getElementById('caixa_pesquisa').value;
    usuario = seletorUsuario.value != '0' ? '&usuario='+seletorUsuario.value : '';
    situacao = '&situacao='+seletorSituacao.value;

    ajustarTagsFiltroLote()

    const url = `/lotes_lista?pagina=${pagina}${pesquisa}${usuario}${situacao}${dataInicio}${dataFinal}`;

    fetch(url)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.text();
    })
    .then(data => {
        var lista = document.getElementById('lugar_da_lista');
        lista.innerHTML = data;
        fecharSeletorData()
        close_filter()

    })
    .catch(error => {
        pararCarregamento()
        console.error('Falha ao carregar os dados:', error);
    });
    pararCarregamento();
}

function expSeletorData(){
    const collapseElement = document.getElementById('divSeletorData');
    const collapse = new bootstrap.Collapse(collapseElement, {
        toggle: false
    });
    collapse.toggle();
}

function fecharSeletorData(){
    const collapseElement = document.getElementById('divSeletorData');
    const collapse = new bootstrap.Collapse(collapseElement, {
        toggle: false
    });
    collapse.hide();
}

function iniciarCarregamento() {
    document.getElementById('loadingOverlay').style.display = 'flex';
}

function pararCarregamento() {
    document.getElementById('loadingOverlay').style.display = 'none';
}

function converterData(data) {
    const [ano, mes, dia] = data.split('-');
    return `${dia}/${mes}/${ano}`;
}

function ajustarTagsFiltroLote(){
    seletorData_inicio = document.getElementById('calendario_inicio');
    seletorData_final = document.getElementById('calendario_final');
    seletorUsuario = document.getElementById('filtro_usuario');
    seletorSituacao = document.getElementById('filtro_status');

    booleanTagsFiltro = false;

    if(seletorData_inicio.value == seletorData_inicio.getAttribute('data_pradrao') && seletorData_final.value == seletorData_final.getAttribute('data_pradrao')) {
        tagData = document.getElementById('filtro_data_tag')
        tagData.style.display = 'none'
        booleanTagsFiltro = booleanTagsFiltro || false
    } else {
        tagData = document.getElementById('filtro_data_tag')
        tagData.style.display = ''
        valueData = document.getElementById('filtro_data_valor')
        valueData.innerHTML = ` de ${converterData(seletorData_inicio.value)} até ${converterData(seletorData_final.value)}`
        booleanTagsFiltro = booleanTagsFiltro || true
    }

    if(seletorSituacao.value == "Ativo"){
        tagSituacao = document.getElementById('filtro_situacao_tag')
        tagSituacao.style.display = 'none'
        booleanTagsFiltro = booleanTagsFiltro || false
    }else{
        tagSituacao = document.getElementById('filtro_situacao_tag')
        tagSituacao.style.display = ''
        situacao_atual = document.getElementById('filtro_situacao_valor');
        situacao_atual.innerHTML = seletorSituacao.value;
        booleanTagsFiltro = booleanTagsFiltro || true
    }

    if(seletorUsuario.value == "0"){
        tagSituacao = document.getElementById('filtro_usuario_tag')
        tagSituacao.style.display = 'none'
        booleanTagsFiltro = booleanTagsFiltro || false
    }else{
        tagSituacao = document.getElementById('filtro_usuario_tag')
        tagSituacao.style.display = ''
        situacao_atual = document.getElementById('filtro_usuario_valor');
        situacao_atual.innerHTML = seletorUsuario.options[seletorUsuario.value].text;
        booleanTagsFiltro = booleanTagsFiltro || true
    }

    if (booleanTagsFiltro) {
    filtro_geral = document.getElementById('FiltrosSelecionados');
    filtro_geral.style.display = '';
    } else {
        filtro_geral = document.getElementById('FiltrosSelecionados');
        filtro_geral.style.display = 'none';
    }
}

function LimparFiltrosLote(filtro){
    console.log(filtro)
    seletorData_inicio = document.getElementById('calendario_inicio');
    seletorData_final = document.getElementById('calendario_final');
    seletorUsuario = document.getElementById('filtro_usuario');
    seletorSituacao = document.getElementById('filtro_status');

    if (filtro == 'todos'){
        seletorData_inicio.value = seletorData_inicio.getAttribute('data_pradrao');
        seletorData_final.value = seletorData_final.getAttribute('data_pradrao');
        seletorUsuario.value = '0';
        seletorSituacao.value = 'Ativo'
    } else if (filtro == 'data'){
        seletorData_inicio.value = seletorData_inicio.getAttribute('data_pradrao');
        seletorData_final.value = seletorData_final.getAttribute('data_pradrao');
    }else if (filtro == 'usuario'){
        seletorUsuario.value = 0;
    }else if (filtro == 'situacao'){
        seletorSituacao.value = 'Ativo'
    }

    pegarPaginaLote(1)
}

async function inativarLotes(){
    let selectedLotes = pegarLotesSelecionados();

    if (selectedLotes.length === 0) {
        adicionarNotificacao('Nenhum lote selecionado!');
        return;
    }

    for (let idLote of selectedLotes) {
        try {
            let response = await fetch(`/lotes?lote=inativar&id_lote=${idLote}`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            if (response.status === 202) {
                console.log(`Lote ${idLote} inativado com sucesso.`);
            } else {
                console.error(`Erro ao inativar o lote ${idLote}`);
            }
        } catch (error) {
            console.error(`Erro na requisição para o lote ${idLote}:`, error);
        }
    }

    adicionarNotificacao('Produtos inativados com sucesso.');
    pegarPaginaLote(1)
}


function pegarLotesSelecionados() {
    let selectedLotes = [];

    const checkboxes = document.querySelectorAll('input[name="selecionavel"]:checked');

    checkboxes.forEach(function(checkbox) {
        const trElement = checkbox.closest('tr');
        const idLote = trElement.getAttribute('id_lote');

        selectedLotes.push(idLote);
    });

    return selectedLotes;
}
