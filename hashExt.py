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
        self.registros = [] #Lista com os registros que estão no bucket

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
        endereço=gerar_endereço(chave,prof_dir) 
        ref_bk=dir.refs[endereço]
        bk_encontrado= ler_bucket(ref_bk)
        for registro in bk_encontrado.registros:
            if registro.chave==chave:
                return True, ref_bk,bk_encontrado
            
        return False, ref_bk, bk_encontrado


    #Funcao de insercao
    def op_inserir(self, chave):
        achou, ref_bk, bk_encontrado = self.op_buscar(chave) #busca pela chave usando a função op_buscar
        #se a chave for encontrada:
        if achou:
            return False  # Erro: chave duplicada
        self.inserir_chave_bk(chave, ref_bk, bk_encontrado) # chama a função inserir_chave_bk e estuda os casos, para conseguir inserir adequadamente 
        return True

    def inserir_chave_bk(self, chave, ref_bk, bucket):
        if bucket.cont < MAX_BK_SIZE: # se encontrar espaço, a chave é inserida e a operação trmina
            bucket.registros.append(chave)
            bucket.cont+=1
            escrever_bucket(ref_bk,bucket) #salva no arquivo

        else: 
            # Se o bucket estiver cheio, chama a função dividir_bk e tenta inserir novamente
            self.dividir_bk(ref_bk, bucket)
            self.op_inserir(chave)  # Recursão indireta

    def dividir_bk(self, ref_bk, bucket):

        if bucket.prof == self.prof_dir:
            self.dobrar_dir()

        novo_bucket = Bucket()
        ref_novo_bucket = self.alocar_novo_bucket(novo_bucket)

        bucket.prof += 1
        novo_bucket.prof = bucket.prof

        for i in range(len(self.dir.refs)):
            endereco_bin = format(i, f'0{self.prof_dir}b')  # binário do índice com padding
            if endereco_bin[-bucket.prof:] == gerar_endereco_bits(ref_novo_bucket, bucket.prof):
                if self.dir.refs[i] == ref_bk:
                    self.dir.refs[i] = ref_novo_bucket

        todos = bucket.registros.copy()
        bucket.registros.clear()
        novo_bucket.registros.clear()

        for chave in todos:
            endereco = gerar_endereço(chave, bucket.prof)
            if self.dir.refs[endereco] == ref_bk:
                bucket.registros.append(chave)
            else:
                novo_bucket.registros.append(chave)

        bucket.cont = len(bucket.registros)
        novo_bucket.cont = len(novo_bucket.registros)

        escrever_bucket(ref_bk, bucket)
        escrever_bucket(ref_novo_bucket, novo_bucket)


    def dobrar_dir(self):
        #caso o diretório precise ser espandido, essa funçao serve para dobrar o tamanho do diretório 
        novas_refs = []
        #Insere cada referência em dir.refs duas vezes em novas_refs
        for ref in self.dir.refs:
            novas_refs.append(ref)  # primeira 
            novas_refs.append(ref)  # segunda
        self.dir.refs = novas_refs # substitui a lista de referências do diretório
        self.dir.dirProf += 1 # incrementa a profundidade global do diretório

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
