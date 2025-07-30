This is a collection of utility functions and decorators that can be used in various projects.

## 1\. Utility Decorators

This module provides a collection of useful decorators for caching, disk-based caching, and retrying function executions.

**How to Import:**

`from utility_pack.decorators import <DecoratorName>`

---

### `timed_lru_cache`

Caches function results in memory with a time-based expiration and LRU eviction policy.

```python
from utility_pack.decorators import timed_lru_cache
import time

@timed_lru_cache(max_size=2, minutes=5)  # Max 2 items, expire after 5 minutes
def expensive_operation(arg):
    print("Calculating...")
    time.sleep(1)  # Simulate a slow operation
    return arg * 2

print(expensive_operation(5))  # Calculates and prints 10
print(expensive_operation(5))  # Returns cached result (10) immediately
```

### `disk_lru_cache`

Caches function results to disk using a LRU eviction policy. This is useful for persisting results across multiple program invocations or in situations where in-memory caching is insufficient. Note that the function's return value MUST be pickleable.  
The disk caching implementation relies on `cloudpickle`, allowing for a wider range of Python objects (including lambdas, functions, and classes) to be serialized and cached, which the standard `pickle` module does not support.

```python
from utility_pack.decorators import disk_lru_cache
import os

@disk_lru_cache(max_size=2, cache_file="my_cache.pkl")
def another_expensive_operation(arg):
    print("Calculating from Disk...")
    return arg * 3

print(another_expensive_operation(4))  # Calculates and prints 12, saves to disk
print(another_expensive_operation(4))  # Retrieves from disk cache (12)
os.remove("my_cache.pkl") #cleanup
```

---

### `retry`

Retries a function execution a specified number of times if it raises an exception.

```python
from utility_pack.decorators import retry

@retry(retry_count=3, delay=0.5) # Retry thrice, delayed 0.5 seconds between attempts
def flaky_function():
    import random
    if random.random() < 0.5:
        raise ValueError("Something went wrong!")
    return "Success!"

print(flaky_function())
```

## 2\. Embeddings

### `utility_pack.embeddings` Module

This module provides functionalities for extracting text embeddings using different methods. It includes options for both textual (character-based n-grams) and semantic (ONNX transformer model based) embeddings.

To import the functionalities, use the following pattern: `from utility_pack.embeddings import <function_or_class_name>`

### `extract_embeddings` Function

This function is the main entry point for extracting embeddings. It takes a list of texts and an optional `embedding_type` argument to specify the desired embedding method.

```python
from utility_pack.embeddings import extract_embeddings, EmbeddingType

texts = ["This is a sample text.", "Another sample text."]

# Example: Extracting textual embeddings
textual_embeddings = extract_embeddings(texts, embedding_type=EmbeddingType.TEXTUAL)
print(f"Textual embeddings shape: {len(textual_embeddings), len(textual_embeddings[0])}")

# Example: Extracting semantic embeddings
semantic_embeddings = extract_embeddings(texts, embedding_type=EmbeddingType.SEMANTIC)
print(f"Semantic embeddings shape: {len(semantic_embeddings), len(semantic_embeddings[0])}")
```

**Parameters:**

*   `texts`: A list of strings to be embedded.
*   `embedding_type`: An `EmbeddingType` enum value specifying the desired embedding method (default: `EmbeddingType.TEXTUAL`).

**Returns:**

A list of embeddings represented as lists of floats. The format depends on the `embedding_type`.

## `Textual Embeddings` using HashingVectorizer

Implements character-based n-gram embeddings using scikit-learn's `HashingVectorizer`.

```python
from utility_pack.embeddings import extract_embeddings, EmbeddingType

texts = ["Simple and short text.", "Another short sample."]
textual_embeddings = extract_embeddings(texts, embedding_type=EmbeddingType.TEXTUAL)
print(f"Textual embeddings for short texts: {len(textual_embeddings), len(textual_embeddings[0])}")
```

## `Semantic Embeddings` using ONNX Transformer Model

