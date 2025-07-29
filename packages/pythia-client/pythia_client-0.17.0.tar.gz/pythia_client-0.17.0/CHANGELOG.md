#### v0.17.0
- Package structure refactoring. Compatible with `pythia-api` v1.28.0

#### v0.16.0

- Refactoring due to type checking of some output. Compatible with `pythia-api` v1.27.0

#### v0.15.0

- Alpha for new method agent_stream. Compatible with `pythia-api` v1.26.0

#### v0.14.0
- Retrieve method for no generation chunk retrieval. Compatible with `pythia-api` v1.25.0

#### v0.13.0
- New methods for the Thread endpoints. Compatible with `pythia-api` v1.24.0

#### v0.12.0
- Remove ALIE endpoints. Make it possible to have both string and files in data extraction endpoint. Compatible with `pythia-api` v1.23.0

#### v0.11.0
- Add the get metrics method for query history. Compatible with `pythia-api` v1.22.0

#### v0.10.3
- List query method now accept date filters. Compatible with `pythia-api` v1.21.0

#### v0.10.2
- Small schema fix ChatMessage roles. Compatible with `pythia-api` v1.20.0

#### v0.10.1
- Small schema fix for Query response, Task/Data-extract response to add detailed token consumption. Compatible with `pythia-api` v1.19.0

#### v0.10.0
- Deprecated `extract_pk_list` and `get_extract_pk_list_results` in favor of a heavy refactor of the `extract_structured_data` method that is customizable enough to support all use-cases. New method `get_extract_structured_data_job` to retrieve the job results. Compatible with `pythia-api` v1.18.0

#### v0.9.0
- Add `get_document_metadata` and `update_document_metadata` that allow metadata listing and updating for a document. Compatible with `pythia-api` v1.16.0 and v1.17.0

#### v0.8.1
- Add  the `facets_count` and `facets_values` method that allow doing facets on documents metadata to either get the count of document verifying a specific filter (`count`) or get a list of values for a metadata field verifying an optional filter (`values`: for example keywords available for specific a pythia document category). All methods like `get_keywords` and `get_docs_by_groupd_id or pythia_category` become deprecated now as these cover all their usage and more. Compatible `pythia-api` v1.15.0

#### v0.7.0
- Add  the `chat` method which is the same as the `query` method, but it can also trigger a quick answer mechanism that answer without using RAG. Compatible `pythia-api` v1.14.0
 
#### v0.6.3
- Add `group_by` and `group_size` params to Query method. Compatible `pythia-api` v1.13.1

#### v0.6.1
- Entity prediction endpoints. Big schema update (with Pydantic Fields). Add query feedback comment/uuid
  Compatible `pythia-api` v1.12.0

#### v0.5.1
- PK List extraction endpoints. Draw endpoints. Following the renaming according to convention of Rest API routes.
  Compatible `pythia-api` v1.11.0

#### v0.4.4
- Now raise error with API status code and message instead of None when crashing. Sentry integration.
  Compatible `pythia-api` v1.10.0

#### v0.3.6

- Add query history and feedback mechanism. Compatible `pythia-api` v1.9.0

#### v0.3.5

- Add Tika indexation mode. Compatible `pythia-api` v1.8.0

#### v0.3.4

- Add native qdrant filters compatibility. Compatible `pythia-api` v1.7.0

#### v0.3.3
- Small rework of the handling of parameters + new paremeters about threshold and returning embedding for light_query.
  Compatible `pythia-api` v1.6.0

#### v0.3.1

- New light_query function to do fast hybrid retrieval without LLM generated answer. Compatible `pythia-api` v1.5.0

#### v0.3.0

- New API key management functions (add, list, revoke). Compatible `pythia-api` v1.4.0

#### v0.2.4

- New optional priority_queue boolean for indexing job function. Compatible `pythia-api` v1.3.0

#### v0.2.3

- New function to get available documents for a specific group_id or pythia_document_category. Compatible with
  `pythia-api` v1.2.0
 
#### v0.2.2

- New function to get available keywords for a specific group_id or pythia_document_category. Compatible with
  `pythia-api` v1.1.0

#### v0.2.1

- Remove print debug. Compatible with `pythia-api` v1.0.0

#### v0.2.0

- Rewrote for future compatibility with the Pythia using PostGre. New endpoints (get files infos). Compatible with
  `pythia-api` v1.0.0

#### v0.1.10

- Remove req for Python 3.11 (>3.8 now). Compatible with `pythia-api` v0.2.4

#### v0.1.9

- Top K params for query function. Compatible with `pythia-api` v0.2.4

#### v0.1.8

- Custom system prompt params for query endpoint. Compatible with `pythia-api` v0.2.3

#### v0.1.7

- MetaJSON schema fix for Mistral models. Compatible with `pythia-api` v0.2.2

#### v0.1.6

- New intent functions: add_intent, predict_intent, delete_intent. Compatible with `pythia-api` v0.2.1

#### v0.1.4
- Minor ESR Ticket schema fix

#### v0.1.3

- Minor modification of Schema for structured data extraction. Compatible with `pythia-api` v0.2.0

#### v0.1.0

- Major refactor of endpoints and function name to follow `pythia-api` refactoring

#### v0.0.11

- Renaming `owner` to `owner`. Compatible with `pythia-api` v0.0.5

#### v0.0.10

- Fix Schema to make score optional (Qdrant compatibility). Compatible with `pythia-api` v0.0.5

#### v0.0.9

- `upload_files` now return a simple json indicating that the background indexing task have been acception. New
  `get_indexing_tasks` function take an `owner` value as parameters and return the top 20 most recent indexing task and
  their results or status. New optional `owner` parameter for the query endpoint to indicate which user sent the message
  in the DB table log. Compatible with `pythia-api` v0.0.5

#### v0.0.8
- NEW: New optional parameter `chat_history` in the `.query()` method. It allows to add previous exchange with the LLM to the new query. Chat History must follow the ChatMessages format (dict containing: content, role, name, meta), see https://docs.haystack.deepset.ai/v2.0/docs/data-classes#chatmessage
- Compatible with `pythia-api` v0.0.4

#### v0.0.7

- New response Schema for the pythia-api after version bump and removal of LiteLLM.

#### v0.0.6
- Added the new parameter `return_content` to the `get_docs_by_filters` method. The method `get_docs_by_filters` now by default doesn't return document content (to save on bandwidth). Set `return_content` to `True` to return the content of the documents.  

#### v0.0.5

- Initial Release. Compatible with `pythia-api` v0.0.1