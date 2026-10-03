# Hồ sơ nộp bài

Đã có benchmark.py, benchmark_result.json, benchmark_output.txt, resource_usage.txt, báo cáo và terraform_source.zip.

Ảnh người dùng chụp nằm trong screenshots/: benchmark-results.png (log kết quả thực từ EC2), ec2-resource-usage.png (log tài nguyên sau benchmark), aws-billing.png (AWS Bills tháng 10/2026). Hai ảnh log được chụp khi mở file trong IDE sau khi EC2 đã được xóa, không phải phiên SSH trực tiếp.

Ảnh Billing hiển thị Pending, tổng USD 0.00 và phần region Singapore USD 3.99; không thể quy chi phí này cho lab us-east-1 hoặc kết luận lab miễn phí. Ảnh chưa hiển thị chi tiết phí EC2/NAT của lab. Billing API của ai-lab-user thiếu quyền ce:GetCostAndUsage.

Không đưa SSH private key, AWS credentials hoặc Terraform state vào file nộp bài. Hạ tầng đã dọn; xem destroy.log và cleanup_verification.txt.
