import openai
import os
from pydantic import Field
from moapy.auto_convert import auto_schema, MBaseModel

# pyscript 환경 감지
try:
    from pyscript import document  # noqa: F401
    ENV = 'pyscript'
except ImportError:
    ENV = os.getenv('ENV', 'local')  # 기본값은 'local'입니다.

if ENV == 'server':
    from moapy.midasutil_server import midas_util, Product
elif ENV == 'pyscript':
    from moapy.midasutil_web import midas_util, Product
else:
    from moapy.midasutil import midas_util, Product


class PythonFuncInput(MBaseModel):
    """
    Python Function Input Class
    """
    refData: dict = Field(default={}, description="json data")
    do_what: str = Field(default="", description="what to do")

@auto_schema(title="Generate Python Function", description="Generate Python Function")
def generate_python_function(inp: PythonFuncInput) -> str:
    openai.api_key = midas_util.get_MAPI_Key(Product.CIVIL)
    refData = inp.refData
    do_what = inp.do_what
    try:
    # Define the prompt
        prompt = f"""
        Given the following JSON data:
        {refData}

        Write a Python function that {do_what} from this data.
        Please provide only the code in a single code block.
        """

        # Call the OpenAI API with gpt-3.5-turbo
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1024,
            n=1,
            temperature=0.7,
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"An error occurred: {e}"

# Example usage
refData = {
    "moapy.wgsd.wgsd_flow.MaterialConcrete":
        {"grade":{"design_code":"ACI318M-19","grade":"C12"},
         "curve_uls":[{"stress":0,"strain":0},{"stress":0,"strain":0.0004500000000000001},
                      {"stress":10.2,"strain":0.0004500000000000001},{"stress":10.2,"strain":0.003}],
         "curve_sls":[{"stress":0,"strain":0},{"stress":12,"strain":0.003}]}}
doWhat = "2D 그래프로 그려줘"
inp = PythonFuncInput(refData=refData, do_what=doWhat)
response = generate_python_function(inp)
print(response)