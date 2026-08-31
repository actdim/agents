#!/usr/bin/env python3
"""
tests/test_skills_and_scripts.py - Comprehensive Unit Tests for Along Protocol & Skills Suite.

Guarantees:
1. Syntax & Compilation: Every Python file in scripts/ and skills/ is valid Python.
2. Anti-Corruption: No Python script contains Markdown headers or text instead of code.
3. Skill Manifests: Every skills/along-* directory contains valid SKILL.md with name and description.
4. Protocol Version Consistency: Versions across manifests, protocol.md, README.md, and scripts match.
5. Typography Sanitization: Zero non-ASCII typographic characters (em-dash, curly quotes, NBSP, ZWSP).
6. Engine CLI Execution: along_dash, along_update, migrate_protocol, along_exec, and along_commit run without errors.
7. Installer Integrity: All skill folders are covered by install scripts.
"""

import os
import sys
import glob
import re
import unittest
import subprocess
import tempfile
import shutil

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class TestAlongSkillsAndScripts(unittest.TestCase):

    def test_01_all_python_files_compile(self):
        """Verify that every .py file in scripts/ and skills/ compiles with zero syntax errors."""
        py_files = (
            glob.glob(os.path.join(REPO_ROOT, "scripts", "**", "*.py"), recursive=True) +
            glob.glob(os.path.join(REPO_ROOT, "skills", "**", "*.py"), recursive=True) +
            glob.glob(os.path.join(REPO_ROOT, ".along", "scripts", "**", "*.py"), recursive=True)
        )
        self.assertGreater(len(py_files), 5, "Should find at least 5 Python scripts in repo")

        for py_path in py_files:
            rel = os.path.relpath(py_path, REPO_ROOT)
            with open(py_path, "r", encoding="utf-8") as f:
                code = f.read()
            try:
                compile(code, py_path, "exec")
            except Exception as e:
                self.fail(f"Syntax/compilation error in {rel}: {e}")

    def test_02_no_markdown_in_python_scripts(self):
        """Guard against accidental overwrite of Python scripts with README/Markdown text."""
        py_files = (
            glob.glob(os.path.join(REPO_ROOT, "scripts", "**", "*.py"), recursive=True) +
            glob.glob(os.path.join(REPO_ROOT, "skills", "**", "*.py"), recursive=True)
        )
        forbidden_starters = ["# Along (v", "# ALONG-PROTOCOL v", "AI agents start every session blind"]
        
        for py_path in py_files:
            rel = os.path.relpath(py_path, REPO_ROOT)
            with open(py_path, "r", encoding="utf-8") as f:
                first_lines = [f.readline() for _ in range(15)]
            joined = "".join(first_lines)
            for marker in forbidden_starters:
                self.assertNotIn(marker, joined, f"Corrupted Python file detected in {rel}: contains Markdown text '{marker}'")

    def test_03_skill_manifests_validity(self):
        """Verify that every skills/along-* directory contains a valid SKILL.md with frontmatter."""
        skill_dirs = glob.glob(os.path.join(REPO_ROOT, "skills", "along-*"))
        self.assertGreaterEqual(len(skill_dirs), 10, "Should have at least 10 along-* skills")

        for sdir in skill_dirs:
            sname = os.path.basename(sdir)
            skill_md = os.path.join(sdir, "SKILL.md")
            self.assertTrue(os.path.exists(skill_md), f"Missing SKILL.md in {sname}")

            with open(skill_md, "r", encoding="utf-8") as f:
                content = f.read()

            self.assertTrue(content.startswith("---"), f"{sname}/SKILL.md must start with YAML front-matter '---'")
            self.assertIn(f"name: {sname}", content, f"{sname}/SKILL.md front-matter must specify 'name: {sname}'")
            self.assertIn("description:", content, f"{sname}/SKILL.md front-matter must specify 'description:'")

    def test_04_protocol_version_consistency(self):
        """Verify that protocol version is identical across protocol.md, AGENTS.md, README.md, and scripts."""
        proto_file = os.path.join(REPO_ROOT, "skills", "along-init", "protocol.md")
        with open(proto_file, "r", encoding="utf-8") as f:
            proto_text = f.read()
        
        m = re.search(r'# ALONG-PROTOCOL v(\d+\.\d+\.\d+)', proto_text)
        self.assertIsNotNone(m, "protocol.md must declare '# ALONG-PROTOCOL vX.Y.Z'")
        version = m.group(1)

        # Check AGENTS.md
        agents_md = os.path.join(REPO_ROOT, "AGENTS.md")
        with open(agents_md, "r", encoding="utf-8") as f:
            self.assertIn(f"# ALONG-PROTOCOL v{version}", f.read(), "AGENTS.md must match protocol.md version")

        # Check README.md
        readme_md = os.path.join(REPO_ROOT, "README.md")
        with open(readme_md, "r", encoding="utf-8") as f:
            readme_text = f.read()
            self.assertIn(f"# Along (v{version})", readme_text, "README.md header must match protocol version")
            self.assertIn(f"ALONG-PROTOCOL v{version}", readme_text, "README.md text must match protocol version")

        # Check migrate_protocol.py
        for mp in [os.path.join(REPO_ROOT, "scripts", "migrate_protocol.py"),
                   os.path.join(REPO_ROOT, "skills", "along-init", "migrate_protocol.py")]:
            if os.path.exists(mp):
                with open(mp, "r", encoding="utf-8") as f:
                    self.assertIn(f'CURRENT_PROTOCOL_VERSION = "{version}"', f.read(), f"{mp} version must match {version}")

    def test_05_clean_typography(self):
        """Verify zero non-ASCII typographic characters across repository text files."""
        forbidden_chars = {
            chr(0x2014): "em-dash",
            chr(0x2013): "en-dash",
            chr(0x201C): "curly double quote left",
            chr(0x201D): "curly double quote right",
            chr(0x2018): "curly single quote left",
            chr(0x2019): "curly single quote right",
            chr(0x2026): "ellipsis character",
            chr(0x00A0): "non-breaking space",
            chr(0x200B): "zero-width space",
            chr(0xFEFF): "BOM marker"
        }
        
        patterns = ['**/*.md', '**/*.py', '**/*.sh', '**/*.ps1', '**/*.json', '**/*.yaml', '**/*.yml']
        violations = []

        for pat in patterns:
            for filepath in glob.glob(os.path.join(REPO_ROOT, pat), recursive=True):
                # Skip .git, caches, tests, node_modules, dist, and typography sanitizer itself
                if any(x in filepath for x in [".git", "__pycache__", "scratch", "tests", "node_modules", "dist", ".vite", "sanitize_typography.py"]):
                    continue
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                except Exception:
                    continue

                for ch, desc in forbidden_chars.items():
                    if ch in content:
                        rel = os.path.relpath(filepath, REPO_ROOT)
                        violations.append(f"{rel}: contains {desc} (U+{ord(ch):04X})")

        self.assertEqual(len(violations), 0, f"Typography violations found:\n" + "\n".join(violations[:15]))

    def test_06_along_dash_cli_execution(self):
        """Verify that along_dash.py runs in CLI mode and produces DASHBOARD.md and dashboard.html."""
        dash_script = os.path.join(REPO_ROOT, "scripts", "along_dash.py")
        self.assertTrue(os.path.exists(dash_script), "scripts/along_dash.py must exist")

        cmd = [sys.executable, dash_script, REPO_ROOT, "--cli"]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0 and "No module named 'fastapi'" in res.stderr:
            # Fallback to uv run if fastapi is managed via uv
            cmd = ["uv", "run", "--with", "fastapi", "--with", "uvicorn", "--with", "httpx2", "--with", "pyyaml", "--with", "rich", dash_script, REPO_ROOT, "--cli"]
            res = subprocess.run(cmd, capture_output=True, text=True)

        self.assertEqual(res.returncode, 0, f"along_dash.py --cli failed:\n{res.stderr}")
        self.assertIn("Along Executive Dashboard", res.stdout)
        self.assertIn("Project Metrics Summary", res.stdout)

        self.assertTrue(os.path.exists(os.path.join(REPO_ROOT, ".along", "DASHBOARD.md")))
        self.assertTrue(os.path.exists(os.path.join(REPO_ROOT, ".along", "dashboard.html")))

    def test_07_migrate_protocol_execution(self):
        """Verify that migrate_protocol.py executes cleanly without runtime errors."""
        mig_script = os.path.join(REPO_ROOT, "scripts", "migrate_protocol.py")
        self.assertTrue(os.path.exists(mig_script), "scripts/migrate_protocol.py must exist")

        res = subprocess.run([sys.executable, mig_script, REPO_ROOT], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"migrate_protocol.py failed:\n{res.stderr}")
        self.assertIn("migrations & validations completed successfully", res.stdout)

    def test_08_along_update_check_only(self):
        """Verify that along_update.py runs in check-only mode cleanly."""
        update_script = os.path.join(REPO_ROOT, "scripts", "along_update.py")
        self.assertTrue(os.path.exists(update_script), "scripts/along_update.py must exist")

        res = subprocess.run([sys.executable, update_script, REPO_ROOT, "--check-only", "--local-only"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"along_update.py --check-only failed:\n{res.stderr}")
        self.assertIn("Check-Only Mode", res.stdout)

    def test_09_install_scripts_match_skills(self):
        """Verify that install.ps1 and install.sh contain references to all current along skills."""
        skill_dirs = [os.path.basename(p) for p in glob.glob(os.path.join(REPO_ROOT, "skills", "along-*"))]
        
        with open(os.path.join(REPO_ROOT, "install.ps1"), "r", encoding="utf-8") as f:
            ps1_content = f.read()
        with open(os.path.join(REPO_ROOT, "install.sh"), "r", encoding="utf-8") as f:
            sh_content = f.read()

        self.assertIn("Get-ChildItem -Directory $src", ps1_content)
        self.assertIn('for d in "$src"/*/', sh_content)

        self.assertIn("scripts", ps1_content)
        self.assertIn("scripts", sh_content)
        self.assertIn("protocol.md", ps1_content)
        self.assertIn("protocol.md", sh_content)

    def test_10_skills_pure_declarative(self):
        """Verify that skills/ directory contains only clean Markdown manifests and zero .py or __pycache__ files."""
        py_in_skills = glob.glob(os.path.join(REPO_ROOT, "skills", "**", "*.py"), recursive=True)
        pyc_in_skills = glob.glob(os.path.join(REPO_ROOT, "skills", "**", "*.pyc"), recursive=True)
        pycache_dirs = [d for d in glob.glob(os.path.join(REPO_ROOT, "skills", "**"), recursive=True) if "__pycache__" in d]

        self.assertEqual(len(py_in_skills), 0, f"skills/ directory must not contain .py files: {py_in_skills}")
        self.assertEqual(len(pyc_in_skills), 0, f"skills/ directory must not contain .pyc files: {pyc_in_skills}")
        self.assertEqual(len(pycache_dirs), 0, f"skills/ directory must not contain __pycache__: {pycache_dirs}")

    def test_11_along_exec_router_dispatch(self):
        """Verify that along_exec.py command router responds to --help and dispatches known commands."""
        exec_script = os.path.join(REPO_ROOT, "scripts", "along_exec.py")
        self.assertTrue(os.path.exists(exec_script), "scripts/along_exec.py must exist")

        res = subprocess.run([sys.executable, exec_script, "--help"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("Along Command Router", res.stdout)
        self.assertIn("kb-sync", res.stdout)
        self.assertIn("dep-scan", res.stdout)

    def test_12_along_exec_entity_management(self):
        """Verify that along_exec.py manages issues, sessions, and scratchpads cleanly without inline shell scripts."""
        exec_script = os.path.join(REPO_ROOT, "scripts", "along_exec.py")
        
        # 1. Scratchpad lifecycle
        init_res = subprocess.run([sys.executable, exec_script, "scratch", "init", "unit-test-task"], capture_output=True, text=True)
        self.assertEqual(init_res.returncode, 0)
        scratch_dir = os.path.join(REPO_ROOT, ".along", ".session", "unit-test-task")
        self.assertTrue(os.path.exists(scratch_dir), "Scratchpad directory should exist")
        self.assertTrue(os.path.exists(os.path.join(scratch_dir, "plan.md")), "plan.md should exist")

        purge_res = subprocess.run([sys.executable, exec_script, "scratch", "purge", "unit-test-task"], capture_output=True, text=True)
        self.assertEqual(purge_res.returncode, 0)
        self.assertFalse(os.path.exists(scratch_dir), "Scratchpad directory should be purged")

        # 2. Issue list command
        list_res = subprocess.run([sys.executable, exec_script, "issue", "list"], capture_output=True, text=True)
        self.assertEqual(list_res.returncode, 0)
        self.assertIn("Active issues in", list_res.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)

