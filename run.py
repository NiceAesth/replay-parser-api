import gevent.monkey; gevent.monkey.patch_all()
from bottle import run, post, request
from osrparse import parse_replay
import base64
import codecs
import json
import os
 
def hexToStr(hex):
    if ord(hex) >= ord('a'):
        return ord(hex) - ord('a') + 10
    return ord(hex) - ord('0')
 
def convert(s):
    new_str = b''
    i = 0
    while i < len(s):
        if s[i] == '\\' and s[i + 1] == 'x':
            new_str += bytes([hexToStr(s[i + 2]) * 16 + hexToStr(s[i + 3])])
            i += 3
        elif s[i] == '\\' and s[i + 1] == 't':
            new_str += bytes([ord('\t')])
            i += 1
        elif s[i] == '\\' and s[i + 1] == 'n':
            new_str += bytes([ord('\n')])
            i += 1
        elif s[i] == '\\' and s[i + 1] == 'r':
            new_str += bytes([ord('\r')])
            i += 1
        elif s[i] == '\\' and s[i + 1] == '\\':
            new_str += bytes([ord('\\')])
            i += 1
        elif s[i] == '\\' and s[i + 1] == '\'':
            new_str += bytes([ord('\'')])
            i += 1
        else:
            new_str += bytes([ord(s[i])])
        i += 1
    return new_str
 
def serializeMods(mods):
    result = []
    for mod in mods:
        result.append(mod.name)
    return result
 
@post('/replay')
def parseReplay():
    byte_string = request.body.read()
 
    byte_string = convert(byte_string.decode("ANSI"))
 
    replay = parse_replay(byte_string)
 
    response = {
        'beatmap_hash': replay.replay_hash,
        'replay_hash': replay.replay_hash,
        'score': replay.score,
        'gekis': replay.gekis,
        'katus': replay.katus,
        'max_combo': replay.max_combo,
        'misses': replay.misses,
        'number_50s': replay.number_50s,
        'number_100s': replay.number_100s,
        'number_300s': replay.number_300s,
        'is_perfect_combo': replay.is_perfect_combo,
        'player_name': replay.player_name,
        'mod_combination': serializeMods(replay.mod_combination)
    }
 
    return json.dumps(response)
 
 
run(reLoader=True, server='gevent', port=int(os.environ.get('PORT', 5000)), host='0.0.0.0')