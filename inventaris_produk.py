"""
PROYEK 1A STRUKTUR DATA
Sistem Manajemen Inventaris Produk

Struktur data utama: Python dict (hash table).
Struktur pembanding: Python list dan Linked List buatan sendiri.

Kompleksitas rata-rata yang diharapkan:
- dict: tambah O(1), cari berdasarkan ID O(1), hapus berdasarkan ID O(1)
- list: tambah di akhir O(1) amortized, cari O(n), hapus berdasarkan ID O(n)
- linked list: tambah di awal O(1), cari O(n), hapus berdasarkan ID O(n)
Catatan: operasi dict dapat menjadi O(n) pada kasus terburuk karena collision.
"""

import time
import statistics


# ============================================================
# 1. LINKED LIST CUSTOM (UNTUK PEMBANDING)
# ============================================================

class Node:
    """Satu simpul pada Linked List."""
    def __init__(self, id_produk, data_produk):
        self.id_produk = id_produk
        self.data_produk = data_produk
        self.next = None


class LinkedListProduk:
    """ADT Linked List sederhana untuk menyimpan produk."""
    def __init__(self):
        self.head = None
        self.jumlah = 0

    def tambah_produk(self, id_produk, data_produk):
        """Menambahkan produk di awal Linked List: O(1)."""
        node_baru = Node(id_produk, data_produk)
        node_baru.next = self.head
        self.head = node_baru
        self.jumlah += 1
        return True

    def cari_produk(self, id_produk):
        """Mencari produk berdasarkan ID: O(n)."""
        sekarang = self.head
        while sekarang is not None:
            if sekarang.id_produk == id_produk:
                return sekarang.data_produk
            sekarang = sekarang.next
        return None

    def hapus_produk(self, id_produk):
        """Menghapus produk berdasarkan ID: O(n) karena harus mencari node."""
        sebelumnya = None
        sekarang = self.head

        while sekarang is not None:
            if sekarang.id_produk == id_produk:
                if sebelumnya is None:
                    self.head = sekarang.next
                else:
                    sebelumnya.next = sekarang.next
                self.jumlah -= 1
                return sekarang.data_produk

            sebelumnya = sekarang
            sekarang = sekarang.next

        return None

    def kosong(self):
        return self.head is None

    def tampilkan_semua(self):
        sekarang = self.head
        while sekarang is not None:
            yield sekarang.id_produk, sekarang.data_produk
            sekarang = sekarang.next


# ============================================================
# 2. ADT INVENTARIS UTAMA MENGGUNAKAN DICT
# ============================================================

class InventarisProduk:
    """
    ADT inventaris dengan dict sebagai struktur data utama.
    Key dict adalah ID produk agar produk mudah ditemukan.
    """

    def __init__(self):
        self.produk = {}

    def tambah_produk(self, id_produk, nama, harga, stok):
        """Menyisipkan produk. Kompleksitas rata-rata: O(1)."""
        if id_produk in self.produk:
            return False, "ID produk sudah terdaftar."

        self.produk[id_produk] = {
            "nama": nama,
            "harga": harga,
            "stok": stok
        }
        return True, "Produk berhasil ditambahkan."

    def cari_produk(self, id_produk):
        """Mencari produk berdasarkan ID. Kompleksitas rata-rata: O(1)."""
        return self.produk.get(id_produk)

    def hapus_produk(self, id_produk):
        """Menghapus produk berdasarkan ID. Kompleksitas rata-rata: O(1)."""
        return self.produk.pop(id_produk, None)

    def tampilkan_produk(self):
        if not self.produk:
            print("Inventaris masih kosong.")
            return

        print("\n=== DAFTAR INVENTARIS PRODUK ===")
        for id_produk, data in self.produk.items():
            print(
                f"ID: {id_produk} | Nama: {data['nama']} | "
                f"Harga: Rp{data['harga']:,.2f} | Stok: {data['stok']}"
            )


