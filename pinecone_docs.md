# Pinecone Database quickstart

This guide shows you how to set up and use Pinecone Database for high-performance semantic search.

<Tip>
  To get started in your browser, use the [Quickstart colab notebook](https://colab.research.google.com/github/pinecone-io/examples/blob/master/docs/pinecone-quickstart.ipynb). To try Pinecone Database locally before creating an account, use [Pinecone Local](/guides/operations/local-development).
</Tip>

## 1. Install an SDK

Pinecone provides [SDKs](/reference/pinecone-sdks) in multiple languages. For this quickstart, install the [Python SDK](/reference/python-sdk), [Node.js SDK](/reference/node-sdk), or [Go SDK](/reference/go-sdk):

<CodeGroup>
  ```shell Python
  pip install pinecone
  ```

  ```shell JavaScript
  npm install @pinecone-database/pinecone
  ```

  ```bash Go
  go get github.com/pinecone-io/go-pinecone/v3/pinecone
  ```
</CodeGroup>

## 2. Get an API key

You need an API key to make calls to your Pinecone project.

Create a new API key in the [Pinecone console](https://app.pinecone.io/organizations/-/keys), or use the widget below to generate a key. If you don't have a Pinecone account, the widget will sign you up for the free [Starter plan](https://www.pinecone.io/pricing/).

<div style={{minWidth: '450px', minHeight:'152px'}}>
  <div id="pinecone-connect-widget">
    <div class="connect-widget-skeleton">
      <div class="skeleton-content" />
    </div>
  </div>
</div>

Your generated API key:

```shell
"{{YOUR_API_KEY}}"
```

## 3. Create an index

In Pinecone, there are two types of indexes for storing vector data: [Dense indexes](/guides/index-data/indexing-overview#dense-indexes) store <Tooltip tip="Each number in a dense vector is a point in a multidimensional space. Vectors that are closer together in that space are semantically similar.">dense vectors</Tooltip> for semantic search, and [sparse indexes](/guides/index-data/indexing-overview#sparse-indexes) store <Tooltip tip="A sparse vector has a very large number of dimensions, where only a small proportion of values are non-zero. The dimensions represent words from a dictionary, and the values represent the importance of these words in the document.">sparse vectors</Tooltip> for lexical/keyword search.

For this quickstart, [create a dense index](/guides/index-data/create-an-index#create-a-dense-index) that is integrated with an [embedding model hosted by Pinecone](/guides/index-data/create-an-index#embedding-models). With integrated models, you upsert and search with text and have Pinecone generate vectors automatically.

<Note>
  If you prefer to use external embedding models, see [Bring your own vectors](/guides/index-data/indexing-overview#bring-your-own-vectors).
</Note>

<CodeGroup>
  ```python Python
  # Import the Pinecone library
  from pinecone import Pinecone

  # Initialize a Pinecone client with your API key
  pc = Pinecone(api_key="{{YOUR_API_KEY}}")

  # Create a dense index with integrated embedding
  index_name = "quickstart-py"
  if not pc.has_index(index_name):
      pc.create_index_for_model(
          name=index_name,
          cloud="aws",
          region="us-east-1",
          embed={
              "model":"llama-text-embed-v2",
              "field_map":{"text": "chunk_text"}
          }
      )
  ```

  ```javascript JavaScript
  // Import the Pinecone library
  import { Pinecone } from '@pinecone-database/pinecone'

  // Initialize a Pinecone client with your API key
  const pc = new Pinecone({ apiKey: '{{YOUR_API_KEY}}' });

  // Create a dense index with integrated embedding
  const indexName = 'quickstart-js';
  await pc.createIndexForModel({
    name: indexName,
    cloud: 'aws',
    region: 'us-east-1',
    embed: {
      model: 'llama-text-embed-v2',
      fieldMap: { text: 'chunk_text' },
    },
    waitUntilReady: true,
  });
  ```

  ```go Go
  package main

  import (
      "context"
      "encoding/json"
      "fmt"
      "log"

      "github.com/pinecone-io/go-pinecone/v3/pinecone"
  )

  func main() {
      ctx := context.Background()

      pc, err := pinecone.NewClient(pinecone.NewClientParams{
          ApiKey: "{{YOUR_API_KEY}}",
      })
      if err != nil {
          log.Fatalf("Failed to create Client: %v", err)
      }

    	indexName := "quickstart-go"
      index, err := pc.CreateIndexForModel(ctx, &pinecone.CreateIndexForModelRequest{
          Name:   indexName,
          Cloud:  pinecone.Aws,
          Region: "us-east-1",
          Embed: pinecone.CreateIndexForModelEmbed{
              Model:    "llama-text-embed-v2",
              FieldMap: map[string]interface{}{"text": "chunk_text"},
          },
      })
      if err != nil {
          log.Fatalf("Failed to create serverless index: %v", idx.Name)
      } else {
          fmt.Printf("Successfully created serverless index: %v", idx.Name)
      }
  }

  // Function to prettify responses
  func prettifyStruct(obj interface{}) string {
    	bytes, _ := json.MarshalIndent(obj, "", "  ")
      return string(bytes)
  }
  ```
</CodeGroup>

## 4. Upsert text

Prepare a sample dataset of factual statements from different domains like history, physics, technology, and music. Format the data as [records](/guides/get-started/glossary#record) with an ID, text, and category.

<CodeGroup>
  ```python Python [expandable]
  records = [
      { "_id": "rec1", "chunk_text": "The Eiffel Tower was completed in 1889 and stands in Paris, France.", "category": "history" },
      { "_id": "rec2", "chunk_text": "Photosynthesis allows plants to convert sunlight into energy.", "category": "science" },
      { "_id": "rec3", "chunk_text": "Albert Einstein developed the theory of relativity.", "category": "science" },
      { "_id": "rec4", "chunk_text": "The mitochondrion is often called the powerhouse of the cell.", "category": "biology" },
      { "_id": "rec5", "chunk_text": "Shakespeare wrote many famous plays, including Hamlet and Macbeth.", "category": "literature" },
      { "_id": "rec6", "chunk_text": "Water boils at 100°C under standard atmospheric pressure.", "category": "physics" },
      { "_id": "rec7", "chunk_text": "The Great Wall of China was built to protect against invasions.", "category": "history" },
      { "_id": "rec8", "chunk_text": "Honey never spoils due to its low moisture content and acidity.", "category": "food science" },
      { "_id": "rec9", "chunk_text": "The speed of light in a vacuum is approximately 299,792 km/s.", "category": "physics" },
      { "_id": "rec10", "chunk_text": "Newton’s laws describe the motion of objects.", "category": "physics" },
      { "_id": "rec11", "chunk_text": "The human brain has approximately 86 billion neurons.", "category": "biology" },
      { "_id": "rec12", "chunk_text": "The Amazon Rainforest is one of the most biodiverse places on Earth.", "category": "geography" },
      { "_id": "rec13", "chunk_text": "Black holes have gravitational fields so strong that not even light can escape.", "category": "astronomy" },
      { "_id": "rec14", "chunk_text": "The periodic table organizes elements based on their atomic number.", "category": "chemistry" },
      { "_id": "rec15", "chunk_text": "Leonardo da Vinci painted the Mona Lisa.", "category": "art" },
      { "_id": "rec16", "chunk_text": "The internet revolutionized communication and information sharing.", "category": "technology" },
      { "_id": "rec17", "chunk_text": "The Pyramids of Giza are among the Seven Wonders of the Ancient World.", "category": "history" },
      { "_id": "rec18", "chunk_text": "Dogs have an incredible sense of smell, much stronger than humans.", "category": "biology" },
      { "_id": "rec19", "chunk_text": "The Pacific Ocean is the largest and deepest ocean on Earth.", "category": "geography" },
      { "_id": "rec20", "chunk_text": "Chess is a strategic game that originated in India.", "category": "games" },
      { "_id": "rec21", "chunk_text": "The Statue of Liberty was a gift from France to the United States.", "category": "history" },
      { "_id": "rec22", "chunk_text": "Coffee contains caffeine, a natural stimulant.", "category": "food science" },
      { "_id": "rec23", "chunk_text": "Thomas Edison invented the practical electric light bulb.", "category": "inventions" },
      { "_id": "rec24", "chunk_text": "The moon influences ocean tides due to gravitational pull.", "category": "astronomy" },
      { "_id": "rec25", "chunk_text": "DNA carries genetic information for all living organisms.", "category": "biology" },
      { "_id": "rec26", "chunk_text": "Rome was once the center of a vast empire.", "category": "history" },
      { "_id": "rec27", "chunk_text": "The Wright brothers pioneered human flight in 1903.", "category": "inventions" },
      { "_id": "rec28", "chunk_text": "Bananas are a good source of potassium.", "category": "nutrition" },
      { "_id": "rec29", "chunk_text": "The stock market fluctuates based on supply and demand.", "category": "economics" },
      { "_id": "rec30", "chunk_text": "A compass needle points toward the magnetic north pole.", "category": "navigation" },
      { "_id": "rec31", "chunk_text": "The universe is expanding, according to the Big Bang theory.", "category": "astronomy" },
      { "_id": "rec32", "chunk_text": "Elephants have excellent memory and strong social bonds.", "category": "biology" },
      { "_id": "rec33", "chunk_text": "The violin is a string instrument commonly used in orchestras.", "category": "music" },
      { "_id": "rec34", "chunk_text": "The heart pumps blood throughout the human body.", "category": "biology" },
      { "_id": "rec35", "chunk_text": "Ice cream melts when exposed to heat.", "category": "food science" },
      { "_id": "rec36", "chunk_text": "Solar panels convert sunlight into electricity.", "category": "technology" },
      { "_id": "rec37", "chunk_text": "The French Revolution began in 1789.", "category": "history" },
      { "_id": "rec38", "chunk_text": "The Taj Mahal is a mausoleum built by Emperor Shah Jahan.", "category": "history" },
      { "_id": "rec39", "chunk_text": "Rainbows are caused by light refracting through water droplets.", "category": "physics" },
      { "_id": "rec40", "chunk_text": "Mount Everest is the tallest mountain in the world.", "category": "geography" },
      { "_id": "rec41", "chunk_text": "Octopuses are highly intelligent marine creatures.", "category": "biology" },
      { "_id": "rec42", "chunk_text": "The speed of sound is around 343 meters per second in air.", "category": "physics" },
      { "_id": "rec43", "chunk_text": "Gravity keeps planets in orbit around the sun.", "category": "astronomy" },
      { "_id": "rec44", "chunk_text": "The Mediterranean diet is considered one of the healthiest in the world.", "category": "nutrition" },
      { "_id": "rec45", "chunk_text": "A haiku is a traditional Japanese poem with a 5-7-5 syllable structure.", "category": "literature" },
      { "_id": "rec46", "chunk_text": "The human body is made up of about 60% water.", "category": "biology" },
      { "_id": "rec47", "chunk_text": "The Industrial Revolution transformed manufacturing and transportation.", "category": "history" },
      { "_id": "rec48", "chunk_text": "Vincent van Gogh painted Starry Night.", "category": "art" },
      { "_id": "rec49", "chunk_text": "Airplanes fly due to the principles of lift and aerodynamics.", "category": "physics" },
      { "_id": "rec50", "chunk_text": "Renewable energy sources include wind, solar, and hydroelectric power.", "category": "energy" }
  ]
  ```

  ```javascript JavaScript [expandable]
  const records = [
    { "_id": "rec1", "chunk_text": "The Eiffel Tower was completed in 1889 and stands in Paris, France.", "category": "history" },
    { "_id": "rec2", "chunk_text": "Photosynthesis allows plants to convert sunlight into energy.", "category": "science" },
    { "_id": "rec3", "chunk_text": "Albert Einstein developed the theory of relativity.", "category": "science" },
    { "_id": "rec4", "chunk_text": "The mitochondrion is often called the powerhouse of the cell.", "category": "biology" },
    { "_id": "rec5", "chunk_text": "Shakespeare wrote many famous plays, including Hamlet and Macbeth.", "category": "literature" },
    { "_id": "rec6", "chunk_text": "Water boils at 100°C under standard atmospheric pressure.", "category": "physics" },
    { "_id": "rec7", "chunk_text": "The Great Wall of China was built to protect against invasions.", "category": "history" },
    { "_id": "rec8", "chunk_text": "Honey never spoils due to its low moisture content and acidity.", "category": "food science" },
    { "_id": "rec9", "chunk_text": "The speed of light in a vacuum is approximately 299,792 km/s.", "category": "physics" },
    { "_id": "rec10", "chunk_text": "Newton’s laws describe the motion of objects.", "category": "physics" },
    { "_id": "rec11", "chunk_text": "The human brain has approximately 86 billion neurons.", "category": "biology" },
    { "_id": "rec12", "chunk_text": "The Amazon Rainforest is one of the most biodiverse places on Earth.", "category": "geography" },
    { "_id": "rec13", "chunk_text": "Black holes have gravitational fields so strong that not even light can escape.", "category": "astronomy" },
    { "_id": "rec14", "chunk_text": "The periodic table organizes elements based on their atomic number.", "category": "chemistry" },
    { "_id": "rec15", "chunk_text": "Leonardo da Vinci painted the Mona Lisa.", "category": "art" },
    { "_id": "rec16", "chunk_text": "The internet revolutionized communication and information sharing.", "category": "technology" },
    { "_id": "rec17", "chunk_text": "The Pyramids of Giza are among the Seven Wonders of the Ancient World.", "category": "history" },
    { "_id": "rec18", "chunk_text": "Dogs have an incredible sense of smell, much stronger than humans.", "category": "biology" },
    { "_id": "rec19", "chunk_text": "The Pacific Ocean is the largest and deepest ocean on Earth.", "category": "geography" },
    { "_id": "rec20", "chunk_text": "Chess is a strategic game that originated in India.", "category": "games" },
    { "_id": "rec21", "chunk_text": "The Statue of Liberty was a gift from France to the United States.", "category": "history" },
    { "_id": "rec22", "chunk_text": "Coffee contains caffeine, a natural stimulant.", "category": "food science" },
    { "_id": "rec23", "chunk_text": "Thomas Edison invented the practical electric light bulb.", "category": "inventions" },
    { "_id": "rec24", "chunk_text": "The moon influences ocean tides due to gravitational pull.", "category": "astronomy" },
    { "_id": "rec25", "chunk_text": "DNA carries genetic information for all living organisms.", "category": "biology" },
    { "_id": "rec26", "chunk_text": "Rome was once the center of a vast empire.", "category": "history" },
    { "_id": "rec27", "chunk_text": "The Wright brothers pioneered human flight in 1903.", "category": "inventions" },
    { "_id": "rec28", "chunk_text": "Bananas are a good source of potassium.", "category": "nutrition" },
    { "_id": "rec29", "chunk_text": "The stock market fluctuates based on supply and demand.", "category": "economics" },
    { "_id": "rec30", "chunk_text": "A compass needle points toward the magnetic north pole.", "category": "navigation" },
    { "_id": "rec31", "chunk_text": "The universe is expanding, according to the Big Bang theory.", "category": "astronomy" },
    { "_id": "rec32", "chunk_text": "Elephants have excellent memory and strong social bonds.", "category": "biology" },
    { "_id": "rec33", "chunk_text": "The violin is a string instrument commonly used in orchestras.", "category": "music" },
    { "_id": "rec34", "chunk_text": "The heart pumps blood throughout the human body.", "category": "biology" },
    { "_id": "rec35", "chunk_text": "Ice cream melts when exposed to heat.", "category": "food science" },
    { "_id": "rec36", "chunk_text": "Solar panels convert sunlight into electricity.", "category": "technology" },
    { "_id": "rec37", "chunk_text": "The French Revolution began in 1789.", "category": "history" },
    { "_id": "rec38", "chunk_text": "The Taj Mahal is a mausoleum built by Emperor Shah Jahan.", "category": "history" },
    { "_id": "rec39", "chunk_text": "Rainbows are caused by light refracting through water droplets.", "category": "physics" },
    { "_id": "rec40", "chunk_text": "Mount Everest is the tallest mountain in the world.", "category": "geography" },
    { "_id": "rec41", "chunk_text": "Octopuses are highly intelligent marine creatures.", "category": "biology" },
    { "_id": "rec42", "chunk_text": "The speed of sound is around 343 meters per second in air.", "category": "physics" },
    { "_id": "rec43", "chunk_text": "Gravity keeps planets in orbit around the sun.", "category": "astronomy" },
    { "_id": "rec44", "chunk_text": "The Mediterranean diet is considered one of the healthiest in the world.", "category": "nutrition" },
    { "_id": "rec45", "chunk_text": "A haiku is a traditional Japanese poem with a 5-7-5 syllable structure.", "category": "literature" },
    { "_id": "rec46", "chunk_text": "The human body is made up of about 60% water.", "category": "biology" },
    { "_id": "rec47", "chunk_text": "The Industrial Revolution transformed manufacturing and transportation.", "category": "history" },
    { "_id": "rec48", "chunk_text": "Vincent van Gogh painted Starry Night.", "category": "art" },
    { "_id": "rec49", "chunk_text": "Airplanes fly due to the principles of lift and aerodynamics.", "category": "physics" },
    { "_id": "rec50", "chunk_text": "Renewable energy sources include wind, solar, and hydroelectric power.", "category": "energy" }
  ];
  ```

  ```go Go [expandable]
  // Add to the main function:
  records := []*pinecone.IntegratedRecord{
      { "_id": "rec1", "chunk_text": "The Eiffel Tower was completed in 1889 and stands in Paris, France.", "category": "history" },
      { "_id": "rec2", "chunk_text": "Photosynthesis allows plants to convert sunlight into energy.", "category": "science" },
      { "_id": "rec3", "chunk_text": "Albert Einstein developed the theory of relativity.", "category": "science" },
      { "_id": "rec4", "chunk_text": "The mitochondrion is often called the powerhouse of the cell.", "category": "biology" },
      { "_id": "rec5", "chunk_text": "Shakespeare wrote many famous plays, including Hamlet and Macbeth.", "category": "literature" },
      { "_id": "rec6", "chunk_text": "Water boils at 100°C under standard atmospheric pressure.", "category": "physics" },
      { "_id": "rec7", "chunk_text": "The Great Wall of China was built to protect against invasions.", "category": "history" },
      { "_id": "rec8", "chunk_text": "Honey never spoils due to its low moisture content and acidity.", "category": "food science" },
      { "_id": "rec9", "chunk_text": "The speed of light in a vacuum is approximately 299,792 km/s.", "category": "physics" },
      { "_id": "rec10", "chunk_text": "Newton’s laws describe the motion of objects.", "category": "physics" },
      { "_id": "rec11", "chunk_text": "The human brain has approximately 86 billion neurons.", "category": "biology" },
      { "_id": "rec12", "chunk_text": "The Amazon Rainforest is one of the most biodiverse places on Earth.", "category": "geography" },
      { "_id": "rec13", "chunk_text": "Black holes have gravitational fields so strong that not even light can escape.", "category": "astronomy" },
      { "_id": "rec14", "chunk_text": "The periodic table organizes elements based on their atomic number.", "category": "chemistry" },
      { "_id": "rec15", "chunk_text": "Leonardo da Vinci painted the Mona Lisa.", "category": "art" },
      { "_id": "rec16", "chunk_text": "The internet revolutionized communication and information sharing.", "category": "technology" },
      { "_id": "rec17", "chunk_text": "The Pyramids of Giza are among the Seven Wonders of the Ancient World.", "category": "history" },
      { "_id": "rec18", "chunk_text": "Dogs have an incredible sense of smell, much stronger than humans.", "category": "biology" },
      { "_id": "rec19", "chunk_text": "The Pacific Ocean is the largest and deepest ocean on Earth.", "category": "geography" },
      { "_id": "rec20", "chunk_text": "Chess is a strategic game that originated in India.", "category": "games" },
      { "_id": "rec21", "chunk_text": "The Statue of Liberty was a gift from France to the United States.", "category": "history" },
      { "_id": "rec22", "chunk_text": "Coffee contains caffeine, a natural stimulant.", "category": "food science" },
      { "_id": "rec23", "chunk_text": "Thomas Edison invented the practical electric light bulb.", "category": "inventions" },
      { "_id": "rec24", "chunk_text": "The moon influences ocean tides due to gravitational pull.", "category": "astronomy" },
      { "_id": "rec25", "chunk_text": "DNA carries genetic information for all living organisms.", "category": "biology" },
      { "_id": "rec26", "chunk_text": "Rome was once the center of a vast empire.", "category": "history" },
      { "_id": "rec27", "chunk_text": "The Wright brothers pioneered human flight in 1903.", "category": "inventions" },
      { "_id": "rec28", "chunk_text": "Bananas are a good source of potassium.", "category": "nutrition" },
      { "_id": "rec29", "chunk_text": "The stock market fluctuates based on supply and demand.", "category": "economics" },
      { "_id": "rec30", "chunk_text": "A compass needle points toward the magnetic north pole.", "category": "navigation" },
      { "_id": "rec31", "chunk_text": "The universe is expanding, according to the Big Bang theory.", "category": "astronomy" },
      { "_id": "rec32", "chunk_text": "Elephants have excellent memory and strong social bonds.", "category": "biology" },
      { "_id": "rec33", "chunk_text": "The violin is a string instrument commonly used in orchestras.", "category": "music" },
      { "_id": "rec34", "chunk_text": "The heart pumps blood throughout the human body.", "category": "biology" },
      { "_id": "rec35", "chunk_text": "Ice cream melts when exposed to heat.", "category": "food science" },
      { "_id": "rec36", "chunk_text": "Solar panels convert sunlight into electricity.", "category": "technology" },
      { "_id": "rec37", "chunk_text": "The French Revolution began in 1789.", "category": "history" },
      { "_id": "rec38", "chunk_text": "The Taj Mahal is a mausoleum built by Emperor Shah Jahan.", "category": "history" },
      { "_id": "rec39", "chunk_text": "Rainbows are caused by light refracting through water droplets.", "category": "physics" },
      { "_id": "rec40", "chunk_text": "Mount Everest is the tallest mountain in the world.", "category": "geography" },
      { "_id": "rec41", "chunk_text": "Octopuses are highly intelligent marine creatures.", "category": "biology" },
      { "_id": "rec42", "chunk_text": "The speed of sound is around 343 meters per second in air.", "category": "physics" },
      { "_id": "rec43", "chunk_text": "Gravity keeps planets in orbit around the sun.", "category": "astronomy" },
      { "_id": "rec44", "chunk_text": "The Mediterranean diet is considered one of the healthiest in the world.", "category": "nutrition" },
      { "_id": "rec45", "chunk_text": "A haiku is a traditional Japanese poem with a 5-7-5 syllable structure.", "category": "literature" },
      { "_id": "rec46", "chunk_text": "The human body is made up of about 60% water.", "category": "biology" },
      { "_id": "rec47", "chunk_text": "The Industrial Revolution transformed manufacturing and transportation.", "category": "history" },
      { "_id": "rec48", "chunk_text": "Vincent van Gogh painted Starry Night.", "category": "art" },
      { "_id": "rec49", "chunk_text": "Airplanes fly due to the principles of lift and aerodynamics.", "category": "physics" },
      { "_id": "rec50", "chunk_text": "Renewable energy sources include wind, solar, and hydroelectric power.", "category": "energy" },
  }
  ```
</CodeGroup>

[Upsert](/guides/index-data/upsert-data) the sample dataset into a new [namespace](/guides/index-data/indexing-overview#namespaces) in your index.

Because your index is integrated with an embedding model, you provide the textual statements and Pinecone converts them to dense vectors automatically.

<CodeGroup>
  ```python Python
  # Target the index
  dense_index = pc.Index(index_name)

  # Upsert the records into a namespace
  dense_index.upsert_records("example-namespace", records)
  ```

  ```javascript JavaScript
  // Target the index
  const index = pc.index(indexName).namespace("example-namespace");

  // Upsert the records into a namespace
  await index.upsertRecords(records);
  ```

  ```go Go
  // Add to the main function:
  // Target the index
  idxModel, err := pc.DescribeIndex(ctx, indexName)
  if err != nil {
      log.Fatalf("Failed to describe index \"%v\": %v", indexName, err)
  }

  idxConnection, err := pc.Index(pinecone.NewIndexConnParams{Host: idxModel.Host, Namespace: "example-namespace"})
  if err != nil {
      log.Fatalf("Failed to create IndexConnection for Host: %v: %v", idxModel.Host, err)
  }

  // Upsert the records into a namespace
  err = idxConnection.UpsertRecords(ctx, records)
  if err != nil {
      log.Fatalf("Failed to upsert vectors: %v", err)
  }
  ```
</CodeGroup>

<Tip>
  To load large amounts of data, [import from object storage](/guides/index-data/import-data) or [upsert in large batches](/guides/index-data/upsert-data#upsert-in-batches).
</Tip>

Pinecone is eventually consistent, so there can be a slight delay before new or changed records are visible to queries. You can [view index stats](/guides/index-data/check-data-freshness) to check if the current vector count matches the number of vectors you upserted (50):

<CodeGroup>
  ```python Python
  # Wait for the upserted vectors to be indexed
  import time
  time.sleep(10)

  # View stats for the index
  stats = dense_index.describe_index_stats()
  print(stats)
  ```

  ```javascript JavaScript
  // Wait for the upserted vectors to be indexed
  await new Promise(resolve => setTimeout(resolve, 10000));

  // View stats for the index
  const stats = await index.describeIndexStats();
  console.log(stats);
  ```

  ```go Go
  // Add to the main function:
  // View stats for the index
  stats, err := idxConnection.DescribeIndexStats(ctx)
  if err != nil {
      log.Fatalf("Failed to describe index \"%v\": %v", indexName, err)
  } else {
      fmt.Printf("%+v", prettifyStruct(*stats))
  }
  ```
</CodeGroup>

The response looks like this:

<CodeGroup>
  ```python Python
  {'dimension': 1024,
   'index_fullness': 0.0,
   'metric': 'cosine',
   'namespaces': {'example-namespace': {'vector_count': 50}},
   'total_vector_count': 50,
   'vector_type': 'dense'}
  ```

  ```javascript JavaScript
  {
    namespaces: { 'example-namespace': { recordCount: 50 } },
    dimension: 1024,
    indexFullness: 0,
    totalRecordCount: 50
  }
  ```

  ```go Go
  {
    "dimension": 1024,
    "index_fullness": 0,
    "total_vector_count": 50,
    "namespaces": {
      "example-namespace": {
        "vector_count": 50
      }
    }
  }
  ```
</CodeGroup>

## 5. Semantic search

[Search the dense index](/guides/search/semantic-search) for ten records that are most semantically similar to the query, "Famous historical structures and monuments".

Again, because your index is integrated with an embedding model, you provide the query as text and Pinecone converts the text to a dense vector automatically.

<CodeGroup>
  ```python Python
  # Define the query
  query = "Famous historical structures and monuments"

  # Search the dense index
  results = dense_index.search(
      namespace="example-namespace",
      query={
          "top_k": 10,
          "inputs": {
              'text': query
          }
      }
  )

  # Print the results
  for hit in results['result']['hits']:
          print(f"id: {hit['_id']:<5} | score: {round(hit['_score'], 2):<5} | category: {hit['fields']['category']:<10} | text: {hit['fields']['chunk_text']:<50}")
  ```

  ```javascript JavaScript
  // Define the query
  const query = 'Famous historical structures and monuments';

  // Search the dense index
  const results = await index.searchRecords({
    query: {
      topK: 10,
      inputs: { text: query },
    },
  });

  // Print the results
  results.result.hits.forEach(hit => {
    console.log(`id: ${hit.id}, score: ${hit.score.toFixed(2)}, category: ${hit.fields.category}, text: ${hit.fields.chunk_text}`);
  });
  ```

  ```go Go
  // Add to the main function:
  // Define the query
  query := "Famous historical structures and monuments"

  // Search the dense index
  res, err := idxConnection.SearchRecords(ctx, &pinecone.SearchRecordsRequest{
      Query: pinecone.SearchRecordsQuery{
          TopK: 10,
          Inputs: &map[string]interface{}{
              "text": query,
          },
      },
  })
  if err != nil {
      log.Fatalf("Failed to search records: %v", err)
  }
  fmt.Printf(prettifyStruct(res))
  ```
</CodeGroup>

Notice that most of the results are about historical structures and monuments. However, a few unrelated statements are included as well and are ranked high in the list, for example, statements about Shakespeare and renewable energy.

<CodeGroup>
  ```console Python
  id: rec17 | score: 0.24  | category: history    | text: The Pyramids of Giza are among the Seven Wonders of the Ancient World.
  id: rec38 | score: 0.19  | category: history    | text: The Taj Mahal is a mausoleum built by Emperor Shah Jahan.
  id: rec5  | score: 0.19  | category: literature | text: Shakespeare wrote many famous plays, including Hamlet and Macbeth.
  id: rec15 | score: 0.11  | category: art        | text: Leonardo da Vinci painted the Mona Lisa.          
  id: rec50 | score: 0.1   | category: energy     | text: Renewable energy sources include wind, solar, and hydroelectric power.
  id: rec26 | score: 0.09  | category: history    | text: Rome was once the center of a vast empire.        
  id: rec47 | score: 0.08  | category: history    | text: The Industrial Revolution transformed manufacturing and transportation.
  id: rec7  | score: 0.07  | category: history    | text: The Great Wall of China was built to protect against invasions.
  id: rec1  | score: 0.07  | category: history    | text: The Eiffel Tower was completed in 1889 and stands in Paris, France.
  id: rec3  | score: 0.07  | category: science    | text: Albert Einstein developed the theory of relativity.
  ```

  ```console JavaScript
  id: rec17, score: 0.24, text: The Pyramids of Giza are among the Seven Wonders of the Ancient World., category: history
  id: rec38, score: 0.19, text: The Taj Mahal is a mausoleum built by Emperor Shah Jahan., category: history
  id: rec5, score: 0.19, text: Shakespeare wrote many famous plays, including Hamlet and Macbeth., category: literature
  id: rec15, score: 0.11, text: Leonardo da Vinci painted the Mona Lisa., category: art
  id: rec50, score: 0.10, text: Renewable energy sources include wind, solar, and hydroelectric power., category: energy
  id: rec26, score: 0.09, text: Rome was once the center of a vast empire., category: history
  id: rec47, score: 0.08, text: The Industrial Revolution transformed manufacturing and transportation., category: history
  id: rec7, score: 0.07, text: The Great Wall of China was built to protect against invasions., category: history
  id: rec1, score: 0.07, text: The Eiffel Tower was completed in 1889 and stands in Paris, France., category: history
  id: rec3, score: 0.07, text: Albert Einstein developed the theory of relativity., category: science
  ```

  ```json Go [expandable]
  {
    "result": {
      "hits": [
        {
          "_id": "rec17",
          "_score": 0.24442708,
          "fields": {
            "category": "history",
            "chunk_text": "The Pyramids of Giza are among the Seven Wonders of the Ancient World."
          }
        },
        {
          "_id": "rec38",
          "_score": 0.1876694,
          "fields": {
            "category": "history",
            "chunk_text": "The Taj Mahal is a mausoleum built by Emperor Shah Jahan."
          }
        },
        {
          "_id": "rec5",
          "_score": 0.18504046,
          "fields": {
            "category": "literature",
            "chunk_text": "Shakespeare wrote many famous plays, including Hamlet and Macbeth."
          }
        },
        {
          "_id": "rec15",
          "_score": 0.109251045,
          "fields": {
            "category": "art",
            "chunk_text": "Leonardo da Vinci painted the Mona Lisa."
          }
        },
        {
          "_id": "rec50",
          "_score": 0.098952696,
          "fields": {
            "category": "energy",
            "chunk_text": "Renewable energy sources include wind, solar, and hydroelectric power."
          }
        },
        {
          "_id": "rec26",
          "_score": 0.085251465,
          "fields": {
            "category": "history",
            "chunk_text": "Rome was once the center of a vast empire."
          }
        },
        {
          "_id": "rec47",
          "_score": 0.07533597,
          "fields": {
            "category": "history",
            "chunk_text": "The Industrial Revolution transformed manufacturing and transportation."
          }
        },
        {
          "_id": "rec7",
          "_score": 0.06859385,
          "fields": {
            "category": "history",
            "chunk_text": "The Great Wall of China was built to protect against invasions."
          }
        },
        {
          "_id": "rec1",
          "_score": 0.06831257,
          "fields": {
            "category": "history",
            "chunk_text": "The Eiffel Tower was completed in 1889 and stands in Paris, France."
          }
        },
        {
          "_id": "rec3",
          "_score": 0.06689669,
          "fields": {
            "category": "science",
            "chunk_text": "Albert Einstein developed the theory of relativity."
          }
        }
      ]
    },
    "usage": {
      "read_units": 6,
      "embed_total_tokens": 8
    }
  }
  ```
</CodeGroup>

## 6. Rerank results

To get a more accurate ranking, search again but this time [rerank the initial results](/guides/search/rerank-results) based on their relevance to the query.

<CodeGroup>
  ```python Python
  # Search the dense index and rerank results
  reranked_results = dense_index.search(
      namespace="example-namespace",
      query={
          "top_k": 10,
          "inputs": {
              'text': query
          }
      },
      rerank={
          "model": "bge-reranker-v2-m3",
          "top_n": 10,
          "rank_fields": ["chunk_text"]
      }   
  )

  # Print the reranked results
  for hit in reranked_results['result']['hits']:
      print(f"id: {hit['_id']}, score: {round(hit['_score'], 2)}, text: {hit['fields']['chunk_text']}, category: {hit['fields']['category']}")
  ```

  ```javascript JavaScript
  // Search the dense index and rerank results
  const rerankedResults = await index.searchRecords({
    query: {
      topK: 10,
      inputs: { text: query },
    },
    rerank: {
      model: 'bge-reranker-v2-m3',
      topN: 10,
      rankFields: ['chunk_text'],
    },
  });

  // Print the reranked results
  rerankedResults.result.hits.forEach(hit => {
    console.log(`id: ${hit.id}, score: ${hit.score.toFixed(2)}, text: ${hit.fields.chunk_text}, category: ${hit.fields.category}`);
  });
  ```

  ```go Go
  // Add to the main function:
  // Search the dense index and rerank results
  topN := int32(10)
  resReranked, err := idxConnection.SearchRecords(ctx, &pinecone.SearchRecordsRequest{
      Query: pinecone.SearchRecordsQuery{
          TopK: 10,
          Inputs: &map[string]interface{}{
              "text": query,
          },
      },
      Rerank: &pinecone.SearchRecordsRerank{
          Model:      "bge-reranker-v2-m3",
          TopN:       &topN,
          RankFields: []string{"chunk_text"},
      },
  })
  if err != nil {
      log.Fatalf("Failed to search records: %v", err)
  }
  fmt.Printf(prettifyStruct(resReranked))
  ```
</CodeGroup>

Notice that all of the most relevant results about historical structures and monuments are now ranked highest.

<CodeGroup>
  ```console Python
  id: rec1  | score: 0.11  | category: history    | text: The Eiffel Tower was completed in 1889 and stands in Paris, France.
  id: rec38 | score: 0.06  | category: history    | text: The Taj Mahal is a mausoleum built by Emperor Shah Jahan.
  id: rec7  | score: 0.06  | category: history    | text: The Great Wall of China was built to protect against invasions.
  id: rec17 | score: 0.02  | category: history    | text: The Pyramids of Giza are among the Seven Wonders of the Ancient World.
  id: rec26 | score: 0.01  | category: history    | text: Rome was once the center of a vast empire.        
  id: rec15 | score: 0.01  | category: art        | text: Leonardo da Vinci painted the Mona Lisa.          
  id: rec5  | score: 0.0   | category: literature | text: Shakespeare wrote many famous plays, including Hamlet and Macbeth.
  id: rec47 | score: 0.0   | category: history    | text: The Industrial Revolution transformed manufacturing and transportation.
  id: rec50 | score: 0.0   | category: energy     | text: Renewable energy sources include wind, solar, and hydroelectric power.
  id: rec3  | score: 0.0   | category: science    | text: Albert Einstein developed the theory of relativity.
  ```

  ```console JavaScript
  id: rec1, score: 0.11, text: The Eiffel Tower was completed in 1889 and stands in Paris, France., category: history
  id: rec38, score: 0.06, text: The Taj Mahal is a mausoleum built by Emperor Shah Jahan., category: history
  id: rec7, score: 0.06, text: The Great Wall of China was built to protect against invasions., category: history
  id: rec17, score: 0.02, text: The Pyramids of Giza are among the Seven Wonders of the Ancient World., category: history
  id: rec26, score: 0.01, text: Rome was once the center of a vast empire., category: history
  id: rec15, score: 0.01, text: Leonardo da Vinci painted the Mona Lisa., category: art
  id: rec5, score: 0.00, text: Shakespeare wrote many famous plays, including Hamlet and Macbeth., category: literature
  id: rec47, score: 0.00, text: The Industrial Revolution transformed manufacturing and transportation., category: history
  id: rec50, score: 0.00, text: Renewable energy sources include wind, solar, and hydroelectric power., category: energy
  id: rec3, score: 0.00, text: Albert Einstein developed the theory of relativity., category: science
  ```

  ```json Go [expandable]
  {
    "result": {
      "hits": [
        {
          "_id": "rec1",
          "_score": 0.10743748,
          "fields": {
            "category": "history",
            "chunk_text": "The Eiffel Tower was completed in 1889 and stands in Paris, France."
          }
        },
        {
          "_id": "rec38",
          "_score": 0.064535476,
          "fields": {
            "category": "history",
            "chunk_text": "The Taj Mahal is a mausoleum built by Emperor Shah Jahan."
          }
        },
        {
          "_id": "rec7",
          "_score": 0.062445287,
          "fields": {
            "category": "history",
            "chunk_text": "The Great Wall of China was built to protect against invasions."
          }
        },
        {
          "_id": "rec17",
          "_score": 0.0153063545,
          "fields": {
            "category": "history",
            "chunk_text": "The Pyramids of Giza are among the Seven Wonders of the Ancient World."
          }
        },
        {
          "_id": "rec26",
          "_score": 0.010652511,
          "fields": {
            "category": "history",
            "chunk_text": "Rome was once the center of a vast empire."
          }
        },
        {
          "_id": "rec15",
          "_score": 0.007876706,
          "fields": {
            "category": "art",
            "chunk_text": "Leonardo da Vinci painted the Mona Lisa."
          }
        },
        {
          "_id": "rec5",
          "_score": 0.00003194182,
          "fields": {
            "category": "literature",
            "chunk_text": "Shakespeare wrote many famous plays, including Hamlet and Macbeth."
          }
        },
        {
          "_id": "rec47",
          "_score": 0.000017502925,
          "fields": {
            "category": "history",
            "chunk_text": "The Industrial Revolution transformed manufacturing and transportation."
          }
        },
        {
          "_id": "rec50",
          "_score": 0.00001631454,
          "fields": {
            "category": "energy",
            "chunk_text": "Renewable energy sources include wind, solar, and hydroelectric power."
          }
        },
        {
          "_id": "rec3",
          "_score": 0.000015936621,
          "fields": {
            "category": "science",
            "chunk_text": "Albert Einstein developed the theory of relativity."
          }
        }
      ]
    },
    "usage": {
      "read_units": 6,
      "embed_total_tokens": 8,
      "rerank_units": 1
    }
  }
  ```
</CodeGroup>

## 7. Improve results

[Reranking results](/guides/search/rerank-results) is one of the most effective ways to improve search accuracy and relevance, but there are many other techniques to consider. For example:

* [Filtering by metadata](/guides/search/filter-by-metadata): When records contain additional metadata, you can limit the search to records matching a [filter expression](/guides/index-data/indexing-overview#metadata-filter-expressions).

* [Hybrid search](/guides/search/hybrid-search): You can add [lexical search](/guides/search/lexical-search) to capture precise keyword matches (e.g., product SKUs, email addresses, domain-specific terms) in addition to semantic matches.

* [Chunking strategies](https://www.pinecone.io/learn/chunking-strategies/): You can chunk your content in different ways to get better results. Consider factors like the length of the content, the complexity of queries, and how results will be used in your application.

## 8. Clean up

When you no longer need your example index, delete it as follows:

<CodeGroup>
  ```python Python
  # Delete the index
  pc.delete_index(index_name)
  ```

  ```javascript JavaScript
  // Delete the index
  await pc.deleteIndex(indexName);
  ```

  ```go Go
  // Add to the main function:
  // Delete the index
  err = pc.DeleteIndex(ctx, indexName)
  if err != nil {
      log.Fatalf("Failed to delete index: %v", err)
  } else {
      fmt.Println("Index \"%v\" deleted successfully", indexName)
  }
  ```
</CodeGroup>

<Tip>
  For production indexes, consider [enabling deletion protection](/guides/manage-data/manage-indexes#configure-deletion-protection).
</Tip>

## Next steps

<CardGroup cols={3}>
  <Card title="Index data" icon="book-open" href="/guides/index-data/indexing-overview">
    Learn more about storing data in Pinecone
  </Card>

  <Card title="Search" icon="magnifying-glass" href="/guides/search/search-overview">
    Explore different forms of vector search.
  </Card>

  <Card title="Optimize" icon="rocket" href="/guides/optimize">
    Find out how to improve performance
  </Card>

  {/* <Card title="Examples" icon="grid-round" iconType="solid" href="/examples">
          Try example notebooks and sample apps
      </Card>
      <Card title="API reference" icon="code-simple" href="/reference">
          Comprehensive details about the Pinecone APIs, SDKs, utilities, and architecture.
      </Card>
      <Card title="Integrations" icon="link-simple" href="/integrations">
          Pinecone's growing number of third-party integrations.
      </Card> */}
</CardGroup>
