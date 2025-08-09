# Sistema de Gerenciamento da loja Coffe Shops Tia Rosa
# Criado e desenvolvido por João Ricardo Vasconcelos Pires

from datetime import datetime

# Informações do sistema
produtos = [
    {"codigo": 1, "nome": "Cafézinho Expresso", "preco": 5.5, "estoque": 45},
    {"codigo": 2, "nome": "Cafézinho Coado", "preco": 4.5, "estoque": 60},
    {"codigo": 3, "nome": "Café com leite", "preco": 4.0, "estoque": 50},
    {"codigo": 4, "nome": "Cappuccino", "preco": 7.5, "estoque": 30},
    {"codigo": 5, "nome": "Pão na chapa", "preco": 4.0, "estoque": 30},
    {"codigo": 6, "nome": "Bauru", "preco": 6.5, "estoque": 25},
    {"codigo": 7, "nome": "Pão de Queijo", "preco": 5.0, "estoque": 60},
    {"codigo": 8, "nome": "Fatia Bolo de Cenoura", "preco": 8.5, "estoque": 24}
]

clientes = []
pedidos = []

# Funções do Menu Principal da loja
def mostrar_menu():
    print("\n=== CARDAPIO PRINCIPAL ===")
    print("1. Olhar Cardápio")
    print("2. Cadastrar um cliente")
    print("3. Fazer um pedido")
    print("4. Emitir relatório de consumos")
    print("0. Sair")

    while True:
        opcao = input("Escolha uma opção: ")
        if opcao in ["0", "1", "2", "3", "4"]:
            return opcao
        print("Opção inválida! Digite as opções 0, 1, 2, 3 ou 4.")

# Código para ver o cardápio disponível
def ver_cardapio():
    print("\n=== CONHEÇA NOSSO CARDÁPIO ===")
    print("{:<5} {:<20} {:<10} {:<10}".format(
        "Cód.", "Produto", "Preço", "Estoque"))
    print("-" *45)

    for produto in produtos:
        print("{:<5} {:<20} R$ {:<8.2f} {:<10}".format(
            produto['codigo'],
            produto['nome'],
            produto['preco'],
            produto['estoque']))
    input("\nPressione ENTER para continuar.")

# Código para sistema de cadastro de clientes da loja
def cadastrar_cliente():
    print("\n==== CADASTRO DE CLIENTE ====")

    while True:
        cpf = input("Digite o CPF (OBS.: somente números):")
        if cpf.isdigit() and len(cpf) == 11:
            break
        print("CPF inválido! Número incorreto ou foram utilizados símbolos. Inserir apenas números.")

    # Para verificar se o cadastro já existe no sistema
    for cliente in clientes:
        if cliente['cpf'] == cpf:
            print("Este cliente já está cadastrado!")
            return

    nome = input("Digite o nome completo: ").title()

    novo_cliente = {
        "cpf": cpf,
        "nome": nome,
        "pontos": 0
    }

    clientes.append(novo_cliente)
    print(f"\nCliente {nome} cadastrado com sucesso!")
    input("Pressione ENTER para continuar.")

