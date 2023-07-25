import click
import logging
from hpotk import Ontology
from hpotk.ontology.load.obographs import load_ontology
from pyphetools.creation import MetaData
from . import ExcelTransformer
from . import output
from . import ClickValidator


@click.group()
def cli():
    pass


@cli.command(name='delimited')
@click.option('--id', required=True, help='The 0-based index of the id column', type=click.IntRange(0, 999))
@click.option('--phenotype', required=True, help='The 0-based index of the phenotype column',
              type=click.IntRange(0, 20, ))
@click.option('--age', help='The 0-based index of the age column', type=click.IntRange(0, 20))
@click.option('--orcid', required=True, help='ORCiD of command executor', callback=ClickValidator.is_orcid)
@click.option('--sep', default="\t", help='The seperator of the delimited file', callback=ClickValidator.is_sep)
@click.argument('filepath', type=click.Path(exists=True))
def delimited(filepath, sep, orcid, id, phenotype, age):
    """Converts a delimited file to a phenopacket based on columns and content passed"""
    logging.info("Loading graph data..")
    o: Ontology = load_ontology('http://purl.obolibrary.org/obo/hp.json')
    metadata = MetaData(created_by="ORCID:{0}".format(orcid))
    metadata.default_versions_with_hpo(version=o.version)
    et = ExcelTransformer(sep, o, id, phenotype, age)
    samples = et.to_phenopackets(filepath)
    output(samples, metadata, "phenopackets")


if __name__ == "__main__":
    cli()
