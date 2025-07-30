# pylint: disable=C0114
from ..function_focus import ValueProducer
from csvpath.matching.productions import Term, Variable, Header, Reference
from ..function import Function
from ..args import Args


class Upper(ValueProducer):
    """uppercases a string"""

    def check_valid(self) -> None:
        self.args = Args(matchable=self)
        a = self.args.argset(1)
        a.arg(types=[Term, Variable, Header, Function, Reference], actuals=[str])
        self.args.validate(self.siblings())
        super().check_valid()

    def _produce_value(self, skip=None) -> None:
        value = self.children[0].to_value(skip=skip)
        self.value = f"{value}".upper()

    def _decide_match(self, skip=None) -> None:
        v = self.to_value(skip=skip)
        self.match = v is not None
