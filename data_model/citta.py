from __future__ import annotations

from typing import TYPE_CHECKING


from data_model.custom_types import IntGEZ

if TYPE_CHECKING:
    from data_model.nazione import Nazione
    from data_model.aeroporto import Aeroporto

class Citta:
    _nome: str # immutabile
    _abitanti: IntGEZ
    _nazione: 'Nazione'
    _aeroporti: set[Aeroporto]

    def __init__(self, nome: str,
                 abitanti: int | IntGEZ,
                 nazione: 'Nazione'):

        # self.set_nome(nome) reso immutabile
        self._nome = nome
        self.set_abitanti(abitanti)
        self.set_nazione(nazione)
        self._aeroporti = set()

        import db.utils
        db.utils.store_citta(self)


    def nome(self) -> str:
        return self._nome

    def abitanti(self) -> IntGEZ:
        return self._abitanti

    '''def set_nome(self, nome: str) -> None:
        self._nome = nome
        # TODO scrivi su db'''

    def set_abitanti(self, abitanti: int | IntGEZ) -> None:
        ab: IntGEZ = abitanti if isinstance(abitanti, IntGEZ) else IntGEZ(abitanti)
        self._abitanti = ab
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

    def aeroporti(self) -> frozenset[Aeroporto]:
        return frozenset(self._aeroporti)

    def _add_aeroporto(self, aeroporto: Aeroporto) -> None:
        self._aeroporti.add(aeroporto)



    def __repr__(self) -> str:
        return f"Citta(nome='{self.nome()}', abitanti={self.abitanti()}, nazione={self.nazione()})"

    def info(self) -> dict[str, str | int]:
        return {
            'nome': self.nome(),
            'n_abitanti': self.abitanti(),
            'nazione': self.nazione().nome()
        }

    def as_dict(self) -> dict[str, str | int | dict[str, str]]:
        return {
                'nome': self.nome(),
                'n_abitanti': self.abitanti(),
                'nazione': {
                    self.nazione().nome(): f"/nazioni/{self.nazione().nome()}"
                },

            }

    ''',
                    'aeroporti': {
                        a.codice(): f"/aeroporti/{a.codice()}" for a in self.aeroporti()
                    }'''


