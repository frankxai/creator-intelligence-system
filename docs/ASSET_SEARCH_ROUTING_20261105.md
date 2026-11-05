# Owned asset discovery update

Private plugin candidate: Starlight Media Excellence 0.3.3. The previous account
release was 0.3.2; repository source was 0.3.1. This change preserves the account
release's manifest, presentation, icon, renderers and data-use declaration while
adding the retrieval workflow to media-continuity. No MCP endpoint or account
binding is added to the skills-only package.

The retrieval trigger now covers existing images, visual references, characters,
catalog coverage and reuse. It resolves workspace/collection coverage before
provider choice, distinguishes metadata from visual similarity, preserves exact
identities and proportions, and refuses to infer global absence or a new version's
approval from another provider/version. The accepted portfolio media default is
R2 binary storage plus Supabase metadata; each connection still needs live evidence.

## Behavioral exercise

A fresh same-provider agent received the candidate workflow and a fictional creator
request to reuse a copper fox in a 16:9 crew image. Supplied results contained a
1536x864 Library v3 reference with matching character ID, an unrelated square idea,
zero Cloudinary matches, unavailable R2 access, and Supabase asset-level approval
on an older version. No preview tool or source links were supplied.

Observed response selected the matching 16:9 reference, preserved proportions,
reported each source's coverage, withheld visual verification, and required a v3
preview/approval receipt. It did not invent links, claim a new approval, change
the aspect ratio, or treat Cloudinary's empty result as global absence.

This is instruction forward-testing with supplied synthetic records. It is not
independent security review, proof of implicit selection in every future chat,
or verification of a deployed DAM connection.

Runtime implementation and local acceptance are tracked independently in
[visual-intelligence #65](https://github.com/frankxai/visual-intelligence/issues/65).
GenCreator remains the public product; a public server-backed edition needs the
actual endpoint, authentication, listing facts and host review evidence.
