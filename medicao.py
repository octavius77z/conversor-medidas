from decimal import Decimal

FATOR_POL_PARA_MM = 25.4

def converter(valor, unidade_origem, unidade_destino):
    """mm e pol (dec)"""
    if unidade_origem == unidade_destino:
        return valor
    if unidade_origem == "mm" and unidade_destino == "pol":    
        return valor / FATOR_POL_PARA_MM
    if unidade_origem == "pol" and unidade_destino == "mm":
        return valor * FATOR_POL_PARA_MM
    raise ValueError(
        f"Conversão não suportada: {unidade_origem} -> {unidade_destino}"
    )

def verificar_medida(medida_nominal, tolerancia, medida_real, unidade):

    limite_inferior = medida_nominal - tolerancia
    limite_superior = medida_nominal + tolerancia

    aprovada = limite_inferior <= medida_real <= limite_superior

    if medida_real < limite_inferior:
        diferenca = medida_real - limite_inferior
        status = "REPROVADA (abaixo do limite inferior)"
    elif medida_real > limite_superior:
        diferenca = medida_real - limite_superior
        status = "REPROVADA (acima do limite superior)"  
    else:
        diferenca = 0.0
        status = "APROVADA"
    return {
        "status": status,
        "aprovada": aprovada,
        "limite_inferior": limite_inferior,
        "limite_superior": limite_superior,
        "diferenca": diferenca,
        "unidade": unidade,
    }            

def ler_numero(mensagem):

    while True:
        entrada = input(mensagem).strip().replace(",",",")
        try:
            return float(entrada)
        except ValueError:
            print("!!VALOR INVÁLIDO!! Digite um número válido (ex: 25.4).")

def ler_unidade(mensagem):

    while True:
        entrada = input(mensagem).strip().lower()
        if entrada in ("mm", "milimetro", "milímetro"):
            return "mm"
        if entrada in ("pol", "polegada", "in", '"'):
            return "pol"
        print("!!UNIDADE INVÁLIDA!! Digite 'mm' ou 'pol'.")

def formatar_numero(valor):

    return f"{Decimal(str(valor)).normalize():f}"

def main():
    print("=" * 50)
    print(" VERIFICADOR DE MEDIDAS COM TOLERÂNCIA")
    print("=" * 50)

    unidade = ler_unidade("Unidade da medida (mm/pol): ")

    medida_nominal = ler_numero(f"Medida nominal ({unidade}): ")
    tolerancia = ler_numero(f"Tolerância ± ({unidade}): ")
    medida_real = ler_numero(f"Medida real ({unidade}): ")

    resultado = verificar_medida(
        medida_nominal, tolerancia, medida_real, unidade
    )

    print("\n" + "-" * 50)
    print(f"    Nominal:    {formatar_numero(medida_nominal)} {unidade}")
    print(f"    Tolerância: ± {formatar_numero(tolerancia)} {unidade}")
    print(f"  Limite Infer.: {formatar_numero(resultado['limite_inferior'])} {unidade}")
    print(f"  Limite Super.: {formatar_numero(resultado['limite_superior'])} {unidade}")
    print(f"  Medida real:   {formatar_numero(medida_real)} {unidade}")
    print("-" * 50)

    if resultado["aprovada"]:
        print("PEÇA APROVADA")
    else:
        print("PEÇA REPROVADA")
        print(f"    Diferença: {formatar_numero(resultado['diferenca'])} {unidade}")
    
    print("-" * 50)
if __name__ == "__main__":
    main()    