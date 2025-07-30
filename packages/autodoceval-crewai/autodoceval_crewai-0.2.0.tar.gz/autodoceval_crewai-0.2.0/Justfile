# Document evaluation and improvement workflow using Just

# Settings
input_dir := "docs/input"
output_dir := "docs/output"

# Default: show available commands
default:
    @just --list

# Auto-improve all documents
all: 
    #!/usr/bin/env python3
    import sys; sys.path.insert(0, '.')
    from pathlib import Path
    from evcrew import DocumentCrew
    from evcrew.utils import read_file
    
    for doc_path in sorted(Path("{{input_dir}}").glob("*.md")):
        name = doc_path.stem
        print(f"\n🔄 Processing {name}...")
        crew = DocumentCrew()
        output_path = Path("{{output_dir}}") / name
        output_path.mkdir(parents=True, exist_ok=True)
        crew.auto_improve_one(read_file(doc_path), output_path, name, str(doc_path))

# Evaluate all documents
evaluate-all:
    #!/usr/bin/env python3
    import sys; sys.path.insert(0, '.')
    from pathlib import Path
    from evcrew import DocumentCrew
    from evcrew.utils import read_file
    
    crew = DocumentCrew()
    for doc_path in sorted(Path("{{input_dir}}").glob("*.md")):
        name = doc_path.stem
        output_path = Path("{{output_dir}}") / name
        output_path.mkdir(parents=True, exist_ok=True)
        content = read_file(doc_path)
        score, feedback = crew.evaluate_one(content)
        print(f"📊 {name}: {score:.0f}%")
        crew.evaluator.save(score, feedback, content, output_path, name, doc_path)

# Evaluate single document
evaluate-one name:
    #!/usr/bin/env python3
    import sys; sys.path.insert(0, '.')
    from pathlib import Path
    from evcrew import DocumentCrew
    from evcrew.utils import read_file
    
    doc_path = Path("{{input_dir}}/{{name}}.md")
    output_path = Path("{{output_dir}}/{{name}}")
    output_path.mkdir(parents=True, exist_ok=True)
    
    crew = DocumentCrew()
    content = read_file(doc_path)
    score, feedback = crew.evaluate_one(content)
    print(f"📊 {{name}}: {score:.0f}%")
    crew.evaluator.save(score, feedback, content, output_path, "{{name}}", doc_path)

# Evaluate and improve all documents
evaluate-and-improve-all:
    #!/usr/bin/env python3
    import sys; sys.path.insert(0, '.')
    from pathlib import Path
    from evcrew import DocumentCrew
    from evcrew.utils import read_file
    
    crew = DocumentCrew()
    for doc_path in sorted(Path("{{input_dir}}").glob("*.md")):
        name = doc_path.stem
        print(f"🔄 {name}: evaluating and improving...")
        output_path = Path("{{output_dir}}") / name
        output_path.mkdir(parents=True, exist_ok=True)
        content = read_file(doc_path)
        improved, score, feedback = crew.evaluate_and_improve_one(content, name)
        print(f"   → Final: {score:.0f}%")
        crew.improver.save(content, improved, score, feedback, output_path, name, doc_path)

# Evaluate and improve single document
evaluate-and-improve-one name:
    #!/usr/bin/env python3
    import sys; sys.path.insert(0, '.')
    from pathlib import Path
    from evcrew import DocumentCrew
    from evcrew.utils import read_file
    
    doc_path = Path("{{input_dir}}/{{name}}.md")
    output_path = Path("{{output_dir}}/{{name}}")
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"🔄 {{name}}: evaluating and improving...")
    crew = DocumentCrew()
    content = read_file(doc_path)
    improved, score, feedback = crew.evaluate_and_improve_one(content, "{{name}}")
    print(f"   → Final: {score:.0f}%")
    crew.improver.save(content, improved, score, feedback, output_path, "{{name}}", doc_path)

# Auto-improve all documents (alias)
auto-improve-all: all

# Auto-improve single document from custom path
auto-improve-one doc name:
    #!/usr/bin/env python3
    import sys; sys.path.insert(0, '.')
    from pathlib import Path
    from evcrew import DocumentCrew
    from evcrew.utils import read_file
    
    crew = DocumentCrew()
    output_path = Path("{{output_dir}}/custom")
    output_path.mkdir(parents=True, exist_ok=True)
    crew.auto_improve_one(read_file("{{doc}}"), output_path, "{{name}}", "{{doc}}")

# Clean all outputs
clean:
    rm -rf {{output_dir}}/*
    @echo "✨ Cleaned output directory"

# Development commands
test: && lint
    uv run pytest evcrew/tests/ -v

lint:
    uv run ruff check evcrew/

format:
    uv run ruff format evcrew/

# Show project structure
structure:
    tree -I '__pycache__|*.pyc|.git|venv|.venv|*.egg-info' .

# Publishing commands
build:
    uv build
    @echo "📦 Package built successfully"

publish-test:
    uv publish --test
    @echo "🧪 Published to TestPyPI"

publish:
    uv publish
    @echo "🚀 Published to PyPI"

# GitHub release
release version:
    git tag -a v{{version}} -m "Release v{{version}}"
    git push origin v{{version}}
    @echo "🏷️  Tagged release v{{version}}"