import google.generativeai as genai
import re

genai.configure(
    api_key=' AIzaSyD4bkU4Lry5bZxettHOHw_gRJ45MsfCBWQ'
)

MODEL_NAME = "gemini-3-flash-preview"

model = genai.GenerativeModel(
    MODEL_NAME
)


# ----------------------------------------
# Complexity explanation
# ----------------------------------------

def generate_reason(
    code,
    complexity,
    score
):

    prompt = f"""

You are an SAP BW ABAP expert.

Analyze this BW transformation code.

Complexity:
{complexity}

Score:
{score}

Explain:

1. Why complexity was assigned
2. Key complexity drivers
3. Migration difficulty

Keep concise.

Code:

{code[:6000]}

"""

    response = model.generate_content(
        prompt
    )

    return response.text


# ----------------------------------------
# Functional overview
# ----------------------------------------

def generate_functional_overview(
    code
):

    prompt = f"""

You are an SAP BW Functional Consultant.

Explain in 3-5 lines:

What this transformation does
in business language.

Code:

{code[:6000]}

"""

    response = model.generate_content(
        prompt
    )

    return response.text


# ----------------------------------------
# Z table overview
# ----------------------------------------

def generate_ztable_overview(
    ztable_details
):

    if not ztable_details:

        return ""

    text=""

    for table in ztable_details:

        text += f"""

Table:
{table["table"]}

Description:
{table["description"]}

Fields:
{table["overview"]}

"""

    prompt=f"""

You are an SAP BW Architect.

Analyze these custom tables.

Determine:

1. Master Data /
Transaction Data /
Lookup Table /
Configuration Table

2. Give 2-3 lines
explaining purpose

3. Mention characteristics

Format:

Table:

Type:

Overview:

Characteristics:

Input:

{text}

"""

    response=model.generate_content(
        prompt
    )

    return response.text