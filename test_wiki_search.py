from langchain import Wikipedia
from langchain.agents.react.base import DocstoreExplorer

def format_step(step: str) -> str:
    return step.strip('\n').strip().replace('\n', '')

def test_wiki_search(search_term: str) -> str:
    # Initialize the Wikipedia docstore
    docstore = DocstoreExplorer(Wikipedia())
    
    try:
        # Perform the search
        result = docstore.search(search_term)
        # Format the result
        formatted_result = format_step(result)
        return formatted_result
    except Exception as e:
        return f"Error occurred: {str(e)}"

if __name__ == "__main__":
    # Example usage
    search_term = "毛泽东"  # You can change this to test different searches
    result = test_wiki_search(search_term)
    print(f"\nSearch term: {search_term}")
    print(f"Result: {result}")
