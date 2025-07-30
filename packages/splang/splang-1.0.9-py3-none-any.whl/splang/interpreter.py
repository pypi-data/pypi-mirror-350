from .opcodes import OPCODES
from .errors import SplangError, SplangWarning, InvalidOpcodeWarning
import time
import warnings

class SplangInterpreter:
    """
    Interpreter for the Splang (Sound Playlist Esolang) language.

    Accepts a playlist as a list of dictionaries, each containing:
      - track_id (unique identifier)
      - duration_min ("mm:ss" string)
      - opcode (int 00-59)
      - last_second (int 0-9)
      - first_second (int 0-9)
      - first_letter (single character)
      - track_name (string)

    The list order defines the program sequence.
    """

    def __init__(self, playlist):
        self.playlist = playlist
        self.prev_pc = None
        self.pc = 0
        self.stack = []
        self.ra_stack = []
        self.heap = {}
        self.labels = {}
        self.running = True
        #Check if playlist had required fields
        for song in self.playlist:
            if not all(k in song for k in ['track_id', 'duration_min', 'opcode', 'last_second', 'first_second', 'first_letter']):
                raise ValueError(f"Missing required fields in song: {song}")
            
        # Process labels in the playlist
        self.process_labels()

    def run(self):
        """Run until HALT or out-of-bounds."""
        while self.running and 0 <= self.pc < len(self.playlist):
            self.step()
        return self

    
    def step(self):
        #print(f"PC={self.pc} stack={self.stack} ra_stack={self.ra_stack} heap={self.heap} labels={self.labels}")
        row = self.playlist[self.pc]
        cmd, param_count = OPCODES.get(row['opcode'], (None, 0))
        if cmd is None:
            #print(f"PC={self.pc} opcode={row['opcode']} row={row}")
            raise ValueError(f"Unknown opcode {row['opcode']} at PC={self.pc}")

        params = []
        for i in range(1, param_count + 1):
            idx = self.pc + i
            if idx >= len(self.playlist):
                raise IndexError(f"Not enough params at PC={self.pc}")
            params.append(self.playlist[idx])

        method = getattr(self, cmd.lower())
        self.prev_pc = self.pc
        jumped = method(params)
        if jumped is not True:
            self.pc = self.prev_pc + 1 + param_count
        #print(f"Executed {cmd} at PC={self.prev_pc}, jumped={jumped}, stack={self.stack}, ra_stack={self.ra_stack}, heap={self.heap}, labels={self.labels}", flush=True)
        return self._state()

    def _state(self):
        return {
            'pc': self.pc,
            'stack': list(self.stack),
            'ra_stack': list(self.ra_stack),
            'heap': dict(self.heap),
            'labels': dict(self.labels),
            'completed_pc' : self.prev_pc,
            'completed_id' : self.playlist[self.prev_pc]['track_id'] if self.prev_pc < len(self.playlist) else None,
            'completed_op': self.playlist[self.prev_pc]['opcode'] if self.prev_pc < len(self.playlist) else None,
            'next_pc': self.pc if self.pc < len(self.playlist) else None,
            'next_id': self.playlist[self.pc]['track_id'] if self.pc < len(self.playlist) else None,
            'next_op': self.playlist[self.pc]['opcode'] if self.pc < len(self.playlist) else None,
            'running': self.running
        }
    
    def process_labels(self):
        """Process labels in the playlist."""
        for i, song in enumerate(self.playlist):
            if song['opcode'] == 2:
                #Get the next track_id as label
                next_idx = i + 1
                if next_idx < len(self.playlist):
                    label_id = self.playlist[next_idx]['track_id']
                    self.labels[label_id] = next_idx + 1
                else:
                    raise IndexError(f"Label at PC={i} is missing a track_id for jump.")

    def heap_get(self, track_id):
        """Get value from heap by track_id."""
        if track_id in self.heap:
            return self.heap[track_id]
        else:
            raise KeyError(f"Track ID '{track_id}' not found in heap.")
        
    def heap_set(self, track_id, value):
        """Set value in heap by track_id."""
        self.heap[track_id] = value
        
    # === Instruction implementations ===
    def nop(self, params): pass
    def halt(self, params): self.running = False; return True
    def label(self, params): self.labels[params[0]['track_id']] = self.pc + 1 + len(params)
    def jump(self, params): self.pc = self.labels[params[0]['track_id']]; return True
    def jumpz(self, params):
        if self.stack and self.stack[-1] == 0:
            self.pc = self.labels[params[0]['track_id']]
            return True
    def jumpnz(self, params):
        if self.stack and self.stack[-1] != 0:
            self.pc = self.labels[params[0]['track_id']]
            return True
    def jumpz_heap(self, params):
        if self.heap_get(params[0]['track_id']) == 0:
            self.pc = self.labels[params[0]['track_id']]
            return True
    def jumpnz_heap(self, params):
        if self.heap_get(params[0]['track_id']) != 0:
            self.pc = self.labels[params[0]['track_id']]
            return True
    def call(self, params):
        self.ra_stack.append(self.pc + 1 + len(params))
        self.pc = self.labels[params[0]['track_id']]
        return True
    def return_(self, params):
        if self.ra_stack:
            self.pc = self.ra_stack.pop()
            return True
        self.running = False
    def add(self, params): a,b = self.stack.pop(), self.stack.pop(); self.stack.append(b+a)
    def sub(self, params): a,b = self.stack.pop(), self.stack.pop(); self.stack.append(b-a)
    def mul(self, params): a,b = self.stack.pop(), self.stack.pop(); self.stack.append(b*a)
    def div(self, params): a,b = self.stack.pop(), self.stack.pop(); self.stack.append(b//a)
    def mod(self, params): a,b = self.stack.pop(), self.stack.pop(); self.stack.append(b%a)
    def pow(self, params): a,b = self.stack.pop(), self.stack.pop(); self.stack.append(b**a)
    def not_implemented(self, params): warnings.warn(InvalidOpcodeWarning(f"Opcode {self.playlist[self.pc]['opcode']} not implemented @ PC={self.pc}"))
    def push_ls(self, params): self.stack.append(int(params[0]['last_second']))
    def push_fs(self, params): self.stack.append(int(params[0]['first_second']))
    def shift_r_ls(self, params): a=self.stack.pop(); self.stack.append((a>>int(params[0]['last_second'])) + int(params[0]['last_second']))
    def shift_l_ls(self, params): a=self.stack.pop(); self.stack.append((a<<int(params[0]['last_second'])) + int(params[0]['last_second']))
    def shift_r_fs(self, params): a=self.stack.pop(); self.stack.append((a>>int(params[0]['first_second'])) + int(params[0]['first_second']))
    def shift_l_fs(self, params): a=self.stack.pop(); self.stack.append((a<<int(params[0]['first_second'])) + int(params[0]['first_second']))
    def pop(self, params): self.stack.pop()
    def dup(self, params): self.stack.append(self.stack[-1])
    def swap(self, params): a,b=self.stack.pop(),self.stack.pop(); self.stack.extend([a,b])
    def store(self, params): self.heap_set(params[0]['track_id'], self.stack.pop())
    def store_top(self, params): val=self.stack.pop(); addr=self.stack.pop(); self.heap[addr] = val
    def load(self, params): self.stack.append(self.heap_get(params[0]['track_id']))
    def load_top(self, params): addr=self.stack.pop(); self.stack.append(self.heap.get(addr, 0))
    def inc_heap(self, params): self.heap_set(params[0]['track_id'], self.heap_get(params[0]['track_id']) + 1)
    def dec_heap(self, params): self.heap_set(params[0]['track_id'], self.heap_get(params[0]['track_id']) - 1)
    def inc(self, params): self.stack.append(self.stack.pop() + 1)
    def dec(self, params): self.stack.append(self.stack.pop() - 1)
    def stdin_int(self, params): val=int(input()); self.stack.append(val)
    def stdin(self, params): s=input(); [self.stack.append(ord(ch)) for ch in s]
    def stdout_int(self, params): print(self.stack.pop())
    def stdout(self, params): print(chr(self.stack.pop()), end='')
    def read_char(self, params): self.stack.append(ord(params[0]['first_letter']))
    def listen(self, params): time.sleep(int(params[0]['duration_min'].split(':')[0]) * 60 + int(params[0]['duration_min'].split(':')[1]))
    def and_(self, params): a,b=self.stack.pop(),self.stack.pop(); self.stack.append(b&a)
    def or_(self, params): a,b=self.stack.pop(),self.stack.pop(); self.stack.append(b|a)
    def xor(self, params): a,b=self.stack.pop(),self.stack.pop(); self.stack.append(b^a)
    def not_(self, params): a=self.stack.pop(); self.stack.append(~a)
    def equal(self, params): a,b=self.stack.pop(),self.stack.pop(); self.stack.append(1 if b==a else 0)
    def not_equal(self, params): a,b=self.stack.pop(),self.stack.pop(); self.stack.append(1 if b!=a else 0)
    def greater(self, params): a,b=self.stack.pop(),self.stack.pop(); self.stack.append(1 if b>a else 0)
    def less(self, params): a,b=self.stack.pop(),self.stack.pop(); self.stack.append(1 if b<a else 0)
    def greater_equal(self, params): a,b=self.stack.pop(),self.stack.pop(); self.stack.append(1 if b>=a else 0)
    def less_equal(self, params): a,b=self.stack.pop(),self.stack.pop(); self.stack.append(1 if b<=a else 0)