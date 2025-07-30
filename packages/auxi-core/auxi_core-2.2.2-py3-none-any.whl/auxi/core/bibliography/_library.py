from pathlib import Path

import bibtexparser  # type: ignore

library: bibtexparser.Library = bibtexparser.parse_file(str(Path(__file__).parent.parent / "data" / "bibliography.bib"))