Leverages a pre-trained ONNX transformer model to generate semantic embeddings. It uses a provided tokenizer to tokenize the input text and utilizes the ONNX runtime for inference. It first compresses the text (if longer than 500 tokens) with `compress_text` and then feeds to the transformer model.

```python
from utility_pack.embeddings import extract_embeddings, EmbeddingType

texts = ["A longer sentence for semantic analysis.", "Another example of a moderately long sentence."]
semantic_embeddings = extract_embeddings(texts, embedding_type=EmbeddingType.SEMANTIC)
print(f"Semantic embeddings for moderately long sentences {len(semantic_embeddings), len(semantic_embeddings[0])}")  #  len(semantic_embeddings) equal total texts.
```

## 3\. Interact with LLMs using several providers

## utility\_pack.llm

This module provides a set of functions for interacting with various Large Language Models (LLMs) including OpenRouter, Ollama, and vLLM. It also includes utilities for text compression, question classification, and passage re-ranking.

To import this module:

```python
from utility_pack.llm import <Function Name>
```

### OpenRouter Chat (Non-Streaming)

Sends a chat message to OpenRouter's API and returns the complete response. Requires the `OPENROUTER_KEY` environment variable to be set.

```python
messages = [
    {"role": "user", "content": "What is the capital of France?"}
]
response = openrouter_chat(messages)
print(response)
```

### OpenRouter Prompt (Non-Streaming)

Sends a single prompt to OpenRouter's API and returns the complete response. Requires the `OPENROUTER_KEY` environment variable to be set.

```python
response = openrouter_prompt("Tell me a joke.")
print(response)
```

### OpenRouter Chat (Streaming)

Streams chunks of the response from OpenRouter's API. Requires the `OPENROUTER_KEY` environment variable to be set..

```python
import asyncio

async def example():
    messages = [{"role": "user", "content": "Write a short story about a cat."}]
    async for chunk in openrouter_chat_stream(messages):
        print(chunk, end="")

asyncio.run(example())
```

### OpenRouter Prompt (Streaming)

Streams chunks of the response from OpenRouter's API for a single prompt. Requires the `OPENROUTER_KEY` environment variable to be set.

```python
import asyncio

async def example():
    async for chunk in openrouter_prompt_stream("Describe the solar system"):
        print(chunk, end="")

asyncio.run(example())
```

### Ollama Chat (Non-Streaming)

Sends a chat message to an Ollama instance and returns the complete response. Requires the `OLLAMA_HOST` environment variable to be set.

```python
messages = [
    {"role": "user", "content": "What is 2 + 2?"}
]
response = ollama_chat(messages)
print(response)
```

### Ollama Prompt (Non-Streaming)

Sends a single prompt to an Ollama instance and returns the complete response. Requires the `OLLAMA_HOST` environment variable to be set.

```python
response = ollama_prompt("Summarize Moby Dick in one sentence.")
print(response)
```

### Ollama Chat (Streaming)

Streams chunks of the response from an Ollama instance. Requires the `OLLAMA_HOST` environment variable to be set.

```python
import asyncio

async def example():
    messages = [{"role": "user", "content": "Explain the theory of relativity."}]
    async for chunk in ollama_chat_stream(messages):
        print(chunk, end="")

asyncio.run(example())
```

### Ollama Prompt (Streaming)

Streams chunks of the response from an Ollama instance for a single prompt. Requires the `OLLAMA_HOST` environment variable to be set.

```python
import asyncio

async def example():
    async for chunk in ollama_prompt_stream("Write a poem about the ocean."):
        print(chunk, end="")

asyncio.run(example())
```

### vLLM Chat (Non-Streaming)

Sends a chat message to a vLLM instance and returns the complete response. Requires the `VLLM_URL` and `VLLM_KEY` environment variables to be set.

```python
messages = [
    {"role": "user", "content": "Translate 'Hello, world!' to French."}
]
response = vllm_chat(messages)
print(response)
```

### vLLM Prompt (Non-Streaming)

