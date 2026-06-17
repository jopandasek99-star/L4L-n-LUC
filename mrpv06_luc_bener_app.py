# ==========================================
    # CORE PROCESSING MATHEMATICAL ALGORITHMS
    # ==========================================
    def calculate_multi_mrp(demands, s_receipts, setup, hold, init_inv, ss, lt, f_lot, moq_val, fpr_interval, build_trace=True):
        n = len(demands)
        
        # =========================================================================
        # FIX LOGIC: Net Requirements Matrix Modifikasi (NR = 0 saat stok cukup)
        # =========================================================================
        net_req = []
        prev_inv = init_inv
        
        for i in range(n):
            available_stock = prev_inv + s_receipts[i]
            
            # Hitung apakah stok yang tersedia cukup untuk Gross Demand + Safety Stock
            if available_stock >= (demands[i] + ss):
                # Stok cukup -> Tidak ada kebutuhan bersih (NR = 0)
                net_req.append(0)
                # Sisa stok dikurangi demand periode ini
                prev_inv = available_stock - demands[i]
            else:
                # Stok kurang -> Hitung kekurangan riil sebagai Net Requirement
                net_val = (demands[i] + ss) - available_stock
                net_req.append(net_val)
                # Karena kurang, sisa stok riil sebelum barang pesanan (Receipt) datang diset ke level Safety Stock
                prev_inv = ss

        # ==========================================
        # generate_poh_and_release — return 3 nilai
        # (Tetap mempertahankan fungsi asli bawaan lo)
        # ==========================================
        def generate_poh_and_release(rec_lot, moq_v=0):
            # Step 1: terapkan MOQ per order
            actual_rec = []
            for i in range(n):
                raw = rec_lot[i]
                actual = max(raw, moq_v) if (moq_v > 0 and raw > 0) else raw
                actual_rec.append(actual)

            # Step 2: hitung POH dari actual_rec
            poh = []
            r_inv = init_inv
            for i in range(n):
                r_inv += s_receipts[i] + actual_rec[i] - demands[i]
                poh.append(r_inv)

            # Step 3: release planning dari actual_rec
            rel_lot = [0] * n
            for i in range(n):
                if actual_rec[i] > 0:
                    target = i - lt
                    rel_lot[max(0, target)] += actual_rec[i]

            return poh, rel_lot, actual_rec
