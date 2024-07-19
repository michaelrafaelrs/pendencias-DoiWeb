import json, datetime
import csv

# Carregar o arquivo JSON com codificação UTF-8
with open('doi-2024-07-01-2024-07-17.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Inicializar contadores
declaracoes_count = len(data['declaracoes'])

# Abrir arquivo de relatório de modificações para CSV
with open('relatorio_modificacoes.csv', 'w', newline='', encoding='utf-8') as file_mod:
    csv_writer_mod = csv.writer(file_mod)
    csv_writer_mod.writerow(['Matrícula', 'Ato' ,'Modificações'])

    # Abrir arquivo de relatório de pendências para CSV
    with open('relatorio_pendencias.csv', 'w', newline='', encoding='utf-8') as file_pend:
        csv_writer_pend = csv.writer(file_pend)
        csv_writer_pend.writerow(['Matricula', 'Ato', 'DataRegistro', 'Pendencias'])

        # Percorrer cada declaração
        for declaracao in data['declaracoes']:
            # Relatório de Modificações
            modificacoes = []
            percen_alienantes = 0.0
            percen_transmitentes = 0.0
            
            # Adicionar item "folha" com valor "0000000" caso não exista
            if not declaracao.get('folha'):
                declaracao['folha'] = '0000000'
                modificacoes.append('folha adicionada "0000000"')

            # Verifica se existe o numeroImovel e se não existir inclui
            if not declaracao.get('numeroImovel'):
                declaracao['numeroImovel'] = 'N/A'
                modificacoes.append('numeroImovel adicionado "N/A"')

            # Formatar campos 'folha', 'numeroRegistroAverbacao', 'matricula'
            for campo in ['folha', 'numeroRegistroAverbacao', 'matricula']:
                if campo in declaracao:
                    valor_original = declaracao[campo]
                    declaracao[campo] = declaracao[campo].zfill(7)
                    if valor_original != declaracao[campo]:
                        modificacoes.append(f'{campo} formatado para {declaracao[campo]}')

            # Verificar e formatar CEP
            if 'cep' in declaracao:
                valor_original = declaracao['cep']
                declaracao['cep'] = declaracao['cep'].zfill(8)
                if valor_original != declaracao['cep']:
                    modificacoes.append(f'cep formatado para {declaracao["cep"]}')
            else:
                declaracao['cep'] = '00000000'
                modificacoes.append('cep adicionado "00000000"')

            # Verificações de pendências conforme as regras fornecidas
            # Relatório de Pendências
            pendencias = []
            # Verificações de pendências conforme as regras fornecidas
            # Verificar se "NI" dos alienantes ou adquirentes é de 14 dígitos (CNPJ) e se "indicadorConjuge" é true
            for parte in ['alienantes', 'adquirentes']:
                if parte in declaracao:
                    for pessoa in declaracao[parte]:
                        # Remove o campo incicador Conjuge quando for CNPJ
                        if 'ni' in pessoa and len(pessoa['ni']) == 14 and pessoa.get("indicadorConjuge"):
                            # Remove 'indicadorConjuge' do dicionário
                            pessoa.pop("indicadorConjuge", None)
                            # Adiciona a modificação à lista de modificações
                            modificacoes.append(f"CNPJ {pessoa['ni']} com indicador de cônjuge removido")
                            pendencias.append(f'!! ATENÇÃO !! CNPJ  {pessoa['ni']} com indicador de cônjuge como TRUE, verifique no sistema')
                        
                        # Remove o campo regimeBens quando nao tiver conjuge
                        if pessoa.get("indicadorConjuge") == False and 'regimeBens' in pessoa:
                            pessoa.pop("regimeBens", None)
                            modificacoes.append(f'({pessoa.get("ni")}) regimeBens removido quando não possui conjuge' )
                            pendencias.append(f'(!! ATENÇÃO !! {pessoa.get("ni")}) regimeBens informado quando não possui conjuge verifique no sistema' )

                         # Verificar se "NI" dos alienantes ou adquirentes esta preenchido e não consta nenhum informação do conjuge
                         # ainda falta medir NI
                        if 'ni' in pessoa and len(pessoa['ni']) != 14 and "indicadorConjuge" not in pessoa:
                            # print(f'Parte {pessoa.get("ni")} NÃO TEM INDICAÇÃO SE possui conjuge')
                            pendencias.append(f'Parte {pessoa.get("ni")}, NÃO TEM INDICAÇÃO SE possui conjuge')
            
                        if pessoa.get('indicadorConjuge') and not pessoa.get('regimeBens'):
                            pendencias.append(f'Parte {pessoa.get("ni")} possui conjuge mas não foi informado regime de bens')
                            #print(f'Parte {pessoa.get("ni")}, possui conjuge mas não foi informado regime de bens')

                        if pessoa.get('indicadorEspolio') and not pessoa.get('cpfInventariante'):
                            pendencias.append(f'Parte {pessoa.get("ni")} é espólio mas não foi informado CPF do inventariante')
                            #print(f'Parte {pessoa.get("ni")} é espólio mas não foi informado CPF do inventariante')

                        # Verifica se o valor do percentual das partes
                        valor_percentual = pessoa.get('participacao')
                        if valor_percentual is not None:
                            if parte == 'alienantes':
                                percen_alienantes += valor_percentual
                                #print(f'Matricula = {declaracao.get("matricula")} -- {pessoa.get("ni")} é = {parte} / Percentual = {pessoa.get("participacao")}  // Percentual Alienantes = {percen_alienantes}')
                            else:
                                percen_transmitentes += valor_percentual
                                #print(f'Matricula = {declaracao.get("matricula")} -- {pessoa.get("ni")} é = {parte} / Percentual = {pessoa.get("participacao")}  // Percentual Transmitentes = {percen_transmitentes}')
                        else:
                            pendencias.append(f'Parte {pessoa.get("ni")} não informou percentual')
                        
            # Verificar se o percentual das partes é maior que 100
            if percen_alienantes > 100:
                    msg = f'{parte.upper()} com percentual MAIOR que 100'
                    pendencias.append(msg)
     
            if percen_transmitentes> 100:
                    msg = f'{parte.upper()} com percentual MAIOR que 100'
                    pendencias.append(msg)

            # Verificar se o percentual das partes é MENOR que 100
            if percen_alienantes < 100:
                    msg = f'{parte.upper()} com percentual MENOR que 100'
                    pendencias.append(msg)
            
            if percen_transmitentes < 100:
                    msg = f'{parte.upper()} com percentual MENOR que 100'
                    pendencias.append(msg)

            # Verificar se "NI" dos alienantes ou adquirentes é de 11 dígitos (CPF) e se "indicadorConjuge" é false
            if declaracao.get('indicadorAreaConstruidaNaoConsta') and 'areaConstruida' in declaracao:
                declaracao.pop('areaConstruida', None)
                pendencias.append('Área construída informada quando indicadorAreaConstruidaNaoConsta é true')

            if declaracao.get('indicadorAreaLoteNaoConsta') and 'areaLote' in declaracao:
                declaracao.pop('areaLote', None)
                pendencias.append('Área do lote informada quando indicadorAreaLoteNaoConsta é true')

            if declaracao.get('indicadorNaoConstaValorBaseCalculoItbiItcmd') and 'valorBaseCalculoItbiItcmd' in declaracao:
                pendencias.append(f'Valor base de cálculo ITBI/ITCMD {declaracao["valorBaseCalculoItbiItcmd"]} informado quando indicadorNaoConstaValorBaseCalculoItbiItcmd é true')
                declaracao.pop('valorBaseCalculoItbiItcmd', None)
                modificacoes.append('Valor base de cálculo ITBI/ITCMD  removido quando indicadorNaoConstaValorBaseCalculoItbiItcmd é true')

            if declaracao.get('indicadorNaoConstaValorOperacaoImobiliaria') and 'valorOperacaoImobiliaria' in declaracao:
                pendencias.append('Valor da operação imobiliária informado quando indicadorNaoConstaValorOperacaoImobiliaria é true')
                declaracao.pop('valorOperacaoImobiliaria', None)
                modificacoes.append('Valor da operação imobiliária removido quando indicadorNaoConstaValorOperacaoImobiliaria é true')

            if not declaracao.get('tipoLogradouro'):
                pendencias.append('Tipo de logradouro nulo')
                # print(f'O tipo de logradouro é nulo para a matricula: {declaracao["matricula"]}')

            if declaracao.get('FormaPagamento') == 7:
                if not declaracao.get('mesAnoUltimaParcela'):
                    pendencias.append('Forma de pagamento 7 sem mês/ano da última parcela')
                if not declaracao.get('valorPagoAteDataAto'):
                    pendencias.append('Forma de pagamento 7 sem valor pago até a data do ato')

            # Escrever no relatório de modificações
            if modificacoes:
                csv_writer_mod.writerow([declaracao.get('matricula', 'N/A'), declaracao.get('numeroRegistroAverbacao', 'N/A'),declaracao.get('dataLavraturaRegistroAverbacao', 'N/A'),'; '.join(modificacoes)])

            # Escrever no relatório de pendências
            if pendencias:
                csv_writer_pend.writerow([declaracao.get('matricula', 'N/A'), declaracao.get('numeroRegistroAverbacao', 'N/A'),declaracao.get('dataLavraturaRegistroAverbacao', 'N/A'),';'.join(pendencias)])

# Substituir ';' por ',' no arquivo de pendências
with open('relatorio_pendencias.csv', 'r', encoding='utf-8') as file_pend:
    conteudo = file_pend.read()

conteudo = conteudo.replace(';', ',')

with open('relatorio_pendencias.csv', 'w', encoding='utf-8') as file_pend:
    file_pend.write(conteudo)
    
# Substituir ';' por ',' no arquivo de modificaçoes
with open('relatorio_modificacoes.csv', 'r', encoding='utf-8') as file_pend:
    conteudo = file_pend.read()

conteudo = conteudo.replace(';', ',')

with open('relatorio_modificacoes.csv', 'w', encoding='utf-8') as file_pend:
    file_pend.write(conteudo)

# Salvar as alterações de volta para o arquivo JSON
with open('doi_modificado.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4)

print(f"Total de declarações: {declaracoes_count} {datetime.datetime.now()}")