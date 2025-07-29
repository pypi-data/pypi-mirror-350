import os
import pandas as pd
from langxchange.openai_helper import OpenAIHelper
from langxchange.llama_helper import LLaMAHelper
from langxchange.google_genai_helper import GoogleGenAIHelper
from langxchange.data_format_cleanup_helper import DataFormatCleanupHelper

# 1. Environment setup (use your own key)
os.environ["OPENAI_API_KEY"] = "sk-svcacct-"
os.environ["GOOGLE_API_KEY"] = "AIza"
os.environ["HUGGINGFACE_TOKEN"] =  "hf_"
# 2. Load the raw survey CSV
path     = os.path.dirname(os.path.abspath(__file__))
examples = os.path.join(path, "examples")

# raw_path = "examples/samplefile.txt" #"StudentPerformanceFactors.csv"
raw_path = "examples/StudentPerformanceFactors.csv"
# raw_path = "examples/Student_performance_data _.csv"
df_raw = pd.read_csv(raw_path)

print("Raw data preview:")
print(df_raw.head(10), "\n")

# 3. Initialize LLM helper and cleanup helper
llm = GoogleGenAIHelper()
cleanup_helper = DataFormatCleanupHelper(llm,"examples/")

# 4. Clean the data
# df_clean, df = cleanup_helper.clean(df_raw,examples,"json")

# print("Cleaned data preview:")
# print(df_clean.head(10), "\n")


df_clean = cleanup_helper.clean(df_raw,examples, "csv")

print("Cleaned DataFrame:")
print(df_clean)

# print("\nRecords List:")
# print(records)

# 5. Timing metrics
print("\nTiming Stats:")
# print(cleanup_helper.stats)
stats = cleanup_helper.stats
print("Timing (seconds):")
print(f"  Prompt:  {stats['prompt_time']:.2f}")
print(f"  Extract: {stats['extract_time']:.2f}")
print(f"  Exec:    {stats['exec_time']:.2f}")
print(f"  Clean:   {stats['clean_time']:.2f}")
print(f"  Total:   {stats['total_time']:.2f}")
print("Percent by stage:", stats["percent_complete"], "\n")

# 6. Save cleaned data
clean_path = "examples/samplefile_responses_cleaned.csv"
df_clean.to_csv(clean_path, index=False)
print(f"✅ Cleaned data saved to {clean_path}")
