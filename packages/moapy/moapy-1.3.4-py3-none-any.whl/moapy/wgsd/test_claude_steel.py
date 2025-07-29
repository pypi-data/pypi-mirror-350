import anthropic

# Claude API 키 설정
client = anthropic.Anthropic(api_key="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")

# 사용자 질문 정의
user_input = """

구조공학 전문가로서 설계 기준과 설계 절차 흐름에 대한 상세 정보를 제공하게 됩니다.

먼저, AISC360-2022의 Steel Beam을 설계 하기 위한 검토항목에 대해 작성합니다.(검토항목은 아래 예시 중 분석 가능한 최대 항목을 포함합니다. : 휨검토, 전단검토, 토션검토, 좌굴 검토, 응력검토, 세장비 검토, 피로검토, 스티프너 검토...)

검토 항목과 관련된 수식에 대해서도 작성합니다.

관련된 수식이 다른 수식을 포함하는 경우 관련된 수식을 모두 포함하여 작성합니다.

1. 설계 흐름도 섹션:
<flow> 태그 안에 설계 절차 노드들을 번호 순서대로 작성하며, 각 노드는 다음 내용 포함:
- 노드 번호
- 노드 명칭
- 해당 노드의 적용된 수식
- 노드 분기점이 있는 경우 분기점 표시

아래를 참고하여 응답결과를 작성하십시오:
2. 응답 결과는 아래 JSON 형식으로만 구조화하여 제공합니다. (JSON Key는 추가하거나 변경하지 않고 사용해주세요.):

```json
{
    "title": "Steel Beam Design Report",
    "section": [
        {
            "title": "Moment Capacity",
            "sub_section": [
                {
                    "title": "Section Classification",
                    "standard": "EN 1993-1-1",
                    "reference": "5.5",
                    "target": "Class 1, 2, 3, or 4"
                },
                {
                    "title": "Flange thickness ratio",
                    "standard": "EN 1993-1-1",
                    "reference": "Table 5.2",
                    "target": "c/tf"
                },
                {
                    "title": "Web thickness ratio",
                    "standard": "EN 1993-1-1",
                    "reference": "Table 5.2",
                    "target": "d/tw"
                },
                {
                    "title": "Plastic moment capacity",
                    "standard": "EN 1993-1-1",
                    "reference": "6.2.5",
                    "target": "Mc,Rd = Wpl·fy/γM0"
                },
                {
                    "title": "Elastic moment capacity",
                    "standard": "EN 1993-1-1",
                    "reference": "6.2.5",
                    "target": "Mc,Rd = Wel·fy/γM0"
                },
                {
                    "title": "Effective section properties",
                    "standard": "EN 1993-1-1",
                    "reference": "6.2.5",
                    "target": "Mc,Rd = Weff·fy/γM0"
                },
                {
                    "title": "Lateral-torsional buckling resistance",
                    "standard": "EN 1993-1-1",
                    "reference": "6.3.2",
                    "target": "Mb,Rd = χLT·Wy·fy/γM1"
                }
            ]
        },
        {
            "title": "Shear Capacity",
            "sub_section": [
                {
                    "title": "Web area",
                    "standard": "EN 1993-1-1",
                    "reference": "6.2.6",
                    "target": "Av = A - 2btf + (tw+2r)tf"
                },
                {
                    "title": "Plastic shear resistance",
                    "standard": "EN 1993-1-1",
                    "reference": "6.2.6",
                    "target": "Vpl,Rd = Av·fy/(√3·γM0)"
                },
                {
                    "title": "Shear buckling check",
                    "standard": "EN 1993-1-5",
                    "reference": "5.2",
                    "target": "hw/tw ≤ 72ε/η"
                }
            ]
        },
        {
            "title": "Combined Bending and Shear",
            "sub_section": [
                {
                    "title": "Reduced moment capacity due to shear",
                    "standard": "EN 1993-1-1",
                    "reference": "6.2.8",
                    "target": "MV,Rd = (Wpl - ρ·Aw²/(4·tw))·fy/γM0"
                },
                {
                    "title": "Shear reduction factor",
                    "standard": "EN 1993-1-1",
                    "reference": "6.2.8",
                    "target": "ρ = (2·VEd/Vpl,Rd - 1)²"
                }
            ]
        },
        {
            "title": "Torsional Effects",
            "sub_section": [
                {
                    "title": "St. Venant torsional constant",
                    "standard": "EN 1993-1-1",
                    "reference": "Annex A",
                    "target": "It"
                },
                {
                    "title": "Warping constant",
                    "standard": "EN 1993-1-1",
                    "reference": "Annex A",
                    "target": "Iw"
                },
                {
                    "title": "Torsional resistance",
                    "standard": "EN 1993-1-1",
                    "reference": "6.2.7",
                    "target": "TRd"
                }
            ]
        },
        {
            "title": "Buckling Resistance",
            "sub_section": [
                {
                    "title": "Slenderness ratio",
                    "standard": "EN 1993-1-1",
                    "reference": "6.3.1",
                    "target": "λ = Lcr/i"
                },
                {
                    "title": "Non-dimensional slenderness",
                    "standard": "EN 1993-1-1",
                    "reference": "6.3.1",
                    "target": "λ̄ = λ/λ1"
                },
                {
                    "title": "Buckling reduction factor",
                    "standard": "EN 1993-1-1",
                    "reference": "6.3.1",
                    "target": "χ = 1/(Φ + √(Φ² - λ̄²))"
                },
                {
                    "title": "Lateral-torsional buckling slenderness",
                    "standard": "EN 1993-1-1",
                    "reference": "6.3.2",
                    "target": "λ̄LT = √(Wy·fy/Mcr)"
                }
            ]
        },
        {
            "title": "Stiffener Design",
            "sub_section": [
                {
                    "title": "Transverse stiffener rigidity",
                    "standard": "EN 1993-1-5",
                    "reference": "9.3.1",
                    "target": "Ist ≥ 1.5·hw³·tw³/a²"
                },
                {
                    "title": "Stiffener buckling resistance",
                    "standard": "EN 1993-1-5",
                    "reference": "9.2.1",
                    "target": "NEd/NRd ≤ 1.0"
                }
            ]
        },
        {
            "title": "Fatigue Assessment",
            "sub_section": [
                {
                    "title": "Stress range",
                    "standard": "EN 1993-1-9",
                    "reference": "7",
                    "target": "Δσ"
                },
                {
                    "title": "Fatigue strength",
                    "standard": "EN 1993-1-9",
                    "reference": "7.1",
                    "target": "ΔσC"
                },
                {
                    "title": "Damage equivalent factor",
                    "standard": "EN 1993-1-9",
                    "reference": "7.1",
                    "target": "λ"
                },
                {
                    "title": "Fatigue verification",
                    "standard": "EN 1993-1-9",
                    "reference": "8",
                    "target": "γFf·Δσ ≤ ΔσC/(γMf·λ)"
                }
            ]
        }
    ]
}
```

주요 지침사항:
- 종속적 노드 간 상호 참조 포함
- 흐름도 순서의 논리적 진행 유지

"""

# Claude API 호출
response = client.messages.create(
    #model="claude-3-opus-20240229",  # 또는 sonnet 사용 가능
    model="claude-3-7-sonnet-20250219",
    # model="claude-3-5-sonnet-20240620",
    max_tokens=4096,
    temperature=0.1,
    messages=[
        {
            "role": "user",
            "content": f"""
당신은 설계기준을 이해하고 있는 구조공학 전문가입니다. 아래 질문에 대한 답변을 만들어주세요.

{user_input}
"""
        }
    ]
)

# 응답 출력
print(response.content[0].text)
