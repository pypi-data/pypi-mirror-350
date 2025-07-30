from agoracorp._cpf import CPF


def cpf(number: str) -> bool:
    return CPF(number).validate()
