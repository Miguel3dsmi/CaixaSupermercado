#------------- Declaração de variáveis -------------
escolha_produto: str = ""
produto: str = ""
quantidade: int = 0
preco_agranel: float = 0.0
preco_atacado: float = 0.0
lista_compras: list = []
valor_final: float = 0.0

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

def atualiza_carrinho(lista_compraz, produtos, quantidades, preco_agr, preco_atac):
    presente = False
    valor_prod = 0
    for elem in lista_compraz:
        if elem['produto'] == produtos:
            elem['quantidade'] += quantidades
            if elem['quantidade'] < 12:
                valor_prod = elem['quantidade'] * preco_agr
            else:
                valor_prod = elem['quantidade'] * preco_atac
            elem['valor_produto'] = valor_prod
            presente = True
    if not presente:
        if quantidades < 12:
            valor_prod = quantidades * preco_agr
        else:
            valor_prod = quantidades * preco_atac
        novo_item = {"produto": produtos, "quantidade": quantidades, "valor_produto": valor_prod}
        lista_compraz.append(novo_item)
    return valor_prod

#------------- Programa sendo executado -------------
while escolha_produto != 'sair':
    print(f"------ Lista de Produtos e Preços ------\n1. Banana -> R$ 0.30 preço granel ou R$ 0.25 preço atacado\n"
          f"2. Laranja -> R$ 0.40 preco granel ou R$ 0.35 preco atacado\n3. Maça -> R$ 0.50 preco granel ou R$ 0.45 preço atacado\n"
          f"4. Kiwi -> R$ 0.40 preço granel ou R$ 0.30 preço atacado\n\nEscolha o produto desejado ou digite 'SAIR' para sair:")
    try:
        escolha_produto = input("Escolha o produto desejado: ").lower().replace("ç","c").strip()
        match escolha_produto:
            case "1" | "banana":
                print("Você escolheu Banana!")
                produto = "banana"
                preco_agranel, preco_atacado = 0.3, 0.25
                quantidade = verificar_quantidade()
            case "2"| "laranja":
                print("Você escolheu Laranja!")
                produto = "laranja"
                preco_agranel, preco_atacado = 0.4, 0.35
                quantidade = verificar_quantidade()
            case "3"| "maca":
                print("Você escolheu Maça!")
                produto = "maça"
                preco_agranel, preco_atacado = 0.5, 0.45
                quantidade = verificar_quantidade()
            case "4"| "kiwi":
                print("Você escolheu Kiwi!")
                produto = "kiwi"
                preco_agranel, preco_atacado = 0.4, 0.3
                quantidade = verificar_quantidade()
            case "sair":
                print("Você escolheu encerrar essa operação.\nO sistema estará encerrando...\n\nVolte sempre!")
            case _:
                print("Opção inválida\n")
        if escolha_produto in ["1", "2", "3", "4", "banana", "laranja", "maca", "kiwi"] and quantidade > 0:
            valor_produto = atualiza_carrinho(lista_compras,produto,quantidade,preco_agranel,preco_atacado)
            print(f"\nVocê escolheu comprar {quantidade} x {produto}\nValor total: R${valor_produto:.2f}\n")
    except KeyboardInterrupt:
        print("Você optou por encerrar o programa antecipadamente!")
    except EOFError:
        print("Programa chegou ao fim sem receber os valores esperados!")
print(f"\n------ Seu carrinho de compras ------\n")
for i, item in enumerate(lista_compras,1):
    print(f"{i}. Produto: {item['produto']}, Quantidade: {item['quantidade']}, Valor: R${item['valor_produto']}")
    valor_final+= item['valor_produto']
print(f"\nO valor total da compra foi R${valor_final:.2f}")