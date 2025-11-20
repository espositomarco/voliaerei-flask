from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from data_model.nazione import Nazione

class Citta:
    _nome: str # immutabile
    _abitanti: int
    _nazione: 'Nazione'

    def __init__(self, nome: str,
                 abitanti: int,
                 nazione: 'Nazione'):

        # self.set_nome(nome) reso immutabile
        self._nome = nome
        self.set_abitanti(abitanti)
        self.set_nazione(nazione)

        import db.utils
        db.utils.store_citta(self)


    def nome(self) -> str:
        return self._nome

    def abitanti(self) -> int:
        return self._abitanti

    '''def set_nome(self, nome: str) -> None:
        self._nome = nome
        # TODO scrivi su db'''

    def set_abitanti(self, abitanti: int) -> None:
        self._abitanti = abitanti
        try:
            import db.utils
            db.utils.store_citta(self)
        except AttributeError:
            pass

    def nazione(self) -> 'Nazione':
        return self._nazione

    def set_nazione(self, nazione: 'Nazione') -> None:
        try:
            self.nazione()._remove_citta(self)
        except AttributeError:
            pass
        self._nazione = nazione
        nazione._add_citta(self)
        try:
            import db.utils
            db.utils.store_citta(self)
        except AttributeError:
            pass



    def __repr__(self) -> str:
        return f"Citta(nome='{self.nome()}', abitanti={self.abitanti()}, nazione={self.nazione()})"

    def info(self) -> dict[str, str]:
        return {
                'nome': self.nome(),
                'n_abitanti': self.abitanti(),
                'nazione': self.nazione().nome()
            }


