### **🔧 SYSTEM DESIGN: SOP Markdown Chunking & Pinecone Uploader**

#### **Step 0 – Setup**

* ✅ Assumes `.env` file is configured with:

  * `OPENAI_API_KEY`

  * `OPENAI_EMBEDDING_MODEL`

  * `PINECONE_API_KEY`

  * `PINECONE_INDEX_NAME`

* ✅ Assumes all `.md` SOP files are stored in a folder: `KBdocs/`

---

### **🧱 STEP 1: Load and Parse Markdown Files**

**Goal:** For each file in `KBdocs/`, extract content and parse by level 2 (`##`) and level 3 (`###`) headers.

**Logic:**

* Iterate through all `.md` files in the folder.

* For each file:

  * Use a Markdown parser (e.g. `markdown-it-py` or regex fallback) to extract sections by `##` (Level 2 headers).

  * For each `## Section`, also capture any nested `### Subsections` (as optional nested content).

  * Keep track of:

    * The top-level file name as `source`

    * The `##` header title (for metadata and contextual prefix)

    * Full text content of the section

---

### **✂️ STEP 2: Chunking Strategy**

**Goal:** Split long `##` sections into semantically clean chunks.

**Logic:**

* If a `## Section` has **\< 1500 words**, keep it as one chunk.

* If **≥ 1500 words**, use `RecursiveCharacterTextSplitter`:

  * `chunk_size = 1000`

  * `chunk_overlap = 100`

* Each resulting chunk should be prepended with its `##` header:

  * Format: `"{Heading 2 Title}\n\n{chunked_text}"`

✅ Only `Heading 2` is prepended. Heading 3s are not included unless part of the text.

---

### **📎 STEP 3: Add Metadata for Each Chunk**

**Metadata schema per chunk:**

json  
CopyEdit  
`{`  
  `"source": "KBdocs/filename.md",`  
  `"section_title": "Heading 2 Title",`  
  `"tags": ["support", "internal", "SOP"],`  
  `"audience": "internal",`  
  `"type": "markdown"`  
`}`

* You can infer `"tags"` or leave them generic for now.

* Store `source` as relative file path.

* Ensure `section_title` is exact string of the level 2 header it came from.

---

### **🧠 STEP 4: Generate Embeddings via OpenAI**

**Goal:** Get embedding for each chunk before upserting to Pinecone.

**Logic:**

* Call OpenAI embedding endpoint using the model in `.env`

* Input is the final chunk text (with `Heading 2` prepended)

* Catch failures or empty returns and log

---

### **🪵 STEP 5: Push to Pinecone**

**Goal:** Upsert each chunk into your Pinecone index.

**Logic:**

* Use `PINECONE_API_KEY` and `PINECONE_INDEX_NAME` from `.env`

* Each chunk should be uploaded with:

  * `id`: deterministic hash (e.g. `uuid5(NAMESPACE_URL, chunk_text)` or `f"{filename}-{heading}-{i}"`)

  * `values`: the embedding vector

  * `metadata`: as defined above

---

### **🧹 STEP 6: Optional Cleanup or Re-Index Logic**

(For later scale/hygiene)

Optional future-proofing:

* Detect if chunk already exists (via unique ID) to avoid duplication

* Add timestamp or versioning to metadata if files change frequently

---

### **🔄 End-to-End Flow Summary**

1. Load `.md` files from `KBdocs/`

2. Parse into `##` sections (+ capture `###`s inside)

3. If section is long, split via character-based method

4. Prepend `##` header to each chunk

5. Generate embedding for each chunk

6. Push chunks to Pinecone with metadata

