from typing import Self, Any
import re


class CodiceVolo(str):
    # Gli oggetti di questa classe *sono* stringhe
    #  che rispettano il formato dei codici dei voli: XY1234
    def __new__(cls, cv: str) -> Self:
        cv: str = cv.upper().strip()  # rendo la stringa maiuscola e senza spazi iniziali e finali
        if re.fullmatch(r'^[A-Z0-9]{2}\d{4}$', cv):
            return super().__new__(cls, cv)

        raise ValueError(f"La stringa '{cv}' non è un codice valido per un volo!")


class CodiceIATA(str):
    def __new__(cls, c: str) -> Self:
        if re.fullmatch(r'^[A-Z]{3}$', c):
            return super().__new__(cls, c)
        raise ValueError(f"La stringa '{c}' non è un codice IATA valido per un aeroporto!")






class IntGEZ(int):
    # Tipo di dato specializzato Intero >= 0 (Greater than or Equal to Zero)
    def __new__(cls, v: float | int | str | bool | Self) -> Self:
        n: int = super().__new__(cls, v)  # prova a convertire v in un int
        if n >= 0:
            return n
        raise ValueError(f"Il valore {n} è minore di 0!")

class IntGE1900(IntGEZ):
    # Tipo di dato specializzato Intero >= 1900
    def __new__(cls, v: float | int | str | bool | Self) -> Self:
        n: int = super().__new__(cls, v)  # prova a convertire v in un int
        if n >= 1900:
            return n
        raise ValueError(f"Il valore {n} è minore di 1900!")

class IntGZ(int):
    # Tipo di dato specializzato Intero > 0 (Greater than Zero)
    def __new__(cls, v: float | int | str | bool | Self) -> Self:
        n: int = super().__new__(cls, v)  # prova a convertire v in un int
        if n > 0:
            return n
        raise ValueError(f"Il valore {n} non è positivo!")




