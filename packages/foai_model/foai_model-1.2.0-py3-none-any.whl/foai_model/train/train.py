import os
import pickle
from pathlib import Path
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
)
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
)
from foai_model.config import MODEL_NAME
from foai_model.logger import logger
from foai_model.file_reader import read_datasets
from foai_model.preprocessing import clean_dataset
from foai_model.utils import log_device_info

MODEL_PATH = Path("model")
os.makedirs(MODEL_PATH, exist_ok=True)


def prepare_data():
    logger.info("Reading raw datasets...")
    df = read_datasets()

    logger.info("Cleaning and preprocessing data...")
    df, dataset, label_encoder = clean_dataset(df)

    logger.info(
        "Data preparation completed. Train size: %d, Test size: %d",
        len(dataset["train"]),
        len(dataset["test"]),
    )

    encoder_path = MODEL_PATH / "checkpoint-latest" / "label_encoder.pkl"
    with open(encoder_path, "wb") as f:
        pickle.dump(label_encoder, f)

    logger.info("LabelEncoder saved to: %s", encoder_path)

    return [df, dataset, label_encoder]


def initialize_bert(df):
    if "labels" not in df.columns:
        logger.error("Column 'labels' not found in dataset.")
        raise ValueError("Missing 'labels' column in dataset")

    num_labels = df["labels"].nunique()
    logger.info("Initializing BERT with %d label(s).", num_labels)

    model = AutoModelForSequenceClassification.from_pretrained(
        pretrained_model_name_or_path=MODEL_NAME, num_labels=num_labels
    )

    logger.info("BERT model '%s' initialized successfully.", MODEL_NAME)

    return model


def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = logits.argmax(axis=-1)

    return {
        "accuracy": accuracy_score(labels, predictions),
        "precision": precision_score(
            labels, predictions, average="weighted", zero_division=0
        ),
        "recall": recall_score(
            labels, predictions, average="weighted", zero_division=0
        ),
        "f1": f1_score(labels, predictions, average="weighted", zero_division=0),
    }


def train(dataset, model, label_encoder):
    logger.info("Initializing training configuration...")

    training_args = TrainingArguments(
        output_dir=MODEL_PATH,
        eval_strategy="epoch",
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=4,
        weight_decay=0.01,
        logging_dir=MODEL_PATH / "logs",
        logging_steps=10,
        save_strategy="epoch",
    )

    logger.info("TrainingArguments:")
    logger.info("- Output dir: %s", training_args.output_dir)
    logger.info("- Epochs: %d", training_args.num_train_epochs)
    logger.info(
        "- Batch size (train/eval): %d", training_args.per_device_train_batch_size
    )
    logger.info("- Evaluation strategy: %s", training_args.eval_strategy)
    logger.info("- Logging dir: %s", training_args.logging_dir)

    logger.info("Creating Trainer instance...")

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset["train"],
        eval_dataset=dataset["test"],
        compute_metrics=compute_metrics,
    )

    logger.info("Starting training...")
    trainer.train()
    logger.info("Training complete. Model saved to output directory.")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokenizer.save_pretrained(MODEL_PATH / "checkpoint-latest")

    trainer.save_model(MODEL_PATH / "checkpoint-latest")

    logger.info("Tokenizer and model saved to: %s", MODEL_PATH / "checkpoint-latest")

    predictions = trainer.predict(dataset["test"])
    y_pred = predictions.predictions.argmax(axis=-1)
    y_true = predictions.label_ids

    logger.info(
        classification_report(y_true, y_pred, target_names=label_encoder.classes_)
    )


def main():
    logger.info("=== Starting training pipeline ===")
    log_device_info()
    df, dataset, label_encoder = prepare_data()
    model = initialize_bert(df)
    train(dataset, model, label_encoder)
    logger.info("=== Training pipeline completed ===")


if __name__ == "__main__":
    main()
