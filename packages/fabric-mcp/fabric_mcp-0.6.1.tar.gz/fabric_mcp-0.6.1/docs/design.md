# Fabric MCP Server: High-Level Design

## 1. Introduction

This document outlines a design for integrating the [Fabric framework](https://github.com/danielmiessler/fabric) (the open-source AI framework by Daniel Miessler, *not* Microsoft Fabric) with the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/). The goal is to allow MCP-compatible clients (like IDEs or chat interfaces) to use Fabric's capabilities—its patterns, models, and configurations—via a standalone MCP server.

This integration brings Fabric's prompt engineering strengths directly into LLM interaction environments.

### 1.1. Key Design Decisions & Open Questions

* **MCP Server Language/Library:** Choose a language (e.g., Go, Python) and library for the standalone MCP server. [DONE]

* **MCP Transport Layer:** Decide on initial transport mechanisms (e.g., stdio, WebSockets).
* **Streaming:** Detail how to proxy streaming responses from Fabric's REST API via the MCP server.
* **Variable/Attachment Handling:** Finalize passing complex inputs (variables, attachments) via MCP tool parameters.
* **Error Handling:** Define how Fabric errors propagate back via MCP.
* **Community Feedback:** Share this design with the Fabric and MCP communities.

## 2. Background Research

### 2.1. Fabric REST API (danielmiessler/fabric)

Fabric provides a REST API (Go/Gin) mirroring many CLI functions.

* **Serving:** Launched via `fabric --serve`.
* **Code Location:** Primarily in the `restapi/` directory.
* **Authentication:** Supports API key (`--api-key`).
* **Endpoints (Inferred):**
  * `/models/names` (GET): List models by vendor.
  * `/patterns` (GET): List patterns.
  * `/patterns/:name` (GET): Get pattern details.
  * `/strategies` (GET): List strategies.
  * `/chat` (POST): Execute a pattern.
  * `/config` (GET/PUT): Manage configuration.

### 2.2. Model Context Protocol (MCP)

MCP is an open standard for integrating LLM applications (Hosts/Clients) with tools/data sources (Servers).

* **Architecture:** Client-Server. Hosts (IDEs, etc.) contain Clients talking to Servers.
* **Purpose:** Standardize tool interaction, often keeping data local.
* **Discovery:** Clients use `list_tools()`.
* **Resources:**
  * Site: <https://modelcontextprotocol.io/>
  * GitHub: <https://github.com/modelcontextprotocol>
  * Spec (Latest): <https://modelcontextprotocol.io/specification/2025-03-26>

## 3. Proposed MCP Integration

### 3.1. Architecture

* **Fabric Role:** `fabric --serve` acts as the backend service via its REST API.
* **MCP Server Role:** A separate, standalone process implements the MCP spec.
* **Interaction:** MCP Server calls Fabric's REST API.
* **Implementation:** MCP Server (Go/Python) needs an HTTP client (for Fabric) and an MCP library (for clients).
* **Host/Client:** MCP Hosts connect to the standalone Fabric MCP Server.

### 3.2. Proposed MCP Tools

Exposed via `list_tools()`:

1. **`fabric_list_patterns`**
   * **Desc:** Lists available Fabric patterns.
   * **Maps to:** `fabric --listpatterns`, `/patterns`.
   * **Returns:** List of pattern names.

2. **`fabric_get_pattern_details`**
   * **Desc:** Retrieves content/metadata for a pattern.
   * **Params:** `pattern_name` (string, required).
   * **Maps to:** Reading `~/.config/fabric/patterns/<pattern_name>/system.md`, `/patterns/:name`.
   * **Returns:** System prompt (Markdown), metadata.

3. **`fabric_run_pattern`**
   * **Desc:** Executes a Fabric pattern.
   * **Params:**
     * `pattern_name` (string, required)
     * `input_text` (string, optional)
     * `model_name` (string, optional): Overrides default.
     * `temperature`, `top_p`, `presence_penalty`, `frequency_penalty` (float, optional)
     * `variables` (map[string]string, optional)
     * `stream` (boolean, optional, default: false): Stream output via MCP.
     * `attachments` (list[string], optional): File paths/URLs.
   * **Maps to:** `fabric -p <name> ...`, `/chat`.
   * **Returns:** LLM output (potentially streamed).

4. **`fabric_list_models`**
   * **Desc:** Lists configured models by vendor.
   * **Maps to:** `fabric --listmodels`, `/models/names`.
   * **Returns:** Structured list/map.

5. **`fabric_list_strategies`**
   * **Desc:** Lists available strategies.
   * **Maps to:** `fabric --liststrategies`, `/strategies`.
   * **Returns:** List of names/descriptions.

6. **`fabric_get_configuration`**
   * **Desc:** Retrieves current Fabric configuration.
   * **Maps to:** Reading config state, `/config`.
   * **Returns:** Key-value map of settings.

### 3.3. Implementation Details

* **MCP Server:** New standalone app (Go/Python).
* **MCP Library:** Required for MCP server protocol.
* **Fabric API Client:** HTTP client within MCP server.
* **Mapping:** Translate MCP requests <=> Fabric REST calls.
* **No Fabric Source Changes:** Avoids modifying core Fabric.
* **Streaming:** MCP server proxies streaming from Fabric API per MCP spec.

### 3.4. Authentication

Use Fabric's API key (`--api-key`). Configure MCP client with this key, potentially using MCP's authorization mechanisms.

## 4. Benefits

* **Seamless Integration:** Use Fabric patterns directly from MCP clients.
* **Enhanced Workflows:** Let IDE LLMs use Fabric's specialized prompts.
* **Standardization:** Adopts an open standard.
* **Leverages Existing Code:** Builds on Fabric's CLI/REST API.

## 5. Next Steps / Open Questions

* **MCP Library:** Research/evaluate Go/Python MCP server libraries or estimate build effort.
* **MCP Transport:** Decide initial transport support (stdio, WebSockets).
* **Streaming:** Detail technical approach for MCP streaming.
* **Variables/Attachments:** Finalize MCP parameter mapping.
* **Error Handling:** Define Fabric-to-MCP error propagation.
* **Feedback:** Share design with Fabric/MCP communities.
