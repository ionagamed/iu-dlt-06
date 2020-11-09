#!/usr/bin/env python
# example of proof of work algorithm

import hashlib
import time
from flask import Flask, request


app = Flask(__name__)
max_nonce = 2 ** 32  # 4 billion


help_text = """
You need to specify header and difficulty_bits as query parameters for this request.
<br>
For example: <a href="http://localhost:5000/?header=header_value&difficulty_bits=5">
http://localhost:5000/?header=header_value&difficulty_bits=5
</a>
""".strip()


@app.route('/', methods=["GET"])
def index():
    difficulty_bits = request.args.get("difficulty_bits")
    if not difficulty_bits:
        return help_text, 400

    header = request.args.get("header")
    if not header:
        return help_text, 400

    hash, nonce = proof_of_work(header, int(difficulty_bits))
    return f"hash: {hash}, nonce: {nonce}"


def proof_of_work(header, difficulty_bits):
    target = 2 ** (256-difficulty_bits)

    for nonce in range(max_nonce):
        hash_result = hashlib.sha256(f"{header}{nonce}".encode('utf-8')).hexdigest()

        if int(hash_result, 16) < target:
            print("Success with nonce %d" % nonce)
            print("Hash is %s" % hash_result)
            return hash_result, nonce

    msg = "Failed after %d (max_nonce) tries" % nonce
    print(msg)
    raise ValueError(msg)


if __name__ == "__main__":
    app.config["DEBUG"] = True
    app.run(host="0.0.0.0")


if __name__ != "__main__":
    nonce = 0
    hash_result = ""

    for difficulty_bits in range(32):
        difficulty = 2 ** difficulty_bits
        print()
        print("Difficulty: %ld (%d bits)" % (difficulty, difficulty_bits))
        print("Starting search...")
        start_time = time.time()
        new_block = "test block with transactions" + hash_result
        (hash_result, nonce) = proof_of_work(new_block, difficulty_bits)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print("Elapsed time: %.4f seconds" % elapsed_time)
        if elapsed_time > 0:
            hash_power = float(int(nonce)/elapsed_time)
            print("Hashing power: %ld hashes per second" % hash_power)
