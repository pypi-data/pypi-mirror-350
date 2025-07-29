# LEGAL
"""
COPYRIGHT 2024 PYTHON SOFTWARE FOUNDATION.
ALL RIGHTS RESERVED.

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public License as published
by the Free Software Foundation; either version 2.1 of the License, or (at your
option) any later version.

This library is distributed AS IS,
WITHOUT ANY WARRANTY implied or otherwise; 
without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
See the GNU Lesser General Public License 
for more details.

You should have received a copy of the GNU Lesser General Public License along
with this library; if not, see <https://www.gnu.org/licenses/>.
"""

# Copyright (c) 2001-2024 Python Software Foundation.
# All Rights Reserved.
# struct3 by Loic M.Herry
# LEGAL
# -----------------

# Detect Python version (py_version==2 for Python 2.7, 3 for Python 3)
py_version = 2  # fallback to Python 2
try:
    unicode
    py_version = 2
except NameError:
    py_version = 3
    unicode = str  # define unicode in Python 3

import os

#----------------------------------------------------------------
# Unified integer-to-bytes and bytes-to-integer functions.
if py_version == 2:
    def int_to_bytes(n, length, byteorder='big', signed=False):
        if signed and n < 0:
            n += 1 << (length * 8)
        result = []
        if byteorder == 'big':
            for i in range(length-1, -1, -1):
                result.append(chr((n >> (8 * i)) & 0xff))
        else:
            for i in range(length):
                result.append(chr((n >> (8 * i)) & 0xff))
        return ''.join(result)

    def int_from_bytes(b, byteorder='big', signed=False):
        n = 0
        length = len(b)
        if byteorder == 'big':
            for i in range(length):
                n = (n << 8) | ord(b[i])
        else:
            for i in range(length-1, -1, -1):
                n = (n << 8) | ord(b[i])
        if signed:
            sign_bit = 1 << (8 * length - 1)
            if n & sign_bit:
                n -= 1 << (8 * length)
        return n
else:
    def int_to_bytes(n, length, byteorder='big', signed=False):
        return n.to_bytes(length, byteorder, signed=signed)
    def int_from_bytes(b, byteorder='big', signed=False):
        return int.from_bytes(b, byteorder, signed=signed)

def _get_byte(b):
    if py_version == 2:
        return ord(b)
    else:
        return b

#----------------------------------------------------------------
def _get_byte_order(fmt):
    if fmt and fmt[0] in '@=<>!':
        return fmt[0], fmt[1:]
    return '@', fmt

def _swap_bytes(data, size):
    if size <= 1:
        return data
    pieces = []
    for i in range(0, len(data), size):
        pieces.append(data[i:i+size][::-1])
    if py_version == 3:
        return b''.join(pieces)
    else:
        return ''.join(pieces)

def _get_alignment(ch):
    if ch in 'xcbB?':
        return 1
    elif ch in 'hH':
        return 2
    elif ch in 'iIlLf':
        return 4
    elif ch in 'qQdP':
        return 8
    elif ch == 'e':
        return 2
    elif ch in 'sSp':
        return 1
    else:
        raise ValueError("Unsupported format character for alignment: " + ch)

def _get_size(ch, field_size=None):
    if ch == 'x':
        return 1
    elif ch == 'c':
        return 1
    elif ch in 'bB':
        return 1
    elif ch == '?':
        return 1
    elif ch in 'hH':
        return 2
    elif ch in 'iIlLnN':
        return 4
    elif ch in 'qQ':
        return 8
    elif ch == 'e':
        return 2
    elif ch == 'f':
        return 4
    elif ch == 'd':
        return 8
    elif ch in 's':
        if field_size is None:
            raise ValueError("Field width required for s format")
        return field_size
    elif ch in 'p':
        if field_size is None:
            raise ValueError("Field width required for p format")
        return field_size
    elif ch == 'P':
        return 8
    else:
        raise ValueError("Unsupported format character: " + ch)

