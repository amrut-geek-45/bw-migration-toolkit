import google.generativeai as genai
from ztable_lookup import get_ztable_info
import os


MODEL_NAME = "gemini-3-flash-preview"

genai.configure(api_key='AIzaSyCbhOydDIETBWhRSYnBQ2ibXYyujP5w6j8')

model = genai.GenerativeModel(MODEL_NAME)


def generate_reason(
    code,
    complexity,
    score
):

    # ------------------------------------
    # Detect Z tables from CSV
    # ------------------------------------

    ztable_details = get_ztable_info(
        code
    )

    if ztable_details:

        ztable_text = "\n".join([

            item["table"]

            for item in ztable_details

        ])

        ztable_section = f"""

4. Are there any custom Z tables present in the logic?

YES

{ztable_text}

"""

    else:

        ztable_section = """

4. Are there any custom Z tables present in the logic?

NO

No custom Z tables found

"""

    prompt = f'''
You are an SAP BW ABAP expert.

Analyze the following BW routine code.

Complexity Level: {complexity}

Rule Engine Score: {score}

Explain:

1. Why this complexity was assigned
2. Key complexity drivers
3. Migration difficulty

Keep the answer concise.

Code:

{code[:6000]}
'''

    response = client.models.generate_content(

        model=MODEL_NAME,

        contents=prompt

    )

    return response.text + ztable_section


def generate_functional_overview(
    code,
    transformation_summary=None
):

    summary_text = ""

    if transformation_summary is not None:

        try:

            summary_text = (

                transformation_summary
                .to_string()

            )

        except:

            summary_text = ""

    prompt = f'''
You are an SAP BW Functional Consultant.

Explain this transformation
for non-technical users.

Rules:

- Maximum 5 lines
- Avoid ABAP terms
- Explain in business language
- Mention source and target
- Mention custom tables if available

Transformation metadata:

{summary_text}

Transformation code:

{code[:6000]}
'''

    response = client.models.generate_content(

        model=MODEL_NAME,

        contents=prompt

    )

    return response.text