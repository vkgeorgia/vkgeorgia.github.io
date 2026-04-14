# Digital Avatar (Frontend in this repo)

This repository now contains the **website integration layer** for the Digital Avatar:
- embeddable widget assets in `digital-avatar/frontend/`
- supporting docs in `digital-avatar/docs/`

## Backend Location

Backend runtime (API, RAG, deployments, DB integrations) has moved to:
- **https://github.com/vkgeorgia/Jeeves**

Any backend changes should be implemented in `vkgeorgia/Jeeves`, not in this repository.

## Current Structure (this repo)

```
digital-avatar/
├── frontend/        # Chat widget assets for website integration
│   ├── widget.js
│   ├── widget.css
│   ├── demo.html
│   ├── script.js
│   └── style.css
└── docs/            # Historical/auxiliary docs
```

## Integration

To embed the widget on pages:

```html
<link rel="stylesheet" href="/digital-avatar/frontend/widget.css">
<script src="/digital-avatar/frontend/widget.js"></script>
```
