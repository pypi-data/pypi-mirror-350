import requests
import os
import math
import openai

# OpenAI API 키 설정
openai.api_key = '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'

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
            result.append(i)
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

# 평가 지표 함수 정의


def precision_at_k(results, relevant_docs, k):
    retrieved_k = results[:k]
    relevant_retrieved = sum(
        [1 for doc in retrieved_k if doc in relevant_docs])
    return relevant_retrieved / k


def recall_at_k(results, relevant_docs, k):
    retrieved_k = results[:k]
    relevant_retrieved = sum(
        [1 for doc in retrieved_k if doc in relevant_docs])
    return relevant_retrieved / len(relevant_docs) if relevant_docs else 0


def mean_reciprocal_rank(results, relevant_docs):
    for i, doc in enumerate(results):
        if doc in relevant_docs:
            return 1 / (i + 1)
    return 0


def dcg(results, relevant_docs):
    dcg_val = 0
    for i, doc in enumerate(results):
        if doc in relevant_docs:
            dcg_val += 1 / math.log2(i + 2)
    return dcg_val


def idcg(relevant_docs, k):
    ideal = sorted([1 / math.log2(i + 2)
                   for i in range(min(len(relevant_docs), k))])
    return sum(reversed(ideal))


def ndcg(results, relevant_docs, k):
    ideal_dcg = idcg(relevant_docs, k)
    if ideal_dcg == 0:
        return 0
    return dcg(results[:k], relevant_docs) / ideal_dcg

# 평가 함수: 하나의 테스트 케이스에 대해 점수 계산
def evaluate_result(result_ids, ref_ids, k):
    if k == 0:
        return {
            "Precision@k": 0,
            "Recall@k": 0,
            "MRR": 0,
            "nDCG@k": 0,
            "Score_100": 0
        }

    precision = precision_at_k(result_ids, ref_ids, k)
    recall = recall_at_k(result_ids, ref_ids, k)
    mrr = mean_reciprocal_rank(result_ids, ref_ids)
    ndcg_val = ndcg(result_ids, ref_ids, k)
    average_score = (precision + recall + mrr + ndcg_val) / 4
    score_100 = average_score * 100
    return {
        "Precision@k": precision,
        "Recall@k": recall,
        "MRR": mrr,
        "nDCG@k": ndcg_val,
        "Score_100": score_100
    }


if __name__ == "__main__":
    url = "https://moa.rpm.kr-dv-midasit.com/"
    headers = get_token()
    question = "concrete shear resistance of RC Beam"


    test_case = [
        {
            "thread_id": "01JP1G6V2WEKYHKT3TE2MEJR68",
            "dgncode": "EN1992-1-1",
            "language": "english",
            "ref_id": [
                "01JP1GGTTNHJ4WKE9GCAQ0B2BZ",
            ]
        },
        {
            "thread_id": "01JP28F6224T6AV9866B16BMM3",
            "dgncode": "NTC2018",
            "language": "italian",
            "ref_id": [
                "01JP28HVS56T92DC7FJWP3EC2G",
            ]
        },
        {
            "thread_id": "01JSDR75BWN2XY3WBP2VKWTYB2",
            "dgncode": "DPT 1301-1302-61",
            "language": "thai",
            "ref_id": [
                "01JSDRAB0XJQQZFKRA7BMZG45D",
            ]
        },
    ]
    for idx, test in enumerate(test_case):
        trans_response = openai.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system",
                    "content": f"당신은 건축/토목 구조 공학 전문가입니다. 아래 문장을 {test['language']} 나라의 언어로 전문용어를 살려서 번역해주세요. 단, 한개의 문장이 아니라 유사한 의미의 문장 여러개를 만들어 주세요, 최소 30개 이상"},
                {"role": "user", "content": question}
            ],
            temperature=0.3
        )
        trans_query = trans_response.choices[0].message.content
        # 검색 수행
        response = search_knw(url, trans_query, "HYBRID", 0.1,
                              10, 0.7, [test["thread_id"]], headers)
        result_cell_ids = []
        for i in response:
            result_cell_ids.append(i["cellId"])
        # 정답 비교 및 점수 계산
        result_score = evaluate_result(
            result_cell_ids, set(test['ref_id']), len(response))
        # 출력
        print(f"\n[{test['dgncode']}] Query Test: {question}, {trans_query}")
        print(f"Retrieved: {result_cell_ids}")
        print(f"Reference: {test['ref_id']}")
        print(f"Precision@k: {result_score['Precision@k']:.3f}")
        print(f"Recall@k: {result_score['Recall@k']:.3f}")
        print(f"MRR: {result_score['MRR']:.3f}")
        print(f"nDCG@k: {result_score['nDCG@k']:.3f}")
        print(f"▶ 총점 (100점 만점): {result_score['Score_100']:.2f}점")