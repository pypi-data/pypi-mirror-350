import asyncio

import pandas as pd

from fmcore import BasePromptTuner
from fmcore import PromptTunerConfig

product_type = "CELLULAR_PHONE"
attribute = "model_number"

train_s3_path = f's3://zvkumarn-autoprompt-tuner/Experiments_dataset/2025_04_25/{product_type}_{attribute}_train.parquet'
test_s3_path = f's3://zvkumarn-autoprompt-tuner/Experiments_dataset/2025_04_25/{product_type}_{attribute}_test.parquet'
val_s3_path = f's3://zvkumarn-autoprompt-tuner/Experiments_dataset/2025_04_25/{product_type}_{attribute}_val.parquet'
output_s3_path = f's3://dc-test-rajsiba/starfish/cdq/{product_type}/{attribute}'

train = pd.read_parquet(train_s3_path)

# Trim the necessary bits and set it as the prompt to be tuned
input_prompt = """
ROLE: You are a Catalog Expert. You analyze product information and you are trying your best to infer missing attribute values.

Analyze the provided Amazon product information in JSON format, detailed above, to determine the value in English of a specific attribute.

Your task is to thoroughly examine the product details. If the attribute's value is clearly inferable from the provided information, make an accurate prediction. 
In scenarios where the value cannot be deduced, indicate this with '[NO]' for Not Obtainable. 
If the attribute does not pertain to the product, use '[NA]' for Not Applicable. 
Ensure your prediction is compatible with the attribute's data type, such as predicting 'True' or 'False' for Boolean attributes, or an integer for Integer attributes. Avoid using scientific notation for any prediction.


Focus your analysis on this specific attribute: 
attribute name: model_number.
"""


def split_into_sections(text):
    parts = text.split('###')
    sections = []
    for part in parts:
        if part.strip():
            lines = part.strip().splitlines()
            title = lines[0].strip(':').strip()
            body = '\n'.join(lines[1:]).strip()
            sections.append((title, body))
    return sections


def replace_last_occurrence(sections, target_title, new_body_text):
    for i in range(len(sections) - 1, -1, -1):
        title, body = sections[i]
        if title == target_title:
            sections[i] = (title, new_body_text)
            break
    return sections


def rebuild_text(sections):
    return ''.join(f"### {title}:\n{body}\n\n" for title, body in sections)


def insert_additional_rule(sections, additional_rule_text):
    # Find the last section starting with "Rules"
    for i in range(len(sections) - 1, -1, -1):
        title, body = sections[i]
        if title.startswith("Rules"):
            # Insert the additional rule at the end
            body = body.rstrip()
            body += f"\n\nAdditional Rule:\n{additional_rule_text}"
            sections[i] = (title, body)
            break
    return sections


def update_text(text, add_additional_rule=False):
    sections = split_into_sections(text)

    sections = replace_last_occurrence(
        sections,
        "Amazon product data",
        """{
"asin": {{input.asin}},
"product_type": {{input.product_type}},
"attribute": {{input.attribute}},
"asin_info": {{input.asin_info}},
"attribute_instructions": {{input.attribute_instructions}}
}"""
    )

    sections = replace_last_occurrence(
        sections,
        "Test value",
        "Now verify the test value of the attribute '{{input.attribute}}': '{{output.attribute_value}}'."
    )

    sections = replace_last_occurrence(
        sections,
        "Output format",
        """Your prediction can only be 'Correct', 'Incorrect', or 'Unknown'.
Output your prediction in the following JSON format. The JSON should not have anything else except the reason and the prediction.
{'{{input.attribute}}': [{"reason": "reason for the prediction", "prediction": "Correct/Incorrect/Unknown"}]} """
    )

    if add_additional_rule:
        additional_rule = (
            "1. If you cannot deduce the value of the '{{input.attribute_value}}' from the given product data\n"
            "    a. if the test value is 'NA' or 'NO' predict 'Correct'\n"
            "    b. else predict 'Unknown'."
        )
        sections = insert_additional_rule(sections, additional_rule)

    updated_text = rebuild_text(sections)
    return updated_text


