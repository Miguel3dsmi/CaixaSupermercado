import pandas as pd
import mysql.connector

#------------- Declaração de variáveis -------------
escolha_produto: str = ""
produto: str = ""
questao: str = ""
escolha_acao: str = ""
quantidade: int = 0
preco_agranel: float = 0.0
preco_atacado: float = 0.0
valor_final: float = 0.0
lista_compras: list = []
lista_removidos: list = []
produto_selecionado: dict = {'idprodutos':"", 'nome':"", 'medida':"", 'valor_und':"", 'valor_atacado':""}

#------------- Função sendo executada -------------
def verificar_quantidade():
    while True:
        try:
            qtd = int(input("Quantos produtos deseja comprar: "))
            if qtd > 0:
                return qtd
            print("Digite uma quantidade maior que zero.\n")
        except ValueError:
            print("Entrada inválida! Digite apenas números inteiros.\n")

def atualiza_carrinho(lista_compraz, prod_sele, qtd):
    presente = False
    valor_prod = 0
    for elem in lista_compraz:
        if elem['produto'] == prod_sele['nome']:
            elem['quantidade'] += qtd
            if elem['quantidade'] < 12:
                valor_prod = elem['quantidade'] * prod_sele['valor_und']
            else:
                valor_prod = elem['quantidade'] * prod_sele['valor_atacado']
            elem['valor_produto'] = valor_prod
            presente = True
    if not presente:
        if qtd < 12:
            valor_prod = qtd * prod_sele['valor_und']
        else:
            valor_prod = qtd * prod_sele['valor_atacado']
        novo_item = {"produto": prod_sele['nome'], "quantidade": qtd, "valor_produto": valor_prod}
        lista_compraz.append(novo_item)
    return valor_prod

def remover_item(lista_compraz):
    end = True
    li_remov = None
    print(f"------ Seu carrinho de compras ------\n")
    for e, elem in enumerate(lista_compraz, 1):
        print(
            f"{e}. Produto: {elem['produto']}, Quantidade: {elem['quantidade']}, Valor: R${elem['valor_produto']:.2f}")
    while end != False:
        try:
            remove = int(input("Quais desses itens acima deseja excluir? "))
            if remove > 0:
                remove = remove - 1
                li_remov = lista_compraz.pop(remove)
                print(f"{remove} excluído.")
                end = False
            else:
                raise IndexError
        except IndexError:
            print("O Valor informardo não está presente nessa lista.")
        except ValueError:
            print("Essa função busca o item a ser removido apenas pelo numero de indexação.")
    return li_remov

def visualizar_exclusao (lista_removidoz):
    if lista_removidoz:
        print("Você escolheu visualizar os item que foram excluídos do carrinho!\n")
        for e, elem in enumerate(lista_removidoz, 1):
            print(f"{e}. Produto removido: {elem['produto']}\n")
    else:
        print("Lista Vazia")

def restaurar (lista_removidoz):
    rest= []
    escolha = ""
    while escolha != "sair" and lista_removidoz:
        for e, elem in enumerate(lista_removidoz, 1):
            print(f"{e}. Produto: {elem['produto']}\n")
        try:
            escolha = input("Escolha qual desses itens deseja restaurar ou escolha 'Sair' caso queira encerrar: ").lower().strip()
            if escolha != "sair":
                escolha = int(escolha)
                if escolha > 0:
                    escolha -= 1
                    rest.append(lista_removidoz.pop(escolha))
                else:
                    print('Escolha invalida!\nLista não possui item número 0.')
        except IndexError:
            print("O Valor informardo não está presente nessa lista.")
        except ValueError:
            print("Essa função busca o item a ser removido apenas pelo numero de indexação.")
    return rest

#------------- Programa sendo executado -------------
data = pd.read_csv("Produtos.csv") #Sistema lendo os arquivos
mercadorias = data.to_dict(orient="records") #Sistema convertendo os arquivos em dicionário

while escolha_produto != 'sair':
    print(f"------ Lista de Produtos ------\nEscolha um dos itens abaixo:\n(recomendamos inserir o numero do produto)\n")
    for i,item in enumerate(mercadorias, 1):
        print(f"{i}. {item['nome']}")
    print(f"\nEscolha o produto desejado ou digite 'SAIR' para sair!")
    try:
        escolha_produto = input("Escolha o produto desejado: ").lower().replace("ç","c").replace("ã","a").strip()
        if escolha_produto != "sair":
            for item in mercadorias:
                if str(item['idprodutos']) == escolha_produto or item['nome'].lower() == escolha_produto:
                    produto_selecionado = item
                    print("\nProduto encontrado!")
                    quantidade = verificar_quantidade()
                    break
            valor_produto = atualiza_carrinho(lista_compras, produto_selecionado, quantidade)
            print(f"\nVocê escolheu comprar {quantidade} x {produto_selecionado['nome']}\nValor total: R${valor_produto:.2f}\n")
            escolha_acao = input("------ Escolha o que deseja fazer agora? ------\n1. Adicionar um novo item ao carrinho;\n2. Excluir um item do carrinho"
                                 "\n3. Visualizar itens excluidos\n4. Sair do programa \n").lower().strip()[0:1]
            match escolha_acao:
                case "1" | "a":
                    print("Você escolheu adicionar um novo item ao carrinho!\n")
                case "2" | "e" | "r":
                    print(f"Você escolheu excluir um novo item do carrinho!\n")
                    lista_removidos.append(remover_item(lista_compras))
                case "3" | "v":
                    visualizar_exclusao(lista_removidos)
                    if lista_removidos:
                        questao = input("Deseja restaurar algum dos itens listados? (s/n) ").strip().lower()[0:1]
                        while questao not in ["s","n"]:
                                print("Responda apenas com 's' para sim ou 'n' para não.")
                                questao = input("Deseja restaurar algum dos itens listados? (s/n): ").strip().lower()[0:1]
                        if questao == "s":
                            lista_compras.extend(restaurar(lista_removidos))
                        else:
                            print("Voltando ao menu.")
                case "4" | "s":
                    print("Você escolheu sair do programa!\nO sistema estará encerrando...\n\nVolte sempre!")
                    escolha_produto = "sair"
        else:
            print("Você escolheu encerrar essa operação.\nO sistema estará encerrando...\nVolte sempre!")
    except KeyboardInterrupt:
        print("\nVocê optou por encerrar o programa antecipadamente!")
    except EOFError:
        print("\nPrograma chegou ao fim sem receber os valores esperados!")
    except ValueError:
        print("\nProduto informado não condiz com itens no sistema!\nTente novamente!\n\n")
print(f"\n------ Seu carrinho de compras ------\n")
for i, item in enumerate(lista_compras,1):
    print(f"{i}. Produto: {item['produto']}, Quantidade: {item['quantidade']}, Valor: R${item['valor_produto']:.2f}")
    valor_final+= item['valor_produto']
print(f"\nO valor total da compra foi R${valor_final:.2f}")