import pandas as pd
import numpy as np
import logging
from pyphetools.creation import Individual, HpTerm

pd.set_option('display.max_colwidth', None)


class ExcelTransformer:
    def __init__(self, sep, ontology, id_pos, phenotype_pos, age_pos):
        self.ontology = ontology
        self.sep = sep
        self.id_pos = id_pos
        self.phenotype_pos = phenotype_pos
        self.age_pos = age_pos

    def __done(self):
        logging.info("Done..")

    def to_phenopackets(self, filepath):
        logging.info('Loading neonatal data [{0}].'.format(filepath))
        df = pd.read_csv(filepath, sep=self.sep, keep_default_na=False)
        self.__done()
        # logging.info("Identifying hpo columns..")
        logging.info("Scanning samples that have no phenotypes..")
        empty_idx = np.where(df.iloc[self.phenotype_pos].eq('') | df.iloc[self.phenotype_pos].isna())[0].tolist()
        empty_samples = [df.iloc[i, 0] for i in empty_idx]
        logging.info(empty_samples)
        # logging.info("Dropping empties..")
        # df.drop(empty_idx, axis=0, inplace=True)
        self.__done()
        logging.info("Mapping rows to phenopackets...")
        samples = []
        for index, row in df.iterrows():
            samples.append(self.__row_to_phenopacket(row))
        self.__done()
        return samples

    def __row_to_phenopacket(self, row):
        terms = self.__to_hpterm(row[self.phenotype_pos].split(","))
        if not self.age_pos:
            return Individual(row[self.id_pos], terms, interpretation_list=[])
        else:
            return Individual(row[self.id_pos], terms, age=row[self.age_pos], interpretation_list=[])

    def __to_hpterm(self, terms):
        result = []
        for term in list(filter(None, terms)):
            term = self.ontology.get_term(term.replace(' ', ''))
            if term:
                result.append(HpTerm(term.identifier.value, term.name))
        return result
