from pathlib import Path

path = Path('templates/backend/products.html')
text = path.read_text(encoding='utf-8')
old_header = "<div class=\"d-flex justify-content-between align-items-center mb-4\">\n            <h1>?��?管�?"\n            <a href=\"{{ url_for('backend.create_product') }}\" class=\"btn btn-primary\">\n                <i class=\"fas fa-plus\"></i> 添�??��?\n            </a>\n        </div>"
new_header = "<div class=\"d-flex flex-wrap justify-content-between align-items-center gap-2 mb-4\">\n            <h1 class=\"mb-0\">?��?管�?"\n            <div class=\"d-flex gap-2\">\n                <a href=\"{{ url_for('backend.dashboard') }}\" class=\"btn btn-outline-secondary\">\n                    <i class=\"fas fa-arrow-left\"></i> 返回
                </a>\n                <a href=\"{{ url_for('backend.create_product') }}\" class=\"btn btn-primary\">\n                    <i class=\"fas fa-plus\"></i> 添�??��?\n                </a>\n            </div>\n        </div>"
if old_header not in text:
    raise SystemExit('header not found in products.html')
text = text.replace(old_header, new_header)
path.write_text(text, encoding='utf-8')
