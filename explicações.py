def op_buscar(chave):
    '''
    A função op_buscar(chave) tem como objetivo realizar a busca de uma chave em uma estrutura de hashing extensível. 
    Para isso, ela utiliza a função gerar_endereço, que calcula o índice no diretório com base na chave informada e na profundidade global (prof_dir). 
    Esse índice é usado para acessar a referência do bucket correspondente no diretório (ref_bk). 
    Em seguida, o conteúdo do bucket é carregado por meio da função ler_bucket, retornando um objeto (bk_encontrado) que contém os registros armazenados naquele bucket. 
    A função percorre os registros do bucket e, se encontrar um registro com a chave igual à fornecida, retorna uma tupla contendo True, a referência do bucket e o próprio bucket encontrado. 
    Caso a chave não seja encontrada, a função retorna False, junto com a mesma referência e o bucket onde a busca foi realizada.
    '''
    endereço = gerar_endereço(chave, prof_dir) 
    ref_bk = dir.refs[endereço]
    bk_encontrado = ler_bucket(ref_bk)
    
    for registro in bk_encontrado.registros:
        if registro.chave == chave:
            return True, ref_bk, bk_encontrado
            
    return False, ref_bk, bk_encontrado

def op_inserir(self, chave):
    '''
    A função op_inserir tem como objetivo inserir uma chave na estrutura de hashing extensível. 
    Inicialmente, ela utiliza a função op_buscar para verificar se a chave já existe. 
    Se a chave for encontrada, a inserção é interrompida e a função retorna False, indicando erro por chave duplicada. 
    Caso contrário, a função chama inserir_chave_bk, que tenta inserir a chave no bucket apropriado. 
    Se a inserção for bem-sucedida, a função retorna True.
    '''
    achou, ref_bk, bk_encontrado = self.op_buscar(chave)
    if achou:
        return False  # Erro: chave duplicada
    self.inserir_chave_bk(chave, ref_bk, bk_encontrado)
    return True

def inserir_chave_bk(self, chave, ref_bk, bucket):
    '''
    A função inserir_chave_bk é responsável por inserir uma chave em um bucket específico, levando em consideração o tamanho máximo permitido. 
    Se o bucket tiver espaço disponível (ou seja, se o contador de registros for menor que MAX_BK_SIZE), a chave é adicionada ao bucket, o contador é incrementado, 
    e o bucket atualizado é escrito de volta no arquivo usando a função escrever_bucket. 
    No entanto, se o bucket estiver cheio, a função chama dividir_bk para realizar o split do bucket, ajustando a estrutura conforme necessário. 
    Após a divisão, a função op_inserir é chamada novamente de forma recursiva para tentar inserir a chave no bucket correto após a reestruturação.
    '''
    if bucket.cont < MAX_BK_SIZE:
        bucket.registros.append(chave)
        bucket.cont += 1
        escrever_bucket(ref_bk, bucket)
    else:
        self.dividir_bk(ref_bk, bucket)
        self.op_inserir(chave)
