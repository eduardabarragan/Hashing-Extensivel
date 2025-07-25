from sys import argv
from hashExt import HashingExtensivel


def buscar(he: HashingExtensivel, chave: int):
    achou,ref_bk, bk_encontrado = he.op_buscar(chave)
    if achou:
        print(f'> Busca pela chave {chave}: Chave encontrada no bucket {ref_bk}')
    
    else:
        print(f'> Busca pela chave {chave}: Chave não encontrada.')

def inserir(he: HashingExtensivel, chave: int):
    inseriu = he.op_inserir(chave)
    if inseriu:
        print(f'> Inserção da chave {chave}: Sucesso.')
    else:
        print(f'> Inserção da chave {chave}: Falha - Chave duplicada.')


def remover(he: HashingExtensivel, chave: int):
    pass

def executa_operacao(arquivo_op, he):

    with open(arquivo_op, 'r') as arq_aberto: #abre arquivo de operações
        for linha in arq_aberto:
            op, valor = linha.strip().split() #separa comando (op) da chave (valor)
            chave = int(valor)

            if op == 'i':
                inserir(he, chave)
            elif op == 'b':
                buscar(he, chave)
            elif op == 'r':
                remover(he, chave)

    
def imprime_diretorio(he: HashingExtensivel):
    impressao = he.imprimir_diretorio()
    print(impressao)
    
def imprime_buckets(he: HashingExtensivel):
    impressao = he.imprimir_buckets()
    print(impressao)


def main() -> None:
    he = HashingExtensivel() #instância da classe Hashing

    if len(argv) == 3 and argv[1] == '-e':
        executa_operacao(argv[2], he)
    elif len(argv) == 2 and argv[1] == '-pd':
        imprime_diretorio(he)
    elif len(argv) == 2 and argv[1] == '-pb':
        imprime_buckets(he)

    he.finaliza()
    #implementar tratamento de erros

if __name__ == '__main__':
    main()