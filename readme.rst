CodeRAG
=======

CodeRAG is an AI-powered code retrieval and augmentation tool that leverages OpenAI's models (such as ``gpt-4`` or ``gpt-3.5-turbo``) for real-time codebase querying, indexing, and improvement. This project integrates a Retrieval-Augmented Generation (RAG) system to help developers seamlessly search through code, receive suggestions, and implement improvements.

Features
--------

- **Real-time Codebase Indexing**: Automatically indexes code files upon changes, with real-time updates.
- **Vector Database Search**: Utilizes FAISS or a similar vector database for fast, efficient code search using embeddings.
- **Conversational Coding Assistance**: Integrates OpenAI's GPT models to provide contextual code suggestions, improvements, and fixes.
- **Configurable Settings**: Environment-specific settings are managed using a ``.env`` file for API keys, model selection, and directories.

Tech Stack
----------

- **OpenAI API**: Leverages GPT-4o (or any other OpenAI model) for conversational and coding improvements.
- **Python**: Core functionality and API interactions.
- **FAISS (Facebook AI Similarity Search)**: For vector-based searching.
- **python-dotenv**: For managing environment variables.
- **Retrieval-Augmented Generation (RAG)**: Combines search and generative models.

Setup Instructions
------------------

Prerequisites
^^^^^^^^^^^^^

- **Python 3.8+**
- **OpenAI API Key** (You can get one `here <https://beta.openai.com/signup/>`_)
- **FAISS** (optional, depending on your choice of vector database)

Step 1: Clone the Repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   git clone https://github.com/yourusername/CodeRAG.git
   cd CodeRAG

Step 2: Install Dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a virtual environment (recommended):

.. code-block:: bash

   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Install required packages:

.. code-block:: bash

   pip install -r requirements.txt

Step 3: Configure Environment Variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a ``.env`` file in the root of the project and add the following variables:

.. code-block:: bash

   OPENAI_API_KEY=your_openai_api_key
   OPENAI_EMBEDDING_MODEL=text-embedding-ada-002
   OPENAI_CHAT_MODEL=gpt-4o
   WATCHED_DIR=path_to_your_code_directory
   FAISS_INDEX_FILE=path_to_faiss_index
   EMBEDDING_DIM=1536  # Modify if you're using a different embedding model

Step 4: Run the Application
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once configured, you can run the application using:

.. code-block:: bash

   python main.py

This will launch the application where you can interact with the conversational AI and retrieve code suggestions based on your queries.

Usage
-----

1. **Ask a Question**: Type your question or code request into the interface. The model will search the indexed codebase and provide suggestions or improvements.
2. **Review Suggestions**: You'll receive a merged or fixed version of the code based on the model's analysis.
3. **Conversational History**: The system keeps track of your queries and the AI responses for better context in future interactions.

Project Structure
-----------------

- ``main.py``: The main script to run the application.
- ``prompt_flow.py``: Handles querying OpenAI's API and manages the search and conversational history.
- ``coderag/config.py``: Stores configuration and environment variables.
- ``coderag/search.py``: Manages vector database (FAISS) searches for relevant code snippets.
- ``.env``: Holds environment-specific settings (OpenAI API keys, model configuration, etc.).
- ``requirements.txt``: Lists the Python dependencies needed to run the project.

Contributing
------------

Feel free to fork this repository, open issues, and submit pull requests.

1. Fork the repository.
2. Create your feature branch (``git checkout -b feature/your-feature``).
3. Commit your changes (``git commit -am 'Add new feature'``).
4. Push to the branch (``git push origin feature/your-feature``).
5. Open a pull request.

License
-------

This project is licensed under the Apache License. See the LICENSE file for details.