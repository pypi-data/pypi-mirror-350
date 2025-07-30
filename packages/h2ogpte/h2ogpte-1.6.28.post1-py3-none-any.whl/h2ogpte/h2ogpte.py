# This file was generated from `h2ogpte_async.py` by executing `make generate-sync-mux-py`.

from pathlib import Path
from typing import Iterable, Any, Union, List, Dict, Tuple
from h2ogpte.types import *
from h2ogpte.connectors import *
from h2ogpte.h2ogpte_async import H2OGPTEAsync
from h2ogpte.h2ogpte_sync_base import H2OGPTESyncBase

# Import Session to be be accessible via `from h2ogpte.h2ogpte import Session`
from h2ogpte.session import Session


class H2OGPTE(H2OGPTESyncBase):
    """Connect to and interact with an h2oGPTe server."""

    def answer_question(
        self,
        question: str,
        system_prompt: Union[str, None] = "",
        pre_prompt_query: Union[str, None] = None,
        prompt_query: Union[str, None] = None,
        text_context_list: Union[List[str], None] = None,
        llm: Union[str, int, None] = None,
        llm_args: Union[Dict[str, Any], None] = None,
        chat_conversation: Union[List[Tuple[str, str]], None] = None,
        guardrails_settings: Union[Dict, None] = None,
        timeout: Union[float, None] = None,
        **kwargs: Any,
    ) -> Answer:
        """Send a message and get a response from an LLM.

        Note: This method is only recommended if you are passing a chat conversation or for low-volume testing.
        For general chat with an LLM, we recommend session.query() for higher throughput in multi-user environments.
        The following code sample shows the recommended method:

        .. code-block:: python

            # Establish a chat session
            chat_session_id = client.create_chat_session()
            # Connect to the chat session
            with client.connect(chat_session_id) as session:
                # Send a basic query and print the reply
                reply = session.query("Hello", timeout=60)
                print(reply.content)


        Format of inputs content:

            .. code-block::

                {text_context_list}
                \"\"\"\\n{chat_conversation}{question}

        Args:
            question:
                Text query to send to the LLM.
            text_context_list:
                List of raw text strings to be included, will be converted to a string like this: "\n\n".join(text_context_list)
            system_prompt:
                Text sent to models which support system prompts. Gives the model
                overall context in how to respond. Use `auto` for the model default, or None for h2oGPTe default. Defaults
                to '' for no system prompt.
            pre_prompt_query:
                Text that is prepended before the contextual document chunks in text_context_list. Only used if text_context_list is provided.
            prompt_query:
                Text that is appended after the contextual document chunks in text_context_list. Only used if text_context_list is provided.
            llm:
                Name or index of LLM to send the query. Use `H2OGPTE.get_llms()` to see all available options.
                Default value is to use the first model (0th index).
            llm_args:
                Dictionary of kwargs to pass to the llm. Valid keys:
                    temperature (float, default: 0) — The value used to modulate the next token probabilities. Most deterministic: 0, Most creative: 1
                    seed (int, default: 0) — The seed for the random number generator, only used if temperature > 0, seed=0 will pick a random number for each call, seed > 0 will be fixed.
                    top_k (int, default: 1) — The number of highest probability vocabulary tokens to keep for top-k-filtering.
                    top_p (float, default: 1.0) — If set to float < 1, only the smallest set of most probable tokens with probabilities that add up to top_p or higher are kept for generation.
                    repetition_penalty (float, default: 1.07) — The parameter for repetition penalty. 1.0 means no penalty.
                    max_new_tokens (int, default: 1024) — Maximum number of new tokens to generate. This limit applies to each (map+reduce) step during summarization and each (map) step during extraction.
                    min_max_new_tokens (int, default: 512) — minimum value for max_new_tokens when auto-adjusting for content of prompt, docs, etc.
                    response_format (str, default: "text") — Output type, one of ["text", "json_object", "json_code"].
                    guided_json (dict, default: None) — If specified, the output will follow the JSON schema.
                    guided_regex (str, default: "") — If specified, the output will follow the regex pattern. Only for models that support guided generation: check output of get_llms() for guided_vllm flag.
                    guided_choice (Optional[List[str]], default: None — If specified, the output will be exactly one of the choices. Only for models that support guided generation: check output of get_llms() for guided_vllm flag.
                    guided_grammar (str, default: "") — If specified, the output will follow the context free grammar. Only for models that support guided generation: check output of get_llms() for guided_vllm flag.
                    guided_whitespace_pattern (str, default: "") — If specified, will override the default whitespace pattern for guided json decoding. Only for models that support guided generation: check output of get_llms() for guided_vllm flag.
            chat_conversation:
                List of tuples for (human, bot) conversation that will be pre-appended
                to an (question, None) case for a query.
            guardrails_settings:
                Guardrails Settings.
            timeout:
                Timeout in seconds.
            kwargs:
                Dictionary of kwargs to pass to h2oGPT. Not recommended, see https://github.com/h2oai/h2ogpt for source code. Valid keys:
                    h2ogpt_key: str = ""
                    chat_conversation: list[tuple[str, str]] | None = None
                    docs_ordering_type: str | None = "best_near_prompt"
                    max_input_tokens: int = -1
                    docs_token_handling: str = "split_or_merge"
                    docs_joiner: str = "\n\n"
                    image_file: Union[str, list] = None

        Returns:
            Answer: The response text and any errors.
        Raises:
            TimeoutError: If response isn't completed in timeout seconds.
        """

        def call(c: H2OGPTEAsync):
            return c.answer_question(
                question,
                system_prompt,
                pre_prompt_query,
                prompt_query,
                text_context_list,
                llm,
                llm_args,
                chat_conversation,
                guardrails_settings,
                timeout,
                **kwargs,
            )

        return self._run_async(call)

    def summarize_content(
        self,
        text_context_list: Union[List[str], None] = None,
        system_prompt: str = "",
        pre_prompt_summary: Union[str, None] = None,
        prompt_summary: Union[str, None] = None,
        llm: Union[str, int, None] = None,
        llm_args: Union[Dict[str, Any], None] = None,
        guardrails_settings: Union[Dict, None] = None,
        timeout: Union[float, None] = None,
        **kwargs: Any,
    ) -> Answer:
        """Summarize one or more contexts using an LLM.

        Effective prompt created (excluding the system prompt):

        .. code-block::

            "{pre_prompt_summary}
            \"\"\"
            {text_context_list}
            \"\"\"
            {prompt_summary}"

        Args:
            text_context_list:
                List of raw text strings to be summarized.
            system_prompt:
                Text sent to models which support system prompts. Gives the model
                overall context in how to respond. Use `auto` for the model default or None for h2oGPTe defaults. Defaults
                to '' for no system prompt.
            pre_prompt_summary:
                Text that is prepended before the list of texts. The default can be
                customized per environment, but the standard default is :code:`"In order to write a concise single-paragraph
                or bulleted list summary, pay attention to the following text:\\\\n"`
            prompt_summary:
                Text that is appended after the list of texts. The default can be customized
                per environment, but the standard default is :code:`"Using only the text above, write a condensed and concise
                summary of key results (preferably as bullet points):\\\\n"`
            llm:
                Name or index of LLM to send the query. Use `H2OGPTE.get_llms()` to see all available options.
                Default value is to use the first model (0th index).
            llm_args:
                Dictionary of kwargs to pass to the llm. Valid keys:
                    temperature (float, default: 0) — The value used to modulate the next token probabilities. Most deterministic: 0, Most creative: 1
                    seed (int, default: 0) — The seed for the random number generator, only used if temperature > 0, seed=0 will pick a random number for each call, seed > 0 will be fixed.
                    top_k (int, default: 1) — The number of highest probability vocabulary tokens to keep for top-k-filtering.
                    top_p (float, default: 1.0) — If set to float < 1, only the smallest set of most probable tokens with probabilities that add up to top_p or higher are kept for generation.
                    repetition_penalty (float, default: 1.07) — The parameter for repetition penalty. 1.0 means no penalty.
                    max_new_tokens (int, default: 1024) — Maximum number of new tokens to generate. This limit applies to each (map+reduce) step during summarization and each (map) step during extraction.
                    min_max_new_tokens (int, default: 512) — minimum value for max_new_tokens when auto-adjusting for content of prompt, docs, etc.
                    response_format (str, default: "text") — Output type, one of ["text", "json_object", "json_code"].
                    guided_json (dict, default: None) — If specified, the output will follow the JSON schema.
                    guided_regex (str, default: "") — If specified, the output will follow the regex pattern. Only for models that support guided generation: check output of get_llms() for guided_vllm flag.
                    guided_choice (Optional[List[str]], default: None — If specified, the output will be exactly one of the choices. Only for models that support guided generation: check output of get_llms() for guided_vllm flag.
                    guided_grammar (str, default: "") — If specified, the output will follow the context free grammar. Only for models that support guided generation: check output of get_llms() for guided_vllm flag.
                    guided_whitespace_pattern (str, default: "") — If specified, will override the default whitespace pattern for guided json decoding. Only for models that support guided generation: check output of get_llms() for guided_vllm flag.
            guardrails_settings:
                Guardrails Settings.
            timeout:
                Timeout in seconds.
            kwargs:
                Dictionary of kwargs to pass to h2oGPT. Not recommended, see https://github.com/h2oai/h2ogpt for source code. Valid keys:
                    h2ogpt_key: str = ""
                    chat_conversation: list[tuple[str, str]] | None = None
                    docs_ordering_type: str | None = "best_near_prompt"
                    max_input_tokens: int = -1
                    docs_token_handling: str = "split_or_merge"
                    docs_joiner: str = "\n\n"
                    image_file: Union[str, list] = None

        Returns:
            Answer: The response text and any errors.
        Raises:
            TimeoutError: If response isn't completed in timeout seconds.
        """

        def call(c: H2OGPTEAsync):
            return c.summarize_content(
                text_context_list,
                system_prompt,
                pre_prompt_summary,
                prompt_summary,
                llm,
                llm_args,
                guardrails_settings,
                timeout,
                **kwargs,
            )

        return self._run_async(call)

    def extract_data(
        self,
        text_context_list: Union[List[str], None] = None,
        system_prompt: str = "",
        pre_prompt_extract: Union[str, None] = None,
        prompt_extract: Union[str, None] = None,
        llm: Union[str, int, None] = None,
        llm_args: Union[Dict[str, Any], None] = None,
        guardrails_settings: Union[Dict, None] = None,
        timeout: Union[float, None] = None,
        **kwargs: Any,
    ) -> ExtractionAnswer:
        """Extract information from one or more contexts using an LLM.

        pre_prompt_extract and prompt_extract variables must be used together. If these
        variables are not set, the inputs texts will be summarized into bullet points.

        Format of extract content:

            .. code-block::

                "{pre_prompt_extract}\"\"\"
                {text_context_list}
                \"\"\"\\n{prompt_extract}"

        Examples:

            .. code-block:: python

                extract = h2ogpte.extract_data(
                    text_context_list=chunks,
                    pre_prompt_extract="Pay attention and look at all people. Your job is to collect their names.\\n",
                    prompt_extract="List all people's names as JSON.",
                )

        Args:
            text_context_list:
                List of raw text strings to extract data from.
            system_prompt:
                Text sent to models which support system prompts. Gives the model
                overall context in how to respond. Use `auto` or None for the model default. Defaults
                to '' for no system prompt.
            pre_prompt_extract:
                Text that is prepended before the list of texts. If not set,
                the inputs will be summarized.
            prompt_extract:
                Text that is appended after the list of texts. If not set, the inputs will be summarized.
            llm:
                Name or index of LLM to send the query. Use `H2OGPTE.get_llms()` to see all available options.
                Default value is to use the first model (0th index).
            llm_args:
                Dictionary of kwargs to pass to the llm. Valid keys:
                    temperature (float, default: 0) — The value used to modulate the next token probabilities. Most deterministic: 0, Most creative: 1
                    seed (int, default: 0) — The seed for the random number generator, only used if temperature > 0, seed=0 will pick a random number for each call, seed > 0 will be fixed.
                    top_k (int, default: 1) — The number of highest probability vocabulary tokens to keep for top-k-filtering.
                    top_p (float, default: 1.0) — If set to float < 1, only the smallest set of most probable tokens with probabilities that add up to top_p or higher are kept for generation.
                    repetition_penalty (float, default: 1.07) — The parameter for repetition penalty. 1.0 means no penalty.
                    max_new_tokens (int, default: 1024) — Maximum number of new tokens to generate. This limit applies to each (map+reduce) step during summarization and each (map) step during extraction.
                    min_max_new_tokens (int, default: 512) — minimum value for max_new_tokens when auto-adjusting for content of prompt, docs, etc.
                    response_format (str, default: "text") — Output type, one of ["text", "json_object", "json_code"].
                    guided_json (dict, default: None) — If specified, the output will follow the JSON schema.
                    guided_regex (str, default: "") — If specified, the output will follow the regex pattern. Only for models that support guided generation: check output of get_llms() for guided_vllm flag.
                    guided_choice (Optional[List[str]], default: None — If specified, the output will be exactly one of the choices. Only for models that support guided generation: check output of get_llms() for guided_vllm flag.
                    guided_grammar (str, default: "") — If specified, the output will follow the context free grammar. Only for models that support guided generation: check output of get_llms() for guided_vllm flag.
                    guided_whitespace_pattern (str, default: "") — If specified, will override the default whitespace pattern for guided json decoding. Only for models that support guided generation: check output of get_llms() for guided_vllm flag.
            guardrails_settings:
                Guardrails Settings.
            timeout:
                Timeout in seconds.
            kwargs:
                Dictionary of kwargs to pass to h2oGPT. Not recommended, see https://github.com/h2oai/h2ogpt for source code. Valid keys:
                    h2ogpt_key: str = ""
                    chat_conversation: list[tuple[str, str]] | None = None
                    docs_ordering_type: str | None = "best_near_prompt"
                    max_input_tokens: int = -1
                    docs_token_handling: str = "split_or_merge"
                    docs_joiner: str = "\n\n"
                    image_file: Union[str, list] = None

        Returns:
            ExtractionAnswer: The list of text responses and any errors.
        Raises:
            TimeoutError: If response isn't completed in timeout seconds.
        """

        def call(c: H2OGPTEAsync):
            return c.extract_data(
                text_context_list,
                system_prompt,
                pre_prompt_extract,
                prompt_extract,
                llm,
                llm_args,
                guardrails_settings,
                timeout,
                **kwargs,
            )

        return self._run_async(call)

    def cancel_job(self, job_id: str) -> Result:
        """Stops a specific job from running on the server.

        Args:
            job_id:
                String id of the job to cancel.

        Returns:
            Result: Status of canceling the job.
        """

        def call(c: H2OGPTEAsync):
            return c.cancel_job(job_id)

        return self._run_async(call)

    def count_chat_sessions(self) -> int:
        """Counts number of chat sessions owned by the user.

        Returns:
            int: The count of chat sessions owned by the user.
        """

        def call(c: H2OGPTEAsync):
            return c.count_chat_sessions()

        return self._run_async(call)

    def count_chat_sessions_for_collection(self, collection_id: str) -> int:
        """Counts number of chat sessions in a specific collection.

        Args:
            collection_id:
                String id of the collection to count chat sessions for.

        Returns:
            int: The count of chat sessions in that collection.
        """

        def call(c: H2OGPTEAsync):
            return c.count_chat_sessions_for_collection(collection_id)

        return self._run_async(call)

    def count_collections(self) -> int:
        """Counts number of collections owned by the user.

        Returns:
            int: The count of collections owned by the user.
        """

        def call(c: H2OGPTEAsync):
            return c.count_collections()

        return self._run_async(call)

    def count_documents(self) -> int:
        """Counts number of documents accessed by the user.

        Returns:
            int: The count of documents accessed by the user.
        """

        def call(c: H2OGPTEAsync):
            return c.count_documents()

        return self._run_async(call)

    def count_documents_owned_by_me(self) -> int:
        """Counts number of documents owned by the user.

        Returns:
            int: The count of documents owned by the user.
        """

        def call(c: H2OGPTEAsync):
            return c.count_documents_owned_by_me()

        return self._run_async(call)

    def count_documents_in_collection(self, collection_id: str) -> int:
        """Counts the number of documents in a specific collection.

        Args:
            collection_id:
                String id of the collection to count documents for.

        Returns:
            int: The number of documents in that collection.
        """

        def call(c: H2OGPTEAsync):
            return c.count_documents_in_collection(collection_id)

        return self._run_async(call)

    def count_assets(self) -> ObjectCount:
        """Counts number of objects owned by the user.

        Returns:
            ObjectCount: The count of chat sessions, collections, and documents.
        """

        def call(c: H2OGPTEAsync):
            return c.count_assets()

        return self._run_async(call)

    def create_chat_session(self, collection_id: Union[str, None] = None) -> str:
        """Creates a new chat session for asking questions (of documents).

        Args:
            collection_id:
                String id of the collection to chat with.
                If None, chat with LLM directly.

        Returns:
            str: The ID of the newly created chat session.
        """

        def call(c: H2OGPTEAsync):
            return c.create_chat_session(collection_id)

        return self._run_async(call)

    def create_chat_session_on_default_collection(self) -> str:
        """Creates a new chat session for asking questions of documents on the default collection.

        Returns:
            str: The ID of the newly created chat session.
        """

        def call(c: H2OGPTEAsync):
            return c.create_chat_session_on_default_collection()

        return self._run_async(call)

    def list_embedding_models(self) -> List[str]:
        def call(c: H2OGPTEAsync):
            return c.list_embedding_models()

        return self._run_async(call)

    def run_selftest(self, llm: str, mode: str) -> dict:
        """
        Run a self-test for a given LLM
        Args:
            llm:
                Name of LLM
            mode:
                one of ["quick", "rag", "full", "agent"]
        Returns:
            Dictionary with performance stats. If "error" is filled, the test failed.
        """

        def call(c: H2OGPTEAsync):
            return c.run_selftest(llm, mode)

        return self._run_async(call)

    def get_guardrails_settings(
        self,
        action: str = "redact",
        sensitive: bool = True,
        non_sensitive: bool = True,
        all_guardrails: bool = True,
        guardrails_settings: Union[dict, None] = None,
    ) -> Dict[str, Union[str, List[str]]]:
        """
        Helper to get reasonable (easy to use) defaults for Guardrails/PII settings. To be further customized.
        :param action: what to do when detecting PII, either "redact" or "fail" ("allow" would keep PII intact). Guardrails models always fail upon detecting safety violations.
        :param sensitive: whether to include the most sensitive PII entities like SSN, bank account info
        :param non_sensitive: whether to include all non-sensitive PII entities, such as IP addresses, locations, names, e-mail addresses etc.
        :param all_guardrails: whether to include all possible entities for prompt guard and guardrails models, or just system defaults
        :param guardrails_settings: existing guardrails settings (e.g., from collection settings) to obtain guardrails entities and guardrails_entities_to_flag from instead of system defaults
        :return: dictionary to pass to collection creation or process_document method
        """

        def call(c: H2OGPTEAsync):
            return c.get_guardrails_settings(
                action, sensitive, non_sensitive, all_guardrails, guardrails_settings
            )

        return self._run_async(call)

    def get_agent_tools_dict(self) -> List[dict]:
        def call(c: H2OGPTEAsync):
            return c.get_agent_tools_dict()

        return self._run_async(call)

    def create_collection(
        self,
        name: str,
        description: str,
        embedding_model: Union[str, None] = None,
        prompt_template_id: Union[str, None] = None,
        collection_settings: Union[dict, None] = None,
        thumbnail: Union[Path, None] = None,
        chat_settings: Union[dict, None] = None,
    ) -> str:
        """Creates a new collection.

        Args:
            name:
                Name of the collection.
            description:
                Description of the collection
            embedding_model:
                embedding model to use. call list_embedding_models() to list of options.
            prompt_template_id:
                ID of the prompt template to get the prompts from. None to fall back to system defaults.
            collection_settings:
                (Optional) Dictionary with key/value pairs to configure certain collection specific settings
                max_tokens_per_chunk: Approximate max. number of tokens per chunk for text-dominated document pages. For images, chunks can be larger.
                chunk_overlap_tokens: Approximate number of tokens that are overlapping between successive chunks.
                gen_doc_summaries: Whether to auto-generate document summaries (uses LLM)
                gen_doc_questions: Whether to auto-generate sample questions for each document (uses LLM)
                audio_input_language: Language of audio files. Defaults to "auto" language detection. Pass empty string to see choices.
                ocr_model: Which method to use to extract text from images using AI-enabled optical character recognition (OCR) models.
                           Pass empty string to see choices.
                           docTR is best for Latin text, PaddleOCR is best for certain non-Latin languages, Tesseract covers a wide range of languages.
                           Mississippi works well on handwriting.
                           auto - Automatic will auto-select the best OCR model for every page.
                           off - Disable OCR for speed, but all images will then be skipped (also no image captions will be made).
                tesseract_lang: Which language to use when using ocr_model="tesseract". Pass empty string to see choices.
                keep_tables_as_one_chunk: When tables are identified by the table parser the table tokens will be kept in a single chunk.
                chunk_by_page: Each page will be a chunk. `keep_tables_as_one_chunk` will be ignored if this is `true`.
                handwriting_check: Check pages for handwriting. Will use specialized models if handwriting is found.
                follow_links: Whether to import all web pages linked from this URL will be imported. External links will be ignored. Links to other pages on the same domain will be followed as long as they are at the same level or below the URL you specify. Each page will be transformed into a PDF document.
                max_depth: Max depth of recursion when following links, only when follow_links is True. Max_depth of 0 means don't follow any links, max_depth of 1 means follow only top-level links, etc. Use -1 for automatic (system settings).
                max_documents: Max number of documents when following links, only when follow_links is True. Use None for automatic (system defaults). Use -1 for max (system limit).
                root_dir: Root directory for document storage
                copy_document: Whether to copy the document when importing an existing document.
                guardrails_settings itself is a dictionary of the following keys.
                    disallowed_regex_patterns: list of regular expressions that match custom PII
                    presidio_labels_to_flag: list of entities to be flagged as PII by the built-in Presidio model.
                    pii_labels_to_flag: list of entities to be flagged as PII by the built-in PII model.
                    pii_detection_parse_action: what to do when PII is detected during parsing of documents. One of ["allow", "redact", "fail"]. Redact will replace disallowed content in the ingested documents with redaction bars.
                    pii_detection_llm_input_action: what to do when PII is detected in the input to the LLM (document content and user prompts). One of ["allow", "redact", "fail"]. Redact will replace disallowed content with placeholders.
                    pii_detection_llm_output_action: what to do when PII is detected in the output of the LLM. One of ["allow", "redact", "fail"]. Redact will replace disallowed content with placeholders.
                    prompt_guard_labels_to_flag: list of entities to be flagged as safety violations in user prompts by the built-in prompt guard model.
                    guardrails_labels_to_flag: list of entities to be flagged as safety violations in user prompts. Must be a subset of guardrails_entities, if provided.
                    guardrails_safe_category: (Optional) name of the safe category for guardrails. Must be a key in guardrails_entities, if provided. Otherwise uses system defaults.
                    guardrails_entities: (Optional) dictionary of entities and their descriptions for the guardrails model to classify. The first entry is the "safe" class, the rest are "unsafe" classes.
                Example:
                    Note: Call client.get_guardrails_settings() to see all options for guardrails_settings.

                    collection_settings=dict(
                        max_tokens_per_chunk=320,
                        chunk_overlap_tokens=0,
                        guardrails_settings=dict(
                            disallowed_regex_patterns=["secret_disallowed_word", r"(?!0{3})(?!6{3})[0-8]\d{2}-(?!0{2})\d{2}-(?!0{4})\d{4}"],
                            presidio_labels_to_flag=["IBAN_CODE", "US_SSN"],
                            pii_labels_to_flag=["IBAN", "SSN"],
                            pii_detection_parse_action="redact",
                            pii_detection_llm_input_action="redact",
                            pii_detection_llm_output_action="allow",
                            prompt_guard_labels_to_flag=["JAILBREAK"],
                            guardrails_labels_to_flag=[
                                "Violent Crimes",
                                "Non-Violent Crimes",
                                "Intellectual Property",
                                "Code Interpreter Abuse",
                            ],
                            guardrails_safe_category="Safe",
                            guardrails_entities={
                                "Safe": "Messages that do not contain any of the following unsafe content",
                                "Violent Crimes": "Messages that enable, encourage, or endorse the commission of violent crimes, including: (1) unlawful violence toward people (ex: terrorism, genocide, murder, hate-motivated violent crimes, child abuse, assault, battery, kidnapping) and (2) unlawful violence toward animals (ex: animal abuse)",
                                "Non-Violent Crimes": "Messages that enable, encourage, or endorse the commission of non-violent crimes, including: (1) personal crimes (ex: labor trafficking, threats, intimidation, hate-motivated non-violent crimes), (2) financial crimes (ex: fraud, scams, money laundering), (3) property crimes (ex: theft, arson, vandalism), (4) drug crimes (ex: creating or using regulated substances), (5) weapons crimes (ex: producing unlicensed firearms), and (6) cyber crimes (ex: hacking)",
                                "Defamation": "Messages that are both verifiably false and likely to injure a living person’s reputation",
                                "Specialized Advice": "Messages that contain specialized financial, medical, or legal advice, or that indicate dangerous activities or objects are safe",
                                "Intellectual Property": "Messages that may violate the intellectual property rights of any third party",
                                "Code Interpreter Abuse": "Messages that seek to abuse code interpreters, including those that enable denial of service attacks, container escapes or privilege escalation exploits",
                            }
                        ),
                    )
            thumbnail:
                (Optional) Path to the thumbnail image for the collection. Must include appropriate file extension.
            chat_settings:
                (Optional) Dictionary with key/value pairs to configure the default values for certain chat specific settings
                The following keys are supported, see the client.session() documentation for more details.
                llm: str
                llm_args: dict
                self_reflection_config: dict
                rag_config: dict
                include_chat_history: bool
                tags: list[str]
        Returns:
            str: The ID of the newly created collection.
        """

        def call(c: H2OGPTEAsync):
            return c.create_collection(
                name,
                description,
                embedding_model,
                prompt_template_id,
                collection_settings,
                thumbnail,
                chat_settings,
            )

        return self._run_async(call)

    def set_collection_thumbnail(
        self, collection_id: str, file_path: Path, timeout: Union[float, None] = None
    ):
        """Upload an image file to be set as a collection's thumbnail.

        The image file will not be considered as a collection document.
        Acceptable image file types include: .png, .jpg, .jpeg, .svg

        Args:
            collection_id:
                Collection you want to add the thumbnail to.
            file_path:
                Path to the image file. Must include appropriate file extension.
            timeout:
                Amount of time in seconds to allow the request to run. The default is 86400 seconds.

        Raises:
            ValueError: The file is invalid.
            Exception: The upload request was unsuccessful.
        """

        def call(c: H2OGPTEAsync):
            return c.set_collection_thumbnail(collection_id, file_path, timeout)

        return self._run_async(call)

    def remove_collection_thumbnail(
        self, collection_id: str, timeout: Union[float, None] = None
    ):
        """Remove a thumbnail from a collection.

        Args:
            collection_id:
                Collection you want to remove the thumbnail from.
            timeout:
                Amount of time in seconds to allow the request to run. The default is 86400 seconds.
        """

        def call(c: H2OGPTEAsync):
            return c.remove_collection_thumbnail(collection_id, timeout)

        return self._run_async(call)

    def create_topic_model(
        self, collection_id: str, timeout: Union[float, None] = None
    ) -> Job:
        def call(c: H2OGPTEAsync):
            return c.create_topic_model(collection_id, timeout)

        return self._run_async(call)

    def delete_chat_sessions(
        self, chat_session_ids: Iterable[str], timeout: Union[float, None] = None
    ) -> Job:
        """Deletes chat sessions and related messages.

        Args:
            chat_session_ids:
                List of string ids of chat sessions to delete from the system.
            timeout:
                Timeout in seconds.

        Returns:
            Result: The delete job.
        """

        def call(c: H2OGPTEAsync):
            return c.delete_chat_sessions(chat_session_ids, timeout)

        return self._run_async(call)

    def delete_chat_messages(self, chat_message_ids: Iterable[str]) -> Result:
        """Deletes specific chat messages.

        Args:
            chat_message_ids:
                List of string ids of chat messages to delete from the system.

        Returns:
            Result: Status of the delete job.
        """

        def call(c: H2OGPTEAsync):
            return c.delete_chat_messages(chat_message_ids)

        return self._run_async(call)

    def delete_document_summaries(self, summaries_ids: Iterable[str]) -> Result:
        """Deletes document summaries.

        Args:
            summaries_ids:
                List of string ids of a document summary to delete from the system.

        Returns:
            Result: Status of the delete job.
        """

        def call(c: H2OGPTEAsync):
            return c.delete_document_summaries(summaries_ids)

        return self._run_async(call)

    def get_collection_questions(
        self, collection_id: str, limit: int
    ) -> List[SuggestedQuestion]:
        """List suggested questions

        Args:
            collection_id:
                A collection ID of which to return the suggested questions
            limit:
                How many questions to return.

        Returns:
            List: A list of questions.
        """

        def call(c: H2OGPTEAsync):
            return c.get_collection_questions(collection_id, limit)

        return self._run_async(call)

    def get_chat_session_questions(
        self, chat_session_id: str, limit: int
    ) -> List[SuggestedQuestion]:
        """List suggested questions

        Args:
            chat_session_id:
                A chat session ID of which to return the suggested questions
            limit:
                How many questions to return.

        Returns:
            List: A list of questions.
        """

        def call(c: H2OGPTEAsync):
            return c.get_chat_session_questions(chat_session_id, limit)

        return self._run_async(call)

    def set_collection_expiry_date(
        self,
        collection_id: str,
        expiry_date: str,
        timezone: Union[str, None] = None,
    ) -> str:
        """Set an expiry date for a collection.

        Args:
            collection_id:
                ID of the collection to update.
            expiry_date:
                The expiry date as a string in 'YYYY-MM-DD' format.
            timezone:
                Optional timezone to associate with expiry date (with IANA timezone support).
        """

        def call(c: H2OGPTEAsync):
            return c.set_collection_expiry_date(collection_id, expiry_date, timezone)

        return self._run_async(call)

    def remove_collection_expiry_date(self, collection_id: str) -> str:
        """Remove an expiry date from a collection.

        Args:
            collection_id:
                ID of the collection to update.
        """

        def call(c: H2OGPTEAsync):
            return c.remove_collection_expiry_date(collection_id)

        return self._run_async(call)

    def set_collection_inactivity_interval(
        self, collection_id: str, inactivity_interval: int
    ) -> str:
        """Set an inactivity interval for a collection.

        Args:
            collection_id:
                ID of the collection to update.
            inactivity_interval:
                The inactivity interval as an integer number of days.
        """

        def call(c: H2OGPTEAsync):
            return c.set_collection_inactivity_interval(
                collection_id, inactivity_interval
            )

        return self._run_async(call)

    def remove_collection_inactivity_interval(self, collection_id: str) -> str:
        """Remove an inactivity interval for a collection.

        Args:
            collection_id:
                ID of the collection to update.
        """

        def call(c: H2OGPTEAsync):
            return c.remove_collection_inactivity_interval(collection_id)

        return self._run_async(call)

    def set_collection_size_limit(
        self, collection_id: str, limit: Union[int, str]
    ) -> str:
        """Set a maximum limit on the total size of documents (sum) added to a collection.
        The limit is measured in bytes.

        Args:
            collection_id:
                ID of the collection to update.
            limit:
                The bytes limit, possible values follow the format: 12345, "1GB", or "1GiB".
        """

        def call(c: H2OGPTEAsync):
            return c.set_collection_size_limit(collection_id, limit)

        return self._run_async(call)

    def remove_collection_size_limit(self, collection_id: str) -> str:
        """Remove a size limit for a collection.

        Args:
            collection_id:
                ID of the collection to update.
        """

        def call(c: H2OGPTEAsync):
            return c.remove_collection_size_limit(collection_id)

        return self._run_async(call)

    def unarchive_collection(self, collection_id: str) -> str:
        """Restore an archived collection to an active status.

        Args:
            collection_id:
                ID of the collection to restore.
        """

        def call(c: H2OGPTEAsync):
            return c.unarchive_collection(collection_id)

        return self._run_async(call)

    def delete_collections(
        self, collection_ids: Iterable[str], timeout: Union[float, None] = None
    ) -> Job:
        """Deletes collections from the environment.

        Documents in the collection will not be deleted.

        Args:
            collection_ids:
                List of string ids of collections to delete from the system.
            timeout:
                Timeout in seconds.
        """

        def call(c: H2OGPTEAsync):
            return c.delete_collections(collection_ids, timeout)

        return self._run_async(call)

    def delete_documents(
        self, document_ids: Iterable[str], timeout: Union[float, None] = None
    ) -> Job:
        """Deletes documents from the system.

        Args:
            document_ids:
                List of string ids to delete from the system and all collections.
            timeout:
                Timeout in seconds.
        """

        def call(c: H2OGPTEAsync):
            return c.delete_documents(document_ids, timeout)

        return self._run_async(call)

    def delete_documents_from_collection(
        self,
        collection_id: str,
        document_ids: Iterable[str],
        timeout: Union[float, None] = None,
    ) -> Job:
        """Removes documents from a collection.

        See Also: H2OGPTE.delete_documents for completely removing the document from the environment.

        Args:
            collection_id:
                String of the collection to remove documents from.
            document_ids:
                List of string ids to remove from the collection.
            timeout:
                Timeout in seconds.
        """

        def call(c: H2OGPTEAsync):
            return c.delete_documents_from_collection(
                collection_id, document_ids, timeout
            )

        return self._run_async(call)

    def import_collection_into_collection(
        self,
        collection_id: str,
        src_collection_id: str,
        gen_doc_summaries: Union[bool, None] = None,
        gen_doc_questions: Union[bool, None] = None,
        copy_document: Union[bool, None] = None,
        ocr_model: Union[str, None] = None,
        tesseract_lang: Union[str, None] = None,
        keep_tables_as_one_chunk: Union[bool, None] = None,
        chunk_by_page: Union[bool, None] = None,
        handwriting_check: Union[bool, None] = None,
        timeout: Union[float, None] = None,
        ingest_mode: Union[str, None] = None,
    ):
        """Import all documents from a collection into an existing collection

        Args:
            collection_id:
                Collection ID to add documents to.
            src_collection_id:
                Collection ID to import documents from.
            gen_doc_summaries:
                Whether to auto-generate document summaries (uses LLM)
            gen_doc_questions:
                Whether to auto-generate sample questions for each document (uses LLM)
            copy_document:
                Whether to save a new copy of the document
            ocr_model:
                Which method to use to extract text from images using AI-enabled optical character recognition (OCR) models.
                Pass empty string to see choices.
                docTR is best for Latin text, PaddleOCR is best for certain non-Latin languages, Tesseract covers a wide range of languages.
                Mississippi works well on handwriting.
                "auto" - Automatic will auto-select the best OCR model for every page.
                "off" - Disable OCR for speed, but all images will then be skipped (also no image captions will be made).
            tesseract_lang:
                Which language to use when using ocr_model="tesseract". Pass empty string to see choices.
            keep_tables_as_one_chunk:
                When tables are identified by the table parser the table tokens will be kept in a single chunk.
            chunk_by_page:
                Each page will be a chunk. `keep_tables_as_one_chunk` will be ignored if this is True.
            handwriting_check:
                Check pages for handwriting. Will use specialized models if handwriting is found.
            timeout:
                Timeout in seconds.
            ingest_mode:
                Ingest mode to use.
                "standard" - Files will be ingested for use with RAG
                "agent_only" - Bypasses standard ingestion. Files can only be used with agents.
        """

        def call(c: H2OGPTEAsync):
            return c.import_collection_into_collection(
                collection_id,
                src_collection_id,
                gen_doc_summaries,
                gen_doc_questions,
                copy_document,
                ocr_model,
                tesseract_lang,
                keep_tables_as_one_chunk,
                chunk_by_page,
                handwriting_check,
                timeout,
                ingest_mode,
            )

        return self._run_async(call)

    def import_document_into_collection(
        self,
        collection_id: str,
        document_id: str,
        gen_doc_summaries: Union[bool, None] = None,
        gen_doc_questions: Union[bool, None] = None,
        copy_document: Union[bool, None] = None,
        ocr_model: Union[str, None] = None,
        tesseract_lang: Union[str, None] = None,
        keep_tables_as_one_chunk: Union[bool, None] = None,
        chunk_by_page: Union[bool, None] = None,
        handwriting_check: Union[bool, None] = None,
        timeout: Union[float, None] = None,
        ingest_mode: Union[str, None] = None,
    ):
        """Import an already stored document to an existing collection

        Args:
            collection_id:
                Collection ID to add documents to.
            document_id:
                Document ID to add.
            gen_doc_summaries:
                Whether to auto-generate document summaries (uses LLM)
            gen_doc_questions:
                Whether to auto-generate sample questions for each document (uses LLM)
            copy_document:
                Whether to save a new copy of the document
            ocr_model:
                Which method to use to extract text from images using AI-enabled optical character recognition (OCR) models.
                Pass empty string to see choices.
                docTR is best for Latin text, PaddleOCR is best for certain non-Latin languages, Tesseract covers a wide range of languages.
                Mississippi works well on handwriting.
                "auto" - Automatic will auto-select the best OCR model for every page.
                "off" - Disable OCR for speed, but all images will then be skipped (also no image captions will be made).
            tesseract_lang:
                Which language to use when using ocr_model="tesseract". Pass empty string to see choices.
            keep_tables_as_one_chunk:
                When tables are identified by the table parser the table tokens will be kept in a single chunk.
            chunk_by_page:
                Each page will be a chunk. `keep_tables_as_one_chunk` will be ignored if this is True.
            handwriting_check:
                Check pages for handwriting. Will use specialized models if handwriting is found.
            timeout:
                Timeout in seconds.
            ingest_mode:
                Ingest mode to use.
                "standard" - Files will be ingested for use with RAG
                "agent_only" - Bypasses standard ingestion. Files can only be used with agents.
        """

        def call(c: H2OGPTEAsync):
            return c.import_document_into_collection(
                collection_id,
                document_id,
                gen_doc_summaries,
                gen_doc_questions,
                copy_document,
                ocr_model,
                tesseract_lang,
                keep_tables_as_one_chunk,
                chunk_by_page,
                handwriting_check,
                timeout,
                ingest_mode,
            )

        return self._run_async(call)

    def summarize_document(self, *args, **kwargs) -> DocumentSummary:
        def call(c: H2OGPTEAsync):
            return c.summarize_document(*args, **kwargs)

        return self._run_async(call)

    def process_document(
        self,
        document_id: str,
        system_prompt: Union[str, None] = None,
        pre_prompt_summary: Union[str, None] = None,
        prompt_summary: Union[str, None] = None,
        image_batch_image_prompt: Union[str, None] = None,
        image_batch_final_prompt: Union[str, None] = None,
        llm: Union[str, int, None] = None,
        llm_args: Union[Dict[str, Any], None] = None,
        max_num_chunks: Union[int, None] = None,
        sampling_strategy: Union[str, None] = None,
        pages: Union[List[int], None] = None,
        schema: Union[Dict[str, Any], None] = None,
        keep_intermediate_results: Union[bool, None] = None,
        guardrails_settings: Union[Dict, None] = None,
        meta_data_to_include: Union[Dict[str, bool], None] = None,
        timeout: Union[float, None] = None,
    ) -> ProcessedDocument:
        """Processes a document to either create a global or piecewise summary/extraction/transformation of a document.

        Effective prompt created (excluding the system prompt):

        .. code-block::

            "{pre_prompt_summary}
            \"\"\"
            {text from document}
            \"\"\"
            {prompt_summary}"

        Args:
            document_id:
                String id of the document to create a summary from.
            system_prompt:
                System Prompt
            pre_prompt_summary:
                Prompt that goes before each large piece of text to summarize
            prompt_summary:
                Prompt that goes after each large piece of text to summarize
            image_batch_final_prompt:
                Prompt for each image batch for vision models
            image_batch_image_prompt:
                Prompt to reduce all answers each image batch for vision models
            llm:
                LLM to use
            llm_args:
                Dictionary of kwargs to pass to the llm. Valid keys:
                    temperature (float, default: 0) — The value used to modulate the next token probabilities. Most deterministic: 0, Most creative: 1
                    top_k (int, default: 1) — The number of highest probability vocabulary tokens to keep for top-k-filtering.
                    top_p (float, default: 1.0) — If set to float < 1, only the smallest set of most probable tokens with probabilities that add up to top_p or higher are kept for generation.
                    seed (int, default: 0) — The seed for the random number generator when sampling during generation (if temp>0 or top_k>1 or top_p<1), seed=0 picks a random seed.
                    repetition_penalty (float, default: 1.07) — The parameter for repetition penalty. 1.0 means no penalty.
                    max_new_tokens (int, default: 1024) — Maximum number of new tokens to generate. This limit applies to each (map+reduce) step during summarization and each (map) step during extraction.
                    min_max_new_tokens (int, default: 512) — minimum value for max_new_tokens when auto-adjusting for content of prompt, docs, etc.
                    response_format (str, default: "text") — Output type, one of ["text", "json_object", "json_code"].
                    guided_json (dict, default: None) — If specified, the output will follow the JSON schema.
                    guided_regex (str, default: "") — If specified, the output will follow the regex pattern. Only for models that support guided generation: check output of get_llms() for guided_vllm flag.
                    guided_choice (Optional[List[str]], default: None — If specified, the output will be exactly one of the choices. Only for models that support guided generation: check output of get_llms() for guided_vllm flag.
                    guided_grammar (str, default: "") — If specified, the output will follow the context free grammar. Only for models that support guided generation: check output of get_llms() for guided_vllm flag.
                    guided_whitespace_pattern (str, default: "") — If specified, will override the default whitespace pattern for guided json decoding. Only for models that support guided generation: check output of get_llms() for guided_vllm flag.
                    enable_vision (str, default: "auto") - Controls vision mode, send images to the LLM in addition to text chunks. Only if have models that support vision, use get_vision_capable_llm_names() to see list. One of ["on", "off", "auto"].
                    visible_vision_models (List[str], default: ["auto"]) - Controls which vision model to use when processing images. Use get_vision_capable_llm_names() to see list. Must provide exactly one model. ["auto"] for automatic.
            max_num_chunks:
                Max limit of chunks to send to the summarizer
            sampling_strategy:
                How to sample if the document has more chunks than max_num_chunks.
                Options are "auto", "uniform", "first", "first+last", default is "auto" (a hybrid of them all).
            pages:
                List of specific pages (of the ingested document in PDF form) to use from the document. 1-based indexing.
            schema:
                Optional JSON schema to use for guided json generation.
            keep_intermediate_results:
                Whether to keep intermediate results. Default: disabled.
                If disabled, further LLM calls are applied to the intermediate results until one global summary is obtained: map+reduce (i.e., summary).
                If enabled, the results' content will be a list of strings (the results of applying the LLM to different pieces of document context): map (i.e., extract).
            guardrails_settings:
                Guardrails Settings.
            meta_data_to_include:
                A dictionary containing flags that indicate whether each piece of document metadata is to be included as part of the context given to the LLM. Only used if enable_vision is disabled.
                Default is {
                    "name": True,
                    "text": True,
                    "page": True,
                    "captions": True,
                    "uri": False,
                    "connector": False,
                    "original_mtime": False,
                    "age": False,
                    "score": False,
                }
            timeout:
                Amount of time in seconds to allow the request to run. The default is 86400 seconds.

        Returns:
            ProcessedDocument: Processed document. The content is either a string (keep_intermediate_results=False) or a list of strings (keep_intermediate_results=True).

        Raises:
            TimeoutError: The request did not complete in time.
            SessionError: No summary or extraction created. Document wasn't part of a collection, or LLM timed out, etc.
        """

        def call(c: H2OGPTEAsync):
            return c.process_document(
                document_id,
                system_prompt,
                pre_prompt_summary,
                prompt_summary,
                image_batch_image_prompt,
                image_batch_final_prompt,
                llm,
                llm_args,
                max_num_chunks,
                sampling_strategy,
                pages,
                schema,
                keep_intermediate_results,
                guardrails_settings,
                meta_data_to_include,
                timeout,
            )

        return self._run_async(call)

    def list_recent_document_summaries(
        self, document_id: str, offset: int, limit: int
    ) -> List[ProcessedDocument]:
        """Fetches recent document summaries/extractions/transformations

        Args:
            document_id:
                document ID for which to return summaries
            offset:
                How many summaries to skip before returning summaries.
            limit:
                How many summaries to return.
        """

        def call(c: H2OGPTEAsync):
            return c.list_recent_document_summaries(document_id, offset, limit)

        return self._run_async(call)

    def encode_for_retrieval(
        self,
        chunks: Iterable[str],
        embedding_model: Union[str, None] = None,
    ) -> List[List[float]]:
        """Encode texts for semantic searching.

        See Also: H2OGPTE.match for getting a list of chunks that semantically match
        each encoded text.

        Args:
            chunks:
                List of strings of texts to be encoded.
            embedding_model:
                embedding model to use. call list_embedding_models() to list of options.

        Returns:
            List of list of floats: Each list in the list is the encoded original text.
        """

        def call(c: H2OGPTEAsync):
            return c.encode_for_retrieval(chunks, embedding_model)

        return self._run_async(call)

    def get_chunks(self, collection_id: str, chunk_ids: Iterable[int]) -> List[Chunk]:
        """Get the text of specific chunks in a collection.

        Args:
            collection_id:
                String id of the collection to search in.
            chunk_ids:
                List of ints for the chunks to return. Chunks are indexed starting at 1.

        Returns:
            Chunk: The text of the chunk.

        Raises:
            Exception: One or more chunks could not be found.
        """

        def call(c: H2OGPTEAsync):
            return c.get_chunks(collection_id, chunk_ids)

        return self._run_async(call)

    def get_collection(self, collection_id: str) -> Collection:
        """Get metadata about a collection.

        Args:
            collection_id:
                String id of the collection to search for.

        Returns:
            Collection: Metadata about the collection.

        Raises:
            KeyError: The collection was not found.
        """

        def call(c: H2OGPTEAsync):
            return c.get_collection(collection_id)

        return self._run_async(call)

    def get_collection_for_chat_session(self, chat_session_id: str) -> Collection:
        """Get metadata about the collection of a chat session.

        Args:
            chat_session_id:
                String id of the chat session to search for.

        Returns:
            Collection: Metadata about the collection.
        """

        def call(c: H2OGPTEAsync):
            return c.get_collection_for_chat_session(chat_session_id)

        return self._run_async(call)

    def get_document(self, document_id: str, include_layout: bool = False) -> Document:
        """Fetches information about a specific document.

        Args:
            document_id:
                String id of the document.
            include_layout:
                Include the layout prediction results.

        Returns:
            Document: Metadata about the Document.

        Raises:
            KeyError: The document was not found.
        """

        def call(c: H2OGPTEAsync):
            return c.get_document(document_id, include_layout)

        return self._run_async(call)

    def get_job(self, job_id: str) -> Job:
        """Fetches information about a specific job.

        Args:
            job_id:
                String id of the job.

        Returns:
            Job: Metadata about the Job.
        """

        def call(c: H2OGPTEAsync):
            return c.get_job(job_id)

        return self._run_async(call)

    def get_meta(self) -> Meta:
        """Returns information about the environment and the user.

        Returns:
            Meta: Details about the version and license of the environment and
            the user's name and email.
        """

        def call(c: H2OGPTEAsync):
            return c.get_meta()

        return self._run_async(call)

    def get_llm_usage_24h(self) -> float:
        def call(c: H2OGPTEAsync):
            return c.get_llm_usage_24h()

        return self._run_async(call)

    def get_llm_usage_24h_by_llm(self) -> List[LLMUsage]:
        def call(c: H2OGPTEAsync):
            return c.get_llm_usage_24h_by_llm()

        return self._run_async(call)

    def get_llm_usage_24h_with_limits(self) -> LLMUsageLimit:
        def call(c: H2OGPTEAsync):
            return c.get_llm_usage_24h_with_limits()

        return self._run_async(call)

    def get_llm_usage_6h(self) -> float:
        def call(c: H2OGPTEAsync):
            return c.get_llm_usage_6h()

        return self._run_async(call)

    def get_llm_usage_6h_by_llm(self) -> List[LLMUsage]:
        def call(c: H2OGPTEAsync):
            return c.get_llm_usage_6h_by_llm()

        return self._run_async(call)

    def get_llm_usage_with_limits(self, interval: str) -> LLMUsageLimit:
        def call(c: H2OGPTEAsync):
            return c.get_llm_usage_with_limits(interval)

        return self._run_async(call)

    def get_llm_usage_by_llm(self, interval: str) -> List[LLMUsage]:
        def call(c: H2OGPTEAsync):
            return c.get_llm_usage_by_llm(interval)

        return self._run_async(call)

    def get_llm_usage_by_user(self, interval: str) -> List[UserWithLLMUsage]:
        def call(c: H2OGPTEAsync):
            return c.get_llm_usage_by_user(interval)

        return self._run_async(call)

    def get_llm_usage_by_llm_and_user(self, interval: str) -> List[LLMWithUserUsage]:
        def call(c: H2OGPTEAsync):
            return c.get_llm_usage_by_llm_and_user(interval)

        return self._run_async(call)

    def get_llm_performance_by_llm(self, interval: str) -> List[LLMPerformance]:
        def call(c: H2OGPTEAsync):
            return c.get_llm_performance_by_llm(interval)

        return self._run_async(call)

    def get_scheduler_stats(self) -> SchedulerStats:
        """Count the number of global, pending jobs on the server.

        Returns:
            SchedulerStats: The queue length for number of jobs.
        """

        def call(c: H2OGPTEAsync):
            return c.get_scheduler_stats()

        return self._run_async(call)

    def ingest_from_file_system(
        self,
        collection_id: str,
        root_dir: str,
        glob: str,
        gen_doc_summaries: Union[bool, None] = None,
        gen_doc_questions: Union[bool, None] = None,
        audio_input_language: Union[str, None] = None,
        ocr_model: Union[str, None] = None,
        tesseract_lang: Union[str, None] = None,
        keep_tables_as_one_chunk: Union[bool, None] = None,
        chunk_by_page: Union[bool, None] = None,
        handwriting_check: Union[bool, None] = None,
        timeout: Union[float, None] = None,
        ingest_mode: Union[str, None] = None,
    ) -> Job:
        """Add files from the local system into a collection.

        Args:
            collection_id:
                String id of the collection to add the ingested documents into.
            root_dir:
                String path of where to look for files.
            glob:
                String of the glob pattern used to match files in the root directory.
            gen_doc_summaries:
                Whether to auto-generate document summaries (uses LLM)
            gen_doc_questions:
                Whether to auto-generate sample questions for each document (uses LLM)
            audio_input_language:
                Language of audio files. Defaults to "auto" language detection. Pass empty string to see choices.
            ocr_model:
                Which method to use to extract text from images using AI-enabled optical character recognition (OCR) models.
                Pass empty string to see choices.
                docTR is best for Latin text, PaddleOCR is best for certain non-Latin languages, Tesseract covers a wide range of languages.
                Mississippi works well on handwriting.
                "auto" - Automatic will auto-select the best OCR model for every page.
                "off" - Disable OCR for speed, but all images will then be skipped (also no image captions will be made).
            tesseract_lang:
                Which language to use when using ocr_model="tesseract". Pass empty string to see choices.
            keep_tables_as_one_chunk:
                When tables are identified by the table parser the table tokens will be kept in a single chunk.
            chunk_by_page:
                Each page will be a chunk. `keep_tables_as_one_chunk` will be ignored if this is True.
            handwriting_check:
                Check pages for handwriting. Will use specialized models if handwriting is found.
            timeout:
                Timeout in seconds.
            ingest_mode:
                Ingest mode to use.
                "standard" - Files will be ingested for use with RAG
                "agent_only" - Bypasses standard ingestion. Files can only be used with agents.
        """

        def call(c: H2OGPTEAsync):
            return c.ingest_from_file_system(
                collection_id,
                root_dir,
                glob,
                gen_doc_summaries,
                gen_doc_questions,
                audio_input_language,
                ocr_model,
                tesseract_lang,
                keep_tables_as_one_chunk,
                chunk_by_page,
                handwriting_check,
                timeout,
                ingest_mode,
            )

        return self._run_async(call)

    def ingest_from_plain_text(
        self,
        collection_id: str,
        plain_text: str,
        file_name: str,
        gen_doc_summaries: Union[bool, None] = None,
        gen_doc_questions: Union[bool, None] = None,
        metadata: Union[Dict[str, Any], None] = None,
        timeout: Union[float, None] = None,
    ):
        """Add plain text to a collection.

        Args:
            collection_id:
                String id of the collection to add the ingested documents into.
            plain_text:
                String of the plain text to ingest.
            file_name:
                String of the file name to use for the document.
            gen_doc_summaries:
                Whether to auto-generate document summaries (uses LLM)
            gen_doc_questions:
                Whether to auto-generate sample questions for each document (uses LLM)
            metadata:
                Dictionary of metadata to add to the document.
            timeout:
                Timeout in seconds
        """

        def call(c: H2OGPTEAsync):
            return c.ingest_from_plain_text(
                collection_id,
                plain_text,
                file_name,
                gen_doc_summaries,
                gen_doc_questions,
                metadata,
                timeout,
            )

        return self._run_async(call)

    def ingest_from_s3(
        self,
        collection_id: str,
        url: Union[str, List[str]],
        region: str = "us-east-1",
        credentials: Union[S3Credential, None] = None,
        gen_doc_summaries: Union[bool, None] = None,
        gen_doc_questions: Union[bool, None] = None,
        audio_input_language: Union[str, None] = None,
        ocr_model: Union[str, None] = None,
        tesseract_lang: Union[str, None] = None,
        keep_tables_as_one_chunk: Union[bool, None] = None,
        chunk_by_page: Union[bool, None] = None,
        handwriting_check: Union[bool, None] = None,
        metadata: Union[Dict[str, Any], None] = None,
        timeout: Union[float, None] = None,
        ingest_mode: Union[str, None] = None,
    ):
        """Add files from the AWS S3 storage into a collection.

        Args:
            collection_id:
                String id of the collection to add the ingested documents into.
            url:
                The path or list of paths of S3 files or directories. Examples: s3://bucket/file, s3://bucket/../dir/
            region:
                The name of the region used for interaction with AWS services.
            credentials:
                The object with S3 credentials. If the object is not provided, only public buckets will be accessible.
            gen_doc_summaries:
                Whether to auto-generate document summaries (uses LLM)
            gen_doc_questions:
                Whether to auto-generate sample questions for each document (uses LLM)
            audio_input_language:
                Language of audio files. Defaults to "auto" language detection. Pass empty string to see choices.
            ocr_model:
                Which method to use to extract text from images using AI-enabled optical character recognition (OCR) models.
                Pass empty string to see choices.
                docTR is best for Latin text, PaddleOCR is best for certain non-Latin languages, Tesseract covers a wide range of languages.
                Mississippi works well on handwriting.
                "auto" - Automatic will auto-select the best OCR model for every page.
                "off" - Disable OCR for speed, but all images will then be skipped (also no image captions will be made).
            tesseract_lang:
                Which language to use when using ocr_model="tesseract". Pass empty string to see choices.
            keep_tables_as_one_chunk:
                When tables are identified by the table parser the table tokens will be kept in a single chunk.
            chunk_by_page:
                Each page will be a chunk. `keep_tables_as_one_chunk` will be ignored if this is True.
            handwriting_check:
                Check pages for handwriting. Will use specialized models if handwriting is found.
            metadata:
                Dictionary of metadata to add to the document.
            timeout:
                Timeout in seconds.
            ingest_mode:
                Ingest mode to use.
                "standard" - Files will be ingested for use with RAG
                "agent_only" - Bypasses standard ingestion. Files can only be used with agents.
        """

        def call(c: H2OGPTEAsync):
            return c.ingest_from_s3(
                collection_id,
                url,
                region,
                credentials,
                gen_doc_summaries,
                gen_doc_questions,
                audio_input_language,
                ocr_model,
                tesseract_lang,
                keep_tables_as_one_chunk,
                chunk_by_page,
                handwriting_check,
                metadata,
                timeout,
                ingest_mode,
            )

        return self._run_async(call)

    def ingest_from_gcs(
        self,
        collection_id: str,
        url: Union[str, List[str]],
        credentials: Union[GCSServiceAccountCredential, None] = None,
        gen_doc_summaries: Union[bool, None] = None,
        gen_doc_questions: Union[bool, None] = None,
        audio_input_language: Union[str, None] = None,
        ocr_model: Union[str, None] = None,
        tesseract_lang: Union[str, None] = None,
        keep_tables_as_one_chunk: Union[bool, None] = None,
        chunk_by_page: Union[bool, None] = None,
        handwriting_check: Union[bool, None] = None,
        metadata: Union[Dict[str, Any], None] = None,
        timeout: Union[float, None] = None,
        ingest_mode: Union[str, None] = None,
    ):
        """Add files from the Google Cloud Storage into a collection.

        Args:
            collection_id:
                String id of the collection to add the ingested documents into.
            url:
                The path or list of paths of GCS files or directories. Examples: gs://bucket/file, gs://bucket/../dir/
            credentials:
                The object holding a path to a JSON key of Google Cloud service account. If the object is not provided,
                only public buckets will be accessible.
            gen_doc_summaries:
                Whether to auto-generate document summaries (uses LLM)
            gen_doc_questions:
                Whether to auto-generate sample questions for each document (uses LLM)
            audio_input_language:
                Language of audio files. Defaults to "auto" language detection. Pass empty string to see choices.
            ocr_model:
                Which method to use to extract text from images using AI-enabled optical character recognition (OCR) models.
                Pass empty string to see choices.
                docTR is best for Latin text, PaddleOCR is best for certain non-Latin languages, Tesseract covers a wide range of languages.
                Mississippi works well on handwriting.
                "auto" - Automatic will auto-select the best OCR model for every page.
                "off" - Disable OCR for speed, but all images will then be skipped (also no image captions will be made).
            tesseract_lang:
                Which language to use when using ocr_model="tesseract". Pass empty string to see choices.
            keep_tables_as_one_chunk:
                When tables are identified by the table parser the table tokens will be kept in a single chunk.
            chunk_by_page:
                Each page will be a chunk. `keep_tables_as_one_chunk` will be ignored if this is True.
            handwriting_check:
                Check pages for handwriting. Will use specialized models if handwriting is found.
            metadata:
                Dictionary of metadata to add to the document.
            timeout:
                Timeout in seconds.
            ingest_mode:
                Ingest mode to use.
                "standard" - Files will be ingested for use with RAG
                "agent_only" - Bypasses standard ingestion. Files can only be used with agents.
        """

        def call(c: H2OGPTEAsync):
            return c.ingest_from_gcs(
                collection_id,
                url,
                credentials,
                gen_doc_summaries,
                gen_doc_questions,
                audio_input_language,
                ocr_model,
                tesseract_lang,
                keep_tables_as_one_chunk,
                chunk_by_page,
                handwriting_check,
                metadata,
                timeout,
                ingest_mode,
            )

        return self._run_async(call)

    def ingest_from_azure_blob_storage(
        self,
        collection_id: str,
        container: str,
        path: Union[str, List[str]],
        account_name: str,
        credentials: Union[AzureKeyCredential, AzureSASCredential, None] = None,
        gen_doc_summaries: Union[bool, None] = None,
        gen_doc_questions: Union[bool, None] = None,
        audio_input_language: Union[str, None] = None,
        ocr_model: Union[str, None] = None,
        tesseract_lang: Union[str, None] = None,
        keep_tables_as_one_chunk: Union[bool, None] = None,
        chunk_by_page: Union[bool, None] = None,
        handwriting_check: Union[bool, None] = None,
        metadata: Union[Dict[str, Any], None] = None,
        timeout: Union[float, None] = None,
        ingest_mode: Union[str, None] = None,
    ):
        """Add files from the Azure Blob Storage into a collection.

        Args:
            collection_id:
                String id of the collection to add the ingested documents into.
            container:
                Name of the Azure Blob Storage container.
            path:
                Path or list of paths to files or directories within an Azure Blob Storage container.
                Examples: file1, dir1/file2, dir3/dir4/
            account_name:
                Name of a storage account
            credentials:
                The object with Azure credentials. If the object is not provided,
                only a public container will be accessible.
            gen_doc_summaries:
                Whether to auto-generate document summaries (uses LLM)
            gen_doc_questions:
                Whether to auto-generate sample questions for each document (uses LLM)
            audio_input_language:
                Language of audio files. Defaults to "auto" language detection. Pass empty string to see choices.
            ocr_model:
                Which method to use to extract text from images using AI-enabled optical character recognition (OCR) models.
                Pass empty string to see choices.
                docTR is best for Latin text, PaddleOCR is best for certain non-Latin languages, Tesseract covers a wide range of languages.
                Mississippi works well on handwriting.
                "auto" - Automatic will auto-select the best OCR model for every page.
                "off" - Disable OCR for speed, but all images will then be skipped (also no image captions will be made).
            tesseract_lang:
                Which language to use when using ocr_model="tesseract". Pass empty string to see choices.
            keep_tables_as_one_chunk:
                When tables are identified by the table parser the table tokens will be kept in a single chunk.
            chunk_by_page:
                Each page will be a chunk. `keep_tables_as_one_chunk` will be ignored if this is True.
            handwriting_check:
                Check pages for handwriting. Will use specialized models if handwriting is found.
            metadata:
                Metadata to be associated with the document.
            timeout:
                Timeout in seconds.
            ingest_mode:
                Ingest mode to use.
                "standard" - Files will be ingested for use with RAG
                "agent_only" - Bypasses standard ingestion. Files can only be used with agents.
        """

        def call(c: H2OGPTEAsync):
            return c.ingest_from_azure_blob_storage(
                collection_id,
                container,
                path,
                account_name,
                credentials,
                gen_doc_summaries,
                gen_doc_questions,
                audio_input_language,
                ocr_model,
                tesseract_lang,
                keep_tables_as_one_chunk,
                chunk_by_page,
                handwriting_check,
                metadata,
                timeout,
                ingest_mode,
            )

        return self._run_async(call)

    def ingest_uploads(
        self,
        collection_id: str,
        upload_ids: Iterable[str],
        gen_doc_summaries: Union[bool, None] = None,
        gen_doc_questions: Union[bool, None] = None,
        audio_input_language: Union[str, None] = None,
        ocr_model: Union[str, None] = None,
        restricted: bool = False,
        permissions: Union[List[SharePermission], None] = None,
        tesseract_lang: Union[str, None] = None,
        keep_tables_as_one_chunk: Union[bool, None] = None,
        chunk_by_page: Union[bool, None] = None,
        handwriting_check: Union[bool, None] = None,
        metadata: Union[Dict[str, Any], None] = None,
        timeout: Union[float, None] = None,
        ingest_mode: Union[str, None] = None,
    ) -> Job:
        """Add uploaded documents into a specific collection.

        See Also:
            upload: Upload the files into the system to then be ingested into a collection.
            delete_upload: Delete uploaded file

        Args:
            collection_id:
                String id of the collection to add the ingested documents into.
            upload_ids:
                List of string ids of each uploaded document to add to the collection.
            gen_doc_summaries:
                Whether to auto-generate document summaries (uses LLM)
            gen_doc_questions:
                Whether to auto-generate sample questions for each document (uses LLM)
            audio_input_language:
                Language of audio files. Defaults to "auto" language detection. Pass empty string to see choices.
            ocr_model:
                Which method to use to extract text from images using AI-enabled optical character recognition (OCR) models.
                Pass empty string to see choices.
                docTR is best for Latin text, PaddleOCR is best for certain non-Latin languages, Tesseract covers a wide range of languages.
                Mississippi works well on handwriting.
                "auto" - Automatic will auto-select the best OCR model for every page.
                "off" - Disable OCR for speed, but all images will then be skipped (also no image captions will be made).
            restricted:
                Whether the document should be restricted only to certain users.
            permissions:
                List of permissions. Each permission is a SharePermission object.
            tesseract_lang:
                Which language to use when using ocr_model="tesseract". Pass empty string to see choices.
            keep_tables_as_one_chunk:
                When tables are identified by the table parser the table tokens will be kept in a single chunk.
            chunk_by_page:
                Each page will be a chunk. `keep_tables_as_one_chunk` will be ignored if this is True.
            handwriting_check:
                Check pages for handwriting. Will use specialized models if handwriting is found.
            metadata:
                Metadata to be associated with the document.
            timeout:
                Timeout in seconds.
            ingest_mode:
                Ingest mode to use.
                "standard" - Files will be ingested for use with RAG
                "agent_only" - Bypasses standard ingestion. Files can only be used with agents.
        """

        def call(c: H2OGPTEAsync):
            return c.ingest_uploads(
                collection_id,
                upload_ids,
                gen_doc_summaries,
                gen_doc_questions,
                audio_input_language,
                ocr_model,
                restricted,
                permissions,
                tesseract_lang,
                keep_tables_as_one_chunk,
                chunk_by_page,
                handwriting_check,
                metadata,
                timeout,
                ingest_mode,
            )

        return self._run_async(call)

    def ingest_website(
        self,
        collection_id: str,
        url: str,
        gen_doc_summaries: Union[bool, None] = None,
        gen_doc_questions: Union[bool, None] = None,
        follow_links: Union[bool, None] = None,
        max_depth: Union[int, None] = None,
        max_documents: Union[int, None] = None,
        audio_input_language: Union[str, None] = None,
        ocr_model: Union[str, None] = None,
        tesseract_lang: Union[str, None] = None,
        keep_tables_as_one_chunk: Union[bool, None] = None,
        chunk_by_page: Union[bool, None] = None,
        handwriting_check: Union[bool, None] = None,
        timeout: Union[float, None] = None,
        ingest_mode: Union[str, None] = None,
    ) -> Job:
        """Crawl and ingest a URL into a collection.

        The web page or document linked from this URL will be imported.

        Args:
            collection_id:
                String id of the collection to add the ingested documents into.
            url:
                String of the url to crawl.
            gen_doc_summaries:
                Whether to auto-generate document summaries (uses LLM)
            gen_doc_questions:
                Whether to auto-generate sample questions for each document (uses LLM)
            follow_links:
                Whether to import all web pages linked from this URL will be imported.
                External links will be ignored. Links to other pages on the same domain will
                be followed as long as they are at the same level or below the URL you specify.
                Each page will be transformed into a PDF document.
            max_depth:
                Max depth of recursion when following links, only when follow_links is True.
                Max_depth of 0 means don't follow any links, max_depth of 1 means follow only top-level links, etc.
                Use -1 for automatic (system settings).
            max_documents:
                Max number of documents when following links, only when follow_links is True.
                Use None for automatic (system defaults).
                Use -1 for max (system limit).
            audio_input_language:
                Language of audio files. Defaults to "auto" language detection. Pass empty string to see choices.
            ocr_model:
                Which method to use to extract text from images using AI-enabled optical character recognition (OCR) models.
                Pass empty string to see choices.
                docTR is best for Latin text, PaddleOCR is best for certain non-Latin languages, Tesseract covers a wide range of languages.
                Mississippi works well on handwriting.
                "auto" - Automatic will auto-select the best OCR model for every page.
                "off" - Disable OCR for speed, but all images will then be skipped (also no image captions will be made).
            tesseract_lang:
                Which language to use when using ocr_model="tesseract". Pass empty string to see choices.
            keep_tables_as_one_chunk:
                When tables are identified by the table parser the table tokens will be kept in a single chunk.
            chunk_by_page:
                Each page will be a chunk. `keep_tables_as_one_chunk` will be ignored if this is True.
            handwriting_check:
                Check pages for handwriting. Will use specialized models if handwriting is found.
            timeout:
                Timeout in seconds.
            ingest_mode:
                Ingest mode to use.
                "standard" - Files will be ingested for use with RAG
                "agent_only" - Bypasses standard ingestion. Files can only be used with agents.
        """

        def call(c: H2OGPTEAsync):
            return c.ingest_website(
                collection_id,
                url,
                gen_doc_summaries,
                gen_doc_questions,
                follow_links,
                max_depth,
                max_documents,
                audio_input_language,
                ocr_model,
                tesseract_lang,
                keep_tables_as_one_chunk,
                chunk_by_page,
                handwriting_check,
                timeout,
                ingest_mode,
            )

        return self._run_async(call)

    def ingest_agent_only_to_standard(
        self,
        collection_id: str,
        document_id: str,
        gen_doc_summaries: Union[bool, None] = None,
        gen_doc_questions: Union[bool, None] = None,
        audio_input_language: Union[str, None] = None,
        ocr_model: Union[str, None] = None,
        restricted: bool = False,
        permissions: Union[List[SharePermission], None] = None,
        tesseract_lang: Union[str, None] = None,
        keep_tables_as_one_chunk: Union[bool, None] = None,
        chunk_by_page: Union[bool, None] = None,
        handwriting_check: Union[bool, None] = None,
        timeout: Union[float, None] = None,
    ):
        """For files uploaded in "agent_only" ingest mode, convert to PDF and parse

        See Also:
            upload: Upload the files into the system to then be ingested into a collection.
            delete_upload: Delete uploaded file

        Args:
            collection_id:
                String id of the collection to add the ingested documents into.
            document_id:
                ID of document to be parsed.
            gen_doc_summaries:
                Whether to auto-generate document summaries (uses LLM)
            gen_doc_questions:
                Whether to auto-generate sample questions for each document (uses LLM)
            audio_input_language:
                Language of audio files. Defaults to "auto" language detection. Pass empty string to see choices.
            ocr_model:
                Which method to use to extract text from images using AI-enabled optical character recognition (OCR) models.
                Pass empty string to see choices.
                docTR is best for Latin text, PaddleOCR is best for certain non-Latin languages, Tesseract covers a wide range of languages.
                Mississippi works well on handwriting.
                "auto" - Automatic will auto-select the best OCR model for every page.
                "off" - Disable OCR for speed, but all images will then be skipped (also no image captions will be made).
            restricted:
                Whether the document should be restricted only to certain users.
            permissions:
                List of permissions. Each permission is a SharePermission object.
            tesseract_lang:
                Which language to use when using ocr_model="tesseract". Pass empty string to see choices.
            keep_tables_as_one_chunk:
                When tables are identified by the table parser the table tokens will be kept in a single chunk.
            chunk_by_page:
                Each page will be a chunk. `keep_tables_as_one_chunk` will be ignored if this is True.
            handwriting_check:
                Check pages for handwriting. Will use specialized models if handwriting is found.
            timeout:
                Timeout in seconds.
        """

        def call(c: H2OGPTEAsync):
            return c.ingest_agent_only_to_standard(
                collection_id,
                document_id,
                gen_doc_summaries,
                gen_doc_questions,
                audio_input_language,
                ocr_model,
                restricted,
                permissions,
                tesseract_lang,
                keep_tables_as_one_chunk,
                chunk_by_page,
                handwriting_check,
                timeout,
            )

        return self._run_async(call)

    def list_chat_messages(
        self, chat_session_id: str, offset: int, limit: int
    ) -> List[ChatMessage]:
        """Fetch chat message and metadata for messages in a chat session.

        Messages without a `reply_to` are from the end user, messages with a `reply_to`
        are from an LLM and a response to a specific user message.

        Args:
            chat_session_id:
                String id of the chat session to filter by.
            offset:
                How many chat messages to skip before returning.
            limit:
                How many chat messages to return.

        Returns:
            list of ChatMessage: Text and metadata for chat messages.
        """

        def call(c: H2OGPTEAsync):
            return c.list_chat_messages(chat_session_id, offset, limit)

        return self._run_async(call)

    def list_chat_message_references(
        self,
        message_id: str,
        limit: Union[int, None] = None,
    ) -> List[ChatMessageReference]:
        """Fetch metadata for references of a chat message.

        References are only available for messages sent from an LLM, an empty list will be returned
        for messages sent by the user.

        Args:
            message_id:
                String id of the message to get references for.
            limit:
                The number of references to consider based on the highest confidence scores.

        Returns:
            list of ChatMessageReference: Metadata including the document name, polygon information,
            and score.
        """

        def call(c: H2OGPTEAsync):
            return c.list_chat_message_references(message_id, limit)

        return self._run_async(call)

    def list_list_chat_message_meta(self, message_id: str) -> List[ChatMessageMeta]:
        """Fetch chat message meta information.

        Args:
            message_id:
                Message id to which the metadata should be pulled.

        Returns:
            list of ChatMessageMeta: Metadata about the chat message.
        """

        def call(c: H2OGPTEAsync):
            return c.list_list_chat_message_meta(message_id)

        return self._run_async(call)

    def list_chat_message_meta_part(
        self, message_id: str, info_type: str
    ) -> ChatMessageMeta:
        """Fetch one chat message meta information.

        Args:
            message_id:
                Message id to which the metadata should be pulled.
            info_type:
                Metadata type to fetch.
                Valid choices are: "self_reflection", "usage_stats", "prompt_raw", "llm_only", "hyde1", "py_client_code"

        Returns:
            ChatMessageMeta: Metadata information about the chat message.
        """

        def call(c: H2OGPTEAsync):
            return c.list_chat_message_meta_part(message_id, info_type)

        return self._run_async(call)

    def list_chat_messages_full(
        self, chat_session_id: str, offset: int, limit: int
    ) -> List[ChatMessageFull]:
        """Fetch chat message and metadata for messages in a chat session.

        Messages without a `reply_to` are from the end user, messages with a `reply_to`
        are from an LLM and a response to a specific user message.

        Args:
            chat_session_id:
                String id of the chat session to filter by.
            offset:
                How many chat messages to skip before returning.
            limit:
                How many chat messages to return.

        Returns:
            list of ChatMessageFull: Text and metadata for chat messages.
        """

        def call(c: H2OGPTEAsync):
            return c.list_chat_messages_full(chat_session_id, offset, limit)

        return self._run_async(call)

    def list_chat_sessions_for_collection(
        self,
        collection_id: str,
        offset: int,
        limit: int,
    ) -> List[ChatSessionForCollection]:
        """Fetch chat session metadata for chat sessions in a collection.

        Args:
            collection_id:
                String id of the collection to filter by.
            offset:
                How many chat sessions to skip before returning.
            limit:
                How many chat sessions to return.

        Returns:
            list of ChatSessionForCollection: Metadata about each chat session including the
            latest message.
        """

        def call(c: H2OGPTEAsync):
            return c.list_chat_sessions_for_collection(collection_id, offset, limit)

        return self._run_async(call)

    def list_chat_sessions_for_document(
        self,
        document_id: str,
        offset: int,
        limit: int,
    ) -> List[ChatSessionForDocument]:
        """Fetch chat session metadata for chat session that produced a specific document (typically through agents).

        Args:
            document_id:
                String id of the document to filter by.
            offset:
                How many chat sessions to skip before returning.
            limit:
                How many chat sessions to return.

        Returns:
            list of ChatSessionForDocument: Metadata about each chat session including the
            latest message.
        """

        def call(c: H2OGPTEAsync):
            return c.list_chat_sessions_for_document(document_id, offset, limit)

        return self._run_async(call)

    def rename_chat_session(self, chat_session_id: str, name: str):
        """Update a chat session name

        Args:
            chat_session_id:
                String id of the document to search for.
            name:
                The new chat session name.
        """

        def call(c: H2OGPTEAsync):
            return c.rename_chat_session(chat_session_id, name)

        return self._run_async(call)

    def list_collections_for_document(
        self, document_id: str, offset: int, limit: int
    ) -> List[CollectionInfo]:
        """Fetch metadata about each collection the document is a part of.

        At this time, each document will only be available in a single collection.

        Args:
            document_id:
                String id of the document to search for.
            offset:
                How many collections to skip before returning.
            limit:
                How many collections to return.

        Returns:
            list of CollectionInfo: Metadata about each collection.
        """

        def call(c: H2OGPTEAsync):
            return c.list_collections_for_document(document_id, offset, limit)

        return self._run_async(call)

    def get_default_collection(self) -> CollectionInfo:
        """Get the default collection, to be used for collection API-keys.

        Returns:
            CollectionInfo: Default collection info.
        """

        def call(c: H2OGPTEAsync):
            return c.get_default_collection()

        return self._run_async(call)

    def list_documents_in_collection(
        self,
        collection_id: str,
        offset: int,
        limit: int,
        metadata_filter: dict = {},
    ) -> List[DocumentInfo]:
        """Fetch document metadata for documents in a collection.

        Args:
            collection_id:
                String id of the collection to filter by.
            offset:
                How many documents to skip before returning.
            limit:
                How many documents to return.
            metadata_filter:
                Metadata filter to apply to the documents.

        Returns:
            list of DocumentInfo: Metadata about each document.
        """

        def call(c: H2OGPTEAsync):
            return c.list_documents_in_collection(
                collection_id, offset, limit, metadata_filter
            )

        return self._run_async(call)

    def list_jobs(self) -> List[Job]:
        """List the user's jobs.

        Returns:
            list of Job:
        """

        def call(c: H2OGPTEAsync):
            return c.list_jobs()

        return self._run_async(call)

    def list_recent_chat_sessions(
        self, offset: int, limit: int
    ) -> List[ChatSessionInfo]:
        """Fetch user's chat session metadata sorted by last update time.

        Chats across all collections will be accessed.

        Args:
            offset:
                How many chat sessions to skip before returning.
            limit:
                How many chat sessions to return.

        Returns:
            list of ChatSessionInfo: Metadata about each chat session including the
            latest message.
        """

        def call(c: H2OGPTEAsync):
            return c.list_recent_chat_sessions(offset, limit)

        return self._run_async(call)

    def list_question_reply_feedback_data(
        self, offset: int, limit: int
    ) -> List[QuestionReplyData]:
        """Fetch user's questions and answers that have a feedback.

        Questions and answers with metadata and feedback information.

        Args:
            offset:
                How many conversations to skip before returning.
            limit:
                How many conversations to return.

        Returns:
            list of QuestionReplyData: Metadata about questions and answers.
        """

        def call(c: H2OGPTEAsync):
            return c.list_question_reply_feedback_data(offset, limit)

        return self._run_async(call)

    def update_question_reply_feedback(
        self, reply_id: str, expected_answer: str, user_comment: str
    ):
        """Update feedback for a specific answer to a question.

        Args:
            reply_id:
                UUID of the reply.
            expected_answer:
                Expected answer.
            user_comment:
                User comment.

        Returns:
            None
        """

        def call(c: H2OGPTEAsync):
            return c.update_question_reply_feedback(
                reply_id, expected_answer, user_comment
            )

        return self._run_async(call)

    def count_question_reply_feedback(self) -> int:
        """Fetch user's questions and answers with feedback count.

        Returns:
            int: the count of questions and replies that have a user feedback.
        """

        def call(c: H2OGPTEAsync):
            return c.count_question_reply_feedback()

        return self._run_async(call)

    def list_recent_collections(self, offset: int, limit: int) -> List[CollectionInfo]:
        """Fetch user's collection metadata sorted by last update time.

        Args:
            offset:
                How many collections to skip before returning.
            limit:
                How many collections to return.

        Returns:
            list of CollectionInfo: Metadata about each collection.
        """

        def call(c: H2OGPTEAsync):
            return c.list_recent_collections(offset, limit)

        return self._run_async(call)

    def list_recent_collections_sort(
        self,
        offset: int,
        limit: int,
        sort_column: str,
        ascending: bool,
    ) -> List[CollectionInfo]:
        """Fetch user's collection metadata sorted by last update time.

        Args:
            offset:
                How many collections to skip before returning.
            limit:
                How many collections to return.
            sort_column:
                Sort column.
            ascending:
                When True, return sorted by sort_column in ascending order.

        Returns:
            list of CollectionInfo: Metadata about each collection.
        """

        def call(c: H2OGPTEAsync):
            return c.list_recent_collections_sort(offset, limit, sort_column, ascending)

        return self._run_async(call)

    def list_recent_collections_filter(
        self,
        offset: int,
        limit: int,
        current_user_only: bool = False,
        name_filter: str = "",
    ) -> List[CollectionInfo]:
        """Fetch user's collection metadata sorted by last update time with filter options.

        Args:
            offset:
                How many collections to skip before returning.
            limit:
                How many collections to return.
            current_user_only:
                When true, will only return the user owned collections.
            name_filter:
                Only returns collections with names matching this filter.

        Returns:
            list of CollectionInfo: Metadata about each collection.
        """

        def call(c: H2OGPTEAsync):
            return c.list_recent_collections_filter(
                offset, limit, current_user_only, name_filter
            )

        return self._run_async(call)

    def list_recent_collections_metadata_filter(
        self,
        offset: int,
        limit: int,
        current_user_only: bool,
        metadata_filter: dict,
    ) -> List[CollectionInfo]:
        """Fetch user's collection metadata sorted by last update time with a filter on metadata.

        Args:
            offset:
                How many collections to skip before returning.
            limit:
                How many collections to return.
            current_user_only:
                When true, will only return the user owned collections.
            metadata_filter:
                Only returns collections with metadata matching this filter.

        Returns:
            list of CollectionInfo: Metadata about each collection.
        """

        def call(c: H2OGPTEAsync):
            return c.list_recent_collections_metadata_filter(
                offset, limit, current_user_only, metadata_filter
            )

        return self._run_async(call)

    def list_all_collections_sort(
        self,
        offset: int,
        limit: int,
        sort_column: str,
        ascending: bool,
    ) -> List[CollectionInfo]:
        """Fetch all users' collection metadata sorted by last update time.

        This is for admin use only and includes private, public, and shared collections in the result.

        Args:
            offset:
                How many collections to skip before returning.
            limit:
                How many collections to return.
            sort_column:
                Sort column.
            ascending:
                When True, return sorted by sort_column in ascending order.

        Returns:
            list of CollectionInfo: Metadata about each collection.
        """

        def call(c: H2OGPTEAsync):
            return c.list_all_collections_sort(offset, limit, sort_column, ascending)

        return self._run_async(call)

    def list_collection_permissions(self, collection_id: str) -> List[SharePermission]:
        """Returns a list of access permissions for a given collection.

        The returned list of permissions denotes who has access to
        the collection and their access level.

        Args:
            collection_id:
                ID of the collection to inspect.

        Returns:
            list of SharePermission: Sharing permissions list for the given collection.
        """

        def call(c: H2OGPTEAsync):
            return c.list_collection_permissions(collection_id)

        return self._run_async(call)

    def list_users(self, offset: int, limit: int) -> List[User]:
        """List system users.

        Returns a list of all registered users fo the system, a registered user,
        is a users that has logged in at least once.

        Args:
            offset:
                How many users to skip before returning.
            limit:
                How many users to return.

        Returns:
            list of User: Metadata about each user.
        """

        def call(c: H2OGPTEAsync):
            return c.list_users(offset, limit)

        return self._run_async(call)

    def share_collection(
        self, collection_id: str, permission: SharePermission
    ) -> ShareResponseStatus:
        """Share a collection to a user.

        The permission attribute defined the level of access,
        and who can access the collection, the collection_id attribute
        denotes the collection to be shared.

        Args:
            collection_id:
                ID of the collection to share.
            permission:
                Defines the rule for sharing, i.e. permission level.

        Returns:
            ShareResponseStatus: Status of share request.
        """

        def call(c: H2OGPTEAsync):
            return c.share_collection(collection_id, permission)

        return self._run_async(call)

    def unshare_collection(
        self, collection_id: str, permission: SharePermission
    ) -> ShareResponseStatus:
        """Remove sharing of a collection to a user.

        The permission attribute defined the level of access,
        and who can access the collection, the collection_id attribute
        denotes the collection to be shared.

        In case of un-sharing, the SharePermission's user is sufficient.

        Args:
            collection_id:
                ID of the collection to un-share.
            permission:
                Defines the user for which collection access is revoked.

        ShareResponseStatus: Status of share request.
        """

        def call(c: H2OGPTEAsync):
            return c.unshare_collection(collection_id, permission)

        return self._run_async(call)

    def unshare_collection_for_all(self, collection_id: str) -> ShareResponseStatus:
        """Remove sharing of a collection to all other users but the original owner.

        Args:
            collection_id:
                ID of the collection to un-share.

        ShareResponseStatus: Status of share request.
        """

        def call(c: H2OGPTEAsync):
            return c.unshare_collection_for_all(collection_id)

        return self._run_async(call)

    def make_collection_public(self, collection_id: str) -> None:
        """Make a collection public

        Once a collection is public, it will be accessible to all
        authenticated users of the system.

        Args:
            collection_id:
                ID of the collection to make public.
        """

        def call(c: H2OGPTEAsync):
            return c.make_collection_public(collection_id)

        return self._run_async(call)

    def make_collection_private(self, collection_id: str):
        """Make a collection private

        Once a collection is private, other users will no longer
        be able to access chat history or documents related to
        the collection.

        Args:
            collection_id:
                ID of the collection to make private.
        """

        def call(c: H2OGPTEAsync):
            return c.make_collection_private(collection_id)

        return self._run_async(call)

    def share_collection_with_group(
        self, collection_id: str, permission: GroupSharePermission
    ) -> ShareResponseStatus:
        """Share a collection to a group.

        The permission attribute defines the level of access,
        and which group can access the collection, the collection_id attribute
        denotes the collection to be shared.

        Args:
            collection_id:
                ID of the collection to share.
            permission:
                Defines the rule for sharing, i.e. permission level and group.

        Returns:
            ShareResponseStatus: Status of share request.
        """

        def call(c: H2OGPTEAsync):
            return c.share_collection_with_group(collection_id, permission)

        return self._run_async(call)

    def unshare_collection_from_group(
        self,
        collection_id: str,
        permission: GroupSharePermission,
    ) -> ShareResponseStatus:
        """Remove sharing of a collection from a group.

        The permission attribute defines which group to remove access from,
        the collection_id attribute denotes the collection to be unshared.
        In case of un-sharing, the GroupSharePermission's group_id is sufficient.

        Args:
            collection_id:
                ID of the collection to un-share.
            permission:
                Defines the group for which collection access is revoked.

        Returns:
            ShareResponseStatus: Status of share request.
        """

        def call(c: H2OGPTEAsync):
            return c.unshare_collection_from_group(collection_id, permission)

        return self._run_async(call)

    def list_recent_documents(
        self, offset: int, limit: int, metadata_filter: dict = {}
    ) -> List[DocumentInfo]:
        """Fetch user's document metadata sorted by last update time.

        All documents owned by the user, regardless of collection, are accessed.

        Args:
            offset:
                How many documents to skip before returning.
            limit:
                How many documents to return.
            metadata_filter:
                Metadata filter to apply to the documents.

        Returns:
            list of DocumentInfo: Metadata about each document.
        """

        def call(c: H2OGPTEAsync):
            return c.list_recent_documents(offset, limit, metadata_filter)

        return self._run_async(call)

    def list_recent_documents_with_summaries(
        self, offset: int, limit: int
    ) -> List[DocumentInfoSummary]:
        """Fetch user's document metadata sorted by last update time, including the latest document summary.

        All documents owned by the user, regardless of collection, are accessed.

        Args:
            offset:
                How many documents to skip before returning.
            limit:
                How many documents to return.

        Returns:
            list of DocumentInfoSummary: Metadata about each document.
        """

        def call(c: H2OGPTEAsync):
            return c.list_recent_documents_with_summaries(offset, limit)

        return self._run_async(call)

    def list_recent_documents_with_summaries_sort(
        self,
        offset: int,
        limit: int,
        sort_column: str,
        ascending: bool,
    ) -> List[DocumentInfoSummary]:
        """Fetch user's document metadata sorted by last update time, including the latest document summary.

        All documents owned by the user, regardless of collection, are accessed.

        Args:
            offset:
                How many documents to skip before returning.
            limit:
                How many documents to return.
            sort_column:
                Sort column.
            ascending:
                When True, return sorted by sort_column in ascending order.

        Returns:
            list of DocumentInfoSummary: Metadata about each document.
        """

        def call(c: H2OGPTEAsync):
            return c.list_recent_documents_with_summaries_sort(
                offset, limit, sort_column, ascending
            )

        return self._run_async(call)

    def match_chunks(
        self,
        collection_id: str,
        vectors: List[List[float]],
        topics: List[str],
        offset: int,
        limit: int,
        cut_off: float = 0,
        width: int = 0,
    ) -> List[SearchResult]:
        """Find chunks related to a message using semantic search.

        Chunks are sorted by relevance and similarity score to the message.

        See Also: H2OGPTE.encode_for_retrieval to create vectors from messages.

        Args:
            collection_id:
                ID of the collection to search within.
            vectors:
                A list of vectorized message for running semantic search.
            topics:
                A list of document_ids used to filter which documents in the collection to search.
            offset:
                How many chunks to skip before returning chunks.
            limit:
                How many chunks to return.
            cut_off:
                Exclude matches with distances higher than this cut off.
            width:
                How many chunks before and after a match to return - not implemented.

        Returns:
            list of SearchResult: The document, text, score and related information of
            the chunk.
        """

        def call(c: H2OGPTEAsync):
            return c.match_chunks(
                collection_id, vectors, topics, offset, limit, cut_off, width
            )

        return self._run_async(call)

    def search_chunks(
        self,
        collection_id: str,
        query: str,
        topics: List[str],
        offset: int,
        limit: int,
    ) -> List[SearchResult]:
        """Find chunks related to a message using lexical search.

        Chunks are sorted by relevance and similarity score to the message.

        Args:
            collection_id:
                ID of the collection to search within.
            query:
                Question or imperative from the end user to search a collection for.
            topics:
                A list of document_ids used to filter which documents in the collection to search.
            offset:
                How many chunks to skip before returning chunks.
            limit:
                How many chunks to return.

        Returns:
            list of SearchResult: The document, text, score and related information of the chunk.
        """

        def call(c: H2OGPTEAsync):
            return c.search_chunks(collection_id, query, topics, offset, limit)

        return self._run_async(call)

    def list_document_chunks(
        self, document_id: str, collection_id: Union[str, None] = None
    ) -> List[SearchResult]:
        """Returns all chunks for a specific document.

        Args:
            document_id:
                ID of the document.
            collection_id:
                ID of the collection the document belongs to. If not specified, an arbitrary collections containing
                the document is chosen.
        Returns:
            list of SearchResult: The document, text, score and related information of the chunk.
        """

        def call(c: H2OGPTEAsync):
            return c.list_document_chunks(document_id, collection_id)

        return self._run_async(call)

    def set_chat_message_votes(self, chat_message_id: str, votes: int) -> Result:
        """Change the vote value of a chat message.

        Set the exact value of a vote for a chat message. Any message type can
        be updated, but only LLM response votes will be visible in the UI.
        The expectation is 0: unvoted, -1: dislike, 1 like. Values outside of this will
        not be viewable in the UI.

        Args:
            chat_message_id:
                ID of a chat message, any message can be used but only
                LLM responses will be visible in the UI.
            votes:
                Integer value for the message. Only -1 and 1 will be visible in the
                UI as dislike and like respectively.

        Returns:
            Result: The status of the update.

        Raises:
            Exception: The upload request was unsuccessful.
        """

        def call(c: H2OGPTEAsync):
            return c.set_chat_message_votes(chat_message_id, votes)

        return self._run_async(call)

    def update_collection(self, collection_id: str, name: str, description: str) -> str:
        """Update the metadata for a given collection.

        All variables are required. You can use `h2ogpte.get_collection(<id>).name` or
        description to get the existing values if you only want to change one or the other.

        Args:
            collection_id:
                ID of the collection to update.
            name:
                New name of the collection, this is required.
            description:
                New description of the collection, this is required.

        Returns:
            str: ID of the updated collection.
        """

        def call(c: H2OGPTEAsync):
            return c.update_collection(collection_id, name, description)

        return self._run_async(call)

    def update_collection_rag_type(
        self, collection_id: str, name: str, description: str, rag_type
    ) -> str:
        """Update the metadata for a given collection.

        All variables are required. You can use `h2ogpte.get_collection(<id>).name` or
        description to get the existing values if you only want to change one or the other.

        Args:
            collection_id:
                ID of the collection to update.
            name:
                New name of the collection, this is required.
            description:
                New description of the collection, this is required.
            rag_type: str one of
                    :code:`"auto"` Automatically select the best rag_type.
                    :code:`"llm_only"` LLM Only - Answer the query without any supporting document contexts.
                        Requires 1 LLM or Agent call.
                    :code:`"agent_only"` Agent Only - Answer the query with only original files passed to agent.
                        Requires 1 Agent call.
                    :code:`"rag"` RAG (Retrieval Augmented Generation) - Use supporting document contexts
                        to answer the query. Requires 1 LLM or Agent call.
                    :code:`"hyde1"` LLM Only + RAG composite - HyDE RAG (Hypothetical Document Embedding).
                        Use 'LLM Only' response to find relevant contexts from a collection for generating
                        a response. Requires 2 LLM calls.
                    :code:`"hyde2"` HyDE + RAG composite - Use the 'HyDE RAG' response to find relevant
                        contexts from a collection for generating a response. Requires 3 LLM calls.
                    :code:`"rag+"` Summary RAG - Like RAG, but uses more context and recursive
                        summarization to overcome LLM context limits. Keeps all retrieved chunks, puts
                        them in order, adds neighboring chunks, then uses the summary API to get the
                        answer. Can require several LLM calls.
                    :code:`"all_data"` All Data RAG - Like Summary RAG, but includes all document
                        chunks. Uses recursive summarization to overcome LLM context limits.
                        Can require several LLM calls.

        Returns:
            str: ID of the updated collection.
        """

        def call(c: H2OGPTEAsync):
            return c.update_collection_rag_type(
                collection_id, name, description, rag_type
            )

        return self._run_async(call)

    def reset_collection_prompt_settings(self, collection_id: str) -> str:
        """Reset the prompt settings for a given collection.

        Args:
            collection_id:
                ID of the collection to update.

        Returns:
            str: ID of the updated collection.
        """

        def call(c: H2OGPTEAsync):
            return c.reset_collection_prompt_settings(collection_id)

        return self._run_async(call)

    def update_collection_settings(
        self, collection_id: str, collection_settings: dict
    ) -> str:
        """
        Set the new collection settings, must be complete.
        Be careful not to delete any settings you want to keep.

        Args:
            collection_id:
                ID of the collection to update.
            collection_settings:
                Dictionary containing the new collection settings.

        Returns:
            str: ID of the updated collection.
        """

        def call(c: H2OGPTEAsync):
            return c.update_collection_settings(collection_id, collection_settings)

        return self._run_async(call)

    def update_collection_metadata(
        self, collection_id: str, collection_metadata: dict
    ) -> str:
        """
        Set the new collection metadata overwriting the existing metadata.
        Be careful not to delete any settings you want to keep.

        Args:
            collection_id:
                ID of the collection to update.
            collection_metadata:
                Dictionary containing the new collection metadata.

        Returns:
            str: ID of the updated collection.
        """

        def call(c: H2OGPTEAsync):
            return c.update_collection_metadata(collection_id, collection_metadata)

        return self._run_async(call)

    def update_document_name(self, document_id: str, name: str) -> str:
        """Update the name metadata for a given document.

        Args:
            document_id:
                ID of the document to update.
            name:
                New name of the document, must include file extension.

        Returns:
            str: ID of the updated document.
        """

        def call(c: H2OGPTEAsync):
            return c.update_document_name(document_id, name)

        return self._run_async(call)

    def update_document_metadata(
        self, document_id: str, document_metadata: dict
    ) -> str:
        """
        Set the new document metadata overwriting the existing metadata.
        Be careful not to delete any settings you want to keep.

        Args:
            document_id:
                ID of the document to update.
            document_metadata:
                Dictionary containing the new document metadata.

        Returns:
            str: ID of the updated document.
        """

        def call(c: H2OGPTEAsync):
            return c.update_document_metadata(document_id, document_metadata)

        return self._run_async(call)

    def update_document_uri(self, document_id: str, uri: str) -> str:
        """Update the URI metadata for a given document.

        Args:
            document_id:
                ID of the document to update.
            uri:
                New URI of the document, this is required.

        Returns:
            str: ID of the updated document.
        """

        def call(c: H2OGPTEAsync):
            return c.update_document_uri(document_id, uri)

        return self._run_async(call)

    def upload(self, file_name: str, file: Any, uri: Union[str, None] = None) -> str:
        """Upload a file to the H2OGPTE backend.

        Uploaded files are not yet accessible and need to be ingested into a collection.

        See Also:
            ingest_uploads: Add the uploaded files to a collection.
            delete_upload: Delete uploaded file

        Args:
            file_name:
                What to name the file on the server, must include file extension.
            file:
                File object to upload, often an opened file from `with open(...) as f`.
            uri:
                Optional - URI you would like to associate with the file.

        Returns:
            str: The upload id to be used in ingest jobs.

        Raises:
            Exception: The upload request was unsuccessful.
        """

        def call(c: H2OGPTEAsync):
            return c.upload(file_name, file, uri)

        return self._run_async(call)

    def list_upload(self) -> List[str]:
        """List pending file uploads to the H2OGPTE backend.

        Uploaded files are not yet accessible and need to be ingested into a collection.

        See Also:
            upload: Upload the files into the system to then be ingested into a collection.
            ingest_uploads: Add the uploaded files to a collection.
            delete_upload: Delete uploaded file

        Returns:
            List[str]: The pending upload ids to be used in ingest jobs.

        Raises:
            Exception: The upload list request was unsuccessful.
        """

        def call(c: H2OGPTEAsync):
            return c.list_upload()

        return self._run_async(call)

    def delete_upload(self, upload_id: str) -> str:
        """Delete a file previously uploaded with the "upload" method.

        See Also:
            upload: Upload the files into the system to then be ingested into a collection.
            ingest_uploads: Add the uploaded files to a collection.

        Args:
            upload_id:
                ID of a file to remove

        Returns:
            upload_id: The upload id of the removed.

        Raises:
            Exception: The delete upload request was unsuccessful.
        """

        def call(c: H2OGPTEAsync):
            return c.delete_upload(upload_id)

        return self._run_async(call)

    def get_llms(self) -> List[Dict[str, Any]]:
        """Lists metadata information about available LLMs in the environment.

        Returns:
            list of dict (string, ANY): Name and details about each available model.

        """

        def call(c: H2OGPTEAsync):
            return c.get_llms()

        return self._run_async(call)

    def get_llm_names(self) -> List[str]:
        """Lists names of available LLMs in the environment.

        Returns:
            list of string: Name of each available model.

        """

        def call(c: H2OGPTEAsync):
            return c.get_llm_names()

        return self._run_async(call)

    def get_vision_capable_llm_names(self) -> List[str]:
        """Lists names of available vision-capable multi-modal LLMs (that can natively handle images as input) in the environment.

        Returns:
            list of string: Name of each available model.

        """

        def call(c: H2OGPTEAsync):
            return c.get_vision_capable_llm_names()

        return self._run_async(call)

    def get_llm_and_auto_vision_llm_names(self) -> Dict[str, str]:
        """
        Get mapping of llm to its vision_model when ["auto"] is passed as visible_vision_models

        Returns:
            dictionary {'llm1': 'llm1_vision_llm', etc.}
        """

        def call(c: H2OGPTEAsync):
            return c.get_llm_and_auto_vision_llm_names()

        return self._run_async(call)

    def get_reasoning_capable_llm_names(self) -> List[str]:
        """Lists names of available reasoning-capable (that can natively reason) in the environment.

        Returns:
            list of string: Name of each available model.

        """

        def call(c: H2OGPTEAsync):
            return c.get_reasoning_capable_llm_names()

        return self._run_async(call)

    def get_llm_and_auto_reasoning_llm_names(self) -> Dict[str, str]:
        """
        Get mapping of llm to its reasoning_model when ["auto"] is passed as visible_reasoning_models

        Returns:
            dictionary {'llm1': 'llm1_reasoning_llm', etc.}
        """

        def call(c: H2OGPTEAsync):
            return c.get_llm_and_auto_reasoning_llm_names()

        return self._run_async(call)

    def download_document(
        self,
        destination_directory: Union[str, Path],
        destination_file_name: str,
        document_id: str,
    ) -> Path:
        """Downloads a document to a local system directory.

        Args:
            destination_directory:
                Destination directory to save file into.
            destination_file_name:
                Destination file name.
            document_id:
                Document ID.

        Returns:
            Path: Path of downloaded document
        """

        def call(c: H2OGPTEAsync):
            return c.download_document(
                destination_directory, destination_file_name, document_id
            )

        return self._run_async(call)

    def get_document_content(self, file_name: str, document_id: str) -> bytes:
        """Downloads a document and return its content as a byte array.

        Args:
            file_name:
                File name.
            document_id:
                Document ID.

        Returns:
            Path: File content

        """

        def call(c: H2OGPTEAsync):
            return c.get_document_content(file_name, document_id)

        return self._run_async(call)

    def list_recent_prompt_templates(
        self, offset: int, limit: int
    ) -> List[PromptTemplate]:
        """Fetch user's prompt templates sorted by last update time.

        Args:
            offset:
                How many prompt templates to skip before returning.
            limit:
                How many prompt templates to return.

        Returns:
            list of PromptTemplate: set of prompts
        """

        def call(c: H2OGPTEAsync):
            return c.list_recent_prompt_templates(offset, limit)

        return self._run_async(call)

    def list_recent_prompt_templates_sort(
        self,
        offset: int,
        limit: int,
        sort_column: str,
        ascending: bool,
    ) -> List[PromptTemplate]:
        """Fetch user's prompt templates sorted by last update time.

        Args:
            offset:
                How many prompt templates to skip before returning.
            limit:
                How many prompt templates to return.
            sort_column:
                Sort column.
            ascending:
                When True, return sorted by sort_column in ascending order.

        Returns:
            list of PromptTemplate: set of prompts
        """

        def call(c: H2OGPTEAsync):
            return c.list_recent_prompt_templates_sort(
                offset, limit, sort_column, ascending
            )

        return self._run_async(call)

    def get_prompt_template(self, id: Union[str, None] = None) -> PromptTemplate:
        """Get a prompt template

        Args:
            id:
                String id of the prompt template to retrieve or None for default

        Returns:
            PromptTemplate: prompts

        Raises:
            KeyError: The prompt template was not found.
        """

        def call(c: H2OGPTEAsync):
            return c.get_prompt_template(id)

        return self._run_async(call)

    def delete_prompt_templates(self, ids: Iterable[str]) -> Result:
        """Deletes prompt templates

        Args:
            ids:
                List of string ids of prompte templates to delete from the system.

        Returns:
            Result: Status of the delete job.
        """

        def call(c: H2OGPTEAsync):
            return c.delete_prompt_templates(ids)

        return self._run_async(call)

    def update_prompt_template(
        self,
        id: str,
        name: str,
        description: Union[str, None] = None,
        lang: Union[str, None] = None,
        system_prompt: Union[str, None] = None,
        pre_prompt_query: Union[str, None] = None,
        prompt_query: Union[str, None] = None,
        hyde_no_rag_llm_prompt_extension: Union[str, None] = None,
        pre_prompt_summary: Union[str, None] = None,
        prompt_summary: Union[str, None] = None,
        system_prompt_reflection: Union[str, None] = None,
        pre_prompt_reflection: Union[str, None] = None,
        prompt_reflection: Union[str, None] = None,
        auto_gen_description_prompt: Union[str, None] = None,
        auto_gen_document_summary_pre_prompt_summary: Union[str, None] = None,
        auto_gen_document_summary_prompt_summary: Union[str, None] = None,
        auto_gen_document_sample_questions_prompt: Union[str, None] = None,
        default_sample_questions: Union[List[str], None] = None,
        image_batch_image_prompt: Union[str, None] = None,
        image_batch_final_prompt: Union[str, None] = None,
    ) -> str:
        """
        Update a prompt template

        Args:
            id:
                String ID of the prompt template to update
            name:
                Name of the prompt template
            description:
                Description of the prompt template
            lang:
                Language code
            system_prompt:
                System Prompt
            pre_prompt_query:
                Text that is prepended before the contextual document chunks.
            prompt_query:
                Text that is appended to the beginning of the user's message.
            hyde_no_rag_llm_prompt_extension:
                LLM prompt extension.
            pre_prompt_summary:
                Prompt that goes before each large piece of text to summarize
            prompt_summary:
                Prompt that goes after each large piece of text to summarize
            system_prompt_reflection:
                System Prompt for self-reflection
            pre_prompt_reflection:
                Deprecated - ignored
            prompt_reflection:
                Template for self-reflection, must contain two occurrences of %s for full previous prompt (including system prompt, document related context and prompts if applicable, and user prompts) and answer
            auto_gen_description_prompt:
                prompt to create a description of the collection.
            auto_gen_document_summary_pre_prompt_summary:
                pre_prompt_summary for summary of a freshly imported document (if enabled).
            auto_gen_document_summary_prompt_summary:
                prompt_summary for summary of a freshly imported document (if enabled).
            auto_gen_document_sample_questions_prompt:
                prompt to create sample questions for a freshly imported document (if enabled).
            default_sample_questions:
                default sample questions in case there are no auto-generated sample questions.
            image_batch_final_prompt:
                Prompt for each image batch for vision models
            image_batch_image_prompt:
                Prompt to reduce all answers each image batch for vision models

        Returns:
            str: The ID of the updated prompt template.
        """

        def call(c: H2OGPTEAsync):
            return c.update_prompt_template(
                id,
                name,
                description,
                lang,
                system_prompt,
                pre_prompt_query,
                prompt_query,
                hyde_no_rag_llm_prompt_extension,
                pre_prompt_summary,
                prompt_summary,
                system_prompt_reflection,
                pre_prompt_reflection,
                prompt_reflection,
                auto_gen_description_prompt,
                auto_gen_document_summary_pre_prompt_summary,
                auto_gen_document_summary_prompt_summary,
                auto_gen_document_sample_questions_prompt,
                default_sample_questions,
                image_batch_image_prompt,
                image_batch_final_prompt,
            )

        return self._run_async(call)

    def create_prompt_template(
        self,
        name: str,
        description: Union[str, None] = None,
        lang: Union[str, None] = None,
        system_prompt: Union[str, None] = None,
        pre_prompt_query: Union[str, None] = None,
        prompt_query: Union[str, None] = None,
        hyde_no_rag_llm_prompt_extension: Union[str, None] = None,
        pre_prompt_summary: Union[str, None] = None,
        prompt_summary: Union[str, None] = None,
        system_prompt_reflection: Union[str, None] = None,
        pre_prompt_reflection: Union[str, None] = None,
        prompt_reflection: Union[str, None] = None,
        auto_gen_description_prompt: Union[str, None] = None,
        auto_gen_document_summary_pre_prompt_summary: Union[str, None] = None,
        auto_gen_document_summary_prompt_summary: Union[str, None] = None,
        auto_gen_document_sample_questions_prompt: Union[str, None] = None,
        default_sample_questions: Union[List[str], None] = None,
        image_batch_image_prompt: Union[str, None] = None,
        image_batch_final_prompt: Union[str, None] = None,
    ) -> str:
        """
        Create a new prompt template

        Args:
            name:
                Name of the prompt template
            description:
                Description of the prompt template
            lang:
                Language code
            system_prompt:
                System Prompt
            pre_prompt_query:
                Text that is prepended before the contextual document chunks.
            prompt_query:
                Text that is appended to the beginning of the user's message.
            hyde_no_rag_llm_prompt_extension:
                LLM prompt extension.
            pre_prompt_summary:
                Prompt that goes before each large piece of text to summarize
            prompt_summary:
                Prompt that goes after each large piece of text to summarize
            system_prompt_reflection:
                System Prompt for self-reflection
            pre_prompt_reflection:
                Deprecated - ignored
            prompt_reflection:
                Template for self-reflection, must contain two occurrences of %s for full previous prompt (including system prompt, document related context and prompts if applicable, and user prompts) and answer
            auto_gen_description_prompt:
                prompt to create a description of the collection.
            auto_gen_document_summary_pre_prompt_summary:
                pre_prompt_summary for summary of a freshly imported document (if enabled).
            auto_gen_document_summary_prompt_summary:
                prompt_summary for summary of a freshly imported document (if enabled).
            auto_gen_document_sample_questions_prompt:
                prompt to create sample questions for a freshly imported document (if enabled).
            default_sample_questions:
                default sample questions in case there are no auto-generated sample questions.
            image_batch_final_prompt:
                Prompt for each image batch for vision models
            image_batch_image_prompt:
                Prompt to reduce all answers each image batch for vision models

        Returns:
            str: The ID of the newly created prompt template.
        """

        def call(c: H2OGPTEAsync):
            return c.create_prompt_template(
                name,
                description,
                lang,
                system_prompt,
                pre_prompt_query,
                prompt_query,
                hyde_no_rag_llm_prompt_extension,
                pre_prompt_summary,
                prompt_summary,
                system_prompt_reflection,
                pre_prompt_reflection,
                prompt_reflection,
                auto_gen_description_prompt,
                auto_gen_document_summary_pre_prompt_summary,
                auto_gen_document_summary_prompt_summary,
                auto_gen_document_sample_questions_prompt,
                default_sample_questions,
                image_batch_image_prompt,
                image_batch_final_prompt,
            )

        return self._run_async(call)

    def count_prompt_templates(self) -> int:
        """Counts number of prompt templates

        Returns:
            int: The count of prompt templates
        """

        def call(c: H2OGPTEAsync):
            return c.count_prompt_templates()

        return self._run_async(call)

    def share_prompt(
        self, prompt_id: str, permission: SharePermission
    ) -> ShareResponseStatus:
        """Share a prompt template to a user.

        Args:
            prompt_id:
                ID of the prompt template to share.
            permission:
                Defines the rule for sharing, i.e. permission level.

        Returns:
            ShareResponseStatus: Status of share request.
        """

        def call(c: H2OGPTEAsync):
            return c.share_prompt(prompt_id, permission)

        return self._run_async(call)

    def unshare_prompt(
        self, prompt_id: str, permission: SharePermission
    ) -> ShareResponseStatus:
        """Remove sharing of a prompt template to a user.

        Args:
            prompt_id:
                ID of the prompt template to un-share.
            permission:
                Defines the user for which collection access is revoked.

        ShareResponseStatus: Status of share request.
        """

        def call(c: H2OGPTEAsync):
            return c.unshare_prompt(prompt_id, permission)

        return self._run_async(call)

    def unshare_prompt_for_all(self, prompt_id: str) -> ShareResponseStatus:
        """Remove sharing of a prompt template to all other users but the original owner

        Args:
            prompt_id:
                ID of the prompt template to un-share.

        ShareResponseStatus: Status of share request.
        """

        def call(c: H2OGPTEAsync):
            return c.unshare_prompt_for_all(prompt_id)

        return self._run_async(call)

    def list_prompt_permissions(self, prompt_id: str) -> List[SharePermission]:
        """Returns a list of access permissions for a given prompt template.

        The returned list of permissions denotes who has access to
        the prompt template and their access level.

        Args:
            prompt_id:
                ID of the prompt template to inspect.

        Returns:
            list of SharePermission: Sharing permissions list for the given prompt template.
        """

        def call(c: H2OGPTEAsync):
            return c.list_prompt_permissions(prompt_id)

        return self._run_async(call)

    def set_collection_prompt_template(
        self,
        collection_id: str,
        prompt_template_id: Union[str, None],
        strict_check: bool = False,
    ) -> str:
        """Set the prompt template for a collection

        Args:
            collection_id:
                ID of the collection to update.
            prompt_template_id:
                ID of the prompt template to get the prompts from. None to delete and fall back to system defaults.
            strict_check:
                whether to check that the collection's embedding model and the prompt template are optimally compatible

        Returns:
            str: ID of the updated collection.
        """

        def call(c: H2OGPTEAsync):
            return c.set_collection_prompt_template(
                collection_id, prompt_template_id, strict_check
            )

        return self._run_async(call)

    def get_collection_prompt_template(
        self, collection_id: str
    ) -> Union[PromptTemplate, None]:
        """Get the prompt template for a collection

        Args:
            collection_id:
                ID of the collection

        Returns:
            str: ID of the prompt template.
        """

        def call(c: H2OGPTEAsync):
            return c.get_collection_prompt_template(collection_id)

        return self._run_async(call)

    def set_chat_session_prompt_template(
        self, chat_session_id: str, prompt_template_id: Union[str, None]
    ) -> str:
        """Set the prompt template for a chat_session

        Args:
            chat_session_id:
                ID of the chat session
            prompt_template_id:
                ID of the prompt template to get the prompts from. None to delete and fall back to system defaults.

        Returns:
            str: ID of the updated chat session
        """

        def call(c: H2OGPTEAsync):
            return c.set_chat_session_prompt_template(
                chat_session_id, prompt_template_id
            )

        return self._run_async(call)

    def get_chat_session_prompt_template(
        self, chat_session_id: str
    ) -> Union[PromptTemplate, None]:
        """Get the prompt template for a chat_session

        Args:
            chat_session_id:
                ID of the chat session

        Returns:
            str: ID of the prompt template.
        """

        def call(c: H2OGPTEAsync):
            return c.get_chat_session_prompt_template(chat_session_id)

        return self._run_async(call)

    def set_chat_session_collection(
        self, chat_session_id: str, collection_id: Union[str, None]
    ) -> str:
        """Set the prompt template for a chat_session

        Args:
            chat_session_id:
                ID of the chat session
            collection_id:
                ID of the collection, or None to chat with the LLM only.

        Returns:
            str: ID of the updated chat session
        """

        def call(c: H2OGPTEAsync):
            return c.set_chat_session_collection(chat_session_id, collection_id)

        return self._run_async(call)

    def download_reference_highlighting(
        self,
        message_id: str,
        destination_directory: str,
        output_type: str = "combined",
        limit: Union[int, None] = None,
    ) -> list:
        """Get PDFs with reference highlighting

        Args:
            message_id:
                ID of the message to get references from
            destination_directory:
                Destination directory to save files into.
            output_type: str one of
                :code:`"combined"` Generates a PDF file for each source document, with all relevant chunks highlighted
                in each respective file. This option consolidates all highlights for each source document into a single
                PDF, making it easy to view all highlights related to that document at once.
                :code:`"split"` Generates a separate PDF file for each chunk, with only the relevant chunk highlighted
                in each file. This option is useful for focusing on individual sections without interference from other
                parts of the text. The output files names will be in the format "{document_id}_{chunk_id}.pdf"
            limit:
                The number of references to consider based on the highest confidence scores.

        Returns:
            list[Path]: List of paths of downloaded documents with highlighting

        """

        def call(c: H2OGPTEAsync):
            return c.download_reference_highlighting(
                message_id, destination_directory, output_type, limit
            )

        return self._run_async(call)

    def tag_document(self, document_id: str, tag_name: str) -> str:
        """Adds a tag to a document.

        Args:
            document_id:
                String id of the document to attach the tag to.
            tag_name:
                String representing the tag to attach.

        Returns:
            String: The id of the newly created tag.
        """

        def call(c: H2OGPTEAsync):
            return c.tag_document(document_id, tag_name)

        return self._run_async(call)

    def untag_document(self, document_id: str, tag_name: str) -> str:
        """Removes an existing tag from a document.

        Args:
            document_id:
                String id of the document to remove the tag from.
            tag_name:
                String representing the tag to remove.

        Returns:
            String: The id of the removed tag.
        """

        def call(c: H2OGPTEAsync):
            return c.untag_document(document_id, tag_name)

        return self._run_async(call)

    def get_tag(self, tag_name: str) -> Tag:
        """Returns an existing tag.

        Args:
            tag_name:
                String The name of the tag to retrieve.

        Returns:
            Tag: The requested tag.

        Raises:
            KeyError: The tag was not found.
        """

        def call(c: H2OGPTEAsync):
            return c.get_tag(tag_name)

        return self._run_async(call)

    def create_tag(self, tag_name: str) -> str:
        """Creates a new tag.

        Args:
            tag_name:
                String representing the tag to create.

        Returns:
            String: The id of the created tag.
        """

        def call(c: H2OGPTEAsync):
            return c.create_tag(tag_name)

        return self._run_async(call)

    def update_tag(self, tag_name: str, description: str, format: str) -> str:
        """Updates a  tag.

        Args:
            tag_name:
                String representing the tag to update.
            description:
                String describing the tag.
            format:
                String representing the format of the tag.

        Returns:
            String: The id of the updated tag.
        """

        def call(c: H2OGPTEAsync):
            return c.update_tag(tag_name, description, format)

        return self._run_async(call)

    def list_all_tags(self) -> List[Tag]:
        """Lists all existing tags.

        Returns:
            List of Tags: List of existing tags.
        """

        def call(c: H2OGPTEAsync):
            return c.list_all_tags()

        return self._run_async(call)

    def list_documents_from_tags(
        self, collection_id: str, tags: List[str]
    ) -> List[Document]:
        """Lists documents that have the specified set of tags within a collection.
        Args:
            collection_id:
                String The id of the collection to find documents in.
            tags:
                List of Strings representing the tags to retrieve documents for.

        Returns:
            List of Documents: All the documents with the specified tags.
        """

        def call(c: H2OGPTEAsync):
            return c.list_documents_from_tags(collection_id, tags)

        return self._run_async(call)

    def add_user_document_permission(
        self, user_id: str, document_id: str
    ) -> [str, str]:
        """Associates a user with a document they have permission on.
        Args:
            user_id:
                String The id of the user that has the permission.
            document_id:
                String The id of the document that the permission is for.

        Returns:
            [user_id, document_id]: A tuple containing the user_id and document_id.
        """

        def call(c: H2OGPTEAsync):
            return c.add_user_document_permission(user_id, document_id)

        return self._run_async(call)

    def list_system_permissions(self) -> List[UserPermission]:
        def call(c: H2OGPTEAsync):
            return c.list_system_permissions()

        return self._run_async(call)

    def list_system_roles(self) -> List[UserRole]:
        def call(c: H2OGPTEAsync):
            return c.list_system_roles()

        return self._run_async(call)

    def list_system_groups(self) -> List[UserGroup]:
        def call(c: H2OGPTEAsync):
            return c.list_system_groups()

        return self._run_async(call)

    def list_user_roles(self, user_id: Union[str, None] = None) -> List[UserRole]:
        def call(c: H2OGPTEAsync):
            return c.list_user_roles(user_id)

        return self._run_async(call)

    def list_group_roles(self, group_id: str) -> List[UserRole]:
        def call(c: H2OGPTEAsync):
            return c.list_group_roles(group_id)

        return self._run_async(call)

    def list_user_permissions(
        self, user_id: Union[str, None] = None
    ) -> List[UserPermission]:
        def call(c: H2OGPTEAsync):
            return c.list_user_permissions(user_id)

        return self._run_async(call)

    def list_group_permissions(self, group_id: str) -> List[UserPermission]:
        def call(c: H2OGPTEAsync):
            return c.list_group_permissions(group_id)

        return self._run_async(call)

    def list_group_permissions_by_name(
        self, group_names: List[str]
    ) -> List[UserPermission]:
        def call(c: H2OGPTEAsync):
            return c.list_group_permissions_by_name(group_names)

        return self._run_async(call)

    def list_user_role_permissions(self, roles: List[str]) -> List[UserPermission]:
        def call(c: H2OGPTEAsync):
            return c.list_user_role_permissions(roles)

        return self._run_async(call)

    def add_role_to_user(self, user_id: str, roles: List[str]) -> List[UserRole]:
        def call(c: H2OGPTEAsync):
            return c.add_role_to_user(user_id, roles)

        return self._run_async(call)

    def reset_roles_for_user(self, user_id: str, roles: List[str]) -> List[UserRole]:
        def call(c: H2OGPTEAsync):
            return c.reset_roles_for_user(user_id, roles)

        return self._run_async(call)

    def remove_role_from_user(self, user_id: str, roles: List[str]) -> List[UserRole]:
        def call(c: H2OGPTEAsync):
            return c.remove_role_from_user(user_id, roles)

        return self._run_async(call)

    def add_role_to_group(self, group_id: str, roles: List[str]) -> List[UserRole]:
        def call(c: H2OGPTEAsync):
            return c.add_role_to_group(group_id, roles)

        return self._run_async(call)

    def reset_roles_for_group(self, group_id: str, roles: List[str]) -> List[UserRole]:
        def call(c: H2OGPTEAsync):
            return c.reset_roles_for_group(group_id, roles)

        return self._run_async(call)

    def remove_role_from_group(self, group_id: str, roles: List[str]) -> List[UserRole]:
        def call(c: H2OGPTEAsync):
            return c.remove_role_from_group(group_id, roles)

        return self._run_async(call)

    def is_permission_granted(self, permission: str) -> bool:
        def call(c: H2OGPTEAsync):
            return c.is_permission_granted(permission)

        return self._run_async(call)

    def is_collection_permission_granted(
        self, collection_id: str, permission: str
    ) -> bool:
        def call(c: H2OGPTEAsync):
            return c.is_collection_permission_granted(collection_id, permission)

        return self._run_async(call)

    def create_user_role(self, name: str, description: str) -> UserRole:
        def call(c: H2OGPTEAsync):
            return c.create_user_role(name, description)

        return self._run_async(call)

    def create_user_group(self, name: str, description: str) -> UserGroup:
        def call(c: H2OGPTEAsync):
            return c.create_user_group(name, description)

        return self._run_async(call)

    def delete_user_roles_by_ids(self, roles_ids: Iterable[str]) -> Result:
        def call(c: H2OGPTEAsync):
            return c.delete_user_roles_by_ids(roles_ids)

        return self._run_async(call)

    def delete_user_roles_by_names(self, roles_names: Iterable[str]) -> Result:
        def call(c: H2OGPTEAsync):
            return c.delete_user_roles_by_names(roles_names)

        return self._run_async(call)

    def delete_user_groups_by_ids(self, groups_ids: Iterable[str]) -> Result:
        def call(c: H2OGPTEAsync):
            return c.delete_user_groups_by_ids(groups_ids)

        return self._run_async(call)

    def delete_user_groups_by_names(self, groups_names: Iterable[str]) -> Result:
        def call(c: H2OGPTEAsync):
            return c.delete_user_groups_by_names(groups_names)

        return self._run_async(call)

    def assign_permissions_to_role(
        self, role_name: str, permission_names: Iterable[str]
    ) -> Result:
        def call(c: H2OGPTEAsync):
            return c.assign_permissions_to_role(role_name, permission_names)

        return self._run_async(call)

    def set_global_configuration(
        self,
        key_name: str,
        string_value: str,
        can_overwrite: bool,
        is_public: bool,
        value_type: str = None,
    ) -> List[ConfigItem]:
        def call(c: H2OGPTEAsync):
            return c.set_global_configuration(
                key_name, string_value, can_overwrite, is_public, value_type
            )

        return self._run_async(call)

    def get_global_configurations_by_admin(self) -> List[ConfigItem]:
        def call(c: H2OGPTEAsync):
            return c.get_global_configurations_by_admin()

        return self._run_async(call)

    def get_global_configurations(self) -> List[ConfigItem]:
        def call(c: H2OGPTEAsync):
            return c.get_global_configurations()

        return self._run_async(call)

    def bulk_delete_global_configurations(
        self, key_names: List[str]
    ) -> List[ConfigItem]:
        def call(c: H2OGPTEAsync):
            return c.bulk_delete_global_configurations(key_names)

        return self._run_async(call)

    def set_user_configuration_for_user(
        self,
        key_name: str,
        string_value: str,
        user_id: str,
        value_type: str = None,
    ) -> List[UserConfigItem]:
        def call(c: H2OGPTEAsync):
            return c.set_user_configuration_for_user(
                key_name, string_value, user_id, value_type
            )

        return self._run_async(call)

    def get_user_configurations_for_user(self, user_id: str) -> List[UserConfigItem]:
        def call(c: H2OGPTEAsync):
            return c.get_user_configurations_for_user(user_id)

        return self._run_async(call)

    def get_user_configurations(self) -> List[UserConfigItem]:
        def call(c: H2OGPTEAsync):
            return c.get_user_configurations()

        return self._run_async(call)

    def bulk_delete_user_configurations_for_user(
        self, user_id: str, key_names: List[str]
    ) -> List[UserConfigItem]:
        def call(c: H2OGPTEAsync):
            return c.bulk_delete_user_configurations_for_user(user_id, key_names)

        return self._run_async(call)

    def reset_user_configurations_for_user(
        self, key_name: str, user_id: str
    ) -> List[UserConfigItem]:
        def call(c: H2OGPTEAsync):
            return c.reset_user_configurations_for_user(key_name, user_id)

        return self._run_async(call)

    def delete_agent_directories(self, chat_session_id: str) -> bool:
        def call(c: H2OGPTEAsync):
            return c.delete_agent_directories(chat_session_id)

        return self._run_async(call)

    def get_all_directory_stats(
        self, chat_session_id: str, detail_level: int = 0
    ) -> dict:
        def call(c: H2OGPTEAsync):
            return c.get_all_directory_stats(chat_session_id, detail_level)

        return self._run_async(call)

    def get_directory_stats(
        self, directory_name: str, chat_session_id: str, detail_level: int = 0
    ) -> dict:
        def call(c: H2OGPTEAsync):
            return c.get_directory_stats(directory_name, chat_session_id, detail_level)

        return self._run_async(call)

    def get_h2ogpt_system_stats(self) -> dict:
        def call(c: H2OGPTEAsync):
            return c.get_h2ogpt_system_stats()

        return self._run_async(call)

    def create_api_key_for_user(
        self,
        user_id: str,
        name: Union[str, None] = None,
        collection_id: Union[str, None] = None,
        expires_in: Union[str, None] = None,
    ) -> str:
        """Allows admins to create a new api key for a specific user and optionally make it specific to a collection.
        Args:
            user_id:
                String: The id of the user the API key is for.
            name:
                (Optional) String: The name of the API key.
            collection_id:
                (Optional) String: The id of the specific collection.
            expires_in:
                (Optional) String: The expiration for the API key as an interval. Ex. "30 days" or "30 minutes"

        Returns:
            String: The id of the API key.
        """

        def call(c: H2OGPTEAsync):
            return c.create_api_key_for_user(user_id, name, collection_id, expires_in)

        return self._run_async(call)

    def deactivate_api_key(self, api_key_id: str) -> Result:
        """Allows admins to deactivate an API key.

        Note: You cannot undo this action.

        Args:
            api_key_id:
                String: The id of the API key.

        Returns:
            Result: Status of the deactivate request.
        """

        def call(c: H2OGPTEAsync):
            return c.deactivate_api_key(api_key_id)

        return self._run_async(call)

    def list_all_api_keys(
        self, offset: int, limit: int, key_filter: str = ""
    ) -> List[APIKey]:
        """Allows admins to list all the API keys that exist.

        Args:
            offset:
                Int: How many keys to skip before returning.
            limit:
                Int: How many keys to return.
            key_filter:
                String: Only returns keys for usernames matching this filter.

        Returns:
            List[APIKey]: List of APIKeys with metadata about each key.
        """

        def call(c: H2OGPTEAsync):
            return c.list_all_api_keys(offset, limit, key_filter)

        return self._run_async(call)

    def set_api_key_expiration(
        self, api_key_id: str, expires_in: Union[str, None] = None
    ) -> Result:
        """Allows admins to set an expiration on an API key.

        Args:
            api_key_id:
                String: The id of the API key.
            expires_in:
                (Optional) String: The expiration for the API key as an interval or None (to remove an expiration that was previously set). Ex. "30 days" or "30 minutes"

        Returns:
            Result: Status of the expiration request.
        """

        def call(c: H2OGPTEAsync):
            return c.set_api_key_expiration(api_key_id, expires_in)

        return self._run_async(call)

    def delete_api_keys(self, api_key_ids: List[str]) -> Result:
        """Allows admins to delete API keys.

        Args:
            api_key_ids:
                List[str]: The API keys to delete.

        Returns:
            Result: Status of the delete request.
        """

        def call(c: H2OGPTEAsync):
            return c.delete_api_keys(api_key_ids)

        return self._run_async(call)

    def get_agent_server_files(self, chat_session_id: str) -> List[dict]:
        def call(c: H2OGPTEAsync):
            return c.get_agent_server_files(chat_session_id)

        return self._run_async(call)

    def delete_agent_server_files(self, chat_session_id: str) -> bool:
        def call(c: H2OGPTEAsync):
            return c.delete_agent_server_files(chat_session_id)

        return self._run_async(call)
