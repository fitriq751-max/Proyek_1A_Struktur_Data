
"""
PROYEK 1B STRUKTUR DATA
SISTEM MANAJEMEN SILSILAH ORGANISASI

Struktur data : General Tree
Bahasa        : Python
Konsep        : Object-Oriented Programming (OOP)

Catatan:
Preorder dan postorder mengikuti aturan General Tree.
Inorder menggunakan aturan khusus untuk General Tree:
anak pertama -> node -> anak-anak berikutnya.
Inorder standar umumnya didefinisikan untuk Binary Tree.
"""


# ==================================================
# 1. KELAS NODE
# ==================================================

class Node:
    def __init__(self, id_pegawai, nama, jabatan):
        self.id_pegawai = str(id_pegawai)
        self.nama = nama
        self.jabatan = jabatan
        self.children = []

    def __str__(self):
        return (
            f"ID: {self.id_pegawai} | "
            f"Nama: {self.nama} | "
            f"Jabatan: {self.jabatan}"
        )


# ==================================================
# 2. KELAS TREE
# ==================================================

class Tree:
    def __init__(self):
        self.root = None

    # ----------------------------------------------
    # INSERT NODE: menambahkan pegawai
    # ----------------------------------------------
    def insert_node(
        self, id_pegawai, nama, jabatan, id_atasan=None
    ):
        if not id_pegawai or not nama or not jabatan:
            print("Gagal: ID, nama, dan jabatan wajib diisi.")
            return False

        id_pegawai = str(id_pegawai).strip()
        nama = nama.strip()
        jabatan = jabatan.strip()

        if not id_pegawai or not nama or not jabatan:
            print("Gagal: data tidak boleh kosong.")
            return False

        if self.root is None:
            if id_atasan is not None:
                print("Gagal: tambahkan root terlebih dahulu.")
                return False

            self.root = Node(id_pegawai, nama, jabatan)
            print("Root berhasil ditambahkan.")
            return True

        if self.search_by_id(id_pegawai) is not None:
            print("Gagal: ID pegawai sudah digunakan.")
            return False

        if id_atasan is None:
            print("Gagal: ID atasan harus diisi.")
            return False

        atasan = self.search_by_id(id_atasan)

        if atasan is None:
            print("Gagal: data atasan tidak ditemukan.")
            return False

        node_baru = Node(id_pegawai, nama, jabatan)
        atasan.children.append(node_baru)

        print(
            f"Pegawai {nama} berhasil ditambahkan "
            f"di bawah {atasan.nama}."
        )
        return True

    # ----------------------------------------------
    # SEARCH BERDASARKAN ID
    # ----------------------------------------------
    def search_by_id(self, id_pegawai):
        if self.root is None:
            return None

        target = str(id_pegawai).strip()
        stack = [self.root]

        while stack:
            node = stack.pop()

            if node.id_pegawai == target:
                return node

            stack.extend(reversed(node.children))

        return None

    # ----------------------------------------------
    # SEARCH NODE: berdasarkan nama atau jabatan
    # ----------------------------------------------
    def search_node(self, kata_kunci):
        hasil = []

        if self.root is None or not kata_kunci.strip():
            return hasil

        kata_kunci = kata_kunci.strip().casefold()
        stack = [self.root]

        while stack:
            node = stack.pop()

            if (
                kata_kunci in node.nama.casefold()
                or kata_kunci in node.jabatan.casefold()
            ):
                hasil.append(node)

            stack.extend(reversed(node.children))

        return hasil

    # ----------------------------------------------
    # PREORDER: node -> anak-anak
    # ----------------------------------------------
    def preorder_traversal(self, node=None, hasil=None):
        if hasil is None:
            hasil = []

        if node is None:
            node = self.root

        if node is None:
            return hasil

        hasil.append(node)

        for anak in node.children:
            self.preorder_traversal(anak, hasil)

        return hasil

    # ----------------------------------------------
    # INORDER KHUSUS GENERAL TREE:
    # anak pertama -> node -> anak berikutnya
    # ----------------------------------------------
    def inorder_traversal(self, node=None, hasil=None):
        if hasil is None:
            hasil = []

        if node is None:
            node = self.root

        if node is None:
            return hasil

        if node.children:
            self.inorder_traversal(node.children[0], hasil)

        hasil.append(node)

        for anak in node.children[1:]:
            self.inorder_traversal(anak, hasil)

        return hasil

    # ----------------------------------------------
    # POSTORDER: anak-anak -> node
    # ----------------------------------------------
    def postorder_traversal(self, node=None, hasil=None):
        if hasil is None:
            hasil = []

        if node is None:
            node = self.root

        if node is None:
            return hasil

        for anak in node.children:
            self.postorder_traversal(anak, hasil)

        hasil.append(node)

        return hasil

    # ----------------------------------------------
    # MENAMPILKAN STRUKTUR TREE
    # ----------------------------------------------
    def tampilkan_struktur(self, node=None, level=0):
        if node is None:
            node = self.root

        if node is None:
            print("Struktur organisasi masih kosong.")
            return

        print(
            "    " * level
            + f"|-- {node.nama} ({node.jabatan}) "
            + f"[{node.id_pegawai}]"
        )

        for anak in node.children:
            self.tampilkan_struktur(anak, level + 1)


