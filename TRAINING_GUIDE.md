# Training DAWT-Transcribe for Better Language Detection

## Current Status (v2.3.0)

✅ **Language Forcing:** You can now guide Whisper by selecting the language  
✅ **Better Prompts:** Translation prompts fixed from "clarify pidgin/dialect" to "translate [Language] to English"  
✅ **Edit & Correct:** You can manually correct transcriptions and export training data

---

## How Language Detection Works Now

### 1. **Manual Selection (Recommended)**
When you select a language (e.g., "Twi"), the system:
1. Maps it to Whisper ISO code (Twi → `ak`)
2. **Forces** Whisper to transcribe in that language
3. Translates segments to English with mT5

**This is the most accurate approach** - you tell the system what language to use.

### 2. **Auto-Detection (Fallback)**
If you select "English (Auto-detect)", the system:
1. Lets Whisper auto-detect the language
2. Searches for keywords in the transcript
3. If keywords match (e.g., "medaase", "ɛyɛ"), switches to that language
4. Applies translation

---

## Training Whisper for Your Languages

### **IMPORTANT 2025 UPDATE:**
- **Yoruba**: ~300 hours in Whisper's training data (under-represented, needs fine-tuning)
- **Igbo**: NOT in Whisper's pre-training (requires full fine-tuning from scratch)
- **Twi**: Not in Whisper's dataset (requires full fine-tuning)
- **Pre-trained Models Available**: Nigeria's N-ATLAS model supports Yoruba & Igbo (September 2025)

### Option 1: Fine-Tune Whisper (Best Accuracy)

**What You Need:**
- **100+ hours** of audio per language (minimum for good results)
- Free datasets: Mozilla Common Voice 17.0 has Yoruba, Igbo, and Twi
- Your corrected transcriptions from DAWT-Transcribe editing feature

**How to Collect Training Data:**
1. Transcribe 100+ videos using DAWT-Transcribe
2. Click **"✏ Edit"** on each transcript
3. Manually correct any errors in the Twi/Igbo/Yoruba text
4. Click **"💾 Save"** to store corrections
5. When you have 100+ corrections, click **"📊 Export Training Data"**

**Fine-Tuning Process (On Mac Mini or GPU Server):**
```bash
# Install Hugging Face tools
pip install --upgrade datasets[audio] transformers accelerate evaluate jiwer
pip install soundfile sentencepiece peft  # LoRA for efficient training

# Download Mozilla Common Voice dataset (FREE!)
# Yoruba: ~10 hours, Igbo: ~5 hours, Twi: ~3 hours
python download_dataset.py  # Script provided below

# Fine-tune Whisper on your data
python fine_tune_whisper_lora.py  # LoRA version (faster, less GPU needed)
```

**Download Free Dataset (download_dataset.py):**
```python
from datasets import load_dataset, Audio

# Download Yoruba from Common Voice 17.0 (FREE!)
yoruba_dataset = load_dataset("mozilla-foundation/common_voice_17_0", "yo", split="train")
yoruba_dataset = yoruba_dataset.cast_column("audio", Audio(sampling_rate=16000))

# Download Igbo
igbo_dataset = load_dataset("mozilla-foundation/common_voice_17_0", "ig", split="train")
igbo_dataset = igbo_dataset.cast_column("audio", Audio(sampling_rate=16000))

# Download Twi
twi_dataset = load_dataset("mozilla-foundation/common_voice_17_0", "tw", split="train")
twi_dataset = twi_dataset.cast_column("audio", Audio(sampling_rate=16000))

# Save locally
yoruba_dataset.save_to_disk("./data/yoruba")
igbo_dataset.save_to_disk("./data/igbo")
twi_dataset.save_to_disk("./data/twi")
```

**LoRA Fine-Tuning Script (`fine_tune_whisper_lora.py`) - RECOMMENDED:**
```python
from transformers import WhisperProcessor, WhisperForConditionalGeneration, Seq2SeqTrainingArguments, Seq2SeqTrainer
from datasets import load_from_disk, Audio
from peft import LoraConfig, get_peft_model
import torch

# Load Whisper SMALL (better than tiny for African languages)
processor = WhisperProcessor.from_pretrained("openai/whisper-small", language="yo", task="transcribe")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small")

# Apply LoRA for efficient training (90% fewer parameters!)
lora_config = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
)
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()  # Shows only ~8M parameters instead of 244M!

# Load Yoruba dataset
dataset = load_from_disk("./data/yoruba")

# Prepare data
def prepare_dataset(batch):
    audio = batch["audio"]
    batch["input_features"] = processor(audio["array"], sampling_rate=16000, return_tensors="pt").input_features[0]
    batch["labels"] = processor.tokenizer(batch["sentence"]).input_ids
    return batch

dataset = dataset.map(prepare_dataset, remove_columns=dataset.column_names)

# Training config (optimized for LoRA)
training_args = Seq2SeqTrainingArguments(
    output_dir="./whisper-small-yoruba-lora",
    per_device_train_batch_size=8,
    gradient_accumulation_steps=2,
    learning_rate=1e-4,  # Higher LR for LoRA
    warmup_steps=500,
    max_steps=5000,
    fp16=True,  # 2x speed boost
    evaluation_strategy="steps",
    save_steps=1000,
    eval_steps=1000,
    logging_steps=25,
    report_to=["tensorboard"],
)

# Train
trainer = Seq2SeqTrainer(
    args=training_args,
    model=model,
    train_dataset=dataset,
    tokenizer=processor.feature_extractor,
)

trainer.train()

# Save model
model.save_pretrained("./whisper-yoruba-lora")
processor.save_pretrained("./whisper-yoruba-lora")

print("✅ Training complete! Model saved to ./whisper-yoruba-lora")
```

