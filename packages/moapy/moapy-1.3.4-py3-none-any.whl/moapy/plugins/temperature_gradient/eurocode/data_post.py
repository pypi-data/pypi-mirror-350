from typing import Optional, Sequence, Union
from pydantic import Field
from moapy.auto_convert import MBaseModel
from moapy.data_pre import (
    Point,
    Length,
    Stress,
    Temperature,
)
from moapy.enum_pre import enUnitLength


class ResultThermal(MBaseModel):
    """
    Result Thermal
    """

    y: list[Length] = Field(default_factory=list, description="Y")
    z: list[Length] = Field(default_factory=list, description="Z")
    temp: list[Temperature] = Field(default_factory=list, description="Temperature")
    stress: list[Stress] = Field(default_factory=list, description="Stress")


class ResultNonlinearTemperatureEffect(MBaseModel):
    """
    Result Nonlinear Temperature Effect
    """

    height: Length = Field(default_factory=Length, description="Height")
    outer: list[list[Point]] = Field(
        default_factory=list[Point], description="Outer polygon"
    )
    inner: list[list[Point]] = Field(
        default_factory=list[Point], description="Inner polygon"
    )
    heating: ResultThermal = Field(default_factory=ResultThermal, description="Heating")
    cooling: ResultThermal = Field(default_factory=ResultThermal, description="Cooling")
    temperature_heating: list[Point] = Field(
        default_factory=list[Point], description="Temperature Heating"
    )
    temperature_cooling: list[Point] = Field(
        default_factory=list[Point], description="Temperature Cooling"
    )


def create_points_from_coordinates(
    x_coords: Sequence[Union[float, int]],
    y_coords: Sequence[Union[float, int]],
    unit: enUnitLength = enUnitLength.MM,
) -> list[Point]:
    """
    x좌표와 y좌표 시퀀스를 받아서 Point 객체 리스트로 변환합니다.

    Args:
        x_coords: x좌표 값들의 시퀀스 (리스트, 튜플, numpy array 등)
        y_coords: y좌표 값들의 시퀀스 (리스트, 튜플, numpy array 등)
        unit: 길이 단위. 기본값은 MM

    Returns:
        List[Point]: Point 객체들의 리스트

    Raises:
        ValueError: x좌표와 y좌표의 개수가 다르거나, 유효하지 않은 입력값인 경우
        TypeError: 입력값의 타입이 올바르지 않은 경우

    Examples:
        >>> points = create_points_from_coordinates([1.0, 2.0], [3.0, 4.0])
        >>> points = create_points_from_coordinates(np.array([1, 2]), np.array([3, 4]))
    """
    # 입력값 검증
    if not (x_coords and y_coords):
        raise ValueError("좌표 리스트가 비어있습니다.")

    if len(x_coords) != len(y_coords):
        raise ValueError(
            f"x좌표({len(x_coords)})와 y좌표({len(y_coords)})의 개수가 일치해야 합니다."
        )

    try:
        # numpy array나 다른 시퀀스 타입을 float로 변환
        x_values = [float(x) for x in x_coords]
        y_values = [float(y) for y in y_coords]
    except (TypeError, ValueError) as e:
        raise TypeError(f"좌표값은 숫자로 변환 가능해야 합니다: {str(e)}")

    try:
        return [
            Point(x=Length(value=x, unit=unit), y=Length(value=y, unit=unit))
            for x, y in zip(x_values, y_values, strict=True)
        ]
    except Exception as e:
        raise ValueError(f"Point 객체 생성 중 오류 발생: {str(e)}") from e


def create_points_collection(
    points: list[Point], slab_points: Optional[list[Point]] = None
) -> list[list[Point]]:
    """
    외부 좌표와 선택적 슬래브 좌표로부터 포인트 컬렉션을 생성합니다.

    Args:
        outer: 외부 윤곽선의 x, y 좌표
        slab: 슬래브의 x, y 좌표 (선택사항)

    Returns:
        List[List[Point]]: 생성된 포인트 컬렉션 리스트
    """
    # 기본적으로 외부 윤곽선의 포인트는 항상 포함
    points_collection = [points]

    # 슬래브 좌표가 있는 경우 추가
    if slab_points is not None:
        points_collection.append(slab_points)

    return points_collection