Sends a single prompt to a vLLM instance and returns the complete response. Requires the `VLLM_URL` and `VLLM_KEY` environment variables to be set.

```python
response = vllm_prompt("Give me three reasons why Python is a popular programming language.")
print(response)
```

### vLLM Chat (Streaming)

Streams chunks of the response from a vLLM instance. Requires the `VLLM_URL` and `VLLM_KEY` environment variables to be set.

```python
import asyncio

async def example():
    messages = [{"role": "user", "content": "Describe the benefits of using AI in healthcare."}]
    async for chunk in vllm_chat_stream(messages):
        print(chunk, end="")

asyncio.run(example())
```

### vLLM Prompt (Streaming)

Streams chunks of the response from a vLLM instance for a single prompt. Requires the `VLLM_URL` and `VLLM_KEY` environment variables to be set.

```python
import asyncio

async def example():
    async for chunk in vllm_prompt_stream("Explain the concept of blockchain technology."):
        print(chunk, end="")

asyncio.run(example())
```

### Classify Question (Generic or Directed)

Classifies a question as either "generic" or "directed" using a pre-trained ONNX model.

```python
question = "What is the meaning of life?"
classification = classify_question_generic_or_directed(question)
print(f"The question is classified as: {classification}")
```

### Passage Re-ranking

Re-ranks a list of passages based on their relevance to a given question using a pre-trained ONNX model.

```python
question = "What are the benefits of exercise?"
passages = [
    "Exercise improves cardiovascular health.",
    "Eating a balanced diet is important for overall well-being.",
    "Regular exercise can help reduce stress and improve mood."
]
ranked_passages = rerank(question, passages)
for passage, score in ranked_passages:
    print(f"Passage: {passage}, Score: {score}")
```

## 4\. Logging

This module provides utility functions for logging exceptions with detailed information, including date/time in Brasilia time zone, filename, function name, line number, stack trace and parameters.

To import this module:

```python
from utility_pack.logger import get_datetime_brasilia, log_exception
```

### `get_datetime_brasilia()`

Returns the current date and time in the "America/Sao\_Paulo" timezone (Brasilia) formatted as a string.

**Example:**

```python
from utility_pack.logger import get_datetime_brasilia

current_time = get_datetime_brasilia()
print(current_time) # Output: e.g., 20/10/2023 - 15:30:45
```

### `log_exception()`

Logs an exception along with detailed context information - Brasilia datetime, filename, function name, line number, full stack trace and function arguments up to 100 characters. The error message is logged using the Python `logging` module at the ERROR level. This is intended to be called inside an `except` block.

**Example:**

```python
from utility_pack.logger import log_exception

def some_function(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        log_exception()

result = some_function(10, 0)
print(result) # Output (in console): None

# Will print out the exception in high detail automatically
```

## 5\. ML

To import this module:

```python
from utility_pack.ml import *  # Import all functions
# or
from utility_pack.ml import timeseries_forecast, find_high_correlation_features, recommend_items
```

---

### `timeseries_forecast`

Creates a time series forecast using the Prophet model.

**Parameters:**

*   `dates` (list): List of dates. Should be compatible with Prophet's date format.
*   `values` (list): List of corresponding numerical values.
*   `num_forecast_periods` (int, optional): Number of periods to forecast into the future. Defaults to 30.

**Returns:**

*   `list`: A list of forecasted values for the specified number of periods.

**Example:**

```python
from utility_pack.ml import timeseries_forecast
dates = ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05']
values = [10, 12, 15, 13, 17]
forecast = timeseries_forecast(dates, values, num_forecast_periods=7)
print(forecast)
```

---

### `find_high_correlation_features`

Identifies and returns a list of highly correlated features in a DataFrame.

**Parameters:**

*   `df` (pd.DataFrame): The input DataFrame.
*   `categorical_columns` (list): List of categorical column names.
*   `ignore_columns` (list): List of columns to ignore.
*   `threshold` (float, optional): The correlation threshold. Columns with correlation above this value are returned. Defaults to 0.9.

