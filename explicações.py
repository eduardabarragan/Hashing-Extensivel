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