# Código para Registro de Pedidos no Sistema
def fazer_pedido():
    if not clientes:
        print("\nNenhum cliente está cadastrado. Primeiro, realize o cadastro.")
        input("Pressione ENTER para continuar.")
        return

    print("\n=== FAZER UM PEDIDO ===")
    print("Clientes disponíveis:")
    for i, cliente in enumerate(clientes, 1):
        print(f"{i}. {cliente['nome']} (CPF: {cliente['cpf']})")

    try:
        opcao = int(input("\nEscolha o cliente (número): ")) - 1
        cliente = clientes[opcao]
    except ValueError:
        print("Favor inserir um número válido.")
        input("Pressione ENTER para continuar.")
        return
    except IndexError:
        print("Número de cliente inválido. Escolha um número contido na lista.")
        input("Pressione ENTER para continuar.")
        return

    # Tudo abaixo agora está corretamente indentado dentro da função
    itens_pedido = []
    total = 0.0

    while True:
        ver_cardapio()
        print("0. Finalizar o pedido")

        try:
            codigo = int(input("\nDigite o código do produto escolhido: "))
            if codigo == 0:
                break

            produto_encontrado = None
            for produto in produtos:
                if produto['codigo'] == codigo:
                    produto_encontrado = produto
                    break

            if produto_encontrado:
                try:
                    quantidade = int(input(f"Quantidade de {produto_encontrado['nome']}: "))

                    if quantidade <= 0:
                        print("Quantidade deve ser positiva!")
                        continue

                    if quantidade > produto_encontrado['estoque']:
                        print(f"Estoque insuficiente. Temos apenas {produto_encontrado['estoque']} unidades disponíveis.")
                    else:
                        itens_pedido.append({
                            "produto": produto_encontrado['nome'],
                            "quantidade": quantidade,
                            "preco_unitario": produto_encontrado['preco']
                        })
                        total += quantidade * produto_encontrado['preco']
                        produto_encontrado['estoque'] -= quantidade
                        print(f"Adicionado {quantidade}x {produto_encontrado['nome']} ao pedido.")
                except ValueError:
                    print("Quantidade deve ser um número inteiro!")
            else:
                print("Produto não encontrado.")
        except ValueError:
            print("Código do produto deve ser um número!")

    # Finalização do pedido
    if not itens_pedido:
        print("Pedido vazio. Nada foi registrado.")
        input("Pressione ENTER para continuar.")
        return

    pontos = int(total // 10)
    cliente['pontos'] += pontos

    novo_pedido = {
        "numero": len(pedidos) + 1,
        "cliente": cliente['nome'],
        "itens": itens_pedido,
        "total": total,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "pontos_ganhos": pontos
    }
    pedidos.append(novo_pedido)

    print("\n=== PEDIDO REGISTRADO ===")
    print(f"Cliente: {cliente['nome']}")
    print(f"Data: {novo_pedido['data']}")
    print("\nItens:")
    for item in itens_pedido:
        print(f"{item['quantidade']}x {item['produto']} - R$ {item['preco_unitario']:.2f} cada")
    print(f"\nTotal: R$ {total:.2f}")
    print(f"Pontos ganhos: {pontos}")
    print(f"Total de pontos agora: {cliente['pontos']}")
    input("\nPressione ENTER para continuar.")

# Relatório de vendas da loja
def ver_relatorio():
    print("\n=== RELATÓRIO DE VENDAS===")
    print(f"Total de clientes: {len(clientes)}")
    print(f"Total de pedidos: {len(pedidos)}")

    if pedidos:
        total_vendas = sum(p['total'] for p in pedidos)
        print(f"\nTotal em vendas: R$ {total_vendas:.2f}")

        print("\nÚltimos pedidos:")
        for pedido in pedidos[-3:]: # Mostrar apenas os últimos 3 pedidos
            print(f"\nPedido #{pedido['numero']} - {pedido['data']}")
            print(f"Cliente: {pedido['cliente']}")
            print(f"Total: R$ {pedido['total']:.2f}")
            print(f"Pontos ganhos: {pedido['pontos_ganhos']}")

    input("\nPressione ENTER para continuar.")

# Estrutura e loop principal do Programa da loja
if __name__ == "__main__":
    print("Seja bem-vindo ao Coffee Shops Tia Rosa!")
    print("Sistema de Gestão de Negócios - Versão 1.0")

    while True:
        opcao = mostrar_menu()

        if opcao == "1":
            ver_cardapio()
        elif opcao == "2":
            cadastrar_cliente()
        elif opcao == "3":
            fazer_pedido()
        elif opcao == "4":
            ver_relatorio()
        elif opcao == "0":
            print("\nObrigado por utilizar nosso sistema!")
            print("Agradecemos a preferência e volte sempre ao Coffee Shops Tia Rosa!")
            break
