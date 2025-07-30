from __future__ import annotations

from dataclasses import dataclass

_spread_divider = "^"
_datasource_divider_before = "("
_datasource_divider_after = ")"
_transformation_divider = "~"


def _get_id_from_factor(factor: str) -> str:
    output = strip_factor_name_from_transformation(factor).replace(
        _datasource_divider_before
        + get_dataset_from_factor_name(factor)
        + _datasource_divider_after,
        "",
    )
    if _spread_divider in output:
        lhs, rhs = output.split(_spread_divider)
        return f"{lhs}{_spread_divider}{_datasource_divider_before}{get_dataset_from_factor_name(factor)}{_datasource_divider_after}{rhs}"
    return output


@dataclass
class Factor:
    source: str
    id: str
    transformation: str

    @staticmethod
    def from_string(factor_name: str) -> Factor:
        return Factor(
            source=get_dataset_from_factor_name(factor_name),
            id=_get_id_from_factor(factor_name),
            transformation=get_transformation_from_factor_name(factor_name),
        )

    def __str__(self) -> str:
        return f"{_datasource_divider_before}{self.source}{_datasource_divider_after}{self.id}{ _transformation_divider + self.transformation if self.transformation != "" else ""}"

    def to_string(self) -> str:
        return str(self)

    @property
    def only_source_and_id(self) -> str:
        return f"{_datasource_divider_before}{self.source}{_datasource_divider_after}{self.id}"

    @property
    def clean_id(
        self,
    ) -> str:  # in case a factor is a spread, remove the dataset from the id
        return self.id.replace(
            _datasource_divider_before + self.source + _datasource_divider_after, ""
        )


def strip_factor_name_from_transformation(factor_name: str) -> str:
    return factor_name.split(_transformation_divider)[0]


def get_dataset_from_factor_name(factor_name: str) -> str:
    return factor_name.split(_datasource_divider_after)[0].replace(
        _datasource_divider_before, ""
    )


def get_transformation_from_factor_name(factor_name: str) -> str:
    return "_".join(factor_name.split(_transformation_divider)[1:])


def ensemble_has_transformations_specified(factor_name: str) -> bool:
    return _transformation_divider + "ensemble(" in factor_name


def construct_ensemble_name(factor_name: str, made_of: list[str]) -> str:
    return "ensemble" + (
        "("
        + ";".join(
            [
                s.replace(
                    strip_factor_name_from_transformation(factor_name)
                    + _transformation_divider,
                    "",
                )
                for s in made_of
            ]
        )
        + ")"
    )


def get_transformations_from_ensemble_name(factor_name: str) -> list[str]:
    if ensemble_has_transformations_specified(factor_name):
        f = strip_factor_name_from_transformation(factor_name)
        t = (
            factor_name.split(_transformation_divider + "ensemble(")[1]
            .replace(")", "")
            .split(";")
        )
        return [f"{f}~{t}" for t in t]
    if (
        _transformation_divider in factor_name
        and _transformation_divider + "ensemble" not in factor_name
    ):
        return [factor_name]
    return []


def get_transformation_param(factor: str) -> tuple[str, str]:
    if _transformation_divider in str(factor):
        transformations = str(factor).split(_transformation_divider)
        transformations[0]
        transformation = (
            transformations[2] if len(transformations) > 2 else transformations[1]
        )
        stationary_method = transformations[1] if len(transformations) > 2 else ""

        if "ensemble" in transformation:
            return "ensemble", "factor"
        if "_" in transformation:
            extractor_splitted = transformation.split("_")
            return (
                "_".join(extractor_splitted[1:]),
                extractor_splitted[0]
                if stationary_method == ""
                else f"{stationary_method}_{extractor_splitted[0]}",
            )

        return transformation, "factor"
    return "original", "factor"
