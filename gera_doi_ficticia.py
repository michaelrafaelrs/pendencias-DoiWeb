import random
import json
from datetime import datetime, timedelta

def generate_random_ni():
    # Gerar um número aleatório de 11 dígitos para CPF ou 14 dígitos para CNPJ
    ni_length = random.choice([11, 14])
    return ''.join(random.choices('0123456789', k=ni_length))

def generate_random_date(start_date, end_date):
    # Gerar uma data aleatória entre as datas inicial e final fornecidas
    time_between_dates = end_date - start_date
    random_number_of_days = random.randrange(time_between_dates.days)
    return start_date + timedelta(days=random_number_of_days)

def generate_random_declaration():
    # Valores pré-definidos para tipoImovel
    tipo_imovel_options = ["15", "31", "65", "67", "69", "71", "89", "90", "91", "92", "93", "94", "95", "96"]
    tipo_servico_options = ["2"]
    TipoParteTransacionada_options = ["1", "2"]
    TipoOperacaoImobiliaria_options = [
        "11", "13", "15", "19", "21", "31", "33", "35", "37", "39", "41", "45", "47",
        "55", "56", "57", "58", "59", "60", "61", "62", "63", "64", "65", "66", "67",
        "68", "69", "70", "71", "72", "73", "74"
    ]
    natureza_titulo_options = ["1", "2", "3", "4", "5"]
    tipo_ato_options = ["3", "4"]
    tipo_livro_options = ["1"]
    forma_pagamento_options = ["5", "10", "11", "7", "9"]
    destinacao_options = ["1"]


    declaracao = {
        "adquirentes": [],
        "alienantes": [],
        "areaImovel": round(random.uniform(10.0, 200.0), 2),
        "bairro": random.choice(["Centro", "Jardim das Flores", "Vila Nova", "Boa Vista", "Bela Vista"]),
        "cep": "00000000",
        "codigoIbge": "5208707",
        "codigoNacionalMatricula": ''.join(random.choices('0123456789', k=16)),
        "complementoEndereco": "n/c",
        "complementoNumeroImovel": str(random.randint(1, 100)),
        "dataLavraturaRegistroAverbacao": "",
        "dataNegocioJuridico": "",
        "destinacao": random.choice(destinacao_options),
        "existeDoiAnterior": random.choice([True, False]),
        "folha": "0000000",
        "formaPagamento": random.choice(forma_pagamento_options),
        "indicadorAreaConstruidaNaoConsta": random.choice([True, False]),
        "indicadorAreaLoteNaoConsta": random.choice([True, False]),
        "indicadorImovelPublicoUniao": random.choice([True, False]),
        "indicadorPermutaBens": random.choice([True, False]),
        "inscricaoMunicipal": ''.join(random.choices('0123456789', k=15)),
        "matricula": ''.join(random.choices('0123456789', k=7)),
        "naturezaTitulo": random.choice(natureza_titulo_options),
        "nomeLogradouro": random.choice(["Rua A", "Avenida B", "Travessa C", "Alameda D", "Praça E"]),
        "numeroImovel": random.choice(["s-n", str(random.randint(1, 1000))]),
        "numeroRegistroAverbacao": ''.join(random.choices('0123456789', k=7)),
        "tipoAto": random.choice(tipo_ato_options),
        "tipoDeclaracao": "0",
        "tipoImovel": random.choice(tipo_imovel_options),
        "tipoLivro": random.choice(tipo_livro_options),
        "tipoLogradouro": random.choice(["RUA", "AVENIDA", "TRAVESSA", "ALAMEDA", "PRAÇA"]),
        "tipoOperacaoImobiliaria": random.choice(TipoOperacaoImobiliaria_options),
        "tipoParteTransacionada": random.choice(TipoParteTransacionada_options),
        "tipoServico": random.choice(tipo_servico_options),
        "valorBaseCalculoItbiItcmd": round(random.uniform(50000, 500000), 2),
        "valorOperacaoImobiliaria": round(random.uniform(50000, 500000), 2),
        "indicadorPagamentoDinheiro": False,
        "valorParteTransacionada":  random.choice([50, 100]),
    }

    # Verificações e ajustes para formaPagamento
    if declaracao["formaPagamento"] == "7":
        declaracao["indicadorAlienacaoFiduciaria"] = True
        declaracao["mesAnoUltimaParcela"] = (datetime.now() + timedelta(days=random.randint(365, 3650))).strftime("%Y-%m-%d")
        declaracao["valorPagoAteDataAto"] = round(random.uniform(10000, 300000), 2)
        declaracao["indicadorPagamentoDinheiro"] = False
    else:
        declaracao.pop("indicadorAlienacaoFiduciaria", None)
        declaracao.pop("mesAnoUltimaParcela", None)
        declaracao.pop("valorPagoAteDataAto", None)

        # declaracao["indicadorAlienacaoFiduciaria"] = False
        # declaracao["mesAnoUltimaParcela"] = None
        # declaracao["valorPagoAteDataAto"] = None
        # declaracao["indicadorPagamentoDinheiro"] = None

    # Gerar datas válidas
    start_date = datetime(2023, 1, 1)
    end_date = datetime.now() - timedelta(days=1)
    negocio_juridico_date = generate_random_date(start_date, end_date)
    lavratura_registro_date = generate_random_date(start_date, negocio_juridico_date)

    declaracao["dataNegocioJuridico"] = negocio_juridico_date.strftime("%Y-%m-%d")
    declaracao["dataLavraturaRegistroAverbacao"] = lavratura_registro_date.strftime("%Y-%m-%d")

    # Gerar adquirentes e alienantes
    for parte in ["adquirentes", "alienantes"]:
        num_partes = random.randint(1, 3)
        for _ in range(num_partes):
            parte_info = {
                "indicadorEstrangeiro": random.choice([True, False]),
                "indicadorNaoConstaParticipacaoOperacao": random.choice([True, False]),
                "indicadorNiIdentificado": random.choice([True, False]),
                "indicadorRepresentante": random.choice([True, False]),
            }

            if parte_info["indicadorNiIdentificado"]:
                parte_info["ni"] = generate_random_ni()
                if len(parte_info["ni"]) == 11:  # CPF
                    parte_info["indicadorConjuge"] = random.choice([True, False])
                    parte_info["indicadorEspolio"] = random.choice([True, False])
                elif len(parte_info["ni"]) == 14:  # CNPJ
                    parte_info["indicadorEspolio"] = False
            else:
                declaracao.pop("ni", None)
                #parte_info["ni"] = None
                parte_info["indicadorEspolio"] = random.choice([True, False])

            if not parte_info["indicadorNaoConstaParticipacaoOperacao"]:
                parte_info["participacao"] = random.choice([50, 100])

            declaracao[parte].append(parte_info)

    return declaracao

def generate_multiple_declarations(n):
    # Gerar múltiplas declarações fictícias
    return [generate_random_declaration() for _ in range(n)]

# Gerar 5 declarações fictícias
declarations = generate_multiple_declarations(5)

# Criar um dicionário com as declarações
data = {"declaracoes": declarations}

# Imprimir como JSON formatado
#print(json.dumps(data, indent=2))

# Salvar as alterações de volta para o arquivo JSON
with open('doi_ficticia.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4)

print("json gerado com sucesso.")