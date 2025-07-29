"""
Utility functions for handling the mime types of heaobject.data.Data objects.
"""
# Pypi ignores the entry in mypy.ini for mimetype_description for some reason.
from mimetype_description import get_mime_type_description, guess_mime_type as _guess_mime_type  #type:ignore
import mimetypes
from collections.abc import Sequence

# Non-standard mimetypes that we may assign to files in AWS S3 buckets.
MIME_TYPES = (('application/x.fastq', ['.fq', '.fastq'], 'FASTQ File'),  # https://en.wikipedia.org/wiki/FASTQ_format
              ('application/x.vcf', ['.vcf'], 'VCF File'),  # https://en.wikipedia.org/wiki/Variant_Call_Format
              ('application/x.fasta', ['.fasta', '.fa', '.fna', '.ffn', '.faa', '.frn'], 'FASTA File'),  # https://en.wikipedia.org/wiki/FASTA_format
              ('application/x.sam', ['.sam'], 'SAM File'),  # https://en.wikipedia.org/wiki/SAM_(file_format)
              ('application/x.bam', ['.bam'], 'BAM File'),  # https://support.illumina.com/help/BS_App_RNASeq_Alignment_OLH_1000000006112/Content/Source/Informatics/BAM-Format.htm#:~:text=A%20BAM%20file%20(*.,file%20naming%20format%20of%20SampleName_S%23.
              ('application/x.bambai', ['.bam.bai'], 'BAM Index File'), # https://support.illumina.com/help/BS_App_RNASeq_Alignment_OLH_1000000006112/Content/Source/Informatics/BAM-Format.htm#:~:text=A%20BAM%20file%20(*.,file%20naming%20format%20of%20SampleName_S%23.
              ('application/x.gff3', ['.gff'], 'GFF File'),  # https://en.wikipedia.org/wiki/General_feature_format and https://github.com/The-Sequence-Ontology/Specifications/blob/master/gff3.md
              ('application/x.gvf', ['.gvf'], 'GVF File'))  # https://github.com/The-Sequence-Ontology/Specifications/blob/master/gvf.md

DEFAULT_MIME_TYPE = 'application/octet-stream'
mimetypes.init()

_extra_descriptions: dict[str, str] = {}


def guess_mime_type(url: str) -> str:
    """
    Returns the mime type for the given URL, file name, or path, based on the file extension.

    :param url: the file path or URL (required).
    :returns: the mime type.
    """
    result = _guess_mime_type(url)
    if result is None:
        result = mimetypes.guess_type(url, False)[0]
    return result if result is not None else DEFAULT_MIME_TYPE

def get_description(mime_type: str) -> str | None:
    result = get_mime_type_description(mime_type)
    if result is None:
        result = _extra_descriptions.get(mime_type)
    if result is None or result.casefold() == 'unknown':
        return None
    return ' '.join(word[0].upper() + word[1:] for word in result.split())

def register_mime_type(mime_type: str, extensions: Sequence[str], description: str):
    for ext in extensions:
        mimetypes.add_type(mime_type, ext)
    _extra_descriptions[mime_type] = description


for mime_type, extensions, description in MIME_TYPES:
        register_mime_type(mime_type, extensions, description)