def _pack_ieee754(value, bits, exp_bits, frac_bits):
    bias = (1 << (exp_bits - 1)) - 1
    if value != value:  # NaN
        sign, E, frac = 0, (1 << exp_bits) - 1, 1
    elif value == float('inf'):
        sign, E, frac = 0, (1 << exp_bits) - 1, 0
    elif value == float('-inf'):
        sign, E, frac = 1, (1 << exp_bits) - 1, 0
    else:
        sign = 0
        if value < 0:
            sign = 1
        abs_value = value if value >= 0 else -value
        if abs_value == 0.0:
            E, frac = 0, 0
        else:
            h = abs_value.hex()
            if h.startswith("0x1."):
                parts = h.split("p")
                exp = int(parts[1])
                frac_hex = parts[0][len("0x1."):]
                # Force float division in Python2:
                m = 1.0 + (float(int(frac_hex, 16)) / (16 ** len(frac_hex))) if frac_hex else 1.0
            else:
                parts = h.split("p")
                exp = int(parts[1])
                frac_hex = h[h.find(".")+1:h.find("p")]
                m = (float(int(frac_hex, 16)) / (16 ** len(frac_hex))) if frac_hex else 0.0
            E_target = exp + bias
            if E_target <= 0:
                E = 0
                frac = int(round(abs_value / (2 ** (1 - bias)) * (2 ** frac_bits)))
                if frac >= (1 << frac_bits):
                    frac = (1 << frac_bits) - 1
            elif E_target >= (1 << exp_bits) - 1:
                E, frac = (1 << exp_bits) - 1, 0
            else:
                E = E_target
                frac = int(round((m - 1.0) * (2 ** frac_bits)))
                if frac == (1 << frac_bits):
                    frac, E = 0, E + 1
                    if E >= (1 << exp_bits) - 1:
                        E, frac = (1 << exp_bits) - 1, 0
    bits_value = (sign << (bits - 1)) | (E << frac_bits) | frac
    if py_version == 3:
        return bytes([(bits_value >> (bits - 8 * (i + 1))) & 0xff for i in range(bits // 8)])
    else:
        return ''.join(chr((bits_value >> (bits - 8 * (i + 1))) & 0xff) for i in range(bits // 8))

def _unpack_ieee754(data, bits, exp_bits, frac_bits):
    bits_value = 0
    for b in data:
        if py_version == 2:
            bits_value = (bits_value << 8) | ord(b)
        else:
            bits_value = (bits_value << 8) | b
    sign = bits_value >> (bits - 1)
    E = (bits_value >> frac_bits) & ((1 << exp_bits) - 1)
    frac = bits_value & ((1 << frac_bits) - 1)
    bias = (1 << (exp_bits - 1)) - 1
    if E == 0:
        if frac == 0:
            return -0.0 if sign else 0.0
        m = float(frac) / (2 ** frac_bits)
        exp = 1 - bias
    elif E == (1 << exp_bits) - 1:
        if frac == 0:
            return float('-inf') if sign else float('inf')
        else:
            return float('nan')
    else:
        m = 1 + float(frac) / (2 ** frac_bits)
        exp = E - bias
    value = m * (2 ** exp)
    return -value if sign else value

#----------------------------------------------------------------
def pack(fmt, *values):
    byte_order, fmt = _get_byte_order(fmt)
    if byte_order == '@':
        native_align = True
        native_little = (int_to_bytes(1, 2, 'little') == (b'\x01\x00' if py_version == 3 else '\x01\x00'))
        little_endian = native_little
    elif byte_order == '<':
        native_align = False; little_endian = True
    elif byte_order in ('>', '!'):
        native_align = False; little_endian = False
    elif byte_order == '=':
        native_align = False
        native_little = (int_to_bytes(1, 2, 'little') == (b'\x01\x00' if py_version == 3 else '\x01\x00'))
        little_endian = native_little
    else:
        native_align = False; little_endian = True

    result = bytearray()
    value_index = 0
    i = 0
    while i < len(fmt):
        rep = 0
        while i < len(fmt) and fmt[i].isdigit():
            rep = rep * 10 + int(fmt[i])
            i += 1
        if rep == 0: rep = 1
        if i >= len(fmt): break
        ch = fmt[i]; i += 1
        if ch in 'sp':
            field_size = rep; rep = 1
        else:
            field_size = None
        for r in range(rep):
            if native_align:
                align = _get_alignment(ch)
                pad = (align - (len(result) % align)) % align
                if pad:
                    result.extend(b'\x00' * pad)
            if ch == 'x':
                result.extend(b'\x00')
            elif ch == 'c':
                value = values[value_index]; value_index += 1
                if isinstance(value, unicode):
                    value = value.encode('utf-8')
                if py_version == 3:
                    if isinstance(value, (bytes, bytearray)):
                        if len(value) != 1:
                            raise ValueError("c format requires a one-byte object")
                        value = value[0]
                    elif isinstance(value, str):
                        if len(value) != 1:
                            raise ValueError("c format requires a single character")
                        value = ord(value)
                    else:
                        value = int(value)
                else:
                    if isinstance(value, unicode):
                        pass
                    if isinstance(value, str):
                        if len(value) != 1:
                            raise ValueError("c format requires a one-byte string")
                    else:
                        value = chr(int(value))
                    value = ord(value)
                result.append(value & 0xFF)
            elif ch in 'bB':
                value = int(values[value_index]); value_index += 1
                result.extend(int_to_bytes(value, 1, 'little', signed=(ch=='b')))
            elif ch == '?':
                value = bool(values[value_index]); value_index += 1
                result.append(1 if value else 0)
            elif ch in 'hH':
                value = int(values[value_index]); value_index += 1
                num_bytes = 2
                result.extend(int_to_bytes(value, num_bytes, ('little' if little_endian else 'big'),
                                             signed=(ch=='h')))
            elif ch in 'iIlLnN':
                value = int(values[value_index]); value_index += 1
                num_bytes = 4
                result.extend(int_to_bytes(value, num_bytes, ('little' if little_endian else 'big'),
                                             signed=(ch in 'iln')))
            elif ch in 'qQ':
                value = int(values[value_index]); value_index += 1
                num_bytes = 8
                result.extend(int_to_bytes(value, num_bytes, ('little' if little_endian else 'big'),
                                             signed=(ch=='q')))
            elif ch == 'e':
                value = values[value_index]; value_index += 1
                num_bytes = 2
                bytes_value = _pack_ieee754(value, 16, 5, 10)
                if little_endian: bytes_value = bytes_value[::-1]
                result.extend(bytes_value)
            elif ch == 'f':
                value = values[value_index]; value_index += 1
                num_bytes = 4
                bytes_value = _pack_ieee754(value, 32, 8, 23)
                if little_endian: bytes_value = bytes_value[::-1]
                result.extend(bytes_value)
            elif ch == 'd':
                value = values[value_index]; value_index += 1
                num_bytes = 8
                bytes_value = _pack_ieee754(value, 64, 11, 52)
                if little_endian: bytes_value = bytes_value[::-1]
                result.extend(bytes_value)
            elif ch == 's':
                value = values[value_index]; value_index += 1
                if isinstance(value, unicode):
                    value = value.encode('utf-8')
                size_field = _get_size(ch, field_size)
                result.extend(value[:size_field].ljust(size_field, b'\x00'))
            elif ch == 'p':
                value = values[value_index]; value_index += 1
                if isinstance(value, unicode):
                    value = value.encode('utf-8')
                size_field = _get_size(ch, field_size)
                length = min(len(value), size_field - 1) if size_field > 0 else 0
                result.append(length)
                result.extend(value[:length].ljust(size_field - 1, b'\x00'))
            elif ch == 'P':
                value = int(values[value_index]); value_index += 1
                num_bytes = 8
                result.extend(int_to_bytes(value, num_bytes, ('little' if little_endian else 'big'), signed=False))
            else:
                raise ValueError("Unsupported format character: " + ch)
    return bytes(result) if py_version == 3 else str(result)

def unpack(fmt, data):
    byte_order, fmt = _get_byte_order(fmt)
    if byte_order == '@':
        native_align = True
        native_little = (int_to_bytes(1, 2, 'little') == (b'\x01\x00' if py_version == 3 else '\x01\x00'))
        little_endian = native_little
    elif byte_order == '<':
        native_align = False; little_endian = True
    elif byte_order in ('>', '!'):
        native_align = False; little_endian = False
    elif byte_order == '=':
        native_align = False
        native_little = (int_to_bytes(1, 2, 'little') == (b'\x01\x00' if py_version == 3 else '\x01\x00'))
        little_endian = native_little
    else:
        native_align = False; little_endian = True

    result = []
    data_index = 0
    i = 0
    while i < len(fmt):
        rep = 0
        while i < len(fmt) and fmt[i].isdigit():
            rep = rep * 10 + int(fmt[i])
            i += 1
        if rep == 0: rep = 1
        if i >= len(fmt): break
        ch = fmt[i]; i += 1
        if ch in 'sp':
            field_size = rep; rep = 1
        else:
            field_size = None
        for r in range(rep):
            if native_align:
                align = _get_alignment(ch)
                pad = (align - (data_index % align)) % align
                data_index += pad
            if ch == 'x':
                data_index += 1
            elif ch == 'c':
                result.append(data[data_index:data_index+1])
                data_index += 1
            elif ch in 'bB':
                b = _get_byte(data[data_index])
                if ch == 'b' and b >= 128:
                    b -= 256
                result.append(b)
                data_index += 1
            elif ch == '?':
                result.append(bool(_get_byte(data[data_index])))
                data_index += 1
            elif ch in 'hH':
                num_bytes = 2
                bts = data[data_index:data_index+num_bytes]
                if not little_endian: bts = bts[::-1]
                result.append(int_from_bytes(bts, 'little', signed=(ch=='h')))
                data_index += num_bytes
            elif ch in 'iIlLnN':
                num_bytes = 4
                bts = data[data_index:data_index+num_bytes]
                if not little_endian: bts = bts[::-1]
                result.append(int_from_bytes(bts, 'little', signed=(ch in 'iln')))
                data_index += num_bytes
            elif ch in 'qQ':
                num_bytes = 8
                bts = data[data_index:data_index+num_bytes]
                if not little_endian: bts = bts[::-1]
                result.append(int_from_bytes(bts, 'little', signed=(ch=='q')))
                data_index += num_bytes
            elif ch == 'e':
                num_bytes = 2
                bts = data[data_index:data_index+num_bytes]
                if little_endian: bts = bts[::-1]
                result.append(_unpack_ieee754(bts, 16, 5, 10))
                data_index += num_bytes
            elif ch == 'f':
                num_bytes = 4
                bts = data[data_index:data_index+num_bytes]
                if little_endian: bts = bts[::-1]
                result.append(_unpack_ieee754(bts, 32, 8, 23))
                data_index += num_bytes
            elif ch == 'd':
                num_bytes = 8
                bts = data[data_index:data_index+num_bytes]
                if little_endian: bts = bts[::-1]
                result.append(_unpack_ieee754(bts, 64, 11, 52))
                data_index += num_bytes
            elif ch == 's':
                size_field = _get_size(ch, field_size)
                result.append(data[data_index:data_index+size_field])
                data_index += size_field
            elif ch == 'p':
                size_field = _get_size(ch, field_size)
                length = _get_byte(data[data_index])
                result.append(data[data_index+1:data_index+size_field][:length])
                data_index += size_field
            elif ch == 'P':
                num_bytes = 8
                bts = data[data_index:data_index+num_bytes]
                if not little_endian: bts = bts[::-1]
                result.append(int_from_bytes(bts, 'little', signed=False))
                data_index += num_bytes
            else:
                raise ValueError("Unsupported format character: " + ch)
    return tuple(result)
