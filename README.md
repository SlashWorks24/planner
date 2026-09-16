# Slash Works Room Planner

Plan a room with Slash Works furniture at actual size, then download a PDF plan or send an inquiry to info@slash-works.com.

**Live site:** https://YOUR-USERNAME.github.io/planner/
**Team view (shows pricing):** add `?team=1` to the end of the link.

## Files

| File | What it is |
|---|---|
| `index.html` | The planner app |
| `settings.js` | Prices, piece names, inquiry email, disclaimer, finishes. **Edit this one.** |
| `data/models.js` | The five furniture models (generated from Rhino .obj files) |
| `data/photos.js` | Product photos and logo (embedded images) |
| `tools/build_models.py` | Rebuilds `data/models.js` from new .obj files |

## Common edits

- **Change a price or name:** open `settings.js` on GitHub, click the pencil icon, edit, then click **Commit changes**. The live site updates in 1 to 2 minutes.
- **Update a 3D model:** export from Rhino as .obj (inches), then run `python3 tools/build_models.py path/to/obj/folder` and upload the new `data/models.js`.

Runs in Chrome and Safari. Needs an internet connection to load three.js and jsPDF.
