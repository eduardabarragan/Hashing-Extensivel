from struct import pack, unpack, calcsize
import io
import os

#Constantes
ARQUIVO_BK = "bucket.dat"
ARQUIVO_DIR = "dir.dat"
MAX_BK_SIZE = 5
NULO = -1

FORMATO_PROF = f'i'
PROFSIZE = calcsize(FORMATO_PROF)
FORMATO_REF = f'i'
REFSIZE = calcsize(FORMATO_REF)
#Formato para struct bucket: int prof, int contaChaves, MK_BK_SIZE ints para chaves
FORMATO_BK = f'ii{MAX_BK_SIZE}i'
BKSIZE = calcsize(FORMATO_BK)

#Revisar 
class Bucket:

    def __init__(self, prof = 0, contChaves= 0, chaves = []) -> None:
        assert len(chaves) <= MAX_BK_SIZE, 'Erro: número de chaves maior do que o máximo permitido'
        self.prof = prof
        self.cont = contChaves
        chaves += [NULO]*(MAX_BK_SIZE - len(chaves))
        self.chaves = chaves

#Revisar funcao 
class Diretorio:
    def __init__(self, bkRef: int = 0) -> None:
        self.prof_dir = 0
        self.refs = [bkRef] 
    
    def __str__(self) -> str:
        tam = pow(2, self.prof_dir)
        strDir = f'Tamanho atual do diretorio = {tam}\n'
        for i, ref in enumerate(self.refs):
            strDir += f'dir[{i}] = bucket[{ref}]\n'
        return strDir

class HashingExtensivel:
    def __init__(self, arq_bk = ARQUIVO_BK, arq_dir = ARQUIVO_DIR):
        #Verifica se o hashing existe 
        if os.path.exists(arq_bk) and os.path.exists(arq_dir):
            #Abrindo arquivo de diretório e de bucket
            self.arq_bk = open(arq_bk, 'rb+')
            self.arq_dir = open(arq_bk, 'rb+')

            #Lendo a profundidade do diretorio
            self.arq_dir.seek(0)
            prof_bytes = self.arq_dir.read(PROFSIZE)
            prof_dir = unpack(FORMATO_PROF, prof_bytes)[0]
            #Calculo do tamanho do diretorio
            tam = pow(2, prof_dir)

            #Lendo os registros do arquivo de diretório para um objeto diretorio
            self.dir = Diretorio()
            self.dir.prof_dir = prof_dir
            self.dir.refs = []
           
            for i in range(tam):
                ref_bytes = self.arq_dir.read(REFSIZE)
                rrn = unpack(FORMATO_REF, ref_bytes)[0]
                self.dir.refs.append(rrn)

        else:
            #Cria arquivos
            self.arq_bk = open(arq_bk, 'w+b')
            self.arq_dir = open(arq_dir, 'w+b')

            #Cria um objeto diretorio e atribua a dir
            self.dir = Diretorio()
            #Inicializa prof_dir com 0
            self.dir.prof_dir = 0 #Ver com a Valeria se precisa msm pq o propria clase faz isso
          

            #Cria um bucket vazio no arquivo de buckets
            bucket = Bucket()
            # O serve para* desmontar a lista de chaves e enviar cada valor separado para o pack exemplo pack(FORMATO_BK,0,0,[1,2,3]) teremos = pack(FORMATO_BK,0,0,1,2,3)
            dados_bk = pack(FORMATO_BK, bucket.prof, bucket.cont, *bucket.chaves)
            self.arq_bk.seek(0)
            self.arq_bk.write(dados_bk)

            #Atribua seu RRN ao dir.refs
            self.dir.refs == [0]

            #Salva a profundidade e o RRN no arquivo de diretório
            self.arq_dir.seek(0)
            self.arq_dir.write(pack(FORMATO_PROF, self.dir.prof_dir))
            self.arq_dir.write(pack(FORMATO_REF, self.dir.refs[0]))






    def gerar_endereco(chave): #aplicar hash(vai ser o valor da chave em binario) e considerar a profundidade global
        #Eduarda
        pass

    #Funcao de busca
    def op_buscar(chave):
        #Ana
        pass

    #Funcao de insercao
    def op_inserir(chave):
        #Deby
        pass

    def inserir_chave_bk(chave, ref_bk, bucket):
        pass

    def dividir_bk(ref_bk, bucket):
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

#Nao tem pseudocodigo
    def carregar_diretorio():
        pass

    def salvar_diretorio():
        pass

    def imprimir_diretorio():
        pass

    def imprimir_buckets():
        pass
