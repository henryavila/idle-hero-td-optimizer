#!/usr/bin/env python3
"""Calculate static base values for Idle Hero TD hero synergies."""

from __future__ import annotations

import math
import struct
from pathlib import Path
from typing import Any

from capstone import CS_ARCH_ARM64, CS_MODE_ARM, Cs
from capstone.arm64 import ARM64_OP_FP, ARM64_OP_IMM, ARM64_OP_MEM, ARM64_OP_REG


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LIBIL2CPP_PATH = (
    PROJECT_ROOT
    / "IdleHeroTD-apk"
    / "apk_analysis"
    / "dados-brutos"
    / "extracted"
    / "split_config.arm64_v8a"
    / "lib"
    / "arm64-v8a"
    / "libil2cpp.so"
)

GET_SYNERGY_VALUE_BASE_ENTRY = 0x1B97708
GET_SYNERGY_VALUE_BASE_DONE = 0x1B97D5C
GET_SYNERGY_VALUE_INVALID = 0x1B97D2C
GET_SYNERGY_VALUE_BASE_END = 0x1B97D60

NON_PERCENT_EFFECT_BASES = {"skillDuration", "energyIncome"}
NEGATIVE_PERCENT_EFFECT_BASES = {"skillCd"}


class SynergyValueCalculator:
    """Tiny emulator for the static value-selection block in GetSynergyValue.

    The real method multiplies this base value by dynamic save/map/slot/account
    modifiers after address 0x1B97D5C. Those runtime modifiers are intentionally
    excluded here so the output is stable from the APK alone.
    """

    def __init__(self, lib_path: Path = LIBIL2CPP_PATH) -> None:
        self.lib_path = lib_path
        self.data = lib_path.read_bytes()
        self.segments = self._read_load_segments()
        self.instructions = self._read_instructions()

    def base_value(self, upgrade_id: int, synergy_num: int) -> int:
        raw = self.base_value_raw(upgrade_id, synergy_num)
        return round_half_up(raw)

    def base_value_raw(self, upgrade_id: int, synergy_num: int) -> float:
        regs: dict[str, int] = {}
        floats: dict[str, float] = {"s8": 0.0}
        flags = {"N": False, "Z": False, "C": False, "V": False}

        set_reg(regs, "w20", synergy_num)
        set_reg(regs, "w21", upgrade_id)

        pc = GET_SYNERGY_VALUE_BASE_ENTRY
        steps = 0
        while True:
            steps += 1
            if steps > 1000:
                raise RuntimeError("GetSynergyValue base emulator exceeded step limit")
            if pc == GET_SYNERGY_VALUE_BASE_DONE:
                return floats["s8"]
            if pc == GET_SYNERGY_VALUE_INVALID:
                return 0.0

            ins = self.instructions.get(pc)
            if ins is None:
                raise RuntimeError(f"Unsupported branch target in synergy value block: {pc:#x}")

            next_pc = pc + 4
            mnemonic = ins.mnemonic

            if mnemonic == "cmp":
                lhs = get_reg(regs, reg_name(ins, 0))
                rhs = operand_value(regs, ins, 1)
                set_flags_sub(flags, lhs, rhs)
            elif mnemonic == "sub":
                set_reg(regs, reg_name(ins, 0), get_reg(regs, reg_name(ins, 1)) - operand_value(regs, ins, 2))
            elif mnemonic == "subs":
                result = get_reg(regs, reg_name(ins, 1)) - operand_value(regs, ins, 2)
                set_reg(regs, reg_name(ins, 0), result)
                set_flags_sub(flags, get_reg(regs, reg_name(ins, 1)), operand_value(regs, ins, 2))
            elif mnemonic == "mov":
                set_reg(regs, reg_name(ins, 0), operand_value(regs, ins, 1))
            elif mnemonic in {"adr", "adrp"}:
                set_reg(regs, reg_name(ins, 0), operand_value(regs, ins, 1))
            elif mnemonic == "add":
                value = get_reg(regs, reg_name(ins, 1)) + shifted_operand_value(regs, ins, 2)
                set_reg(regs, reg_name(ins, 0), value)
            elif mnemonic == "lsr":
                set_reg(regs, reg_name(ins, 0), get_reg(regs, reg_name(ins, 1)) >> get_reg(regs, reg_name(ins, 2)))
            elif mnemonic == "ldrh":
                address = memory_address(regs, ins, 1)
                set_reg(regs, reg_name(ins, 0), self.read_u16(address))
            elif mnemonic == "ldr":
                dest = reg_name(ins, 0)
                address = memory_address(regs, ins, 1)
                if dest.startswith("s"):
                    floats[dest] = self.read_f32(address)
                else:
                    raise RuntimeError(f"Unexpected ldr target in synergy value block: {ins.op_str}")
            elif mnemonic == "fmov":
                dest = reg_name(ins, 0)
                source = ins.operands[1]
                if source.type == ARM64_OP_FP:
                    floats[dest] = float(source.fp)
                elif source.type == ARM64_OP_REG:
                    floats[dest] = struct.unpack("<f", struct.pack("<I", get_reg(regs, reg_name(ins, 1)) & 0xFFFFFFFF))[0]
                else:
                    raise RuntimeError(f"Unsupported fmov source: {ins.op_str}")
            elif mnemonic == "movi":
                floats["s8"] = 0.0
            elif mnemonic == "b":
                next_pc = branch_target(ins)
            elif mnemonic.startswith("b."):
                condition = mnemonic.split(".", 1)[1]
                if condition_holds(condition, flags):
                    next_pc = branch_target(ins)
            elif mnemonic == "tbz":
                value = get_reg(regs, reg_name(ins, 0))
                bit = operand_value(regs, ins, 1)
                if ((value >> bit) & 1) == 0:
                    next_pc = branch_target(ins, 2)
            elif mnemonic == "br":
                next_pc = get_reg(regs, reg_name(ins, 0))
            else:
                raise RuntimeError(f"Unsupported instruction in synergy value block: {ins.mnemonic} {ins.op_str}")

            pc = next_pc

    def read_u16(self, address: int) -> int:
        return struct.unpack_from("<H", self.data, self.vaddr_to_offset(address))[0]

    def read_f32(self, address: int) -> float:
        return struct.unpack_from("<f", self.data, self.vaddr_to_offset(address))[0]

    def vaddr_to_offset(self, address: int) -> int:
        for start, end, offset in self.segments:
            if start <= address < end:
                return offset + (address - start)
        raise KeyError(f"Virtual address not mapped in {self.lib_path}: {address:#x}")

    def _read_load_segments(self) -> list[tuple[int, int, int]]:
        e_phoff = struct.unpack_from("<Q", self.data, 32)[0]
        e_phentsize, e_phnum = struct.unpack_from("<HH", self.data, 54)
        segments: list[tuple[int, int, int]] = []
        for index in range(e_phnum):
            offset = e_phoff + index * e_phentsize
            p_type, _p_flags, p_offset, p_vaddr, _p_paddr, p_filesz, _p_memsz, _p_align = struct.unpack_from(
                "<IIQQQQQQ", self.data, offset
            )
            if p_type == 1:
                segments.append((p_vaddr, p_vaddr + p_filesz, p_offset))
        return segments

    def _read_instructions(self) -> dict[int, Any]:
        md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
        md.detail = True
        start_offset = self.vaddr_to_offset(GET_SYNERGY_VALUE_BASE_ENTRY)
        end_offset = self.vaddr_to_offset(GET_SYNERGY_VALUE_BASE_END)
        code = self.data[start_offset:end_offset]
        return {ins.address: ins for ins in md.disasm(code, GET_SYNERGY_VALUE_BASE_ENTRY)}


