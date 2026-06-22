# AI For You - Substack Publisher Skill

Publishes an AI For You newsletter to Substack as a draft, including uploading local infographic images to Substack's CDN. Invoke with `/content-kit-substack [post number]` or `/content-kit-substack [path to newsletter file]`.

Handles image upload correctly: local file paths are uploaded to Substack's CDN first (via the substack_client Python library), then the real CDN URLs are used when building the draft. Passing local paths directly to the MCP image tool creates broken `assetError` nodes.
