import pandas as pd
import chromadb

EXCEL_FILE_PATH = r"data/univ_legit.xlsx"
CHROMA_PATH = r"chroma_db" # Path where ChromaDB will store its data

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma_client.get_or_create_collection(name="colleges_and_programs")

print(f"ChromaDB collection '{collection.name}' initialized.")

# Load Excel Data
print(f"Loading data from Excel file: {EXCEL_FILE_PATH}")
try:
    # Read all sheets from the Excel file into a dictionary of DataFrames
    all_sheets_data = pd.read_excel(EXCEL_FILE_PATH, sheet_name=None)
    print(f"Successfully loaded {len(all_sheets_data)} sheets.")
    # DEBUGGING
    print(f"Actual sheet names found: {list(all_sheets_data.keys())}")
    # END OF DEBUGGING
except FileNotFoundError:
    print(f"Error: Excel file not found at {EXCEL_FILE_PATH}. Please check the path.")
    exit()
except Exception as e:
    print(f"An error occurred while reading the Excel file: {e}")
    exit()

# Access specific DataFrames by their sheet names
try:
    colleges_df = all_sheets_data["LIST OF COLLEGES"]
    programs_df = all_sheets_data["PROGRAMS table"] 
    junction_df = all_sheets_data["COLLEGE_PROGRAMS_junction"]
    onlineresources_df = all_sheets_data["ONLINE RESOURCES table"]
    scholarships_df = all_sheets_data["SCHOOL_SCHOLARSHIPS table"]

    print("Accessed all five required sheets.")
except KeyError as e:
    print(f"Error: Missing expected sheet in Excel file. Please ensure sheet names are exact: {e}")
    exit()

# Merge DataFrames to create comprehensive records 
print("Merging data from different sheets...")

# Merge junction_df with colleges_df on SCHOOL_ID
merged_data = pd.merge(
    junction_df,
    colleges_df,
    on="SCHOOL_ID",
    how="left"
)

# Merge the result with programs_df
final_combined_data = pd.merge(
    merged_data,
    programs_df,
    on="PROGRAM_ID",
    how="left"
)

# Merge everything else with onlineresources_df
real_final_combined_data = pd.merge(
    final_combined_data,
    onlineresources_df,
    on="PROGRAM_ID",
    how="left"

)

# Merge everything with scholarships_df
actually_really_final_combined_data = pd.merge(
    real_final_combined_data,
    scholarships_df,
    on="SCHOOL_ID",
    how="left"
)

# Handle potential NaN values from merges (e.g., if an ID didn't match)
actually_really_final_combined_data = actually_really_final_combined_data.fillna('N/A')

print(f"Finished merging. Total combined records: {len(actually_really_final_combined_data)}")

# Prepare Data for ChromaDB 
documents_to_add = []
metadatas_to_add = []
ids_to_add = []
record_counter = 0 # Unique counter for generating IDs


for index, row in actually_really_final_combined_data.iterrows():
    # CRITICAL PART: Constructing the document text from each combined row 
    # This creates a rich, descriptive string that the AI can easily understand.
    # We're combining information from all three original sheets into one coherent sentence.
    
    institution_name = row['INSTITUTION_NAME']
    institution_type = row['INSTITUTION_TYPE']
    municipality = row['MUNICIPALITY']
    province = row['PROVINCE']
    program_name = row['PROGRAM_NAME']
    website_address = row['WEBSITE_ADDRESS']
    resource_name = row['RESOURCE_NAME']
    resource_link = row['LINK']
    resource_types = row['TYPE']
    dost_eligibility = row['DOST_ELIGIBLE']

    

    document_content = (
        f"The {institution_name} ({institution_type} college) "
        f"located in {municipality}, {province} offers the {program_name} program. "
        f"Their website is {website_address}."
    )

    documents_to_add.append(document_content)
    
    # Store useful metadata for potential filtering or more detailed retrieval
    metadatas_to_add.append({
        "school_id": row['SCHOOL_ID'],
        "program_id": row['PROGRAM_ID_x'],
        "institution_name": institution_name,
        "institution_type": institution_type,
        "province": province,
        "municipality": municipality,
        "program_name": program_name,
        "resource_name": resource_name,
        "resource_link": resource_link,
        "resource_types": resource_types,
        "dost_eligibility": dost_eligibility,
    })
    
    ids_to_add.append(f"school_program_offering_{record_counter}")
    record_counter += 1

print(f"\nPrepared {len(documents_to_add)} documents for ChromaDB.")

# Add to ChromaDB 
if documents_to_add:
    print("Adding documents to ChromaDB...")
    # Using upsert will add new documents or update existing ones if IDs match
    collection.upsert(
        documents=documents_to_add,
        metadatas=metadatas_to_add,
        ids=ids_to_add
    )
    print("Documents successfully added/updated in ChromaDB.")
else:
    print("No documents were prepared from the Excel file. ChromaDB not updated.")
