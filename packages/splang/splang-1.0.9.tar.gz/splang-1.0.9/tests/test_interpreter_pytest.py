import pytest
import warnings
from splang.interpreter import SplangInterpreter
from splang.errors import SplangError, SplangWarning, InvalidOpcodeWarning

@ pytest.fixture
def song_factory():
     def make_song(track_id='~', duration_min="0:00", first_letter='~'):
        """
            Create a testing song with the required fields:
            - track_id (string)
            - opcode (int 0-59)
            - last_second (int 0-9)
            - first_second (int 0-5)
            - first_letter (single character)
            - duration_min (string in format "mm:ss")
        """
        if not isinstance(track_id, str):
            raise TypeError("track_id must be a string")
        if not isinstance(first_letter, str) or len(first_letter) != 1:
            raise ValueError("first_letter must be a single character string")
        #Check split duration_min into minutes and seconds
        if not isinstance(duration_min, str) or not (
            len(duration_min.split(':')) == 2 and
            all(part.isdigit() for part in duration_min.split(':')) and
            0 <= int(duration_min.split(':')[1]) < 60
        ):
            raise ValueError("duration_min must be a string in format 'mm:ss' with valid minutes and seconds")
        last_second = int(duration_min.split(':')[1]) % 10
        first_second = int(duration_min.split(':')[1]) // 10
        opcode = 10 * first_second + last_second
        return {
            'track_id': track_id,
            'opcode': opcode,
            'last_second': last_second,
            'first_second': first_second,
            'first_letter': first_letter,
            'duration_min': duration_min
        }
     return make_song


def test_nop_and_halt(song_factory):
    # NOP then HALT
    p = [ song_factory(duration_min="0:00"), # NOP
          song_factory(duration_min="0:01"), # HALT
          song_factory('s1', "0:20"),  # PUSH_LS
          song_factory('p1', "0:04"),  # param1 with last_second 4
        ]
    #print(p)
    interp = SplangInterpreter(p)
    interp.run()
    assert not interp.running
    assert interp.pc == 1  # Should stop at HALT
    assert interp.stack == []  # Stack should be empty after HALT


def test_push_ls_and_add(song_factory):
    p = []
    p.append(song_factory('s0', "0:20")) # PUSH_LS
    p.append(song_factory('p1', "0:02"))  # param1 with last_second 2
    p.append(song_factory('s1', "0:20")) # PUSH_LS
    p.append(song_factory('p2', "0:03"))  # param2 with last_second 3
    p.append(song_factory('s2', "0:10")) # ADD
    p.append(song_factory('s3', "0:01")) # HALT
    interp = SplangInterpreter(p)
    interp.run()
    assert interp.stack == [5]



def test_store_and_load_heap(song_factory):
    p = []
    key = 'keytrack'
    p.append(song_factory('s0', "0:20"))  # PUSH_LS
    p.append(song_factory('p1', "0:04"))  # param1 with last_second 4
    p.append(song_factory('s1', "0:30"))  # STORE
    p.append(song_factory(key, "0:00"))  # key track
    p.append(song_factory('s2', "0:32"))  # LOAD
    p.append(song_factory(key, "0:00"))  # key track
    p.append(song_factory('s3', "0:01"))  # HALT
    interp = SplangInterpreter(p)
    interp.run()
    assert interp.stack == [4]


def test_undef_opcode_raises(song_factory):
    """
    Test that an undefined opcode raises a ValueError.
    """
    p = [
         song_factory('s1', "0:16"),  # Undefined opcode
    ]
    interp = SplangInterpreter(p)
    # assert runs without raising an error
    with pytest.warns(InvalidOpcodeWarning):
        interp.run()

def test_unknown_opcode_raises(song_factory):
    """
    Test that an unknown opcode raises a ValueError.
    """
    p = [
         song_factory('s1', "0:01"),  # Defined opcode
    ]
    p[0]['opcode'] = 99  # Unknown opcode
    interp = SplangInterpreter(p)
    with pytest.raises(ValueError):
        interp.run()

def test_unknown_heap_key_raises(song_factory):
    """
    Test that trying to load a non-existent heap key raises a KeyError.
    """
    p = [
            song_factory('s1', "0:20"),  # PUSH_LS
            song_factory('p1', "0:04"),  # param1 with last_second 4
            song_factory('s2', "0:32"),  # LOAD
            song_factory('nonexistent_key', "0:00"),  # Non-existent key
            song_factory('s3', "0:01")   # HALT
        ]
    interp = SplangInterpreter(p)
    with pytest.raises(KeyError):
        interp.run()

def test_jump_to_label(song_factory):
    """
    Test that jumping to a label works correctly.
    """
    p = [
        song_factory('s1', "0:03"),  # JUMP
        song_factory('label1', "0:00"),  # param1 with track_id = 'label1'
        song_factory('s2', "0:01"),  # HALT
        song_factory('s3', "0:02"),  # LABEL
        song_factory('label1', "0:00"),  # param1 with track_id = 'label1'
        song_factory('s4', "0:20"),  # PUSH_LS
        song_factory('p1', "0:04"),  # param1 with last_second 4
        song_factory('s5', "0:01")   # HALT
    ]
    interp = SplangInterpreter(p)
    interp.run()
    assert interp.stack == [4]