# Filter only valid rows
valid_rows = train[train["aqumen_prompt"].notna() & (train["aqumen_prompt"].str.strip() != "")]

eval_prompt = None

if not valid_rows.empty:
    while eval_prompt is None:
        random_row = valid_rows.sample(1)
        candidate = random_row.iloc[0]["aqumen_prompt"]
        if not candidate or len(candidate) < 10:
            continue
        else:
            eval_prompt = update_text(candidate)
            break
else:
    print("No valid rows found.")

print("INPUT PROMPT")
print(input_prompt)
print("EVAL PROMPT")
print(eval_prompt)

mode = "light"

prompt_tuner_config = {
    "task_type": "TEXT_GENERATION",
    "dataset_config": {
            "inputs": {
                "TRAIN": {
                    "path": train_s3_path,
                    "storage": "S3",
                    "format": "PARQUET",
                },
                "VAL": {
                    "path": val_s3_path,
                    "storage": "S3",
                    "format": "PARQUET",
                },
                "TEST": {
                    "path": test_s3_path,
                    "storage": "S3",
                    "format": "PARQUET",
                },
            },
            "output": {
                "name": "results",
                "path": output_s3_path,
                "storage": "S3",
                "format": "PARQUET",
            },
        },
    "prompt_config": {
        "prompt": input_prompt,
        "input_fields": [{
                "name": "asin",
                "description": "This field represent the unique identifier for a product",
            },
            {
                "name": "product_type",
                "description": "This fields represent the type of product",
            },
            {
                "name": "attribute",
                "description": "This field represents the attribute to be extracted",
            },
            {
                "name": "asin_info",
                "description": "This field represent the information related to product",
            },
            {
                "name": "attribute_instructions",
                "description": "This field represent the additional information related to product like possible values for attribute_value",
            },
        ],
        "output_fields": [{
            "name": "attribute_value",
            "description": "This field represent the value extracted for the given attribute_name from the product",
        }],
    },
    "framework": "DSPY",
    "optimizer_config": {
        "optimizer_type": "MIPRO_V2",
        "student_config": {
            'provider_type': 'LAMBDA',
            'model_id': 'mistralai/Mistral-Nemo-Instruct-2407',
            'model_params': {
                'temperature': 1.0,
                'max_tokens': 1024,
                'top_p': 0.9
            },
            'provider_params': {
                'retries': {
                    'max_retries': 3,
                    'backoff_factor': 1.0,
                    'jitter': 1.0,
                    'retryable_exceptions': ['InvalidSignatureException', 'ThrottlingException',
                        'ModelTimeoutException', 'ServiceUnavailableException',
                        'ModelNotReadyException', 'ServiceQuotaExceededException',
                        'ModelErrorException', 'EndpointConnectionError'
                    ]
                },
                'rate_limit': {
                    'max_rate': 10000,
                    'time_period': 60
                },
                'region': 'us-west-2',
                "role_arn": "",
                'function_arn': 'arn:aws:lambda:us-west-2:136238946932:function:MistralNemo'
            }
        },
        "teacher_config": {
            "provider_type": "BEDROCK",
            "model_id": "anthropic.claude-3-5-sonnet-20240620-v1:0",
            "model_params": {
                "temperature": 0.5,
                "max_tokens": 1024
            },
            "provider_params_list": [
                {
                    "retries": {
                        "max_retries": 50
                    },
                    "rate_limit": {
                        "max_rate": 400
                    },
                    "role_arn": "arn:aws:iam::863518436859:role/ModelFactoryBedrockAccessRole",
                    "region": "us-east-1"
                },
                {
                    "retries": {
                        "max_retries": 50
                    },
                    "rate_limit": {
                        "max_rate": 400
                    },
                    "role_arn": "arn:aws:iam::615299746603:role/ModelFactoryBedrockAccessRole",
                    "region": "us-east-1"
                },
                {
                    "retries": {
                        "max_retries": 50
                    },
                    "rate_limit": {
                        "max_rate": 400
                    },
                    "role_arn": "arn:aws:iam::615299746603:role/ModelFactoryBedrockAccessRole",
                    "region": "us-west-2"
                },
                {
                    "retries": {
                        "max_retries": 50
                    },
                    "rate_limit": {
                        "max_rate": 400
                    },
                    "role_arn": "arn:aws:iam::710271919393:role/ModelFactoryBedrockAccessRole",
                    "region": "us-east-1"
                },
                {
                    "retries": {
                        "max_retries": 50
                    },
                    "rate_limit": {
                        "max_rate": 400
                    },
                    "role_arn": "arn:aws:iam::710271919393:role/ModelFactoryBedrockAccessRole",
                    "region": "us-west-2"
                },
                {
                    "retries": {
                        "max_retries": 50
                    },
                    "rate_limit": {
                        "max_rate": 400
                    },
                    "role_arn": "arn:aws:iam::872515274170:role/ModelFactoryBedrockAccessRole",
                    "region": "us-east-1"
                },
                {
                    "retries": {
                        "max_retries": 50
                    },
                    "rate_limit": {
                        "max_rate": 400
                    },
                    "role_arn": "arn:aws:iam::872515274170:role/ModelFactoryBedrockAccessRole",
                    "region": "us-west-2"
                }
            ]
        },
        "evaluator_config": {
            "evaluator_type": "LLM_AS_A_JUDGE_BOOLEAN",
            "evaluator_params": {
                "prompt": eval_prompt,
                "criteria": "model_number[0]['prediction'] == 'Correct'",
                "llm_config": {
                    "provider_type": "BEDROCK",
                    "model_id": "anthropic.claude-3-haiku-20240307-v1:0",
                    "model_params": {
                        "temperature": 0.5,
                        "max_tokens": 1024
                    },
                    "provider_params_list": [
                        {
                            "retries": {
                                "max_retries": 50
                            },
                            "rate_limit": {
                                "max_rate": 400
                            },
                            "role_arn": "arn:aws:iam::863518436859:role/ModelFactoryBedrockAccessRole",
                            "region": "us-east-1"
                        },
                        {
                            "retries": {
                                "max_retries": 50
                            },
                            "rate_limit": {
                                "max_rate": 400
                            },
                            "role_arn": "arn:aws:iam::615299746603:role/ModelFactoryBedrockAccessRole",
                            "region": "us-east-1"
                        },
                        {
                            "retries": {
                                "max_retries": 50
                            },
                            "rate_limit": {
                                "max_rate": 400
                            },
                            "role_arn": "arn:aws:iam::615299746603:role/ModelFactoryBedrockAccessRole",
                            "region": "us-west-2"
                        },
                        {
                            "retries": {
                                "max_retries": 50
                            },
                            "rate_limit": {
                                "max_rate": 400
                            },
                            "role_arn": "arn:aws:iam::710271919393:role/ModelFactoryBedrockAccessRole",
                            "region": "us-east-1"
                        },
                        {
                            "retries": {
                                "max_retries": 50
                            },
                            "rate_limit": {
                                "max_rate": 400
                            },
                            "role_arn": "arn:aws:iam::710271919393:role/ModelFactoryBedrockAccessRole",
                            "region": "us-west-2"
                        },
                        {
                            "retries": {
                                "max_retries": 50
                            },
                            "rate_limit": {
                                "max_rate": 400
                            },
                            "role_arn": "arn:aws:iam::872515274170:role/ModelFactoryBedrockAccessRole",
                            "region": "us-east-1"
                        },
                        {
                            "retries": {
                                "max_retries": 50
                            },
                            "rate_limit": {
                                "max_rate": 400
                            },
                            "role_arn": "arn:aws:iam::872515274170:role/ModelFactoryBedrockAccessRole",
                            "region": "us-west-2"
                        }
                    ]
                }
            }
        },
        "optimizer_params": {
            "minibatch": False,
            "optimizer_metric": "ACCURACY"
        },
    }
}

async def run_pt(prompt_tuner_config=None):
    prompt_tuner_config = PromptTunerConfig(**prompt_tuner_config)
    print(prompt_tuner_config.model_dump())
    tuner = BasePromptTuner.of(config=prompt_tuner_config)
    await tuner.tune()


if __name__ == "__main__":
    asyncio.run(run_pt(prompt_tuner_config=prompt_tuner_config))
