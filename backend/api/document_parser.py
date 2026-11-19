import os
import re
from docx import Document as DocxDocument
import pypdf

KNOWN_POLICIES = [
    "About the College, Governance and Applicability",
    "Admission Policy",
    "Academic Policy",
    "Attendance Policy",
    "Examination and Evaluation Policy",
    "Fee Structure, Payment and Refund Policy",
    "Scholarship and Financial Assistance Policy",
    "Student Code of Conduct and Discipline Policy",
    "Anti-Ragging Policy",
    "Prevention of Sexual Harassment and Gender Equity Policy",
    "Grievance Redressal and Equal Opportunity Policy",
    "Library Policy",
    "Information Technology and Acceptable Use Policy",
    "Data Privacy and Records Management Policy",
    "Campus Safety, Security and Health Policy",
    "Hostel Policy",
    "Transport Policy",
    "Placement and Career Development Policy",
    "Research, Publication Ethics and Anti-Plagiarism Policy",
    "Faculty and Staff Service Policy",
    "Leave Policy for Staff",
    "Financial Management, Procurement and Audit Policy",
    "Infrastructure, Maintenance and Environmental Sustainability Policy",
    "Internal Quality Assurance, Accreditation and Compliance Policy",
    "Policy Review, Amendment and Interpretation"
]

def clean_section_title(text):
    text = text.strip()
    # Check if matches known policy
    for p in KNOWN_POLICIES:
        if p.lower() in text.lower():
            return p

    # Section X or Number. Heading
    m = re.match(r'^(\d+\.\s+[A-Za-z\s,\-\(\)&]+)', text)
    if m:
        return m.group(1).strip()
    
    if text.startswith("Contents") or text.startswith("Preface"):
        return text.split('\n')[0].strip()

    return None


def extract_from_docx(file_path):
    doc = DocxDocument(file_path)
    passages = []
    current_section = "General / Introduction"
    current_clause = ""
    current_page = 1
    char_count_for_page = 0
    full_text_parts = []

    for element in doc.element.body:
        tag_name = element.tag.split('}')[-1] if '}' in element.tag else element.tag

        if tag_name == 'p':
            p_text = element.text.strip()
            if not p_text:
                continue

            sec = clean_section_title(p_text)
            if sec:
                current_section = sec
                current_clause = sec
            else:
                clause_match = re.match(r'^(\d+\.\d+)', p_text)
                if clause_match:
                    current_clause = f"{current_section} (Clause {clause_match.group(1)})"

            passages.append({
                'section': current_clause or current_section,
                'page': current_page,
                'text': p_text
            })
            full_text_parts.append(p_text)
            char_count_for_page += len(p_text)
            if char_count_for_page > 1800:
                current_page += 1
                char_count_for_page = 0

        elif tag_name == 'tbl':
            table_lines = []
            for row in element.xpath('.//w:tr'):
                cells_text = [cell.text.strip() for cell in row.xpath('.//w:tc') if cell.text and cell.text.strip()]
                if cells_text:
                    table_lines.append(" | ".join(cells_text))
            
            if table_lines:
                tbl_text = "\n".join(table_lines)
                passages.append({
                    'section': current_clause or current_section,
                    'page': current_page,
                    'text': tbl_text
                })
                full_text_parts.append(tbl_text)
                char_count_for_page += len(tbl_text)
                if char_count_for_page > 1800:
                    current_page += 1
                    char_count_for_page = 0

    return "\n\n".join(full_text_parts), passages


def extract_from_pdf(file_path):
    reader = pypdf.PdfReader(file_path)
    passages = []
    full_text_parts = []
    current_section = "General"
    current_clause = ""

    for idx, page in enumerate(reader.pages):
        page_num = idx + 1
        text = page.extract_text() or ""
        text = text.strip()
        if not text:
            continue
        
        full_text_parts.append(text)
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        for p in paragraphs:
            sec = clean_section_title(p)
            if sec:
                current_section = sec
                current_clause = sec
            else:
                clause_match = re.match(r'^(\d+\.\d+)', p)
                if clause_match:
                    current_clause = f"{current_section} (Clause {clause_match.group(1)})"

            passages.append({
                'section': current_clause or current_section,
                'page': page_num,
                'text': p
            })

    return "\n\n".join(full_text_parts), passages


def extract_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    passages = []
    lines = content.split('\n')
    current_section = "General"
    current_clause = ""
    current_page = 1
    char_count = 0
    buffer = []

    def commit_buffer():
        nonlocal buffer, char_count, current_page
        if buffer:
            p_text = "\n".join(buffer)
            passages.append({
                'section': current_clause or current_section,
                'page': current_page,
                'text': p_text
            })
            char_count += len(p_text)
            if char_count > 1800:
                current_page += 1
                char_count = 0
            buffer = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            commit_buffer()
            continue

        sec = clean_section_title(stripped)
        if sec:
            commit_buffer()
            current_section = sec
            current_clause = sec
            buffer.append(stripped)
            continue
        else:
            clause_match = re.match(r'^(\d+\.\d+)', stripped)
            if clause_match:
                commit_buffer()
                current_clause = f"{current_section} (Clause {clause_match.group(1)})"

        buffer.append(stripped)

    commit_buffer()
    return content, passages


def parse_document_file(file_path, file_type):
    file_type = file_type.lower()
    if file_type == 'docx':
        return extract_from_docx(file_path)
    elif file_type == 'pdf':
        return extract_from_pdf(file_path)
    elif file_type in ['txt', 'text']:
        return extract_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_type}. Supported: PDF, DOCX, TXT")


def chunk_passages(passages, chunk_size=500, overlap=100):
    chunks = []
    chunk_index = 0

    for item in passages:
        text = item['text']
        section = item['section']
        page = item['page']

        if len(text) <= chunk_size:
            chunks.append({
                'chunk_index': chunk_index,
                'section_title': section,
                'page_number': page,
                'content': text,
                'token_count': len(text.split())
            })
            chunk_index += 1
        else:
            start = 0
            while start < len(text):
                end = start + chunk_size
                if end < len(text):
                    last_space = text.rfind(' ', start, end)
                    if last_space != -1 and last_space > start + (chunk_size // 2):
                        end = last_space
                chunk_slice = text[start:end].strip()
                if chunk_slice:
                    chunks.append({
                        'chunk_index': chunk_index,
                        'section_title': section,
                        'page_number': page,
                        'content': chunk_slice,
                        'token_count': len(chunk_slice.split())
                    })
                    chunk_index += 1
                
                if end >= len(text):
                    break
                start = max(end - overlap, start + 1)

    return chunks
