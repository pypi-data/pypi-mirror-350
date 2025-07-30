from fmcore.inference.base_inference_manager import BaseInferenceManager
from fmcore.inference.types.inference_manager_types import InferenceManagerConfig
import random

# -------------------------------
# Configuration Definitions
# -------------------------------

bedrock_config_dict = {
    "inference_manager_type": "MULTI_PROCESS",
    "llm_config": {
        "provider_type": "BEDROCK",
        "model_id": "anthropic.claude-3-haiku-20240307-v1:0",
        "model_params": {
            "max_tokens": 512,
            "temperature": 0.9,
            "top_p": 1.0,
        },
        "provider_params_list": [
            {
                "role_arn": "arn:aws:iam::872515274170:role/ModelFactoryBedrockAccessRole",
                "region": "us-east-1",
                "rate_limit": {"max_rate": 1000},
                "retries": {"max_retries": 3, "strategy": "constant"},
            },
            {
                "role_arn": "arn:aws:iam::872515274170:role/ModelFactoryBedrockAccessRole",
                "region": "us-west-2",
                "rate_limit": {"max_rate": 1000},
                "retries": {"max_retries": 3, "strategy": "constant"},
            },
        ],
    },
    "inference_manager_params": {"num_process": 10},
}

lambda_inference_manager_config = {
    "inference_manager_type": "MULTI_PROCESS",
    "llm_config": {
        "provider_type": "LAMBDA",
        "model_id": "mistralai/Mistral-Nemo-Instruct-2407",
        "model_params": {
            "temperature": 0.5,
            "max_tokens": 1024
        },
        "provider_params": {
            "role_arn": "arn:aws:iam::<accountId>:role/<roleId>",
            "function_arn": "arn:aws:lambda:<region>:<accountId>:function:<function_arn>",
            "region": "us-west-2",
            "rate_limit": {
                "max_rate": 10000,
                "time_period": 60
            },
            "retries": {
                "max_retries": 3
            }
        }
    },
    "inference_manager_params": {
        "num_process": 10
    }
}

# -------------------------------
# Question Generator
# -------------------------------

question_templates = [
    "What is the capital of {}?",
    "How do you cook {}?",
    "Can you explain {} in simple terms?",
    "What are the benefits of {}?",
    "Who discovered {}?",
    "Why is {} important?",
    "What's the difference between {} and {}?",
    "How can I improve my {} skills?",
    "Is {} good for health?",
    "Tell me a fun fact about {}."
]

fillers = [
    "Python", "quantum physics", "broccoli", "machine learning", "Napoleon",
    "Java vs Python", "public speaking", "meditation", "Venus", "photosynthesis"
]

def get_random_questions(n: int):
    questions = []
    for _ in range(n):
        template = random.choice(question_templates)
        if "{} and {}" in template:
            f1, f2 = random.sample(fillers, 2)
            question = template.format(f1, f2)
        else:
            f = random.choice(fillers)
            question = template.format(f)
        questions.append([{"role": "user", "content": question}])
    return questions


# -------------------------------
# Run Inference
# -------------------------------

def run_inference(config_dict, num_questions=100):
    config = InferenceManagerConfig(**config_dict)
    messages = get_random_questions(num_questions)
    inference_manager = BaseInferenceManager.of(config=config)
    inference_manager.run(dataset=messages)


# -------------------------------
# Test Either Config Here
# -------------------------------

if __name__ == "__main__":
    # Choose one:
    run_inference(bedrock_config_dict, 50000)
    #run_inference(lambda_inference_manager_config)
