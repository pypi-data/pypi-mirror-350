import math
from collections.abc import Callable
from typing import Any, ClassVar

from pydantic import Field
from scipy.optimize._shgo import shgo  # type: ignore

from auxi.chemistry.validation import strCompoundFormula
from auxi.core.physicalconstants import R
from auxi.core.validation import floatFraction, floatPositiveOrZero, strNotEmpty

from ..state import SilicateSlagEquilibriumTpxState
from ._model import Model


class GrundyKimBroschMulti(Model[floatPositiveOrZero, floatPositiveOrZero, dict[str, floatFraction]]):
    """
    Ternary silicate slag dynamic viscosity model by Grundy, Kim, and Brosch.

    Args:
    ----
        bff : Bond fraction function with temperature, pressure and composition as input and returns dictionary of bond fractions.

    Raises:
    ------
        ValueError: If SiO2 is not specified.
        ValueError: If the compound formula is not found in the model's .yaml data file.

    Returns:
    -------
       Dynamic viscosity in [Pa.s].

    References:
    ----------
        grundy2008-part1, grundy2008-part2, kim2012-part3
    """

    data: ClassVar[dict[str, dict[str, Any]]] = {}

    references: ClassVar[list[strNotEmpty]] = ["grundy2008-part1", "grundy2008-part2"]

    bff: Callable[[float, float, dict[str, float]], dict[str, float]]
    cation: dict[str, str] = Field(default_factory=dict)
    struc_unit: dict[str, str] = Field(default_factory=dict)
    struc_ox_count: dict[str, float] = Field(default_factory=dict)
    cation_count: dict[str, int] = Field(default_factory=dict)
    parameters: dict[str, dict[str, float]] = Field(default_factory=dict)
    names: dict[str, str] = Field(default_factory=dict)
    equilibrium_stoic: dict[str, int] = Field(default_factory=dict)
    molar_mass: dict[str, float] = Field(default_factory=dict)
    structural_x: dict[str, float] = Field(default_factory=dict)
    compound_scope: list[strCompoundFormula] = Field(default_factory=list)

    def model_post_init(self, __context: Any) -> None:
        super().model_post_init(__context)

        data = GrundyKimBroschMulti.data
        self.compound_scope = ["SiO2", "Al2O3", "MgO", "CaO"]

        self.cation: dict[str, str] = {c: data[c]["cation"] for c in self.compound_scope}
        self.cation_count: dict[str, int] = {c: data[c]["cation_count"] for c in self.compound_scope}
        self.struc_unit: dict[str, str] = {c: data[c]["struc_unit"] for c in self.compound_scope}
        self.struc_ox_count: dict[str, float] = {c: data[c]["struc_ox_count"] for c in self.compound_scope}
        self.parameters: dict[str, dict[str, float]] = {c: data[c]["parameters"] for c in self.compound_scope}
        self.names: dict[str, str] = {data[c]["struc_unit"]: c for c in self.compound_scope}
        self.equilibrium_stoic: dict[str, int] = {c: data[c]["stoic"] for c in data}
        self.molar_mass: dict[str, float] = {c: data[c]["molar_mass"] for c in data}

    def calculate(
        self, T: floatPositiveOrZero = 298.15, p: floatPositiveOrZero = 101325, x: dict[str, floatFraction] = {}
    ) -> float:
        # validate input
        state = SilicateSlagEquilibriumTpxState(T=T, p=p, x=x)
        for c in state.x:
            if c not in self.compound_scope:
                raise ValueError(f"{c} is not a valid formula. Valid options are '{' '.join(self.compound_scope)}'.")

        # convert input composition to structural unit fractions
        x_struc_unit = self._structural_fractions(state)

        # table 1 of grundy2008-part2
        delta_G = self._delta_G(x_struc_unit)

        # eqn 18 in grundy2008-part2
        eq_constant_K = self._constant_K(state.T, delta_G)

        # eqn 9 - 11 in grundy2008-part2
        eq_x_struc_unit = self._equilib_compositions(eq_constant_K, x_struc_unit)

        # eqn 2 to 3 in grundy2008-part1
        p_SiSi = self._probability_SiSi(state, eq_x_struc_unit)

        # eqn 4 in grundy2008-part2
        A_parameter = self._calculate_A_parameter(eq_x_struc_unit, p_SiSi, state)

        # eqn 5 in grundy2008-part2
        E_parameter = self._calculate_E_parameter(eq_x_struc_unit, p_SiSi, state)

        # eqn 10 in grundy2008-part1
        mu = math.exp(float(A_parameter + E_parameter / (R * state.T)))

        self.structural_x = eq_x_struc_unit

        return mu

    def _structural_fractions(self, state: SilicateSlagEquilibriumTpxState) -> dict[str, float]:
        x_struc_unit: dict[str, float] = {}
        for comp in state.x:
            x_struc_unit[self.struc_unit[comp]] = self.cation_count[comp] * state.x[comp]

        x_struc_unit = self._normalise_fractions(x_struc_unit)

        return x_struc_unit

    def _full_fractions(self, struc_fracs: dict[str, float]) -> dict[str, float]:
        x_full_unit: dict[str, float] = {}
        for comp, value in struc_fracs.items():
            x_full_unit[self.names[comp]] = value / self.cation_count[self.names[comp]]

        x_full_unit = self._normalise_fractions(x_full_unit)

        return x_full_unit

    def _normalise_fractions(self, dict_in: dict[str, float]) -> dict[str, float]:
        x_sum: float = sum(dict_in[comp] for comp in dict_in)
        normalised_dict: dict[str, float] = {}
        for key, value in dict_in.items():
            normalised_dict[key] = value / x_sum
        return normalised_dict

    def _count_oxygens(self, x_comps: dict[str, float]):
        n_tot_oxygen: float = 0.0
        for key, value in x_comps.items():
            n_tot_oxygen += self.struc_ox_count[self.names[key]] * value
        return n_tot_oxygen

    # eqn 2 to 3 grundy2008-part1
    def _probability_SiSi(self, state: SilicateSlagEquilibriumTpxState, x_comps: dict[str, float]) -> float:
        adjusted_comp = self._full_fractions(x_comps)
        x_b = self.bff(state.T, state.p, adjusted_comp)
        p_SiSi: float = (x_b["Si-Si"] * self._count_oxygens(x_comps)) / (2 * x_comps["SiO2"])
        return p_SiSi

    def _calculate_A_parameter(
        self, x_comp: dict[str, float], p_SiSi: float, state: SilicateSlagEquilibriumTpxState
    ) -> float:
        MOx = state.compounds.copy()
        MOx.remove("SiO2")
        for c in range(len(MOx)):
            MOx[c] = self.struc_unit[MOx[c]]

        # eqn 4 in grundy2008-part2
        A_SiO2_star = self.parameters["SiO2"]["A_*"]
        A_SiO2_E = self.parameters["SiO2"]["A_E"]

        # term 1
        sum_A_X = sum([self.parameters[self.names[comp]]["A"] * x_comp[comp] for comp in MOx])

        # term 4
        sum_A_MSi_X = sum([self.parameters[self.names[comp]]["A_M_Si"] * x_comp[comp] for comp in MOx])

        # term 5
        sum_XM = sum([x_comp[comp] for comp in MOx])
        sum_A_R_XX = sum([self.parameters[self.names[comp]]["A_M_Si_R"] * x_comp[comp] / sum_XM for comp in MOx])

        A_param = sum_A_X + x_comp["SiO2"] * (
            A_SiO2_star + A_SiO2_E * p_SiSi**40 + sum_A_MSi_X + sum_A_R_XX * (p_SiSi**4 - p_SiSi**40)
        )
        return A_param

    def _calculate_E_parameter(
        self, x_comp: dict[str, float], p_SiSi: float, state: SilicateSlagEquilibriumTpxState
    ) -> float:
        MOx = state.compounds.copy()
        MOx.remove("SiO2")
        for c in range(len(MOx)):
            MOx[c] = self.struc_unit[MOx[c]]

        # eqn 5 in grundy2008-part2
        E_SiO2_star = self.parameters["SiO2"]["E_*"]
        E_SiO2_E = self.parameters["SiO2"]["E_E"]

        # term 1
        sum_E_X = sum([self.parameters[self.names[comp]]["E"] * x_comp[comp] for comp in MOx])

        # term 4
        sum_E_MSi_X = sum([self.parameters[self.names[comp]]["E_M_Si"] * x_comp[comp] for comp in MOx])

        # term 5
        sum_XM = sum([x_comp[comp] for comp in MOx])
        sum_E_R_XX = sum([self.parameters[self.names[comp]]["E_M_Si_R"] * x_comp[comp] / sum_XM for comp in MOx])

        E_param = sum_E_X + x_comp["SiO2"] * (
            E_SiO2_star + E_SiO2_E * p_SiSi**40 + sum_E_MSi_X + sum_E_R_XX * (p_SiSi**4 - p_SiSi**40)
        )
        return E_param

    def _delta_G(self, x_comp: dict[str, float]) -> dict[str, float]:
        x_SiO2 = x_comp["SiO2"]

        # check type of associate species
        system_type = self._system_type(x_comp)

        # calculate delta G
        delta_G = self._calc_delta_G(system_type, x_SiO2)
        return delta_G

        # eqn 18 in grundy2008-part2

    def _constant_K(self, temp: float, delta_G: dict[str, float]) -> dict[str, float]:
        const_K: dict[str, float] = {}
        for dG, value in delta_G.items():
            const_K[dG] = math.exp(value / (-1 * R * temp))
        return const_K

        # eqn 9 - 11 in grundy2008-part2

    def _equilib_compositions(self, const_K: dict[str, float], x_comp: dict[str, float]):
        if "AlO15" in x_comp:
            # new_comp = self._solve_associate(const_K, x_comp)
            parameters, system_lists = self._prepare_params_for_optimisation(x_comp)

            solution_x, solution_y = self._find_solutions(parameters, system_lists, const_K, x_comp)

            new_comp = self._calc_x_star(parameters, system_lists, solution_x, solution_y, x_comp)

            return new_comp
        else:
            return x_comp

    def _prepare_params_for_optimisation(self, x_comp: dict[str, float]):
        # list of non-SiO2 species that can react to form associate species
        non_sio2 = ["AlO15", "CaO", "MgO"]
        associate_formers = ["CaO", "MgO"]

        # associates that can form from comps in list non_sio2
        associates = ["CaAl2O4", "MgAl2O4"]

        # add missing components to x_comp but with amount as 0.0
        missing_comps: list[str] = []
        for comp in associate_formers:
            if comp not in x_comp:
                x_comp[comp] = 0.0
                missing_comps.append(comp)
            else:
                continue

        # get stoiciometric coefficients
        a = self.equilibrium_stoic[associates[0]]  # CaAl2O4
        b = self.equilibrium_stoic[associates[1]]  # MgAl2O4

        c = self.equilibrium_stoic[self.names[non_sio2[0]]]  # AlO15
        d = self.equilibrium_stoic[self.names[non_sio2[1]]]  # CaO
        e = self.equilibrium_stoic[self.names[non_sio2[2]]]  # MgO

        # divide a, b, c by greatest common divisor. Note, order is important
        a, b, c, d, e = self._gcd_a_b_c([a, b, c, d, e])

        # get input amounts of the two non-SiO2 compounds
        C = x_comp[non_sio2[0]]  # AlO15
        D = x_comp[non_sio2[1]]  # CaO
        E = x_comp[non_sio2[2]]  # MgO

        params = (a, b, c, d, e, C, D, E)
        lists = (non_sio2, associate_formers, missing_comps, associates)

        return params, lists

    def _find_solutions(
        self,
        params: tuple[float, float, float, float, float, float, float, float],
        lists: tuple[list[Any], list[Any], list[Any], list[Any]],
        const_K: dict[str, float],
        x_comp: dict[str, float],
    ):
        a, b, c, d, e, C, D, E = params
        _, associate_formers, missing_comps, associates = lists

        # build equation to solve
        def equation_shgo(x_: Any, *args: Any):
            a, b, c, d, e, C, D, E, x_SiO2, const_K = args

            const_K_1 = const_K[associates[0]]  # CaAl2O4
            const_K_2 = const_K[associates[1]]  # MgAl2O4

            # x_[0] is x that needs to be solved
            N_tot = a * x_[0] + b * x_[1] + (C - c * x_[0] - c * x_[1]) + (D - d * x_[0]) + (E - e * x_[1]) + x_SiO2

            # CaAl2O4 -- a, c, d, const_K_1
            r1 = ((a * x_[0]) / N_tot) ** a - const_K_1 * (
                ((C - c * x_[0] - c * x_[1]) / N_tot) ** c * ((D - d * x_[0]) / N_tot) ** d
            )

            # MgAl2O4 -- b, c, e, const_K_2
            r2 = ((b * x_[1]) / N_tot) ** b - const_K_2 * (
                ((C - c * x_[0] - c * x_[1]) / N_tot) ** c * ((E - e * x_[1]) / N_tot) ** e
            )

            # take square to avoid negatives
            return r1**2 + r2**2

        # solve x

        # number of equilibrium reactions that have Al2O3 as reactant
        num_eq_rxns = len(associate_formers) - len(missing_comps)

        # set upper bounds to input fraction divided by its stoiciometric coefficient
        bounds_x = (0, min(C / (num_eq_rxns * c), D / d))
        bounds_y = (0, min(C / (num_eq_rxns * c), E / e))
        bounds = bounds_x, bounds_y

        # args contains all information to solve equation_shgo. This is given to shgo solver
        args = (a, b, c, d, e, C, D, E, x_comp["SiO2"], const_K)

        # find the root of the equation
        solutions: Any = shgo(
            func=equation_shgo,
            bounds=bounds,
            args=args,
        )

        # # solution to equation_shgo
        solution_x: float = solutions.x[0]
        solution_y: float = solutions.x[1]

        return solution_x, solution_y

    def _calc_x_star(
        self,
        params: tuple[float, float, float, float, float, float, float, float],
        lists: tuple[list[Any], list[Any], list[Any], list[Any]],
        solution_x: float,
        solution_y: float,
        x_comp: dict[str, float],
    ):
        a, b, c, d, e, _, _, _ = params
        non_sio2, _, missing_comps, associates = lists

        # get prime fractions
        X_prime: dict[str, float] = {}

        # derived from eqn 11 - 12 in kim2012-part3
        N_tot = (
            x_comp["SiO2"]  # SiO2
            + a * solution_x  # CaAl2O4
            + b * solution_y  # MgAl2O4
            + x_comp[non_sio2[0]]
            - c * solution_x
            - c * solution_y  # AlO15
            + x_comp[non_sio2[1]]
            - d * solution_x  # CaO
            + x_comp[non_sio2[2]]
            - e * solution_y  # MgO
        )

        X_prime["SiO2"] = x_comp["SiO2"] / N_tot  # SiO2

        X_prime[associates[0]] = (a * solution_x) / N_tot  # CaAl2O4
        X_prime[associates[1]] = (b * solution_y) / N_tot  # MgAl2O4

        X_prime[non_sio2[0]] = (x_comp[non_sio2[0]] - c * solution_x - c * solution_y) / N_tot  # AlO15
        X_prime[non_sio2[1]] = (x_comp[non_sio2[1]] - d * solution_x) / N_tot  # CaO
        X_prime[non_sio2[2]] = (x_comp[non_sio2[2]] - e * solution_y) / N_tot  # MgO

        # eqn 13 in kim2012-part3
        # get number of Al's the associate species constributes
        num_Al_1 = self.equilibrium_stoic[self.names["AlO15"]] / self.equilibrium_stoic[associates[0]]  # CaAl2O4
        num_Al_2 = self.equilibrium_stoic[self.names["AlO15"]] / self.equilibrium_stoic[associates[1]]  # MgAl2O4

        N_tot_star = (
            X_prime["SiO2"]  # SiO2
            + num_Al_1 * X_prime[associates[0]]  # CaAl2O4
            + num_Al_2 * X_prime[associates[1]]  # MgAl2O4
            + X_prime[non_sio2[0]]  # AlO15
            + X_prime[non_sio2[1]]  # CaO
            + X_prime[non_sio2[2]]  # MgO
        )

        # calculate adjusted composition
        X_star: dict[str, float] = {}
        X_star["SiO2"] = (
            X_prime["SiO2"] + num_Al_1 * X_prime[associates[0]] + num_Al_2 * X_prime[associates[1]]
        ) / N_tot_star  # SiO2
        X_star[non_sio2[0]] = (X_prime[non_sio2[0]]) / N_tot_star  # AlO15
        X_star[non_sio2[1]] = (X_prime[non_sio2[1]]) / N_tot_star  # CaO
        X_star[non_sio2[2]] = (X_prime[non_sio2[2]]) / N_tot_star  # MgO

        for comp in missing_comps:
            del X_star[comp]

        return X_star

    def _remove_SiO2(self, comps: list[str]):
        non_sio2_comps: list[str] = []
        for x in comps:
            if x == "SiO2":
                pass
            else:
                non_sio2_comps.append(x)
        return non_sio2_comps

    def _gcd_a_b_c(self, list_coeffs: list[int]):
        options: list[int] = []

        for coeff1 in list_coeffs:
            for coeff2 in list_coeffs:
                options.extend([math.gcd(coeff1, coeff2)])

        gcd: int = min(options)

        a_new = list_coeffs[0] / gcd
        b_new = list_coeffs[1] / gcd
        c_new = list_coeffs[2] / gcd
        d_new = list_coeffs[3] / gcd
        e_new = list_coeffs[4] / gcd

        return a_new, b_new, c_new, d_new, e_new

    def _system_type(self, x_comp: dict[str, float]):
        comps = list(x_comp.keys())
        non_sio2_comps = self._remove_SiO2(comps)

        if "AlO15" in non_sio2_comps:
            return "Contains Al2O3"

        else:
            return "No Al2O3 present"

    def _calc_delta_G(
        self, system_type: str, x_SiO2: float
    ) -> dict[str, float]:  # TODO: implement for both associate species
        if system_type == "Contains Al2O3":
            delta_G_CaAl2O4: float = 5000 - 100000 * x_SiO2
            delta_G_MgAl2O4: float = 13000 - 105000 * x_SiO2
            return {"CaAl2O4": delta_G_CaAl2O4, "MgAl2O4": delta_G_MgAl2O4}

        else:
            return {"": 0.0}


GrundyKimBroschMulti.load_data()
