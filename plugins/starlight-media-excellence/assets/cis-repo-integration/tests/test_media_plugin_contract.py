import sys,unittest,tempfile,shutil,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from validate_media_plugin import verify, P
class MediaPluginContract(unittest.TestCase):
    def test_valid_source(self):self.assertEqual(verify(),[])
    def test_missing_manifest_fails(self):
        with tempfile.TemporaryDirectory() as d:self.assertIn('missing plugin.json',verify(Path(d)))
    def test_mismatch_fails(self):
        with tempfile.TemporaryDirectory() as d:
            x=Path(d);shutil.copytree(P,x/'plugin');mp=x/'plugin/plugin.json';p=json.loads(mp.read_text());p['name']='wrong';mp.write_text(json.dumps(p));self.assertTrue(any('identity drift' in e for e in verify(x/'plugin')))
    def test_injected_mcp_fails(self):
        with tempfile.TemporaryDirectory() as d:
            x=Path(d)/'plugin';shutil.copytree(P,x);(x/'mcp.json').write_text('{}');self.assertTrue(any('unexpected MCP' in e for e in verify(x)))
if __name__=='__main__':unittest.main()
