# CRAG-MM Search APIs

CRAG-MM is a visual question-answering benchmark that focuses on factuality of Retrieval Augmented Generation (RAG). It offers a unique collection of image and question-answering sets to enable comprehensive assessment of wearable devices.

## CRAG-MM Search API Description

The CRAG-MM Search API is a Python library that provides a unified interface for searching images and text. It supports both image and text queries, and can be used to retrieve relevant information from a given set of retrieved contents.

The *image search* API uses CLIP embeddings to encode the images. It takes an image or an image url as input and returns a list of similar images with the relevant information about the entities contained in the image. Similarity is determined by cosine similarity of the embeddings. See *Search for images* below for an example.

The *web search* API uses chromadb full text search to build an index for pre-fetched web search results. It takes a text query as input, and returns relevant webpage urls and meta data such as page title and page snippets. You can download the webpage content based on the urls and use the information to build Retreival Augmented Generation (RAG) systems. Here, relevancy of the webpages are calculated based on cosine similarity. See *Search for text queries* below for an example.

Main class - `search.py`, contains UnifiedSearch class to handle image and text search.

demo - `python demo.py`


## Installation

```bash
pip install cragmm-search-pipeline==0.4.2
```

## Usage
### Task 1
```python
from cragmm_search.search import UnifiedSearchPipeline

# initiate image search API only
search_pipeline = UnifiedSearchPipeline(
    image_model_name="openai/clip-vit-large-patch14-336",
    image_hf_dataset_id="crag-mm-2025/image-search-index-validation",
)
```


### Task 2

```python
from cragmm_search.search import UnifiedSearchPipeline

# initiate both image and web search API
search_pipeline = UnifiedSearchPipeline(
    image_model_name="openai/clip-vit-large-patch14-336",
    image_hf_dataset_id="crag-mm-2025/image-search-index-validation",
    text_model_name="sentence-transformers/all-MiniLM-L6-v2",
    web_hf_dataset_id="crag-mm-2025/web-search-index-validation",
)
```

### Task 2 - private / interal evaluator

```python
from cragmm_search.search import UnifiedSearchPipeline

# initiate both image and web search API
search_pipeline = UnifiedSearchPipeline(
    image_model_name="openai/clip-vit-large-patch14-336",
    image_hf_dataset_id="crag-mm-2025/image-search-index-public-test",
    text_model_name="sentence-transformers/all-MiniLM-L6-v2",
    web_hf_dataset_id="crag-mm-2025/web-search-index-public-test",
    web_hf_dataset_id_private="crag-mm-2025/web-search-contents-db-private",
)
# result keys: ['index', 'score', 'page_name', 'page_url', 'page_snippet', 'page_result', 'page_last_modified', 'search_result_type']
```

### Get all image urls in the index
```python
img_urls = search_pipeline._get_all_image_urls()
# returns a list of unique image urls
```

### Search for images

```python
# Search the pipeline with an image
image_path = "data/image_sample.jpg"
print(f"Searching for: '{image_path}'")
results = search_pipeline(image_path, k=2)
print("Image search results:")
assert results is not None, "No results found"
for result in results:
    print(result)
```

#### Output
```
{
   "index":4065,
   "score":0.9726169109344482,
   "url":"https://upload.wikimedia.org/wikipedia/commons/3/3d/Front_view_of_Statue_of_Liberty_with_pedestal_and_base_2024.jpg",
   "entities":[
      {
         "entity_name":"Statue of Liberty",
         "entity_attributes":{
            "alternative_names":"Liberty Enlightening the World",
            "location":"Liberty Island, New York City",
            "height_of_copper_statue":"151 ft 1 in",
            "height_from_ground_level_to_torch":"305 ft 1 in",
            "sculptor":"Frédéric Auguste Bartholdi",
            "dedication_date":"October 28, 1886"
         }
      }
   ]
}{
   "index":3752,
   "score":0.86649090051651,
   "url":"https://upload.wikimedia.org/wikipedia/commons/e/ed/Currier_and_Ives_Liberty2.jpg",
   "entities":[
      {
         "entity_name":"Statue of Liberty",
         "entity_attributes":{
            "alternative_names":"Liberty Enlightening the World",
            "location":"Liberty Island, New York City",
            "height_of_copper_statue":"151 ft 1 in",
            "height_from_ground_level_to_torch":"305 ft 1 in",
            "sculptor":"Frédéric Auguste Bartholdi",
            "dedication_date":"October 28, 1886"
         }
      }
   ]
}
```

### Search for text queries

```python
# Search the pipeline with a text query
text_query = "how long are the leaves of Tradescantia Zebrina?"
print(f"Searching for: '{text_query}'")
results = search_pipeline(text_query, k=3)
for result in results:
    print(result)
```

