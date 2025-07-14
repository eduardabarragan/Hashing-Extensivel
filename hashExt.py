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
    def __init__(self):
        pass

    def gerar_endereco():
        pass

    #Funcao de busca
    def op_buscar(chave):
        pass

    #Funcao de insercao
    def op_inserir(chave):
        pass

    def inserir_chave_bk(chave, ref_bk, bucket):
        pass

    def dividir_bk (ref_bk, bucket):
        pass

    def dobrar_dir():
        pass

    def encontrar_novo_intervalo(bucket):
        pass

    def encontrar_novo_intervalo(bucket):
        pass
    
    #Funcao de remocao
    def op_remover(chave):
        pass

    def remover_chave_bk(chave, ref_bk, bucket):
        pass

    def tentar_combinar_bk (chave_removida, ref_bk, bucket):
        pass

    def encontrar_bk_amigo(chave_removida, bucket):
        pass

    def combinar_bk(ref_bk, bucket, ref_amigo, bk_amigo):
        pass

    def tentar_diminuir_dir():
        pass

