from typing import Annotated

from pydantic import BaseModel, Field, Optional, StringConstraints, Union

valid_models = [
    "2.7B",
    "6B-v4",
    "euterpe-v2",
    "genji-python-6b",
    "genji-jp-6b",
    "genji-jp-6b-v2",
    "krake-v2",
    "hypebot",
    "infillmodel",
    "cassandra",
    "sigurd-2.9b-v1",
    "blue",
    "red",
    "green",
    "purple",
    "clio-v1",
    "kayra-v1",
]


ModelType = Annotated[str, StringConstraints(pattern=r"|".join(valid_models))]


class GenerationParameters(BaseModel):
    stop_sequences: Optional[list]
    bad_word_ids: Optional[list]
    use_string: bool = True
    logit_bias: Optional[list]
    logit_bias_exp: Optional[list]
    order: Optional[list]
    repretition_penalty_whitelist: Optional[list]
    temperature: float = Field(..., ge=0.1, le=100)
    temperature: Union[int, float] = Field(..., ge=0.1, le=100)
    min_length: int = Field(..., ge=1, le=2048)
    max_length: int = Field(..., ge=1, le=2048)
    do_sample: Optional[bool]
    early_stopping: Optional[bool]
    num_beams: Optional[int]
    top_k: Optional[int]
    top_a: Optional[int]
    top_p: Optional[int]
    typical_p: Optional[int]
    repetition_penalty: Optional[int]
    pad_token_id: Optional[int]
    bos_token_id: Optional[int]
    eos_token_id: Optional[int]
    length_penalty: Optional[int]
    no_repeat_ngram_size: Optional[int]
    encoder_no_repeat_ngram_size: Optional[int]
    num_return_sequences: Optional[int]
    max_time: Optional[int]
    use_cache: Optional[bool]
    num_beam_groups: Optional[int]
    diversity_penalty: Optional[int]
    tail_free_sampling: Optional[Field(int, ge=0, le=1)]
    repetition_penalty_range: Optional[Field(int, ge=0, le=8192)]
    repetition_penalty_slope: Optional[Field(int, ge=0, le=10)]
    get_hidden_states: Optional[bool]
    repetition_penalty_frequency: Optional[Field(int, ge=-2, le=2)]
    repetition_penalty_presence: Optional[Field(int, ge=-2, le=2)]
    next_word: Optional[bool]
    prefix: Optional[str]
    output_nonzero_probs: Optional[bool]
    generate_until_sentence: Optional[bool]
    num_logprobs: Optional[Field(int, ge=0, le=30)]
    cfg_uc: Optional[str]
    cfg_scale: Optional[Field(int, ge=0)]
    cfg_alpha: Optional[Field(int, ge=0, le=1)]
    phrase_rep_pen: Optional[str]
    top_g: Optional[Field(int, ge=0, le=65536)]
    mirostat_tau: Optional[Field(int, ge=0)]
    mirostat_lr: Optional[Field(int, ge=0, le=1)]


class AiGenerateRequest(BaseModel):
    input_text: str = Field(..., min_length=1, max_length=40000)
    model: ModelType
    parameters: GenerationParameters


class AiGenerateResponse(BaseModel):
    output: Optional[str]
    error: Optional[str]
