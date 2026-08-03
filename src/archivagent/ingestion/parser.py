import gzip
import lxml.etree as ET
from collections import deque
from typing import Generator
from src.archivagent.models.schemas import LiteratureCategorization, AcademicAuthor

class DBLPStreamParser:
    def __init__(self, file_path: str, target_year: int | None = None, batch_size: int = 100):
        self.file_path = file_path
        self.target_year = target_year
        self.batch_size = batch_size

    def parse_stream(self) -> Generator[list[LiteratureCategorization], None, None]:
        batch = deque()

        with gzip.open(self.file_path, 'rb') as f:
            context = ET.iterparse(
                f,
                events=('end',),
                load_dtd=True,
                resolve_entities=True
            )

            for event, elem in context:
                if elem.tag in ['article', 'inproceedings', 'book']:
                    year_elem = elem.find('year')

                    if year_elem is not None and (self.target_year is None or year_elem.text == str(self.target_year)):
                        title = elem.findtext('title', default='Unknown Title')
                        venue = elem.findtext('booktitle') or elem.findtext('journal') or 'Unknown Venue'

                        authors = [
                            AcademicAuthor(name=author.text)
                            for author in elem.findall('author') if author.text
                        ]

                        category = "Books & Guides" if elem.tag == 'book' else "Papers & Articles"

                        try:
                            valid_record = LiteratureCategorization(
                                title=title,
                                authors=authors,
                                venue=venue,
                                year=int(year_elem.text),
                                category=category,
                                abstraction=None
                            )
                            batch.append(valid_record)
                             
                        except ValueError:
                            # Silently discard genuinely malformed records
                            pass

                    elem.clear()
                    if elem.getparent() is not None:
                        elem.getparent().remove(elem)
                
                if len(batch) >= self.batch_size:
                    yield list(batch)
                    batch.clear()

            if batch:
                yield list(batch)

# --- Testing Block ---
if __name__ == "__main__":
    parser = DBLPStreamParser("data/raw/dblp.xml.gz", target_year=None, batch_size=5)
    print("Beginning iterative stream-parse of DBLP XML via lxml... (Diagnostic Mode)")
    for i, batch in enumerate(parser.parse_stream()):
        print(f"Batch {i+1}: Yielded {len(batch)} validated records.")
        for record in batch[:2]:
            print(f"  -> [{record.category}] {record.title}")
        break
