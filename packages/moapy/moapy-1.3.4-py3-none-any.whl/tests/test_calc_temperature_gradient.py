import json
from pathlib import Path
from typing import Any, Callable, TypeAlias, TypeVar, Union
from moapy.plugins.temperature_gradient.nonlinear_temperature_effect import (
    calc_eurocode,
)
from moapy.plugins.temperature_gradient.eurocode.data_input import (
    NonlinearTemperatureInput,
)
from moapy.plugins.temperature_gradient.eurocode.data_post import (
    ResultNonlinearTemperatureEffect,
)
from moapy.plugins.temperature_gradient.eurocode.data_pre import (
    CompositeBoxGirderSection,
    CompositeIGirderSection,
    CompositeTubSection,
    PSC1CellSection,
    PSC2CellSection,
    PSC_ISection,
    PSC_TSection,
    SteelBoxGirderSection,
    SteelIGirderSection,
)


BASE_SECTION_RESULT_DIR = "./tests/calc_temperature_gradient/data/"

T = TypeVar("T")
PathLike: TypeAlias = Union[str, Path]


def _ensure_absolute_path(file_path: PathLike) -> Path:
    """
    상대 경로를 절대 경로로 변환합니다.

    Args:
        file_path: 변환할 파일 경로

    Returns:
        Path: 절대 경로
    """
    path = Path(file_path)
    if not path.is_absolute():
        path = Path(BASE_SECTION_RESULT_DIR) / path
    return path


def read_file_with_processor(
    file_path: PathLike, processor: Callable[[Any], T], encoding: str = "utf-8"
) -> T:
    """
    파일을 읽고 지정된 프로세서로 처리합니다.

    Args:
        file_path: 파일 경로
        processor: 파일 내용을 처리할 함수
        encoding: 파일 인코딩 (기본값: utf-8)

    Returns:
        T: 처리된 결과
    """
    abs_path = _ensure_absolute_path(file_path)
    with open(abs_path, "r", encoding=encoding) as f:
        return processor(f)


def get_json_data(file_path: PathLike) -> dict:
    """JSON 파일을 읽어서 딕셔너리로 반환합니다."""
    return read_file_with_processor(file_path, json.load)


def get_result(file_path: PathLike) -> "ResultNonlinearTemperatureEffect":
    """파일을 읽어서 ResultNonlinearTemperatureEffect 모델로 변환합니다."""
    return read_file_with_processor(
        file_path,
        lambda f: ResultNonlinearTemperatureEffect.model_validate_json(f.read()),
    )


def test_calc_temperature_gradient_SteelBoxGirderSection():
    input_data = get_json_data("./input/steel_box_input.json")
    nonlinear_temperature_input = NonlinearTemperatureInput.model_validate(
        input_data["nonlinear_temperature_input"]
    )
    assert isinstance(
        nonlinear_temperature_input.section_input.section, SteelBoxGirderSection
    )

    res = calc_eurocode(nonlinear_temperature_input)
    expected = get_result("steel_box_example.json")
    assert res.heating == expected.heating
    assert res.temperature_heating == expected.temperature_heating
    assert res.cooling == expected.cooling
    assert res.temperature_cooling == expected.temperature_cooling
    assert res.inner == expected.inner
    assert res.outer == expected.outer


def test_calc_temperature_gradient_SteelIGirderSection():
    input_data = get_json_data("./input/steel_I_input.json")
    nonlinear_temperature_input = NonlinearTemperatureInput.model_validate(
        input_data["nonlinear_temperature_input"]
    )
    assert isinstance(
        nonlinear_temperature_input.section_input.section, SteelIGirderSection
    )

    res = calc_eurocode(nonlinear_temperature_input)
    expected = get_result("steel_I_example.json")

    assert res.heating == expected.heating
    assert res.temperature_heating == expected.temperature_heating
    assert res.cooling == expected.cooling
    assert res.temperature_cooling == expected.temperature_cooling
    assert res.inner == expected.inner
    assert res.outer == expected.outer


def test_calc_temperature_gradient_CompositeSteelBoxSection():
    input_data = get_json_data("./input/composite_steel_box_input.json")
    nonlinear_temperature_input = NonlinearTemperatureInput.model_validate(
        input_data["nonlinear_temperature_input"]
    )
    assert isinstance(
        nonlinear_temperature_input.section_input.section, CompositeBoxGirderSection
    )

    res = calc_eurocode(nonlinear_temperature_input)
    expected = get_result("composite_steel_box_example.json")

    assert res.heating == expected.heating
    assert res.temperature_heating == expected.temperature_heating
    assert res.cooling == expected.cooling
    assert res.temperature_cooling == expected.temperature_cooling
    assert res.inner == expected.inner
    assert res.outer == expected.outer


