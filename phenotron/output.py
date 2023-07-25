from pyphetools.creation import Individual

def output(samples, metadata, output_dir):
    Individual.output_individuals_as_phenopackets(samples, metadata = metadata.to_ga4gh())
