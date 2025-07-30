__version__ = '0.36.1'

from rdworks.conf    import Conf
from rdworks.mol     import Mol
from rdworks.mollibr import MolLibr

from rdworks.stereoisomers import complete_stereoisomers
from rdworks.tautomers import complete_tautomers
from rdworks.ionized import IonizedStates

from rdworks.readin import read_csv, merge_csv, read_dataframe, read_smi, read_sdf, read_mae 
from rdworks.std import desalt_smiles, standardize_smiles, standardize

from rdworks.rgroup import expand_rgroup, most_common, most_common_in_NP
from rdworks.scaffold import scaffold_network, scaffold_tree, BRICS_fragmented, BRICS_fragment_indices
from rdworks.matchedseries import MatchedSeries

from rdworks.descriptor import rd_descriptor, rd_descriptor_f
from rdworks.xml import list_predefined_xml, get_predefined_xml, parse_xml

import rdkit
import logging

__rdkit_version__ = rdkit.rdBase.rdkitVersion

rdkit_logger = rdkit.RDLogger.logger().setLevel(rdkit.RDLogger.CRITICAL)

main_logger = logging.getLogger()
main_logger.setLevel(logging.INFO) # level: DEBUG < INFO < WARNING < ERROR < CRITICAL
logger_formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s %(message)s', 
                                     datefmt='%Y-%m-%d %H:%M:%S')
logger_ch = logging.StreamHandler()
logger_ch.setFormatter(logger_formatter)
main_logger.addHandler(logger_ch)
