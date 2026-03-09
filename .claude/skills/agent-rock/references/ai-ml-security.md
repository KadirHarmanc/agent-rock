# AI/ML Security Reference

Use this reference when the project uses AI/ML libraries, LLMs, model serving, or
ML pipeline infrastructure. AI/ML applications introduce unique attack surfaces around
model inputs, serialization, prompt handling, and data pipelines.

## Detection

AI/ML code is present when you see:
- **Python ML:** `tensorflow`, `torch`, `pytorch`, `keras`, `scikit-learn`, `transformers`, `langchain`, `llama-index`, `openai`, `anthropic`, `cohere`
- **Model serving:** `fastapi` + model loading, `flask` + ML, `triton`, `seldon`, `mlflow`, `bentoml`, `ray[serve]`
- **Data pipeline:** `pandas`, `numpy`, `dask`, `airflow`, `prefect`, `dagster`
- **Notebooks:** `.ipynb` files with ML imports
- **Model files:** `*.pkl`, `*.pickle`, `*.pt`, `*.pth`, `*.h5`, `*.onnx`, `*.safetensors`, `*.gguf`
- **Config:** `model_config.yaml`, `.env` with API keys, `transformers` cache dirs

---

## Category 1: Unsafe Model Deserialization

```
Grep: pickle\.load
Grep: torch\.load
Grep: joblib\.load
Grep: np\.load\(.*allow_pickle
Grep: dill\.load
Grep: cloudpickle
Grep: shelve\.open
Grep: yaml\.load\(.*Loader
Grep: marshal\.load
```

**Critical Risk:** Pickle and related deserializers execute arbitrary code during loading.

Check:
- `pickle.load()` on untrusted or user-supplied files → **Critical: RCE**
- `torch.load()` without `weights_only=True` (PyTorch < 2.0 default is unsafe)
- `joblib.load()` on user-uploaded model files
- `np.load(..., allow_pickle=True)` on untrusted data
- `yaml.load()` without `SafeLoader`
- Models loaded from user-controlled paths or URLs without integrity checks
- No model file signature verification

**Safe alternatives:**
- Use `safetensors` format instead of pickle-based formats
- `torch.load(..., weights_only=True)` for PyTorch 2.0+
- `yaml.safe_load()` instead of `yaml.load()`

---

## Category 2: LLM & Prompt Injection

```
Grep: (openai|anthropic|cohere)\.(chat|complete|messages)
Grep: ChatCompletion\.create
Grep: messages\.create
Grep: langchain|LLMChain|ConversationChain
Grep: PromptTemplate
Grep: f".*\{.*user.*\}.*".*prompt
Grep: system.*prompt.*=
```

Check:
- User input directly concatenated into system prompts (prompt injection)
- Missing input sanitization before LLM calls
- LLM output executed as code or shell commands (indirect injection → RCE)
- LLM output used in SQL queries, file paths, or URLs without validation
- System prompts containing secrets, API keys, or internal instructions
- No output filtering for sensitive data in LLM responses
- Tool/function calling with user-controlled function names or arguments
- RAG pipelines ingesting untrusted documents (indirect prompt injection)

**Prompt injection patterns:**
```
Grep: \.format\(.*user
Grep: f".*{.*input.*}
Grep: prompt.*\+.*user
Grep: template.*render.*user
```

---

## Category 3: API Key & Credential Exposure

```
Grep: (OPENAI|ANTHROPIC|COHERE|HUGGING_FACE|HF)_(API_KEY|TOKEN|SECRET)
Grep: sk-[a-zA-Z0-9]{20,}
Grep: api[_-]?key.*=.*['"][a-zA-Z0-9]
Grep: bearer.*token
```

Check:
- LLM API keys hardcoded in source files
- API keys in notebook cells (`.ipynb` outputs may persist in git)
- `.env` files committed with API keys
- API keys logged during model calls
- Keys in Docker build arguments or layers
- Missing key rotation or per-environment key separation

---

## Category 4: Model Supply Chain

```
Grep: from_pretrained\(
Grep: hub\.load
Grep: transformers.*download
Grep: huggingface|hf_hub
Grep: model_name.*=
```

Check:
- Models downloaded from untrusted sources without hash verification
- `from_pretrained()` with user-controlled model name (arbitrary model loading)
- No pinned model versions (vulnerable to model poisoning)
- Custom model repos without integrity verification
- Missing model provenance tracking
- Pre-trained models from unverified community sources

---

## Category 5: Data Pipeline Security

```
Grep: pd\.read_(csv|json|excel|sql|pickle|parquet)
Grep: spark\.read
Grep: boto3.*s3.*get_object
Grep: requests\.get.*\.json\(\)
Grep: urllib.*urlopen
```

Check:
- Data loaded from user-controlled URLs or file paths
- SQL queries constructed from pipeline parameters without parameterization
- Sensitive training data accessible without access controls
- PII in training datasets without anonymization
- Data pipeline credentials hardcoded
- Missing input validation on data pipeline parameters
- CSV/Excel parsing with formulas that execute code

---

## Category 6: Model Serving & API Security

```
Grep: @app\.(get|post).*predict
Grep: @app\.(get|post).*inference
Grep: @app\.(get|post).*generate
Grep: /api.*(model|predict|infer|generate|embed|complete)
```

Check:
- Model inference endpoints without authentication
- No rate limiting on inference endpoints (resource exhaustion / cost)
- Missing input size limits (large inputs causing OOM)
- Model output returned without sanitization
- No input validation on tensor shapes or data types
- Batch inference allowing unbounded batch sizes
- Missing request timeout on inference calls
- Model version not pinned in serving config

---

## Category 7: Notebook Security

```
Glob: **/*.ipynb
```

Check:
- Executed notebook outputs containing API keys, tokens, or secrets
- Database connection strings in notebook cells
- Notebooks with `!pip install` or `!apt-get` (supply chain risk)
- Sensitive data (PII, credentials) in cell outputs committed to git
- Notebooks running as root or with elevated privileges
- Magic commands executing system commands with user input

---

## Category 8: Training & Fine-Tuning Risks

```
Grep: \.train\(
Grep: \.fit\(
Grep: Trainer\(
Grep: training_args
Grep: fine.?tun
```

Check:
- Training data poisoning vectors (user-contributed training data without validation)
- Checkpoint files in pickle format (deserialization risk)
- Training scripts with hardcoded credentials for data access
- Model artifacts stored in world-readable locations
- Missing reproducibility controls (no seed, no version tracking)
- Gradient/weight logging exposing training data

---

## Common False Positive Filters

- `pickle.load` in test fixtures with controlled test data → lower risk
- `torch.load` with `weights_only=True` → safe
- API keys loaded from environment variables (not hardcoded) → not a source code finding
- `from_pretrained("gpt2")` with well-known model names → lower supply chain risk (but note)
- Notebook outputs cleared before commit → not a data leak
