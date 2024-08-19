from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List

def text_chunker(all_rows: List[dict]):
    SENTENCE_ENDINGS = [".","!","?"]
    WORD_BREAKS = ['\n','\t','}','{','[',']','(',')',' ',':',';',',']
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        separators = SENTENCE_ENDINGS + WORD_BREAKS, chunk_size = 300, chunk_overlap = 20
    )
    combined_content = ""
    page_break_positions = []
    for page in all_rows:
        combined_content += page["pageContent"]
        page_break_positions.append(len(combined_content))
    chunked_content_list = splitter.split_text(combined_content)

    chunked_with_page_numbers = []
    current_page = 1

    for chunked_content in chunked_content_list:
        chunk_end_position = combined_content.find(chunked_content) + len(chunked_content)

        while current_page < len(page_break_positions) and chunk_end_position > page_break_positions[current_page - 1]:
            current_page+=1
        
        chunked_with_page_numbers.append(
            {
                "pageContent": chunked_content,
                "pageNumber": str(current_page)
            }
        )

    return chunked_with_page_numbers
    