import argparse
import pickle
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from huggingface_hub import hf_hub_download
import nltk

from foai_model.config import MAX_TOKEN_LENGTH
from foai_model.logger import logger
from foai_model.preprocessing import clean_resume

nltk.download('punkt_tab')

REPO_ID = "Dar3cz3Q/foai_model"
SUBFOLDER = "checkpoint"

logger.info("Loading tokenizer and model from HuggingFace hub...")
tokenizer = AutoTokenizer.from_pretrained(REPO_ID, subfolder=SUBFOLDER)
model = AutoModelForSequenceClassification.from_pretrained(REPO_ID, subfolder=SUBFOLDER)
model.eval()
device = torch.device("cpu")
model.to(device)
logger.info("Model loaded and moved to CPU.")

encoder_path = hf_hub_download(
    repo_id=REPO_ID, filename="label_encoder.pkl", subfolder=SUBFOLDER
)

with open(encoder_path, "rb") as f:
    label_encoder = pickle.load(f)

index_to_label = dict(enumerate(label_encoder.classes_))
logger.info("Label encoder loaded: %s", index_to_label)

def predict(text):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=MAX_TOKEN_LENGTH,
    )

    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        logits = model(**inputs).logits
        probs = torch.nn.functional.softmax(logits, dim=1).squeeze().cpu().numpy()

    category_distribution = {
        label: round(float(probs[idx]) * 100, 2)
        for idx, label in index_to_label.items()
    }

    predicted_class_id = int(torch.argmax(logits, dim=1).item())
    predicted_label = index_to_label[predicted_class_id]

    return {
        "predicted_id": predicted_class_id,
        "predicted_category": predicted_label,
        "category_distribution": category_distribution
    }


def main():
    parser = argparse.ArgumentParser(
        description="Predict category distribution from text."
    )
    parser.add_argument("--text", type=str, required=True, help="Text to classify")

    args = parser.parse_args()
    resume = clean_resume(args.text)
    result = predict(resume)

    print("Result:", result)


if __name__ == "__main__":
    main()
