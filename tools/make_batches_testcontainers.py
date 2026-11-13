#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Split the pages of java.testcontainers.org into translation batches.

Writes .work/batches.json: a list of batches, each with the prose parts it
covers, so the work can be handed to parallel translators.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (name, [slug prefixes]) - pages are matched by prefix, longest first
GROUPS = [
    ("root-a", [""]),
    ("root-b", ["contributing", "contributing_docs", "error_missing_container_runtime_environment",
                "examples", "getting_help", "jitpack_dependencies"]),
    ("features-a", ["features/advanced_options", "features/commands", "features/configuration",
                    "features/container_logs", "features/creating_container"]),
    ("features-b", ["features/creating_images", "features/files", "features/image_name_substitution",
                    "features/jib", "features/networking", "features/reuse", "features/startup_and_waits"]),
    ("databases-a", ["modules/databases/cassandra", "modules/databases/clickhouse",
                     "modules/databases/cockroachdb", "modules/databases/couchbase",
                     "modules/databases/cratedb", "modules/databases/databend",
                     "modules/databases/db2", "modules/databases/influxdb", "modules/databases/jdbc",
                     "modules/databases/mariadb"]),
    ("databases-b", ["modules/databases/mongodb", "modules/databases/mssqlserver",
                     "modules/databases/mysql", "modules/databases/neo4j",
                     "modules/databases/oceanbase", "modules/databases/oraclefree",
                     "modules/databases/oraclexe", "modules/databases/orientdb",
                     "modules/databases/postgres", "modules/databases/presto"]),
    ("databases-c", ["modules/databases/questdb", "modules/databases/r2dbc",
                     "modules/databases/scylladb", "modules/databases/tidb",
                     "modules/databases/timeplus", "modules/databases/trino",
                     "modules/databases/yugabytedb", "modules/databases"]),
    ("modules-a", ["modules/activemq", "modules/azure", "modules/chromadb", "modules/consul",
                   "modules/docker_compose", "modules/docker_mcp_gateway",
                   "modules/docker_model_runner", "modules/elasticsearch", "modules/gcloud",
                   "modules/grafana"]),
    ("modules-b", ["modules/hivemq", "modules/k3s", "modules/k6", "modules/kafka", "modules/ldap",
                   "modules/localstack", "modules/milvus", "modules/minio", "modules/mockserver",
                   "modules/nginx", "modules/ollama", "modules/openfga"]),
    ("modules-c", ["modules/pinecone", "modules/pulsar", "modules/qdrant", "modules/rabbitmq",
                   "modules/redpanda", "modules/solace", "modules/solr", "modules/toxiproxy",
                   "modules/typesense", "modules/vault", "modules/weaviate",
                   "modules/webdriver_containers"]),
    ("quickstart", ["quickstart"]),
    ("test-framework", ["test_framework_integration"]),
    ("system-req", ["supported_docker_environment"]),
]


def main():
    index = json.load(open(os.path.join(ROOT, ".work", "index.json"), encoding="utf-8"))
    assigned = {}
    batches = []
    for name, prefixes in GROUPS:
        parts, slugs = [], []
        for e in index:
            if e["slug"] in assigned:
                continue
            slug = e["slug"]
            for p in prefixes:
                if p == "":
                    hit = slug == ""
                elif p.endswith("/"):
                    hit = slug.startswith(p)
                else:
                    hit = slug == p or slug.startswith(p + "/")
                if hit:
                    parts.extend(os.path.basename(x) for x in e["prose_parts"])
                    slugs.append(slug)
                    assigned[slug] = name
                    break
        batches.append({"name": name, "pages": slugs, "parts": parts})

    left = [e["slug"] for e in index if e["slug"] not in assigned]
    if left:
        raise SystemExit("unassigned pages: %s" % left)

    with open(os.path.join(ROOT, ".work", "batches.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(batches, f, ensure_ascii=False, indent=1)
    for b in batches:
        size = sum(os.path.getsize(os.path.join(ROOT, ".work", "prose", p)) for p in b["parts"])
        print("%-14s pages %2d parts %2d chars %6d" % (b["name"], len(b["pages"]), len(b["parts"]), size))


if __name__ == "__main__":
    main()
