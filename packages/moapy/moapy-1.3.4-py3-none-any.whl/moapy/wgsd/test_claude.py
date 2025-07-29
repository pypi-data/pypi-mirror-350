import anthropic

# Claude API 키 설정
client = anthropic.Anthropic(api_key="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")

# 사용자 질문 정의
user_input = """

구조공학 전문가로서 설계 기준과 설계 절차 흐름에 대한 상세 정보를 제공하게 됩니다.

먼저, Eurocode2 RC Beam을 설계 하기 위한 검토항목에 대해 분석합니다.(검토항목은 아래 예시 중 분석 가능한 최대 항목을 포함합니다. : 휨검토, 전단검토, 철근비검토, 철근량검토, 균열검토, 콘크리트 응력검토, 철근 응력검토, 좌굴 검토...)

검토 항목과 관련된 수식에 대해서도 분석합니다.

관련된 수식이 다른 수식을 포함하는 경우 관련된 수식을 모두 포함하여 분석합니다.

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
    "title": "RC Beam Design Report",
    "section": [
        {
            "title": "Moment Capacity",
            "sub_section": [
                {
                    "title": "minimum rebar ratio",
                    "standard": "BSEN1992",
                    "reference": "9.2.1.1",
                    "target": normalize("A_{s,min}")
                },
                {
                    "title": "maximum reinforcement area",
                    "standard": "BSEN1992",
                    "reference": "9.2.1.1",
                    "target": normalize("A_{s,max}")
                },
                {
                    "title": "bending moment capacity",
                    "standard": "BSEN1992",
                    "reference": "6.1",
                    "target": normalize("M_{Rd}")
                }
            ]
        },
        {
            "title": "Shear Capacity",
            "sub_section": [
                {
                    "title": "concrete shear strength",
                    "standard": "BSEN1992",
                    "reference": "6.2.2",
                    "target": normalize("V_{Rd,c}")
                },
                {
                    "title": "shear strength of reinforcement",
                    "standard": "BSEN1992",
                    "reference": "6.2.3",
                    "target": normalize("V_{Rd,s}")
                }
            ]
        },
        {
            "title": "Concrete Stress Limitation",
            "sub_section": [
                {
                    "title": "concrete stress",
                    "standard": "BSEN1992",
                    "reference": "3.1.7",
                    "target": normalize("\\sigma_c")
                },
                {
                    "title": "limit value of concrete stress",
                    "standard": "BSEN1992",
                    "reference": "7.2",
                    "target": "SIGMA_ccrit"
                }
            ]
        },
        {
            "title": "Reinforcement Stress Limitation",
            "sub_section": [
                {
                    "title": "limit value of reinforcement stress",
                    "standard": "BSEN1992",
                    "reference": "7.2",
                    "target": "SIGMA_scrit"
                }
            ]
        },
        {
            "title": "Concrete Crack Width",
            "sub_section": [
                {
                    "title": "crack width",
                    "standard": "BSEN1992",
                    "reference": "7.3.4",
                    "target": normalize("w_k")
                }
            ]
        }
    ]
}

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