**Returns:**

*   `list`: A list of column names that are highly correlated with other columns.

**Example:**

```python
import pandas as pd
from utility_pack.ml import find_high_correlation_features

data = {'col1': [1, 2, 3, 4, 5], 'col2': [2, 4, 6, 8, 10], 'col3': ['A', 'B', 'A', 'C', 'B']}
df = pd.DataFrame(data)
categorical_cols = ['col3']
ignore_cols = []
high_corr_features = find_high_correlation_features(df, categorical_cols, ignore_cols, threshold=0.95)
print(high_corr_features)
```

---

### `prepare_dataframe_to_ml`

Prepares a DataFrame for machine learning by handling categorical and numerical features, missing values, high correlation, and dimensionality reduction using `prince`.

**Parameters:**

*   `df` (pd.DataFrame): The input DataFrame.

**Returns:**

*   `pd.DataFrame` or `np.ndarray`: A transformed DataFrame or numpy array ready for machine learning. The return type depends on which `prince` method is used (FAMD, MCA) or if it returns the numerical columns directly.

**Example:**

```python
import pandas as pd
from utility_pack.ml import prepare_dataframe_to_ml

data = {'col1': [1, 2, 3, 4, 5], 'col2': [2.0, 4.0, 6.0, 8.0, 10.0], 'col3': ['A', 'B', 'A', 'C', 'B']}
df = pd.DataFrame(data)
prepared_df = prepare_dataframe_to_ml(df)
print(prepared_df)
```

---

### `recommend_items`

Recommends items to sources using Alternating Least Squares (ALS) matrix factorization.

**Parameters:**

*   `df` (pd.DataFrame): Input DataFrame with 'source', 'item', and 'rating' columns. If 'rating' column is missing then the function will treat all interactions as a positive feedback with rating equals to 1.
*   `num_factors` (int, optional): Number of latent factors. Defaults to 20.
*   `num_iterations` (int, optional): Number of ALS iterations. Defaults to 5.
*   `reg` (float, optional): Regularization parameter. Defaults to 0.1.

**Returns:**

*   `pd.DataFrame`: DataFrame with columns 'source', 'recommended\_item', and 'recommendation\_score'.

**Example:**

```python
import pandas as pd
from utility_pack.ml import recommend_items

data = {'source': ['A', 'A', 'B', 'B', 'C'], 'item': ['X', 'Y', 'X', 'Z', 'Y'], 'rating': [5, 4, 3, 5, 2]}
df = pd.DataFrame(data)
recommendations = recommend_items(df, num_factors=10, num_iterations=3, reg=0.05)
print(recommendations)
```

## 6\. OCR Utility Package

This package provides functions for performing OCR on images, with preprocessing steps for improved accuracy. It includes functionalities for binarization, deskewing, and raw OCR extraction.

To import this module:

```python
from utility_pack.ocr_util import ocr_image_pipeline, raw_ocr_with_topbottom_leftright
```

### `ocr_image_pipeline`

This function performs a complete OCR pipeline on a PIL image. It includes binarization using Sauvola's method, deskewing, and extracting text using Tesseract OCR. It prioritizes processing binarized and deskewed images, falling back on the original image if the initial attempt yields no text. It also performs post-processing to remove extra spaces and newline characters. This is the primary function you'll likely use.

```python
from PIL import Image
from utility_pack.ocr_util import ocr_image_pipeline

# Load the image
image_path = 'path/to/your/image.png'  # Replace with your image path
pil_image = Image.open(image_path)

# Perform OCR
text = ocr_image_pipeline(pil_image)

# Print the extracted text
print(text)
```

### `raw_ocr_with_topbottom_leftright`

This function performs raw OCR extraction on a PIL image or a processed image (like the output of `sauvola_binarization` or `rotate_image`), ordering the text by its position on the page (top to bottom, then left to right). It returns the extracted text as a single string, with each line separated by a newline character. It uses pytesseract's `image_to_data` function to obtain bounding box information and text.