# ==================================================
# 3. DATA CONTOH ORGANISASI
# ==================================================

def buat_data_contoh():
    organisasi = Tree()

    organisasi.insert_node(
        "ORG001", "Dr. Ahmad", "Rektor"
    )

    organisasi.insert_node(
        "ORG002", "Dr. Siti", "Dekan FST", "ORG001"
    )

    organisasi.insert_node(
        "ORG003", "Dr. Budi",
        "Dekan Fakultas Tarbiyah", "ORG001"
    )

    organisasi.insert_node(
        "ORG004", "M. Rafi",
        "Ketua Prodi Teknik Informatika", "ORG002"
    )

    organisasi.insert_node(
        "ORG005", "Nadia Putri",
        "Ketua Prodi Sistem Informasi", "ORG002"
    )

    organisasi.insert_node(
        "ORG006", "Andi Saputra",
        "Dosen Teknik Informatika", "ORG004"
    )

    organisasi.insert_node(
        "ORG007", "Dewi Lestari",
        "Staf Fakultas Tarbiyah", "ORG003"
    )

    return organisasi


# ==================================================
# 4. MENAMPILKAN HASIL TRAVERSAL
# ==================================================

def tampilkan_traversal(judul, daftar_node):
    print(f"\n{judul}")

    if not daftar_node:
        print("Tidak ada data.")
        return

    for nomor, node in enumerate(daftar_node, start=1):
        print(
            f"{nomor}. {node.nama} - {node.jabatan}"
        )


# ==================================================
# 5. MENU PROGRAM
# ==================================================

def main():
    organisasi = buat_data_contoh()

    while True:
        print("\n" + "=" * 52)
        print(" SISTEM MANAJEMEN SILSILAH ORGANISASI")
        print("=" * 52)
        print("1. Tampilkan struktur organisasi")
        print("2. Tambah pegawai atau jabatan")
        print("3. Cari pegawai")
        print("4. Preorder Traversal")
        print("5. Inorder Traversal")
        print("6. Postorder Traversal")
        print("7. Tampilkan semua traversal")
        print("8. Keluar")
        print("=" * 52)

        pilihan = input("Pilih menu (1-8): ").strip()

        if pilihan == "1":
            print("\nSTRUKTUR ORGANISASI")
            organisasi.tampilkan_struktur()

        elif pilihan == "2":
            print("\nTAMBAH PEGAWAI/JABATAN")

            id_pegawai = input("ID pegawai: ").strip()
            nama = input("Nama pegawai: ").strip()
            jabatan = input("Jabatan: ").strip()
            id_atasan = input(
                "ID atasan (kosongkan hanya jika membuat root): "
            ).strip()

            organisasi.insert_node(
                id_pegawai,
                nama,
                jabatan,
                id_atasan if id_atasan else None
            )

        elif pilihan == "3":
            kata_kunci = input(
                "Masukkan nama atau jabatan: "
            ).strip()

            hasil = organisasi.search_node(kata_kunci)

            if hasil:
                print(f"\nDitemukan {len(hasil)} hasil:")

                for node in hasil:
                    print(node)
            else:
                print("Data pegawai tidak ditemukan.")

        elif pilihan == "4":
            tampilkan_traversal(
                "HASIL PREORDER TRAVERSAL",
                organisasi.preorder_traversal()
            )

        elif pilihan == "5":
            tampilkan_traversal(
                "HASIL INORDER TRAVERSAL "
                "(ATURAN KHUSUS GENERAL TREE)",
                organisasi.inorder_traversal()
            )

        elif pilihan == "6":
            tampilkan_traversal(
                "HASIL POSTORDER TRAVERSAL",
                organisasi.postorder_traversal()
            )

        elif pilihan == "7":
            tampilkan_traversal(
                "PREORDER TRAVERSAL",
                organisasi.preorder_traversal()
            )

            tampilkan_traversal(
                "INORDER TRAVERSAL "
                "(ATURAN KHUSUS GENERAL TREE)",
                organisasi.inorder_traversal()
            )

            tampilkan_traversal(
                "POSTORDER TRAVERSAL",
                organisasi.postorder_traversal()
            )

        elif pilihan == "8":
            print("Program selesai. Terima kasih.")
            break

        else:
            print("Pilihan tidak valid. Masukkan angka 1-8.")


if __name__ == "__main__":
    main()
