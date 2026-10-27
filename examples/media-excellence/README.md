# Renderable Media Excellence reference

This is **authored architecture illustration**, not a product capture. It demonstrates
one source-driven cross-format workflow without invented KPIs, customer testimony,
publication events, or official logos.

Run from repository root:

```bash
python -m pip install cairosvg pymupdf pillow
python scripts/render_media_pack.py --output /tmp/starlight-media-sample
```

Requires FFmpeg with libx264 available in PATH. `--skip-video` renders stills,
editable SVG, an accessible keyboard-navigable `scene.html`, four-page vector PDF,
VTT captions and manifest without FFmpeg. The resulting MP4 is silent by design;
audiovisual finish and substantive product-proof capture are separate workflows.

The `scene.json` is the editable master for this example. Its SHA-256 appears in
`manifest.json` with hashes of every actual rendition. Renderer does not grant QA,
founder approval, publishing permission or DAM upload. The ZIP media pack can be
uploaded to Drive/R2 only after a production adaptor with explicit auth and
appropriate rights has been tested. Artifact absolute paths are not public URLs.

## Independent acceptance

1. Compare first, middle and last frames of MP4 against the storyboard.
2. Inspect all PDF pages at full size and mobile thumbnail scale.
3. Verify output SHA-256s against the manifest and exercise the interactive
   scene's keyboard and button navigation.
4. Reject stale revision, false live-product claims and duplicate publication.
5. Keep authoring, renderer QA and release approval as distinct receipts.

Future work: convert this reference into a reusable scene composer/editor and bind
approved artifact records into real GenCreator/CIS DAM contracts.

The PDF /ID fields are seeded from the frozen scene digest. Reproducing the same scene in the tested renderer environment yields byte-identical artifacts, including the vector carousel PDF.
