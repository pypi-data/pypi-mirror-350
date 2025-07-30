import os

if os.environ.get("MAITAI_ENV") in ["prod", "staging", "development", "test"]:
    from maitai_models.config import Config, InferenceLocations
else:
    from maitai.models.config import Config, InferenceLocations


def get_default_config() -> Config:
    return Config(
        inference_location=InferenceLocations.SERVER,
        evaluation_enabled=True,
        apply_corrections=False,
        model="gpt-4o",
        temperature=1,
        streaming=False,
        response_format="text",
        stop=None,
        logprobs=False,
        max_tokens=None,
        n=1,
        frequency_penalty=0,
        presence_penalty=0,
        timeout=0,
        context_retrieval_enabled=False,
        fallback_model=None,
        safe_mode=False,
        extract_request_metadata=True,
        metadata={},
    )


def reconcile_config_with_default(config_dict: dict) -> Config:
    default_config_json = get_default_config().model_dump()
    for key, value in default_config_json.items():
        if key not in config_dict:
            config_dict[key] = value
    return Config.model_validate(config_dict)
