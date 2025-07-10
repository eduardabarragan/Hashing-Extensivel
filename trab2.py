from sys import argv
from hashExt import HashingExtencivel

#em todas as implementação deve-se chamar as funções do hashExt

def executa_operacao(arq):
    #implementar
    

def imprime_dir():
    #implementar
    

def imprime_buckets():
    #implememtar
   


def main() -> None:
    if len(argv) == 3 and argv[1] == '-e':
        executa_operacao(argv[2])
    elif len(argv) == 2 and argv[1] == '-pd':
        imprime_dir()
    elif len(argv) == 2 and argv[1] == '-pb':
        imprime_buckets()
    
    #implementar tratamento de erros