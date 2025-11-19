from __future__ import annotations

# github.com/espositomarco/voliaerei-flask

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from data_model.citta import Citta


class Nazione:

    _nome: str
    _citta: set['Citta']

    def __init__(self, nome: str) -> None:
        self.set_nome(nome)
        self._citta = set()
        # TODO scrivi su db

    def nome(self) -> str:
        return self._nome

    def set_nome(self, nome: str) -> None:
        self._nome = nome
        # TODO scrivi su db

    def citta(self) -> frozenset['Citta']:
        return frozenset(self._citta)

    def _add_citta(self, citta: 'Citta') -> None:
        self._citta.add(citta)
        # TODO scrivi su db

    def _remove_citta(self, citta: 'Citta') -> None:
        self._citta.remove(citta)
        # TODO scrivi su db

    def __str__(self) -> str:
        return f"Nazione '{self._nome}'"

    def __repr__(self) -> str:
        return f"Nazione(nome='{self._nome}')"


    def info(self) -> dict[str, dict[str, str]]:
        return {self.nome():
            {
                'nome': self.nome(),
            }
        }