def test_calc_temperature_gradient_CompositeIGirderSection():
    input_data = get_json_data("./input/composite_steel_I_input.json")
    nonlinear_temperature_input = NonlinearTemperatureInput.model_validate(
        input_data["nonlinear_temperature_input"]
    )
    assert isinstance(
        nonlinear_temperature_input.section_input.section, CompositeIGirderSection
    )

    res = calc_eurocode(nonlinear_temperature_input)
    expected = get_result("composite_steel_I_example.json")

    assert res.heating == expected.heating
    assert res.temperature_heating == expected.temperature_heating
    assert res.cooling == expected.cooling
    assert res.temperature_cooling == expected.temperature_cooling
    assert res.inner == expected.inner
    assert res.outer == expected.outer


def test_calc_temperature_gradient_CompositeTubGirderSection():
    input_data = get_json_data("./input/composite_steel_tub_input.json")
    nonlinear_temperature_input = NonlinearTemperatureInput.model_validate(
        input_data["nonlinear_temperature_input"]
    )
    assert isinstance(
        nonlinear_temperature_input.section_input.section, CompositeTubSection
    )

    res = calc_eurocode(nonlinear_temperature_input)
    expected = get_result("composite_steel_tub_example.json")

    assert res.heating == expected.heating
    assert res.temperature_heating == expected.temperature_heating
    assert res.cooling == expected.cooling
    assert res.temperature_cooling == expected.temperature_cooling
    assert res.inner == expected.inner
    assert res.outer == expected.outer


def test_calc_temperature_gradient_PSC1CellSection():
    input_data = get_json_data("./input/psc_1_cell_input.json")
    nonlinear_temperature_input = NonlinearTemperatureInput.model_validate(
        input_data["nonlinear_temperature_input"]
    )
    assert isinstance(
        nonlinear_temperature_input.section_input.section, PSC1CellSection
    )

    res = calc_eurocode(nonlinear_temperature_input)
    expected = get_result("psc_1_cell_example.json")

    assert res.heating == expected.heating
    assert res.temperature_heating == expected.temperature_heating
    assert res.cooling == expected.cooling
    assert res.temperature_cooling == expected.temperature_cooling
    assert res.inner == expected.inner
    assert res.outer == expected.outer


def test_calc_temperature_gradient_PSC2CellSection():
    input_data = get_json_data("./input/psc_2_cell_input.json")
    nonlinear_temperature_input = NonlinearTemperatureInput.model_validate(
        input_data["nonlinear_temperature_input"]
    )
    assert isinstance(
        nonlinear_temperature_input.section_input.section, PSC2CellSection
    )

    res = calc_eurocode(nonlinear_temperature_input)
    expected = get_result("psc_2_cell_example.json")

    assert res.heating == expected.heating
    assert res.temperature_heating == expected.temperature_heating
    assert res.cooling == expected.cooling
    assert res.temperature_cooling == expected.temperature_cooling
    assert res.inner == expected.inner
    assert res.outer == expected.outer


def test_calc_temperature_gradient_PSC_ISection():
    input_data = get_json_data("./input/psc_I_input.json")
    nonlinear_temperature_input = NonlinearTemperatureInput.model_validate(
        input_data["nonlinear_temperature_input"]
    )
    assert isinstance(nonlinear_temperature_input.section_input.section, PSC_ISection)

    res = calc_eurocode(nonlinear_temperature_input)
    expected = get_result("psc_I_example.json")

    assert res.heating == expected.heating
    assert res.temperature_heating == expected.temperature_heating
    assert res.cooling == expected.cooling
    assert res.temperature_cooling == expected.temperature_cooling
    assert res.inner == expected.inner
    assert res.outer == expected.outer


def test_calc_temperature_gradient_PSC_TSection():
    input_data = get_json_data("./input/psc_T_input.json")
    nonlinear_temperature_input = NonlinearTemperatureInput.model_validate(
        input_data["nonlinear_temperature_input"]
    )
    assert isinstance(nonlinear_temperature_input.section_input.section, PSC_TSection)

    res = calc_eurocode(nonlinear_temperature_input)
    expected = get_result("psc_T_example.json")

    assert res.heating == expected.heating
    assert res.temperature_heating == expected.temperature_heating
    assert res.cooling == expected.cooling
    assert res.temperature_cooling == expected.temperature_cooling
    assert res.inner == expected.inner
    assert res.outer == expected.outer
