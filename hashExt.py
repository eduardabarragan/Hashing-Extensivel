from struct import pack, unpack, calcsize
import io
import os

#Constantes
MAX_BK_SIZE = 5
NULO = -1

FORMATO_PROF = f'i'
PROFSIZE = calcsize(FORMATO_PROF)
#Formato para struct bucket: int prof, int contaChaves, MK_BK_SIZE ints para chaves
FORMATO_BK = f'ii{MAX_BK_SIZE}i'
BKSIZE = calcsize(FORMATO_BK)

class Bucket:

    def __init__(self, prof = 0, contChaves= 0, chaves = []) -> None:
        assert len(chaves) <= MAX_BK_SIZE, 'Erro: número de chaves maior do que o máximo permitido'
        self.prof = prof
        self.cont = contChaves
        chaves += [NULO]*(MAX_BK_SIZE - len(chaves))
        self.chaves = chaves

class Diretorio:
    def __init__(self, bkRef: int = 0) -> None:
        self.dirProf = 0
        self.refs = [bkRef]
    
    def __str__(self) -> str:
        tam = pow(2, self.dirProf)
        strDir = f'Tamanho atual do diretorio = {tam}\n'
        for i, ref in enumerate(self.refs):
            strDir += f'dir[{i}] = bucket[{ref}]\n'
        return strDir

class HashingExtencivel:
    def _init_(self):
        pass

    def gerar_endereco(chave): #aplicar hash(vai ser o valor da chave em binario) e considerar a profundidade global
        pass

    def carregar_diretorio():
        pass

    def salvar_diretorio():
        pass

    def inserir(chave):
        pass

    def buscar(chave):
        pass

    def remover(chave):
        pass

    def imprimir_diretorio():
        pass

    def imprimir_buckets():
        pass