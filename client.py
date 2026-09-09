"""
Autonomous Agent Merkle Tree Cryptographic Proof Skill
Pure Python Standard Library implementation using hashlib SHA-256.
"""
import hashlib
from typing import List, Tuple, Dict, Any

class MerkleTree:
    """
    Binary Merkle Tree with inclusion proof generation and verification.
    """
    def __init__(self, leaves: List[str]):
        self.raw_leaves = list(leaves)
        self.leaves = [self._hash(l) for l in leaves]
        self.levels = [self.leaves]
        self._build_tree()

    def _hash(self, val: str) -> str:
        return hashlib.sha256(val.encode("utf-8")).hexdigest()

    def _combine(self, h1: str, h2: str) -> str:
        return hashlib.sha256((h1 + h2).encode("utf-8")).hexdigest()

    def _build_tree(self):
        curr = self.leaves
        while len(curr) > 1:
            next_level = []
            for i in range(0, len(curr), 2):
                h1 = curr[i]
                h2 = curr[i + 1] if i + 1 < len(curr) else curr[i]
                next_level.append(self._combine(h1, h2))
            self.levels.append(next_level)
            curr = next_level

    def root(self) -> str:
        return self.levels[-1][0] if self.levels and self.levels[-1] else ""

    def get_proof(self, index: int) -> List[Tuple[str, str]]:
        proof = []
        curr_idx = index
        for lvl in self.levels[:-1]:
            is_right = (curr_idx % 2 == 1)
            sibling_idx = curr_idx - 1 if is_right else curr_idx + 1
            if sibling_idx < len(lvl):
                sibling_hash = lvl[sibling_idx]
            else:
                sibling_hash = lvl[curr_idx]
            proof.append(("left" if is_right else "right", sibling_hash))
            curr_idx //= 2
        return proof

    @staticmethod
    def verify_proof(leaf_data: str, proof: List[Tuple[str, str]], root: str) -> bool:
        curr = hashlib.sha256(leaf_data.encode("utf-8")).hexdigest()
        for direction, sib in proof:
            if direction == "left":
                curr = hashlib.sha256((sib + curr).encode("utf-8")).hexdigest()
            else:
                curr = hashlib.sha256((curr + sib).encode("utf-8")).hexdigest()
        return curr == root
