"""Behavior tests: generated renditions, hash-bound receipts, and rejection cases."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'scripts'))
from render_media_pack import check, process
from verify_media_manifest import verify


class MediaPackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scene=json.loads((BASE/'examples/media-excellence/scene.json').read_text())

    def test_known_example_passes_schema(self):
        check(self.scene)

    def test_rejects_unproven_source_lane(self):
        test=copy.deepcopy(self.scene)
        test['kind']='live-product-demo'
        with self.assertRaisesRegex(ValueError,'authored architectural'):
            check(test)

    def test_rejects_overlong_copy(self):
        test=copy.deepcopy(self.scene)
        test['beats'][0]['headline'][0]='this is a headline line much longer than possible'
        with self.assertRaisesRegex(ValueError,'headline'):
            check(test)

    def test_real_renditions_and_manifest_integrity(self):
        with tempfile.TemporaryDirectory() as d:
            dest=Path(d)
            manifest=process(['--output',d,'--skip-video'])
            self.assertEqual(verify(dest/'manifest.json'),[])
            self.assertEqual(len(manifest['artifacts']),13)
            self.assertEqual(manifest['state']['qa'],'NOT_REVIEWED')
            self.assertFalse(manifest['claims']['live_product_proof'])
            self.assertTrue((dest/'scene.html').read_text().find('ArrowRight') >= 0)
            import fitz
            doc=fitz.open(dest/'carousel.pdf')
            self.assertEqual(len(doc),4)
            doc.close()
            with open(dest/'carousel-01.svg','ab') as f: f.write(b'\n<!--tampered-->')
            self.assertTrue(any('hash mismatch' in x for x in verify(dest/'manifest.json')))

    def test_pdf_reproducible_across_fresh_renders(self):
        with tempfile.TemporaryDirectory() as d:
            first=Path(d)/'a'
            second=Path(d)/'b'
            left=process(['--output',str(first),'--skip-video'])
            right=process(['--output',str(second),'--skip-video'])
            self.assertEqual(left['source_revision'],right['source_revision'])
            for name in ('carousel.pdf','carousel-01.svg','wide-architecture.png'):
                self.assertEqual((first/name).read_bytes(),(second/name).read_bytes())

    def test_rejects_fake_publication_and_traversal(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            src={
                'schema_version':'media-rendition-receipt.v1',
                'source_revision':'0'*64,
                'rights':'original','evidence_note':'sample',
                'artifacts':[{'path':'../unsafe','sha256':'0'*64,'bytes':0}],
                'state':{'render':'RENDERED','qa':'NOT_REVIEWED','approval':'FOUNDER_APPROVED','publication':'PUBLISHED'},
                'claims':{'live_product_proof':True},'kind':'authored-architecture-illustration',
            }
            path=root/'manifest.json'
            path.write_text(json.dumps(src))
            r=';'.join(verify(path))
            for word in ('unsafe artifact path','approved without','published without','conceptual illustration'):
                self.assertIn(word,r)


if __name__=='__main__':unittest.main()
