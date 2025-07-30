# peak_autocorrect/core.py

import os, json, time
import numpy as np
import faiss
import onnxruntime as ort
from sklearn.preprocessing import MinMaxScaler
from rapidfuzz.distance import DamerauLevenshtein
from pythainlp.soundex import soundex

class PeakAutocorrectTH:
    def __init__(self, index_path='th_db_address.faiss'):
        self.index = faiss.read_index(index_path)
        self.session1 = ort.InferenceSession("vectorizer1.onnx")
        self.session2 = ort.InferenceSession("vectorizer2.onnx")
        with open("db_vocab.json", 'r', encoding='utf-8-sig') as f:
            self.doc = json.load(f)

    def key1(self, first: str):
        return f"{soundex(first)}"

    def onnx_inference(self, texts, session):
        input_name = session.get_inputs()[0].name
        inputs = {input_name: np.array(texts)}
        output_name = session.get_outputs()[0].name
        outputs = session.run([output_name], inputs)
        return outputs

    def embedding_onnx(self, query):
        query_vec = self.onnx_inference(query, self.session1)[0]
        query_phonetic = [self.key1(d) for d in query]
        phonetic_vec = self.onnx_inference(query_phonetic, self.session2)[0]
        lengths = np.array([[len(d)] for d in query], dtype='float32')
        scaler = MinMaxScaler()
        lengths_scaled = scaler.fit_transform(lengths)
        final = np.hstack([query_vec, lengths_scaled, phonetic_vec])
        return final

    def run(self, query, k=1):
        query_vec = self.embedding_onnx(query)
        start = time.time()
        distances, indices = self.index.search(query_vec, k)
        end = time.time()
        for n, indice in enumerate(indices):
            print(f"Top matches for: {query[n]}")
            for i, idx in enumerate(indice):
                print(f"- {self.doc[idx]} {distances[0][i]:.3f}")
        print(f"Inference time: {end - start:.4f} seconds")
