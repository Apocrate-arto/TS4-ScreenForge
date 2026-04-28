# Screen Forge TS4
# Copyright (C) 2026 Apocrate_arto
# SPDX-License-Identifier: GPL-3.0-or-later
from pathlib import Path
import struct


class EntreePackage:
    def __init__(
        self,
        type_id,
        group_id,
        instance_id,
        offset,
        size,
        offset_pos=None,
        size_flags_pos=None,
        mem_size_pos=None,
        compressed=False,
    ):
        self.type_id = type_id
        self.group_id = group_id
        self.instance_id = instance_id
        self.offset = offset
        self.size = size
        self.offset_pos = offset_pos
        self.size_flags_pos = size_flags_pos
        self.mem_size_pos = mem_size_pos
        self.compressed = compressed


class ServicePackage:
    def __init__(self, chemin_package: str):
        self.chemin_package = Path(chemin_package)
        self.donnees = bytearray(self.chemin_package.read_bytes())
        self.entrees = []

    def lire_index(self):
        if self.donnees[:4] != b"DBPF":
            raise ValueError("Package DBPF invalide.")

        index_count = struct.unpack_from("<I", self.donnees, 36)[0]
        index_size = struct.unpack_from("<I", self.donnees, 44)[0]
        index_offset = struct.unpack_from("<I", self.donnees, 64)[0]

        if index_size != 4 + index_count * 32:
            raise ValueError(
                f"Format d'index non supporté: count={index_count}, size={index_size}"
            )

        curseur = index_offset + 4

        for _ in range(index_count):
            type_id, group_id, inst_hi, inst_lo, offset, size_flags, mem_size, _compression = struct.unpack_from(
                "<IIIIIIII",
                self.donnees,
                curseur
            )

            instance_id = (inst_hi << 32) | inst_lo
            size = size_flags & 0x7FFFFFFF
            compressed = bool(size_flags & 0x80000000)

            self.entrees.append(
                EntreePackage(
                    type_id=type_id,
                    group_id=group_id,
                    instance_id=instance_id,
                    offset=offset,
                    size=size,
                    offset_pos=curseur + 16,
                    size_flags_pos=curseur + 20,
                    mem_size_pos=curseur + 24,
                    compressed=compressed,
                )
            )

            curseur += 32

    def trouver_ressource(self, type_id: int, group_id: int, instance_id: int):
        for entree in self.entrees:
            if (
                entree.type_id == type_id
                and entree.group_id == group_id
                and entree.instance_id == instance_id
            ):
                return entree

        disponibles = [
            f"{e.type_id:08X}!{e.group_id:08X}!{e.instance_id:016X}"
            for e in self.entrees
        ]

        raise ValueError(
            f"Ressource introuvable: {type_id:08X}!{group_id:08X}!{instance_id:016X}\n"
            f"Disponibles: {disponibles}"
        )

    def remplacer_ressource(self, entree: EntreePackage, nouveau_binaire: bytes):
        index_offset = struct.unpack_from("<I", self.donnees, 64)[0]

        debut = entree.offset
        fin = entree.offset + entree.size

        ancienne_taille = entree.size
        nouvelle_taille = len(nouveau_binaire)
        delta = nouvelle_taille - ancienne_taille

        self.donnees = (
            self.donnees[:debut]
            + bytearray(nouveau_binaire)
            + self.donnees[fin:]
        )

        if index_offset > debut:
            index_offset += delta
            struct.pack_into("<I", self.donnees, 64, index_offset)

        for item in self.entrees:
            if item is not entree and item.offset > debut:
                item.offset += delta

            item.offset_pos += delta if item.offset_pos and item.offset_pos > debut else 0
            item.size_flags_pos += delta if item.size_flags_pos and item.size_flags_pos > debut else 0
            item.mem_size_pos += delta if item.mem_size_pos and item.mem_size_pos > debut else 0

        entree.size = nouvelle_taille

        for item in self.entrees:
            if item.offset_pos is not None:
                struct.pack_into("<I", self.donnees, item.offset_pos, item.offset)

            if item.size_flags_pos is not None:
                size_flags = item.size
                if item.compressed:
                    size_flags |= 0x80000000
                struct.pack_into("<I", self.donnees, item.size_flags_pos, size_flags)

            if item.mem_size_pos is not None:
                struct.pack_into("<I", self.donnees, item.mem_size_pos, item.size)

    def sauvegarder(self, chemin_sortie: str):
        Path(chemin_sortie).write_bytes(self.donnees)