```python
from PIL import Image
from utility_pack.ocr_util import raw_ocr_with_topbottom_leftright

# Load the image
image_path = 'path/to/your/image.png'  # Replace with your image path
pil_image = Image.open(image_path)

# Perform OCR
text = raw_ocr_with_topbottom_leftright(pil_image)

# Print the extracted text
print(text)
```

## 7\. Pandas Parallelization

This function allows you to parallelize a Pandas DataFrame's `apply` operation using multiple processes, significantly speeding up computations on large datasets. It leverages `cloudpickle` to serialize the function, enabling it to be passed between processes safely.

To import this module:

```python
from utility_pack.ocr_util import parallelize_apply
```

### Usage

`**parallelize_apply(df, func, n_jobs=-1)**`

Applies a function to a Pandas DataFrame in parallel.

*   `df`: The Pandas DataFrame to apply the function to.
*   `func`: The function to apply to each chunk of the DataFrame. The function will receive a Pandas DataFrame chunk as input.
*   `n_jobs`: The number of processes to use. `-1` uses all available CPU cores.

```python
import pandas as pd
from utility_pack.ocr_util import parallelize_apply

# Sample DataFrame
data = {'col1': range(100000), 'col2': range(100000, 200000)}
df = pd.DataFrame(data)

# Define a simple function to apply (e.g., square each value in column 'col1')
def square_col1(df_chunk):
    df_chunk['col1_squared'] = df_chunk['col1'] ** 2
    return df_chunk

# Parallelize the apply operation
result_df = parallelize_apply(df.copy(), square_col1, n_jobs=4) # Use 4 processes

# The 'result_df' now contains an additional column 'col1_squared'
print(result_df.head())
```

## 8\. JSON Parser Utility

This utility provides a function to extract and parse JSON data from strings, handling cases where the JSON is encapsulated within triple backticks or exists as a standalone string.

To import this module:

```python
from utility_pack.parsers import find_and_parse_json_from_string
```

---

### Finding and Parsing JSON within Triple Backticks

````python
from utility_pack.parsers import find_and_parse_json_from_string

response_string = """
Some surrounding text.
```json
{
  "name": "example",
  "value": 123
}
```
More surrounding text.  
"""

parsed_json = find_and_parse_json_from_string(response_string)  
print(parsed_json)

## Expected Output: {'name': 'example', 'value': 123}
````

## 9\. PDF to Text Extraction with OCR Strategies

This module provides functionality to extract text from PDF files, with options to control OCR execution based on different strategies. It leverages the `fitz` (PyMuPDF) library for PDF processing and `PIL` for image manipulation and a custom `ocr_image_pipeline` for OCR.

To import this module:

```python
from utility_pack.pdfs import pdf_to_text, OcrStrategy
```

### Extract Text from PDF

The `pdf_to_text` function is the primary entry point for extracting text. It accepts a PDF file path and an OCR strategy to determine when to apply OCR.

```python
from utility_pack.pdfs import pdf_to_text, OcrStrategy

filepath = "path/to/your/pdf_file.pdf"  # Replace with the actual path to your PDF file
result = pdf_to_text(filepath, strategy_ocr=OcrStrategy.Auto)

print(result['full_text'])
```

### OCR Strategies

The `OcrStrategy` Enum defines the available strategies for handling OCR.

*   **Always:** OCR is performed on every page.
*   **Never:** OCR is never performed. Extracts only text that is already vectorized in the PDF (if any).
*   **Auto:** OCR is performed on pages which have less then 10 words already extracted from their vectorized text, or detected as photos.

```python
from utility_pack.pdfs import pdf_to_text, OcrStrategy

filepath = "path/to/your/pdf_file.pdf"

# Example using the 'Always' strategy:
result = pdf_to_text(filepath, strategy_ocr=OcrStrategy.Always)
print(result['full_text'])
```

### Customize Zoom Factor

The `zoom_factor` parameter in `pdf_to_text` and `get_pdf_page_as_image` functions allows customization of the resolution of the converted image before OCR is performed. Higher values means more pixels and potentially better OCR results, at the cost of performance.