def effect_base_key(effect_key: str) -> str:
    if effect_key.endswith("_global"):
        return effect_key.removesuffix("_global")
    if effect_key.endswith("_personal"):
        return effect_key.removesuffix("_personal")
    return effect_key


def format_bonus_value(value: int, effect_key: str) -> str:
    base_key = effect_base_key(effect_key)
    if base_key in NON_PERCENT_EFFECT_BASES:
        return f"+{value}"
    sign = "-" if base_key in NEGATIVE_PERCENT_EFFECT_BASES else "+"
    return f"{sign}{value}%"


def round_half_up(value: float) -> int:
    if value >= 0:
        return int(math.floor(value + 0.5))
    return int(math.ceil(value - 0.5))


def reg_name(ins: Any, index: int) -> str:
    return ins.reg_name(ins.operands[index].reg)


def get_reg(regs: dict[str, int], name: str) -> int:
    if name in {"wzr", "xzr"}:
        return 0
    return regs.get(name, 0)


def set_reg(regs: dict[str, int], name: str, value: int) -> None:
    value &= 0xFFFFFFFFFFFFFFFF
    if name.startswith("w"):
        value &= 0xFFFFFFFF
        regs[name] = value
        regs[f"x{name[1:]}"] = value
    elif name.startswith("x"):
        regs[name] = value
        regs[f"w{name[1:]}"] = value & 0xFFFFFFFF
    else:
        regs[name] = value


