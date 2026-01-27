# DEVELOPMENT.md

## 1. Thiết lập Kaggle API Token

- Vào [Kaggle Settings → Account](https://www.kaggle.com/settings/account).
- Trong mục **API**, chọn **Create New API Token**.
- Tải về file `kaggle.json`.

### Linux/Mac

```bash
mkdir -p ~/.kaggle
mv ~/Downloads/kaggle.json ~/.kaggle/kaggle.json
chmod 600 ~/.kaggle/kaggle.json
```

### Windows

Copy file vào C:\Users\<username>\.kaggle\kaggle.json.
