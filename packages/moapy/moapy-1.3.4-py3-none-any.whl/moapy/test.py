md = """
# 강철 보(Steel Beam) 설계 계산서

## 1. 프로젝트 정보

- **프로젝트명**: 상업용 건물 구조 설계
- **작성자**: 홍길동
- **날짜**: 2025-04-08
- **참조 규격**: KDS 14 31 10

## 2. 입력 변수

| 기호 | 설명 | 값 | 단위 |
|------|------|-----|------|
| $L$ | 보 길이 | 6.0 | m |
| $b$ | 보 폭 | 200 | mm |
| $h$ | 보 높이 | 400 | mm |
| $f_y$ | 항복 강도 | 400 | MPa |
| $E$ | 탄성 계수 | 200,000 | MPa |
| $q$ | 분포 하중 | 15 | kN/m |

## 3. 단면 특성 계산

### 3.1 단면적 ($A$)

$$A = b \times h \tag{3.1}$$

$$A = 200 \times 400 = 80,000 \; \text{mm}^2 = 0.08 \; \text{m}^2$$

### 3.2 단면 2차 모멘트 ($I$)

$$I = \frac{b \times h^3}{12} \tag{3.2}$$

$$I = \frac{200 \times 400^3}{12} = 1.067 \times 10^9 \; \text{mm}^4 = 1.067 \times 10^{-3} \; \text{m}^4$$

### 3.3 단면 계수 ($Z$)

$$Z = \frac{b \times h^2}{6} \tag{3.3}$$

$$Z = \frac{200 \times 400^2}{6} = 5.333 \times 10^6 \; \text{mm}^3 = 5.333 \times 10^{-3} \; \text{m}^3$$

## 4. 하중 분석

### 4.1 최대 휨 모멘트 ($M_{max}$)

단순 지지된 보에서 등분포 하중 $q$에 의한 최대 휨 모멘트:

$$M_{max} = \frac{q L^2}{8} \tag{4.1}$$

$$M_{max} = \frac{15 \times 6.0^2}{8} = 67.5 \; \text{kN} \cdot \text{m}$$

### 4.2 최대 전단력 ($V_{max}$)

$$V_{max} = \frac{q L}{2} \tag{4.2}$$

$$V_{max} = \frac{15 \times 6.0}{2} = 45 \; \text{kN}$$

## 5. 강도 검토

### 5.1 휨 강도 검토

최대 휨 응력 ($\sigma_{max}$):

$$\sigma_{max} = \frac{M_{max}}{Z} \tag{5.1}$$

$$\sigma_{max} = \frac{67.5 \times 10^6}{5.333 \times 10^6} = 12.66 \; \text{MPa}$$

허용 휨 응력 ($\sigma_{allow}$):

$$\sigma_{allow} = 0.66 \times f_y \tag{5.2}$$

$$\sigma_{allow} = 0.66 \times 400 = 264 \; \text{MPa}$$

안전율 ($SF_{bending}$):

$$SF_{bending} = \frac{\sigma_{allow}}{\sigma_{max}} \tag{5.3}$$

$$SF_{bending} = \frac{264}{12.66} = 20.85 > 1.5 \quad \therefore \text{안전}$$

### 5.2 처짐 검토

최대 처짐량 ($\delta_{max}$):

$$\delta_{max} = \frac{5 q L^4}{384 E I} \tag{5.4}$$

$$\delta_{max} = \frac{5 \times 15 \times 6.0^4 \times 10^3}{384 \times 200,000 \times 1.067 \times 10^{-3}} = 6.59 \; \text{mm}$$

허용 처짐량 ($\delta_{allow}$):

$$\delta_{allow} = \frac{L}{360} \tag{5.5}$$

$$\delta_{allow} = \frac{6000}{360} = 16.67 \; \text{mm}$$

안전율 ($SF_{deflection}$):

$$SF_{deflection} = \frac{\delta_{allow}}{\delta_{max}} \tag{5.6}$$

$$SF_{deflection} = \frac{16.67}{6.59} = 2.53 > 1.0 \quad \therefore \text{안전}$$

## 6. 결론

수행된 구조 계산에 따르면, 제안된 강철 보(200mm × 400mm)는 주어진 하중 조건에서 다음과 같이 안전합니다:

1. 휨 강도 안전율: 20.85 > 1.5 ✓
2. 처짐 안전율: 2.53 > 1.0 ✓

따라서 제안된 보 단면은 설계 요구 사항을 충족합니다.

## 7. 참고 문헌

1. 대한건축학회 (2019). 건축구조기준 KDS 14 31 10
2. 한국강구조학회 (2020). 강구조 설계 지침서
"""

import subprocess
import os
# reference.docx 절대경로로 지정 (예: 현재 경로 기준)
reference_docx_path = r"C:\MIDAS\moapy_release\moapy\ref_4.docx"  # 적절히 수정 필요

def convert_md_to_docx(md: str, docx_file: str, reference: str = None):
    """
    Convert Markdown content to DOCX using Pandoc and optional reference DOCX template.

    :param md: Markdown content as a string
    :param docx_file: Path to the output DOCX file
    :param reference: Optional reference DOCX file path for styling
    """
    try:
        with open('temp.md', 'w', encoding='utf-8') as temp_md_file:
            temp_md_file.write(md)

        command = ['pandoc', 'temp.md', '-o', docx_file]

        if reference:
            command += ['--reference-doc', reference]

        subprocess.run(command, check=True)
        print(f"✅ Successfully converted Markdown to {docx_file}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during DOCX conversion: {e}")
    finally:
        if os.path.exists('temp.md'):
            os.remove('temp.md')
            
convert_md_to_docx(md, 'output.docx', reference_docx_path)