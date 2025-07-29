# TrainLoop Evals SDK (Python)

Automatically capture LLM calls from Python apps so they can be graded later.

## Install

```bash
pip install trainloop-evals-sdk
```

## Quick example

```python
from trainloop_evals import collect, trainloop_tag
collect()  # patch HTTP clients
openai.chat.completions.create(..., trainloop_tag("my-tag"))
```

Set `TRAINLOOP_DATA_FOLDER` to choose where event files are written.

See the [project README](../../README.md) for more details.
