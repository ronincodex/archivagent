import os
import asyncio
import aiofiles
from src.archivagent.models.schemas import LiteratureCategorization

class ArchiveOrganizer:
    def __init__(self, base_dir: str = "data/processed"):
        self.base_dir = base_dir

    async def _create_file_structure(self, record: LiteratureCategorization):
        """Asynchronously generates nested directories and writes the abstraction markdown."""
        
        # Clean strings to ensure safe directory and file names on Linux
        safe_category = record.category.replace(" & ", "_").replace(" ", "_")
        safe_venue = "".join(c for c in record.venue if c.isalnum() or c in (' ', '-', '_')).strip()[:50]
        safe_title = "".join(c for c in record.title if c.isalnum() or c in (' ', '-', '_')).strip()[:50]
        
        # Construct the nested path: data/processed/Category/Venue/Year/
        dir_path = os.path.join(self.base_dir, safe_category, safe_venue, str(record.year))
        
        # Offload the blocking directory creation to a background thread 
        # to prevent freezing the event loop
        await asyncio.to_thread(os.makedirs, dir_path, exist_ok=True)
        
        file_path = os.path.join(dir_path, f"{safe_title}.md")
        
        # Use true asynchronous I/O to write the file to disk
        async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
            content = (
                f"# {record.title}\n\n"
                f"**Venue:** {record.venue}\n"
                f"**Year:** {record.year}\n\n"
                f"## Abstraction\n"
                f"{record.abstraction or 'Pending AI generation...'}\n"
            )
            await f.write(content)

    async def process_batch(self, batch: list[LiteratureCategorization]):
        """Schedules concurrent I/O tasks for a batch of records."""
        # Create a list of coroutines for the event loop
        tasks = [self._create_file_structure(record) for record in batch]
        
        # Gather executes all directory creations and file writes concurrently
        await asyncio.gather(*tasks)

# --- Testing Block ---
if __name__ == "__main__":
    from src.archivagent.ingestion.parser import DBLPStreamParser
    
    async def main():
        print("Extracting first batch from parser...")
        # Instantiating the parser with target_year=None to instantly grab records
        parser = DBLPStreamParser("data/raw/dblp.xml.gz", target_year=None, batch_size=5)
        organizer = ArchiveOrganizer()
        
        # Manually pull the first yielded batch from the generator
        batch = next(parser.parse_stream())
        
        print(f"Concurrently generating nested directories and files for {len(batch)} records...")
        await organizer.process_batch(batch)
        print("Asynchronous organization complete. Run 'tree data/processed/' to view the structure.")

    # Boot the event loop
    asyncio.run(main())