```python
from utility_pack.pdfs import pdf_to_text, OcrStrategy

filepath = "path/to/your/pdf_file.pdf"
result = pdf_to_text(filepath, strategy_ocr=OcrStrategy.Auto, zoom_factor=4.0) # Setting zoom to 4.0
print(result['full_text'])
```

### Get a PDF Page as an Image

The `get_pdf_page_as_image` function converts a specific page of a PDF into a PIL image object (via a PixMap object from pymupdf). This allows you to get image representations of specific pdf pages, which are used as inputs to the OCR process.

```python
from utility_pack.pdfs import get_pdf_page_as_image

filepath = "path/to/your/pdf_file.pdf"
page_number = 0 # first page

pix_image = get_pdf_page_as_image(filepath, page_number)
print(type(pix_image))
```

### Determine if a page is a photo

The `is_photo` function determines if a pix\_image contains a photo based on the amount of white pixels.

```python
from utility_pack.pdfs import get_pdf_page_as_image, is_photo

filepath = "path/to/your/pdf_file.pdf"
page_number = 0

pix_image = get_pdf_page_as_image(filepath, page_number)
is_it_a_photo = is_photo(pix_image)
print(is_it_a_photo)
```

## 10\. Text Utilities

This module provides a collection of text processing and utility functions for tasks such as cleaning, compressing, comparing, and chunking text.

### Usage

Import functions and classes as follows:

```python
from utility_pack.text import (
    get_uuid,
    remove_stopwords,
    remove_accents_replace,
    remove_accents_completely,
    remove_special_characters,
    remove_asian_characters,
    remove_html_tags,
    cleanup_markdown,
    remove_extra_whitespace,
    remove_numbers,
    remove_urls,
    remove_emails,
    compress_text,
    StringSimilarity,
    string_similarity,
    string_similarity_from_list,
    find_needle_in_haystack,
    chunk_text
)
```

Here separated single examples of each available module functionality

### `get_uuid`

Generates a short UUID.

```python
from utility_pack.text import get_uuid
unique_id = get_uuid()
print(unique_id)
```

### `remove_stopwords`

Removes common English (default) or Portuguese stopwords from a string.

```python
from utility_pack.text import remove_stopwords
text = "This is an example sentence with some stopwords."
cleaned_text = remove_stopwords(text)
print(cleaned_text)  # Output: example sentence stopwords.
```

### `remove_accents_replace`

Removes accents by replacing accented characters with their base characters.

```python
from utility_pack.text import remove_accents_replace
text = "Êxèmplo çøm áçêntøs."
cleaned_text = remove_accents_replace(text)
print(cleaned_text)  # Output: Exemplo com acentos.
```

### `remove_accents_completely`

Removes accents entirely, deleting accented characters.

```python
from utility_pack.text import remove_accents_completely
text = "Êxèmplo çøm áçêntøs."
cleaned_text = remove_accents_completely(text)
print(cleaned_text)  # Output: Exmplo cm cnts.
```

### `remove_special_characters`

Removes special characters, leaving only alphanumeric characters and spaces.

```python
from utility_pack.text import remove_special_characters
text = "Hello! This is a test@example.com."
cleaned_text = remove_special_characters(text)
print(cleaned_text)  # Output: Hello This is a testexamplecom
```

### `remove_asian_characters`

Removes Asian characters from the given string.

```python
from utility_pack.text import remove_asian_characters
text = "Hello こんにちは 世界"
cleaned_text = remove_asian_characters(text)
print(cleaned_text) # Output: Hello
```

### `remove_html_tags`

Removes HTML tags from a string.

```python
from utility_pack.text import remove_html_tags
text = "<p>This is <b>bold</b> text.</p>"
cleaned_text = remove_html_tags(text)
print(cleaned_text)  # Output: This is bold text.
```

### `cleanup_markdown`

Converts Markdown to plain text by removing Markdown formatting.

