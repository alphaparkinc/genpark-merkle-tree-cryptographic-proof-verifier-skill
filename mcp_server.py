"""MCP Server for Merkle Tree Cryptographic Proof Skill."""
import json
import sys
from client import MerkleTree

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")
            params = req.get("params", {})

            if method == "tools/list":
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "tools": [
                            {
                                "name": "build_merkle_tree",
                                "description": "Construct Merkle tree and get root & proofs",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "leaves": {"type": "array", "items": {"type": "string"}}
                                    },
                                    "required": ["leaves"]
                                }
                            },
                            {
                                "name": "verify_merkle_proof",
                                "description": "Verify leaf inclusion with Merkle proof",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "leaf": {"type": "string"},
                                        "proof": {"type": "array"},
                                        "root": {"type": "string"}
                                    },
                                    "required": ["leaf", "proof", "root"]
                                }
                            }
                        ]
                    }
                }
            elif method == "tools/call":
                name = params.get("name")
                args = params.get("arguments", {})
                if name == "build_merkle_tree":
                    mt = MerkleTree(args["leaves"])
                    out = {"root": mt.root(), "leaf_count": len(args["leaves"])}
                else:
                    valid = MerkleTree.verify_proof(args["leaf"], [tuple(p) for p in args["proof"]], args["root"])
                    out = {"valid": valid}
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(out)}]}
                }
            else:
                res = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}
            print(json.dumps(res), flush=True)
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            print(json.dumps(err), flush=True)

if __name__ == "__main__":
    main()