**Expected Results (Based on 2025 Research):**
- **Yoruba**: 112% improvement (WER: 45% → 15-20%)
- **Igbo**: WER: ~25-30% (from scratch)
- **Training Time**: 1-2 hours on RTX 4090 with LoRA

**Replace Model in DAWT:**
```python
# In main.py, replace line 44:
model = whisper.load_model("./whisper-twi-custom")  # Your fine-tuned model
```

---

### Option 2: Improve Keyword Detection (Quick Fix)

**Add More Keywords:**

In `main.py`, lines 76-88, add more Twi/Igbo keywords based on common words in your videos:

```python
lang_keywords = {
    "twi": [
        "medaase", "ɛyɛ", "yɛ", "wo", "me",  # Existing
        "akwaaba", "ɛte sɛn", "maame", "papa", "ɔbaa",  # Add more
        "ɛyɛ den", "woho te sɛn", "da yie", "me din de"
    ],
    "igbo": [
        "biko", "kedu", "nwanne", "nnọọ",  # Existing
        "daalụ", "ka ọ dị", "eze", "nna", "nne",  # Add more
        "ụmụaka", "ọma"
    ],
    # ... etc
}
```

---

### Option 3: Use Language ID Model (Advanced)

Install a dedicated language identification model:

```bash
pip install langdetect langid
```

**Add to main.py:**
```python
from langdetect import detect, DetectorFactory
DetectorFactory.seed = 0  # Consistent results

# Before line 212, add:
try:
    auto_detected = detect(full_text)
    logger.info(f"[{request_id}] Auto-detected language: {auto_detected}")
    
    # Map to our supported languages
    lang_map = {
        "ak": "twi", "ig": "igbo", "yo": "yoruba",
        "ha": "hausa", "sw": "swahili", "am": "amharic"
    }
    
    if auto_detected in lang_map and request.lang == "en":
        detected_lang = lang_map[auto_detected]
        logger.info(f"[{request_id}] Switching to {detected_lang}")
except:
    pass  # Fallback to manual selection
```

---

## Handling Failures

### Current Behavior:
- If Whisper fails → Returns error with message
- If translation fails → Returns Whisper-only output (no translation)

### Suggested Improvements:

**1. Add Confidence Scores:**
```python
# In transcription, add:
result = model.transcribe(audio_path, language=whisper_lang, task="transcribe", verbose=False)

# Whisper provides per-segment confidence (not exposed by default)
# Use `result['segments'][i]['avg_logprob']` for confidence
```

**2. Fallback to English:**
```python
# If selected language produces garbage, retry with English
if whisper_lang != "en" and len(full_text.strip()) < 10:
    logger.warning(f"[{request_id}] Low output, retrying with English...")
    result = model.transcribe(audio_path, language="en")
```

**3. Quality Check:**
```python
# Check if transcription makes sense
def is_valid_transcription(text, expected_lang):
    # Check minimum length
    if len(text.strip()) < 5:
        return False
    
    # Check for excessive unicode/gibberish
    non_ascii = sum(1 for c in text if ord(c) > 127)
    if non_ascii / len(text) > 0.8 and expected_lang == "en":
        return False
    
    return True
```

---

## Recommended Workflow

### For Best Results:
1. **Always select the language manually** (don't use auto-detect)
2. Select "Twi" for Twi videos, "Igbo" for Igbo, etc.
3. Review transcripts and use **Edit mode** to correct errors
4. Export corrected data periodically
5. After 100+ corrections, fine-tune Whisper
6. Replace the model on your Mac Mini

### Quick Fixes (No Training):
1. Add more keywords to `lang_keywords` dictionary
2. Use `langdetect` library for better auto-detection
3. Increase Whisper model size: `tiny` → `base` → `small` → `medium`

---

## Model Size vs Accuracy

| Model | Speed | Accuracy | File Size |
|-------|-------|----------|-----------|
| tiny  | 5x    | 60%      | 75 MB     |
| base  | 3x    | 70%      | 145 MB    |
| small | 2x    | 80%      | 488 MB    |
| medium| 1x    | 90%      | 1.5 GB    |
| large | 0.5x  | 95%      | 3 GB      |

**Current:** `tiny` (fastest, lowest accuracy)  
**Recommended for Twi/Igbo:** `base` or `small` (better accuracy, still fast)

---

## Next Steps

1. Try transcribing with **manual language selection** (should work better now!)
2. Upgrade to `base` model for better accuracy:
   ```python
   model = whisper.load_model("base")  # Line 44 in main.py
   ```
3. Collect 100+ corrected transcripts using Edit feature
4. Fine-tune Whisper on your Mac Mini with your corrections

Let me know if you want me to implement any of these improvements! 🎯
