# HIP — the base-model regeneration pass

The deepest lever in `write-human`. Instead of editing the surface style, it
regenerates the text through a **base model** (non-instruction-tuned), which
lacks the instruction-tuning / RLHF fingerprints that detectors track. This is
the "Humanization by Iterative Paraphrasing" approach the detector research
recommends; the rest of the skill (voice, rhythm, self-audit) runs on top of it.

## Why a base model, and why local

Commercial models (ChatGPT, Claude, Gemini) are instruction-tuned and RLHF'd —
their output carries exactly the artifacts detectors flag. Base models do not.
No cloud API serves base models, so this pass must run locally.

## Model

`Qwen3-8B-Base`, quant `Q4_K_M` (~5.0 GB). 8B base model, ungated, the
"Qwen-3-Base" family the research names. Sized for a 16 GB Apple-Silicon Mac.

Source: `mradermacher/Qwen3-8B-Base-GGUF` → `Qwen3-8B-Base.Q4_K_M.gguf`.

## Setup (once)

```bash
# 1. download the GGUF (~5 GB)
mkdir -p ~/models/write-human
curl -L -C - -o ~/models/write-human/Qwen3-8B-Base.Q4_K_M.gguf \
  "https://huggingface.co/mradermacher/Qwen3-8B-Base-GGUF/resolve/main/Qwen3-8B-Base.Q4_K_M.gguf"

# 2. import into Ollama as a raw (no chat-template) model
cat > ~/models/write-human/Modelfile <<'EOF'
FROM /Users/sarthhakkaluuchaa/models/write-human/Qwen3-8B-Base.Q4_K_M.gguf
TEMPLATE "{{ .Prompt }}"
EOF
ollama create qwen3-8b-base -f ~/models/write-human/Modelfile

# 3. sanity check (raw completion, not chat)
ollama run qwen3-8b-base "The quick brown fox"
```

## Usage

```bash
python3 scripts/hip.py input.txt > output.txt          # 2 passes, 200-word chunks
python3 scripts/hip.py input.txt --passes 3            # more passes = more paraphrase
cat input.txt | python3 scripts/hip.py - --temp 1.0    # higher temp = more varied
```

Sampling defaults: temperature 0.9, top_p 0.95, top_k 40, repeat_penalty 1.1.
Base models need higher temperature than instruct models to sound natural.

## Honest tradeoffs

- **Faithfulness.** A base model is a paraphraser, not a faithful editor — it
  can drift a fact or drop a detail. Run the voice / self-audit pass from
  `SKILL.md` afterwards, and restore any lost specifics from the draft.
- **Detector claim, tested: does not hold on Clever.** A 2-pass Qwen3-8B-Base
  run scored 97% AI on Clever — statistically identical to instruction-tuned
  rewrites (97-99%). The "base models read as human" finding was measured against
  GPTZero and Pangram, not Clever, and did not reproduce here. See `evals/hip/`.
  Do not sell this as a detector-beater.
- **Quality varies.** Base-model paraphrases can be uneven; chunk size, passes,
  and temperature are the tuning knobs.
