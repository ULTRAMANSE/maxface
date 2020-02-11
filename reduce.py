# coding = utf-8
import numpy as np
import io
import zlib
import sqlite3


def reduce_data(face_arr):
    out = io.BytesIO()
    np.savez(out, face_arr)
    out.seek(0)
    data = out.read()
    return sqlite3.Binary(zlib.compress(data, zlib.Z_BEST_COMPRESSION))  # 对数据进行压缩并返回二进制数据


def decompress_data(face_arr):
    out = io.BytesIO(face_arr)
    out.seek(0)
    data = out.read()
    out2 = io.BytesIO(zlib.decompress(data))  # 解压
    return np.load(out2)
