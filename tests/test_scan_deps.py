#!/usr/bin/env python3
"""
tests/test_scan_deps.py - Unit tests for along_scan_deps.py AI Dependencies Discovery engine.
"""

import os
import sys
import json
import shutil
import tempfile
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCAN_DEPS_MODULE = os.path.join(REPO_ROOT, "skills", "along-dep-scan")
sys.path.insert(0, SCAN_DEPS_MODULE)

import along_dep_scan as along_scan_deps

class TestAlongScanDeps(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="along_test_deps_")

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_01_node_dependencies_discovery(self):
        """Test scanning Node.js project with npm/pnpm dependencies containing AGENTS.md and llms.txt."""
        pkg_json = {
            "name": "test-node-app",
            "dependencies": {
                "mock-lib-a": "^1.0.0",
                "@scoped/mock-lib-b": "^2.1.0",
                "regular-lib-c": "^3.0.0"
            }
        }
        with open(os.path.join(self.test_dir, "package.json"), "w", encoding="utf-8") as f:
            json.dump(pkg_json, f)

        # Create mock node_modules
        lib_a_dir = os.path.join(self.test_dir, "node_modules", "mock-lib-a")
        os.makedirs(lib_a_dir, exist_ok=True)
        with open(os.path.join(lib_a_dir, "AGENTS.md"), "w", encoding="utf-8") as f:
            f.write("# Mock Lib A Rules\nAlways use function X.")
        with open(os.path.join(lib_a_dir, "package.json"), "w", encoding="utf-8") as f:
            json.dump({"name": "mock-lib-a", "version": "1.0.0", "ai": {"rules": "AGENTS.md"}}, f)

        lib_b_dir = os.path.join(self.test_dir, "node_modules", "@scoped", "mock-lib-b")
        os.makedirs(lib_b_dir, exist_ok=True)
        with open(os.path.join(lib_b_dir, "llms.txt"), "w", encoding="utf-8") as f:
            f.write("# Scoped Lib B LLMS Context")

        # regular-lib-c has no AI files
        lib_c_dir = os.path.join(self.test_dir, "node_modules", "regular-lib-c")
        os.makedirs(lib_c_dir, exist_ok=True)
        with open(os.path.join(lib_c_dir, "package.json"), "w", encoding="utf-8") as f:
            json.dump({"name": "regular-lib-c", "version": "3.0.0"}, f)

        results = along_scan_deps.scan_node_deps(self.test_dir)
        self.assertEqual(len(results), 2, "Should discover 2 packages with AI context")

        pkg_names = [r["package"] for r in results]
        self.assertIn("mock-lib-a", pkg_names)
        self.assertIn("@scoped/mock-lib-b", pkg_names)
        self.assertNotIn("regular-lib-c", pkg_names)

    def test_02_python_dependencies_discovery(self):
        """Test scanning Python project with requirements.txt and .venv site-packages."""
        with open(os.path.join(self.test_dir, "requirements.txt"), "w", encoding="utf-8") as f:
            f.write("mock-ai-tool>=1.0.0\nstandard-pkg==2.0\n")

        # Mock virtual environment
        site_pkgs = os.path.join(self.test_dir, ".venv", "Lib", "site-packages")
        os.makedirs(site_pkgs, exist_ok=True)

        tool_dir = os.path.join(site_pkgs, "mock_ai_tool")
        os.makedirs(tool_dir, exist_ok=True)
        with open(os.path.join(tool_dir, "AGENTS.md"), "w", encoding="utf-8") as f:
            f.write("# Mock AI Tool Instructions")

        # dist-info metadata
        dist_info = os.path.join(site_pkgs, "mock_ai_tool-1.2.0.dist-info")
        os.makedirs(dist_info, exist_ok=True)
        with open(os.path.join(dist_info, "METADATA"), "w", encoding="utf-8") as f:
            f.write("Metadata-Version: 2.1\nName: mock-ai-tool\nVersion: 1.2.0\n")

        results = along_scan_deps.scan_python_deps(self.test_dir)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["package"], "mock-ai-tool")
        self.assertEqual(results[0]["version"], "1.2.0")
        self.assertEqual(results[0]["ecosystem"], "pypi")

    def test_03_rust_dependencies_discovery(self):
        """Test scanning Rust project with Cargo.toml and vendored dependencies."""
        cargo_content = """
        [package]
        name = "test-rust-app"
        version = "0.1.0"

        [dependencies]
        mock-crate-a = "0.5.0"
        mock-crate-b = "1.0"
        """
        with open(os.path.join(self.test_dir, "Cargo.toml"), "w", encoding="utf-8") as f:
            f.write(cargo_content)

        # Mock vendored crate
        v_crate_a = os.path.join(self.test_dir, "vendor", "mock-crate-a")
        os.makedirs(v_crate_a, exist_ok=True)
        with open(os.path.join(v_crate_a, "llms.txt"), "w", encoding="utf-8") as f:
            f.write("# Mock Crate A LLMs instructions")

        results = along_scan_deps.scan_rust_deps(self.test_dir)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["package"], "mock-crate-a")
        self.assertEqual(results[0]["ecosystem"], "cargo")

    def test_04_run_scanner_and_kb_generation(self):
        """Test full scanner lifecycle: creates .along/KB/topic--dependencies.md idempotently."""
        pkg_json = {
            "dependencies": {
                "fast-sdk": "^1.0.0"
            }
        }
        with open(os.path.join(self.test_dir, "package.json"), "w", encoding="utf-8") as f:
            json.dump(pkg_json, f)

        sdk_dir = os.path.join(self.test_dir, "node_modules", "fast-sdk")
        os.makedirs(sdk_dir, exist_ok=True)
        with open(os.path.join(sdk_dir, "AGENTS.md"), "w", encoding="utf-8") as f:
            f.write("# Fast SDK rules")

        results = along_scan_deps.run_scanner(self.test_dir, dry_run=False)
        self.assertEqual(len(results), 1)

        dep_kb = os.path.join(self.test_dir, "docs", "topic--dependencies.md")
        self.assertTrue(os.path.isfile(dep_kb), "docs/topic--dependencies.md should be created")

        with open(dep_kb, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("fast-sdk", content)
        self.assertIn("node_modules/fast-sdk/AGENTS.md", content)
        self.assertIn("protocol: along", content)

        # Re-run after removing dependency from package.json (idempotency check)
        with open(os.path.join(self.test_dir, "package.json"), "w", encoding="utf-8") as f:
            json.dump({"dependencies": {}}, f)

        results_empty = along_scan_deps.run_scanner(self.test_dir, dry_run=False)
        self.assertEqual(len(results_empty), 0)

        with open(dep_kb, "r", encoding="utf-8") as f:
            content_empty = f.read()
        self.assertNotIn("fast-sdk", content_empty)
        self.assertIn("No active dependencies with AI instructions", content_empty)

if __name__ == "__main__":
    unittest.main()

