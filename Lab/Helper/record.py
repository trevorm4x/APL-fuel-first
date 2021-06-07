from dataclasses import dataclass, asdict, field, fields

from uncertainties import ufloat

from Helper.numbers import print_unc

SI_unit_dict = {
    -2: 'c',
    -3: 'm',
    -6: '\u03BC',
    -9: 'n',
    0: ' ',
    3: 'k',
    6: 'M',
    9: 'G',
    12: 'T'
}

inv_SI_unit_dict = {k: i
                    for i, k in SI_unit_dict.items()}
inv_SI_unit_dict.update({'u':-6})


@dataclass(eq=False)
class Unit:
    scale: str = field()
    unit: str = field()

    def __post_init__(self):
        self.e = inv_SI_unit_dict[self.scale]

    def __repr__(self):
        return self.scale + self.unit

    def __eq__(self, other):
        if self.unit == other.unit:
            return True

    def __mul__(self, other):
        newscale = SI_unit_dict[self.e + other.e]
        newunit = self.unit + other.unit

        return Unit(newscale, '*'.join(newunit))


@dataclass(eq=False)
class Measurement:
    value: float=field()
    unc: float=field()
    unit: Unit=field()

    def __post_init__(self):
        self.ufloat=self.__ufloat__()
        self.interval=self.__interval__()

    def __ufloat__(self):
        return ufloat(
            self.value, self.unc) * \
            10**inv_SI_unit_dict[self.unit.scale]

    def __interval__(self):
        return [self.ufloat.n-self.ufloat.s,
                self.ufloat.n+self.ufloat.s]

    def __str__(self):
        val, unc, digs=print_unc(self.value, self.unc, False)
        return f'{val} +/- {unc} {self.unit}'

    def __eq__(self, other):
        if self.unit != other.unit:
            return False
        if self.interval[0] < other.interval[1] < self.interval[1]:
            return True
        if self.interval[0] < other.interval[0] < self.interval[1]:
            return True
        return False

    def __mul__(self, other):
        return Measurement(self.value * other.value,
                           (self.unc**2 + other.unc**2)**.5,
                           self.unit*other.unit)
