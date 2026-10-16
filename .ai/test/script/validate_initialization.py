"""Static import/configuration checks. Never starts services or executes SQL."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[3]
NS = {"m": "http://maven.apache.org/POM/4.0.0"}
SOURCE_REVISION = "7e31b5374f4b889a9ea306d73a5623b1e49c786a"
EXPECTED_MODULES = {
    "big-market-app", "big-market-api", "big-market-domain",
    "big-market-infrastructure", "big-market-querys", "big-market-trigger",
    "big-market-types",
}
# Exact initialization exceptions; Java, SQL, test and Mapper changes are not allowed.
IMPORT_CHANGES = {
    "README.md", ".gitignore", "pom.xml",
    ".github/workflows/docker-image.yml",
    ".github/workflows/openai-code-review.yml",
    "big-market-app/pom.xml", "big-market-trigger/pom.xml",
    "big-market-infrastructure/pom.xml",
    "big-market-app/Dockerfile", "big-market-app/ActionDockerfile",
    "big-market-app/build.sh",
    "big-market-app/src/main/resources/application.yml",
    "big-market-app/src/main/resources/application-dev.yml",
    "big-market-app/src/main/resources/application-test.yml",
    "big-market-app/src/main/resources/application-prod.yml",
    "big-market-app/src/main/resources/spring/spring-config-token.xml",
}


def run(args: list[str], *, cwd: Path = ROOT, data: str | None = None):
    result = subprocess.run(
        args, cwd=cwd, input=data, capture_output=True,
        encoding="utf-8", errors="replace", timeout=60,
    )
    if result.returncode:
        raise RuntimeError(f"{args[0]} exited {result.returncode}: {result.stderr.strip()}")
    return result.stdout


def check_structure() -> None:
    pom = ET.parse(ROOT / "pom.xml").getroot()
    modules = {m.text for m in pom.findall("m:modules/m:module", NS)}
    assert modules == EXPECTED_MODULES, f"Unexpected modules: {modules}"
    assert pom.findtext("m:parent/m:version", namespaces=NS) == "2.7.12"
    assert pom.findtext("m:properties/m:java.version", namespaces=NS) == "1.8"
    assert pom.findtext("m:properties/m:skipTests", namespaces=NS) == "true"
    for module in sorted(modules):
        p = ROOT / module / "pom.xml"
        assert p.is_file(), f"Missing {p}"
        model = ET.parse(p).getroot()
        for dep in model.findall("m:dependencies/m:dependency", NS):
            if dep.findtext("m:groupId", namespaces=NS) == "cn.bugstack":
                name = dep.findtext("m:artifactId", namespaces=NS)
                assert name in modules, f"Missing reactor dependency: {name}"
    xml_files = [ROOT / "pom.xml"]
    for module in modules:
        xml_files.append(ROOT / module / "pom.xml")
        xml_files.extend((ROOT / module / "src").rglob("*.xml"))
    for p in xml_files:
        ET.parse(p)
    for p in [ROOT / "pom.xml", *(ROOT / m / "pom.xml" for m in modules)]:
        model = ET.parse(p).getroot()
        assert not model.findall(".//m:dependency[m:artifactId='redisson-spring-boot-starter']", NS)
    amqp = pom.find("m:dependencyManagement/m:dependencies/m:dependency[m:artifactId='spring-boot-starter-amqp']", NS)
    assert amqp is not None and amqp.find("m:version", NS) is None
    resources = ROOT / "big-market-app/src/main/resources"
    for name in ["application.yml", "application-dev.yml", "application-test.yml", "application-prod.yml"]:
        text = (resources / name).read_text(encoding="utf-8")
        assert "192.168." not in text and "116.198." not in text and "117.72." not in text
    assert "TBD" not in (ROOT / ".ai/project.md").read_text(encoding="utf-8")
    for name in ["big_market", "big_market_01", "big_market_02", "xxl_job"]:
        sql = ROOT / f"docs/dev-ops/mysql/sql/{name}.sql"
        assert sql.is_file() and f"`{name}`" in sql.read_text(encoding="utf-8")
    paths = ["big-market-app/target/probe.jar", "data/probe.log", ".env", "config/application-dev.yml"]
    ignored = run(["git", "check-ignore", "--no-index", *paths])
    assert set(ignored.splitlines()) == set(paths), "Local files not ignored"
    for name in [".ai/project.md", "docs/dev-ops/mysql/sql/big_market.sql", "AGENTS.md"]:
        result = subprocess.run(["git", "check-ignore", "--no-index", "-q", name], cwd=ROOT)
        assert result.returncode == 1, f"Required source ignored: {name}"
    print(f"PASS: 7 modules, {len(xml_files)} XML files, dependency/configuration and ignore checks")


def check_import(source: Path) -> None:
    source = source.resolve()
    command = ["git", "-c", f"safe.directory={source.as_posix()}"]
    revision = run([*command, "rev-parse", "HEAD"], cwd=source).strip()
    assert revision == SOURCE_REVISION, "Source revision differs from import baseline"
    assert not run([*command, "status", "--porcelain"], cwd=source).strip(), "Source worktree changed"
    names = run([*command, "ls-files", "-z"], cwd=source).split("\0")
    names = [name for name in names if name]
    changed: list[str] = []
    java_count = 0
    for name in names:
        original, copied = source / name, ROOT / name
        assert copied.is_file(), f"Source file not copied: {name}"
        if hashlib.sha256(original.read_bytes()).digest() != hashlib.sha256(copied.read_bytes()).digest():
            assert name in IMPORT_CHANGES, f"Unexpected import modification: {name}"
            changed.append(name)
        if name.endswith(".java"):
            java_count += 1
    assert (ROOT / "docs/upstream-readme.md").read_bytes() == (source / "README.md").read_bytes()
    print(f"PASS: {len(names)} imported files, {java_count} unchanged Java files, {len(changed)} documented conversions")
    for name in changed:
        print(f"  converted: {name}")


def check_compose() -> None:
    # Docker Compose can parse arbitrary YAML inside x-* extension blocks.
    # Escape Spring placeholders so Compose does not attempt to interpolate them.
    resources = ROOT / "big-market-app/src/main/resources"
    for path in sorted(resources.glob("application*.yml")):
        original = path.read_text(encoding="utf-8").replace("$", "$$")
        wrapper = "x-spring-config:\n" + "\n".join("  " + line for line in original.splitlines())
        wrapper += "\nservices:\n  syntax-check:\n    image: scratch\n"
        run(["docker", "compose", "-f", "-", "config", "--quiet"], data=wrapper)
    raw = run(["docker", "compose", "-f", "docs/dev-ops/docker-compose-local.yml", "config", "--format", "json"])
    config = json.loads(raw)
    ports: set[tuple[str, str]] = set()
    for service in config["services"].values():
        for port in service.get("ports", []):
            address = (str(port["published"]), port.get("protocol", "tcp"))
            assert address not in ports, f"Port collision: {address}"
            assert port["host_ip"] == "127.0.0.1", "Local service exposed beyond loopback"
            ports.add(address)
        for volume in service.get("volumes", []):
            if volume["type"] == "bind":
                assert Path(volume["source"]).is_file(), f"Missing bind source: {volume['source']}"
    assert len(config["services"]) == 5
    print("PASS: 4 Spring YAML files, local Compose schema, unique ports and SQL mounts (no containers started)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, help="Optional read-only original repository")
    parser.add_argument("--compose", action="store_true", help="Parse YAML with Docker Compose; no daemon/start")
    options = parser.parse_args()
    try:
        check_structure()
        if options.source:
            check_import(options.source)
        if options.compose:
            check_compose()
    except (AssertionError, OSError, RuntimeError, ValueError, ET.ParseError, subprocess.TimeoutExpired) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print("Static checks only: compilation, service connectivity and business behavior remain unverified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
