# Phân tích module chức năng tìm kiếm sản phẩm bằng hình ảnh

Dưới đây là cách **chia module chức năng tìm kiếm sản phẩm bằng hình ảnh (visual product search)** theo **module kỹ thuật**, và mình sẽ **ghi rõ loại model** (CNN / Transformer / ANN / RNN …) **trong ngoặc** như bạn yêu cầu. Cách chia này phản ánh **cách các công ty lớn thực sự triển khai** (Shopee, Lazada, Amazon, Pinterest).

---

## 1️⃣ Image Ingestion & Preprocessing Module

### (không phải model học sâu chính, chỉ xử lý ảnh)

#### Chức năng

- Nhận ảnh người dùng upload / chụp
- Resize, normalize
- Augmentation nhẹ (nếu inference batch)
- Chuẩn hoá input cho model downstream

#### Công nghệ

- OpenCV, Pillow
- TorchVision transforms

➡️ **Module này KHÔNG phải CNN/ANN/RNN**

---

## 2️⃣ Product Detection / Segmentation Module

### (CNN / Transformer)

#### Mục đích - Detection

Chi tiết mục đích bên dưới.

- Ảnh người dùng thường có:
  - Nhiều vật thể
  - Background nhiễu
- Cần xác định **vùng chứa sản phẩm chính**

#### Model phổ biến - Detection

Các model phổ biến được liệt kê bên dưới.

- YOLOv5 / YOLOv8 (**CNN-based detector**)
- Faster R-CNN (**CNN**)
- DETR (**Transformer-based detector**)
- SAM – Segment Anything (**Transformer + ViT**)
- Mask R-CNN (phân vùng chính xác)

#### Input → Output - Detection

- Input: ảnh gốc
- Output: bounding box / mask của sản phẩm

📌 **Ghi chú thực tế**

> Shopee/Lazada **gần như chắc chắn có module này**, nếu không kết quả search sẽ rất tệ.

---

## 3️⃣ Image Feature Extraction / Embedding Module

### (CNN hoặc Vision Transformer)

#### ĐÂY LÀ TRÁI TIM CỦA HỆ THỐNG

#### Mục đích - Embedding

Chi tiết mục đích bên dưới.

- Chuyển ảnh (hoặc crop ảnh sản phẩm) → vector embedding (128–1024 chiều)

#### Model thường dùng - Embedding

Các model thường dùng được liệt kê bên dưới.

- ResNet / EfficientNet (**CNN**)
- Vision Transformer – ViT (**Transformer**)
- DINO / DINOv2 (**Self-supervised ViT**)
- CLIP image encoder (**ViT hoặc CNN backbone**)

#### Output

```text
image → embedding vector (float[])
```

📌 **Thực tế hiện nay**

- Công ty mới → dùng **CLIP / DINOv2**
- Công ty cũ → ResNet + metric learning

---

## 4️⃣ Multimodal Alignment Module (tuỳ chọn nhưng rất phổ biến)

### (Transformer – Contrastive Learning)

#### Mục đích - Multimodal Alignment

Chi tiết mục đích bên dưới.

- Gắn kết **ảnh ↔ text (title, description, category)**

#### Model - Multimodal Alignment

Các model được liệt kê bên dưới.

- CLIP (image encoder + text encoder) (**Transformer**)
- BLIP / ALIGN (**Transformer**)

#### Tác dụng

- Cho phép:
  - Image → Image search
  - Image → Text search
  - Re-rank theo semantic meaning

📌 **Shopee/Lazada gần như chắc chắn dùng CLIP-like model**

---

## 5️⃣ Vector Indexing & Similarity Search Module

### (ANN – Approximate Nearest Neighbor)

⚠️ **ANN ở đây KHÔNG phải neural network**
ANN = _Approximate Nearest Neighbor_

#### Mục đích - Re-ranking

- Tìm nhanh các embedding gần nhất trong hàng triệu sản phẩm

#### Thuật toán

- HNSW (**ANN graph-based**)
- IVF + PQ (**ANN quantization**)

#### Thư viện / hệ thống

- Faiss (**ANN**)
- Milvus (**ANN + Vector DB**)
- ScaNN (**ANN**)
- Elasticsearch

#### Input → Output - ANN

```text
query embedding → top-K nearest embeddings
```

---

## 6️⃣ Candidate Re-ranking Module

### (ML truyền thống / Light DL / đôi khi Transformer)

#### Mục đích - On-device

- ANN chỉ cho “gần về mặt vector”
- Cần sắp xếp lại theo **logic kinh doanh**

#### Feature đầu vào

- Vector similarity score
- Giá, brand, category
- Popularity, CTR
- Text similarity (title)

### Filter: Pandas/Numpy

#### Model - Re-ranking

- Gradient Boosting (XGBoost, LightGBM) (**ML truyền thống**)
- MLP nhỏ (**Feed-forward NN**)
- Cross-encoder Transformer (**Transformer**, nếu rất cao cấp)

---

## 7️⃣ OCR & Attribute Extraction Module (tuỳ sản phẩm)

### (CNN / Transformer / CRNN)

#### Khi nào cần

- Sản phẩm có chữ:
  - Logo
  - Nhãn
  - Model number

#### Model - OCR

- CRNN (**CNN + RNN**)
- Transformer OCR (TrOCR) (**Transformer**)

➡️ Dùng để boost re-ranking, KHÔNG phải core search

---

## 8️⃣ Feedback Loop & Online Learning Module

### (ML system, không phải model cụ thể)

#### Mục đích - Feedback

- Thu thập:
  - Click
  - Add-to-cart
  - Purchase

- Fine-tune embedding / re-ranking model

#### Kỹ thuật

- Offline retraining
- Hard negative mining
- A/B testing

---

## 9️⃣ (Tuỳ chọn) On-device Inference Module

### (CNN / ViT lightweight)

#### Mục đích

- Giảm latency
- Privacy

#### Model - On-device

- MobileNetV3 (**CNN**)
- EfficientNet-Lite (**CNN**)
- Quantized ViT (**Transformer**)

---

## 🔎 TÓM TẮT TOÀN BỘ PIPELINE (rất quan trọng)

```text
Ảnh người dùng
 → Preprocessing
 → Detection / Segmentation (CNN / Transformer)
 → Embedding extraction (CNN / ViT)
 → (Multimodal alignment – CLIP) (Transformer)
 → ANN search (ANN)
 → Re-ranking (ML / Transformer)
 → Kết quả sản phẩm
```

---

## 🎯 Nếu bạn làm project ML/DL (sinh viên AI)

### Khuyến nghị học & làm theo thứ tự

1. Embedding + ANN search (**bắt buộc**)
2. CLIP (image encoder) (**rất nên**)
3. YOLO (detection)
4. Faiss / Milvus (ANN)
5. Re-ranking đơn giản
