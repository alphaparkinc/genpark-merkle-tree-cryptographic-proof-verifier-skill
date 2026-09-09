"""Example usage for Merkle Tree Cryptographic Proof Skill."""
from client import MerkleTree

def main():
    print("Executing Merkle Tree Cryptographic Proof...")
    transactions = ["tx_transfer_01", "tx_mint_02", "tx_vote_03", "tx_deploy_04"]
    mt = MerkleTree(transactions)
    root = mt.root()
    print("Merkle Root:", root)

    target_idx = 2 # tx_vote_03
    proof = mt.get_proof(target_idx)
    print(f"Proof for '{transactions[target_idx]}':", proof)

    valid = MerkleTree.verify_proof(transactions[target_idx], proof, root)
    print("Proof validity:", valid)
    assert valid == True, "Verification failed"
    print("Merkle Tree Proof verified successfully!")

if __name__ == "__main__":
    main()
