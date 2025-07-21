from struct import pack, unpack, calcsize
import io
import os

#Constantes
ARQUIVO_BK = "buckets.dat"
ARQUIVO_DIR = "diretorio.dat"
TAM_MAX_BK = 5
NULO = -1

FORMATO_PROF = f'i'
PROFSIZE = calcsize(FORMATO_PROF)
FORMATO_REF = f'i'
REFSIZE = calcsize(FORMATO_REF)
#Formato para struct bucket: int prof, int contaChaves, TAM_MAX_BK ints para chaves
FORMATO_BK = f'ii{TAM_MAX_BK}i'
BKSIZE = calcsize(FORMATO_BK)

#Revisar 
class Bucket:

    def __init__(self, prof = 0, cont= 0, chaves = []) -> None:
        assert len(chaves) <= TAM_MAX_BK, 'Erro: número de chaves maior do que o máximo permitido'
        self.prof = prof
        self.cont = cont
        chaves += [NULO]*(TAM_MAX_BK - len(chaves))
        self.chaves = chaves

class Diretorio:
    def __init__(self, ref_bk: int = 0) -> None:
        self.prof_dir = 0
        self.refs = [ref_bk]

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
            self.dir.prof_dir = 0 

            #Cria um bucket vazio no arquivo de buckets
            bucket = Bucket()
            # O serve para* desmontar a lista de chaves e enviar cada valor separado para o pack exemplo pack(FORMATO_BK,0,0,[1,2,3]) teremos = pack(FORMATO_BK,0,0,1,2,3)
            dados_bk = pack(FORMATO_BK, bucket.prof, bucket.cont, *bucket.chaves)
            self.arq_bk.seek(0)
            self.arq_bk.write(dados_bk)

            #Atribua seu RRN ao dir.refs
            self.dir.refs == [0]


    def gerar_endereco(chave, profundidade):
        '''Função hash para gerar endereço da chave'''
        val_ret = 0 #Armazenará a sequência de bits
        mascara = 1 #Para extrair o bit menos significativo
        val_hash = chave 
        for j in range(profundidade):
            val_ret = val_ret << 1 #Extrai o bit de mais baixa ordem de val_hash
            bit_baixa_ordem = val_hash & mascara
            val_ret = val_ret | bit_baixa_ordem #Insire bit_baixa_ordem no final de val_ret
            val_hash = val_hash >> 1

        return val_ret

    #Funcao de busca
    def op_buscar(self,chave):
        with open(ARQUIVO_BK, 'rb') as arq_bk:
            endereco = self.gerar_endereco(chave,self.dir.prof_dir) 
            ref_bk = self.dir.refs[endereco]

            #Posiciona o ponteiro para encontrar o bucket da ref_bk
            arq_bk.seek(ref_bk * BKSIZE)
            bk_bytes = arq_bk.read(BKSIZE)

            #Le os dados correspondentes para bk_encontrado
            bk_encontrado = Bucket()
            dados_bk = unpack(FORMATO_BK,bk_bytes)
            bk_encontrado.prof = dados_bk[0]
            bk_encontrado.cont = dados_bk[1]
            bk_encontrado.chaves = dados_bk[2: 2 + bk_encontrado.cont]

            #Procura pela chave
            for reg in bk_encontrado.chaves:
                if reg == chave:
                    return True, ref_bk,bk_encontrado
                
            return False, ref_bk, bk_encontrado


    #Funcao de insercao
    def op_inserir(self, chave: int):
        #busca pela chave usando a função op_buscar
        achou, ref_bk, bk_encontrado = self.op_buscar(chave)
        if achou:
            return False  # Erro: chave duplicada
        self.inserir_chave_bk(chave, ref_bk, bk_encontrado) 
        return True

    def inserir_chave_bk(self, chave:int, ref_bk: int, bucket:Bucket):
        #se encontrar espaço, a chave é inserida e a operação termina
        if bucket.cont < TAM_MAX_BK: 
            #Insere a chave no bucket
            posi_nulo =  bucket.cont
            bucket.chaves[posi_nulo] = chave
            bucket.cont+=1

            #Escreve em ref_bk no arquivo de buckets
            with open(ARQUIVO_BK, 'r+b') as arq_bk:
                arq_bk.seek(ref_bk * BKSIZE)
                arq_bk.write(pack(FORMATO_BK,bucket.prof,bucket.cont, *bucket.chaves))

        else: 
            # Se o bucket estiver cheio, chama a função dividir_bk e tenta inserir novamente
            self.dividir_bk(ref_bk, bucket)
            self.op_inserir(chave)  #Recursão indireta

    def dividir_bk(self, ref_bk: int, bucket: Bucket):
        if bucket.prof == self.dir.prof_dir:
            self.dobrar_dir()

        #Crie um novo_bucket
        novo_bk: Bucket = Bucket()
        arq_bk = open(ARQUIVO_BK, 'rb+')

        #Atribui o seu RRN a ref_novo_bucket
        arq_bk.seek(0, 2)  
        tam_arq = arq_bk.tell()
        ref_novo_bucket = tam_arq // BKSIZE

        novo_inicio, novo_fim = self.encontrar_novo_intervalo(bucket)
        #Insere novo_bucket no dir de acordo com novo_inicio e novo_fim
        for i in range(novo_inicio,novo_fim + 1):
            self.dir.refs[i] = ref_novo_bucket
        
        #Incrementa bucket.prof e novo_bucket.prof receber bucket.prof
        bucket.prof += 1
        novo_bk.prof = bucket.prof

        #Redistribui as chaves entre bucket e novo_bucket considerando a dir_prof
        redistribuir = []
        bucket.chaves = []
        novo_bk.chaves = []

        for chave in bucket.chaves:
            if chave != NULO:
                redistribuir.append(chave)

        for chave in redistribuir:
            endereco = self.gerar_endereco(chave,self.dir.prof_dir) 
            ref = self.dir.refs[endereco]
            if ref == ref_novo_bucket:
                novo_bk.chaves.append(chave)
            else:
                bucket.chaves.append(chave)

        #Preenche o final com NULO até TAM_MAX_BK
        bucket.cont = len(bucket.chaves)
        bucket.chaves += [NULO]*(TAM_MAX_BK - bucket.cont )

        novo_bk.cont = len(novo_bk.chaves)
        novo_bk.chaves += [NULO]*(TAM_MAX_BK - novo_bk.cont)

        #Escreva bucket e novo_bucket nos respectivos RRNs do arquivo de buckets
        arq_bk.seek(ref_bk * BKSIZE)
        dados_bk = pack(FORMATO_BK, bucket.prof, bucket.cont, *bucket.chaves)
        arq_bk.write(dados_bk)
        
        arq_bk.seek(ref_novo_bucket * BKSIZE)
        dados_novo_bk = pack(FORMATO_BK, novo_bk.prof, novo_bk.cont, *novo_bk.chaves)
        arq_bk.write(dados_novo_bk)



    def dobrar_dir(self):
        '''Caso o diretório precise ser espandido, essa funçao serve para dobrar o tamanho do diretório '''
        novas_refs = []
        #Insere cada referência em dir.refs duas vezes em novas_refs
        for ref in self.dir.refs:
            novas_refs.append(ref)  # primeira 
            novas_refs.append(ref)  # segunda
        self.dir.refs = novas_refs # substitui a lista de referências do diretório
        self.dir.prof_dir += 1 # incrementa a profundidade global do diretório

    def encontrar_novo_intervalo(self, bucket:Bucket):
        mascara = 1
        chave = bucket.chaves[0]
        end_comum = self.gerar_endereco(chave, bucket.prof)
        end_comum = end_comum << 1
        end_comum = end_comum | mascara
        bits_a_preencher = self.dir.prof_dir - (bucket.prof + 1)
        novo_inicio, novo_fim = end_comum, end_comum
        for i in range(bits_a_preencher):
            novo_inicio = novo_inicio << 1
            novo_fim = novo_fim << 1
            novo_fim = novo_fim | mascara
        return novo_inicio, novo_fim

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

    def finaliza(self):
        #Abre o arquivo de diretorio e de buckets
        arq_bk = open(ARQUIVO_BK, 'rb')
        arq_dir = open(ARQUIVO_DIR,'wb')
        arq_dir.seek(0)

        #Escreve a profundidade
        arq_dir.write(pack(FORMATO_PROF, self.dir.prof_dir))

        #Escreve os RRN's dos buckets
        for ref in self.dir.refs:
            arq_dir.write(pack(FORMATO_REF, ref))
        
        #Fecha os arquivos
        arq_dir.close()
        arq_bk.close()
        

#Nao tem pseudocodigo
    def carregar_diretorio():
        pass

    def salvar_diretorio():
        pass

    def imprimir_diretorio(self,):
        tam = pow(2, self.dir.prof_dir)
        saida = f'Tamanho atual do diretorio = {tam}\n'
        for i, ref in enumerate(self.dir.refs): #Revisar o uso do enumerate
            saida += f'dir[{i}] = bucket[{ref}]\n'
        return saida
      
        
    def imprimir_buckets():
        pass