```python
from utility_pack.text import cleanup_markdown
text = "# This is a heading\n* This is a list item"
cleaned_text = cleanup_markdown(text)
print(cleaned_text)
# Output:
# This is a heading
# This is a list item
```

### `remove_extra_whitespace`

Removes extra whitespace, leaving only single spaces between words.

```python
from utility_pack.text import remove_extra_whitespace
text = "  This   has   extra    spaces.  "
cleaned_text = remove_extra_whitespace(text)
print(cleaned_text)  # Output: This has extra spaces.
```

### `remove_numbers`

Removes all numeric characters from the string.

```python
from utility_pack.text import remove_numbers
text = "This is a test string with 123 numbers."
cleaned_text = remove_numbers(text)
print(cleaned_text)  # Output: This is a test string with  numbers.
```

### `remove_urls`

Removes URLs from a string.

```python
from utility_pack.text import remove_urls
text = "Visit my website at https://www.example.com."
cleaned_text = remove_urls(text)
print(cleaned_text)  # Output: Visit my website at .
```

### `remove_emails`

Removes email addresses from a string.

```python
from utility_pack.text import remove_emails
text = "Contact me at test@example.com."
cleaned_text = remove_emails(text)
print(cleaned_text)  # Output: Contact me at .
```

### `compress_text`

Compresses text using semantic compression. Requires `compressor` package to be installed.

```python
from utility_pack.text import compress_text
text = "This is a long sentence that will be compressed."
compressed_text = compress_text(text, compression_rate=0.7)
print(compressed_text)
```

### `string_similarity`

Calculates the similarity between two strings using fuzzy matching based on Enum `StringSimilarity`.

```python
from utility_pack.text import string_similarity, StringSimilarity
string1 = "apple"
string2 = "aplle"
similarity = string_similarity(string1, string2, method=StringSimilarity.Ratio)
print(similarity)  # Output: e.g. 80
```

### `string_similarity_from_list`

Calculates the similarity between a reference string and a list of strings, and returns the most similar string (or top N most similar).

```python
from utility_pack.text import string_similarity_from_list
reference_string = "apple"
list_of_strings = ["aplle", "banana", "orange"]
result = string_similarity_from_list(reference_string, list_of_strings)
print(result)  # Output: ('aplle', 80) (example value)
```

### `find_needle_in_haystack`

Reranks documents to find the "needle" (best match) in a "haystack" (list of documents) using a combination of textual and semantic reranking.

```python
from utility_pack.text import find_needle_in_haystack
needle = "What is the capital of France?"
haystack = [
    "Paris is the capital of France.",
    "London is the capital of England.",
    "France is a country in Europe."
]
result = find_needle_in_haystack(needle, haystack)
print(result)
```

### `chunk_text`

Splits text into chunks of specified token count with optional overlap.

```python
from utility_pack.text import chunk_text
text = "This is a long piece of text that needs to be chunked."
chunks = chunk_text(text, chunk_token_count=10, overlap=2)
print(chunks)
```

## 11\. Vector Databases

This library provides two classes for vector storage and retrieval: `MiniVectorDB` for lightweight, in-memory storage with metadata filtering, and `VectorDB` for scalable, production-ready storage using MongoDB and LMDB.

### MiniVectorDB

`MiniVectorDB` offers a simple, file-based vector database with metadata filtering capabilities. It uses pickle for storage and Faiss for indexing.

```python
from utility_pack.vector_storage import MiniVectorDB
import numpy as np

# Initialize a MiniVectorDB instance
db = MiniVectorDB(storage_file='my_vector_db.pkl')
```

#### Store a single embedding

```python
unique_id = "doc1"
embedding = np.array([0.1, 0.2, 0.3], dtype=np.float32)
metadata = {"category": "science", "author": "John Doe"}

db.store_embedding(unique_id, embedding, metadata)
```

#### Store a batch of embeddings

