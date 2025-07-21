from sys import argv
from hashExt import HashingExtensivel


def buscar(he: HashingExtensivel, chave: int):
    achou,ref_bk, bk_encontrado = he.op_buscar(chave)
    if achou:
        print(f'> Busca pela chave {chave}: Chave encontrada no bucket {ref_bk}')
    
    else:
        print(f'> Busca pela chave {chave}: Chave não encontrada.')

def inserir(he: HashingExtensivel, chave: int):
    pass

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
    he.imprimir_diretorio()

def imprime_buckets(he: HashingExtensivel):
    he.imprimir_buckets()


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