# ============================================================
# 3. OPERASI LIST UNTUK BENCHMARK
# ============================================================

def cari_produk_list(data_list, id_produk):
    for produk in data_list:
        if produk["id"] == id_produk:
            return produk
    return None


def hapus_produk_list(data_list, id_produk):
    for indeks, produk in enumerate(data_list):
        if produk["id"] == id_produk:
            return data_list.pop(indeks)
    return None


# ============================================================
# 4. FUNGSI BANTU BENCHMARK
# ============================================================

def median_waktu(fungsi, percobaan=5):
    """Mengembalikan median waktu operasi dalam detik."""
    hasil = []
    for _ in range(percobaan):
        mulai = time.perf_counter()
        fungsi()
        selesai = time.perf_counter()
        hasil.append(selesai - mulai)
    return statistics.median(hasil)


def median_waktu_dengan_persiapan(persiapan, operasi, percobaan=5):
    """
    Menyiapkan salinan data di luar waktu yang diukur.
    Yang diukur hanya operasi yang diberikan pada parameter operasi.
    """
    hasil = []
    for _ in range(percobaan):
        data = persiapan()
        mulai = time.perf_counter()
        operasi(data)
        selesai = time.perf_counter()
        hasil.append(selesai - mulai)
    return statistics.median(hasil)


def buat_data_list(jumlah):
    return [
        {
            "id": f"PRD{i:06d}",
            "nama": f"Produk {i}",
            "harga": 1000.0 + i,
            "stok": 10
        }
        for i in range(jumlah)
    ]


def buat_data_dict(data_list):
    return {
        produk["id"]: {
            "nama": produk["nama"],
            "harga": produk["harga"],
            "stok": produk["stok"]
        }
        for produk in data_list
    }


def buat_linked_list(data_list):
    linked = LinkedListProduk()
    # Dibalik agar urutan ID di Linked List sama dengan urutan data sumber.
    for produk in reversed(data_list):
        data = {
            "nama": produk["nama"],
            "harga": produk["harga"],
            "stok": produk["stok"]
        }
        linked.tambah_produk(produk["id"], data)
    return linked


def benchmark():
    """Membandingkan waktu tambah, cari, dan hapus untuk list, Linked List, dict."""
    print("\n=== BENCHMARK: LIST vs LINKED LIST vs DICT ===")
    print("Waktu dalam detik; median dari 5 percobaan.")
    print("Persiapan/salinan data tidak dimasukkan ke waktu operasi.")
    print("Pencarian dan penghapusan menguji ID terakhir (kasus pencarian panjang).\n")

    # Ukuran dibatasi agar pengujian masih wajar di laptop mahasiswa.
    for n in (1000, 10000, 50000):
        sumber_list = buat_data_list(n)
        sumber_dict = buat_data_dict(sumber_list)
        target = f"PRD{n - 1:06d}"
        id_baru = f"PRD{n:06d}"

        produk_list_baru = {
            "id": id_baru,
            "nama": "Produk Baru",
            "harga": 25000.0,
            "stok": 5
        }
        produk_dict_baru = {
            "nama": "Produk Baru",
            "harga": 25000.0,
            "stok": 5
        }

        # PENCARIAN
        cari_list = median_waktu(
            lambda: cari_produk_list(sumber_list, target)
        )
        cari_linked = median_waktu_dengan_persiapan(
            lambda: buat_linked_list(sumber_list),
            lambda data: data.cari_produk(target)
        )
        cari_dict = median_waktu(
            lambda: sumber_dict.get(target)
        )

        # PENYISIPAN
        sisip_list = median_waktu_dengan_persiapan(
            lambda: sumber_list.copy(),
            lambda data: data.append(produk_list_baru.copy())
        )
        sisip_linked = median_waktu_dengan_persiapan(
            lambda: buat_linked_list(sumber_list),
            lambda data: data.tambah_produk(id_baru, produk_dict_baru.copy())
        )
        sisip_dict = median_waktu_dengan_persiapan(
            lambda: sumber_dict.copy(),
            lambda data: data.__setitem__(id_baru, produk_dict_baru.copy())
        )

        # PENGHAPUSAN
        hapus_list = median_waktu_dengan_persiapan(
            lambda: sumber_list.copy(),
            lambda data: hapus_produk_list(data, target)
        )
        hapus_linked = median_waktu_dengan_persiapan(
            lambda: buat_linked_list(sumber_list),
            lambda data: data.hapus_produk(target)
        )
        hapus_dict = median_waktu_dengan_persiapan(
            lambda: sumber_dict.copy(),
            lambda data: data.pop(target, None)
        )

        print(f"JUMLAH DATA: {n:,}")
        print(f"{'Operasi':<14}{'Python list':>16}{'Linked List':>16}{'dict':>16}")
        print("-" * 62)
        print(f"{'Pencarian':<14}{cari_list:>16.9f}{cari_linked:>16.9f}{cari_dict:>16.9f}")
        print(f"{'Penyisipan':<14}{sisip_list:>16.9f}{sisip_linked:>16.9f}{sisip_dict:>16.9f}")
        print(f"{'Penghapusan':<14}{hapus_list:>16.9f}{hapus_linked:>16.9f}{hapus_dict:>16.9f}")
        print("-" * 62)

    print("\nCatatan: hasil waktu dapat berbeda tergantung spesifikasi laptop.")
    print("Gunakan hasil yang benar-benar tampil sebagai data laporan.")


