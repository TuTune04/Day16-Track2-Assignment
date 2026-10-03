# Báo cáo Lab 16 — AWS CPU LightGBM

1. Thực hiện trên EC2 t3.medium (2 vCPU, 4 GB RAM), region us-east-1; timestamp UTC: 2026-10-03T19:44:14.323376+00:00.
2. Dataset Kaggle mlg-ulb/creditcardfraud có 284,807 giao dịch và 492 giao dịch gian lận; tải qua endpoint công khai, không cần token.
3. Tách stratified với seed 42: train 182,276, validation 45,569, test 56,962; test không tham gia early stopping.
4. Load data 2.347 giây; training 2.356 giây; early stopping theo validation AUC chọn iteration 1.
5. Test AUC-ROC 0.939058, Accuracy 0.999210, F1 0.769231.
6. Precision 0.773196, Recall 0.765306 tại threshold 0.5. Accuracy cao do dữ liệu mất cân bằng, cần xem AUC/F1/Recall cùng nhau.
7. Median inference 1 dòng 1.157 ms; p95 1.959 ms.
8. Batch 1000 dòng mất 1.463 ms, tương đương 683,577 dòng/giây; đo sau warmup, gồm overhead Python; model chỉ có 1 iteration nên throughput cao.
9. Log top/free/ip được thu ngay sau benchmark; không dùng để kết luận CPU peak trong lúc training. Toàn bộ training/inference chạy trên EC2.
10. Billing API bị AccessDenied (thiếu ce:GetCostAndUsage); người dùng đã bổ sung 3 ảnh trong screenshots/. Ảnh Bills đang Pending, chưa xác nhận chi phí EC2/NAT riêng của lab us-east-1.
