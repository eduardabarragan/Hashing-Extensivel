from sys import argv
from hashExt import HashingExtencivel

#em todas as implementações deve-se chamar as funções do hashExt

def executa_operacao(arquivo_op):
    he = HashingExtencivel() #instância da classe Hashing
    he.carregar_diretorio() #(implementar na classe Hashing ainda). Lê o arquivo diretorio.dat e carrega ele na memória

    with open(arquivo_op, 'r') as arq_aberto: #abre arquivo de operações
        for linha in arq_aberto:
            op, valor = linha.strip().split() #separa comando (op) da chave (valor)
            chave = int(valor)

            if op == 'i':
                print(he.inserir(chave))
            elif op == 'b':
                print(he.buscar(chave))
            elif op == 'r':
                print(he.remover(chave))

    he.salvar_diretorio()
    

def imprime_diretorio():
    he = HashingExtencivel()
    he.carregar_diretorio()
    he.imprimir_diretorio()
    

def imprime_buckets():
    he = HashingExtencivel()
    he.carregar_diretorio()
    he.imprimir_buckets()


def main() -> None:
    if len(argv) == 3 and argv[1] == '-e':
        executa_operacao(argv[2])
    elif len(argv) == 2 and argv[1] == '-pd':
        imprime_diretorio()
    elif len(argv) == 2 and argv[1] == '-pb':
        imprime_buckets()
    
    #implementar tratamento de erros