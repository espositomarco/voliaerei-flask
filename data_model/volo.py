from __future__ import annotations
from typing import TYPE_CHECKING

from data_model.custom_types import CodiceVolo, IntGEZ

if TYPE_CHECKING:
    from data_model.aeroporto import Aeroporto
    from data_model.compagnia import Compagnia

class Volo:
    _codice: CodiceVolo #immutabile
    _durata: IntGEZ

    _partenza: Aeroporto # immutabile
    _arrivo: Aeroporto #immutabile
    _compagnia: Compagnia #immutabile

    def __init__(self,
                 codice: CodiceVolo | str,
                 durata: IntGEZ | int,
                 compagnia: Compagnia,
                 partenza: Aeroporto,
                 arrivo: Aeroporto) -> None:
        self._codice = codice if isinstance(codice, CodiceVolo) else CodiceVolo(codice)
        self.set_durata(durata)
        self._compagnia = compagnia
        self._compagnia._add_volo(self)
        self._partenza = partenza
        self._partenza._add_volo_in_partenza(self)
        self._arrivo = arrivo
        self._arrivo._add_volo_in_arrivo(self)

        import db.utils
        db.utils.store_volo(self)


    def codice(self) -> CodiceVolo:
        return self._codice

    def durata(self) -> IntGEZ:
        return self._durata

    def partenza(self) -> Aeroporto:
        return self._partenza

    def arrivo(self) -> Aeroporto:
        return self._arrivo

    def compagnia(self) -> Compagnia:
        return self._compagnia

    def set_durata(self, durata: IntGEZ | int) -> None:
        self._durata = durata if isinstance(durata, IntGEZ) else IntGEZ(durata)
        try:
            import db.utils
            db.utils.store_volo(self)
        except AttributeError:
            pass

    def info(self) -> dict[str, str]:
        return {
            "codice": self.codice(),
            "durata_minuti": self.durata(),
            "partenza": self.partenza().codice(),
            "arrivo": self.arrivo().codice(),
            "compagnia": self.compagnia().nome()
        }

    def as_dict(self) -> dict[str, str]:
        return {
            "codice": self.codice(),
            "durata_minuti": self.durata(),
            "partenza": {
                self.partenza().codice(): f"/aeroporti/{self.partenza().codice()}"
            },
            "arrivo": {
                self.arrivo().codice(): f"/aeroporti/{self.arrivo().codice()}"
            },
            "compagnia": {
                self.compagnia().nome(): f"/compagnie/{self.compagnia().nome()}"
            }
        }