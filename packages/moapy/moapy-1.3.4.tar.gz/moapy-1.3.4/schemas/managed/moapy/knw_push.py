import requests
import os
import openai

# OpenAI API 키 설정
openai.api_key = "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"

def get_token():
    post_members_login_url = f'https://members.rpm.kr-dv-midasit.com/auth/api/v1/login'

    body = {
        'email': "bschoi@midasit.com",
        'password': "midasit0901"
    }

    login_response = requests.post(post_members_login_url, json=body)
    login_info = login_response.json()
    token = login_info['token']
    headers = {
        'X-AUTH-TOKEN': 'Bearer ' + token
    }
    return headers


def search_knw(url, query, method, simScore, topK, keyWeight, id_l, headers):
    url += 'backend/gpt/retrieve'
    data = {
        "source": query,
        "refThreadList": id_l,
        "similarityScore": simScore,
        "similarTopK": topK,
        "retrievalType": method,
        "keywordSearchWeight": keyWeight,
        "isServiceSearch": False,
        "productName": "CIVIL"
    }
    input_response = requests.post(url, json=data, headers=headers)
    if input_response.status_code == 200:
        raw_data = input_response.json()
        result = []
        for i in raw_data:
            result.append(i["source"])
        return result
    else:
        print("검색 실패~!")


def post_knw(thread_id, headers, contents):
    post_gpt_knowledge_url = 'https://moa.rpm.kr-dv-midasit.com/backend/gpt/threads/knowledges/' + \
        thread_id + '/cells'

    data = {
        'cell': {
            'role': 'assistant',
            'source': contents
        }
    }
    input_response = requests.post(
        post_gpt_knowledge_url, json=data, headers=headers)
    if (input_response.status_code == 200):
        print('knw upload success')
        return input_response.json()['cell']['cellId']
    else:
        print("knw upload fail")
        return False


if __name__ == "__main__":
    url = "https://moa.rpm.kr-dv-midasit.com/"
    headers = get_token()

    knw_thread_id = "01JTPZKEGW6RNXD1WHKN6PPSMP"

    # knw 등록
    file_path = r"C:\Users\bschoi\OneDrive - MIDAS\회사관련자료\2025-1\ntc2018\italy_nct"
    file_l = os.listdir(file_path)
    for f in file_l:
        text = open(file_path+f"/{f}", 'r', encoding='utf-8').read()
        # text를 영어로 번역
        translation_response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "당신은 전문 번역가입니다. 주어진 텍스트를 영어로 정확하게 번역해주세요."},
                {"role": "user", "content": text}
            ],
            temperature=0.1
        )
        translated_text = translation_response.choices[0].message.content
        text = translated_text  # 번역된 텍스트로 대체
        post_knw(knw_thread_id, headers, text)