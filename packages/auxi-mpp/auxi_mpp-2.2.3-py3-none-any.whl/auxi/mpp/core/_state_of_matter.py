from enum import IntEnum


# TODO: move to auxi-core
class StateOfMatter(IntEnum):
    unknown = 0
    solid = 1
    liquid = 2
    solid_liquid = solid | liquid
    gas = 4
    solid_gas = solid | gas
    solid_liquid_gas = solid | liquid | gas
    plasma = 8
    solid_plasma = solid | plasma
    solid_liquid_plasma = solid | liquid | plasma
    solid_liquid_gas_plasma = solid | liquid | gas | plasma
    liquid_plasma = liquid | plasma
    liquid_gas_plasma = liquid | gas | plasma
    gas_plasma = gas | plasma
