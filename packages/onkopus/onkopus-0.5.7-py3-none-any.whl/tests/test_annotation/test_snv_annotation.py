import unittest, os
import onkopus


class TestCLIAnnotation(unittest.TestCase):
#

    def test_cli_annotation(self):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        infile = __location__ + "/../test_files/somaticMutations.hg38.ln200.vcf"
        outfile = infile + ".anno.csv"
        bframe = onkopus.read_file(infile)
        bframe.data = onkopus.annotate_variant_data(bframe.data, genome_version="hg19")
        onkopus.write_file(outfile,bframe)

        for var in bframe.data.keys():
            vartype = bframe.data[var]["type"]
            #print(vartype)
            #print(var, bframe.data[var])

        self.assertEqual(bframe.data["chr7:21745009A>G"]["UTA_Adapter_gene"]["hgnc_symbol"],"DNAH11","")