def operand_value(regs: dict[str, int], ins: Any, index: int) -> int:
    operand = ins.operands[index]
    if operand.type == ARM64_OP_IMM:
        return int(operand.imm)
    if operand.type == ARM64_OP_REG:
        return get_reg(regs, ins.reg_name(operand.reg))
    raise RuntimeError(f"Unsupported operand value: {ins.mnemonic} {ins.op_str}")


def shifted_operand_value(regs: dict[str, int], ins: Any, index: int) -> int:
    operand = ins.operands[index]
    value = operand_value(regs, ins, index)
    if operand.shift.type:
        value <<= operand.shift.value
    return value


def memory_address(regs: dict[str, int], ins: Any, index: int) -> int:
    operand = ins.operands[index]
    if operand.type != ARM64_OP_MEM:
        raise RuntimeError(f"Expected memory operand: {ins.mnemonic} {ins.op_str}")
    address = get_reg(regs, ins.reg_name(operand.mem.base)) + operand.mem.disp
    if operand.mem.index:
        address += get_reg(regs, ins.reg_name(operand.mem.index)) << operand.shift.value
    return address


def branch_target(ins: Any, index: int = 0) -> int:
    return int(ins.operands[index].imm)


def set_flags_sub(flags: dict[str, bool], lhs: int, rhs: int) -> None:
    mask = 0xFFFFFFFF
    sign = 0x80000000
    lhs &= mask
    rhs &= mask
    result = (lhs - rhs) & mask
    flags["Z"] = result == 0
    flags["N"] = bool(result & sign)
    flags["C"] = lhs >= rhs
    flags["V"] = bool(((lhs ^ rhs) & (lhs ^ result) & sign) != 0)


def condition_holds(condition: str, flags: dict[str, bool]) -> bool:
    if condition == "eq":
        return flags["Z"]
    if condition == "ne":
        return not flags["Z"]
    if condition in {"hs", "cs"}:
        return flags["C"]
    if condition in {"lo", "cc"}:
        return not flags["C"]
    if condition == "hi":
        return flags["C"] and not flags["Z"]
    if condition == "ls":
        return (not flags["C"]) or flags["Z"]
    if condition == "gt":
        return (not flags["Z"]) and flags["N"] == flags["V"]
    if condition == "le":
        return flags["Z"] or flags["N"] != flags["V"]
    if condition == "lt":
        return flags["N"] != flags["V"]
    if condition == "ge":
        return flags["N"] == flags["V"]
    raise RuntimeError(f"Unsupported ARM64 branch condition: {condition}")
