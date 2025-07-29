from dataclasses import dataclass, field

@dataclass
class ReportForm:
    id: str = ''  # NOTE: Do not print to JSON
    is_used = False # NOTE : Do not print to json. just for the calculate logic
    is_user_input = False
    code_name: str = ''
    reference: str = ''
    title: str = ''
    description: str = ''
    figure_path: str = ''
    descript_table: list = field(default_factory=list)
    comp_type: str = ''
    symbol: str = ''
    formula: list = field(default_factory=list)
    result_value: float = 0.0
    result_table: list = field(default_factory=list)
    result_variable: dict = field(default_factory=dict)
    use_std: bool = False # DEPRECATED 예정
    ref_std: str = ''
    unit: str = ''
    notation: str = 'standard'
    decimal: int = 0  # Default integer value
    limits: dict = field(default_factory=dict)
    
    def to_dict(self):
        return {
            'isInput': self.is_user_input,
            'codeName': self.code_name,
            'reference': self.reference if isinstance(self.reference, list) else [self.reference],
            'title': self.title,
            'description': self.description,
            'figurePath': self.figure_path,
            'descriptTable': self.descript_table,
            'compType': self.comp_type,
            'symbol': self.symbol,
            'result': {
                "value": str(self.result_value),
                "table": self.result_table if isinstance(self.result_table, list) else [self.result_table],
                "formula": self.formula[0] if isinstance(self.formula, list) and self.formula else self.formula,
                "variables": self.result_variable if isinstance(self.result_variable, dict) else {self.result_variable},
            },
            'refStd': self.ref_std,
            'unit': self.unit,
            'notation': self.notation,
            'decimal': self.decimal,
            # 'limits': self.limits if isinstance(self.limits, dict) else [self.limits],
        }
    
    def __repr__(self) -> str:
        full_formula = ""
        full_formula += f"{self.symbol}"
        for curr_formula in self.formula if self.formula else []:
            full_formula += " = " + f"{curr_formula}"
        full_formula += " = " + f"{self.result}" + f" {self.unit}"
                
        return (
            f"[{self.code_name} {self.reference}] "
            f"{self.title}\n"
            f"{self.description}\n"
            f"{full_formula}"
        )