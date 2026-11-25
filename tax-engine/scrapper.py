#!/usr/bin/env python3
"""Ingestor del corpus oficial RMF 2026 publicado por el SAT.

Descubre exclusivamente PDFs del árbol RMF 2026, los procesa uno a uno en
archivos temporales, conserva el texto UTF-8 y elimina cada PDF al terminar.
No realiza OCR.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import logging
import re
import sys
import tempfile
import time
import unicodedata
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


PAGE_URL = (
    "https://www.sat.gob.mx/minisitio/NormatividadRMFyRGCE/"
    "normatividad_rmf_rgce2026.html"
)

DEFAULT_OUTPUT = Path("data") / "rmf_2026"
LIVA_SOURCE_URL = "https://www.diputados.gob.mx/LeyesBiblio/pdf/LIVA.pdf"
LIVA_OUTPUT = Path("data") / "legal" / "liva"
RLIVA_SOURCE_URL = (
    "https://www.diputados.gob.mx/LeyesBiblio/regley/Reg_LIVA_250914.pdf"
)
RLIVA_OUTPUT = Path("data") / "legal" / "rliva"
LISR_SOURCE_URL = "https://www.diputados.gob.mx/LeyesBiblio/pdf/LISR.pdf"
LISR_OUTPUT = Path("data") / "legal" / "lisr"
RLISR_SOURCE_URL = (
    "https://www.diputados.gob.mx/LeyesBiblio/regley/Reg_LISR_060516.pdf"
)
RLISR_OUTPUT = Path("data") / "legal" / "rlisr"
CFF_SOURCE_URL = "https://www.diputados.gob.mx/LeyesBiblio/pdf/CFF.pdf"
CFF_OUTPUT = Path("data") / "legal" / "cff"
RCFF_SOURCE_URL = "https://www.diputados.gob.mx/LeyesBiblio/regley/Reg_CFF.pdf"
RCFF_OUTPUT = Path("data") / "legal" / "rcff"
LIEPS_SOURCE_URL = "https://www.diputados.gob.mx/LeyesBiblio/pdf/LIEPS.pdf"
LIEPS_OUTPUT = Path("data") / "legal" / "lieps"
RLIEPS_SOURCE_URL = "https://www.diputados.gob.mx/LeyesBiblio/regley/Reg_LIEPS.pdf"
RLIEPS_OUTPUT = Path("data") / "legal" / "rlieps"
FRONTERA_NORTE_OUTPUT = Path("data") / "legal" / "frontera_norte"
FRONTERA_NORTE_2018_SOURCE_URL = (
    "https://www.sat.gob.mx/minisitio/EstimulosFiscalesFronteraNorteSur/"
    "region_fronteriza_norte_iva/documentos/"
    "Decreto_de_estimulos_fiscales_region_fronteriza_norte.pdf"
)
FRONTERA_NORTE_2020_SOURCE_URL = (
    "https://www.sat.gob.mx/minisitio/EstimulosFiscalesFronteraNorteSur/"
    "region_fronteriza_norte_iva/documentos/"
    "Modificacion_al_Decreto_region_fronteriza_norte.pdf"
)
FRONTERA_NORTE_2022_SOURCE_URL = (
    "https://www.sat.gob.mx/minisitio/EstimulosFiscalesFronteraNorteSur/"
    "documentos/Decreto_Reforma_EstimulosFiscalesFronteraNorte.pdf"
)
FRONTERA_NORTE_2024_SOURCE_URL = (
    "https://www.sat.gob.mx/cs/Satellite?blobcol=urldata&blobkey=id&"
    "blobtable=MungoBlobs&blobwhere=1461176402660&ssbinary=true"
)
FRONTERA_NORTE_2025_SOURCE_URL = (
    "https://www.sat.gob.mx/minisitio/EstimulosFiscalesFronteraNorteSur/"
    "documentos/"
    "Decreto_modifica_diversos_estimulos_fiscales_region_fronteriza_norte_sur.pdf"
)
LIF_2026_SOURCE_URL = "https://www.diputados.gob.mx/LeyesBiblio/pdf/LIF_2026.pdf"
LIF_2026_OUTPUT = Path("data") / "legal" / "lif_2026"

USER_AGENT = (
    "Mozilla/5.0 (compatible; RMF2026ResearchBot/1.0; "
    "+local legal-tax research; respects SAT public documents)"
)

PDF_LINK_RE = re.compile(r"\.pdf(?:$|[?#])", re.IGNORECASE)
OFFICIAL_RMF_PATH_RE = re.compile(r"/documentos2026/rmf/", re.IGNORECASE)
ANNEX_NUMBER_RE = re.compile(r"\bAnexo\s+(\d+)\b", re.IGNORECASE)
PUBLICATION_DATE_RE = re.compile(
    r"(?:publicad[oa]\s+el\s+)?(\d{1,2})\s+de\s+([a-záéíóú]+)\s+de\s+(\d{4})",
    re.IGNORECASE,
)

MONTHS = {
    "enero": 1,
    "febrero": 2,
    "marzo": 3,
    "abril": 4,
    "mayo": 5,
    "junio": 6,
    "julio": 7,
    "agosto": 8,
    "septiembre": 9,
    "octubre": 10,
    "noviembre": 11,
    "diciembre": 12,
}

ORDINALS = {
    "primera": 1,
    "segunda": 2,
    "tercera": 3,
    "cuarta": 4,
    "quinta": 5,
    "sexta": 6,
    "septima": 7,
    "octava": 8,
    "novena": 9,
    "decima": 10,
    "decima primera": 11,
    "decima segunda": 12,
    "decima tercera": 13,
    "decima cuarta": 14,
    "decima quinta": 15,
    "decima sexta": 16,
}

MANIFEST_FIELDS = [
    "document_id",
    "title",
    "document_type",
    "fiscal_year",
    "source_year",
    "annex_number",
    "modification_number",
    "publication_date",
    "source_url",
    "fallback_url",
    "source_used",
    "filename_txt",
    "sha256_pdf",
    "pages",
    "characters_extracted",
    "extraction_status",
    "error",
]

OFFICIAL_FALLBACKS = {
    "anexo_19_base": "https://dof.gob.mx/2026/SHCP/SHCP_260126.pdf",
}


@dataclass
class RMFDocument:
    document_id: str
    title: str
    document_type: str
    fiscal_year: int
    source_year: int
    annex_number: int | None
    modification_number: int | None
    publication_date: str | None
    source_url: str
    fallback_url: str | None
    source_used: str | None
    filename_txt: str
    sha256_pdf: str | None = None
    pages: int | None = None
    characters_extracted: int | None = None
    extraction_status: str = "pending"
    error: str | None = None


def build_session() -> requests.Session:
    retry = Retry(
        total=5,
        connect=5,
        read=5,
        status=5,
        backoff_factor=1.0,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET", "HEAD"}),
        respect_retry_after_header=True,
    )

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": USER_AGENT,
            "Accept": (
                "text/html,application/xhtml+xml,application/pdf,"
                "application/xml;q=0.9,*/*;q=0.8"
            ),
            "Accept-Language": "es-MX,es;q=0.9,en;q=0.7",
        }
    )
    session.mount("https://", HTTPAdapter(max_retries=retry))
    session.mount("http://", HTTPAdapter(max_retries=retry))
    return session


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def ascii_slug(value: str, max_len: int = 140) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^A-Za-z0-9._-]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("._-")
    return (value[:max_len] or "documento").rstrip("._-")


def filename_from_url(url: str) -> str:
    path = unquote(urlparse(url).path)
    name = Path(path).name
    if not name.lower().endswith(".pdf"):
        name = f"{name}.pdf"
    return ascii_slug(name, max_len=180)


def infer_annex_number(text: str) -> int | None:
    match = ANNEX_NUMBER_RE.search(text)
    return int(match.group(1)) if match else None


def without_accents(value: str) -> str:
    return "".join(
        char
        for char in unicodedata.normalize("NFKD", value)
        if not unicodedata.combining(char)
    )


def infer_publication_date(context: str) -> str | None:
    match = PUBLICATION_DATE_RE.search(context)
    if not match:
        return None
    day, month_name, year = match.groups()
    month = MONTHS.get(without_accents(month_name.lower()))
    if month is None:
        return None
    return f"{int(year):04d}-{month:02d}-{int(day):02d}"


def infer_source_year(title: str, url: str) -> int:
    for value in (title, unquote(urlparse(url).path)):
        match = re.search(
            r"\bRMF(?:\s+para)?[\s_-]*(20\d{2})\b",
            value,
            re.IGNORECASE,
        )
        if match:
            return int(match.group(1))
    return 2026


def infer_modification_number(title: str, document_type: str) -> int | None:
    normalized = normalize_space(without_accents(title).lower())

    if document_type == "anticipated":
        match = re.search(
            r"version anticipada\s+(\d+)\s*[a-z.]*\s+rm",
            normalized,
        )
        return int(match.group(1)) if match else None

    if document_type == "compiled_rmf":
        match = re.search(r"^compilado\s+(\d+)\s*[a-z.]*\s+rm", normalized)
        return int(match.group(1)) if match else None

    match = re.search(
        r"\b(\d+)\s*[a-z.]*\s+(?:resolucion\s+de\s+)?modificacion",
        normalized,
    )
    if match:
        return int(match.group(1))

    for label, number in sorted(ORDINALS.items(), key=lambda item: -len(item[0])):
        if re.search(rf"\b{re.escape(label)}\s+modificacion\b", normalized):
            return number
    return None


def infer_anticipated_version(title: str) -> int | None:
    normalized = normalize_space(without_accents(title).lower())
    match = re.match(r"(\d+)\s*[a-z.]*\s+version anticipada", normalized)
    return int(match.group(1)) if match else None


def classify_document(title: str, url: str, annex_number: int | None) -> str | None:
    path = urlparse(url).path.lower()
    normalized = without_accents(title).lower()

    if "/documentos2026/rmf/anticipadas/" in path:
        return "anticipated"
    if "/documentos2026/rmf/compiladas/" in path:
        return "compiled_annex" if annex_number is not None else "compiled_rmf"
    if "/documentos2026/rmf/anexos/" in path:
        return "annex_modification" if "modific" in normalized else "annex_base"
    if "/documentos2026/rmf/rmf/" in path:
        return "rmf_modification" if "modific" in normalized else "rmf_base"
    return None


def build_document_id(
    document_type: str,
    annex_number: int | None,
    modification_number: int | None,
    anticipated_version: int | None,
) -> str:
    if document_type == "rmf_base":
        return "rmf_2026_base"
    if document_type == "rmf_modification":
        return f"rmf_2026_modificacion_{modification_number or 0:02d}"
    if document_type == "annex_base":
        return f"anexo_{annex_number or 0:02d}_base"
    if document_type == "annex_modification":
        return (
            f"anexo_{annex_number or 0:02d}_modificacion_"
            f"{modification_number or 0:02d}"
        )
    if document_type == "anticipated":
        return (
            f"rmf_2026_anticipada_modificacion_{modification_number or 0:02d}_"
            f"version_{anticipated_version or 0:02d}"
        )
    if document_type == "compiled_rmf":
        return f"compilado_rmf_modificacion_{modification_number or 0:02d}"
    if document_type == "compiled_annex":
        return (
            f"compilado_anexo_{annex_number or 0:02d}_modificacion_"
            f"{modification_number or 0:02d}"
        )
    raise ValueError(f"Tipo documental no soportado: {document_type}")


def fetch_html(session: requests.Session, url: str, timeout: int) -> str:
    logging.info("Leyendo índice SAT: %s", url)
    response = session.get(url, timeout=timeout)
    response.raise_for_status()

    # El micrositio SAT contiene texto UTF-8, pero la respuesta HTTP puede
    # provocar que requests infiera una codificación incorrecta.
    try:
        return response.content.decode("utf-8-sig")
    except UnicodeDecodeError:
        response.encoding = response.apparent_encoding
        return response.text


def documents_from_html(html: str, base_url: str) -> list[RMFDocument]:
    soup = BeautifulSoup(html, "html.parser")
    documents: list[RMFDocument] = []
    seen_urls: set[str] = set()

    for anchor in soup.find_all("a", href=True):
        href = normalize_space(anchor.get("href", ""))
        if not href:
            continue

        absolute_url = urljoin(base_url, href)

        if not PDF_LINK_RE.search(absolute_url):
            continue
        if not OFFICIAL_RMF_PATH_RE.search(urlparse(absolute_url).path):
            continue
        if absolute_url in seen_urls:
            continue

        title = normalize_space(anchor.get_text(" ", strip=True))
        if not title:
            title = filename_from_url(absolute_url)

        context = normalize_space(anchor.parent.get_text(" ", strip=True))
        annex_number = infer_annex_number(title) or infer_annex_number(absolute_url)
        document_type = classify_document(title, absolute_url, annex_number)
        if document_type is None:
            continue
        modification_number = infer_modification_number(title, document_type)
        document_id = build_document_id(
            document_type,
            annex_number,
            modification_number,
            infer_anticipated_version(title),
        )
        documents.append(
            RMFDocument(
                document_id=document_id,
                title=title,
                document_type=document_type,
                fiscal_year=2026,
                source_year=infer_source_year(title, absolute_url),
                annex_number=annex_number,
                modification_number=modification_number,
                publication_date=infer_publication_date(context),
                source_url=absolute_url,
                fallback_url=OFFICIAL_FALLBACKS.get(document_id),
                source_used=None,
                filename_txt=f"{document_id}.txt",
            )
        )
        seen_urls.add(absolute_url)

    return documents


def intermediate_page_urls(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    result: list[str] = []
    for anchor in soup.find_all("a", href=True):
        href = normalize_space(anchor.get("href", ""))
        if not href or href.startswith("#"):
            continue
        absolute_url = urljoin(base_url, href).split("#", 1)[0]
        parsed = urlparse(absolute_url)
        path = parsed.path.lower()
        if absolute_url == base_url or PDF_LINK_RE.search(absolute_url):
            continue
        if parsed.netloc != urlparse(PAGE_URL).netloc:
            continue
        if "2026" not in path or "rmf" not in path or "rgce" in path:
            continue
        if path.endswith((".html", ".htm")) and absolute_url not in result:
            result.append(absolute_url)
    return result


def discover_rmf_documents(
    session: requests.Session,
    html: str,
    base_url: str,
    timeout: int,
) -> list[RMFDocument]:
    documents = documents_from_html(html, base_url)
    seen_urls = {doc.source_url for doc in documents}

    for page_url in intermediate_page_urls(html, base_url):
        page_html = fetch_html(session, page_url, timeout)
        for doc in documents_from_html(page_html, page_url):
            if doc.source_url not in seen_urls:
                documents.append(doc)
                seen_urls.add(doc.source_url)

    type_order = {
        "rmf_base": 0,
        "rmf_modification": 1,
        "annex_base": 2,
        "annex_modification": 3,
        "anticipated": 4,
        "compiled_rmf": 5,
        "compiled_annex": 6,
    }
    documents.sort(
        key=lambda doc: (
            type_order[doc.document_type],
            doc.annex_number or 0,
            doc.modification_number or 0,
            doc.publication_date or "",
            doc.title.lower(),
        )
    )
    return documents


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download_pdf_temporarily(
    session: requests.Session,
    doc: RMFDocument,
    temp_dir: Path,
    timeout: int,
) -> tuple[Path, str]:
    digest = hashlib.sha256()
    temp_path: Path | None = None
    download_url = doc.fallback_url or doc.source_url
    source_used = doc.source_used or ("DOF" if doc.fallback_url else "SAT")

    try:
        temp_dir.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            prefix="rmf_2026_",
            suffix=".pdf",
            dir=temp_dir,
            delete=False,
        ) as temp_file:
            temp_path = Path(temp_file.name)
            logging.info("Descargando temporalmente desde %s: %s", source_used, download_url)
            with session.get(download_url, stream=True, timeout=timeout) as response:
                response.raise_for_status()
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        temp_file.write(chunk)
                        digest.update(chunk)

        if temp_path.stat().st_size == 0:
            raise RuntimeError("El SAT devolvió un archivo vacío.")
        with temp_path.open("rb") as fh:
            if fh.read(5) != b"%PDF-":
                raise RuntimeError("El archivo temporal no tiene cabecera %PDF-.")
        doc.source_used = source_used
        return temp_path, digest.hexdigest()
    except Exception:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)
        raise


def extract_pdf_text(pdf_path: Path, txt_path: Path) -> tuple[int, int, str, str | None]:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError(
            "Falta pypdf. Instala dependencias con: "
            "python -m pip install requests beautifulsoup4 pypdf"
        ) from exc
    reader = PdfReader(str(pdf_path))
    pages = len(reader.pages)
    characters = 0
    useful_characters = 0
    page_errors: list[str] = []
    temp_txt = txt_path.with_suffix(txt_path.suffix + ".part")

    txt_path.parent.mkdir(parents=True, exist_ok=True)
    with temp_txt.open("w", encoding="utf-8") as out:
        for index, page in enumerate(reader.pages, start=1):
            out.write(f"===== PAGE {index} =====\n\n")
            try:
                text = page.extract_text() or ""
            except Exception as exc:
                page_errors.append(f"Página {index}: {exc}")
                text = ""
            text = re.sub(r"\b(Artículo\s+\d+)\s+-([A-Z])", r"\1-\2", text)
            characters += len(text)
            useful_characters += len(re.sub(r"\s+", "", text))
            out.write(text)
            out.write("\n\n")

    temp_txt.replace(txt_path)
    if useful_characters < max(50, pages * 10):
        status = "needs_ocr"
    elif page_errors:
        status = "partial"
    else:
        status = "ok"
    error = "; ".join(page_errors) if page_errors else None
    return pages, characters, status, error


def write_manifest(documents: list[RMFDocument], output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "manifest.json"
    csv_path = output_dir / "manifest.csv"
    json_temp = json_path.with_suffix(".json.part")
    csv_temp = csv_path.with_suffix(".csv.part")

    json_temp.write_text(
        json.dumps(
            {
                "source_page": PAGE_URL,
                "document_count": len(documents),
                "documents": [asdict(doc) for doc in documents],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    json_temp.replace(json_path)

    with csv_temp.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=MANIFEST_FIELDS)
        writer.writeheader()
        for doc in documents:
            writer.writerow(asdict(doc))
    csv_temp.replace(csv_path)
    return json_path, csv_path


def load_previous_manifest(output_dir: Path) -> dict[str, dict[str, object]]:
    manifest_path = output_dir / "manifest.json"
    if not manifest_path.exists():
        return {}
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        return {
            item["document_id"]: item
            for item in payload.get("documents", [])
            if isinstance(item, dict) and item.get("document_id")
        }
    except (OSError, json.JSONDecodeError, TypeError) as exc:
        logging.warning("No se pudo reutilizar el manifest anterior: %s", exc)
        return {}


def resume_document(
    doc: RMFDocument,
    previous: dict[str, object] | None,
    text_dir: Path,
) -> bool:
    if previous is None:
        return False
    txt_path = text_dir / doc.filename_txt
    if not txt_path.is_file() or txt_path.stat().st_size == 0:
        return False
    if previous.get("source_url") != doc.source_url:
        return False
    if previous.get("filename_txt") != doc.filename_txt:
        return False
    if previous.get("extraction_status") not in {"ok", "partial", "needs_ocr"}:
        return False

    for field in (
        "sha256_pdf",
        "pages",
        "characters_extracted",
        "extraction_status",
        "error",
    ):
        setattr(doc, field, previous.get(field))
    return True


def process_document(
    session: requests.Session,
    doc: RMFDocument,
    text_dir: Path,
    temp_dir: Path,
    timeout: int,
    delay: float,
) -> None:
    temp_pdf: Path | None = None
    try:
        temp_pdf, doc.sha256_pdf = download_pdf_temporarily(
            session,
            doc,
            temp_dir,
            timeout,
        )
        txt_path = text_dir / doc.filename_txt
        (
            doc.pages,
            doc.characters_extracted,
            doc.extraction_status,
            doc.error,
        ) = extract_pdf_text(temp_pdf, txt_path)
    except Exception as exc:
        doc.extraction_status = "error"
        doc.error = str(exc)
        logging.exception("No se pudo procesar %s", doc.document_id)
    finally:
        if temp_pdf is not None:
            temp_pdf.unlink(missing_ok=True)
        if delay > 0:
            time.sleep(delay)


def ingest_liva(session: requests.Session, timeout: int) -> tuple[RMFDocument, Path]:
    output_dir = LIVA_OUTPUT
    temp_dir = output_dir / ".tmp"
    doc = RMFDocument(
        document_id="liva_vigente",
        title="Ley del Impuesto al Valor Agregado",
        document_type="law",
        fiscal_year=2021,
        source_year=1978,
        annex_number=None,
        modification_number=None,
        publication_date="2021-11-12",
        source_url=LIVA_SOURCE_URL,
        fallback_url=None,
        source_used="Cámara de Diputados",
        filename_txt="liva_vigente.txt",
    )
    process_document(
        session=session,
        doc=doc,
        text_dir=output_dir,
        temp_dir=temp_dir,
        timeout=timeout,
        delay=0,
    )

    manifest = {
        "document_id": doc.document_id,
        "title": doc.title,
        "document_type": doc.document_type,
        "source": "Cámara de Diputados",
        "source_url": doc.source_url,
        "original_publication": "1978-12-29",
        "last_reform": "2021-11-12",
        "status": "vigente",
        "sha256_pdf": doc.sha256_pdf,
        "pages": doc.pages,
        "characters_extracted": doc.characters_extracted,
        "extraction_status": doc.extraction_status,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "manifest.json"
    manifest_temp = manifest_path.with_suffix(".json.part")
    manifest_temp.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    manifest_temp.replace(manifest_path)
    return doc, manifest_path


def ingest_rliva(session: requests.Session, timeout: int) -> tuple[RMFDocument, Path]:
    output_dir = RLIVA_OUTPUT
    temp_dir = output_dir / ".tmp"
    doc = RMFDocument(
        document_id="rliva_vigente",
        title="Reglamento de la Ley del Impuesto al Valor Agregado",
        document_type="regulation",
        fiscal_year=2014,
        source_year=2006,
        annex_number=None,
        modification_number=None,
        publication_date="2014-09-25",
        source_url=RLIVA_SOURCE_URL,
        fallback_url=None,
        source_used="Cámara de Diputados",
        filename_txt="rliva_vigente.txt",
    )
    process_document(
        session=session,
        doc=doc,
        text_dir=output_dir,
        temp_dir=temp_dir,
        timeout=timeout,
        delay=0,
    )

    manifest = {
        "document_id": doc.document_id,
        "title": doc.title,
        "document_type": doc.document_type,
        "consolidated_source": "Cámara de Diputados",
        "consolidated_source_url": doc.source_url,
        "original_publication_date": "2006-12-04",
        "last_reform_date": "2014-09-25",
        "official_publication_source": "DOF",
        "status": "vigente",
        "sha256_pdf": doc.sha256_pdf,
        "pages": doc.pages,
        "characters_extracted": doc.characters_extracted,
        "extraction_status": doc.extraction_status,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "manifest.json"
    manifest_temp = manifest_path.with_suffix(".json.part")
    manifest_temp.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    manifest_temp.replace(manifest_path)
    return doc, manifest_path


def ingest_lisr(session: requests.Session, timeout: int) -> tuple[RMFDocument, Path]:
    output_dir = LISR_OUTPUT
    temp_dir = output_dir / ".tmp"
    doc = RMFDocument(
        document_id="lisr_vigente",
        title="Ley del Impuesto sobre la Renta",
        document_type="law",
        fiscal_year=2024,
        source_year=2013,
        annex_number=None,
        modification_number=None,
        publication_date="2024-04-01",
        source_url=LISR_SOURCE_URL,
        fallback_url=None,
        source_used="Cámara de Diputados",
        filename_txt="lisr_vigente.txt",
    )
    process_document(
        session=session,
        doc=doc,
        text_dir=output_dir,
        temp_dir=temp_dir,
        timeout=timeout,
        delay=0,
    )

    manifest = {
        "document_id": doc.document_id,
        "title": doc.title,
        "document_type": doc.document_type,
        "consolidated_source": "Cámara de Diputados",
        "consolidated_source_url": doc.source_url,
        "original_publication_date": "2013-12-11",
        "last_reform_date": "2024-04-01",
        "official_publication_source": "DOF",
        "status": "vigente",
        "sha256_pdf": doc.sha256_pdf,
        "pages": doc.pages,
        "characters_extracted": doc.characters_extracted,
        "extraction_status": doc.extraction_status,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "manifest.json"
    manifest_temp = manifest_path.with_suffix(".json.part")
    manifest_temp.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    manifest_temp.replace(manifest_path)
    return doc, manifest_path


def ingest_rlisr(session: requests.Session, timeout: int) -> tuple[RMFDocument, Path]:
    output_dir = RLISR_OUTPUT
    temp_dir = output_dir / ".tmp"
    doc = RMFDocument(
        document_id="rlisr_vigente",
        title="Reglamento de la Ley del Impuesto sobre la Renta",
        document_type="regulation",
        fiscal_year=2016,
        source_year=2015,
        annex_number=None,
        modification_number=None,
        publication_date="2016-05-06",
        source_url=RLISR_SOURCE_URL,
        fallback_url=None,
        source_used="Cámara de Diputados",
        filename_txt="rlisr_vigente.txt",
    )
    process_document(
        session=session,
        doc=doc,
        text_dir=output_dir,
        temp_dir=temp_dir,
        timeout=timeout,
        delay=0,
    )

    manifest = {
        "document_id": doc.document_id,
        "title": doc.title,
        "document_type": doc.document_type,
        "consolidated_source": "Cámara de Diputados",
        "consolidated_source_url": doc.source_url,
        "original_publication_date": "2015-10-08",
        "last_reform_date": "2016-05-06",
        "official_publication_source": "DOF",
        "status": "vigente",
        "sha256_pdf": doc.sha256_pdf,
        "pages": doc.pages,
        "characters_extracted": doc.characters_extracted,
        "extraction_status": doc.extraction_status,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "manifest.json"
    manifest_temp = manifest_path.with_suffix(".json.part")
    manifest_temp.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    manifest_temp.replace(manifest_path)
    return doc, manifest_path


def ingest_cff(session: requests.Session, timeout: int) -> tuple[RMFDocument, Path]:
    output_dir = CFF_OUTPUT
    temp_dir = output_dir / ".tmp"
    doc = RMFDocument(
        document_id="cff_vigente",
        title="Código Fiscal de la Federación",
        document_type="code",
        fiscal_year=2026,
        source_year=1981,
        annex_number=None,
        modification_number=None,
        publication_date=None,
        source_url=CFF_SOURCE_URL,
        fallback_url=None,
        source_used="Cámara de Diputados",
        filename_txt="cff_vigente.txt",
    )
    process_document(
        session=session,
        doc=doc,
        text_dir=output_dir,
        temp_dir=temp_dir,
        timeout=timeout,
        delay=0,
    )

    original_publication_date = None
    last_reform_date = None
    txt_path = output_dir / doc.filename_txt
    if doc.extraction_status != "error" and txt_path.is_file():
        header = txt_path.read_text(encoding="utf-8")[:15000]
        original_match = re.search(
            r"(?:Nuevo C[oó]digo\s+)?Publicado en el Diario Oficial de la "
            r"Federaci[oó]n el (\d{1,2}) de ([a-záéíóú]+) de (\d{4})",
            header,
            re.IGNORECASE,
        )
        reform_match = re.search(
            r"[ÚU]ltima Reforma DOF (\d{2})-(\d{2})-(\d{4})",
            header,
            re.IGNORECASE,
        )
        if original_match:
            day, month_name, year = original_match.groups()
            month = MONTHS.get(without_accents(month_name.lower()))
            if month is not None:
                original_publication_date = (
                    f"{int(year):04d}-{month:02d}-{int(day):02d}"
                )
        if reform_match:
            day, month, year = reform_match.groups()
            last_reform_date = f"{year}-{month}-{day}"
        if original_publication_date is None or last_reform_date is None:
            doc.extraction_status = "partial"
            doc.error = "No se pudieron validar ambas fechas en el encabezado del CFF."

    manifest = {
        "document_id": doc.document_id,
        "title": doc.title,
        "document_type": doc.document_type,
        "consolidated_source": "Cámara de Diputados",
        "consolidated_source_url": doc.source_url,
        "original_publication_date": original_publication_date,
        "last_reform_date": last_reform_date,
        "official_publication_source": "DOF",
        "status": "vigente",
        "sha256_pdf": doc.sha256_pdf,
        "pages": doc.pages,
        "characters_extracted": doc.characters_extracted,
        "extraction_status": doc.extraction_status,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "manifest.json"
    manifest_temp = manifest_path.with_suffix(".json.part")
    manifest_temp.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    manifest_temp.replace(manifest_path)
    return doc, manifest_path


def ingest_rcff(session: requests.Session, timeout: int) -> tuple[RMFDocument, Path]:
    output_dir = RCFF_OUTPUT
    temp_dir = output_dir / ".tmp"
    doc = RMFDocument(
        document_id="rcff_vigente",
        title="Reglamento del Código Fiscal de la Federación",
        document_type="regulation",
        fiscal_year=2014,
        source_year=2014,
        annex_number=None,
        modification_number=None,
        publication_date="2014-04-02",
        source_url=RCFF_SOURCE_URL,
        fallback_url=None,
        source_used="Cámara de Diputados",
        filename_txt="rcff_vigente.txt",
    )
    process_document(
        session=session,
        doc=doc,
        text_dir=output_dir,
        temp_dir=temp_dir,
        timeout=timeout,
        delay=0,
    )

    last_reform_date = None
    txt_path = output_dir / doc.filename_txt
    if doc.extraction_status != "error" and txt_path.is_file():
        header = txt_path.read_text(encoding="utf-8")[:15000]
        reform_match = re.search(
            r"[ÚU]ltima (?:Reforma|reforma publicada) DOF "
            r"(\d{2})-(\d{2})-(\d{4})",
            header,
            re.IGNORECASE,
        )
        if reform_match:
            day, month, year = reform_match.groups()
            last_reform_date = f"{year}-{month}-{day}"

    manifest = {
        "document_id": doc.document_id,
        "title": doc.title,
        "document_type": doc.document_type,
        "consolidated_source": "Cámara de Diputados",
        "consolidated_source_url": doc.source_url,
        "original_publication_date": "2014-04-02",
        "last_reform_date": last_reform_date,
        "official_publication_source": "DOF",
        "status": "vigente",
        "sha256_pdf": doc.sha256_pdf,
        "pages": doc.pages,
        "characters_extracted": doc.characters_extracted,
        "extraction_status": doc.extraction_status,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "manifest.json"
    manifest_temp = manifest_path.with_suffix(".json.part")
    manifest_temp.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    manifest_temp.replace(manifest_path)
    return doc, manifest_path


def ingest_lieps(session: requests.Session, timeout: int) -> tuple[RMFDocument, Path]:
    output_dir = LIEPS_OUTPUT
    temp_dir = output_dir / ".tmp"
    doc = RMFDocument(
        document_id="lieps_vigente",
        title="Ley del Impuesto Especial sobre Producción y Servicios",
        document_type="law",
        fiscal_year=2026,
        source_year=1980,
        annex_number=None,
        modification_number=None,
        publication_date=None,
        source_url=LIEPS_SOURCE_URL,
        fallback_url=None,
        source_used="Cámara de Diputados",
        filename_txt="lieps_vigente.txt",
    )
    process_document(
        session=session,
        doc=doc,
        text_dir=output_dir,
        temp_dir=temp_dir,
        timeout=timeout,
        delay=0,
    )

    original_publication_date = None
    last_reform_date = None
    txt_path = output_dir / doc.filename_txt
    if doc.extraction_status != "error" and txt_path.is_file():
        header = txt_path.read_text(encoding="utf-8")[:15000]
        original_match = re.search(
            r"(?:Nueva Ley\s+)?[Pp]ublicada en el Diario Oficial de la "
            r"Federaci[oó]n el (\d{1,2}) de ([a-záéíóú]+) de (\d{4})",
            header,
            re.IGNORECASE,
        )
        reform_match = re.search(
            r"[ÚU]ltima (?:Reforma|reforma publicada) DOF "
            r"(\d{2})-(\d{2})-(\d{4})",
            header,
            re.IGNORECASE,
        )
        if original_match:
            day, month_name, year = original_match.groups()
            month = MONTHS.get(without_accents(month_name.lower()))
            if month is not None:
                original_publication_date = (
                    f"{int(year):04d}-{month:02d}-{int(day):02d}"
                )
        if reform_match:
            day, month, year = reform_match.groups()
            last_reform_date = f"{year}-{month}-{day}"
        if original_publication_date is None or last_reform_date is None:
            doc.extraction_status = "partial"
            doc.error = "No se pudieron validar ambas fechas en el encabezado de la LIEPS."

    manifest = {
        "document_id": doc.document_id,
        "title": doc.title,
        "document_type": doc.document_type,
        "consolidated_source": "Cámara de Diputados",
        "consolidated_source_url": doc.source_url,
        "original_publication_date": original_publication_date,
        "last_reform_date": last_reform_date,
        "official_publication_source": "DOF",
        "status": "vigente",
        "sha256_pdf": doc.sha256_pdf,
        "pages": doc.pages,
        "characters_extracted": doc.characters_extracted,
        "extraction_status": doc.extraction_status,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "manifest.json"
    manifest_temp = manifest_path.with_suffix(".json.part")
    manifest_temp.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    manifest_temp.replace(manifest_path)
    return doc, manifest_path


def ingest_rlieps(session: requests.Session, timeout: int) -> tuple[RMFDocument, Path]:
    output_dir = RLIEPS_OUTPUT
    temp_dir = output_dir / ".tmp"
    doc = RMFDocument(
        document_id="rlieps_vigente",
        title="Reglamento de la Ley del Impuesto Especial sobre Producción y Servicios",
        document_type="regulation",
        fiscal_year=2026,
        source_year=2006,
        annex_number=None,
        modification_number=None,
        publication_date=None,
        source_url=RLIEPS_SOURCE_URL,
        fallback_url=None,
        source_used="Cámara de Diputados",
        filename_txt="rlieps_vigente.txt",
    )
    process_document(
        session=session,
        doc=doc,
        text_dir=output_dir,
        temp_dir=temp_dir,
        timeout=timeout,
        delay=0,
    )

    original_publication_date = None
    last_reform_date = None
    txt_path = output_dir / doc.filename_txt
    if doc.extraction_status != "error" and txt_path.is_file():
        header = txt_path.read_text(encoding="utf-8")[:15000]
        original_match = re.search(
            r"(?:Nuevo Reglamento\s+)?[Pp]ublicado en el Diario Oficial de la "
            r"Federaci[oó]n el (\d{1,2}) de ([a-záéíóú]+) de (\d{4})",
            header,
            re.IGNORECASE,
        )
        reform_match = re.search(
            r"[ÚU]ltima (?:Reforma|reforma publicada) DOF "
            r"(\d{2})-(\d{2})-(\d{4})",
            header,
            re.IGNORECASE,
        )
        if original_match:
            day, month_name, year = original_match.groups()
            month = MONTHS.get(without_accents(month_name.lower()))
            if month is not None:
                original_publication_date = (
                    f"{int(year):04d}-{month:02d}-{int(day):02d}"
                )
        if reform_match:
            day, month, year = reform_match.groups()
            last_reform_date = f"{year}-{month}-{day}"
        if original_publication_date is None:
            doc.extraction_status = "partial"
            doc.error = "No se pudo validar la fecha original en el encabezado del RLIEPS."

    manifest = {
        "document_id": doc.document_id,
        "title": doc.title,
        "document_type": doc.document_type,
        "consolidated_source": "Cámara de Diputados",
        "consolidated_source_url": doc.source_url,
        "original_publication_date": original_publication_date,
        "last_reform_date": last_reform_date,
        "official_publication_source": "DOF",
        "status": "vigente",
        "sha256_pdf": doc.sha256_pdf,
        "pages": doc.pages,
        "characters_extracted": doc.characters_extracted,
        "extraction_status": doc.extraction_status,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "manifest.json"
    manifest_temp = manifest_path.with_suffix(".json.part")
    manifest_temp.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    manifest_temp.replace(manifest_path)
    return doc, manifest_path


def ingest_frontera_norte(
    session: requests.Session,
    timeout: int,
) -> tuple[list[RMFDocument], Path]:
    output_dir = FRONTERA_NORTE_OUTPUT
    temp_dir = output_dir / ".tmp"
    specifications = (
        (
            "decreto_frontera_norte_2018",
            "Decreto de estímulos fiscales región fronteriza norte",
            "2018-12-31",
            FRONTERA_NORTE_2018_SOURCE_URL,
        ),
        (
            "modificacion_frontera_norte_2020",
            "Decreto por el que se modifica el diverso de estímulos fiscales región fronteriza norte",
            "2020-12-30",
            FRONTERA_NORTE_2020_SOURCE_URL,
        ),
        (
            "reforma_frontera_norte_2022",
            "Decreto por el que se reforma el diverso de estímulos fiscales "
            "región fronteriza norte, publicado en el Diario Oficial de la "
            "Federación el 31 de diciembre de 2018, y su posterior modificación",
            "2022-10-21",
            FRONTERA_NORTE_2022_SOURCE_URL,
        ),
        (
            "modificacion_frontera_norte_2024",
            "Decreto por el que se modifica el diverso por el que se otorgan "
            "estímulos fiscales a sectores clave de la industria exportadora "
            "consistentes en la deducción inmediata de la inversión en bienes "
            "nuevos de activo fijo y la deducción adicional de gastos de "
            "capacitación, el Decreto de estímulos fiscales región fronteriza "
            "norte, el Decreto de estímulos fiscales región fronteriza sur, el "
            "Decreto por el que se establecen estímulos fiscales en materia del "
            "impuesto especial sobre producción y servicios aplicables a los "
            "combustibles que se indican, el Decreto por el que se establecen "
            "estímulos fiscales complementarios a los combustibles automotrices "
            "y el Decreto por el que se establecen estímulos fiscales a la "
            "enajenación de los combustibles que se mencionan en la frontera sur "
            "de los Estados Unidos Mexicanos",
            "2024-12-24",
            FRONTERA_NORTE_2024_SOURCE_URL,
        ),
        (
            "modificacion_frontera_norte_2025",
            "Decreto por el que se modifica los diversos de estímulos fiscales "
            "región fronteriza norte, el Decreto de estímulos fiscales región "
            "fronteriza sur, el Decreto por el que se establecen estímulos "
            "fiscales en materia del impuesto especial sobre producción y "
            "servicios aplicables a los combustibles que se indican, el Decreto "
            "por el que se establecen estímulos fiscales complementarios a los "
            "combustibles automotrices y el Decreto por el que se establecen "
            "estímulos fiscales a la enajenación de los combustibles que se "
            "mencionan en la frontera sur de los Estados Unidos Mexicanos",
            "2025-12-31",
            FRONTERA_NORTE_2025_SOURCE_URL,
        ),
    )
    documents: list[RMFDocument] = []
    manifest_documents: list[dict[str, object]] = []

    for document_id, title, publication_date, source_url in specifications:
        year = int(publication_date[:4])
        doc = RMFDocument(
            document_id=document_id,
            title=title,
            document_type="decree",
            fiscal_year=year,
            source_year=year,
            annex_number=None,
            modification_number=None,
            publication_date=publication_date,
            source_url=source_url,
            fallback_url=None,
            source_used="SAT",
            filename_txt=f"{document_id}.txt",
        )
        process_document(
            session=session,
            doc=doc,
            text_dir=output_dir,
            temp_dir=temp_dir,
            timeout=timeout,
            delay=0.5,
        )
        documents.append(doc)
        manifest_documents.append(
            {
                "document_id": doc.document_id,
                "title": doc.title,
                "document_type": doc.document_type,
                "publication_date": doc.publication_date,
                "source": "SAT",
                "source_url": doc.source_url,
                "official_publication_source": "DOF",
                "sha256_pdf": doc.sha256_pdf,
                "pages": doc.pages,
                "characters_extracted": doc.characters_extracted,
                "extraction_status": doc.extraction_status,
            }
        )

    manifest = {
        "collection_id": "frontera_norte",
        "title": "Decreto de estímulos fiscales región fronteriza norte",
        "status": "vigente",
        "original_publication_date": "2018-12-31",
        "latest_modification_date": "2025-12-31",
        "valid_through": "2026-12-31",
        "documents": manifest_documents,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "manifest.json"
    manifest_temp = manifest_path.with_suffix(".json.part")
    manifest_temp.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    manifest_temp.replace(manifest_path)
    return documents, manifest_path


def ingest_lif_2026(session: requests.Session, timeout: int) -> tuple[RMFDocument, Path]:
    output_dir = LIF_2026_OUTPUT
    temp_dir = output_dir / ".tmp"
    doc = RMFDocument(
        document_id="lif_2026",
        title="Ley de Ingresos de la Federación para el Ejercicio Fiscal de 2026",
        document_type="law",
        fiscal_year=2026,
        source_year=2025,
        annex_number=None,
        modification_number=None,
        publication_date=None,
        source_url=LIF_2026_SOURCE_URL,
        fallback_url=None,
        source_used="Cámara de Diputados",
        filename_txt="lif_2026.txt",
    )
    process_document(
        session=session,
        doc=doc,
        text_dir=output_dir,
        temp_dir=temp_dir,
        timeout=timeout,
        delay=0,
    )

    publication_date = None
    effective_from = None
    txt_path = output_dir / doc.filename_txt
    if doc.extraction_status != "error" and txt_path.is_file():
        text = txt_path.read_text(encoding="utf-8")
        normalized_text = normalize_space(text)
        publication_match = re.search(
            r"[Pp]ublicada en el Diario Oficial de la Federaci[oó]n el "
            r"(\d{1,2}) de ([a-záéíóú]+) de (\d{4})",
            normalized_text,
            re.IGNORECASE,
        )
        effective_match = re.search(
            r"[Ll]a presente Ley entrar[aá] en vigor el "
            r"(\d{1,2}) de ([a-záéíóú]+) de (\d{4})",
            normalized_text,
            re.IGNORECASE,
        )
        if publication_match:
            day, month_name, year = publication_match.groups()
            month = MONTHS.get(without_accents(month_name.lower()))
            if month is not None:
                publication_date = f"{int(year):04d}-{month:02d}-{int(day):02d}"
        if effective_match:
            day, month_name, year = effective_match.groups()
            month = MONTHS.get(without_accents(month_name.lower()))
            if month is not None:
                effective_from = f"{int(year):04d}-{month:02d}-{int(day):02d}"
        if publication_date is None or effective_from is None:
            doc.extraction_status = "partial"
            doc.error = "No se pudieron validar las fechas de la LIF 2026."

    manifest = {
        "document_id": doc.document_id,
        "title": doc.title,
        "document_type": doc.document_type,
        "consolidated_source": "Cámara de Diputados",
        "consolidated_source_url": doc.source_url,
        "publication_date": publication_date,
        "effective_from": effective_from,
        "official_publication_source": "DOF",
        "status": "vigente",
        "sha256_pdf": doc.sha256_pdf,
        "pages": doc.pages,
        "characters_extracted": doc.characters_extracted,
        "extraction_status": doc.extraction_status,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "manifest.json"
    manifest_temp = manifest_path.with_suffix(".json.part")
    manifest_temp.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    manifest_temp.replace(manifest_path)
    return doc, manifest_path


def print_documents(documents: list[RMFDocument]) -> None:
    if not documents:
        print("No se encontraron documentos RMF 2026.")
        return

    for doc in documents:
        print(
            f"{doc.document_type:20} | {doc.document_id:52} | {doc.title}\n"
            f"{'':20} | {'':52} | {doc.source_url}"
        )

    counts = {
        document_type: sum(
            1 for doc in documents if doc.document_type == document_type
        )
        for document_type in (
            "rmf_base",
            "rmf_modification",
            "annex_base",
            "annex_modification",
            "anticipated",
            "compiled_rmf",
            "compiled_annex",
        )
    }
    print(f"\nDocumentos : {len(documents)}")
    for document_type, count in counts.items():
        print(f"{document_type:20}: {count}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Descubre el corpus RMF 2026 y lo convierte a texto UTF-8."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Directorio de salida (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Descubre y lista todo el corpus RMF 2026 sin descargar PDFs.",
    )
    parser.add_argument(
        "--extract-all",
        action="store_true",
        help="Descarga temporalmente y extrae a TXT todo el corpus descubierto.",
    )
    parser.add_argument(
        "--extract-liva",
        action="store_true",
        help="Descarga temporalmente y extrae la LIVA vigente a TXT.",
    )
    parser.add_argument(
        "--extract-rliva",
        action="store_true",
        help="Descarga temporalmente y extrae el RLIVA vigente a TXT.",
    )
    parser.add_argument(
        "--extract-lisr",
        action="store_true",
        help="Descarga temporalmente y extrae la LISR vigente a TXT.",
    )
    parser.add_argument(
        "--extract-rlisr",
        action="store_true",
        help="Descarga temporalmente y extrae el RLISR vigente a TXT.",
    )
    parser.add_argument(
        "--extract-cff",
        action="store_true",
        help="Descarga temporalmente y extrae el CFF vigente a TXT.",
    )
    parser.add_argument(
        "--extract-rcff",
        action="store_true",
        help="Descarga temporalmente y extrae el RCFF vigente a TXT.",
    )
    parser.add_argument(
        "--extract-lieps",
        action="store_true",
        help="Descarga temporalmente y extrae la LIEPS vigente a TXT.",
    )
    parser.add_argument(
        "--extract-rlieps",
        action="store_true",
        help="Descarga temporalmente y extrae el RLIEPS vigente a TXT.",
    )
    parser.add_argument(
        "--extract-frontera-norte",
        action="store_true",
        help="Descarga temporalmente y extrae la cadena normativa de frontera norte.",
    )
    parser.add_argument(
        "--extract-lif-2026",
        action="store_true",
        help="Descarga temporalmente y extrae la LIF 2026 a TXT.",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Omite TXT completos que coincidan con el manifest existente.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=90,
        help="Timeout HTTP en segundos (default: 90).",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.5,
        help="Pausa entre descargas para no golpear el servidor (default: 0.5s).",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Logging detallado.",
    )
    args = parser.parse_args()
    if args.resume and not args.extract_all:
        parser.error("--resume requiere --extract-all")
    legal_extractors = sum(
        (
            args.extract_liva,
            args.extract_rliva,
            args.extract_lisr,
            args.extract_rlisr,
            args.extract_cff,
            args.extract_rcff,
            args.extract_lieps,
            args.extract_rlieps,
            args.extract_frontera_norte,
            args.extract_lif_2026,
        )
    )
    if legal_extractors and (args.list or args.extract_all or args.resume):
        parser.error(
            "Los extractores legales no se combinan con opciones del corpus RMF"
        )
    if legal_extractors > 1:
        parser.error("Los extractores legales son mutuamente excluyentes")
    return args


def main() -> int:
    args = parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    session = build_session()

    try:
        if args.extract_liva:
            doc, manifest_path = ingest_liva(session, args.timeout)
            print(f"Manifest JSON: {manifest_path}")
            print(f"Documento    : {doc.document_id}")
            print(f"Estado       : {doc.extraction_status}")
            return 0 if doc.extraction_status != "error" else 1

        if args.extract_rliva:
            doc, manifest_path = ingest_rliva(session, args.timeout)
            print(f"Manifest JSON: {manifest_path}")
            print(f"Documento    : {doc.document_id}")
            print(f"Estado       : {doc.extraction_status}")
            return 0 if doc.extraction_status != "error" else 1

        if args.extract_lisr:
            doc, manifest_path = ingest_lisr(session, args.timeout)
            print(f"Manifest JSON: {manifest_path}")
            print(f"Documento    : {doc.document_id}")
            print(f"Estado       : {doc.extraction_status}")
            return 0 if doc.extraction_status != "error" else 1

        if args.extract_rlisr:
            doc, manifest_path = ingest_rlisr(session, args.timeout)
            print(f"Manifest JSON: {manifest_path}")
            print(f"Documento    : {doc.document_id}")
            print(f"Estado       : {doc.extraction_status}")
            return 0 if doc.extraction_status != "error" else 1

        if args.extract_cff:
            doc, manifest_path = ingest_cff(session, args.timeout)
            print(f"Manifest JSON: {manifest_path}")
            print(f"Documento    : {doc.document_id}")
            print(f"Estado       : {doc.extraction_status}")
            return 0 if doc.extraction_status != "error" else 1

        if args.extract_rcff:
            doc, manifest_path = ingest_rcff(session, args.timeout)
            print(f"Manifest JSON: {manifest_path}")
            print(f"Documento    : {doc.document_id}")
            print(f"Estado       : {doc.extraction_status}")
            return 0 if doc.extraction_status != "error" else 1

        if args.extract_lieps:
            doc, manifest_path = ingest_lieps(session, args.timeout)
            print(f"Manifest JSON: {manifest_path}")
            print(f"Documento    : {doc.document_id}")
            print(f"Estado       : {doc.extraction_status}")
            return 0 if doc.extraction_status != "error" else 1

        if args.extract_rlieps:
            doc, manifest_path = ingest_rlieps(session, args.timeout)
            print(f"Manifest JSON: {manifest_path}")
            print(f"Documento    : {doc.document_id}")
            print(f"Estado       : {doc.extraction_status}")
            return 0 if doc.extraction_status != "error" else 1

        if args.extract_frontera_norte:
            documents, manifest_path = ingest_frontera_norte(session, args.timeout)
            print(f"Manifest JSON: {manifest_path}")
            print(f"Documentos   : {len(documents)}")
            errors = sum(doc.extraction_status == "error" for doc in documents)
            print(f"Errores      : {errors}")
            return 0 if errors == 0 else 1

        if args.extract_lif_2026:
            doc, manifest_path = ingest_lif_2026(session, args.timeout)
            print(f"Manifest JSON: {manifest_path}")
            print(f"Documento    : {doc.document_id}")
            print(f"Estado       : {doc.extraction_status}")
            return 0 if doc.extraction_status != "error" else 1

        html = fetch_html(session, PAGE_URL, args.timeout)
        documents = discover_rmf_documents(session, html, PAGE_URL, args.timeout)
        document_ids = [doc.document_id for doc in documents]
        duplicate_ids = sorted(
            document_id
            for document_id in set(document_ids)
            if document_ids.count(document_id) > 1
        )
        if duplicate_ids:
            raise RuntimeError(
                "IDs documentales duplicados: " + ", ".join(duplicate_ids)
            )

        if args.list or not args.extract_all:
            print_documents(documents)
            return 0

        output_dir: Path = args.output
        text_dir = output_dir / "txt"
        temp_dir = output_dir / ".tmp"
        text_dir.mkdir(parents=True, exist_ok=True)
        previous = load_previous_manifest(output_dir) if args.resume else {}
        total = len(documents)

        for position, doc in enumerate(documents, start=1):
            print(f"[{position}/{total}] {doc.document_id} — {doc.title}")
            if args.resume and resume_document(
                doc,
                previous.get(doc.document_id),
                text_dir,
            ):
                logging.info("Ya extraído, se omite: %s", doc.filename_txt)
            else:
                process_document(
                    session=session,
                    doc=doc,
                    text_dir=text_dir,
                    temp_dir=temp_dir,
                    timeout=args.timeout,
                    delay=args.delay,
                )
            write_manifest(documents, output_dir)

        json_path, csv_path = write_manifest(documents, output_dir)
        print(f"\nManifest JSON: {json_path}")
        print(f"Manifest CSV : {csv_path}")
        print(f"Documentos   : {len(documents)}")

        return 0

    except requests.RequestException as exc:
        logging.error("Error HTTP: %s", exc)
        return 2
    except KeyboardInterrupt:
        logging.error("Interrumpido por usuario.")
        return 130
    except Exception as exc:
        logging.exception("Error: %s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
