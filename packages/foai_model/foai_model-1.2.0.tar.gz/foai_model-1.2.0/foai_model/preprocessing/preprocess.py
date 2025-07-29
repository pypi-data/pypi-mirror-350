import re
from datasets import Dataset
from transformers import AutoTokenizer
from sklearn.preprocessing import LabelEncoder

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

from foai_model.config import MODEL_NAME, MAX_TOKEN_LENGTH, TEST_SPLIT_SIZE
from foai_model.logger import logger
from .categories import CATEGORY_MAPPING

nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)

stop_words = set(stopwords.words("english"))


def clean_resume(text):
    logger.debug("Cleaning resume text...")
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = re.sub(r"\S+@\S+", "", text)
    text = re.sub(r"\+?\d[\d -]{8,}\d", "", text)
    text = re.sub(r"\n", " ", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words]

    return " ".join(tokens)


def simplify_category(category):
    for group, values in CATEGORY_MAPPING.items():
        if category in values:
            logger.debug("Mapping category '%s' to group '%s'", category, group)
            return group
    logger.debug("No mapping found for category '%s', keeping as is.", category)
    return category


def tokenize_categories(df):
    label_encoder = LabelEncoder()
    df["labels"] = label_encoder.fit_transform(df["Category"])
    logger.info("Encoded categories into %d label(s)", df["labels"].nunique())
    return [df, label_encoder]


def clean_dataset(df):
    logger.info("Starting dataset cleaning and tokenization pipeline...")

    original_shape = df.shape
    df = df.dropna()
    logger.info(
        "Dropped %d rows with NaN values (from %s to %s)",
        original_shape[0] - df.shape[0],
        original_shape,
        df.shape,
    )

    logger.info("Simplifying category labels...")
    df["Category"] = df["Category"].apply(simplify_category)

    logger.info("Encoding category labels...")
    df, label_encoder = tokenize_categories(df)

    logger.info("Cleaning resume texts...")
    df["Resume"] = df["Resume"].apply(clean_resume)

    logger.info("Converting DataFrame to Hugging Face Dataset...")
    dataset = Dataset.from_pandas(df[["Resume", "labels"]])
    logger.info("Converted to Dataset with %d total records.", len(dataset))

    logger.info("Splitting dataset into train/test sets...")
    dataset = dataset.train_test_split(test_size=TEST_SPLIT_SIZE)
    logger.info(
        "Train size: %d, Test size: %d",
        len(dataset["train"]),
        len(dataset["test"]),
    )

    logger.info("Tokenizing resume texts...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    tokenized_dataset = dataset.map(
        lambda e: tokenizer(
            e["Resume"],
            truncation=True,
            padding="max_length",
            max_length=MAX_TOKEN_LENGTH,
        )
    )
    logger.info("Finished tokenization.")

    logger.info("Dataset cleaning and tokenization pipeline completed.")
    return [df, tokenized_dataset, label_encoder]