#### Output
```
Searching for: 'how long are the leaves of Tradescantia Zebrina?'
{
	'index': 38214,
	'score': 0.6437532901763916,
	'page_name': 'Tradescantia zebrina - Wikipedia',
	'page_snippet': 'The stalked, parallel-veined leaves are mostly ovate, 4 to 10 cm long and 1.5 to 3 cm wide, pointed towards the tip, rounded to the base. The upper surface is glabrous to mildly hairy, the underside hairless to averagely hairy, ciliate towards the leaf base. The structure of the flower—usually ...Tradescantia zebrina has attractive zebra-patterned leaves, the upper surface showing purple new growth and green older growth parallel to the central axis, as well as two broad silver-colored stripes on the outer edges, with the lower leaf surface presenting a deep uniform magenta. The leaves are bluish green and usually have two longitudinal stripes that are silvery on the surface and purple on the underside. The stalked, parallel-veined leaves are mostly ovate, 4 to 10 cm long and 1.5 to 3 cm wide, pointed towards the tip, rounded to the base. The upper surface is glabrous to mildly hairy, the underside hairless to averagely hairy, ciliate towards the leaf base. The structure of the flower—usually from the three pink petals and the white sexual organs—is similar to that of the other Tradescantia, but unlike what happens in those, the plant branches off thanks to new buds whose attachment starts below that of the leaf (and not above). The three only grown at the base petals are ovate-blunt, pink to purple and 5 to 9 mm long. The six equally sized stamens are violet hairy. Three carpels have become a top permanent ovary grown. They form capsule fruits that contain gray-brown seeds. Skin irritation may result from repeated contact with or prolonged handling of the plant—particularly from the clear, watery sap (a characteristic unique to T. zebrina as compared with the other aforementioned types). Tradescantia zebrina is native to Mexico, Central America, and Colombia, but can also be found on the Caribbean islands. It is classified as a Category 1b Invasive Species in South Africa, and thus may no longer be planted or propagated. All trade in seeds, cuttings or other propagative material is prohibited. It may not be transported or be allowed to disperse, either in rural or urban areas. It is also an invasive species in the Galápagos Islands. Tradescantia zebrina var. Tradescantia zebrina, formerly known as Zebrina pendula, is a species of creeping plant in the Tradescantia genus. Common names include silver inch plant and wandering Jew. The latter name is controversial, and some now use the alternative wandering dude. The plant is popular in cultivation due to its fast growth and attractive foliage.',
	'page_url': 'https://en.wikipedia.org/wiki/Tradescantia_zebrina'
} {
	'index': 38228,
	'score': 0.6077773571014404,
	'page_name': 'Tradescantia Care Guide | The Little Botanical',
	'page_snippet': 'Our Tradescantia care guide helps your stripy, silvery green and purple leaved friend grow and thrive in your home. Learn more now!The name “Tradescantia” is in honour of John Tradescant, who was King Charles I of England’s gardener. Similarly, “Zebrina” means “zebra” in Portuguese. Aim to water your plant once every 7-10 days, allowing the top few cms of soil to dry out first · Give your plant the occasional trim to keep the leaves fresh and encourage new growth Place your plant in a bright to medium-lit spot, to maintain the vibrant colours of the leaves. Tradescantias enjoy lots of humidity, making them the perfect plants for kitchens and bathrooms. The Tradescantia Zebrina can also be mildly toxic if ingested, so keep it away from small children and curious pets. To maintain its beautiful purple colour, make sure it gets good light. A sunny window sill is perfect. If your plant doesn’t have access to enough light, the leaves will fade, becoming dull over time. ... Meet our enchanting Tradescantia Zebrina, its mesmerising striped foliage trails beautifully as it grows. A very popular, on-trend gang of trailing house plants. Why not add them to a high shelf and just watch those gorgeous leaves grow and trail. ... This week we’re bringing you all you need to know about the gorgeous Tradescantia Zebrina.',
	'page_url': 'https://thelittlebotanical.com/guides/tradescantia-care-guide/'
} {
	'index': 38212,
	'score': 0.6041664481163025,
	'page_name': 'How to Care for Tradescantia Zebrina | The Little Botanical',
	'page_snippet': 'Discover all you need to know to care for Tradescantia Zebrina, named for his zebra-like pattern, to keep him happy and healthy.This week we’re bringing you all you need to know about the gorgeous Tradescantia Zebrina. With his trademark stripy leaves this guy is strangely reminiscent of a zebra, so if you want to add some dazzle to your indoor jungle, then this is the plant for you. Not only does he look fab with his unusual stripy leaves in hues of green, silver and deep purple and thick juicy stems, he’s also a fast-growing, stunning houseplant. He’s undeniably an all-round winning addition to your indoor plant line up, we’ll think you’ll be going wild for this guy. Read on to discover all you need to know to care for Tradescantia Zebrina to keep him happy and healthy. Give your Tradescantia Zebrina a drink every 7 to 10 days once the top couple of centimetres of soil has dried out. Push your thumb a few centimetres into the top of the soil and if it feels dry then your plant is ready for a water. He will need water less frequently in the winter than in the summer. Make sure your plant is not left sitting in water as this can cause root rot. To maintain the lovely purple hue on the leaves, place your plant in a warm, bright and sunny spot. Here at TLB we make it oh-so-simple to add botanical style to your indoor décor and the Tradescantia Zebrina is no exception. The stunning tri-colour leaves of this beauty really pop when planted in our bespoke stoneware in natural shades of almond, charcoal or grey.',
	'page_url': 'https://thelittlebotanical.com/how-to-care-for-your-tradescantia-zebrina/'
}
```

Note: The Search APIs only return urls for images and webpages, instead of full contents. To get the full webpage contents and images, you will have to download it yourself. During the challenge, participants can assume that the connection to these urls are available. 

### More examples

```bash
python demo.py
```

## Build the search API.

### Generate image index

```bash
python image_search_mock_api/generate_index.py --index-data-dir data/image_index_data --output-dir image_search_mock_api/mock_kg_test`
```

### Generate web search index

```bash
python web_search_mock_api/generate_index.py --input web_search_mock_api/corpus/chunked
```
