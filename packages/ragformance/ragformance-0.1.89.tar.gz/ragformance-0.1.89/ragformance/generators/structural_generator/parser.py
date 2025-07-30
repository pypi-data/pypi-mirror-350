from __future__ import annotations

import re
import os
import uuid

from pydantic import Field
from pydantic.dataclasses import dataclass


@dataclass
class SubSection: 
    title: str
    content: str
    page_number: list[int]

@dataclass
class Section:
    title: str
    content: str
    pages_number : list[int]
    subsections : list[SubSection] = Field(default =[])

    @classmethod
    def get_sections(cls, raw_section: str, page_number: int)-> Section:
        raw_section = raw_section.strip()
        section_fields = raw_section.split("\n", maxsplit=1)
        return Section(section_fields[0], section_fields[1] if len(section_fields) >1 else "", [page_number])
        
@dataclass
class Page:
    content: str
    page_number: int
    _id: str = Field(default = str(uuid.uuid4()))
    sections: list[Section] = Field(default = [])
    subsections: list[SubSection] = Field(default = [])

    @classmethod
    def get_page(cls, raw_pages: str, page_number) -> Page:
        page_title=f"# Page {page_number}"
        page_content = raw_pages[len(page_title):].strip()
        return Page(page_content, page_number)
    
    
    def get_sections_starting_in_page(self) -> list[Section]:
        section_regexp = r"((?:\n|^)#{2}\s.*?(?=\n#{2}|\Z))"
        raw_sections = re.findall(section_regexp, self.content, re.DOTALL)
        sections = [Section.get_sections(raw_section, self.page_number) for raw_section in raw_sections]
        return sections

@dataclass
class Manual:
    pages: list[Page]
    sections: list[Section]
    name: str

    @classmethod
    def get_manual(cls, manual: str, file_name: str) -> Manual:
        pages = cls.get_pages(manual)
        sections = cls.get_sections(pages)
        return cls(pages, sections, file_name)
    
    @classmethod
    def get_pages(slf, text: str) -> list[Page]:
        pages_regexp = r"(# Page.*?(?=\n# Page|\Z))"
        pages_raw= re.findall(pages_regexp, text, re.DOTALL)
        pages = [Page.get_page(raw_page, id_page+1) for id_page, raw_page in enumerate(pages_raw)]
        return pages
    
    @classmethod
    def get_sections(cls, pages: list[Page]) -> list[Section]:
        sections_dict = {}
        subsections_dict = {}
        for id_page, page in enumerate(pages):
            if not page.content.startswith("## ") and id_page >0:
                # Unfinished section or sub-sections
                unfinished_section = pages[id_page-1].sections[-1]
                unfinished_content = page.content.split("\n##")[0]
                unfinished_section.content += unfinished_content
                unfinished_section.pages_number.append(page.page_number)
                page.sections.append(unfinished_section)
            sections = page.get_sections_starting_in_page()
            page.sections += sections
            sections_dict.update({section.title: section for section in sections})
        return  list(sections_dict.values())
    
    def get_subsections(cls, pages: list[Page], sections: list[Section]) -> list[SubSection]:
        subsections_dict = {}
        for id_page, page in enumerate(sections):
            if not page.content.startswith("## ") and id_page >0:
                unfinished_subsection = pages[id_page-1].sections[-1]
                unfinished_content = page.content.split("\n##")[0]
                unfinished_subsection.content += unfinished_content
                unfinished_subsection.pages_number.append(page.page_number)
                page.sections.append(unfinished_subsection)
            sections = page.get_sections_starting_in_page()
            page.sections += sections
            subsections_dict.update({section.title: section for section in sections})
        return  list(subsections_dict.values())
        

    @classmethod
    def get_manual_structure(cls, raw_manual: str, file_name: str) -> Manual:
        pages = Manual.get_pages(raw_manual)
        sections = Manual.get_sections(pages)
        return Manual(pages, sections, file_name)

    
    @classmethod
    def from_file(cls, folder_path: str, file_name: str)-> Manual:
        file_path = os.path.join(folder_path, file_name)
        with open(file_path) as f: 
            text = f.read()
        return cls.get_manual_structure(text, file_name)