```python
unique_ids = ["doc2", "doc3"]
embeddings = [
    np.array([0.4, 0.5, 0.6], dtype=np.float32),
    np.array([0.7, 0.8, 0.9], dtype=np.float32)
]
metadata_dicts = [
    {"category": "history", "author": "Jane Smith"},
    {"category": "technology", "author": "Peter Jones"}
]

db.store_embeddings_batch(unique_ids, embeddings, metadata_dicts)
```

#### Get a vector by its unique ID

```python
unique_id = "doc1"
vector = db.get_vector(unique_id)
print(vector)
```

#### Delete an embedding

```python
unique_id = "doc1"
db.delete_embedding(unique_id)
```

#### Find the most similar embeddings (Semantic Search)

```python
query_embedding = np.array([0.2, 0.3, 0.4], dtype=np.float32)
metadata_filter = {"category": "science"}
exclude_filter = {"author": "John Doe"}
or_filters = [{"category": "science"}, {"author": "Jane Smith"}]

ids, distances, metadatas = db.find_most_similar(query_embedding, metadata_filter=metadata_filter, exclude_filter=exclude_filter, or_filters=or_filters, k=3)

print(f"IDs: {ids}")
print(f"Distances: {distances}")
print(f"Metadatas: {metadatas}")
```

#### Persist the database to disk

```python
db.persist_to_disk()
```

### VectorDB

`VectorDB` is designed for production environments, integrating MongoDB for metadata storage and LMDB for efficient vector storage. It depends on the `ShardedLmdbStorage` helper class for LMDB management. From `utility_pack.vector_storage_helper` import ShardedLmdbStorage

```python
from utility_pack.vector_storage_helper import ShardedLmdbStorage
from utility_pack.vector_storage import VectorDB

# Initialize ShardedLmdbStorage. Ensure to provide lmdb_dir at init
vector_storage = ShardedLmdbStorage(base_path="shards/vectors", num_shards=5)
text_storage = ShardedLmdbStorage(base_path="shards/texts", num_shards=5)

db = VectorDB(mongo_uri="mongodb://localhost:27017/", mongo_database="my_db", mongo_collection="my_collection", vector_storage=vector_storage, text_storage=text_storage)
```

#### Store a batch of embeddings with metadata and text

```python
unique_ids = ["doc1", "doc2"]
embeddings = [
    np.array([0.1, 0.2, 0.3], dtype=np.float32),
    np.array([0.4, 0.5, 0.6], dtype=np.float32)
]
metadata_dicts = [
    {"category": "science", "author": "John Doe", "text_content": "This is a science document."},
    {"category": "history", "author": "Jane Smith", "text_content": "This is a history document."}
]

db.store_embeddings_batch(unique_ids, embeddings, metadata_dicts=metadata_dicts, text_field="text_content")
```

#### Delete embeddings by unique IDs

```python
unique_ids = ["doc1", "doc2"]
db.delete_embeddings_batch(unique_ids)
```

#### Delete embeddings based on metadata

```python
metadata_filters = {"category": "science"}
db.delete_embeddings_by_metadata(metadata_filters)
```

#### Find the most similar embeddings (basic usage)

```python
query_embedding = np.array([0.2, 0.3, 0.4], dtype=np.float32)
filters = {"category": "science"}
output_fields = ["author"]

ids, distances, metadatas = db.find_most_similar(query_embedding, filters=filters, output_fields=output_fields, k=3)

print(f"IDs: {ids}")
print(f"Distances: {distances}")
print(f"Metadatas: {metadatas}")
```

#### Find the most similar embeddings with batch processing

```python
query_embedding = np.array([0.2, 0.3, 0.4], dtype=np.float32)
filters = {"category": "science"}
output_fields = ["author"]

ids, distances, metadatas = db.find_most_similar_in_batches(query_embedding, filters=filters, output_fields=output_fields, k=3, max_ram_usage_gb=1)

print(f"IDs: {ids}")
print(f"Distances: {distances}")
print(f"Metadatas: {metadatas}")
```

#### Check the count for each of the storages

```python
db.check_counts()
```

```python
total_count = db.get_total_count()
print(f"Total count of documents: {total_count}")
```
