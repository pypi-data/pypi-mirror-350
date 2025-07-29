from moapy.auto_convert import auto_schema, MBaseModel
from moapy.designers_guide.func_execute import calc_content_27
from moapy.designers_guide.core_engine.execute_calc_general import DG_Result_Reports
from pydantic import Field, ConfigDict

class TestData(MBaseModel):
    dgnsitu: str = Field(description="Design situation", default="Persistent")
    strenghtclass: str = Field(description="Strength class", default="C30/37")
    sect_type: str = Field(description="Section type", default="Reinforced concrete section")
    v_ed: float = Field(description="Design shear force", default=350.0)
    n_ed: float = Field(description="Design axial force", default=1850.0)
    phi_sl: float = Field(description="Diameter of longitudinal tensile reinforcement", default=32.0)
    n_sl: int = Field(description="Number of longitudinal tensile reinforcement", default=4)
    b_w: float = Field(description="Width of the web", default=300.0)
    d: float = Field(description="Effective depth", default=450.0)
    a_c: float = Field(description="Cover to the longitudinal reinforcement", default=35.0)
    a_v: float = Field(description="Area of shear reinforcement", default=100.0)

@auto_schema(
    title="DGNDEV REVOLUTION",
    description="Eurocode 2 shear design for reinforced concrete beam",
    std_type="EUROCODE",
    design_code="EN1992-1-1:2004"
)
def ec2_shear_design(inp: TestData) -> DG_Result_Reports:
    return calc_content_27(inp.dgnsitu, inp.strenghtclass, inp.sect_type, inp.v_ed, inp.n_ed, inp.phi_sl, inp.n_sl, inp.b_w, inp.d, inp.a_c, inp.a_v)

if __name__ == "__main__":
    inp = {"inp":{"dgnsitu":"Persistent","strenghtclass":"C30/37","sectType":"Reinforced concrete section","vEd":350,"nEd":1850,"phiSl":32,"nSl":4,"bW":300,"d":450,"aC":35,"aV":100}}

    print(ec2_shear_design(**inp))
