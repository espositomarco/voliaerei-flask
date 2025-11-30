from __future__ import annotations

from data_model.citta import Citta
from data_model.custom_types import IntGE1900
from data_model.volo import Volo


class Compagnia:

    _nome: str # immutabile
    _fondazione: IntGE1900 # immutabile
    _citta: Citta # mutabile
    _voli: set[Volo]

    def __init__(self, nome: str,
                 citta: Citta,
                 fondazione: int | IntGE1900) -> None:
        self._nome = nome
        self._fondazione = fondazione if isinstance(fondazione, IntGE1900) else IntGE1900(fondazione)
        self.set_citta(citta)
        self._voli = set()
        import db.utils
        db.utils.store_compagnia(self)

    def nome(self) -> str:
        return self._nome

    def fondazione(self) -> IntGE1900:
        return self._fondazione

    def citta(self) -> Citta:
        return self._citta

    def set_citta(self, citta: Citta) -> None:
        self._citta = citta
        try:
            import db.utils
            db.utils.store_compagnia(self)
        except AttributeError:
            pass

    def info(self) -> dict[str, str | int]:
        return {
            "nome": self.nome(),
            "fondazione": self.fondazione(),
            "citta": self.citta().nome()
        }

    def as_dict(self) -> dict[str, str | int | dict[str, str]]:
        return {
            "nome": self.nome(),
            "fondazione": self.fondazione(),
            "citta": {
                self.citta().nome(): f"/citta/{self.citta().nome()}"
            }
        }

    def voli(self) -> frozenset[Volo]:
        return frozenset(self._voli)

    def _add_volo(self, volo: Volo) -> None:
        self._voli.add(volo)