# ============================================================
# 5. MENU COMMAND LINE INTERFACE
# ============================================================

def main():
    inventaris = InventarisProduk()

    while True:
        print("\n=== SISTEM MANAJEMEN INVENTARIS PRODUK ===")
        print("1. Tambah produk")
        print("2. Cari produk berdasarkan ID")
        print("3. Hapus produk berdasarkan ID")
        print("4. Tampilkan semua produk")
        print("5. Bandingkan list, Linked List, dan dict")
        print("6. Keluar")

        pilihan = input("Pilih menu (1-6): ").strip()

        if pilihan == "1":
            id_produk = input("ID Produk: ").strip()
            nama = input("Nama Produk: ").strip()

            try:
                harga = float(input("Harga Produk: "))
                stok = int(input("Stok Produk: "))

                if not id_produk or not nama:
                    print("ID dan nama produk tidak boleh kosong.")
                elif harga < 0 or stok < 0:
                    print("Harga dan stok tidak boleh negatif.")
                else:
                    berhasil, pesan = inventaris.tambah_produk(
                        id_produk, nama, harga, stok
                    )
                    print(pesan)
            except ValueError:
                print("Input tidak valid. Harga harus angka dan stok bilangan bulat.")

        elif pilihan == "2":
            id_produk = input("Masukkan ID yang dicari: ").strip()
            data = inventaris.cari_produk(id_produk)

            if data is None:
                print("Produk tidak ditemukan.")
            else:
                print("\n=== DETAIL PRODUK ===")
                print("ID Produk :", id_produk)
                print("Nama      :", data["nama"])
                print(f"Harga     : Rp{data['harga']:,.2f}")
                print("Stok      :", data["stok"])

        elif pilihan == "3":
            id_produk = input("Masukkan ID yang dihapus: ").strip()
            data = inventaris.hapus_produk(id_produk)

            if data is None:
                print("Produk tidak ditemukan.")
            else:
                print(f"Produk '{data['nama']}' berhasil dihapus.")

        elif pilihan == "4":
            inventaris.tampilkan_produk()

        elif pilihan == "5":
            benchmark()

        elif pilihan == "6":
            print("Program selesai. Terima kasih.")
            break

        else:
            print("Pilihan tidak valid. Silakan pilih 1-6.")


if __name__ == "__main__":
    main()
