class CPF:
    def __init__(self, cpf: str) -> None:
        self.cpf = self.__format(cpf)

    def validate(self) -> bool:
        cpf = self.cpf[:9]

        # calculates first digit and second digit
        cpf += self.__calc_cpf_validation_digit(cpf)
        cpf += self.__calc_cpf_validation_digit(cpf)

        return self.cpf == cpf

    def __format(self, cpf: str) -> str:
        return cpf.replace(".", "").replace("-", "")

    def __calc_cpf_validation_digit(self, cpf: str) -> str:
        tmp_result, multiply = 0, 2

        for digit in reversed(cpf):

            tmp_result += int(digit) * multiply

            multiply += 1

        tmp_result %= 11

        return str(11 - tmp_result) if tmp_result >= 2 else "0"

    def __str__(self) -> str:
        return self.cpf
