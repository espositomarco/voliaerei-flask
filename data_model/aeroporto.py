from __future__ import annotations

from data_model.citta import Citta
from data_model.custom_types import CodiceIATA
from data_model.volo import Volo


class Aeroporto:
    _nome: str
    _codice: CodiceIATA
    _citta: Citta
    _voli_in_partenza: set[Volo] #unknown at creation
    _voli_in_arrivo: set[Volo] #unknown at creation

    def __init__(self, codice: str | CodiceIATA, nome: str, citta: Citta) -> None:
        self._codice = codice if isinstance(codice, CodiceIATA) else CodiceIATA(codice)
        self.set_nome(nome)
        self._citta = citta
        self._citta._add_aeroporto(self)
        self._voli_in_partenza = set()
        self._voli_in_arrivo = set()
        import db.utils
        db.utils.store_aeroporto(self)

    def nome(self) -> str:
        return self._nome

    def set_nome(self, nome: str) -> None:
        self._nome = nome
        try:
            import db.utils
            db.utils.store_aeroporto(self)
        except AttributeError:
            pass

    def codice(self) -> CodiceIATA:
        return self._codice

    def citta(self) -> Citta:
        return self._citta

    def info(self) -> dict[str, str | CodiceIATA]:
        return dict(codice=self.codice(), nome=self.nome(), citta=self.citta().nome())

    def as_dict(self) -> dict[str, str | CodiceIATA | dict[str, str]]:
        return {
            "codice": self.codice(),
            "nome": self.nome(),
            "citta": {
                self.citta().nome(): f"/citta/{self.citta().nome()}"
            }
        }

    def voli_in_partenza(self) -> frozenset[Volo]:
        return frozenset(self._voli_in_partenza)

    def voli_in_arrivo(self) -> frozenset[Volo]:
        return frozenset(self._voli_in_arrivo)

    def _add_volo_in_partenza(self, v: Volo) -> None:
        self._voli_in_partenza.add(v)

    def _add_volo_in_arrivo(self, v: Volo) -> None:
        self._voli_in_arrivo.add(v)


    def get_voli_verso_aeroporto(self, altro: Aeroporto, durata_massima: int|None) -> list[dict]:
        durata_massima: int = durata_massima if durata_massima is not None else 10000000
        res: list[dict] = list()
        for volo in self.voli_in_partenza():
            if volo.arrivo() == altro and volo.durata() <= durata_massima:
                res.append(volo.info())
        return res

